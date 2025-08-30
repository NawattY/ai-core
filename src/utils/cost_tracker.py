from dataclasses import dataclass

MODEL_PRICING = {
    "gpt-4o-mini": {"input_per_1k": 0.0005, "output_per_1k": 0.0015},
    "gpt-4o": {"input_per_1k": 0.005, "output_per_1k": 0.015},
}

@dataclass
class Usage:
    prompt_tokens: int
    completion_tokens: int
    model: str

def estimate_cost(usage: Usage) -> float:
    pricing = MODEL_PRICING.get(usage.model, MODEL_PRICING["gpt-4o-mini"])
    return (usage.prompt_tokens/1000)*pricing["input_per_1k"] + (usage.completion_tokens/1000)*pricing["output_per_1k"]
