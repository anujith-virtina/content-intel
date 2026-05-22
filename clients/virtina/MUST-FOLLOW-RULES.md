# Virtina Blog — Mandatory Rules (Locked Memory)

This file is the source of truth. Every agent (researcher, analyzer, creator, publisher) MUST read this file in full at the start of every Virtina task. These rules were established through extensive QA in May 2026. Do not deviate.

## Reference posts (gold standards)

- Post 42074: https://virtina.com/launching-fast-without-strategy-ecommerce-costs/ — fix-it diagnostic article
- Post 42108: https://virtina.com/?p=42108 — pre-integration playbook

Local cached copies in `clients/virtina/reference/`. Refresh every 30 days or after manual updates.

## Authoritative sub-files

- `clients/virtina/brand-teal.txt` — verified brand hex values (slate #43627f, link blue #00a0e2, etc.)
- `clients/virtina/body-font-size.txt` — verified body font-size (16px)
- `clients/virtina/reference/visual-specs.md` — colors, typography, spacing (full table)
- `clients/virtina/reference/html-templates.md` — exact HTML patterns A–M
- `clients/virtina/reference/published-posts-inventory.md` — every existing virtina.com post for uniqueness checks
- `clients/virtina/style/voice.md`, `audience.md`, `brand.md` — content voice and style rules

---

## 1. UNIQUENESS — EVERY VIRTINA BLOG MUST BE UNIQUE

Before writing any new Virtina blog, the researcher must run all 5 checks below and save a uniqueness audit file to `clients/virtina/output/research/uniqueness-audit-{YYYY-MM-DD}.md`. A topic is REJECTED if it fails ANY single check. This is non-negotiable.

### Pre-check: Refresh the inventory if stale
- Check `last_updated` field in `published-posts-inventory.md`
- If older than 7 days, refresh via WP REST API: `GET https://virtina.com/wp-json/wp/v2/posts?per_page=100&page=N&status=publish&orderby=date&order=desc`
- Paginate until you have all posts published since `last_updated`
- Add new posts to inventory and update `total_posts` and `last_updated`

### CHECK 1 — Title word overlap
- No existing post title shares 3 or more consecutive meaningful words with the proposed title
- Ignore stop words (the, a, an, is, to, for, in, of, and, or, with)
- REJECT if 3+ consecutive content words match

### CHECK 2 — Slug overlap
- The proposed slug must not be a substring of any existing slug
- The proposed slug must not contain 2 or more words from any existing slug
- REJECT if substring match OR 2+ word overlap found

### CHECK 3 — Primary keyword uniqueness
- The primary keyword must not be the focus keyword of any existing post
- Cross-check against slug fields (slugs encode the focus keyword)
- REJECT if primary keyword is already claimed by an existing post

### CHECK 4 — Angle/thesis uniqueness
- The thesis (point of view) must be different from any existing Virtina post on a related topic
- Even if the title is different, reject if the argument or coverage is substantially the same
- Cross-check angle against the inventory's excerpt fields
- REJECT if angle overlap exists even with a different title

### CHECK 5 — Topic cluster saturation
- Count existing posts in the same topic cluster (e.g., WooCommerce, migration, SEO, B2B)
- REJECT if 5 or more posts already exist on the same general subject within the cluster
- "Same general subject" means posts a reader seeking info on topic X would already find

### Audit file requirement
Save results to `clients/virtina/output/research/uniqueness-audit-{YYYY-MM-DD}.md` with:
- All candidate topics evaluated (even rejected ones)
- Which checks each candidate passed or failed
- Final selected topic with explicit PASS notation for all 5 checks

### Additional uniqueness rules (post-draft)

**Phrasing uniqueness:**
- After draft is written, no sentence longer than 8 words may appear verbatim in any existing Virtina post
- The publisher runs this check before any PUT call
- If duplicate phrasing detected, the creator rewrites those passages

**Structural uniqueness via different blog formats:**
- The standard format (used in post 42074) is one option, not the only option
- Section 11 defines additional supported formats — pick the format that best fits the topic and that hasn't been overused recently

Duplicate content damages SEO for both posts. Originality is non-negotiable.

---

## 2. STRUCTURE (DEFAULT EXPLANATORY FORMAT)

For standard explanatory articles (most "how to / why / what" topics), use this order:

1. H1 title (sentence case)
2. Author byline + category + updated date
3. Featured image at 1309×500 px
4. Summary block (Template A)
5. Introduction block (Template B)
6. Table of Contents (Template C with H3 heading) — use `clients/virtina/reference/toc-working-template.html` as the exact source. **NEVER use Thrive Architect `thrv-styled_list` class-based markup** — it depends on Thrive CSS that is not always loaded and breaks arrow rendering. The inline SVG approach in toc-working-template.html is the only approved pattern.
7. Body sections — H2 with id (Template D), paragraphs (Template E), bullet lists (Template F), section images at 670×352 (Template G)
8. People Also Ask block (Template H)
9. Conclusion block (Template I)
10. FAQ accordion (Template J)
11. Author bio block (Template K)

---

## 3. IMAGES

### Sourcing
API priority: Pexels API > Openverse (source=stocksnap filter) > Wikimedia Commons.

Never:
- `source.unsplash.com` (deprecated 2024, returns random unrelated images)
- `placehold.co` or any external placeholder in saved content
- Branded text-on-color cards (Pillow-generated)
- Random stock with no topical relevance (flowers, landscapes, nature on a B2B article)

Openverse usage: use `source=stocksnap` filter and short 3-4 word queries matching stock photo naming conventions (e.g. "office team meeting", "laptop desk business"). Long academic descriptions return old Wikimedia/Flickr junk.

### Topic keyword library
- Featured: `laptop office business`, `ecommerce dashboard laptop`, `business professional desk`
- Item master / SKU / data: `macbook desk business work`, `working typing computer desk`
- Integration / pricing / dev: `office team meeting computers`, `coworkers office computer work`
- Warehouse / fulfillment / inventory: `warehouse worker inventory`, `shipping fulfillment workers`
- Strategy / planning: `business meeting whiteboard`, `team strategy planning office`

### Required count and dimensions
- 1 featured image at exactly 1309×500 px
- 2–3 body images at exactly 670×352 px each (up to 5 for pillar guides over 2500 words)
- File size under 200 KB per image (JPEG quality 82)
- All body images same dimensions

### Required attributes
- `featured_media` on post object set to a real uploaded media ID, never 0
- Each image `alt_text` 80–150 chars, descriptive, includes 1–2 article keywords naturally
- Every image `src` must begin with `https://virtina.com/wp-content/uploads/`

### Subject relevance
For B2B ecommerce / WooCommerce / ERP / integration topics, images must show business / office / warehouse / data / ecommerce scenes. Never acceptable: nature, flowers, landscapes, mountains, water, forests, animals, building exteriors, FEMA scenes, old historical computers.

---

## 4. TABLE OF CONTENTS

Use **Template C** from `html-templates.md` exactly. The canonical live example is in `clients/virtina/reference/toc-working-template.html` (verified 2026-05-22, post 42202).

**CRITICAL — Do NOT use Thrive Architect class-based markup:**
- NEVER: `<ul class="tcb-styled-list">` / `<li class="thrv-styled-list-item">` / `<div class="tcb-styled-list-icon">`
- These Thrive CSS classes render arrows only when Thrive's frontend CSS is loaded — they silently break otherwise
- Post 42202 was repaired 2026-05-22 by replacing this markup with inline Template C

Specs:
- H3 'Table of Contents' heading (never H2)
- `<ul>` with `list-style:none!important` — NO SPACE before `!important`
- Items as real `<a href="#anchor">` links
- TOC link text color: `#00a0e2` with `!important`
- Arrow: inline `<svg>` inside `<span aria-hidden="true">` with `position:absolute!important;left:0!important;top:8px!important;` — `fill:#43627f`
- NEVER Unicode `→`, NEVER Font Awesome, NEVER Thrive icon wrappers
- Every body H2 must have `id` attribute matching anchor href
- Place TOC after Introduction div, before first body H2 section div

---

## 5. BULLET LISTS

Use **Template F** from `html-templates.md` exactly. Specs:

- `<ul>` with `list-style:none;padding-left:4px;margin:8px 0 16px 0`
- `<li>` with `display:flex;align-items:flex-start;gap:10px;padding:6px 0`
- Circle `<span>`: `flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block`
- Text `<span>`: `font-size:16px;line-height:1.75;color:#2d3e50`
- `<li>` font-size must equal `body-font-size.txt` value (16px)
- Circle background-color must equal the slate value from `brand-teal.txt` (#43627f)
- No Font Awesome, no HTML entities, no default browser bullets

Safe body-only regex (excludes TOC `<ul>` which has `!important`):
```python
body_ul_re = re.compile(r'<ul\s+style="(?![^"]*!important)[^"]*"[^>]*>.*?</ul>', re.DOTALL)
```

---

## 6. LINKS

- External (non-virtina.com): `target="_blank" rel="noopener noreferrer"` — Template M
- Internal virtina.com: no `target` attribute, `style="outline: none;"` — Template L
- Every article: 5–10 internal Virtina links woven naturally in body prose
- **Maximum 2 external (non-virtina.com) links per article** — no exceptions
- **Never link to competitor domains** (shopify.com, bigcommerce.com, etc.)
- Anchor text varied, never repeat the same anchor twice, never "click here"
- Internal links in body sections only — not in intro, not in conclusion

Pre-publish: count external hrefs. If more than 2, convert excess to plain text. Strip all competitor-domain links entirely.

---

## 7. VOICE AND STYLE

Banned characters:
- Em dashes (— U+2014), `&mdash;`, `&#8212;`, `&#x2014;` — banned everywhere: titles, headings, body, bullets, conclusions. Replace with commas, colons, periods, or hyphens. The publisher script must grep for all four forms before any PUT call.

H3 heading pattern for Thrive Architect posts (verified from post 42177, May 2026):
- Correct: `<h3 style="color:#43627f;font-size:22px;">TEXT</h3>`
- Wrong: `<h3><span style="font-weight: normal;"><span>TEXT</span></span></h3>` — this is the Elementor pattern, does NOT work in Thrive posts

Banned words:
- Hype: revolutionary, game-changing, best-in-class, cutting-edge, transform your, unlock value, synergize
- Filler: delve, leverage, navigate (verb), realm, landscape, ecosystem, "in today's fast-paced world", "it's important to note", "in conclusion"

Required:
- Sentence case headings (never Title Case)
- Active voice, second person ("you")
- Quotes from sources under 15 words; paraphrase otherwise
- Word count: 1500–2500 (standard) or 2500–3500 (pillar guide)

---

## 8. WORDPRESS PUBLISHING

- Status always: `draft` (never auto-publish)
- Endpoint: `/wp-json/wp/v2/posts` with Basic Auth (`$env:WP_USERNAME` + `$env:WP_APP_PASSWORD`)
- `featured_media` set with a real uploaded media ID, never 0
- Yoast `meta_description`: 150–160 chars
- Yoast SEO title: 60 chars max, format `{Title} | Virtina`
- Categories and tags from existing Virtina taxonomy

---

## 9. PRE-PUBLISH CHECKLIST

The publisher runs every item before any PUT call. If any item fails, fix and re-verify. Never publish a broken post.

**Uniqueness:**
- [ ] All 5 uniqueness checks passed (audit file exists at `output/research/uniqueness-audit-{date}.md`)
- [ ] CHECK 1 PASS: No existing post title shares 3+ consecutive meaningful words
- [ ] CHECK 2 PASS: No existing slug is substring match or 2+ word overlap
- [ ] CHECK 3 PASS: Primary keyword not focus of any existing post
- [ ] CHECK 4 PASS: No angle/thesis overlap even with different title
- [ ] CHECK 5 PASS: Topic cluster not saturated (fewer than 5 existing posts on same general subject)
- [ ] No 8+ word verbatim sequence with any existing post (phrasing uniqueness guard)

**Structure (for chosen format from section 11):**
- [ ] All required sections present in correct order for chosen format
- [ ] H1, H2, H3 hierarchy correct
- [ ] Every H2 has `id` attribute matching TOC anchor href

**Images:**
- [ ] Featured image set (real media ID, not 0)
- [ ] Featured image exactly 1309×500
- [ ] Featured image alt 80–150 chars
- [ ] Body image count: 2–3 (up to 5 for pillar guides)
- [ ] All body images exactly 670×352
- [ ] All body images have unique 80–150 char alt text
- [ ] Every image `src` begins with `https://virtina.com/wp-content/uploads/`
- [ ] Every image visually relevant to article topic (no nature on B2B articles)
- [ ] No `source.unsplash.com` URLs anywhere in content
- [ ] No `placehold.co` URLs anywhere in content

**TOC:**
- [ ] Heading is H3
- [ ] Items are `<a href="#anchor">` real links
- [ ] TOC link color is `#00a0e2` with `!important`
- [ ] Arrow is SVG icon with `fill:#43627f` — not Unicode text, not Font Awesome
- [ ] `!important` has NO SPACE before it (correct: `list-style:none!important`)
- [ ] Every body H2 has matching `id` attribute

**Bullets:**
- [ ] All body bullet lists use Template F (CSS circle pattern)
- [ ] Circle `background-color` is `#43627f` (read from `brand-teal.txt`)
- [ ] `<li>` font-size is `16px` (read from `body-font-size.txt`)
- [ ] Text `<span>` has `font-size:16px;line-height:1.75;color:#2d3e50`
- [ ] No default browser bullets anywhere
- [ ] No orphan `<<` or `>>` text fragments (Thrive serializer corruption)

**Links:**
- [ ] All external links: `target="_blank" rel="noopener noreferrer"`
- [ ] All internal virtina.com links: no `target` attribute
- [ ] 5–10 internal Virtina links present
- [ ] External link count is 2 or fewer
- [ ] No links to competitor domains (shopify.com, bigcommerce.com, etc.)

**Voice:**
- [ ] No em dashes — grep for `—`, `&mdash;`, `&#8212;`, `&#x2014;` — all four forms must be zero
- [ ] No banned hype/filler words
- [ ] Sentence case headings throughout
- [ ] Word count appropriate for format
- [ ] All H3 tags use `<h3 style="color:#43627f;font-size:22px;">TEXT</h3>` — never the Elementor `<span style="font-weight: normal;">` pattern

**WordPress:**
- [ ] Status: `draft`
- [ ] `featured_media` is a real media ID, not 0
- [ ] Yoast meta title (60 chars max, ends `| Virtina`) set
- [ ] Yoast meta description (150–160 chars) set
- [ ] Category and tags set

---

## 10. AGENT BEHAVIOR ENFORCEMENT

Every agent must:
1. Read this file in full at start of any Virtina task
2. Read all sub-files referenced: `brand-teal.txt`, `body-font-size.txt`, `visual-specs.md`, `html-templates.md`, `published-posts-inventory.md`, `voice.md`, `audience.md`, `brand.md`
3. Use templates from `html-templates.md` — never improvise HTML structure
4. Run the pre-publish checklist (section 9) before any PUT call
5. Refuse to publish if any checklist item fails
6. Never claim success without confirming saved content matches expectations

---

## 11. SUPPORTED BLOG FORMATS — VARY ACROSS POSTS FOR UNIQUENESS

The standard explanatory format (section 2) is the default but not the only option. Pick the format that fits the topic AND that hasn't been overused in recent virtina.com posts. Review the last 10 posts in `published-posts-inventory.md` and rotate formats.

### Format A — Standard explanatory (default)
Structure as defined in section 2. Use for: how-to guides, diagnostic articles, technical explanations, framework breakdowns. Reference: post 42074, post 42108.

### Format B — Conversational Q&A (LLM-style)
A whole article structured as a conversation between an inquisitive reader and a Virtina expert. Use for: topics where readers have many specific sub-questions, AI/chatbot topics, decision-making guides where each answer raises a follow-up question.

Structure: H1 often phrased as a question. Each body H2 is a verbatim reader question, followed by a clear 2–4 paragraph answer. One body image every 2–3 questions. The H2 questions become the TOC — no separate question list needed.

### Format C — Listicle with opinions
Use for: comparison topics, "X mistakes" articles, "X tools/strategies" pieces — only when each list item has a defensible opinion, never neutral surveys. Each H2 is one list item with an opinionated heading.

Structure: H1 often "X [number] [things]". Each H2 item defended with 2–3 paragraphs. Never publish a listicle without picking sides — Virtina voice is opinionated.

### Format D — Decision-tree / playbook
Use for: "Should I X or Y?" topics, migration decisions, build-vs-buy, platform selection. Reader walks through a sequence of decisions or phases.

Structure: H1 often "Should you X" or "How to decide between X and Y". Body sections are sequenced phases or decisions. Bullet lists for criteria/checklists at each step.

### Format E — Contrarian thesis
Use for: opinion pieces challenging conventional wisdom, "Don't blame X" style articles.

Structure: H1 with vivid contrarian phrasing, often using analogy. First 1–2 body sections set up the conventional wisdom and why it falls short. Remaining sections build the contrarian case with evidence and examples. PAA covers pushback questions.

### Format F — Case study / before-and-after
Use for: real client wins, specific platform/integration projects, measurable outcome stories.

Structure: H1 "How [client/segment] [achieved outcome]". Summary states headline result with concrete numbers. Body sections: "The challenge", "What we tried first", "What actually worked", "Results", "What other teams can learn". Body images show dashboards/workflows.

### Format selection rule
The analyzer picks the format during the brief stage based on:
1. Topic fit — which format suits the subject best
2. Recency check — do not reuse any format used in 3+ of the last 10 published posts
3. User's explicit format request
4. Default to Format A if no clear winner

The brief must state explicitly which format is chosen and why.

---

## 12. WHEN A NEW ISSUE APPEARS

If any issue is reported that is not covered by this file:
1. Add the rule to the appropriate section above
2. Add the verification step to the pre-publish checklist (section 9)
3. Update reference templates in `html-templates.md` if structural change needed
4. Update `brand-teal.txt` or `body-font-size.txt` if a color/size value changes
5. Commit and push immediately
6. The fix becomes permanent — never re-fixed manually
