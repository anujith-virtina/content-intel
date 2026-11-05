---
title: Research notes - WooCommerce emails not sending
client: virtina
date: 2026-11-02
topic: woocommerce emails not sending (problem/fix + lead path, US)
audience: US WooCommerce store owners whose order, customer, password-reset or invoice emails fail
stage: research
slug: order-emails-not-sending
---

# Research: WooCommerce emails not sending

Rules read: MUST-FOLLOW-RULES.md (all sections), voice.md, audience.md, brand.md, internal-links.md, inventory. Uniqueness: `uniqueness-audit-woo-emails-2026-11-02.md` (GO, all 5 checks pass). Competitors: `competitor-analysis-woo-emails-2026-11-02.md`.

## Recommendation
- **Title/H1:** WooCommerce emails not sending? Diagnose it in four steps, then decide who fixes it
- **Yoast title:** WooCommerce Emails Not Sending? How to Fix It | Virtina (54 chars)
- **Slug:** `order-emails-not-sending` (fallback `store-emails-not-sending`)
- **Primary keyword:** woocommerce emails not sending. Variants: woocommerce not sending order emails, woocommerce email notifications not working, woocommerce new order email not received.
- **Angle:** a missing email fails at one of four stages: (1) never triggered, (2) triggered but not sent, (3) sent but not delivered, (4) delivered to spam. WooCommerce's own log names the stage in minutes. Owner fixes the first checks; developer handoff criteria are explicit.
- **Suggested format for analyzer:** Format D (decision tree/playbook), or Format A if recency rule blocks D. Includes required "problem/solution" case snippet and a checklist/numbered steps (4b).
- **US focus:** US spelling, US store-owner scenarios (holiday-season order loss), Gmail and Yahoo as the US-dominant mailbox providers is NOT stated as a statistic (unverified); say "major mailbox providers like Gmail and Yahoo".

## Sub-questions the reader asks
1. Which emails are failing, and are they supposed to be sent at all?
2. Did WooCommerce try to send them?
3. Did they leave my server, and did the receiver accept them?
4. Why do they go to spam?
5. What can I fix myself, and when do I need a developer?

## VERIFIED FACTS (source URL per fact)

### A. How WooCommerce sends email
- A1. WooCommerce sends email through WordPress's core `wp_mail()` function. When mail does not send, the problem is often the web host's mail function, or a deliverability problem where the server sends the message but it never arrives. Source: https://woocommerce.com/document/email-faq/
- A2. The official doc recommends a dedicated third-party SMTP provider because it is more reliable than your own server's mail-sending function, and says an average site usually stays within free tiers. Same source. (Do not name any plugin or provider; the doc does not.)
- A3. The doc says admin emails and WordPress password reset emails may not show in the WooCommerce log; for those, check the SMTP provider's logs or use a mail logging plugin. Same source.

### B. Stage 1: the email was never triggered
- B1. Orders in **Pending payment** do not trigger emails. Causes: customer abandoned an external payment page or the card was declined (varies by gateway). If payment succeeded but status did not update, that is a gateway communication problem, not an email problem. Source: https://woocommerce.com/document/email-faq/
- B2. An order that successfully moves to **Processing** should trigger the order notification, provided that email is enabled. Same source.
- B3. A theme, custom code or plugin conflict can throw an error before the order status changes, so no email is sent. The doc says to check logs for fatal errors and rule out conflicts with other plugins and themes disabled, using a default theme. Same source. (Virtina angle: do this on a staging copy, not live. The doc itself does not say staging; this is Virtina's added advice.)
- B4. Each email has an enable switch: WooCommerce > Settings > Emails > select the template > "Enable this email notification". Same source.

### C. Stage 2: triggered but not sent (the WooCommerce email log)
- C1. Menu path: WooCommerce > Status > Logs, source `transactional-emails`. Create a test order or trigger the email, then find the entry. Source: https://woocommerce.com/document/email-faq/
- C2. Four statuses: **Sent** (handed to the mail system; INFO), **Failed** (mail-sending returned an error, often with a reason; WARNING), **Disabled** (type turned off; NOTICE), **Skipped** (a required condition is missing, such as no recipient; NOTICE). Same source.
- C3. Sent and failed attempts also appear as private order notes; disabled and skipped appear only in the log. Same source.
- C4. If entries are missing, check WooCommerce > Status > Logs > Settings (logging on, threshold not hiding INFO or NOTICE). Same source.
- C5. Raw customer email addresses are not written to this log; recipients show as a username or "guest". Same source.
- C6. A Failed status "usually points to hosting or mail-sending setup"; no entry at all means check for fatal errors and conflicts. Same source (paraphrase).
- C7. A missing recipient produces "Skipped": the fix is to fill in the recipient in the email's settings. Same source.
- The doc does not state which WooCommerce version added this log. [unverified version]. Phrase as "current WooCommerce versions" and tell readers to look for it.

### D. Stage 3 and 4: sent but not delivered, or in spam
- D1. From address: use an address on your own site's domain in WooCommerce > Settings > Emails. Public free domains such as Gmail or Yahoo in the From field often cause mail to be marked spam or blocked, because the sending server does not match the declared sender. Source: https://woocommerce.com/document/email-faq/ and https://woocommerce.com/document/email-authentication/
- D2. Email authentication: SPF lists which servers may send for a domain; DKIM signs messages and receivers check the signature against a DNS record; DMARC tells receivers what to do with messages that fail both. Source: https://woocommerce.com/document/email-authentication/
- D3. If your host sends your store's email, ask the host to confirm SPF, DKIM and DMARC are set up; if you use an SMTP service, follow its domain authentication steps. Same source.
- D4. Authentication is worth setting up even if you only send transactional email, because other mailbox providers are likely to follow Google and Yahoo. Same source (paraphrase of the page's advice).
- D5. Gmail and Yahoo: Google's rules took effect Feb 1, 2024. For all senders to Gmail: SPF or DKIM, valid forward and reverse DNS (PTR), TLS, spam rate below 0.3% in Postmaster Tools (recommended below 0.10%), RFC 5322 format, one From address. Source: https://support.google.com/mail/answer/81126
- D6. Senders of more than 5,000 messages a day to Gmail must also have SPF and DKIM and DMARC (policy may be "none"), From domain aligned with SPF or DKIM, and one-click unsubscribe for marketing mail. Same Google source. A typical small store's transactional volume is well under that. [Avoid claiming the reader's volume; say "most single stores send far less, so the all-sender rules matter most".]
- D7. Yahoo (Sender Hub best practices, enforcement from Feb 2024): SPF or DKIM for all senders; both plus DMARC (at least p=none) for bulk senders; keep spam rate below 0.3%; From domain must align with SPF or DKIM. Source: https://senders.yahooinc.com/best-practices/ . Yahoo does not define "bulk sender" on that page.
- D8. Third-party testing: the Woo authentication doc names mail-tester.com for a test-order check. Do not link it (external cap) and do not recommend it as the only tool.

### E. Competitor-derived (secondary, single-source; use with hedging or leave out)
- E1. "Hosts often disable PHP mail to prevent abuse." Only from the WPBeginner article (https://www.wpbeginner.com/wp-tutorials/how-to-fix-woocommerce-not-sending-order-emails/), a secondary and affiliate-linked source. The official Woo doc does not discuss host limits. Phrase as "some hosts limit or block outgoing mail" and tag [secondary source]. Virtina's own post 43264 already says hosts can limit outgoing mail.

## Safe diagnostic order (use as the post's backbone)
1. Is an email supposed to fire? Check the order status (Processing vs Pending payment) and the per-email enable box and recipient.
2. Trigger a test order. Open WooCommerce > Status > Logs > `transactional-emails`.
3. Read the status. Sent, go to step 5. Failed, host or mail setup (step 6). Disabled or Skipped, settings. No entry, check fatal errors and conflicts on a staging copy.
4. Check the spam and junk folders, and the recipient address spelling, for the test.
5. Check the From address uses your own domain.
6. Route mail through a dedicated SMTP service (vendor-neutral). Check SPF, DKIM, DMARC records with the host or the SMTP service.
7. For password-reset and admin emails, use the SMTP provider's log or a mail logging plugin, since the WooCommerce log may not show them.

## When to bring in a developer (Virtina-derived judgment, flagged as opinion not citation)
- Orders are paid but status never reaches Processing (gateway callback problem).
- The log shows Failed with a host-level reason, or no entry plus fatal errors.
- You suspect a plugin or theme conflict but cannot test on a staging copy.
- You do not have DNS access, or records exist but mail still lands in spam.
- Custom emails, B2B approval emails or ERP-triggered messages stopped after an update (link to HPOS compatibility post, where custom fields went blank in emails).
- Emails fail again after a fix (recurring failure).
Brand tie-in: "stop the bleeding" (fix revenue-leaking issues fast). Use "talk to us" or "contact", never "reach out". Partner, not vendor. No "cheap". No "our guide".

## Case snippet (required for Problem/solution type, 4b)
Plan a 2-3 sentence illustrative scenario with no invented stats or client: e.g., a store owner sees paid orders in the dashboard but gets no new-order email; the log shows Skipped because the recipient field is blank. Mark clearly as an example, not a client case. Do not fabricate a customer name.

## Semantic terms (10-15, to appear naturally)
transactional emails, wp_mail(), SMTP service, SPF record, DKIM signature, DMARC policy, From address, domain alignment, spam folder, Pending payment, Processing status, email log, test order, reverse DNS (PTR), mailbox provider, deliverability, staging site, plugin conflict, fatal error, password reset email.

## LINK LIST

### External (max 2, both fetched and loaded; no competitor domains)
| # | URL | Use | Anchor suggestion |
|---|---|---|---|
| 1 | https://woocommerce.com/document/email-faq/ | log, statuses, pending payment, From address | WooCommerce email troubleshooting guide |
| 2 | https://support.google.com/mail/answer/81126 | Gmail sender rules since Feb 2024 | Gmail sender guidelines |
Optional swap for #2: https://woocommerce.com/document/email-authentication/ (also loads), but it is the same publisher as #1 and Google is the primary source for the rules. Yahoo link (https://senders.yahooinc.com/best-practices/) loaded but is reserved as plain-text reference only (cap of 2).
Each external link: `target="_blank" rel="noopener noreferrer"`.

### Internal service pages (lead targets). All fetched and loaded; canonical `link` confirmed by REST `/pages?include=`
| URL | Fit | Suggested anchor (2-5 words, no "our") |
|---|---|---|
| https://virtina.com/woocommerce-bug-fix/ | Best fit: service page with an "Email & Order Notifications" card | WooCommerce bug fix service |
| https://virtina.com/ai-powered-woocommerce-bug-fix/ | Symptom-led fix page, "Fix my WooCommerce store" CTA | AI-assisted WooCommerce bug fixing |
| https://virtina.com/woocommerce-support/ | Ongoing support, one-time fix request | WooCommerce support and maintenance |
| https://virtina.com/ecommerce-store-takeover/ | For stores inherited from another developer, has "Email & Order Issues" form option | store takeover service |
| https://virtina.com/platforms/woocommerce-development-services/ | Broad money page (use the `/platforms/` form; `/woocommerce-development-services/` is a 301) | WooCommerce development company |
Do NOT use `/woocommerce-customizations/` or `/ecommerce-integration/` for this post: both load but contain nothing about email. `/ecommerce-bug-fix/` is a 400-word thin page; skip. `/contact/` is a 301: use `/get-in-touch/` for any contact link (not fetched this run; verify before use).

### Internal posts (live, fetched, loaded)
| URL | Why | Suggested anchor |
|---|---|---|
| https://virtina.com/woocommerce-bug-fix-guide/ | broader bug list incl. a short email section | common WooCommerce bugs |
| https://virtina.com/woocommerce-checkout-not-working-agency/ | revenue-loss sibling, agency selection | WooCommerce checkout failures |
| https://virtina.com/woocommerce-hpos-plugin-compatibility/ | update-caused blank custom fields in emails; plugin conflicts | HPOS plugin compatibility |
| https://virtina.com/woocommerce-holiday-season-checklist/ | confirmation email timing before peak season | holiday season checklist |
| https://virtina.com/woocommerce-issues-killing-conversions/ | technical glitches section | WooCommerce conversion killers |
| https://virtina.com/ecommerce-website-problems/ | "check the order, the email and the payment record" | ecommerce website problems |
| https://virtina.com/woocommerce-mobile-checkout-buy-now-pay-later/ | order-email check in sale-week routine | mobile checkout fixes |
Not usable: `customer-payment-declined-guide` (43089) is a draft, public URL 404s. Anchors must be clean noun phrases; a 5-10 internal link target is met with 5 service plus 3-5 posts. Place links in body only (not intro or conclusion). Previous precedent: do NOT repeat the platform boilerplate sentence.
Link verification method: WebFetch loaded each URL (HTTP 200 inferred); redirects not observable by WebFetch for same-host moves, so canonical form is taken from the REST `link` field, which matches every URL above. Re-verify with a no-redirect check right before push (run by orchestrator, since sub-agents have no Bash).

## What could not be verified
- Whether `wp_mail()` uses PHP `mail()` via PHPMailer by default: developer.wordpress.org page returned title and dates only. The Woo doc says "host's core email function". Safe phrasing: "WooCommerce hands email to WordPress, which hands it to your host's mail setup". Avoid the PHPMailer detail.
- WooCommerce version that introduced the `transactional-emails` log. Not stated.
- That hosts commonly block PHP mail (only secondary source E1).
- Cron or Action Scheduler as an email-failure cause: no primary source found. **Leave out** unless the analyzer finds a doc. (User listed it; not verified, so do not state it.)
- Any statistic on how many orders or how much revenue are lost to missing emails: none found; **use none**.
- Ahrefs volume/KD/traffic potential: from the user, not re-checked.
- Real SERP rank order: approximated from search-tool order.
- Gmail/Yahoo pages have no visible last-updated date; footers show 2026. Date the claims as "since February 2024".
- Post 43089 slug and public availability.

## Style reminders for the creator
- US English. Short sentences (max 20 words), max 3 sentences per paragraph. First sentence of every H2 answers the H2 question. Minimum 6 H3s. Include Introduction, People Also Ask, Conclusion, FAQ (6-8 Q&As). Question-style body H2s; keep structural labels verbatim.
- No plugin or provider names. No em dashes, no banned words.
- Prose for authority; bullets only for genuinely list-shaped items (the diagnostic steps and the handoff list).
- Natural lead path: after the diagnostic, a short "when it stops being a DIY job" section linking the bug-fix service page, plus a contact link; no brochure tone.
