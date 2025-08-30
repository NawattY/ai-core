import json
from src.llm.providers import OpenAIProvider
from src.storage.vector.pgvector_store import search_similar
from src.schemas.models import QARequest, QAResult

SYSTEM = "You are a retrieval-augmented QA assistant. Answer in Thai if the user query is Thai; otherwise answer in the query language. Keep answers concise (<120 words)."

def qa(req: QARequest) -> QAResult:
    provider = OpenAIProvider()
    q_emb = provider.embed([req.query])[0]
    docs = search_similar(q_emb, top_k=req.top_k)
    context = "\n\n".join([d[1] for d in docs])
    sources = [d[3] for d in docs if d[3]]

    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": f"QUERY:\n{req.query}\n\nCONTEXT:\n{context}\n\nReturn JSON with keys: answer, references (unique urls). If context is not enough, say 'ไม่พบข้อมูลเพียงพอ'."}
    ]
    resp = provider.chat(messages, response_format={"type": "json_object"})
    try:
        data = json.loads(resp["content"])
        ans = data.get("answer", "")
        refs = data.get("references", []) or list(dict.fromkeys(sources))
    except Exception:
        ans = resp["content"]
        refs = list(dict.fromkeys(sources))

    return QAResult(answer=ans, references=refs)
