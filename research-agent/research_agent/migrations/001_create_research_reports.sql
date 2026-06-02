CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS research_reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  product_idea TEXT NOT NULL,
  report JSONB NOT NULL,
  model TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS research_reports_product_idea_idx
  ON research_reports (product_idea);

CREATE INDEX IF NOT EXISTS research_reports_created_at_idx
  ON research_reports (created_at DESC);
