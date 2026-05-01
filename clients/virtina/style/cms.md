# Publishing — Virtina

## Channels enabled

- [x] file
- [x] cms (WordPress)
- [x] linkedin
- [x] facebook
- [x] instagram
- [x] x

## Critical: Thrive Architect activation (manual step required)

Virtina's WordPress site uses **Thrive Architect** as its visual page builder. Every published post gets its design (SVG icon bullets, section boxes, FAQ accordion, styled content boxes) from Thrive Architect's metadata — NOT from the post_content field.

**The WordPress REST API cannot activate Thrive Architect for a post.** Thrive stores its design data in post meta fields (`tve_updated_post`, `tve_globals`) that are inaccessible via REST API or Application Password auth.

**Required manual step after every REST API push:**
1. Go to WP Admin > Posts > find the post > click Edit
2. Click the **"Launch Thrive Architect"** button (blue, near top of editor)
3. Thrive will import the post HTML into its visual editor
4. Review layout — apply section box backgrounds, confirm FAQ accordion style, verify bullet icons
5. Save from within Thrive Architect

**Without this step, the post renders as plain unstyled HTML** — no design boxes, no SVG bullets, no FAQ accordion. The HTML content we push is still correct and will be correctly parsed by Thrive when it's activated.

---

## Confirmation policy

```yaml
require_confirmation: true   # always show payload and wait for approval before any CMS push
```

---

## Frontmatter schema for published files

Every file in `output/published/` gets this frontmatter:

```yaml
---
title: ...
client: virtina
date: YYYY-MM-DD
slug: ...
author: Virtina
stage: published
category: ...            # B2B eCommerce | Migration | Performance | CRO | Platform Selection
tags: [...]              # 3-5 relevant tags
meta_description: ...    # 150-160 chars for SEO
seo_title: ...           # 60 chars max
canonical_url:           # blank until published to WordPress
featured_image:          # blank for now
channels: [file]
---
```

---

## CMS: WordPress

```yaml
platform: wordpress
endpoint: https://virtina.com/wp-json/wp/v2/posts
auth_method: application_password
auth_env_var: WP_APP_PASSWORD
username_env_var: WP_USERNAME
default_status: draft
format: html
```

---

## Social: LinkedIn

```yaml
char_limit: 3000
preferred_length: 1200-1800
hook_chars: ~210           # what shows above "see more" — first 2 lines must hook
hashtags: 3-5
hashtag_style: lowercase
links_in_post: false       # link goes in first comment, never in post body
cta_style: question or soft invitation — never hard sell
voice: professional but conversational; share an insight, not a brag
```

---

## Social: Facebook

```yaml
preferred_length: 200-500  # Facebook penalizes long posts
hook: first sentence       # truncates fast on mobile
hashtags: 1-2
links_in_post: true
cta_style: direct          # "Read the full breakdown:" / "See how we did it:"
voice: slightly more casual than LinkedIn; credible, not lifestyle
```

---

## Social: Instagram

```yaml
visible_caption: 150-300   # only first ~125 chars show before "more"
hook: first line
hashtags: 5-10             # mix broad (#ecommerce, #B2B) and specific (#magentodevelopment, #shopifyplus)
links_in_post: false       # direct to "link in bio"
cta_style: "Save this post" / "Tag a colleague who needs this" / "Link in bio for the full article"
voice: visual-first — caption supports the image, doesn't replace it
image_note: every Instagram post requires an image suggestion (carousel, single image, or reel concept) — flag for client to provide separately
```

---

## Social: X / Twitter

```yaml
single_post_target: 240-275  # leave room for URL
thread_length: 4-7
thread_format: numbered      # "1/n" at end of each post
first_post: hook (most important)
last_post: link + CTA
hashtags: 1-2                # use sparingly
voice: punchier and more opinionated than LinkedIn — strong takes rewarded
```

---

## Categories

Use one of:
- B2B eCommerce
- Migration
- Performance
- CRO
- Platform Selection

---

## SEO defaults

- Meta description: 150-160 chars
- SEO title: 60 chars max, format `{Title} | Virtina`

---

## WordPress block structure

> Findings verified against reference post ID 41576 (`launching-fast-without-strategy-ecommerce-costs`) raw content via REST API `context=edit`, 2026-04-30.

### Critical: Virtina uses plain HTML, not Gutenberg blocks

Post content is stored and submitted as **flat HTML with no Gutenberg block comment delimiters**. There are zero `<!-- wp: -->` comments in any published post's `content.raw`. Do not wrap content in Gutenberg block markup. Submit raw semantic HTML only.

### Page builder / theme

**No Elementor, no page builder.** Posts use a standard WordPress theme with hand-authored flat HTML. There are no `elementor-*` wrapper divs, no `.wp-block-*` classes, and no shortcodes in post content. The theme applies Font Awesome icon styling via CSS pseudo-elements — it expects the FA license comment + `<span>` structure inside `<li>` elements (see Body list items below).

---

### Summary block

```html
<h2 dir="ltr">Summary</h2>
<p dir="ltr">Summary paragraph text here.</p>
```

The Summary `<h2>` carries `dir="ltr"`. Subsequent paragraphs also use `dir="ltr"`. Do NOT use `<p><strong>Summary:</strong> text</p>`.

---

### Introduction block

```html
<h2>Introduction</h2>
<p dir="ltr">Introduction paragraph.</p>
```

The Introduction `<h2>` does NOT carry `dir="ltr"` (unlike Summary). Paragraphs use `dir="ltr"`.

---

### Table of Contents

```html
<h3>Table of Contents</h3>
<ul>
<li style=""><span style=""><a href="#section-anchor-slug" style="outline: none;">Section Title</a></span></li>
<li><span><a href="#section-anchor-slug" style="outline: none;">Section Title</a></span></li>
<li><span><a href="#conclusion" style="outline: none;">Conclusion</a></span></li>
<li><span><a href="#faq">FAQ&#8217;s</a></span></li>
</ul>
```

- Uses `<h3>` (not `<h2>`)
- First `<li>` has `style=""` on both the `<li>` and the inner `<span>`: `<li style=""><span style="">`. All subsequent `<li>` items have no style attribute on the `<li>`, and the `<span>` has no style attribute either.
- Every body section `<a>` uses `style="outline: none;"`
- The final FAQ link does NOT use `style="outline: none;"` — it is bare: `<a href="#faq">FAQ&#8217;s</a>`
- Hand-rolled HTML — no plugin, no shortcode, no block
- Anchor IDs on section headings: `id="section-anchor-slug"` (kebab-case of heading text)

---

### Body list items (with Font Awesome icon treatment)

```html
<ul>
<li style=""><!--! Font Awesome Free 6.7.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License) Copyright 2024 Fonticons, Inc. --><span>List item text</span></li>
<li style=""><!--! Font Awesome Free 6.7.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License) Copyright 2024 Fonticons, Inc. --><span>List item text</span></li>
</ul>
```

**Critical:** The FA license HTML comment `<!--! Font Awesome Free 6.7.1 ... -->` must appear immediately before `<span>` inside every `<li style="">` in body sections. Without it, the theme's CSS pseudo-element targeting fails and the icon does not render. All `<li>` elements in body bullet lists must use `style=""` (empty style attribute).

The FA comment in full:
```
<!--! Font Awesome Free 6.7.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License) Copyright 2024 Fonticons, Inc. -->
```

Note: TOC `<li>` items do NOT use this FA comment pattern — only body section bullet lists do.

---

### Section headings with anchor IDs

```html
<h2 id="section-anchor-slug">Section heading</h2>
<p dir="ltr">Body paragraph.</p>
```

Body section `<h2>` elements carry `id="..."` for anchor navigation (matches TOC href). No `style=""` or `dir=""` attribute on body `<h2>` elements. Use `<h3>` for subsections. Paragraphs use `dir="ltr"`.

---

### Tables

```html
<table data-rows="5" data-cols="3" data-v="middle">
  <thead>
    <tr>
      <th style="" data-direction=""><p><strong>Column Header</strong></p></th>
      <th style="" data-direction=""><p><strong>Column Header</strong></p></th>
      <th style="" data-direction="" colspan="1" rowspan="1"><p><strong>Column Header</strong></p></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td data-th="Column Header" style=""><p>Cell text</p></td>
      <td data-th="Column Header" style=""><p>Cell text</p></td>
      <td data-th="Column Header" style="" colspan="1" rowspan="1"><p>Cell text</p></td>
    </tr>
  </tbody>
</table>
```

- `<table>` carries `data-rows`, `data-cols`, `data-v` attributes
- `<th>` carries `style=""` and `data-direction=""` attributes; header text wrapped in `<p><strong>...</strong></p>`
- `<td>` carries `data-th="Column Header"` and `style=""` attributes; cell text wrapped in `<p>...</p>`
- Last column in each row uses explicit `colspan="1" rowspan="1"`

---

### Inline images

```html
<span><img alt="Alt text" data-id="41607" width="670" data-init-width="768" height="352" data-init-height="404" title="" loading="lazy" src="https://virtina.com/wp-content/uploads/2026/03/img1.jpg" data-width="670" data-height="352" style="aspect-ratio: auto 768 / 404;"></span>
```

- Images are wrapped in `<span>` (not `<figure>`)
- Carry `data-id`, `data-init-width`, `data-init-height`, `data-width`, `data-height` attributes
- `style="aspect-ratio: auto {original-width} / {original-height};"` inline style
- `loading="lazy"` attribute present
- No `<figcaption>`, no caption wrapper

---

### Conclusion block

```html
<h2 style="" id="conclusion">Conclusion</h2>
<p style="">Conclusion paragraph text.</p>
<p style="">Second conclusion paragraph with links.</p>
```

Both the `<h2>` and every `<p>` in Conclusion carry `style=""` (empty style attribute). The `<h2>` also carries `id="conclusion"`. This pattern distinguishes Conclusion from regular body sections.

---

### FAQ / Frequently Asked Questions block

```html
<h2 style="" id="faq">Frequently Asked Questions</h2>
<h3>Question text here?</h3>
<p dir="ltr">Answer text here.</p>
<h3>Another question?</h3>
<p dir="ltr">Answer text.</p>
```

**CONFIRMED:** FAQ Q&A items are stored directly in `content.raw` as `<h3>` questions followed by `<p dir="ltr">` answers. There is no separate ACF field or plugin for FAQ rendering. The `<h2>` heading carries both `style=""` and `id="faq"`. Answer paragraphs use `dir="ltr"`. There is no accordion — FAQ renders as flat sequential HTML.

---

### People Also Ask block

```html
<h2 id="people-also-ask">People also ask</h2>
<h3>Question text?</h3>
<p dir="ltr">Answer text.</p>
```

Plain `<h2>` with `id="people-also-ask"` (no `style=""`). Questions as `<h3>`, answers as `<p dir="ltr">`. Structurally identical to FAQ section but uses plain heading (no `style=""`).

---

### Author bio

Theme-rendered. Set the post `author` field (integer user ID) in the REST API payload. Bios are not embedded in content. Author ID 9 = Gigi JK (used on reference post).

---

### Setting Yoast SEO meta via REST API

The site uses **Yoast SEO v27.5**. To set SEO fields via the REST API, include these in the `meta` object of the POST/PUT payload:

```json
{
  "meta": {
    "_yoast_wpseo_title": "SEO Title Here | Virtina",
    "_yoast_wpseo_metadesc": "150-160 character meta description.",
    "_yoast_wpseo_focuskw": "focus keyword phrase"
  }
}
```

If Yoast has not registered these keys as `show_in_rest: true`, the API will silently ignore them — set meta fields in the WordPress admin as a fallback. Verify by fetching the post with `context=edit` after the PUT and checking `yoast_head_json.description`.

---

### Categories for B2B/WooCommerce content

| Category name | ID |
|---|---|
| eCommerce | 405 |
| eCommerce SEO | 123 |
| WooCommerce | 79 |
| B2B eCommerce | 84 |
| Performance Optimization | 334 |
| Conversion Optimization | 128 |
| eCommerce Development | 415 |

For a WooCommerce B2B performance article: use categories `[79, 84, 334]`.

---

### REST API payload template (WordPress)

```json
{
  "title": "Post title here",
  "slug": "kebab-case-slug",
  "content": "<h2 dir=\"ltr\">Summary</h2><p dir=\"ltr\">...</p>",
  "status": "draft",
  "categories": [79, 84, 334],
  "tags": [],
  "featured_media": 0,
  "author": 9,
  "meta": {
    "_yoast_wpseo_title": "SEO Title | Virtina",
    "_yoast_wpseo_metadesc": "Meta description 150-160 chars.",
    "_yoast_wpseo_focuskw": "focus keyword"
  }
}
```

**Auth:** HTTP Basic Auth with base64-encoded `username:app_password`. Read credentials from `WP_USERNAME` and `WP_APP_PASSWORD` environment variables.

**Endpoint:** `PUT https://virtina.com/wp-json/wp/v2/posts/{id}` to update existing; `POST https://virtina.com/wp-json/wp/v2/posts` to create new.

**Status must always be `"draft"`** — never `"publish"` without explicit user confirmation.
