-- Garden Festival — Supabase leaderboard setup
-- Run this once in your Supabase project: Dashboard → SQL Editor → New query → paste → Run.

create table if not exists public.scores (
  id          bigint generated always as identity primary key,
  name        text not null check (char_length(name) <= 20),
  score       integer not null check (score >= 0),
  character   text,
  created_at  timestamptz not null default now()
);

-- Index so the Top-10 query is fast.
create index if not exists scores_score_idx on public.scores (score desc);

-- Row Level Security: anyone can READ and INSERT, but NOT update or delete.
-- (Family-friendly: scores can be added and seen, but not tampered with.)
alter table public.scores enable row level security;

create policy "anyone can read scores"
  on public.scores for select
  using (true);

create policy "anyone can insert scores"
  on public.scores for insert
  with check (true);

-- Note: no update/delete policies => those actions are denied for the public key.
