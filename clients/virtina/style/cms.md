# Publishing — Virtina

## Channels enabled

- [x] file
- [x] cms (WordPress)
- [x] linkedin
- [x] facebook
- [x] instagram
- [x] x

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

> Findings based on reference post ID 41576 (`launching-fast-without-strategy-ecommerce-costs`), fetched 2026-04-30 with `context=edit`.

### Critical: Virtina uses plain HTML, not Gutenberg blocks

Post content is stored and submitted as **flat HTML with no Gutenberg block comment delimiters**. There are zero `<!-- wp: -->` comments in any published post's `content.raw`. Do not wrap content in Gutenberg block markup. Submit raw semantic HTML only.

---

### Summary block

```html
<h2 dir="ltr">Summary</h2>
<p dir="ltr">Summary paragraph text here.</p>
```

The Summary is a standard `<h2>` with `dir="ltr"`. Do NOT use `<p><strong>Summary:</strong> text</p>`.

---

### Introduction block

```html
<h2>Introduction</h2>
<p dir="ltr">Introduction paragraph.</p>
```

Note: The Introduction `<h2>` does NOT carry `dir="ltr"` (unlike Summary). Paragraphs use `dir="ltr"`.

---

### Table of Contents

```html
<h3>Table of Contents</h3>
<ul>
<li style=""><span style=""><a href="#section-anchor-slug" style="outline: none;">Section Title</a></span></li>
<li><span><a href="#section-anchor-slug" style="outline: none;">Section Title</a></span></li>
<li><span><a href="#conclusion" style="outline: none;">Conclusion</a></span></li>
<li><span><a href="#faq">FAQ</a></span></li>
</ul>
```

- Uses `<h3>` (not `<h2>`)
- First `<li>` has `style=""` on the element; subsequent items have no style attribute
- Every `<a>` uses `style="outline: none;"`
- Hand-rolled HTML — no plugin, no shortcode, no block
- Anchor IDs are kebab-case slugs matching the section heading text

---

### Body list items (with icon treatment)

```html
<ul>
<li style=""><span>List item text</span></li>
<li style=""><span>List item text</span></li>
</ul>
```

Body list items use `<li style=""><span>text</span></li>` pattern (not plain `<li>text</li>`). The theme applies Font Awesome icon treatment via CSS pseudo-elements to this `<span>` structure. In the reference post these items also contain an FA license comment before the span — that comment is cosmetic only and does not need to be reproduced.

---

### Section headings

```html
<h2>Section heading</h2>
<p dir="ltr">Body paragraph.</p>
```

Standard `<h2>` without style or dir attribute for most body sections. Use `<h3>` for subsections. Paragraphs use `dir="ltr"`.

---

### Conclusion block

```html
<h2 style="">Conclusion</h2>
<p style="">Conclusion paragraph text.</p>
```

Note the `style=""` empty attribute on both the `<h2>` and the first `<p>` — this distinguishes Conclusion from regular body sections visually.

---

### FAQ / Frequently Asked Questions block

```html
<h2 style="">Frequently Asked Questions</h2>
```

**UNKNOWN — inspect manually.** The FAQ answers are not present in `content.raw`. They appear to be stored outside the post content field — likely in ACF fields, a custom FAQ plugin, or a separate post type. The raw API response for the reference post (ID 41576) contains only the `<h2>` heading with no Q&A items following it. Until this is confirmed, place FAQ Q&A as standard HTML:

```html
<h2 style="">Frequently Asked Questions</h2>
<h3>Question text here?</h3>
<p>Answer text here.</p>
```

---

### Image blocks

**UNKNOWN — inspect manually.** The reference post has no `<img>` tags in `content.raw`. The featured image is set via the `featured_media` REST API field (integer, media attachment ID). Inline images may be absent from this post type or stored differently. Do not guess at image block markup.

**Featured image:** Set via REST API as `"featured_media": <attachment_id>`. The attachment must already exist in the WordPress media library.

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
