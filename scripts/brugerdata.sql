-- Kør i Supabase -> SQL Editor (én gang). Gemmer hver brugers valgte retter, indkøbsliste og ugeplan, så de kan ses på flere enheder.
-- Kun brugeren selv kan læse, ændre og slette sin egen række. Rækken slettes automatisk, hvis brugeren slettes.
create table if not exists public.brugerdata (
  user_id uuid primary key references auth.users (id) on delete cascade,
  data jsonb not null,
  genereret text,
  opdateret timestamptz not null default now()
);

alter table public.brugerdata enable row level security;

drop policy if exists "bruger ejer sin data" on public.brugerdata;
create policy "bruger ejer sin data" on public.brugerdata
  for all to authenticated
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

grant select, insert, update, delete on public.brugerdata to authenticated;
