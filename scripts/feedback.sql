-- Kør i Supabase -> SQL Editor (én gang). Opretter tabellen til feedback-chatten på siden.
-- Alle (anon) må KUN sende feedback ind; ingen kan læse den udefra. Du læser den i Table Editor.
create table if not exists public.feedback (
  id bigint generated always as identity primary key,
  oprettet timestamptz not null default now(),
  type text not null check (char_length(type) <= 40),
  besked text not null check (char_length(besked) between 3 and 1500),
  email text check (email is null or char_length(email) <= 200),
  kontekst jsonb,
  side text check (side is null or char_length(side) <= 200)
);
alter table public.feedback enable row level security;
drop policy if exists "alle kan sende feedback" on public.feedback;
create policy "alle kan sende feedback" on public.feedback for insert to anon, authenticated with check (true);
grant insert on public.feedback to anon, authenticated;
