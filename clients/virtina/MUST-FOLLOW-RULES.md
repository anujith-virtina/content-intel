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

### REAL PROFESSIONAL PHOTOS, NEVER BRANDED TEXT CARDS

Virtina images must be real photographs of people, workplaces, or objects — never programmatically generated text-on-color cards (no matter how branded they look). Pillow-generated images with titles like "B2B Pricing Architecture" or "ERP Integration" printed on a teal background are categorically rejected.

**Required image sourcing order:**
1. Unsplash source URL: `https://source.unsplash.com/{w}x{h}/?{keywords}` — try 3 keyword variants
2. Unsplash random featured: `https://source.unsplash.com/featured/{w}x{h}/`
3. picsum.photos: `https://picsum.photos/{w}/{h}` — real random photographs, acceptable fallback
4. NEVER fall through to Pillow text card generation

**Image processing requirements:**
- Download raw photo bytes, verify size > 5000 bytes
- Resize using scale-to-cover + center-crop to exact target dimensions
- Compress to JPEG quality 82/75/65/55 until under 200KB
- All image fetching must follow HTTP redirects

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

## 4a. BULLET LISTS

Every bullet list in Virtina body content must use the exact template extracted from post 42074. Default browser round bullets are categorically rejected.

**Required markup (copy verbatim, extracted from 42074):**
```html
<ul style="list-style:none;padding-left:4px;margin:8px 0 16px 0;">
<li style="display:flex;align-items:flex-start;gap:8px;padding:4px 0;"><svg viewBox="0 0 512 512" width="10" height="10" style="fill:#43627f;flex-shrink:0;margin-top:5px;" xmlns="http://www.w3.org/2000/svg"><path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512z"/></svg><span style="font-size:16px;line-height:1.75;">List item text here</span></li>
</ul>
```

Rules:
- `list-style:none` on `<ul>` (no `!important` — body lists are not TOC)
- `<li>` uses `display:flex;align-items:flex-start` so icon aligns with first line of text, never floats above
- SVG circle icon: `fill:#43627f` (Virtina slate), `width="10" height="10"`, `flex-shrink:0`, `margin-top:5px`
- `<span>` wraps all item text: `font-size:16px;line-height:1.75;`
- TOC lists are different — they use `!important` overrides and arrow characters, not this template

The canonical template file lives at `clients/virtina/list-template.html`. Refresh it from post 42074 if its content ever changes.

When fixing existing lists: strip any existing SVG icons and span wrappers from each `<li>`, then re-wrap using this exact template. Never leave plain `<li>text</li>` without the SVG+span structure.

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
- [ ] No image is a Pillow-generated text-on-color card (all images must be real photographs)
- [ ] Featured image sourced from Unsplash or picsum.photos (real photo, not branded card)
- [ ] All body images sourced from Unsplash or picsum.photos (real photos, not branded cards)
- [ ] All body bullet lists use SVG circle icon + flex layout (not default round bullets)
- [ ] No plain <li>text</li> without SVG icon and span wrapper
- [ ] Bullet icon fill color is #43627f (Virtina slate), not any other color

If ANY checklist item fails, fix before publishing. Never push a broken post. This rule overrides any other instruction.
