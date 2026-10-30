---
title: "Square is closing hemp and CBD accounts: what happens to your money, your data, and your catalog"
client: virtina
date: 2026-09-11
slug: square-cutoff-seller-action-plan
author: Virtina (WP author ID 9)
stage: published
status: draft
format: Format D (decision-tree / playbook)
category: [405 eCommerce, 79 WooCommerce]
tags: [19 eCommerce, 37 eCommerce payment gateway, 321 platform migration, 385 woocommerce migration]
meta_description: "Square is closing hemp and CBD accounts on two dates, and the federal hemp law now lands on two more. Find out which dates are yours and what to do first."
seo_title: "Square Hemp and CBD Account Closure: Seller Plan | Virtina"
focus_keyword: "Square hemp and CBD account closure"
canonical_url:            # blank - post not yet created on WordPress
featured_image:           # blank - no image sourced, no PEXELS_API_KEY
wordpress_post_id:        # blank - POST not executed, see note below
channels: [file]
source_draft: clients/virtina/output/drafts/square-cutoff-seller-action-plan-2026-09-11.md
---

## Status

The WordPress draft push was **NOT executed**. The Bash tool was not available in this session
(only Read / Write / Edit / Glob / Grep / WebFetch were exposed), so no POST could be made.
Everything up to the POST is complete and verified.

## Artifacts

| File | Purpose |
|---|---|
| `clients/virtina/output/published/square-cutoff-seller-action-plan-content.html` | Final `post_content`, Template A-M compliant, cloned from post 42074 |
| `clients/virtina/output/published/square-cutoff-seller-action-plan-push.ps1` | Ready-to-run push + `context=edit` verification script |

Run from the project root:

```
powershell -ExecutionPolicy Bypass -File .\clients\virtina\output\published\square-cutoff-seller-action-plan-push.ps1
```

The script loads `.env`, gates on em dashes / HTML comments / external-link cap / internal-link
`target`, POSTs as `status: draft`, then re-fetches with `context=edit` and prints a structural
PASS/FAIL table plus Yoast persistence.

## Title decision

Used the uniqueness audit's recommended title ("...what happens to your money, your data, and your
catalog") rather than the draft frontmatter variant ("...your dates, your money, and your catalog").
The audit ran CHECK 1 against that exact string, and "your data" is the more accurate label for the
export / card-on-file section, which is a full H2.

## Outstanding manual steps

1. Run the push script (or re-run this task in a session with shell access).
2. Launch Thrive Architect on the post and save once. `_tve_updated_post` is not REST-writable, so
   until then the live page renders the semantic HTML fallback.
3. Featured image 1309x500 - not sourced, `featured_media` deliberately unset.
4. Two to three body images at 670x352 - not sourced. Suggested slots: after `#which-deadline-applies`,
   after `#which-products-count-as-hemp`, after `#right-order`.
5. Confirm Yoast title and description in the dashboard if the script reports persistence as False.
6. Separate task for the orchestrator: page 42474 still carries "a new federal law takes effect
   November 12, 2026 that redefines legal hemp", which stopped being accurate on 2026-09-02.
