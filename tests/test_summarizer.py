from src.schemas.models import SummarizeRequest
from src.chains.summarizer import summarize

def test_import_only():
    # Smoke test for import; actual LLM call requires valid API key
    assert SummarizeRequest
