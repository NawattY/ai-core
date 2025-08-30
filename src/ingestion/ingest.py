from typing import Iterable, List, Dict
from uuid import uuid4
from src.llm.providers import OpenAIProvider
from src.storage.vector.pgvector_store import upsert_document

def simple_split(text: str, chunk_size: int = 1200, overlap: int = 200) -> List[str]:
    chunks = []
    i = 0
    while i < len(text):
        chunks.append(text[i:i+chunk_size])
        i += max(1, chunk_size - overlap)
    return chunks

def ingest_texts(texts_with_meta: Iterable[Dict]):
    # texts_with_meta: [{"text":..., "source":..., "doc_id":optional}]
    provider = OpenAIProvider()
    for item in texts_with_meta:
        text = item["text"]
        source = item.get("source", "")
        doc_id = item.get("doc_id") or str(uuid4())
        for idx, chunk in enumerate(simple_split(text)):
            emb = provider.embed([chunk])[0]
            upsert_document(doc_id=f"{doc_id}:{idx}", content=chunk, source=source, embedding=emb)
