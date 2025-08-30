from typing import List, Tuple
from sqlalchemy import text
from src.storage.db import engine

def upsert_document(doc_id: str, content: str, source: str, embedding: List[float]):
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO documents (doc_id, content, source, embedding)
            VALUES (:doc_id, :content, :source, :embedding)
            ON CONFLICT (doc_id, source) DO UPDATE
            SET content = EXCLUDED.content, embedding = EXCLUDED.embedding
        """), dict(doc_id=doc_id, content=content, source=source, embedding=embedding))

def search_similar(query_embedding: List[float], top_k: int = 4) -> List[Tuple[str, str, float, str]]:
    # returns list of (doc_id, content, score, source)
    with engine.begin() as conn:
        res = conn.execute(text("""
            SELECT doc_id, content, 1 - (embedding <=> :q) AS score, source
            FROM documents
            ORDER BY embedding <=> :q
            LIMIT :k
        """), dict(q=query_embedding, k=top_k)).all()
    return [(r[0], r[1], float(r[2]), r[3]) for r in res]
