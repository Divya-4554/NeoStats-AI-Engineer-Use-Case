# utils/rag.py
from typing import List
from config.config import settings
from models.embeddings import get_embeddings_client

# Correct new import for text splitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain.docstore.document import Document

try:
    from langchain.vectorstores import FAISS
except Exception:
    FAISS = None


def chunk_documents(text: str) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP
    )
    chunks = splitter.split_text(text)
    docs = [Document(page_content=c) for c in chunks]
    return docs


def build_faiss_index_from_texts(texts: List[str]):
    if FAISS is None:
        raise RuntimeError("FAISS vectorstore not available. Install langchain and faiss-cpu.")

    embeddings = get_embeddings_client()
    docs = []
    for t in texts:
        docs.extend(chunk_documents(t))

    vs = FAISS.from_documents(docs, embeddings)
    return vs


def retrieve_from_index(vs, query: str, k: int = 4):
    results = vs.similarity_search_with_score(query, k=k)
    return results

