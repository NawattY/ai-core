from fastapi import FastAPI
from src.schemas.models import SummarizeRequest, SummaryResult, QARequest, QAResult
from src.chains.summarizer import summarize
from src.chains.rag import qa

app = FastAPI(title="ai-core", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/summarize", response_model=SummaryResult)
def do_summarize(req: SummarizeRequest):
    return summarize(req)

@app.post("/qa", response_model=QAResult)
def do_qa(req: QARequest):
    return qa(req)
