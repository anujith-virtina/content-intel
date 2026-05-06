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

## 5. VOICE AND STYLE

(See clients/virtina/style/voice.md, audience.md, brand.md, examples.md for full detail.)

Key reminders:
- Sentence case headings, not Title Case
- Active voice, second person ("you")
- Banned words: delve, leverage, navigate (verb), realm, landscape, ecosystem, "in today's fast-paced world", "it's important to note", "in conclusion", "revolutionary", "game-changing", "best-in-class", "cutting-edge", "transform your", "unlock value", "synergize"
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

If ANY checklist item fails, fix before publishing. Never push a broken post. This rule overrides any other instruction.
