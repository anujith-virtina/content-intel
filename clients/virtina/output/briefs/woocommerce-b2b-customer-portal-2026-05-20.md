---
title: Content Brief — WooCommerce B2B Customer Portal
client: virtina
date: 2026-05-20
topic: B2B customer self-service portal for WooCommerce
audience: B2B ecommerce decision-makers — manufacturers, distributors, wholesalers running WooCommerce
stage: brief
slug: woocommerce-b2b-customer-portal
format: Format B — Conversational Q&A
---

# Content Brief: WooCommerce B2B Customer Portal

---

## 1. Format choice and rationale

**Selected format: Format B — Conversational Q&A (LLM-style)**

**Rationale:** The research surfaced 10 distinct buyer questions that WooCommerce B2B decision-makers type into Google or ask an AI. Each question is independently answerable in 200-400 words. The Q&A structure maps directly to how LLMs cite content: a verbatim buyer question as H2 becomes the exact prompt an AI matches against. No competitor article uses this format for WooCommerce-specific B2B portal content. The topic is naturally decision-guide shaped (each answer raises the next logical question), which is the exact use case for Format B per MUST-FOLLOW-RULES.md section 11.

**Format overuse check:**
- All 10 of the last 10 published Virtina posts used Format A (standard explanatory). Format A is overused; this post must NOT use Format A.
- Format B: zero uses in last 10 posts. Clear to use.
- No FAQ accordion (Template J) is added to Format B articles. The H2 questions ARE the article — do not append a separate FAQ section.

**User explicitly requested Format B.** This overrides any other consideration.

---

## 2. Thesis statement

Your WooCommerce store's built-in account page is not a B2B customer portal, and the gap between the two is why your buyers still call instead of reorder — this article explains what a real portal includes, which plugins build it on WooCommerce, what it costs and how long it takes, and when the ROI math actually works.

---

## 3. Target keyword and secondary keywords

**Primary keyword:** B2B customer portal WooCommerce

**Secondary keywords:**
- WooCommerce B2B account management
- B2B self-service portal ecommerce
- WooCommerce wholesale portal
- B2B buyer portal manufacturers distributors
- B2BKing WooCommerce B2B
- Wholesale Suite WooCommerce B2B
- WooCommerce B2B plugin

**Slug:** `woocommerce-b2b-customer-portal` (confirmed unique — no existing Virtina post uses this slug or any near-match)

---

## 4. Competitor being outperformed and why this article beats it

**Primary competitor:** shopify.com/enterprise/blog/b2b-customer-portal

**Why Virtina's article beats it:**
Shopify's guide is strong on data (83% self-service preference, Dermalogica 3x reorder rate) but advocates for Shopify exclusively. A WooCommerce operator reading it gets zero actionable guidance. Virtina's Q&A article answers the specific questions a WooCommerce B2B buyer asks before commissioning a portal build — real plugin names, real timelines, real cost ranges, and the "when not to build" angle that no competitor article covers. The Q&A structure also outperforms Shopify's narrative format for LLM/AI citation, because AI reads question-matched sections as authoritative answers rather than scanning for buried data points.

**Secondary competitors to outperform:**
- chatty.net/blog/b2b-self-service-portal — good data, no WooCommerce specifics
- wizcommerce.com/b2b-customer-portal — 12 H2 sections of product marketing, no WooCommerce plugin context, no "when not to build" guidance

---

## 5. H2 questions — final selection and order

All 10 questions from the research pass the uniqueness check. None duplicate an H2 from any existing Virtina post. All 10 are included below, ordered for logical Q&A flow (definition > problem > features > plugins > cost/time > specific capabilities > ERP dependency > ROI > when not to build > adoption).

The TOC entry (shortened version) follows each question in brackets.

---

### H2-1: What exactly is a B2B customer portal, and is it different from my WooCommerce account page?

**TOC entry (5-7 words):** What is a B2B customer portal?

**Anchor ID:** `what-is-b2b-portal`

**Direct opening answer (1-2 sentences):**
A B2B customer portal is a private, account-specific dashboard where your buyers can check order status, download invoices, view their contract pricing, and reorder without calling anyone — and it is very different from the standard WooCommerce "My Account" page, which was built for individual consumers, not company accounts.

**What the answer must cover:**
- The standard WooCommerce "My Account" page: what it includes by default (order history, basic account settings, simple login). Fine for B2C; inadequate for B2B.
- What makes a B2B portal different: company account hierarchy (multiple users under one corporate account with different permission levels), buyer-specific pricing that only shows after authenticated login, reorder tools with one-click bulk reorder from past orders, invoice management and payment terms visibility, quote request submission.
- One concrete framing: "If your buyers are logging in and seeing the same account page your retail customers see, you don't have a B2B portal."

**Word count:** 220-280 words

**Internal link candidates:**
- Post 26936 (`b2b-ecommerce-marketplace-on-woocommerce`) — anchor text suggestion: "WooCommerce's B2B flexibility" — note: confirm URL before use

---

### H2-2: Why are my B2B buyers calling the sales team instead of reordering online?

**TOC entry:** Why buyers call instead of reorder online

**Anchor ID:** `why-buyers-call-sales`

**Direct opening answer (1-2 sentences):**
Your buyers are calling because your online store does not show them their contract pricing, does not let them reorder from their order history, and does not tell them whether the SKU they need is in stock — and until those three things are true, calling a sales rep is faster than using your website.

**What the answer must cover:**
- Stat: 75% of B2B buyers prefer to purchase without a sales rep interaction (Gartner, 2025) — but self-service preference does not fix a broken self-service experience.
- The three specific feature gaps that drive phone calls: (1) pricing is wrong or missing for authenticated accounts, (2) no reorder from order history, (3) no real-time inventory visibility.
- This is a feature gap, not a buyer behavior problem. Framing: "Don't blame your customers for calling. Fix what's missing."
- Brief forward reference: these are the exact features a portal provides (covered in H2-3).

**Word count:** 220-260 words

**Internal link candidates:**
- Post 20127 (`b2b-ecommerce-challenges`) — anchor text: "top challenges B2B businesses face online" (confirm URL before use)

---

### H2-3: What does a WooCommerce B2B customer portal actually include — what are the must-have features?

**TOC entry:** Must-have B2B portal features on WooCommerce

**Anchor ID:** `b2b-portal-features`

**Direct opening answer (1-2 sentences):**
A production-ready WooCommerce B2B portal needs seven core features: company account hierarchy, contract-specific pricing display, reorder from order history, real-time inventory visibility, invoice download with payment terms, a quote request workflow, and shipment tracking — none of which WooCommerce provides out of the box.

**What the answer must cover:**
- List the 7 features using Template F bullet list format (with bold labels). For each:
  - **Company account hierarchy.** Multiple users under one company account with admin and buyer roles.
  - **Contract-specific pricing.** Each authenticated account sees only their negotiated prices — not public prices.
  - **Reorder from order history.** One-click reorder of a previous order, including quantity and SKU. Cite: repeat orders increased 33% in 6 months after enabling one-click reorder (wizcommerce.com).
  - **Real-time inventory visibility.** Live stock levels at login, not cached snapshots.
  - **Invoice and payment terms access.** PDF invoice download; net-30/60 payment terms visible.
  - **Quote request workflow.** Buyer submits quote request inside the portal; sales team responds without phone tag.
  - **Shipment tracking.** Order status and tracking number accessible without calling logistics.
- Brief note: WooCommerce provides none of these natively. They require plugins (covered in H2-4).

**Word count:** 300-360 words

**Internal link candidates:**
- Post 41511 (`ai-quote-automation-b2b-sales-delays`) — anchor text: "quote request workflow automation" — link when mentioning the quote workflow feature (confirm URL before use)

---

### H2-4: Which WooCommerce plugins actually build this — B2BKing, Wholesale Suite, or custom development?

**TOC entry:** B2BKing vs. Wholesale Suite vs. custom dev

**Anchor ID:** `woocommerce-b2b-portal-plugins`

**Direct opening answer (1-2 sentences):**
B2BKing and Wholesale Suite are the two dominant plugin paths for building a WooCommerce B2B portal, and the right choice depends on whether you need an all-in-one solution or a modular stack — custom development is the path only when both plugins reach their limits.

**What the answer must cover:**
- **B2BKing:** 137+ features in a single plugin. Covers subaccounts, tiered pricing, bulk order forms, CRM hub, role-based catalogs, B2B registration with approval workflow. 10,000+ active WooCommerce stores. Pricing: $149-$349/yr. Best for operators who want one plugin to handle the full portal with minimal configuration overhead.
- **Wholesale Suite:** A four-plugin stack (Wholesale Prices, Wholesale Order Form, Wholesale Lead Capture, Wholesale Payments). More modular — buy only what you need — but combined cost is higher and configuration requires coordinating across plugins. Better for teams with a developer on staff who wants granular control.
- **Custom development:** When neither plugin handles your specific account hierarchy, your custom ERP field mapping, or your unique catalog rule complexity. Custom adds significant cost and timeline (see H2-5). Virtina builds on top of both plugin paths and can extend either with custom code where needed.
- **The table lives here** (see section 6 below for full specification).

**Word count:** 320-400 words

**Internal link candidates:**
- Post 42108 (`woocommerce-erp-integration`) — anchor text: "WooCommerce ERP connectors" — when mentioning plugin ERP compatibility
- Post 38586 (`woocommerce-developer-for-ecommerce-success`) — anchor text: "experienced WooCommerce developer" — when mentioning custom development path

---

### H2-5: How long does it take to build a WooCommerce B2B customer portal, and what does it cost?

**TOC entry:** WooCommerce B2B portal cost and timeline

**Anchor ID:** `b2b-portal-cost-timeline`

**Direct opening answer (1-2 sentences):**
A plugin-based WooCommerce B2B portal typically takes 4-12 weeks to implement and costs $15,000-$40,000; a custom-built portal runs 3-6 months and $40,000-$80,000 — and the range depends almost entirely on whether your ERP needs to sync in real time.

**What the answer must cover:**
- Two paths with distinct timelines and costs:
  - Plugin path (B2BKing or Wholesale Suite): 4-12 weeks. $15K-$40K including configuration, design customization, testing, and QA. The low end is clean installs with simple pricing rules. The high end involves custom account hierarchy, multiple buyer roles, and moderate ERP integration.
  - Custom path: 3-6 months. $40K-$80K+. Used when plugin architecture can't support the required catalog logic, account structure, or integration complexity.
- Context: WooCommerce B2B implementation costs $46K-$135K over three years vs. $240K-$540K for Magento Commerce (nopio.com data). Even the high end of WooCommerce custom is a fraction of enterprise alternatives.
- What drives cost up: real-time ERP sync (adds 4-8 weeks), custom account hierarchy beyond what plugins support natively, buyer-specific catalog rules at SKU level (thousands of pricing rules = database load).
- Note to creator: these are Virtina's working ranges based on research. Do not present as guarantees. A real scoping call determines actual cost.

**Word count:** 280-340 words

**Internal link candidates:**
- None required for this section specifically. Can include post 42108 if mentioning ERP sync complexity.

---

### H2-6: Can a WooCommerce portal show each buyer their own pricing and catalog without exposing prices to other accounts?

**TOC entry:** Account-specific pricing without exposure

**Anchor ID:** `account-specific-pricing`

**Direct opening answer (1-2 sentences):**
Yes — both B2BKing and Wholesale Suite support role-based pricing that displays contract prices only when the correct buyer account is authenticated, and hidden catalog mode prevents unauthenticated visitors or wrong-account logins from seeing any pricing at all.

**What the answer must cover:**
- How role-based pricing works: each buyer account (or buyer role/tier) is assigned a price ruleset. When the buyer logs in, prices update to their contract rates. No other account sees those rates.
- Hidden catalog: guest visitors and non-portal buyers see no prices (or see a "log in to see pricing" message). This is critical for distributors with negotiated rates that differ by customer.
- Practical concern for distributors: if you sell the same SKU to three customers at three different price points, the portal must enforce this cleanly. Both plugins handle this, but the data setup (mapping each account to the correct price tier) requires careful configuration — it's not automatic on installation.
- Brief mention: this is one of the most common questions Virtina receives from distributors considering a portal project. The answer is yes, but the configuration must be done correctly.

**Word count:** 240-280 words

**Internal link candidates:**
- Post 42074 (`woocommerce-b2b-performance-fix`) — anchor text: "portal page load speed" — if mentioning that large price-rule sets can slow page load under load

---

### H2-7: Does my WooCommerce B2B portal need to connect to my ERP, and how hard is that?

**TOC entry:** Does your portal need ERP integration?

**Anchor ID:** `portal-erp-integration`

**Direct opening answer (1-2 sentences):**
If your pricing or inventory changes more than once a week, yes — without ERP sync, your portal shows stale data and buyers will stop trusting it within the first month.

**What the answer must cover:**
- The core problem with no ERP sync: portal inventory shows numbers that diverge from actual warehouse stock as soon as an order ships, a return is processed, or a price contract is updated. Buyers who discover stale data revert to phone calls. The portal undermines itself.
- What ERP sync does: pushes real-time stock levels and contract pricing from the ERP into WooCommerce so the portal always reflects current data. Pulls orders back into the ERP so fulfillment runs in one system.
- ERP compatibility: NetSuite, SAP Business One, Epicor, Infor all have documented WooCommerce connectors. Timeline: ERP integration adds 4-8 weeks to any portal project.
- The exception: if pricing is static and inventory turns slowly (updated weekly), a scheduled sync (daily batch) may be sufficient and avoids the complexity of real-time middleware.
- Internal link to post 42108 here — this is the natural cross-link point.

**Word count:** 250-300 words

**Internal link candidates:**
- Post 42108 (`woocommerce-erp-integration`) — anchor text: "connect WooCommerce to your ERP" — REQUIRED link in this section
- Post 37434 (`guide-on-woocommerce-rest-api`) — anchor text: "WooCommerce REST API connections" — when mentioning API-based ERP integration

---

### H2-8: What does a B2B portal actually do to my sales rep workload and customer service costs?

**TOC entry:** Impact on sales rep time and support costs

**Anchor ID:** `portal-roi-operations`

**Direct opening answer (1-2 sentences):**
The math is straightforward: a portal-processed order costs $1-3 to handle versus $30-60 for a phone or email order, and when buyers can reorder, track shipments, and download invoices themselves, your support ticket volume drops 30-50%.

**What the answer must cover:**
- Specific numbers from research:
  - Order processing cost: $1-3 (portal) vs. $30-60 (manual). Source: chatty.net.
  - Support ticket reduction: 30-50% (chatty.net).
  - Sales rep admin time: 26% of rep time goes to administrative tasks that portal self-service eliminates (Forrester via chatty.net).
  - SKU breadth: portal customers buy 25% more SKUs than non-portal customers (Adelco case, Commercetools).
  - Repeat orders: one-click reorder increased repeat orders 33% in 6 months (wizcommerce.com).
- What happens to freed sales rep time: they shift from order-taking and status calls to account expansion, new relationship development, and consultative selling.
- Frame this as operational leverage, not headcount reduction. Sales reps don't disappear — they stop being expensive order clerks.

**Word count:** 250-300 words

**Internal link candidates:**
- Post 41808 (`ecommerce-site-search-optimization`) — anchor text: "portal search and catalog navigation" — if mentioning how search within the portal improves buyer SKU discovery
- Post 20127 (`b2b-ecommerce-challenges`) — anchor text: "B2B buyer experience expectations" (confirm URL before use)

---

### H2-9: When does a WooCommerce B2B portal NOT make sense — are there situations where we shouldn't build one?

**TOC entry:** When not to build a B2B portal

**Anchor ID:** `when-not-to-build-portal`

**Direct opening answer (1-2 sentences):**
A portal does not pay off when your buyers order fewer than four times per year, when your catalog has under 50 SKUs, or when your sales process is inherently consultative — in those cases, the investment in portal infrastructure will not recover its cost.

**What the answer must cover:**
- Three specific situations where a portal is the wrong call:
  - **Low order frequency.** If your average buyer orders fewer than 4 times per year, the self-service efficiency gain is too small to justify $15K-$80K. The math requires volume.
  - **Small catalog.** If you have fewer than 50 SKUs, the browsing and reorder complexity a portal solves does not exist. A simple contact form and a PDF price list serve these buyers better.
  - **Consultative buying processes.** Capital equipment, custom manufacturing, and engineered-to-order products require a sales conversation regardless of what the portal can do. A portal won't replace that — it will just add friction.
- Virtina's position: this is the "when not to build" guidance that no competitor article provides. Being honest about this builds trust with decision-makers who are genuinely evaluating fit.
- Note to creator: this is the contrarian angle that differentiates the article. Do not soften it. The point is that a portal is not universally the right answer, and saying so directly builds credibility.
- Flag: the three criteria are logical reasoning, not published data. Present as Virtina's implementation experience, not cited research.

**Word count:** 260-300 words

**Internal link candidates:**
- Post 39589 (`b2b-ecommerce-for-manufacturers`) — anchor text: "B2B ecommerce for manufacturers" — when framing this for the manufacturing buyer segment (confirm URL before use)

---

### H2-10: How do I get my B2B buyers to actually use the portal instead of calling their account rep?

**TOC entry:** Getting buyers to use the portal

**Anchor ID:** `buyer-portal-adoption`

**Direct opening answer (1-2 sentences):**
Buyer adoption is the most underdiscussed problem in B2B portal implementation — you can build a technically perfect portal and still have buyers defaulting to phone calls six months later, because adoption is a change management problem, not a feature problem.

**What the answer must cover:**
- The adoption gap: none of the 6 competitor articles reviewed address this. It is the most common post-launch problem Virtina sees.
- Four specific tactics:
  1. **Show buyers their contract pricing is online before go-live.** Many B2B buyers don't know their negotiated rates are accessible in the portal. Proactively show this in the onboarding email — "Log in now to see your account pricing."
  2. **Demonstrate one-click reorder in the onboarding sequence.** The biggest friction reducer. Walk buyers through it with a 60-second video or a guided first-login walkthrough.
  3. **Keep a human fallback for the first 90 days.** Don't cut off account rep access at portal launch. Let buyers self-serve AND still call. Over 90 days, self-service becomes the default for routine orders.
  4. **Track portal activity by account.** Know which buyer accounts are not logging in by month 2. Have your rep follow up with those accounts specifically — personalized outreach outperforms generic "don't forget your portal" emails.
- Closing point: adoption is the difference between a portal that pays off and one that sits unused. The technology is the easy part.

**Word count:** 290-360 words

**Internal link candidates:**
- Post 42074 (`woocommerce-b2b-performance-fix`) — anchor text: "portal page speed" — if noting that slow portal load kills adoption
- Post 38586 (`woocommerce-developer-for-ecommerce-success`) — anchor text: "WooCommerce development partner" — brief mention when discussing portal configuration support

---

## 6. Table specification

**Table title:** WooCommerce B2B portal: out-of-the-box vs. B2BKing vs. Wholesale Suite vs. custom development

**Which H2 section:** Appears inside H2-4 ("Which WooCommerce plugins actually build this?") after the intro paragraph and before the bullet discussion of custom dev.

**Format:** Standard HTML table. Creator uses Gutenberg `wp:table` block markup with standard table HTML. No special Virtina template for tables — use clean semantic HTML inside the section div.

**Columns (5 columns):**
| Feature | WooCommerce (default) | B2BKing | Wholesale Suite | Custom dev |

**Rows (what to compare):**

| Feature | WooCommerce (default) | B2BKing | Wholesale Suite | Custom dev |
|---|---|---|---|---|
| Company account hierarchy | No | Yes | Partial (with add-ons) | Yes |
| Role-based / contract pricing | No | Yes | Yes | Yes |
| Bulk / quick order form | No | Yes | Yes | Yes |
| Reorder from order history | Basic (no bulk reorder) | Yes | Yes | Yes |
| Invoice download | No | Yes | No (requires add-on) | Yes |
| Quote request workflow | No | Yes | No | Yes |
| B2B registration with approval | No | Yes | Yes (via Lead Capture plugin) | Yes |
| Real-time ERP sync support | No | Via third-party connector | Via third-party connector | Yes (custom) |
| Annual cost (plugin only) | Free | $149-$349/yr | $300-$600/yr (stack) | Project-based |

**Notes for creator:**
- "Partial" and "Via third-party connector" entries should not have a checkmark or X — use the text as written.
- Do not add a "winner" column. Let the table speak for itself.
- Table caption (below table): "Feature comparison as of 2026. Plugin capabilities subject to vendor updates."
- This table is the primary scannability element of the article. Format it clearly.

---

## 7. Image plan

### FEATURED IMAGE
- **Section:** Featured / hero (above H1 or as WordPress featured image)
- **Literal subject:** A business professional — mid-career, business casual — seated at a desk with a laptop showing a dashboard or account management screen with order lists and data visible. Clean, bright office environment. No text overlaid on image.
- **Pexels search:** `business professional laptop dashboard office`
- **Dimensions:** 1309x500 px (crop-resized after download)
- **Alt text (80-150 chars):** `Business professional reviewing a B2B customer portal dashboard on a laptop in a modern office workspace`
- **Alt text char count:** 101 chars — within range.

---

### BODY IMAGE 1
- **Section:** Under H2-3 ("What does a WooCommerce B2B customer portal actually include?") — place after the bullet list, before the closing paragraph
- **Literal subject:** A warehouse worker or fulfillment team member in a high-visibility safety vest scanning or checking inventory shelves in a storage aisle. Shelving with boxes or pallets visible in background. This represents the inventory visibility and order management context of the portal features.
- **Pexels search:** `warehouse worker inventory shelves`
- **Dimensions:** 670x352 px
- **Alt text (80-150 chars):** `Warehouse worker in high-visibility vest checking inventory shelves representing B2B order and stock management`
- **Alt text char count:** 110 chars — within range.

---

### BODY IMAGE 2
- **Section:** Under H2-5 ("How long does it take to build a WooCommerce B2B customer portal, and what does it cost?") — place after the cost range paragraph, before the "what drives cost up" bullet
- **Literal subject:** A small business or agency team of 2-3 people seated at a table reviewing documents or a laptop screen together. The image conveys a project kickoff or implementation scoping meeting. Business casual dress, visible laptop or papers on table.
- **Pexels search:** `business team meeting laptop table`
- **Dimensions:** 670x352 px
- **Alt text (80-150 chars):** `Small business team reviewing WooCommerce portal implementation plans at a meeting table with laptop and documents`
- **Alt text char count:** 116 chars — within range.

---

### BODY IMAGE 3
- **Section:** Under H2-10 ("How do I get my B2B buyers to actually use the portal?") — place after the four-tactic bullet list, before or after the closing paragraph
- **Literal subject:** A business person — could be a sales rep or account manager — at a desk speaking on a phone or headset while looking at a laptop or monitor showing data. Represents the account rep still present as a fallback during portal onboarding. Office setting.
- **Pexels search:** `business person phone laptop office desk`
- **Dimensions:** 670x352 px
- **Alt text (80-150 chars):** `Account manager at a desk on a phone call while reviewing customer account data on a laptop representing B2B portal onboarding support`
- **Alt text char count:** 138 chars — within range.

---

## 8. Internal links plan

All internal links go in body sections only. Not in intro, not in conclusion. Use Template L (no target attribute, `style="outline: none;"`). Maximum 2 external links in the entire article.

**7 internal links selected from the 10 research candidates:**

| # | Post slug | Anchor text suggestion | Which H2 section |
|---|---|---|---|
| 1 | `woocommerce-erp-integration` | "connect WooCommerce to your ERP" | H2-7 (ERP integration section) — REQUIRED |
| 2 | `woocommerce-erp-integration` | "WooCommerce ERP connectors" | H2-4 (plugin section, when discussing ERP compatibility) |
| 3 | `woocommerce-b2b-performance-fix` | "portal page load speed" | H2-6 or H2-10 (when mentioning slow portals killing adoption/buyer trust) |
| 4 | `guide-on-woocommerce-rest-api` | "WooCommerce REST API connections" | H2-7 (API-based ERP integration) |
| 5 | `woocommerce-developer-for-ecommerce-success` | "experienced WooCommerce developer" | H2-4 (when discussing custom development path) |
| 6 | `ai-quote-automation-b2b-sales-delays` | "quote request workflow" | H2-3 (when listing quote workflow as a portal feature) |
| 7 | `b2b-ecommerce-marketplace-on-woocommerce` | "WooCommerce's B2B capabilities" | H2-1 (when establishing what WooCommerce can and cannot do for B2B) |
| 8 | `b2b-ecommerce-for-manufacturers` | "B2B ecommerce for manufacturers" | H2-9 (when-not-to-build section, manufacturer framing) |

**Notes:**
- Links 1 and 2 both go to the same post (`woocommerce-erp-integration`). This is acceptable — it's the closest companion post in the Virtina catalog and two distinct anchor texts justify two links.
- Confirm all URLs are live before publishing. Suggested URL pattern: `https://virtina.com/{slug}/`
- The three research candidates not selected (posts 20127, 41808, 39941) are excluded either because the anchor moment is weaker or the section where they would appear is already link-dense.

---

## 9. Word count target

**Target: 2,200-2,700 words**

Breakdown:
- Intro (Template B): 80-120 words
- H2-1 through H2-10: 200-360 words each = approx. 2,600 words at midpoints
- Table (inside H2-4): does not add to word count significantly
- PAA block (Template H): 3-4 questions, 2-4 sentences each = approx. 120-180 words
- Conclusion (Template I): 2 paragraphs, 60-100 words

**Note:** This is a standard post (not a pillar guide), so word count stays at 2,200-2,700. The upper bound for pillar guides (2,500-3,500) does not apply. 3 body images are appropriate at this length. Do not pad to hit a higher count.

---

## 10. Pre-brief uniqueness confirmation

**Uniqueness audit file:** `C:\content-intel\clients\virtina\output\research\uniqueness-audit-2026-05-20.md`

**All 5 uniqueness checks — PASSED:**

| Check | Result | Notes |
|---|---|---|
| 1. Topic uniqueness | PASS | No existing Virtina post covers B2B customer self-service portal as primary subject |
| 2. Angle uniqueness | PASS | No existing post argues the WooCommerce-specific, plugin-comparison, "when not to build" angle |
| 3. Keyword uniqueness | PASS | "B2B customer portal WooCommerce" does not appear as focus term in any existing post title or excerpt |
| 4. Phrasing uniqueness | PASS (to be re-verified by publisher after draft) | No 8-word sequences from research notes match existing post excerpts; publisher must verify draft |
| 5. Structural uniqueness | PASS | Format B not used in any of last 10 published posts |

**Closest existing post:** ID 26936, `b2b-ecommerce-marketplace-on-woocommerce`, "Customization of the B2B eCommerce Marketplace on the WooCommerce Platform" (2022). Covers multi-vendor marketplace customization — different topic (supplier side vs. buyer-facing account UX), different audience problem (marketplace operator setup vs. B2B buyer self-service), different thesis. Zero duplication risk.

**Second closest:** ID 42108, `woocommerce-erp-integration` (May 11, 2026). Covers system-to-system ERP data sync. This post covers buyer-facing portal UX, features, and ROI. Complementary, not duplicative — the two posts cross-link naturally.

**Slug confirmed unique:** `woocommerce-b2b-customer-portal` does not match any existing slug in the 303-post inventory.

---

## 11. Banned words and style reminders for the creator

### Banned words — zero tolerance
- Em dashes (— U+2014) and `&mdash;` — replace with periods, commas, colons, or hyphens. No exceptions.
- Hype words: revolutionary, game-changing, best-in-class, cutting-edge, world-class, industry-leading, transform your, unlock value, synergize
- Filler words: delve, leverage, navigate (as verb), realm, landscape, ecosystem
- Filler phrases: "in today's fast-paced world," "it's important to note," "in conclusion," "to summarize," "in the world of," "as we know"

### Headings — sentence case only
Correct: `What exactly is a B2B customer portal, and is it different from my WooCommerce account page?`
Wrong: `What Exactly Is A B2B Customer Portal, And Is It Different From My WooCommerce Account Page?`

Apply sentence case to every H2, H3, and H4 in the article.

### Voice rules
- Second person ("you," "your buyers," "your sales team") throughout body prose
- Active voice — not "the portal will be configured by your developer" but "your developer configures the portal"
- Contractions are fine: "don't," "it's," "you're"
- Short paragraphs: 2-3 sentences maximum per paragraph
- Lead each section with the direct answer first (Format B rule) — do not build up to the answer; give it in sentence 1

### Citation rules
- Gartner stat: "75% of B2B buyers prefer to purchase without a sales rep interaction (Gartner, 2025)" — do not inflate to 83%
- Quote citations: under 15 words verbatim; paraphrase longer quotes
- Two external links maximum across the entire article. Choose the two most important sources. All other citations are paraphrased without a hyperlink or cited as "per [source name]" in plain text.
- Never link to competitor domains: shopify.com, bigcommerce.com, etc.
- Internal Virtina links: Template L — no target attribute, `style="outline: none;"`

### Bullet list formatting
All bullet lists in the body use Template F (CSS circle pattern). No default browser bullets anywhere. Creator must copy the exact Template F HTML from `html-templates.md` — do not improvise.

### Table formatting
The comparison table in H2-4 uses clean semantic HTML table inside the section div. No special Virtina template for tables. Table caption required below the table.

### Format B structural rules — for creator
- H2 questions are the article structure. There is no FAQ accordion (Template J) at the end.
- TOC entries are shortened versions of each H2 question (5-7 words each). Use the TOC entry text specified in section 5 above.
- Every H2 has the anchor ID specified in section 5. The TOC href matches the anchor ID exactly.
- Summary block (Template A) is a 3-5 sentence overview that an AI can read as a standalone synopsis of the full article.
- Intro block (Template B) sets up the problem (buyers calling instead of reordering online) before H2-1. It does not repeat the H2-1 answer — it establishes the stakes.
- PAA block (Template H) comes after H2-10, before the Conclusion.
- Conclusion (Template I) closes on white text over `#00d5c0` teal background. No "in conclusion" phrase.
- No author bio (Template K) needed in the draft — publisher adds this.

### What the creator must NOT do
- Do not write a generic "what is a portal" intro that repeats publicly available definitions. Start with the problem this specific audience faces (buyers calling instead of reordering).
- Do not soften the "when not to build" section (H2-9). The whole point is that Virtina is honest about when the investment is not worth it. Hedge language undermines this.
- Do not name any Virtina competitor agencies (Absolute Web, Coalition Technologies, etc.) anywhere in the article.
- Do not link to Shopify, BigCommerce, or any competitor platform domain — not even as a citation.
- Do not reference the Dermalogica case study with a Shopify link. Paraphrase the outcome without the link.
- Do not claim Virtina has a specific portal case study unless the internal team confirms a specific client outcome. Use "Virtina's implementation experience" language instead.
- Do not write more than 400 words for any single H2 section. If a section is running long, cut the weakest supporting point.
- Do not invent plugin prices. B2BKing: $149-$349/yr. Wholesale Suite: $300-$600/yr (stack). Mark these as approximate and subject to change.
- Do not use semicolons anywhere in the article.

---

## 12. SEO metadata (for publisher)

**Yoast SEO title (max 60 chars):** `WooCommerce B2B Customer Portal Guide | Virtina`
- Char count: 49 chars — within limit.

**Yoast meta description (150-160 chars):** `Learn what a WooCommerce B2B customer portal includes, which plugins build it, what it costs, and how to get your buyers to stop calling and start self-serving.`
- Char count: 160 chars — at upper limit.

**WordPress status:** `draft` (never auto-publish)

**Category suggestions:** WooCommerce, B2B eCommerce (use existing Virtina taxonomy)

**Tag suggestions:** WooCommerce B2B, customer portal, B2BKing, Wholesale Suite, B2B self-service, buyer portal (use existing tags where available)

---

*Brief authored: 2026-05-20. Creator should not deviate from H2 question text, anchor IDs, or image specifications without flagging to the orchestrator first.*
