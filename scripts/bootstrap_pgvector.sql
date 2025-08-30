CREATE EXTENSION IF NOT EXISTS vector;

-- Documents (RAG chunks)
CREATE TABLE IF NOT EXISTS documents (
  id SERIAL PRIMARY KEY,
  doc_id TEXT,
  source TEXT,
  content TEXT,
  embedding vector(1536),
  created_at TIMESTAMP DEFAULT NOW()
);
CREATE UNIQUE INDEX IF NOT EXISTS uq_documents_doc_id_source ON documents(doc_id, source);
CREATE INDEX IF NOT EXISTS idx_documents_embedding ON documents USING ivfflat (embedding vector_cosine_ops);

-- LLM logs
CREATE TABLE IF NOT EXISTS llm_logs (
  id SERIAL PRIMARY KEY,
  event_time TIMESTAMP DEFAULT NOW(),
  model TEXT,
  prompt_tokens INT,
  completion_tokens INT,
  total_tokens INT,
  cost_usd NUMERIC(10,6),
  input_preview TEXT,
  output_preview TEXT
);
