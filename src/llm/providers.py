from typing import Dict, Any, List
from openai import OpenAI
from src.config import settings

class OpenAIProvider:
    def __init__(self, model: str | None = None):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = model or settings.LLM_MODEL

    def chat(self, messages: List[Dict[str, str]], response_format: Dict[str, Any] | None = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {"model": self.model, "messages": messages}
        if response_format:
            params["response_format"] = response_format
        resp = self.client.chat.completions.create(**params)
        choice = resp.choices[0]
        return {
            "content": choice.message.content,
            "usage": {
                "prompt_tokens": getattr(resp.usage, "prompt_tokens", 0),
                "completion_tokens": getattr(resp.usage, "completion_tokens", 0),
                "total_tokens": getattr(resp.usage, "total_tokens", 0),
            }
        }

    def embed(self, texts: List[str]) -> List[List[float]]:
        emb_model = settings.VECTOR_EMBEDDING_MODEL
        resp = self.client.embeddings.create(model=emb_model, input=texts)
        return [d.embedding for d in resp.data]
