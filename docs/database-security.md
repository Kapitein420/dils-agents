# Database Security Inventory — All Projects

Master reference for what Supabase projects exist, what tables they hold, and RLS status.

Last updated: 2026-04-15

---

## Project 1 — Investment Tracker

**Supabase project:** `uyxualynbqmchugzvdpc`
**Used by:** `my-projects/investment-tracker`
**Contains:** Real investor/deal data, signed NDAs, company contacts, audit trail

### Tables (14)
User, Asset, Company, PipelineStage, AssetCompanyTracking, StageStatus,
Comment, StageHistory, ActivityLog, SavedView, Document, SigningToken,
InvestorInvite, AssetContent

### RLS status: ✅ LOCKED
- Script: `my-projects/investment-tracker/supabase-rls-policies.sql`
- Run date: 2026-04-15
- Policy: All tables have `deny_anon_all` RESTRICTIVE policy
- Storage: `documents` bucket deny-anon policy
- Service role (Next.js server actions) bypasses RLS as intended

### Security notes
- IDOR ownership checks in server actions (companyId match for INVESTOR)
- Signed URLs for all file access (2h expiry)
- bcrypt password hashing (cost 10)
- JWT session 8h maxAge, hourly refresh

---

## Project 2 — Personal Stack (life-agents + agent-hq)

**Supabase project:** `hdlxhwlbweuhqgqowiqu`
**Used by:** `life-agents` (sync scripts) + `agent-hq` (Telegram webhook, uptime monitor)
**Contains:** Personal health check-ins, Telegram conversation state, uptime history

### Tables (3)
- `check_ins` — morning/evening check-ins from Telegram
- `conversation_state` — what question the bot is expecting
- `uptime_checks` — deploy health monitoring

### RLS status: ✅ LOCKED
- Script: `agent-hq/sql/003_rls_lockdown.sql`
- Run date: 2026-04-15
- Policy: `deny_anon_all` + `deny_authenticated_all` on all 3 tables
- Writes come from service role only (Telegram webhook, cron jobs)

### Security notes
- Telegram webhook gated by `TELEGRAM_WEBHOOK_SECRET_TOKEN`
- agent-hq deployment gated by Basic Auth middleware
- Vercel cron jobs use service role
- Local sync scripts (`npm run sync`) use service role from `life-agents/.env`

---

## Projects without databases

| Project | Why no RLS needed |
|---------|------------------|
| `my-projects/dnd-tracker` | No Supabase — local JSON |
| `studio-agents` | No database — markdown specs only |
| `dils-agents` | No database — agent specs + reports |

---

## Emergency rollback

If RLS breaks an app and you need quick rollback, each SQL file has a commented-out rollback section at the bottom. Uncomment and run in the Supabase SQL editor of the relevant project.

## Rotation policy

- `SUPABASE_SERVICE_ROLE_KEY` should be rotated quarterly
- If a key is exposed in git or logs, rotate immediately via Supabase dashboard → Settings → API
- RLS provides defense-in-depth: even if the key leaks, the damage is bounded to what the service role can do (everything, but at least logged)

## Audit trail

- Investment Tracker: `ActivityLog` table records all mutations with userId + metadata
- Personal Stack: `check_ins.created_at` + `uptime_checks.checked_at` provide temporal audit

## Future additions

When a new project adds Supabase:
1. Write its RLS script in that project's `sql/` folder
2. Update this document with the new project entry
3. Run the script in the matching Supabase project
4. Verify via the sanity-check query at the bottom of each script
