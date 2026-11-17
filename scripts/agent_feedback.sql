-- Kør i Supabase -> SQL Editor (én gang). Giver Product Owner (via GitHub-handlingen .github/workflows/feedback-product-owner.yml) en SMAL adgang til feedback-tabellen.
--
-- Hvad adgangen kan:  læse nye beskeder (id, tidspunkt, type, tekst, teknisk baggrund, side) og markere dem som læst af agenten.
-- Hvad den IKKE kan:  se e-mailadresser, brugere, gemte madplaner eller noget andet i databasen. Ingen service-nøgle bruges.
-- Beskyttet af en tilfældig hemmelighed, som kun du kender. Databasen gemmer kun et fingeraftryk (hash) af den.
--
-- SÅDAN:
--  1. Lav en tilfældig hemmelighed på mindst 32 tegn. I PowerShell:
--       -join ((48..57)+(65..90)+(97..122) | Get-Random -Count 40 | ForEach-Object {[char]$_})
--  2. Erstat SKRIV_HEMMELIGHEDEN_HER nedenfor med den (kun i SQL-editoren, ALDRIG i filen i repoet), og kør hele scriptet.
--  3. Læg den samme hemmelighed i GitHub: Settings -> Secrets and variables -> Actions -> New repository secret
--       navn: SUPABASE_FEEDBACK_TOKEN    værdi: hemmeligheden
--  4. Send den ikke til nogen og skriv den ikke i en chat.
-- Kan køres igen for at skifte hemmelighed.

alter table public.feedback add column if not exists agent_set timestamptz;  -- hvornår agenten har læst beskeden (adskilt fra din egen "behandlet" i admin)

create table if not exists public.agent_noegle (hash text primary key);
alter table public.agent_noegle enable row level security;
revoke all on public.agent_noegle from anon, authenticated;

do $$
declare t text := 'SKRIV_HEMMELIGHEDEN_HER';
begin
  if t = 'SKRIV_HEMMELIGHEDEN_HER' or length(t) < 32 then
    raise exception 'Erstat SKRIV_HEMMELIGHEDEN_HER med din egen tilfældige hemmelighed på mindst 32 tegn';
  end if;
  delete from public.agent_noegle;
  insert into public.agent_noegle (hash) values (encode(sha256(convert_to(t, 'utf8')), 'hex'));
end $$;

create or replace function public.agent_feedback_hent(hemmelig text) returns json
language plpgsql security definer set search_path = public as $$
begin
  if not exists (select 1 from public.agent_noegle where hash = encode(sha256(convert_to(coalesce(hemmelig, ''), 'utf8')), 'hex')) then
    raise exception 'ikke tilladt';
  end if;
  return coalesce((
    select json_agg(x) from (
      select id, oprettet, type, besked, kontekst, side   -- bevidst IKKE email
      from public.feedback where agent_set is null order by id limit 100
    ) x), '[]'::json);
end $$;

create or replace function public.agent_feedback_marker(hemmelig text, ider bigint[]) returns integer
language plpgsql security definer set search_path = public as $$
declare n integer;
begin
  if not exists (select 1 from public.agent_noegle where hash = encode(sha256(convert_to(coalesce(hemmelig, ''), 'utf8')), 'hex')) then
    raise exception 'ikke tilladt';
  end if;
  update public.feedback set agent_set = now() where id = any(ider) and agent_set is null;
  get diagnostics n = row_count;
  return n;
end $$;

revoke all on function public.agent_feedback_hent(text) from public;
revoke all on function public.agent_feedback_marker(text, bigint[]) from public;
grant execute on function public.agent_feedback_hent(text) to anon;
grant execute on function public.agent_feedback_marker(text, bigint[]) to anon;
