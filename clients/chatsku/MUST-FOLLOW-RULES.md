# ChatSKU Blog — Mandatory Rules (Locked Memory)

This file is the source of truth for every ChatSKU blog. Every agent (researcher, analyzer, creator, publisher) MUST read this file in full at the start of every ChatSKU task. These rules were established at client onboarding in May 2026. Do not deviate.

## Reference posts (gold standards)

- Post 151: https://chatsku.com/rfq-automation-manufacturers/ — RFQ automation guide (most complete structure)
- Post 1: https://chatsku.com/pdf-catalog-sales-liability/ — catalog pain narrative

Local cached copy: `clients/chatsku/reference/post-151-working.html`. Refresh every 30 days or after manual updates.

## Authoritative sub-files

- `clients/chatsku/brand-primary.txt` — verified brand accent hex (#00C9B1) and full color palette
- `clients/chatsku/body-font-size.txt` — verified body font-size (16px), line-height (1.6), image dimensions (860×452)
- `clients/chatsku/reference/published-posts-inventory.md` — all existing chatsku.com posts for uniqueness checks
- `clients/chatsku/style/voice.md`, `audience.md`, `brand.md`, `cms.md`, `examples.md` — content and publishing rules

## Tech stack note (critical)
ChatSKU uses WordPress + **Elementor 4.0.3 page builder**. Every post is built as an Elementor page (not a standard WordPress post). This means:

### What the publisher MUST do (verified from post 151)
Every ChatSKU post requires THREE things pushed via REST API — not just `content`:

1. **`content`** — standard HTML (semantic `<h2>`, `<p>`, `<ul>` etc.) as the fallback
2. **`meta._elementor_data`** — the full Elementor widget JSON (sections → columns → widgets)
3. **`meta._elementor_edit_mode`** = `"builder"` and **`meta._elementor_template_type`** = `"wp-post"`

Without `_elementor_data`, posts render as plain WordPress content — NOT matching the site design.

### Elementor widget structure (verified from post 96)
Each H2 section = one Elementor section with a 100% column containing:
- **heading widget** (H2, `title_color: "#1a1a2e"`, `font_size: 28px`)
- **text-editor widget** (HTML paragraphs/lists)
- **image widget** (when a body image belongs in that section) — **MUST come AFTER text-editor, never before**

**CRITICAL — widget order**: image widget MUST be the last widget in the column (after text-editor). If image precedes text-editor, Elementor prepends the image into the text-editor's rendered div, causing a doubled image on the page. This is a confirmed Elementor 4.0.3 rendering bug.

H3 sub-headings (PAA questions, FAQ questions, section sub-heads):
- Separate **heading widget** (`header_size: "h3"`, `title_color: "#1a1a2e"`, `font_size: 22px`)

Image widget settings:
```json
{"image": {"id": MEDIA_ID, "url": "...", "alt": "...", "source": "library", "size": ""},
 "align": "center", "width": {"size": 100, "unit": "%"},
 "border_radius": {"top": "10", "right": "10", "bottom": "10", "left": "10", "unit": "px"}}
```

Section color scheme (verified from post 96 — b2b-ecommerce-chatbot-dallas — the authoritative reference):
| Section type       | Background | Section padding | Notes |
|--------------------|-----------|----------------|-------|
| Executive Summary  | `#f9f9fb` | 60px top/bottom | Light gray |
| Introduction       | `#ffffff` | 60px top/bottom | White |
| Body sections      | cycle: `#f0f4ff` / `#ffffff` / `#f9f9fb` / `#ffffff` | 60px top/bottom | Starting at `#f0f4ff` |
| PAA section        | (next in cycle) | 60px top/bottom | |
| Conclusion         | `#1a1a2e` | 20px top / 30px bottom | Dark navy; heading `#ffffff`; body `color:#aaaacc; text-align:center; font-size:18px; max-width:720px; margin:0 auto;` |
| FAQ                | `#f9f9fb` | 60px top/bottom | Light gray |

**CRITICAL**: Section padding has NO right/left keys. All left/right padding is on the column, not the section.

Column settings (every section — verified from post 96):
```json
{
  "_column_size": 100, "width": "100",
  "padding": {"unit": "px", "top": "20", "right": "20", "bottom": "20", "left": "20", "isLinked": true}
}
```

Section settings template:
```json
{
  "background_background": "classic",
  "background_color": "<see table above>",
  "padding": {"top": "60", "bottom": "60", "unit": "px"}
}
```

### Script template
`clients/chatsku/output/research/build_elementor_post186_v3.py` — reference implementation matching post 96 structure exactly. Use as the template for every new ChatSKU post.

### What does NOT apply here
- No Thrive Architect markup
- No `!important` CSS overrides
- No SVG arrow TOC
- No inline `border-radius:50%` bullet circles
- No Virtina-style `<div>` wrappers

---

## 1. UNIQUENESS — EVERY CHATSKU BLOG MUST BE UNIQUE

Before writing any new ChatSKU blog, the creator and analyzer must verify:

### A) Topic uniqueness
- Read `clients/chatsku/reference/published-posts-inventory.md` fully
- Confirm the new topic does not duplicate any existing post's primary subject
- Existing posts: RFQ automation, lead loss from no chatbot, AI chatbot evaluation, PDF catalog problems
- All 4 existing posts are geographically tagged Dallas/DFW — new posts should not repeat this unless explicitly requested for local SEO

### B) Angle uniqueness
- The thesis must differ from any existing ChatSKU post on a related topic
- Cross-check proposed angle against inventory titles and excerpts

### C) Keyword uniqueness
- Primary keyword/slug must not match any existing slug
- Existing slugs: `rfq-automation-manufacturers`, `ai-chatbot-for-manufacturers-dallas`, `b2b-ecommerce-chatbot-dallas`, `pdf-catalog-sales-liability`

### D) Phrasing uniqueness
- After drafting, no 8-word sequence may appear verbatim in any existing ChatSKU post
- Publisher checks before any PUT call

### E) Structural uniqueness via formats
All 4 existing posts use Format A (standard explanatory). New posts should vary — use Format B, C, D, E, or F per section 11.

---

## 2. STRUCTURE (DEFAULT EXPLANATORY FORMAT)

For standard explanatory articles, use this order:

1. H1 title (sentence case)
2. Author byline + category + date
3. Featured image at 860×452 px
4. H2: Executive Summary — 2–3 paragraph overview
5. H2: Introduction — sets up the pain / scenario
6. H2: Body sections (3–6 sections, each with paragraphs and bullet lists as needed)
7. H2: People Also Ask — 3–4 Q&As using H3 for questions (NEW — adds SEO value; existing posts skip this)
8. H2: Conclusion + CTA
9. H2: Frequently Asked Questions — 4–6 Q&As (NEW — gap in existing posts; include for SEO)

Note: "Executive Summary" replaces Virtina's "Summary" label. "Introduction" stays the same. Both are standard H2 headings, no decorative box wrappers needed (Elementor handles presentation).

---

## 3. IMAGES

### Sourcing
API priority: Pexels API (PEXELS_API_KEY — shared with Virtina) > Openverse (source=stocksnap, short queries) > Wikimedia Commons.

Never: source.unsplash.com (deprecated), placehold.co, text-on-color cards.

For Openverse: use short 3–4 word queries matching stock photo naming conventions. Filter with `source=stocksnap`. Long academic queries return irrelevant results.

### Required dimensions (from post 151 — verified ChatSKU standard)
- **Featured image**: 860 × 452 px
- **Body images**: 860 × 452 px (same dimensions as featured)
- Resize method: scale-to-cover + center-crop (Pillow LANCZOS)
- File format: JPEG, quality 82, max 200 KB

### Required count
- 1 featured image
- 1–2 body images (chatsku.com posts use 2 — match this)

### Required attributes
- `featured_media` field set with real uploaded media ID, never 0
- Alt text: 80–150 chars, descriptive, includes 1–2 article keywords
- Every image `src` must begin with `https://chatsku.com/wp-content/uploads/`

### Topic keyword library
- Featured: `B2B sales team office`, `manufacturer office buyer`, `distributor warehouse desk`
- Catalog/data: `product catalog spreadsheet`, `inventory SKU computer office`
- Sales/buyer: `sales team computer screens`, `B2B sales conversation meeting`
- Quote/pricing: `business quote document desk`, `price negotiation business`
- After-hours: `laptop desk night working late`, `office empty after hours`

### Subject relevance
Images must show business/office/manufacturing/warehouse/sales scenes. Never: nature, flowers, landscapes, animals, or anything visually unrelated to B2B sales or manufacturing.

---

## 4. HEADINGS AND STRUCTURE

- Sentence case for all headings, never Title Case
- H1: article title only
- H2: major sections (Executive Summary, Introduction, body sections, FAQ, Conclusion)
- H3: sub-sections within H2 sections, also used for PAA questions
- No `id` attributes required on headings unless TOC is used
- TOC is optional for ChatSKU (existing posts don't use one) — include if article is 2,000+ words

If TOC is included, use simple anchor links:
```html
<ul>
  <li><a href="#section-anchor">Section title</a></li>
</ul>
```
No `!important` styles, no SVG arrows, no complex inline CSS. Elementor handles default link styling.

---

## 5. BULLET LISTS

Standard HTML — no Thrive-specific workarounds needed:

```html
<ul>
  <li><strong>Label.</strong> Explanation text.</li>
  <li><strong>Label.</strong> Explanation text.</li>
</ul>
```

No custom CSS circles, no inline `border-radius:50%`, no `list-style:none` overrides. Elementor's CSS handles list styling. Keep bullet HTML clean.

---

## 6. LINKS

- External (non-chatsku.com): `target="_blank" rel="noopener noreferrer"`
- Internal chatsku.com: no `target` attribute, same tab
- Every article: **minimum 3 internal links to pages + at least 2 internal links to existing blog posts** (interlink the blog as it grows)
- For pillar posts (2,000+ words): up to 9–10 total internal links is appropriate
- **Internal pages (link where relevant — do NOT use all, pick contextually appropriate ones):**
  - `/demo/` — book a demo
  - `/signup/` — start free trial
  - `/features/` — catalog integration / what ChatSKU connects to
  - `/pricing/` — see pricing
  - `/revenue-calculator` — model the ROI / revenue impact calculator
  - `/faq/` — FAQ page
  - `/for-b2b-manufacturers-distributors-and-wholesalers/` — solution page for distributors/manufacturers
  - `/ai-sales-assistant-b2b-ecommerce/` — B2B AI sales assistant solution page
  - `/pdf-catalog-chatbot/` — PDF catalog chatbot solution
  - `/rfq-automation-for-product-catalogs/` — RFQ automation solution page (also a blog post)
  - `/passive-catalog/` — the "passive catalog" problem (catalog shows products but can't close)
  - `/response-gap/` — the "response gap" problem (48-hour sales-rep delay)
  - `/human-bottleneck/` — human bottleneck problem
  - `/black-hole-pipeline/` — black hole pipeline problem
  - `/complex-configuration/` — complex configuration problem
  - `/headcount-ceiling/` — headcount ceiling problem
- **Internal blog posts (interlink where contextually relevant):**
  - `/pdf-catalog-sales-liability/` — Why your PDF catalog is your biggest sales liability
  - `/ai-chatbot-for-manufacturers-dallas/` — 5 questions before buying an AI chatbot
  - `/b2b-ecommerce-chatbot-dallas/` — How DFW distributors lose leads without a chatbot
  - `/rfq-automation-manufacturers/` — What is RFQ automation and why manufacturers need it
  - `/rfq-form-conversion-rate/` — Why your RFQ form has a 1.8% conversion rate (Blog #2)
  - `/convert-pdf-catalog-to-website/` — How to convert a PDF catalog to a searchable website
  - `/b2b-catalog-issues-costing-sales/` — Your B2B catalog is costing you money, here's how much
  - `/b2b-after-hours-buyer-problem/` — Your buyers don't wait until morning (after-hours lead problem)
  - `/b2b-catalog-conversion-rate/` — Why your B2B catalog conversion rate is stuck (Blog #3)
  - `/lost-b2b-revenue-calculator/` — How to calculate lost B2B revenue from after-hours buyers and slow quote response (Blog #4)
  - `/best-b2b-catalog-chatbots-2026/` — Best B2B catalog chatbots in 2026 (vendor roundup, post 294 — commercial/comparison intent)
  - `/what-is-a-b2b-catalog-chatbot/` — What is a B2B catalog chatbot? Complete 2026 guide (post 353 — definitional/top-of-funnel companion to 294)
  - `/b2b-conversational-commerce/` — B2B conversational commerce: definition, use cases, and ROI (post 380)
  - `/what-is-a-passive-catalog/` — What is a passive catalog? (post 397 — companion to the /passive-catalog/ problem page)
  - `/b2b-chatbot-for-woocommerce/` — How to add a B2B chatbot to your WooCommerce store (post 685 — first platform-specific post; WooCommerce how-to)
  - Add new posts to this list immediately after publishing
- **RULE: Before writing any new post, fetch https://chatsku.com/blog/ to check for posts published after this file was last updated. Never rely solely on this file.**
- **Maximum 2 external (non-chatsku.com) links per article** — no exceptions
- **Never link to competitor tools** (Drift, Intercom, Tidio, BigCommerce B2B, etc.)
- Anchor text varied, never "click here"

---

## 7. VOICE AND STYLE

Read `clients/chatsku/style/voice.md` in full.

Banned:
- Em dashes (— U+2014) and `&mdash;` — replace with periods, commas, hyphens
- "just a chatbot" — undermines positioning
- "AI-powered" as generic filler
- "solutions" as noun filler
- Hype: revolutionary, game-changing, cutting-edge, "transform your..."
- Filler: delve, leverage, navigate (verb), "in today's fast-paced world"

Required:
- Sentence case headings
- Second person ("you", "your")
- Word count: 1,200–2,000 (standard) or 2,000–3,000 (pillar guide)
- Open with a buyer scenario or vivid pain — not a definition
- End with a direct, specific CTA — not "learn more"

---

## 8. WORDPRESS PUBLISHING

- Status always: `draft`
- REST API endpoint: `/wp-json/wp/v2/posts` with Basic Auth
- Credentials: `$env:CHATSKU_WP_USERNAME` and `$env:CHATSKU_WP_APP_PASSWORD`
- DO NOT use Virtina's WP_USERNAME / WP_APP_PASSWORD — different site, different credentials
- **Cloudflare requirement:** Every request to chatsku.com MUST include browser User-Agent header or Cloudflare returns 403. Use: `'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'`
- `featured_media` set with a real media ID, never 0
- Yoast meta title: 60 chars max, format `{Title} | ChatSKU`
- Yoast meta description: 150–160 chars
- **Yoast meta CANNOT be set via REST API** — `_yoast_wpseo_title` and `_yoast_wpseo_metadesc` are not registered with `show_in_rest` on chatsku.com. Must be entered manually: WP Admin → Posts → Edit → Yoast SEO panel → SEO tab.

**REQUIRED: Elementor data — every post MUST include in the `meta` field:**
```json
{
  "meta": {
    "_elementor_edit_mode": "builder",
    "_elementor_template_type": "wp-post",
    "_elementor_data": "[... JSON string from build_elementor script ...]"
  }
}
```
Without this, the post renders as plain WordPress content and will not match the site design. Use `clients/chatsku/output/research/build_elementor_post186_v3.py` as the canonical template. Parse the HTML into Elementor sections (one section per H2), with heading/text-editor/image widgets per section.

**REQUIRED after every Elementor data push — clear the cache:**
```python
urllib.request.Request('https://chatsku.com/wp-json/elementor/v1/cache', headers=HEADERS, method='DELETE')
```
Without this, WordPress serves a stale rendered version (old widget IDs, old layout). The cache clear is mandatory — not optional.

**Conclusion section** requires three widgets (verified from post 96):
1. `heading` widget — `align: "center"`, `title_color: "#ffffff"`
2. `text-editor` widget — each `<p>` styled `color:#aaaacc; text-align:center; font-size:18px; max-width:720px; margin:0 auto;` — NO inline CTA links in body text
3. `button` widget — `background_color: "#e94560"`, `button_text_color: "#ffffff"`, `border_radius: 6px`, `align: center`, link to `https://chatsku.com/demo/`

**WP content field** — after building Elementor data, also strip any bare `<img>` tags from the WordPress `content` field. Even in Elementor builder mode, leftover `<img>` tags in `content` can leak into the rendered output alongside the Elementor image widgets, causing doubled images.

---

## 9. PRE-PUBLISH CHECKLIST

Run before any PUT call. Fix all failures before publishing.

**Uniqueness:**
- [ ] Topic not duplicated against `published-posts-inventory.md`
- [ ] Angle/thesis distinct from existing ChatSKU posts
- [ ] Slug doesn't match any existing slug
- [ ] No 8-word sequence appears verbatim in any existing ChatSKU post

**Structure:**
- [ ] All required sections present for chosen format
- [ ] "Executive Summary" present as H2 (not "Summary")
- [ ] Conclusion present with CTA button widget (not inline link) linking to chatsku.com/demo/
- [ ] Conclusion heading is centered and white (#ffffff)
- [ ] Conclusion body text styled: color:#aaaacc; text-align:center; font-size:18px

**Images:**
- [ ] Featured image set (real media ID, not 0)
- [ ] Featured image exactly 860×452
- [ ] Featured image alt 80–150 chars
- [ ] Body images: 1–2 images, each exactly 860×452
- [ ] All body images have unique 80–150 char alt text
- [ ] Every image `src` begins with `https://chatsku.com/wp-content/uploads/`
- [ ] Every image visually relevant (no nature/flowers on B2B article)
- [ ] No source.unsplash.com or placehold.co URLs anywhere

**Content:**
- [ ] No em dashes (— or `&mdash;`)
- [ ] No banned hype/filler words (check brand.md)
- [ ] ChatSKU never called "just a chatbot"
- [ ] "AI-powered" not used as generic filler
- [ ] Sentence case headings throughout
- [ ] CTA at end links to chatsku.com/signup/ or chatsku.com/demo/
- [ ] Word count appropriate for format

**Links:**
- [ ] All external links: `target="_blank" rel="noopener noreferrer"`
- [ ] Internal chatsku.com links: no `target` attribute
- [ ] External link count is 2 or fewer
- [ ] No links to competitors (Drift, Intercom, Tidio, BigCommerce B2B, etc.)
- [ ] 3–5 internal ChatSKU links present

**WordPress:**
- [ ] Status: `draft`
- [ ] `featured_media` is a real media ID, not 0
- [ ] Yoast meta title set (ends `| ChatSKU`, 60 chars max)
- [ ] Yoast meta description set (150–160 chars)
- [ ] Credentials used are `CHATSKU_WP_USERNAME` / `CHATSKU_WP_APP_PASSWORD`
- [ ] `_elementor_edit_mode` = `"builder"` set in meta
- [ ] `_elementor_template_type` = `"wp-post"` set in meta
- [ ] `_elementor_data` JSON set in meta (non-empty, parses as valid JSON array)
- [ ] Elementor cache cleared after push: `DELETE /wp-json/elementor/v1/cache`
- [ ] WP `content` field has no bare `<img>` tags (strip them before pushing)
- [ ] Image widgets are ordered AFTER text-editor widgets in every section
- [ ] Yoast meta title and description set manually in WP dashboard (cannot be set via REST API)

---

## 10. AGENT BEHAVIOR ENFORCEMENT

Every agent must:
1. Read this file in full at start of any ChatSKU task
2. Read all sub-files: `brand-primary.txt`, `body-font-size.txt`, `published-posts-inventory.md`, `voice.md`, `audience.md`, `brand.md`, `cms.md`
3. Use standard semantic HTML for content — no Thrive-specific markup
4. Run the pre-publish checklist (section 9) before any PUT call
5. Refuse to publish if any checklist item fails
6. Use ChatSKU's credentials, not Virtina's

---

## 11. SUPPORTED BLOG FORMATS — VARY ACROSS POSTS FOR UNIQUENESS

All 4 existing ChatSKU posts are Format A. New posts should vary. Track format usage in `published-posts-inventory.md`.

### Format A — Standard explanatory (default)
How-to guides, diagnostic articles, technical explanations. Structure: Executive Summary, Introduction, body sections, PAA, Conclusion, FAQ. Reference: post 151.

### Format B — Conversational Q&A (LLM-style)
Reader questions as H2 headings, each answered in 2–4 paragraphs. Use for: "How does X work for B2B catalog?" topics, evaluation guides, feature explainers where buyers have many follow-up questions.

### Format C — Listicle with opinions
Each H2 is a numbered, opinionated point. Use for: "X mistakes", "X signs", "X reasons" articles. Always takes a position — never neutral surveys.

### Format D — Decision-tree / playbook
Sequenced decisions or phases. Use for: "Should I use X or Y?", "How to choose between ERP integration approaches", build-vs-buy guides.

### Format E — Contrarian thesis
Challenges conventional wisdom. Use for: "Why generic chatbots fail for B2B", "Stop thinking of your catalog as a brochure" angles.

### Format F — Case study / before-and-after
Real or representative client scenarios with concrete numbers. Use for: "How a manufacturer captured 40% more after-hours leads" style posts.

### Format selection rule
1. Check existing post formats in `published-posts-inventory.md` — all 4 are Format A
2. Do not use Format A for more than 1 of the next 3 posts — rotate
3. Pick format that best fits the topic
4. Brief must state chosen format and reason

---

## 12. WHEN A NEW ISSUE APPEARS

If any issue is reported not covered by this file:
1. Add the rule to the appropriate section above
2. Add the verification step to the pre-publish checklist (section 9)
3. Update `brand-primary.txt` or `body-font-size.txt` if a color/size value changes
4. Commit and push immediately
5. The fix becomes permanent — never re-fixed manually
