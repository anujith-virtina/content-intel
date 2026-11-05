---
title: Brief, WooCommerce emails not sending (diagnose by stage, then decide who fixes it)
client: virtina
date: 2026-11-02
topic: woocommerce emails not sending
audience: US WooCommerce store owners and ops managers losing order, confirmation, password-reset or invoice emails
stage: brief
slug: order-emails-not-sending
research: clients/virtina/output/research/woo-emails-not-sending-2026-11-02.md
---

# Brief: WooCommerce emails not sending? Diagnose it in four steps

## 1. Thesis (one sentence)

> A missing WooCommerce email fails at one of four stages (never triggered, not sent, sent but not delivered, or landed in spam), and WooCommerce's own transactional-emails log names the stage in minutes, so diagnose before you buy or install anything, then hand the cases that need server, DNS or code access to a developer with the right evidence.

Why this angle, why now, why Virtina:
- **Defensible.** All five ranking competitors are vendors selling a plugin, host or sending service. None uses the built-in log, none says when to stop DIY, none cites Gmail rules at source (competitor file, cross-cutting gaps).
- **Now.** Holiday-season order volume starts in November. A silent order inbox costs the most then.
- **Virtina fit.** "Fix revenue-leaking issues fast" is brand theme 6. The post earns trust with a vendor-neutral diagnosis, then routes to the bug-fix pages, which own the commercial intent.

## 2. Locked inputs (do not change)

| Item | Value |
|---|---|
| H1 | **WooCommerce emails not sending? Diagnose it in four steps** (57 chars). The locked 82-char H1 was tightened per the ~70 limit. "Who fixes it" is carried by the Summary, the developer H2 and the meta description. Keyword is in H1, first 100 words, meta. |
| Slug | `order-emails-not-sending` (fallback `store-emails-not-sending`) |
| Yoast title | WooCommerce Emails Not Sending? How to Fix It \| Virtina (54 chars) |
| Meta description (157 chars) | WooCommerce emails not sending? Find which of four stages is failing, read the built-in email log, and learn when to hand the fix to a WooCommerce developer. |
| Focus keyword | woocommerce emails not sending |
| Categories | WooCommerce (79), eCommerce (405) |
| Length | 2,000 to 2,600 words visible prose (target about 2,450) |
| Draft status | draft only |

## 3. Format decision (MUST-FOLLOW-RULES section 11)

1. **Format chosen: D (Decision-tree / playbook).**
2. **Reason:** the reader walks a fixed sequence of checks, each with a branch ("log says Failed, go here; says Skipped, go there"), which is the D structure, and it ends in a build-vs-escalate decision.
3. **Recency check (last 10 by date in corpus.json, newest first):** 43336 (5 nightmares, C), 43728 (WooCommerce vs BigCommerce, A or D), 43583 (returns policy, A), 43418 (Magento checklist and cost, A), 43414 (WooCommerce cost, A), 43420 (firearms payments, A), 43507 (Volusion to BigCommerce, A or D), 43421 (B2B dev guide, A), 43361 (HPOS compatibility, A), 43362 (spam update, A). Plus unlisted drafts 43753 (E) and 43758 (C). The corpus and the local inventory carry no format field (inventory last_updated 2026-09-09, stale), so these are inferred from titles and sibling briefs.
4. **Count:** A about 7 of 10, C 1 (2 with draft 43758), D 0 to 2, E 0 (1 with draft 43753). **Overused and skipped: Format A.** D is at most 2 of 10, so it passes the "not 3 or more" rule. C and E also skipped (C is 2 with the draft; E was used by the other November draft).
5. **Structure note:** Format D uses the standard section frame (Summary, Introduction, TOC, body, PAA, Conclusion, FAQ). The body H2s are sequenced steps, each with a decision outcome.

## 4. Uniqueness re-verification

Re-checked against `uniqueness-audit-woo-emails-2026-11-02.md` and the 596-object corpus.json:
- **Pre-check 0 (pages):** PASS. No page slug or H1 about email delivery. The commercial `/woocommerce-bug-fix/` page has only a pitch card for "Email & Order Notifications", no editorial answer.
- **CHECK 1 title:** PASS. No title shares 3+ consecutive content words with "WooCommerce emails not sending diagnose four steps".
- **CHECK 2 slug:** PASS. `order-emails-not-sending` shares at most 1 word (`order`) with `order-fulfillment-services-ecommerce`. `emails` and `sending` appear in no slug.
- **CHECK 3 keyword:** PASS. No post or page is focused on "woocommerce emails not sending".
- **CHECK 4 angle:** PASS. Post 40347 has one two-step "How to Fix Email Errors" section (use an SMTP plugin, check From). This post's thesis is stage-based diagnosis plus developer handoff criteria, which no existing page argues.
- **CHECK 5 cluster:** PASS for the email sub-niche (2 passing mentions: 40347 section, 43264 bullet). The wider WooCommerce troubleshooting cluster is saturated at 7 or more; the sub-niche justification is documented.
- **Slug caveat:** the natural slug `woocommerce-emails-not-sending` fails CHECK 2, which is why the slug omits `woocommerce`.

## 5. Hard rules for the creator (this post)

**Zero unverified statistics.** Only these numbers may appear: Feb 1, 2024 (Google sender rules effective date), 0.3% spam rate threshold (Google), 5,000 messages a day (Google bulk-sender threshold), the four log statuses. No order-loss percentages, no revenue-loss figures, no "X% of stores".

**Do not:**
- Name any plugin, SMTP provider, mail tester or host. The official doc names none.
- Mention cron, WP-Cron or Action Scheduler (unverified).
- State that hosts block PHP mail. Hedge only as: the official guide points to the host's mail function as a frequent cause.
- Mention PHPMailer or claim `wp_mail()` uses PHP `mail()`. Safe wording: WooCommerce hands email to WordPress, which hands it to your host's mail setup.
- State which WooCommerce version added the log. Write "current WooCommerce versions" and "look under Status, Logs".
- Link draft 43089 (not live) or any URL not on the lists in section 7.
- Name Yahoo with a link. Yahoo may be mentioned as plain text once: it set comparable sender requirements from February 2024 (verified in research D7).
- Reuse wording from post 40347's "How to Fix Email Errors" section (watch: "stop using the default WordPress email function", "From address is valid and actually exists") or from 43264 (watch: "If your host limits outgoing mail, use a dedicated email service").
- Use the stock "builds on WooCommerce/Magento/BigCommerce/Shopify" sentence or any variant.
- Use "our", "we offer", "contact us", "reach out", "check out", "read our", "see our". The links carry the reference.
- Invent a client, customer name, byline or number. The case snippet is labelled illustrative.
- Use em dashes (four forms), semicolons, exclamation marks, banned hype or filler words (leverage, navigate as a verb, realm, landscape, ecosystem, "it's important to note", "in conclusion").
- Add a Yahoo, Gmail or mail-tester external link beyond the two allowed.

**Do:** US spelling and US scenarios; second person; max 3 sentences per paragraph; max 20 words per sentence; sentence-case headings; first sentence of every body H2 answers the H2; prose for authority; bullets only for genuinely list-shaped content (log statuses, checklist, handoff list).

## 6. Outline with word budgets (total about 2,450)

Section order: Summary, Introduction, TOC, body H2s 1 to 7, PAA, Conclusion, FAQ, author bio.

### Summary (about 75 words)
Teal box. State the thesis in plain terms: four stages, the built-in log names the stage, owner-fixable checks first, then criteria for a developer. Keyword in first sentence. Must say who fixes what.

### Introduction (about 120 words, 2 paragraphs)
Open on the cost of a silent inbox in the weeks before holiday peak: orders arrive but the owner and customer get nothing. State the common mistake: installing a mail tool before knowing which stage broke. Keyword "WooCommerce emails not sending" within the first 100 words of the post (Summary counts). No links.

### Body H2 1: Why do WooCommerce emails go missing, and which stage failed? (about 210 words) [id: four-stages]
- **Locked first sentence (20 words):** "A missing WooCommerce email fails at one of four stages: never triggered, not sent, not delivered, or landed in spam."
- Content: the four-stage model in prose, then Template N table (columns: Stage, What it means, Where to look first; 4 rows). Table caption in 14px grey per template.
- **H3:** "How does an order email travel from checkout to inbox?" Plain explanation: WooCommerce triggers on a status change, hands the message to WordPress, which hands it to your host's mail setup, which passes it to the receiving mailbox provider. Hedge: the official guide often points at the host's mail function.
- Link here: **/woocommerce-issues-killing-conversions/**, anchor "WooCommerce conversion killers" (technical glitches cost conversions; one sentence).
- Image 1 after this section.

### Body H2 2: Was the email ever triggered? (about 230 words) [id: step-1-triggered]
- **Locked first sentence (20 words):** "An email is triggered only when the order reaches a status that fires it, and that email is switched on."
- **H3:** "Is the order stuck in Pending payment?" Pending payment sends nothing. Causes: customer left an external payment page, or card declined (varies by gateway). If payment succeeded but the status never moved, that is a gateway communication problem, not an email problem. Orders that reach Processing should fire the notification when enabled. Links: **/woocommerce-checkout-not-working-agency/** anchor "WooCommerce checkout failures"; **/ecommerce-website-problems/** anchor "ecommerce website problems" (check the order, the email and the payment record together; one sentence).
- **H3:** "Is the email switched on and addressed to someone?" Path: WooCommerce, Settings, Emails, pick the template, "Enable this email notification". Blank recipient causes Skipped (stage 2 pays this off).

### Body H2 3: Did WooCommerce actually send the email? (about 310 words) [id: step-2-sent]
- **Locked first sentence (18 words):** "You can tell in minutes from the transactional-emails log, which marks each attempt sent, failed, disabled, or skipped."
- Content: place a test order or trigger the email, then open WooCommerce, Status, Logs, source transactional-emails.
- **H3:** "What do sent, failed, disabled and skipped mean?" Template F bullets, 4 items (genuinely list-shaped): Sent = handed to the mail system (not proof of delivery); Failed = mail-sending returned an error, often with a reason, usually points to hosting or mail setup; Disabled = that email type is turned off; Skipped = a required condition is missing, such as a recipient. Add: sent and failed attempts also appear as private order notes; recipients show as a username or "guest", not a raw address.
- **H3:** "Illustrative case: paid orders, no new-order email". Label it clearly "Illustrative example, not a client case." Scenario (2 to 3 sentences, no numbers, no names): owner sees paid orders in the dashboard but gets no new-order message; log shows Skipped because the recipient field is blank; filling in the recipient and placing another test order shows Sent. Satisfies the problem/solution snippet rule.
- **H3:** "What if the log is empty, or the email is not in it?" Check Logs, Settings (logging on, threshold not hiding info or notice entries). No entry at all means look for fatal errors and for plugin or theme conflicts, tested on a staging copy, not the live store (Virtina's own advice; say so plainly, the Woo doc does not mention staging). Admin emails and WordPress password-reset emails may not appear in the WooCommerce log; check the SMTP provider's own logs or a mail logging tool. No plugin names. Link: **/woocommerce-bug-fix-guide/**, anchor "common WooCommerce bugs" (broader bug list).
- Image 2 after this section.

### Body H2 4: Did the receiving mailbox accept it? (about 210 words) [id: step-3-delivered]
- **Locked first sentence (20 words):** "A Sent status only means WooCommerce handed the message onward, so delivery depends on your From address and mail setup."
- **H3:** "Does the From address use your own domain?" Use an address on your site's domain in WooCommerce, Settings, Emails. A free-mail From (Gmail, Yahoo) often gets marked spam or blocked, because the sending server does not match the declared sender (Woo email guide).
- **H3:** "Should store mail go through a dedicated SMTP service?" The official guide recommends a dedicated third-party SMTP provider as more reliable than your own server's mail function, and says an average site usually stays within free tiers. Say "SMTP service", never a brand. Also check the junk folder and the recipient spelling on the test order.
- No internal links needed here.

### Body H2 5: Why do store emails land in spam, and how do you fix it? (about 260 words) [id: step-4-spam]
- **Locked first sentence (16 words):** "Store emails land in spam when receivers cannot confirm the message really came from your domain."
- **H3:** "What do SPF, DKIM and DMARC each do?" SPF lists which servers may send for your domain. DKIM signs each message so the receiver can check it against a DNS record. DMARC tells receivers what to do when a message fails both. If your host sends your mail, ask the host to confirm all three are set up; if you use an SMTP service, follow its domain-authentication steps.
- **H3:** "What do Gmail's sender rules require?" Attribute to Google's sender guidelines, link once: https://support.google.com/mail/answer/81126 with `target="_blank" rel="noopener noreferrer"`, anchor "Gmail sender guidelines". Since February 2024, all senders to Gmail need SPF or DKIM, valid forward and reverse DNS, TLS, and a reported spam rate under 0.3% in Postmaster Tools. Senders of more than 5,000 messages a day also need SPF, DKIM and DMARC plus aligned domains. Do not claim the reader's volume. One plain-text sentence: Yahoo set comparable requirements from the same month. Advice from the Woo guide: set authentication up anyway because other mailbox providers are likely to follow.
- Also link the Woo troubleshooting guide once in this H2 or in H2 3: https://woocommerce.com/document/email-faq/ with `target="_blank" rel="noopener noreferrer"`, anchor "WooCommerce email troubleshooting guide" (place in H2 3 where the log is introduced, the better home).

### Body H2 6: What is the full checklist to run on one test order? (about 150 words) [id: diagnostic-checklist]
- **Locked first sentence (18 words):** "Run seven checks in order on a single test order, and stop at the first one that fails."
- Template F bullets with bold step labels ("Step 1." to "Step 7.") as the numbered checklist. One line each, with the branch outcome:
  1. Confirm the order status is Processing, not Pending payment.
  2. Confirm the email is enabled and has a recipient.
  3. Read the transactional-emails log entry for the test order.
  4. If Sent, check the junk folder and the recipient spelling.
  5. Confirm the From address uses your own domain.
  6. Route mail through a dedicated SMTP service and confirm SPF, DKIM and DMARC records.
  7. For password-reset and admin emails, read the SMTP provider's log instead.
- Add one closing sentence: if the same failure returns after a fix, treat it as a developer case (leads into the next H2).
- No H3 needed (under 200 words). Link: **/woocommerce-support/**, anchor "WooCommerce support and maintenance", in the recurring-failure sentence. Body only.

### Body H2 7: When should you bring in a WooCommerce developer? (about 320 words) [id: bring-in-developer]
- **Locked first sentence (20 words):** "Bring in a developer when paid orders never reach Processing, the log shows host errors, or you cannot test safely."
- Tone: criteria and facts, no sales language. This is the lead-gen H2. The primary lead link sits in the sentence where the decision is made.
- **H3:** "Which signs point to a developer-level problem?" Template F bullets (list-shaped criteria): paid orders whose status never reaches Processing (gateway callback); log shows Failed with a host-level reason, or no entry plus fatal errors; suspected plugin or theme conflict and no staging copy; no DNS access, or records exist but mail still lands in spam; custom, B2B approval or ERP-triggered emails stopped after an update; the failure returns after a fix. Links placed in this H3's prose or bullets: **/woocommerce-bug-fix/**, anchor "WooCommerce bug fix service" (primary lead target, in the sentence that frames the decision); **/woocommerce-hpos-plugin-compatibility/**, anchor "HPOS plugin compatibility" (update-caused blank custom fields in emails); **/platforms/woocommerce-development-services/**, anchor "WooCommerce development company" (custom or ERP-triggered emails); **/ecommerce-store-takeover/**, anchor "store takeover service" (store inherited from another developer, unknown custom code).
- **H3:** "What should you hand the developer?" Template F bullets (list-shaped): the log excerpt with status, reason and timestamp; results of the seven checks, noting where it failed; screenshots of the SPF, DKIM and DMARC DNS records; the From address and mail setup in use (host, SMTP service); example order numbers; what changed recently (updates, new plugins). Close with the benefit: the evidence turns an open-ended hunt into a short fix.
- Optional 10th link if it fits without crowding: **/ai-powered-woocommerce-bug-fix/**, anchor "AI-powered WooCommerce bug-fix". Skip if the section already has four service links.
- Image 3 inside this section, near the top.

### People also ask (about 150 words, 4 questions, Template H, answers 2 to 3 sentences)
1. How do I test WooCommerce emails? (Place a test order, read the transactional-emails log.)
2. Why am I not getting new order emails as the store owner? (Admin recipient and enable switch; admin emails may not show in the log; SMTP provider log.)
3. Do emails send when an order is Pending payment? (No; explain.)
4. Why do WooCommerce emails go to spam? (From domain, authentication; point to H2 5.)
No internal links.

### Conclusion (about 85 words, Template I, white text on teal)
Restate: four stages, one log, owner checks first, evidence-led handoff. No links, no CTA language, no "contact us". End on the practical value of diagnosing first.

### FAQ (about 330 words, Template J, 7 questions, answers 2 to 3 sentences)
1. What does a Sent status in the WooCommerce email log mean?
2. Can a plugin or theme conflict stop store emails?
3. Do I need a dedicated SMTP service for WooCommerce?
4. Why do password-reset emails not show in the WooCommerce log?
5. Is it safe to use a Gmail or Yahoo address as the From address?
6. How do I know whether my host is the problem?
7. What should I send a developer to speed up the fix?
Answers must not duplicate PAA wording. No links.

### Author bio (Template K)
Use the standard Virtina bio boilerplate from the latest published post. Do not invent a byline.

## 7. Link map (internal 9 required, 10 optional; external 2)

Method: all internal URLs were loaded in research and match the REST `link` field. The orchestrator must re-verify with a no-redirect check right before push. Every anchor is a clean noun phrase of 2 to 5 words, unique, no leading article, no gerund, no "our". Internal links only in body H2 sections, never in Summary, Introduction, PAA, Conclusion or FAQ. Internal links: no `target`, `style="outline: none;"` (Template L).

| # | URL | Anchor | H2 / H3 |
|---|---|---|---|
| 1 | /woocommerce-issues-killing-conversions/ | WooCommerce conversion killers | H2 1, H3 order travel |
| 2 | /woocommerce-checkout-not-working-agency/ | WooCommerce checkout failures | H2 2, H3 Pending payment |
| 3 | /ecommerce-website-problems/ | ecommerce website problems | H2 2, H3 Pending payment |
| 4 | /woocommerce-bug-fix-guide/ | common WooCommerce bugs | H2 3, H3 empty log |
| 5 | /woocommerce-support/ | WooCommerce support and maintenance | H2 6, closing sentence |
| 6 | /woocommerce-bug-fix/ | WooCommerce bug fix service | H2 7, H3 signs (PRIMARY lead link) |
| 7 | /woocommerce-hpos-plugin-compatibility/ | HPOS plugin compatibility | H2 7, H3 signs |
| 8 | /platforms/woocommerce-development-services/ | WooCommerce development company | H2 7, H3 signs |
| 9 | /ecommerce-store-takeover/ | store takeover service | H2 7, H3 signs |
| 10 (optional) | /ai-powered-woocommerce-bug-fix/ | AI-powered WooCommerce bug-fix | H2 7 |

External (max 2, `target="_blank" rel="noopener noreferrer"`, Template M):
1. https://woocommerce.com/document/email-faq/ , anchor "WooCommerce email troubleshooting guide", H2 3 (log, statuses, Pending payment, From address).
2. https://support.google.com/mail/answer/81126 , anchor "Gmail sender guidelines", H2 5.

Do not link: draft 43089, `/woocommerce-customizations/`, `/ecommerce-integration/`, `/ecommerce-bug-fix/` (thin), `/contact/` (301), `/woocommerce-development-services/` (301), any competitor domain, mail-tester, Yahoo. `/get-in-touch/` is not verified for this run; use it only if the orchestrator verifies it, and only in the body.

Rule check: 1 of the 2 service-page links sits in H2 6, 4 in H2 7. That clusters service links where the decision is made, which is the intended lead path, and each is stated as a fact ("a bug fix service handles X"), not a pitch.

## 8. Verified facts to use (source for each)

All from https://woocommerce.com/document/email-faq/ unless stated.
- WooCommerce sends email through WordPress's `wp_mail()`; failures are often the host's mail function or a deliverability problem. (Use semantic term `wp_mail()` once; do not add PHPMailer detail.)
- Dedicated third-party SMTP is recommended as more reliable than your own server's mail function; an average site usually stays within free tiers.
- Pending payment orders send no emails; Processing should fire the notification if enabled; payment succeeded but status stuck is a gateway issue.
- Theme, custom code or plugin conflict can throw an error before the status changes, so no email. Check for fatal errors; rule out conflicts by disabling plugins and using a default theme (Virtina adds: do this on staging).
- Per-email switch: WooCommerce, Settings, Emails, template, "Enable this email notification".
- Log: WooCommerce, Status, Logs, source `transactional-emails`; statuses Sent, Failed, Disabled, Skipped; sent and failed also appear as private order notes; disabled and skipped only in the log; raw addresses not logged (username or "guest"); missing entries, check Logs, Settings.
- Admin and WordPress password-reset emails may not appear in the log; use the SMTP provider's logs or a mail logging tool.
- From address on your own domain; free-mail From (Gmail, Yahoo) often marked spam or blocked (also https://woocommerce.com/document/email-authentication/ , cited only as background, not linked).
- SPF, DKIM and DMARC definitions and the host-or-SMTP-service setup advice (email-authentication doc). Authentication worthwhile even for transactional-only senders because other providers are likely to follow Google and Yahoo.
- Google (https://support.google.com/mail/answer/81126): rules effective Feb 1, 2024; all senders SPF or DKIM, valid forward and reverse DNS (PTR), TLS, spam rate below 0.3% in Postmaster Tools (recommended below 0.10%), RFC 5322 format; more than 5,000 messages a day to Gmail also needs SPF, DKIM and DMARC (policy may be none), aligned From domain, and one-click unsubscribe for marketing mail.
- Yahoo (plain text only, verified in research D7): comparable authentication and spam-rate requirements from February 2024.

Virtina-derived judgment (flag as opinion, not citation): staging-first conflict testing; the developer-trigger list; the handoff package. Phrase as "in practice" or "a developer will ask for", not as a cited fact.

## 9. Semantic terms (13 minimum, 15 target, natural prose only)

transactional emails, `wp_mail()`, SMTP service, SPF record, DKIM signature, DMARC policy, From address, domain alignment, spam folder, Pending payment, Processing status, email log, test order, reverse DNS (PTR), mailbox provider, deliverability, staging site, plugin conflict, fatal error, password reset email. (Pick 15 and confirm in the draft; the creator lists the ones used.)

## 10. Image plan

Rules: Pexels first (needs PEXELS_API_KEY; if absent, Openverse cc0 with provider ranking), preview each candidate visually, 4 different photo shoots, no reuse. Excluded because used on the other two drafts: Pexels or Unsplash IDs 4487383, 7735708, 4483941, 7988674, 14020705, 6214472, 7857567, 5833238. Also avoid warehouse, containers, handshake, spreadsheet-with-pen scenes. Upload to virtina.com media; every src starts `https://virtina.com/wp-content/uploads/`.

| Slot | Size | Scene to find | Search queries | Placement | Alt text (80 to 150 chars) |
|---|---|---|---|---|---|
| Featured | 1309x500 | Laptop with an email inbox open, desk, wide composition with room to crop | "laptop email inbox desk", "email inbox laptop office" | Top of post | Store owner checking an email inbox on a laptop after WooCommerce order emails stopped sending |
| Body 1 | 670x352 | Person at laptop checking an order or order list | "person laptop online order", "checking orders laptop desk" | After H2 1 | Online store manager reviewing a new customer order on a laptop to see whether the confirmation email was sent |
| Body 2 | 670x352 | Laptop dashboard with charts or admin screen, hands on keyboard | "laptop dashboard analytics desk", "website admin dashboard laptop" | After H2 3 | Laptop screen showing a store dashboard while the owner checks the WooCommerce email log for failed notifications |
| Body 3 | 670x352 | Support person or developer at a desk with monitors and code | "developer desk monitors code", "support agent headset desk" | Inside H2 7 | Support developer at a desk reviewing server mail settings and DNS records to fix WooCommerce order emails |

Constraints: JPEG q82, under 200 KB each, scale-to-cover plus centre-crop, `width="670" height="352"` and all data attributes per Template G, `loading="lazy"`, real `data-id`. Set `featured_media` to the uploaded featured ID (never 0). Alt lengths above are about 95 to 115 characters; re-count before upload. Visually QA that no screen shows a readable brand, no stray text, no hands-on-mouse generic stock that does not suit the scene.

## 11. Pre-push gates the publisher must run (in addition to section 9 of MUST-FOLLOW-RULES)

- 8-gram dedup against all live and local Virtina posts with `<style>` blocks and inline styles stripped. Watch strings: "default WordPress email function", "host limits outgoing mail", "From address is valid and actually exists", any "builds on WooCommerce" platform sentence.
- Blocking regex: no plugin or provider names (for example SMTP plugin brand names, mail tester, Postmark/SendGrid class names), no `cron`, `Action Scheduler`, `PHPMailer`, `blocks PHP mail`, no percent signs other than `0.3%` and `0.10%` (if used), no digits followed by `%` elsewhere, no "our ", "we offer", "contact us", "reach out", "check out".
- Counts: 7 body H2s with ids matching TOC; at least 6 H3s (plan has 12 body H3s plus 4 PAA H3s); 9 or 10 internal links, 2 external; 0 internal links in Summary, Introduction, PAA, Conclusion, FAQ.
- Readability: Flesch calibrated against the Virtina corpus, 0 sentences over 20 words, 0 paragraphs over 3 sentences.
- Yoast fields sent in `meta` on push (`yoast_wpseo_title`, `yoast_wpseo_metadesc`, `yoast_wpseo_focuskw`), verified with a `context=edit` GET.
- Thrive: `_tve_updated_post` is not REST-writable; the post carries semantic HTML and needs one open-and-save in Thrive Architect before it renders correctly. Flag to the user.

## 12. Locked versus creator judgment

**Locked:** thesis, H1, slug, Yoast title, meta, focus keyword, categories, Format D, the seven body H2 headings and their first sentences, link URLs and anchors, external links, image plan, banned items list, the four-status bullet set, the handoff and trigger criteria.

**Creator judgment:** wording of H3 openers beyond the headings given, examples inside the illustrative case, the exact content of the table cells, which 15 semantic terms are used, the intro's opening hook (no statistics), whether to add the optional 10th link, the Conclusion's closing line.

## 13. Risks

- **Overlap with post 40347.** Mitigation: stage-based structure, no plugin names, link it once as a broader bug list.
- **Service links read as pitch.** Mitigation: state each as a fact tied to a specific failure; no possessives.
- **Word count creep** from 12 H3s and a table. Budgets above sum to about 2,450; cap the table at 4 short rows and keep each H3 to about 100 words.
- **Stale or contested claims.** Google and Yahoo pages carry no visible updated date; date every claim "since February 2024". The log's introduction version is unknown; the post says "current WooCommerce versions".
