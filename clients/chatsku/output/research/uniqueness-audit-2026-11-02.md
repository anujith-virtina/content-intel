---
title: Uniqueness audit, ChatSKU post supporting /black-hole-pipeline/
client: chatsku
date: 2026-11-02
topic: inquiry visibility / support post for money page 27
audience: owners, sales managers, ecommerce managers at B2B manufacturers, distributors, wholesalers
stage: research
slug: inquiry-tracking-seven-day-count
---

# Uniqueness audit

Corpus checked: 52 posts (live + draft) in chatsku-headings-2026-11-02.md and chatsku-texts-2026-11-02.json, plus the money page text (black-hole-pipeline-page-2026-11-02.md). The old inventory file is stale and was not relied on.

## What the money page already owns (do not repeat)

- Symptoms: inquiries scattered across email, phone, forms; no single owner; no tracking, follow-up or audit trail; "pipeline exists in people's heads and inboxes"; managers blind to volume, quote stage, pipeline value.
- Fix statement: every ChatSKU conversation captured and shown in one dashboard with inquiry source, product interest, buyer intent signals, quote status.
- Banned phrases for the new post (they are the page's own copy): "single source of truth", "heads and inboxes", "no audit trail", "if it isn't tracked, it isn't revenue", "Your competitor answered. You didn't know it happened."
- The page offers no measurement method, no definition of a record, no way to size the gap. That is the open lane.

## Who owns what among the 52 posts (body-level grep results)

Terms swept: audit trail, single source of truth, system of record, inquiry log, reconcil*, unified/shared inbox, pipeline value, quote stage, inquiry source, intent signal, visibility, voicemail, missed call, lead source, unlogged, inquiry volume, seven/7-day, this week, self-check, tally.

| Post | What it owns | Overlap with the new topic |
|---|---|---|
| 299 quote-to-order | Silence AFTER a quote is sent. Table row "Visibility into quote status" (rep memory or stale CRM field vs real-time view). Checklist "No visibility into losses". | Low. Different moment (post-quote). Link to it, do not restate the table. |
| 3846 trade show | Open-question queue after a show: "Turn each open question into a lead" (question, product, contact details, time), "shared inbox where they wait for two days", set a reply owner. | Medium on the owner and shared-inbox idea. New post must not retell the owner/reply-time advice. Different channel (booth). |
| 3798 who it is built for | Fit test; "Nobody owns follow-up. If quote requests land in an inbox nobody reads, the assistant cannot fix that." | Low-medium. One-line mention only, link out. |
| 3010 will AI replace reps | Manager's week: "more visibility into what buyers are asking", "real pipeline visibility, not a guess", "Name one person who owns every lead". | Medium on manager visibility. New post takes the PRE-rollout measurement angle, not the day-in-the-life. |
| 3956 agent vs chatbot vs rep | Compare table row "Visibility into buyer questions", complete RFQ sent to team or CRM, "who owns the transcripts". | Low. Product comparison. |
| 3929 cross-reference | A "record nobody designed" for part-number cross-references (six fields, owner, date stamp). | Medium on the "what must a record hold" form. Different object (part mapping, not inquiry). Do not reuse the "record nobody designed" framing or "stamp a date on every row". |
| 3294 (DRAFT, not to be linked) | KPI redesign after rollout: deflection rate, qualified-handoff rate, time-to-quota. | Low. That is post-rollout metrics. New post is the pre-rollout baseline. Keep metric names distinct. |
| 2992, 1855, 1300, 2783 | Response-time and quote-speed clocks. | Low. Speed, not visibility. |
| 369, 186, 266, 251, 1684 | Buyers leaving, after-hours loss, conversion, RFQ form conversion/best practices. | Low. Form conversion, not inquiry accounting. Grep for "inquiry volume" hits only inside ROI and benchmark sentences. |
| 2684, 2869 | Self-checks on an ERP export and on AI-agent readability. | Format overlap only ("run it this week"). Different surface. |
| 702 funnel inversion (draft) | Contact form taxes the buyer; answer first. | Low. |

No post contains: "unlogged", "inquiry log", "audit trail" (one hit, AP2 payments in 2129, unrelated), "system of record", "seven-day"/"7-day" counts, a method for counting inquiries across inbox, phone, and forms, or a rate that measures how much inbound demand has no shared record. "Reconcile" appears only for PDF-vs-spreadsheet (3846), Reciprocal Rank Fusion (2468), and ERP price sources (3956/2684).

## Candidate topics

| # | Candidate | Verdict | Reason |
|---|---|---|---|
| A | How to measure the inquiries you cannot see: a 7-day count across inbox, phone, forms and the unlogged inquiry rate | PASS | Zero body-level hits for method or metric. Upstream of the money page. Reader acts on it Monday. Fits product (the website-conversation share lands in the dashboard; the rest is shown honestly as process work). |
| B | What a sales manager should be able to see (pipeline report spec) | FAIL as standalone | 3010 owns manager visibility narrative; 3294 draft owns KPI redesign; 2992 has a KPI case. Fold one short section into A. |
| C | Minimum fields an inquiry record must hold | FAIL as standalone | Money page lists the dashboard fields; 3929 and 3846 each define a record. Fold in as a short section of A, with different fields and framing. |
| D | Who owns an incoming inquiry (ownership/handoff rules) | FAIL | 3846, 3798, 3010, 3956 all say "name an owner". Saturated. |
| E | Attribution: which channel brings the best inquiries | FAIL | Drifts into marketing analytics, off brand.md themes; 186/277 own the after-hours revenue math. |

## Product-fit check (brand.md + live pages)

- brand.md themes: quote workflow automation (yes), after-hours capture (adjacent), real-time analytics on buyer intent (yes, listed under the single product).
- Verified on live pages 2026-11-02: /demo/ shows an admin dashboard with products, quotes, orders, customers, analytics, chatbot settings, team management. /ai-sales-assistant-b2b-ecommerce/ lists "Full conversation logs" and shopper-intent analytics. 3956 says a complete RFQ goes to team or CRM with the conversation attached. Money page lists source, product interest, intent signals, quote status.
- NOT claimable: phone-call capture, email-inbox capture, automatic CRM write-back beyond "sends RFQ to your CRM or inbox", a named "inquiry dashboard" field list beyond the money page, deployment times beyond brand.md (one line of code, live in under a day; demo page says about four hours on average).
- The honest framing: ChatSKU turns the website conversation door into structured records. Phone and email stay a process problem the count exposes. The post says so, which also separates it from vendor pages that claim to unify everything.

## Verdict

CHOSEN: Candidate A.
Title: How many B2B inquiries never reach your pipeline? Run a 7-day count
Slug: inquiry-tracking-seven-day-count (shares no word with any of the 52 slugs except none; checked "inquiry", "tracking", "seven", "day", "count" against all slugs. "rate" is not in the slug.)
Primary keyword: b2b inquiry tracking
Format recommendation: D (decision-tree / playbook). Recent posts are mostly A/B/E; D gives sequenced steps and suits the count-then-decide shape.

## Post-draft dedup reminders

- Run the 8-gram shingle audit against all 52 posts AND the money page text before push.
- Fence list for the creator: no retelling of 299's silence table, 3846's open-question queue, 3010's persona narrative, 3294's KPI names (deflection, qualified-handoff, time-to-quota), 3929's six-field record.
- Vary the boilerplate platform and "live in under a day" sentences; both recur across the corpus.
