# ai-core (Starter Kit)

Reusable AI core library for AI projects.

## Features
- **Summarizer Chain** (Thai/English) with JSON output (`title`, `summary`, `bullet_points`, `sources`)
- **RAG (Document Q&A)** using PGVector (PostgreSQL). Qdrant adapter can be added later.
- **Conversation Memory** (buffer) for chatbot use.
- **FastAPI endpoints**: `/health`, `/summarize`, `/qa`
- **Cost/Prompt logging** to PostgreSQL
- **Config via `.env`** (works locally and on Cloud)

## Quickstart
1) Copy `.env.example` → `.env` and fill values.
2) Start DB: `docker compose up -d` (PostgreSQL with pgvector)
3) Create tables: `make db-migrate`
4) Install deps: `pip install -r requirements.txt`
5) Run API: `uvicorn src.services.api:app --reload --port 8000`

## Endpoints
- `GET /health` → `{ "status": "ok" }`
- `POST /summarize`
  ```json
  { "text": "....", "language": "th", "max_tokens": 300, "sources": ["https://..."] }
  ```
- `POST /qa`
  ```json
  { "query": "ทำไมหุ้น AAPL ขึ้นวันนี้?", "top_k": 4 }
  ```

## Folder Structure
```
ai-core/
├─ README.md                         # คำอธิบายโปรเจกต์ การใช้งานเบื้องต้น
├─ .env.example                      # ตัวอย่างตัวแปรแวดล้อม (API keys, DB URL, models)
├─ requirements.txt                  # รายการไลบรารี Python ที่ต้องใช้
├─ docker-compose.yml                # Dev stack สำหรับ PostgreSQL + PGVector (local)
├─ Makefile                          # คำสั่งลัด: db-migrate / run / test
├─ scripts/
│  └─ bootstrap_pgvector.sql         # สร้างตาราง documents, llm_logs, index vector
└─ src/
   ├─ __init__.py
   ├─ config.py                      # Pydantic settings โหลดค่าจาก .env (OPENAI_API_KEY, DB, MODEL)
   ├─ prompts/
   │  ├─ summarizer.txt              # System prompt สำหรับสรุปข่าว/บทความ (JSON schema)
   │  └─ qa.txt                      # System prompt สำหรับ RAG/QA (อ้างอิงเฉพาะ context)
   ├─ schemas/
   │  └─ models.py                   # Pydantic I/O: SummarizeRequest/Result, QARequest/Result
   ├─ utils/
   │  ├─ logging.py                  # Structured logger (stdout)
   │  └─ cost_tracker.py             # ประเมินค่าใช้จ่ายต่อคำขอจาก token usage
   ├─ llm/
   │  └─ providers.py                # Abstraction เรียก LLM/Embedding (OpenAI/สลับได้ในอนาคต)
   ├─ storage/
   │  ├─ db.py                       # SQLAlchemy engine + ฟังก์ชัน log การใช้งาน LLM (llm_logs)
   │  └─ vector/
   │     ├─ pgvector_store.py        # Adapter เก็บ/ค้น embedding ใน PGVector
   │     └─ (qdrant_store.py)        # (optional) Adapter Qdrant สำหรับสลับ backend
   ├─ ingestion/
   │  └─ ingest.py                   # Pipeline: split → embed → upsert เข้าฐานเวกเตอร์
   ├─ memory/
   │  └─ memory.py                   # ConversationBufferMemory (เก็บ turn ล่าสุดของแชตบอท)
   ├─ chains/
   │  ├─ summarizer.py               # Summarizer Chain → คืนค่า JSON (title/summary/bullets/sources)
   │  └─ rag.py                      # RetrievalQA Chain → embed query, ค้นเวกเตอร์, รวม context, ตอบ
   ├─ services/
   │  └─ api.py                      # FastAPI endpoints: /health, /summarize, /qa
   └─ tests/
      └─ test_summarizer.py          # Smoke test เบื้องต้น (import/structure)
```

## Folder Guide
- `src/config.py` – Pydantic settings (API keys, DB URL, models)
- `src/llm/providers.py` – OpenAI provider abstraction (chat + embed)
- `src/chains/summarizer.py` – Summarizer Chain
- `src/chains/rag.py` – RetrievalQA Chain
- `src/memory/memory.py` – ConversationBufferMemory
- `src/storage/db.py` – SQLAlchemy engine + LLM logs
- `src/storage/vector/pgvector_store.py` – PGVector adapter
- `src/ingestion/ingest.py` – Split → Embed → Upsert pipeline
- `src/schemas/models.py` – Pydantic I/O models
- `src/services/api.py` – FastAPI app
- `src/utils/*` – logging, cost tracking

## Notes
- You can add `src/storage/vector/qdrant_store.py` to swap vector backend later.
- For local prototyping without costs, consider adding an Ollama provider (not included).

MIT License.
