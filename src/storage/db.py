from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def log_llm_usage(model: str, prompt_tokens: int, completion_tokens: int, total_tokens: int, cost_usd: float, input_preview: str, output_preview: str):
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO llm_logs(model, prompt_tokens, completion_tokens, total_tokens, cost_usd, input_preview, output_preview)
            VALUES (:model, :pt, :ct, :tt, :cost, :ip, :op)
        """), dict(model=model, pt=prompt_tokens, ct=completion_tokens, tt=total_tokens, cost=cost_usd,
                     ip=input_preview[:500], op=output_preview[:500]))
