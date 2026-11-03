-- Kør i Supabase -> SQL Editor (én gang) for at slå admin-siden /admin.html til.
-- Kun brugeren med den BEKRÆFTEDE e-mail nedenfor kan læse feedback og se brugerstatistik. Alle andre afvises stadig.
-- Hold "Confirm email" slået til under Authentication -> Providers -> Email, så ingen kan oprette en bruger med din e-mail uden at eje den.

alter table public.feedback add column if not exists behandlet boolean not null default false;

grant select on public.feedback to authenticated;
grant update (behandlet) on public.feedback to authenticated;

drop policy if exists "admin kan laese feedback" on public.feedback;
create policy "admin kan laese feedback" on public.feedback for select to authenticated
  using ((auth.jwt() ->> 'email') = 'jonasvilladsen@live.dk');

drop policy if exists "admin kan opdatere feedback" on public.feedback;
create policy "admin kan opdatere feedback" on public.feedback for update to authenticated
  using ((auth.jwt() ->> 'email') = 'jonasvilladsen@live.dk')
  with check ((auth.jwt() ->> 'email') = 'jonasvilladsen@live.dk');

create or replace function public.admin_statistik() returns json
language plpgsql security definer set search_path = public, auth as $$
begin
  if coalesce(auth.jwt() ->> 'email', '') <> 'jonasvilladsen@live.dk' then
    raise exception 'ikke tilladt';
  end if;
  return json_build_object(
    'brugere_i_alt', (select count(*) from auth.users),
    'bekraeftede', (select count(*) from auth.users where email_confirmed_at is not null),
    'nye_7_dage', (select count(*) from auth.users where created_at > now() - interval '7 days'),
    'aktive_7_dage', (select count(*) from auth.users where last_sign_in_at > now() - interval '7 days'),
    'pr_dag', (select coalesce(json_agg(json_build_object('dag', d::date, 'antal',
                 (select count(*) from auth.users u where u.created_at::date = d::date)) order by d), '[]'::json)
               from generate_series(current_date - 29, current_date, interval '1 day') d)
  );
end $$;

revoke all on function public.admin_statistik() from public, anon;
grant execute on function public.admin_statistik() to authenticated;
