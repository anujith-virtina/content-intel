---
client: virtina
date: 2026-04-30
stage: research
topic: WordPress block structure diff — reference post vs draft 42074
---

# WP Diff Findings: Reference Post vs Draft 42074

## Reference post
- **ID:** 41576
- **Slug:** launching-fast-without-strategy-ecommerce-costs
- **Status:** publish
- **Categories:** 405 (eCommerce), 123 (eCommerce SEO)
- **Tags:** [] (none)
- **Author:** 9 (Gigi JK)
- **Featured media:** 41608 (has a featured image)

## Draft post 42074
- **ID:** 42074
- **Slug:** (empty — not set)
- **Status:** draft
- **Categories:** [1] (Uncategorized — wrong)
- **Tags:** [] (none)
- **Author:** 29
- **Featured media:** 0 (no featured image)

---

## Block structure analysis: what the reference post actually uses

The reference post content (`content.raw`) is **plain HTML, not Gutenberg block markup**. There are zero `<!-- wp: -->` block comments in the raw content. Virtina's WordPress stores post content as classic-editor-style HTML, not block editor JSON. This is consistent across both the reference post and the draft.

The post content is serialized as flat HTML, meaning:
- No `<!-- wp:paragraph -->` wrapping
- No `<!-- wp:heading -->` wrapping
- No Gutenberg block delimiters of any kind
- Content is rendered directly as HTML by a page builder or a theme that bypasses block rendering

**Implication:** Future posts must be submitted as raw HTML, not Gutenberg block markup. The `creator` and `publisher` agents should output plain semantic HTML.

---

## Summary block

**Pattern found in reference post:**
```html
<h2 dir="ltr">Summary</h2>
<p dir="ltr">[Summary text paragraph 1]</p>
<p dir="ltr">[Summary text paragraph 2]</p>
```
- Uses a plain `<h2>` with `dir="ltr"` attribute
- No Gutenberg block wrapper
- No custom CSS class
- No shortcode

**Problem in draft 42074:**
The Summary is a `<p>` with a `<strong>Summary:</strong>` label inline — not a proper `<h2>` heading. It will not match the site's visual pattern and will not anchor-link correctly.

**Correct pattern:**
```html
<h2 dir="ltr">Summary</h2>
<p dir="ltr">[Summary content]</p>
```

---

## Introduction block

**Pattern:**
```html
<h2>Introduction</h2>
<p dir="ltr">[paragraph]</p>
```
Note: The Introduction `<h2>` does NOT carry the `dir="ltr"` attribute (unlike the Summary h2). Subsequent `<p>` tags use `dir="ltr"`.

---

## Table of Contents

**Pattern found in reference post:**
```html
<h3>Table of Contents</h3>
<ul>
  <li style=""><span style=""><a href="#section-anchor" style="outline: none;">Section Title</a></span></li>
  <li><span><a href="#section-anchor" style="outline: none;">Section Title</a></span></li>
</ul>
```
- Uses `<h3>` (not `<h2>`) for the TOC label
- `<ul>` list of `<li>` items with `<span>` + `<a>` wrappers
- Anchor links use `style="outline: none;"` on the `<a>` tag
- First `<li>` has `style=""` on the li element; subsequent items may or may not
- **No plugin used** — hand-rolled HTML (no Rank Math TOC block, no LuckyWP shortcode)
- Anchor IDs correspond to the actual section heading text (kebab-case slugs)

**Problem in draft 42074:**
The draft uses a Markdown-style TOC that was uploaded as plain Markdown links `[Section](#section)` — these will not render correctly in WordPress HTML. Additionally the draft uses `<h2>` for the TOC in the published file vs `<h3>` in the reference.

**Correct pattern:**
```html
<h3>Table of Contents</h3>
<ul>
<li style=""><span style=""><a href="#the-60-second-self-audit" style="outline: none;">The 60-second self-audit</a></span></li>
<li><span><a href="#hosting-and-server-configuration" style="outline: none;">Hosting and server configuration</a></span></li>
</ul>
```

---

## FAQ / Frequently Asked Questions section

**Pattern found in reference post:**
```html
<h2 style="">Frequently Asked Questions</h2>
```
The reference post's FAQ section ends the content — there are no actual Q&A items rendered in the raw `content.raw` field. The FAQ questions and answers are likely rendered by a separate plugin (possibly an ACF repeater field, a custom FAQ plugin, or a Yoast SEO FAQ block that is stored outside `content`). The raw content field only contains the `<h2>` heading and nothing after it.

**UNKNOWN — inspect manually.** The FAQ answers are not present in the `content.raw` API response. They may be stored in ACF fields (the post has `acf: []` which returns empty for the authenticated user context, suggesting ACF fields may require a separate endpoint or additional ACF REST API capability) or in a separate custom post type.

**Problem in draft 42074:**
The draft uses plain `<h2>` + `<p>` for each Q&A pair — standard HTML. This will render but may not match the site's FAQ styling or schema markup injection.

---

## Conclusion block

**Pattern found in reference post:**
```html
<h2 style="">Conclusion</h2>
<p style="">[Conclusion paragraph]</p>
```
- The Conclusion `<h2>` uses `style=""` (an empty style attribute, not `dir="ltr"`)
- Paragraph also uses `style=""` (not `dir="ltr"`)
- This is the only section with `style=""` instead of `dir="ltr"` on the h2

**Problem in draft 42074:**
Conclusion uses `<h2>` without `style=""` attribute. Minor but inconsistent.

---

## List items with Font Awesome icons

The reference post uses a specific list pattern with embedded Font Awesome SVG comments inside `<li>` elements:
```html
<ul>
  <li style=""><!--! Font Awesome Free 6.7.1 by @fontawesome ... --><span>item text</span></li>
</ul>
```
This pattern is used for bullet lists in body sections (not the TOC). The FA comment is a license comment, not functional markup, but it signals that the theme injects FA icons into list items via CSS pseudo-elements targeting `<li>` inside certain containers.

**Draft 42074** uses plain `<li>` without spans or FA comments — this will render without the icon treatment.

---

## Image blocks

The reference post content does **not** contain any `<img>` tags in `content.raw`. The featured image is set via the `featured_media: 41608` field (a separate media attachment). Inline images in the content appear to be absent from the reference post entirely.

**Pattern for featured image:** Set via the `featured_media` REST API field (integer, media attachment ID).

**For inline images** (if used): UNKNOWN — the reference post does not contain inline images. Inspect other published posts manually for the image block pattern.

---

## Author bio

Not present in `content.raw`. The author bio is rendered by the theme outside the post content field. Author ID is set via the `author` field (integer). The reference post uses `author: 9` (Gigi JK). Author bios are theme-rendered widgets, not content-embedded blocks.

---

## SEO meta fields (Yoast)

The site uses **Yoast SEO** (plugin v27.5), confirmed via `yoast_head` in the API response.

Yoast SEO meta fields are **not directly settable via the standard WP REST API** using `meta` fields in the POST body — Yoast requires its own REST API endpoint or the `yoast_head_json` fields to already exist on the post.

**What IS settable via REST API:**
- `title` → affects the post title
- `excerpt` → used as meta description fallback

**To set Yoast SEO title and description via REST API**, use the `meta` payload with Yoast's registered meta keys:
```json
{
  "meta": {
    "_yoast_wpseo_title": "SEO Title Here | Virtina",
    "_yoast_wpseo_metadesc": "150-160 char description here."
  }
}
```
These are Yoast's private meta keys. They may or may not be exposed in the REST API depending on whether Yoast has registered them as `show_in_rest: true`. If the PUT request ignores them, Yoast meta must be set via the WordPress admin UI.

**Focus keyword:** `_yoast_wpseo_focuskw`

---

## Categories and tags used in reference post

- **Categories:** 405 (eCommerce), 123 (eCommerce SEO)
- **Tags:** none (empty array)

For a B2B WooCommerce performance article, appropriate categories would be:
- 79 (WooCommerce)
- 84 (B2B eCommerce)
- 334 (Performance Optimization)

---

## Summary of structural problems in draft 42074

1. **Summary block** — `<p><strong>Summary:</strong>` instead of `<h2 dir="ltr">Summary</h2>`
2. **No slug set** — `slug` field is empty; WordPress will auto-generate a verbose slug from the title
3. **Wrong category** — category [1] (Uncategorized) instead of [79, 84, 334]
4. **No featured image** — `featured_media: 0`; reference post has a proper featured image
5. **TOC uses wrong tag** — `<h3>Table of Contents</h3>` is correct per reference, but the list structure uses plain `<li>` without `<span>` wrappers and `style="outline: none;"` on links
6. **List items** — plain `<li>text</li>` without `<span>` wrapper used in reference
7. **No Yoast SEO meta** — focus keyword and meta description not set via `_yoast_wpseo_*` fields
