import json, pathlib
from src.llm.providers import OpenAIProvider
from src.schemas.models import SummarizeRequest, SummaryResult
from src.utils.cost_tracker import estimate_cost, Usage
from src.storage.db import log_llm_usage

_PROMPT = (pathlib.Path(__file__).parent.parent / "prompts" / "summarizer.txt").read_text(encoding="utf-8")

def summarize(req: SummarizeRequest) -> SummaryResult:
    provider = OpenAIProvider()
    system = _PROMPT.format(max_tokens=req.max_tokens, language=req.language)
    user = f"TEXT:\n{req.text.strip()}\n\nSOURCES: {json.dumps(req.sources or [], ensure_ascii=False)}"

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user}
    ]
    resp = provider.chat(messages, response_format={"type": "json_object"})
    usage = Usage(
        prompt_tokens=resp["usage"]["prompt_tokens"],
        completion_tokens=resp["usage"]["completion_tokens"],
        model=provider.model
    )
    cost = estimate_cost(usage)

    try:
        data = json.loads(resp["content"])
    except Exception:
        data = {"title": "", "summary": resp["content"], "bullet_points": [], "sources": req.sources or []}

    result = SummaryResult(
        title=data.get("title", ""),
        summary=data.get("summary", ""),
        bullet_points=data.get("bullet_points", []),
        sources=data.get("sources", req.sources or [])
    )
    # log
    log_llm_usage(model=provider.model,
                  prompt_tokens=usage.prompt_tokens,
                  completion_tokens=usage.completion_tokens,
                  total_tokens=usage.prompt_tokens+usage.completion_tokens,
                  cost_usd=cost,
                  input_preview=req.text[:500],
                  output_preview=result.summary[:500])
    return result
