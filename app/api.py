import sys
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
import shutil

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.pipeline import ingest_pdf_to_faiss
from src.embeddings import get_embeddings
from src.vectorstore import load_faiss
from src.llm_qwen import QwenLLM
from src.rag_chain import answer_question

DATA_RAW_DIR = ROOT / "data" / "raw"
INDEX_DIR = ROOT / "vectorstore" / "faiss_index"

DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
INDEX_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="Qwen PDF RAG API",
    description="Upload PDF, build FAISS index, and ask questions using Qwen.",
    version="1.0.0"
)


class AskRequest(BaseModel):
    question: str
    k: int = 5
    model_name: str = "Qwen/Qwen2.5-0.5B-Instruct"


@app.get("/")
def home():
    return {"message": "Qwen PDF RAG API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(...),
    use_ocr: bool = Form(True)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    pdf_path = DATA_RAW_DIR / file.filename

    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    stats = ingest_pdf_to_faiss(
        str(pdf_path),
        INDEX_DIR,
        use_ocr_if_needed=use_ocr
    )

    return {
        "message": "PDF uploaded and FAISS index created successfully",
        "filename": file.filename,
        "pages": stats["pages"],
        "chunks": stats["chunks"],
        "index_dir": str(INDEX_DIR)
    }


@app.post("/ask")
def ask_question(request: AskRequest):
    if not INDEX_DIR.exists():
        raise HTTPException(status_code=404, detail="FAISS index not found. Upload PDF first.")

    embeddings = get_embeddings()
    vectorstore = load_faiss(INDEX_DIR, embeddings)

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": request.k}
    )

    llm = QwenLLM(model_name=request.model_name)

    answer, docs = answer_question(
        llm,
        retriever,
        request.question
    )

    sources = []
    for doc in docs:
        sources.append({
            "source": doc.metadata.get("source"),
            "page_number": doc.metadata.get("page_number"),
            "page_description": doc.metadata.get("page_description"),
            "content_preview": doc.page_content[:1500]
        })

    return {
        "question": request.question,
        "answer": answer,
        "sources": sources
    }