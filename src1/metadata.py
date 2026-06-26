from typing import List
from langchain_core.documents import Document

from src1.model import client, model
from azure.ai.inference.models import (
    SystemMessage,
    UserMessage
)


def describe_page(text: str) -> str:
    """
    Generate page summary using LLM.
    """

    # avoid huge prompts
    text = text[:1500]

    if len(text.strip()) < 100:
        clean = " ".join(text.replace("\n", " ").split())
        if not clean:
            return "Empty or OCR-unreadable page"
        words = clean.split()[:10]
        return words

    response = client.complete(
        messages=[
            SystemMessage(
                "You summarize PDF pages in one concise sentence."
            ),

            UserMessage(
                f"Summarize this page:\n\n{text}"
            ),
        ],
        temperature=0.3,
        top_p=1.0,
        model=model
    )

    return response.choices[0].message.content


def add_page_descriptions(docs: List[Document]) -> List[Document]:
    """
    Add LLM-generated page descriptions.
    """
    for doc in docs:

        summary = describe_page(doc.page_content)

        doc.metadata["page_description"] = summary

    return docs