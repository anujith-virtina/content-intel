# ImpelHub Blog — Mandatory Rules (Locked Memory)

This file is the source of truth for ImpelHub content. Every agent (researcher, analyzer, creator, publisher) MUST read this file in full at the start of every ImpelHub task. These rules were established during initial onboarding on 2026-06-10. Do not deviate.

## Reference posts (gold standards)

- Post 12356: https://impelhub.com/blog/fractional-leadership-b2b-startups-cto-cmo-cfo/ — best-structured post (TL;DR, TOC, H2/H3 hierarchy, images, Related Reading, Conclusion). NOTE: 12356 uses old `elementor-widget-accordion` — use post 12433 as the FAQ accordion reference instead.
- Post 12433: https://impelhub.com/blog/product-market-fit-signals-b2b-saas/ — use for FAQ accordion reference (`elementor-widget-n-accordion`, `nested-accordion.default`)

Local cached copy: `clients/impelhub/reference/post-12356-working.html`

Refresh every 30 days or after manual updates.

## Authoritative sub-files

- `clients/impelhub/brand-primary.txt` — confirmed brand color (#5736fd, ImpelHub purple)
- `clients/impelhub/body-font-size.txt` — body font-size (16px estimated; verify via dev tools)
- `clients/impelhub/reference/published-posts-inventory.md` — all 50 existing posts for uniqueness checks
- `clients/impelhub/style/voice.md`, `audience.md`, `brand.md` — content voice and style rules
- `clients/impelhub/style/cms.md` — Elementor HTML patterns, CTA conventions, image keywords
- `clients/impelhub/style/examples.md` — structural templates and opening/closing hook patterns

---

## 1. UNIQUENESS — EVERY IMPELHUB BLOG MUST BE UNIQUE

Before writing any new ImpelHub blog, the researcher must run all 5 checks below and save a uniqueness audit file to `clients/impelhub/output/research/uniqueness-audit-{YYYY-MM-DD}.md`. A topic is REJECTED if it fails ANY single check. This is non-negotiable.

### Pre-check: Refresh the inventory if stale
- Check `last_updated` field in `published-posts-inventory.md`
- If older than 7 days, refresh via WP REST API: `GET https://impelhub.com/wp-json/wp/v2/posts?per_page=100&_fields=id,slug,title,date,excerpt,link`
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
- The thesis (point of view) must be different from any existing ImpelHub post on a related topic
- Even if the title is different, reject if the argument or coverage is substantially the same
- Cross-check angle against the inventory's excerpt fields
- REJECT if angle overlap exists even with a different title

### CHECK 5 — Topic cluster saturation
- Count existing posts in the same topic cluster
- REJECT if 5 or more posts already exist on the same general subject within the cluster
- Exception: if the sub-niche angle is clearly unique and documented, saturation does not block

### Cluster saturation current status (as of 2026-06-10)
- GTM / Growth Strategy: 11 posts — SATURATED. New entries require very specific sub-niche angle.
- AI & Business Intelligence: 13 posts — SATURATED. Founder-decision angle required to justify new post.
- ICP / Customer / Market Analysis: 8 posts — borderline saturated; strong unique angle required.
- Fractional Leadership: 2 posts — open.
- B2B SaaS Founder Decisions: 2 posts — open.
- Positioning / Messaging: 6 posts — borderline; angle must be distinctly new.
- SMB / Manufacturing: 4 posts — open.
- BattleBoard / Competitive: 1 post — open.
- ImpelHub Platform: 3 posts — open.

### Audit file requirement
Save results to `clients/impelhub/output/research/uniqueness-audit-{YYYY-MM-DD}.md` with:
- All candidate topics evaluated (even rejected ones)
- Which checks each candidate passed or failed
- Final selected topic with explicit PASS notation for all 5 checks

### Additional uniqueness rules (post-draft)

**Phrasing uniqueness:**
- After draft is written, no sentence longer than 8 words may appear verbatim in any existing ImpelHub post
- The publisher runs this check before any PUT call
- If duplicate phrasing detected, the creator rewrites those passages

**Structural uniqueness via different blog formats:**
- Section 11 defines supported formats — pick the format that best fits the topic and hasn't been overused recently

Duplicate content damages SEO for both posts. Originality is non-negotiable.

---

## 2. STRUCTURE (DEFAULT FORMAT)

ImpelHub's default article structure (from reference post 12356):

1. H2 "TL;DR: Key Takeaways" — 4–7 bullet points using colored arrow pattern (→ in #5736fd)
2. Table of Contents block (H3 heading, anchor links with same arrow pattern)
3. Body sections — H2 with id attribute (for TOC anchor), H3 subheadings inside long H2 sections
4. Section images — Elementor image widget, placed after content-heavy sections
5. "Related Reading" callout box (dark background container with 2–4 arrow links)
6. Conclusion (H2 id="conclusion")
7. FAQ accordion — MUST use `elementor-widget-n-accordion` (`data-widget_type="nested-accordion.default"`) with `<details>/<summary>` structure. Do NOT use the old `elementor-widget-accordion` (`accordion.default`). Confirmed from live posts 12433 and newer. 5–7 Q&As.

---

## 3. IMAGES

### Sourcing
Pexels API primary (PEXELS_API_KEY env var). All images must be visually previewed before selection — keyword searches alone produce generic mismatches.

Never:
- `source.unsplash.com` (deprecated 2024)
- `placehold.co` or any external placeholder in saved content
- Images with text overlaid (promotional cards, slides)
- Generic nature/landscape on a founder/B2B strategy article

### Topic keyword library for ImpelHub
- Founder/CEO scenes: 'founder laptop strategy', 'CEO desk decision', 'startup founder office'
- Growth/strategy: 'business strategy whiteboard', 'growth dashboard analytics', 'business meeting decision'
- Data/AI: 'AI business intelligence', 'business analytics dashboard', 'data driven business'
- Team/execution: 'startup team execution', 'business team planning', 'growth team meeting'
- Competition: 'competitive analysis business', 'market research desk', 'business intelligence screens'

### Required count and dimensions
- 1 featured image — standard WordPress featured image (dimensions: verify from reference post; 1200×628 is common for ImpelHub)
- 2–3 body images placed after heavy content sections (Elementor image widget)
- All body images same aspect ratio (horizontal/landscape orientation)
- File size: under 300 KB per image preferred

### Required attributes
- `featured_media` on post object: real uploaded media ID, never 0
- Each image `alt` text: 60–150 chars, descriptive, includes 1–2 article keywords naturally
- Every image `src` must begin with `https://impelhub.com/wp-content/uploads/`

### Subject relevance
For founder/B2B strategy topics: images must show office, strategy, data, team, or decision-making scenes. No nature, landscapes, animals, or generic illustrations unless directly topic-relevant.

---

## 4. TABLE OF CONTENTS

ImpelHub TOC pattern confirmed from reference post 12356:

- H3 "Table of Contents" heading (not H2)
- Container uses `data-settings="{&quot;background_background&quot;:&quot;classic&quot;}"` (styled background box)
- Each TOC item: `<p><span style="color:#5736fd;">→</span> <a href="#anchor" style="color:#5736fd;text-decoration:none;">Section Title</a></p>`
- Unicode → arrow (NOT SVG, NOT Font Awesome — ImpelHub uses Unicode, unlike Virtina)
- Every body H2 must have `id` attribute matching the TOC anchor href
- Place TOC after TL;DR block, before first body H2 section

CRITICAL — ImpelHub uses Unicode → arrows colored in #5736fd. Virtina uses SVG arrows. Never mix these patterns across clients.

---

## 4b. MODERN CONTENT STANDARDS (LLM + SEO)

Applied to every ImpelHub blog post.

### Paragraph length
- **Max 3 sentences per paragraph.** No exceptions.
- This applies to every paragraph: TL;DR body, introduction, body sections, FAQ answers, conclusion.
- Before any PUT call, the publisher scans for paragraphs with 4+ sentences and splits them.

### Sentence length
- **Max 20 words per sentence.** Average sentence length should stay ≤18 words.
- ImpelHub voice naturally uses shorter sentences — 3-word punches followed by 12-15 word explanations.

### Header density
- **One heading (H2 or H3) every 150-300 words.** If a section exceeds 300 words without a sub-heading, add an H3.

### H3 subheading requirements
- **Every H2 section that exceeds 200 words must contain at least one H3 subheading.**
- Use H3 inside H2 sections whenever the H2 covers multiple sub-points, stages, or decision branches.
- H3 text must be natural-language questions or descriptive phrases. Generic labels are banned: "Overview", "Background", "Introduction", "Summary" are never acceptable H3 text.
- At the article level: minimum 6 H3 subheadings across all H2 sections.

### Direct-answer discipline (critical for LLM citation)
- **The first sentence of every H2 section must directly answer the question posed by that H2 heading.**
- Do not open a section with context-setting, background, or caveats. Answer first.
- This is the single most important rule for LLM citation.

### Semantic keyword coverage
- Each post must include 10-15 semantically related terms naturally in body prose (not stuffed).
- The researcher includes a semantic term list in the research file. The creator confirms coverage in the draft.

### ImpelHub-specific content requirements

**Every ImpelHub blog must:**
- Open with a TL;DR section (H2, 4-7 arrow bullets)
- Include a Table of Contents
- End with a Conclusion section and FAQ (n-accordion, 5-7 Q&As)
- Close with one ImpelHub CTA (from cms.md CTA list)
- Use at least 2 internal ImpelHub links in body prose, colored #5736fd

**ImpelHub voice must not:**
- Describe ImpelHub as "consulting" or "just AI"
- Use "synergize", "transformative", "innovative solutions", "best-in-class"
- Use "in conclusion" as an opener (even in the Conclusion section)
- Use em dashes (—) — replace with comma, period, or colon

---

## 4c. REAL COMPETITOR RESEARCH REQUIRED

Every new ImpelHub post must be preceded by actual competitor research.

### What real research means
- Run at least 2 web_search queries targeting the primary keyword and close variants before writing
- Fetch the top 3-5 ranking pages to assess their actual content depth, structure, and weaknesses
- Save evidence to `clients/impelhub/output/research/competitor-analysis-{YYYY-MM-DD}.md`

### Required competitor analysis file structure
For each top 5 ranking page:
1. Position in SERP
2. URL
3. Title
4. Domain (who runs it)
5. Estimated word count
6. Three specific weaknesses in the competing content
7. How the ImpelHub post outperforms on each weakness

### Saturation flag
- Count how many posts in the same cluster already exist in `published-posts-inventory.md`
- If saturated (see Section 1 cluster status), document the unique sub-niche angle that justifies a new post

### Honesty rule
- If web_search returned no useful results or competitors are stronger than expected, report that honestly
- Never claim competitor research was done unless a real competitor-analysis file exists with actual URLs

---

## 5. BULLET LISTS

ImpelHub does not use custom CSS bullet patterns. Standard Elementor text-editor bullets are acceptable. Prefer prose over bullets unless content is genuinely list-shaped.

When bullets are needed:
- Use standard `<ul>/<li>` inside Elementor text-editor widget
- Or use the ImpelHub arrow pattern: `<p><span style="color:#5736fd;">→</span> [item text]</p>`
- Never use em dashes as list markers
- Bullets ONLY for genuinely list-shaped content — not for flowing arguments

---

## 6. LINKS

### Internal ImpelHub links
- Minimum 2, maximum 8 internal impelhub.com links per article
- Link style: `style="color:#5736fd;"` or `style="color:#5736fd;font-weight:500;"`
- Placed in body sections only — not in TL;DR, not in Conclusion
- Anchor text: descriptive noun phrase, naturally varied

### External links
- Maximum 2 external (non-impelhub.com) links per article
- External links: `target="_blank" rel="noopener noreferrer"`
- Never link to competitor domains (McKinsey, BCG, Aha!, etc.)

### Anchor text rules
- Clean noun phrase or descriptive question fragment
- No leading articles ("a", "an", "the") in isolation
- No "click here", "read more", or generic anchors
- Vary anchor text across the article — never repeat the same anchor

### ImpelHub internal links to use (from cms.md CTA conventions)
- Growth lever quiz: https://impelhub.com/find-out-where-your-business-should-focus-next-for-growth-in-just-3-minutes/
- Contact / playbook: https://impelhub.com/contact/
- How it works: https://impelhub.com/how-impelhub-works/
- Startup playbook PDF: https://impelhub.com/wp-content/uploads/2025/05/impelhub-startup-growth-strategies-playbook.pdf

---

## 7. VOICE AND STYLE

### Banned characters
- Em dashes (— U+2014), `&mdash;`, `&#8212;`, `&#x2014;` — banned everywhere. Replace with comma, colon, period, or hyphen.
- Semicolons — avoid; prefer shorter sentences

### Heading style
- Sentence case always (never Title Case)
- ImpelHub headings are punchy and specific — not "Introduction" or "Overview"
- H2 headings often phrased as direct questions the reader has
- H3 headings often name the sub-topic or signal a decision branch

### Elementor heading widget pattern (ImpelHub)
- Correct: `<h2 class="elementor-heading-title elementor-size-default">Heading text</h2>` inside Elementor heading widget
- Correct: `<h3 class="elementor-heading-title elementor-size-default">Subheading</h3>` inside Elementor heading widget
- NEVER use Thrive Architect H3 pattern: `<h3 style="color:#43627f;font-size:22px;">` — that is Virtina only
- NEVER use `<p><b>` as a heading substitute

### Banned words
AI tells (never use): delve, leverage, navigate (verb), realm, landscape, ecosystem, "in today's fast-paced world", "it's important to note", "in conclusion" (as opener), "innovative solutions"

Consultant-speak banned: "synergize", "transformative journey", "thought partnership", "best-in-class", "world-class", "industry-leading", "strategic enablement", "alignment workshop"

Hype banned: revolutionary, game-changing, cutting-edge, "transform your..."

### Required voice elements
- Second person ("you", "your") dominant
- Short declarative sentences — 3-word punches welcome
- ImpelHub phrases: "Guardians of Growth", "Speed to ROI", "decision filter", "Big League Strategy. SMB Velocity."
- Trademark symbols where applicable: Impeleration™, BattleBoard™
- Word count: 1500–2500 (standard), 2500–3500 (pillar/decision guide)

---

## 8. WORDPRESS PUBLISHING

- Platform: WordPress + Elementor
- Status always: `draft` (never auto-publish)
- Endpoint: `https://impelhub.com/wp-json/wp/v2/posts` with Basic Auth (`$env:IMPELHUB_WP_USERNAME` + `$env:IMPELHUB_WP_APP_PASSWORD`)
- `featured_media` set with a real uploaded media ID, never 0
- Yoast meta_title: 60 chars max, format `{Title} | ImpelHub`
- Yoast meta_description: 150–160 chars, conversational and decision-filter framed
- DO NOT use Virtina credentials (`WP_USERNAME`/`WP_APP_PASSWORD`) — separate installation
- DO NOT use ChatSKU credentials — separate installation

---

## 9. PRE-PUBLISH CHECKLIST

The publisher runs every item before any PUT call. If any item fails, fix and re-verify.

**Uniqueness:**
- [ ] All 5 uniqueness checks passed (audit file exists at `output/research/uniqueness-audit-{date}.md`)
- [ ] CHECK 1 PASS: No existing title shares 3+ consecutive meaningful words
- [ ] CHECK 2 PASS: No existing slug is substring match or 2+ word overlap
- [ ] CHECK 3 PASS: Primary keyword not focus of any existing post
- [ ] CHECK 4 PASS: No angle/thesis overlap even with different title
- [ ] CHECK 5 PASS: Topic cluster not saturated (or sub-niche angle documented)
- [ ] No 8+ word verbatim sequence with any existing post

**Modern content standards (section 4b):**
- [ ] Paragraphs: no paragraph has 4 or more sentences — scan entire content before PUT
- [ ] Sentences: no sentence exceeds 20 words — spot check 5 random sentences per section
- [ ] Direct answers: first sentence of every H2 body section directly answers the H2 question
- [ ] Semantic coverage: 10-15 related terms present naturally (researcher confirms in research file)
- [ ] ImpelHub required elements: TL;DR, TOC, Conclusion, FAQ n-accordion (`nested-accordion.default`), CTA, 2+ internal links

**Competitor research (section 4c):**
- [ ] web_search run for primary keyword (and at least 1 variant) before writing
- [ ] Competitor analysis file saved: `output/research/competitor-analysis-{date}.md`
- [ ] At least 3 top-ranking pages fetched and documented

**Structure:**
- [ ] All required sections present: TL;DR, TOC, body H2s, Related Reading (optional), Conclusion, FAQ
- [ ] H1, H2, H3 hierarchy correct
- [ ] Every body H2 has `id` attribute matching TOC anchor href
- [ ] H3 subheadings present inside every H2 section that exceeds 200 words
- [ ] Minimum 6 H3 subheadings across the full article
- [ ] TOC uses Unicode → arrows in #5736fd, NOT SVG (ImpelHub pattern, not Virtina)

**Images:**
- [ ] Featured image set (real media ID, not 0)
- [ ] Body image count: 2–3
- [ ] All body images horizontally oriented, visually relevant to topic
- [ ] All images visually previewed before selection
- [ ] Every image `src` begins with `https://impelhub.com/wp-content/uploads/`
- [ ] No `source.unsplash.com` URLs anywhere
- [ ] No `placehold.co` URLs anywhere

**Voice:**
- [ ] No em dashes — grep for `—`, `&mdash;`, `&#8212;`, `&#x2014;`
- [ ] No banned hype/consultant-speak words
- [ ] Sentence case headings throughout
- [ ] ImpelHub not described as "consulting" or "just AI"
- [ ] Elementor heading widget pattern used (not Thrive H3 pattern)
- [ ] Word count appropriate for format

**Links:**
- [ ] Internal link count: 2–8 impelhub.com links, colored #5736fd
- [ ] External link count: 2 or fewer
- [ ] No links to competitor domains
- [ ] External links have `target="_blank" rel="noopener noreferrer"`
- [ ] Article ends with one of the 4 ImpelHub CTAs from cms.md

**WordPress:**
- [ ] Status: `draft`
- [ ] `featured_media` is a real media ID, not 0
- [ ] Credentials: IMPELHUB_WP_USERNAME + IMPELHUB_WP_APP_PASSWORD (not Virtina or ChatSKU)
- [ ] Yoast meta title (60 chars max, ends `| ImpelHub`) set
- [ ] Yoast meta description (150–160 chars) set

---

## 10. AGENT BEHAVIOR ENFORCEMENT

Every agent must:
1. Read this file in full at start of any ImpelHub task
2. Read all sub-files referenced: `brand-primary.txt`, `body-font-size.txt`, `published-posts-inventory.md`, `voice.md`, `audience.md`, `brand.md`, `cms.md`, `examples.md`
3. Use the reference post structure from `post-12356-working.html` — never improvise Elementor HTML
4. Run the pre-publish checklist (section 9) before any PUT call
5. Refuse to publish if any checklist item fails
6. Never claim success without confirming saved content matches expectations

---

## 11. SUPPORTED BLOG FORMATS — VARY ACROSS POSTS FOR UNIQUENESS

Review the last 10 posts in `published-posts-inventory.md` and rotate formats.

### Format A — Standard explanatory (default)
H2 sections explaining how/why/what. TL;DR at top, TOC, body H2s with H3 subheadings, images after heavy sections, Related Reading box, Conclusion, FAQ. Reference: post 12356 (Fractional Leadership). Use for: how-to guides, decision guides, technical explanations.

### Format B — Conversational Q&A (LLM-style)
Each body H2 is a verbatim founder question, followed by a clear 2-4 paragraph answer. The H2 questions become the TOC. Use for: topics where founders have many specific sub-questions, decision-making guides.

### Format C — Listicle with opinions
H1 often "X [number] [things]". Each H2 item defended with 2-3 paragraphs. Never neutral surveys — ImpelHub picks sides. Use for: comparisons, "X mistakes", "X signs you're ready", tools/approaches comparisons.

### Format D — Decision-tree / playbook
"Should I X or Y?" or "How to decide between X and Y". Sequenced phases or decisions. Bullet-based criteria at each step. Use for: hire vs don't hire decisions, build vs buy, platform selection, timing decisions.

### Format E — Contrarian thesis
H1 with vivid contrarian phrasing. First sections set up conventional wisdom and why it fails. Remaining sections build the contrarian case with evidence. PAA/FAQ covers pushback questions. Use for: challenging startup orthodoxy, "stop doing X" pieces.

### Format F — Case study / before-and-after
H1 "How [founder segment] [achieved outcome]". Summary states headline result with concrete numbers. Body: The challenge, What they tried first, What actually worked, Results, What others can learn. Use for: real ImpelHub outcomes, specific market segment wins.

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
3. Update `examples.md` if a structural or voice pattern changes
4. Update `brand-primary.txt` or `body-font-size.txt` if a visual value changes
5. Commit and push immediately
6. The fix becomes permanent — never re-fixed manually
