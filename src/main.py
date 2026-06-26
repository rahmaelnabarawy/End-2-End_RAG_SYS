from src.loaders import load_pdf_pages
from src.metadata import add_page_descriptions

FILE_PATH = "data/raw/andrew-ng-machine-learning-yearning.pdf"

docs = load_pdf_pages(FILE_PATH)

print(f"Total pages: {len(docs)}")

print(docs[0].page_content[:500])

print(docs[0].metadata)

docs = docs[15:17]

docs = add_page_descriptions(docs)

for doc in docs:
    print(doc.metadata)
