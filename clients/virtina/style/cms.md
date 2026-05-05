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

Confirmed against reference post 41576 content.raw and rendered Thrive CSS, 2026-05-05.

**Critical:** Bullets vs arrows — the `<ul>` MUST have `list-style:none!important` or the browser shows default disc bullets. Thrive normally applies this via its CSS class `.tcb-styled-list`, but that class is only present after Thrive activation. For REST API pushes, apply `list-style:none!important` inline on both `<ul>` and every `<li>`.

```html
<h3>Table of Contents</h3>
<ul style="list-style:none!important;padding-left:0!important;margin:0 0 1.5em 0!important;">
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#00a0e2;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#section-anchor-slug" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">Section Title</a></li>
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#00a0e2;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#conclusion" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">Conclusion</a></li>
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#00a0e2;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#faq" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">FAQ</a></li>
</ul>
```

**Rules:**
- Plain `<h3>` — NO inline style on the heading
- `list-style:none!important` on BOTH `<ul>` AND every `<li>` — mandatory, kills disc bullets
- `padding-left:32px` on `<li>` creates space for the absolute-positioned arrow SVG
- Arrow: inline SVG, `fill:#00a0e2`, `position:absolute;left:0;top:8px`, inside `<span aria-hidden="true">`
- Arrow SVG path: `M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z`
- Link: `color:#00a0e2!important`, `font-family:metropolis,arial!important`, `font-size:16px!important`, `font-weight:500!important`
- Links open in same tab — no `target` attribute
- Anchor IDs on section headings: `id="section-anchor-slug"` (kebab-case)
- **Font:** `metropolis, arial` — confirmed from `body { font-family:metropolis,arial }` page CSS

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

> Specs confirmed from reference post 41576 CSS: `.thrv_toggle_title` (collapsed), `.tve-state-expanded` (open), `.tve-toggle-text`, `tve-u-19d0618d368`, 2026-05-02.

The FAQ section uses an inline-styled `<details>/<summary>` HTML5 accordion that visually replicates Thrive Architect's toggle component. Because WordPress's `wp_kses_post` filter strips Thrive wrapper divs on REST API save, we use `<details>/<summary>` with matching inline CSS instead.

**Inject this `<style>` block once, immediately before the FAQ `<h2>` heading:**

```html
<style>
details.vfaq>summary{list-style:none;}
details.vfaq>summary::-webkit-details-marker{display:none;}
details.vfaq[open]>summary{background:linear-gradient(#00d5c0,#00d5c0)!important;}
details.vfaq .vfaq-answer p{font-size:15px!important;color:#6e6e6e!important;line-height:1.75!important;}
</style>
```

**FAQ heading:**

```html
<h2 style="" id="faq">Frequently Asked Questions</h2>
```

**Each FAQ item (repeat for every Q&A pair):**

```html
<details class="vfaq" style="background:transparent;margin-top:7px;">
<summary style="cursor:pointer;padding:17px;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:12px;background:rgba(245,245,245,0.5);">
<span style="font-size:16px;font-weight:600;color:#43627f;line-height:2;flex:1;">Question text here?</span>
<svg viewBox="0 0 24 24" width="17" height="17" style="fill:#50565f;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg"><path d="M16,12A2,2 0 0,1 18,10A2,2 0 0,1 20,12A2,2 0 0,1 18,14A2,2 0 0,1 16,12M10,12A2,2 0 0,1 12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12M4,12A2,2 0 0,1 6,10A2,2 0 0,1 8,12A2,2 0 0,1 6,14A2,2 0 0,1 4,12Z"/></svg>
</summary>
<div class="vfaq-answer" style="padding:30px 22px;background:#fff;">
<p>Answer text here.</p>
</div>
</details>
```

**Visual rules (confirmed from ref 41576):**
- Collapsed header background: `rgba(245,245,245,0.5)` — near-white
- Open header background: `linear-gradient(#00d5c0,#00d5c0)` — teal (applied via `details[open]>summary` CSS)
- Question text: 16px, `font-weight:600`, `color:#43627f`, `line-height:2`, `flex:1`
- Dots icon: 17px SVG (three-dots / more-vert), `fill:#50565f`, on the **right** side
- Answer container: `padding:30px 22px`, `background:#fff`
- Answer paragraph text: `font-size:15px`, `color:#6e6e6e`, `line-height:1.75` (forced via CSS `!important` to override inline paragraph styles)
- `margin-top:7px` between items; no margin on outer container

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
