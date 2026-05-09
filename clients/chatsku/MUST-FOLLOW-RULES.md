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
ChatSKU uses WordPress + **Elementor 4.0.3**, NOT Thrive Architect. This means:
- Standard Gutenberg block HTML renders correctly — no `!important` CSS wars
- No SVG arrow TOC required — simple `<a href="#anchor">` links work
- No complex inline style overrides needed
- Post content is clean semantic HTML — `<h2>`, `<p>`, `<ul>`, `<li>` tags
- Bullet styling through standard CSS classes, not inline `border-radius:50%` circles
- The Virtina Thrive-specific HTML patterns DO NOT apply here

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
- Every article: 3–5 internal ChatSKU links (fewer pages than Virtina — don't force more than exist)
- Internal pages available: `/`, `/demo/`, `/signup/`, `/features/`, `/pricing/`, `/blog/`
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
- `featured_media` set with a real media ID, never 0
- Yoast meta title: 60 chars max, format `{Title} | ChatSKU`
- Yoast meta description: 150–160 chars
- Categories and tags from ChatSKU's existing WordPress taxonomy

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
- [ ] Conclusion present with CTA linking to chatsku.com/signup/ or chatsku.com/demo/

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
