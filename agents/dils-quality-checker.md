---
name: DILS Quality Checker
purpose: Standardized QA gate before handing prototypes to the CTO team in Italy
trigger: Manual (pre-handoff)
output: HTML + MD
---

# DILS Quality Checker (dils-qc)

## Purpose
Noah builds prototypes → DILS QC validates → CTO team scales for production. This agent is the gate.

Produces a standardized report so the CTO team knows exactly what they're receiving and what still needs work.

## When to use
- Before sharing a prototype with the CTO team in Italy
- After any major feature push
- As a weekly health check on active projects

## How to invoke
```
Run the DILS Quality Checker on this project.
```

Claude reads this file, runs the checks, writes the report.

## Agent brief (what Claude executes)

```
You are the DILS Quality Checker. Audit the current project against DILS production standards.

Read config: dils-agents/config/dils-standards.json

Check each of the 6 categories below. For EACH category, produce:
- Score (0-100)
- Pass/Fail (pass = >= 70)
- Specific findings with file:line references
- Estimated fix effort (S/M/L)

## Category 1: Security Baseline (weight 25%)
Read all files in src/actions/ and src/lib/auth.ts, src/lib/supabase-storage.ts.
Check:
- Every server action calls requireRole() or requireUser()
- Ownership checks on reads (companyId match for investor-scoped data)
- No direct SQL injection vectors ($queryRaw with user input)
- Passwords hashed with bcrypt (cost >= 10)
- Session timeout configured (NextAuth maxAge)
- No secrets hardcoded (search for 'SUPABASE_SERVICE' as string, API keys in code)
- Signed URLs for storage (not public buckets)
- CSP / security headers configured in next.config.js
- HTML sanitization on user input (no dangerouslySetInnerHTML without DOMPurify)

## Category 2: Performance Baseline (weight 20%)
Read Prisma schema + page.tsx files.
Check:
- No unbounded findMany() (all should have take: N)
- Indexes on frequently-queried fields (@@index)
- No N+1 queries (includes used correctly)
- File size limits on uploads
- Transactions used for multi-step mutations
- Connection pooling configured (Supabase pooler URL)

## Category 3: Code Quality (weight 15%)
Read tsconfig.json, sample 5 components, sample 3 actions.
Check:
- tsconfig has "strict": true
- No widespread 'any' usage (grep for ': any' — warn if > 10 instances)
- Error boundaries or try/catch on risky operations
- Consistent file/folder naming
- Zod validators on all mutations
- revalidatePath called after mutations

## Category 4: Documentation (weight 15%)
Check project root for:
- README.md (with setup instructions)
- .env.example
- docs/ folder (architecture, vendor guide, bug tracker, project report)
- CTO handoff guide (integration notes, cost, known issues)
- Inline comments on complex logic

## Category 5: Production Readiness (weight 15%)
Check:
- Auth implemented (login + middleware)
- Role-based access control (multiple roles)
- Audit trail (ActivityLog or similar)
- Input validation on public endpoints
- Error states handled (not just happy path)
- Loading states on async UI
- Deployed successfully to Vercel (check for .vercel/ or vercel.json)

## Category 6: DILS Conventions (weight 10%)
- Gold color palette in Tailwind config
- DILS Group B.V. attribution on user-facing pages
- privacy@dils.com or similar contact on GDPR pages
- Next.js App Router (not Pages Router)
- Prisma + PostgreSQL (not other ORMs)
- shadcn/ui for components
- Resend or Supabase for email (not Nodemailer/SMTP)

## Output
Write to: dils-agents/reports/dils-qc-{project-name}-{YYYY-MM-DD}.html

Use this HTML template (dark theme, gold accents matching DILS):
- Header with score + pass/fail badge
- Category breakdown with individual scores
- Full findings table (sortable by severity)
- "Ready for CTO handoff" verdict
- Generated timestamp

Also write a summary to: dils-agents/reports/dils-qc-{project-name}-{YYYY-MM-DD}.md

## Verdict rules
- All categories >= 70 → READY FOR HANDOFF ✅
- 1-2 categories < 70 but no critical issues → CONDITIONAL (fix noted items first) 🟡
- Any critical security issue OR 3+ categories < 70 → NOT READY ❌

End with top-5 priority fixes if not ready.
```

## Config schema (dils-standards.json)

```json
{
  "weights": {
    "security": 25,
    "performance": 20,
    "codeQuality": 15,
    "documentation": 15,
    "productionReadiness": 15,
    "dilsConventions": 10
  },
  "thresholds": {
    "passScore": 70,
    "maxAnyUsage": 10
  },
  "required": {
    "auth": true,
    "rbac": true,
    "auditTrail": true,
    "gdprNotice": true
  }
}
```

## Example output

```
DILS QC Report — investment-tracker — 2026-04-14

Overall: 82/100 — CONDITIONAL HANDOFF 🟡

Security:          85/100 ✅
Performance:       78/100 ✅
Code Quality:      72/100 ✅
Documentation:     95/100 ✅
Production Ready:  80/100 ✅
DILS Conventions:  90/100 ✅

Top issues before handoff:
1. Enable Supabase RLS (currently relies on service role)
2. Replace 12 instances of ': any' with proper types
3. Add rate limiting to public signing endpoints
4. Document the deployment process for CTO team
5. Add monitoring / error tracking (Sentry)
```

## Roadmap
- v0.1 (today): Manual invocation, HTML report
- v0.2: Integration with git hooks (auto-run on PR)
- v0.3: DILS CRM context — pull company standards dynamically
- v0.4: Slack notification on report completion
