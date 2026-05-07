# REFERENCE POST — ALWAYS COPY THIS STRUCTURE

Post ID 42074 on virtina.com is the locked reference for every Virtina blog. Before writing or publishing any new Virtina post:

1. Fetch post 42074 via WordPress REST API (?context=edit)
2. Use its EXACT HTML structure for: Summary block, TOC, body section headings, body image markup, FAQ accordion, Conclusion block, featured image markup
3. Copy the same inline styles, CSS classes, id attributes, span wrappers, list-style overrides
4. Only change the TEXT CONTENT — never the HTML structure
5. Verify the new post's HTML structure matches 42074 by diffing before publishing

Local cached copy lives at reference-42074-working.html in project root. Refresh this cache once a month or when 42074 is manually updated.

DO NOT try to construct Thrive/Gutenberg HTML from scratch. DO NOT improvise structure. ALWAYS clone from 42074.

This rule overrides everything else in this file. If you cannot fetch 42074, refuse to publish until you can.

---

# Virtina Blog — Mandatory Rules (Locked Memory)

This file is the source of truth for every Virtina blog. The orchestrator, creator, analyzer, and publisher agents MUST read this file at the start of every Virtina task. These rules were established after extensive QA in May 2026. Do not deviate.

Reference benchmark for visual and structural match: https://virtina.com/launching-fast-without-strategy-ecommerce-costs/

## 1. TABLE OF CONTENTS

Required structure exactly:

```html
<h3>Table of Contents</h3>
<ul style="list-style:none !important; padding-left:0 !important; margin:0 0 1.5em 0 !important;">
  <li style="list-style:none !important; padding:8px 0 !important; padding-left:32px !important; position:relative !important; line-height:1.5 !important; margin:0 !important;">
    <span aria-hidden="true" style="position:absolute !important; left:0 !important; top:8px !important; color:#16afa0 !important; font-weight:bold !important; font-size:1.1em !important;">→</span>
    <a href="#anchor-id" style="color:#16afa0 !important; text-decoration:none !important;">Section title</a>
  </li>
</ul>
```

Rules:
- Heading must be H3, never H2
- Items must be real <a href="#anchor"> links, never plain text
- Arrow color and link text color: #16afa0 (Virtina brand teal)
- list-style:none !important on BOTH ul AND li to kill default round bullets
- !important on every property to override Thrive theme defaults
- Every H2 in the article body must have id attribute matching the TOC anchor href
- Place TOC after Introduction, before first body H2

## 2. IMAGES

### Featured image (required, never skip)
- Exactly 1309 x 500 pixels
- Set via featured_media field with a real uploaded media ID, never 0
- Filename: {slug}-featured-1309x500.jpg
- Alt text required: 80-150 chars, descriptive, naturally includes 1-2 article keywords
- Placeholder fallback if real image not available: https://placehold.co/1309x500
  Alt text starts with "TODO REPLACE: " followed by descriptive text

### Body images (required, never skip)
- Minimum 2, default 3, maximum 5 (5 only if article exceeds 2500 words)
- Every body image exactly 670 x 352 pixels — same dimensions for all, never mix sizes
- Filename: {slug}-section-{n}-670x352.jpg
- Alt text required for each: 80-150 chars, unique per image, descriptive
- Use Gutenberg block markup with explicit width="670" height="352":

```html
<!-- wp:image {"width":"670px","height":"352px","sizeSlug":"large","className":"is-resized"} -->
<figure class="wp-block-image size-large is-resized"><img src="..." alt="..." width="670" height="352"/></figure>
<!-- /wp:image -->
```

### Alt text quality
- Never generic ("image", "photo", "diagram", "illustration")
- Always describe what's shown AND the concept it illustrates
- Naturally include 1-2 article keywords without stuffing
- Length: 80-150 characters

### REAL IMAGES, NEVER PLACEHOLDER URLS

For every Virtina post, body and featured images must be real files uploaded to virtina.com WordPress media library via POST /wp/v2/media. Never reference placehold.co, placeholder.com, or any external placeholder URL in published post content. Placeholder URLs are only acceptable during draft generation as a marker; they MUST be replaced with uploaded media before any PUT call to /wp/v2/posts/{id}. The publisher's pre-publish checklist must verify every image src begins with https://virtina.com/wp-content/uploads/ — no exceptions.

If real image generation fails for a section, use picsum.photos random real photographs as fallback (not Pillow branded cards). Never publish with external placeholder URLs.

### REAL TOPICAL PHOTOS — USE WORKING APIS, NOT DEAD ENDPOINTS

NEVER use these (they are deprecated, random, or fake):
- `source.unsplash.com` — DEPRECATED 2024. Returns random unrelated images regardless of keywords. A B2B integration article ended up with pink flowers and forest canyons because of this endpoint. It is dead. Never use it under any condition.
- `placehold.co` or any external placeholder service in saved post content
- Pillow text-on-color cards (e.g. teal background with "B2B Pricing Architecture" text) — categorically rejected
- Random stock images with no topical relevance (flowers, landscapes, nature scenes on a B2B tech article)

ALWAYS use one of these working APIs (in priority order):
1. **Pexels API**: `https://api.pexels.com/v1/search?query={keywords}&orientation=landscape&per_page=5`
   - Header: `Authorization: $env:PEXELS_API_KEY`
   - Use `src.large2x` field from each photo in response
2. **Pixabay API**: `https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={keywords}&image_type=photo&orientation=horizontal&per_page=5`
   - Use `largeImageURL` field from each hit in response

**Image sourcing process:**
1. Search with topic-specific keywords (e.g. `warehouse manager laptop` for B2B operations)
2. Pick the first relevant result
3. Download the high-res source URL
4. Crop with Pillow: scale-to-cover + center-crop to exact target dimensions
5. Compress to JPEG quality 82, verify under 200KB
6. Upload to virtina.com via POST /wp-json/wp/v2/media (multipart)
7. Set alt_text via POST on the media item
8. Reference only the uploaded virtina.com URL in post content

**If no API key is set:** STOP and tell the user to register at https://www.pexels.com/api/new/ (free, 2 minutes) and run: `[System.Environment]::SetEnvironmentVariable('PEXELS_API_KEY', 'your-key', 'User')`. Do NOT use random or unrelated images. Honesty about missing credentials beats publishing pink flowers on a B2B integration article.

## 3. LINKS

- Every external link (non-virtina.com): target="_blank" rel="noopener noreferrer"
- Every internal virtina.com link: no target attribute, opens in same tab
- Every article must include 5-10 internal Virtina links to service, platform, industry, or related blog pages
- Links woven into body prose naturally — not in intro, not in conclusion
- Anchor text varied — never "click here", never the same anchor twice in one article

## 4. STRUCTURE

Every Virtina article must include in this order:

1. H1 title (sentence case, never Title Case)
2. Author byline + category + updated date line
3. Featured image (1309x500)
4. <h2>Summary</h2> + 2-3 sentence summary
5. <h2>Introduction</h2> + intro paragraphs
6. <h3>Table of Contents</h3> with styled list per rule 1
7. Body sections (H2 main, H3 sub-sections, body images at 670x352 placed at logical breakpoints)
8. <h2>People Also Ask</h2> with 3-4 short Q&As
9. <h2>Conclusion</h2> + closing paragraph
10. <h2>Frequently Asked Questions</h2> with 6-8 Q&As (use H4 for question text)
11. Author bio block

## 4a. BULLET LISTS — SIMPLE BULLETPROOF MARKUP

Use this exact pattern, no variations. This is the locked Virtina bullet template:

```html
<ul style="list-style:none; padding-left:0; margin:0 0 1.5em 0;">
<li style="position:relative; padding:8px 0 8px 28px; line-height:1.6; margin:0;"><span style="position:absolute; left:0; top:14px; width:10px; height:10px; background-color:#16afa0; border-radius:50%; display:inline-block;"></span><strong>Heading.</strong> Body text here.</li>
<li style="position:relative; padding:8px 0 8px 28px; line-height:1.6; margin:0;"><span style="position:absolute; left:0; top:14px; width:10px; height:10px; background-color:#16afa0; border-radius:50%; display:inline-block;"></span><strong>Next heading.</strong> Body text here.</li>
</ul>
```

Why this exact pattern:
- Pure CSS circle via `border-radius:50%` + `background-color:#16afa0` — no SVG, no Font Awesome
- `position:absolute; left:0; top:14px` aligns the circle with first-line text baseline, never floating above
- `padding:8px 0 8px 28px` on `<li>` creates indented space for the circle and vertical rhythm
- No HTML entities, no icon classes, no external dependencies
- Cannot be corrupted by Thrive serialization
- Renders identically in all browsers

**Forbidden — these ALL caused real failures:**
- SVG inline icons (`<svg viewBox="0 0 512 512"...>`) — the outer `<ul>` tag got double-wrapped as `<<ul...>>` on PUT, rendering visible `<` and `>` characters as text on the live page
- `display:flex` + `align-items:flex-start` approach — Thrive serializer corrupted the outer tag on save
- Font Awesome icons (`<i class="fa-circle">`) — fail when FA stylesheet not loaded
- HTML entities like `&#9679;` or `&bull;`
- Default `<ul><li>` without list-style:none (shows browser round bullets)
- Orphan `<<` or `>>` text outside of valid HTML tags

**TOC lists are different** — they use `!important` on all properties and arrow text characters. This template is for body content lists only.

**Pre-publish verification:** After any PUT, GET the saved content and search for `<<` or `>>` — if found, the markup is corrupted. Also check for `list-style:none;padding-left:4px` (old SVG-style) — if found, rewrite before publish.

## 5. VOICE AND STYLE

(See clients/virtina/style/voice.md, audience.md, brand.md, examples.md for full detail.)

Key reminders:
- Sentence case headings, not Title Case
- Active voice, second person ("you")
- Banned words: delve, leverage, navigate (verb), realm, landscape, ecosystem, "in today's fast-paced world", "it's important to note", "in conclusion", "revolutionary", "game-changing", "best-in-class", "cutting-edge", "transform your", "unlock value", "synergize"
- Banned characters: Em dashes (— Unicode U+2014) and HTML entity &mdash; are forbidden in all Virtina content. Use periods, commas, colons, or regular hyphens instead. The publisher must scan content for em dashes before any PUT and replace them with proper punctuation. This applies to all article body, FAQ, summary, and conclusion text.
- 1500-2500 words for standard articles, 2500-3500 for pillar guides
- Always include Summary block at top
- Quotes from sources: under 15 words, paraphrase otherwise

## 6. WORDPRESS PUBLISHING

- Status always: draft (never auto-publish)
- REST API endpoint: /wp-json/wp/v2/posts with Basic Auth from $env:WP_USERNAME and $env:WP_APP_PASSWORD
- featured_media field always set with a real media ID, never 0
- Yoast/Rank Math meta_description: 150-160 characters
- SEO title: 60 characters maximum, format "{Title} | Virtina"
- Set appropriate category and tags from Virtina's existing taxonomy

## 7. PRE-PUBLISH CHECKLIST

The publisher MUST verify ALL of these before any PUT call. If any fails, fix before publishing.

- [ ] Featured image set (featured_media is a real ID, not 0)
- [ ] Featured image is exactly 1309x500
- [ ] Featured image has alt text 80-150 chars, descriptive
- [ ] Body image count between 2 and 5
- [ ] All body images are exactly 670x352
- [ ] All body images have unique descriptive alt text 80-150 chars
- [ ] No image missing alt text
- [ ] No image uses generic alt text
- [ ] TOC heading is H3
- [ ] TOC items are <a href="#anchor"> real links, color #16afa0
- [ ] TOC has visible teal arrows, NOT default round bullets
- [ ] list-style:none with !important on both ul and li
- [ ] Every H2 has matching id attribute
- [ ] All external links: target="_blank" rel="noopener noreferrer"
- [ ] All internal virtina.com links open in same tab
- [ ] Article has 5-10 internal Virtina links
- [ ] Status is draft
- [ ] No banned words from voice.md present
- [ ] Summary, Introduction, Conclusion, FAQ all present
- [ ] Word count appropriate
- [ ] No em dashes (— U+2014) or &mdash; entities anywhere in content
- [ ] All image src URLs begin with https://virtina.com/wp-content/uploads/ — no external placeholder URLs
- [ ] No source.unsplash.com URLs in content (deprecated, returns random unrelated photos)
- [ ] No placehold.co URLs in content
- [ ] All images visually relevant to post topic (warehouse/business/data/ecommerce, NOT flowers/landscapes/nature)
- [ ] All body bullet lists use the simple CSS-circle pattern (background-color:#16afa0; border-radius:50%)
- [ ] No orphan << or >> text in body content (indicates Thrive serializer corrupted a <ul> tag)
- [ ] All bullets align with first-line text baseline (position:absolute; top:14px)

If ANY checklist item fails, fix before publishing. Never push a broken post. This rule overrides any other instruction.
