# ImpelHub Blog — Verified Design System

## 0. CORRECTIONS FROM THE USER, 2026-09-11 — AUTHORITATIVE, READ FIRST

The user manually repaired post 12478 after three failed attempts by me. Their findings override
everything below. Reference post they used: **ID 12330** (`/blog/when-to-hire-first-sales-rep-b2b-saas/`).

### Containers must be BOXED at 860px

The article rendered **full-width (1296px)** instead of the 860px centered column. The document has
**no single wrapping root container** - it is ~13 separate top-level containers, one per section, and
every one had `content_width: "full"`.

**Required on EVERY top-level container:**
```json
"content_width": "boxed",
"boxed_width": {"unit": "px", "size": 860}
```

Do NOT copy `content_width: "full"` from post 12433. It renders at 860px there for other reasons and
does not transfer.

**DEAD END, never retry:** the WP Admin classic "Post Settings" metabox Layout control
(Inherit / Layout 1 / Layout 2) **reverts to "Inherit" on save and never persists** on this theme.

**Verification:** body text must start at the same left x-position as a published reference post,
**~337px**, in every section. Check this before declaring done.

### Arrows ARE the ImpelHub style

Reference 12433 has none, so I deleted all 17 arrows. That was wrong. The user restored them.
- **TL;DR** uses arrow bullet formatting.
- **TOC** is the pink/lavender box **AND** arrow-style links. Both, not either/or.

### Other corrections
- **FAQ heading is TITLE CASE**: "Frequently Asked Questions". Not sentence case.
- **Category: "Ai"**, never "Uncategorized".
- **No separate "Related Reading" block.** Weave those links into the Conclusion prose.
- Author bio + social share block at the bottom already exist site-wide; do not add or duplicate.
- CSS ID anchors required on every TOC target.

---


**Extracted 2026-09-10 from live impelhub.com posts via Chrome computed styles (`getComputedStyle`), not from cached HTML and not estimated.**

Method: loaded posts 12433 and 12356 in a real browser, read computed styles off rendered elements, then swept the 10 most recent posts via `/wp-json/wp/v2/posts` + `DOMParser` for image dimensions and widget types.

This file supersedes any estimated value elsewhere. Where it contradicts `cms.md`, `body-font-size.txt`, or `MUST-FOLLOW-RULES.md`, **this file wins** and the other file should be corrected.

---

## 1. Layout

| Property | Verified value | Notes |
|---|---|---|
| Content container width | **860px** (`859.988px`) | `max-width:100%`. Identical on 12433 and 12356. |
| Container padding | `0px` | Elementor `e-con-full e-flex e-con e-parent` |
| Text alignment | **`start`** (left) | Never centered for body copy or headings |
| Body background | white | |

Everything in the article column is 860px wide. Body images render full-bleed to that 860px.

---

## 2. Typography

Two families. **Red Hat Display** for headings, **Inter** for body. Both are theme-loaded, so do not declare `font-family` inline.

### Body text
| Property | Verified value |
|---|---|
| font-family | `Inter, sans-serif` |
| font-size | **16px** |
| font-weight | 400 |
| line-height | **1.8em = 28.8px** inside a text-editor widget (see 6b). 22.72px only outside one. |
| color | **`rgb(51,51,51)` = `#333333`** |
| margin-bottom | **20px** per `<p>` |
| text-align | start |

> `body-font-size.txt` previously said "16px estimated — verify via dev tools". Now **confirmed 16px**, and the line-height and color are recorded here for the first time.

### H1 (post title)
`Red Hat Display`, **36px**, weight **600**, line-height **46.8px**, color **`rgb(0,0,0)` = `#000000`**, margin-top 25px. Consistent across both posts.

### H2 / H3 — READ THIS BEFORE STYLING ANYTHING

**H2 and H3 carry NO inline `style` attribute on any sampled post.** They are styled by Elementor's per-post generated CSS, driven by each post's widget typography settings. That is why the two "gold standard" posts disagree:

| Post | H2 | H3 |
|---|---|---|
| 12433 (2026-04-22) | Red Hat Display **26px** / 700 / `#0d0b1e` | Red Hat Display **20px** / 700 / `#0d0b1e` |
| 12356 (2026-04-17) | Red Hat Display **40px** / 700 / `#1a1a2e` | Red Hat Display **30px** / 600 / `#3d3d5c` |

**Consequence:** you cannot reproduce a post's heading look by pushing `post_content` alone. The sizes live in Elementor widget settings. **But you CAN write those settings over REST via `_elementor_data` - see section 6b.** Pushing HTML without `_elementor_data` inherits theme defaults and will NOT match either reference post.

**Rule:** push clean semantic `<h2>`/`<h3>` with no inline typography, and **build `_elementor_data` with the 12433 widget settings** (section 6b). Do not invent inline heading CSS to fake it, and do not copy Virtina's `<h3 style="color:#43627f;font-size:22px;">` pattern, which is Thrive-only.

If a single canonical target is needed, use **12433** (26px H2 / 20px H3, `#0d0b1e`) — it is newer and uses the current accordion widget.

### H4 (FAQ questions inside the accordion)
`Red Hat Display`, 20px, weight **400**, color **`rgb(253,158,208)` = `#fd9ed0`** (pink).

> This is the "secondary colour" that `cms.md` recorded as *"not confirmed from CSS; verify via browser dev tools"*. **Now confirmed: `#fd9ed0`.** It appears only as the accordion question colour.

### List items
16px, line-height **28.8px** (= 1.8), color **`#0d0b1e`**. Note the body-copy colour (`#333333`) and the list colour (`#0d0b1e`) genuinely differ.

---

## 3. Colour palette (all verified from computed styles)

| Token | Hex | Where it appears |
|---|---|---|
| Brand purple | **`#5736fd`** | Every link, TOC arrows, inline accents |
| Body text | **`#333333`** | Paragraph copy |
| Heading ink | **`#0d0b1e`** | H2/H3 on 12433, list items |
| Heading ink (older) | `#1a1a2e` / `#3d3d5c` | H2/H3 on 12356 only |
| H1 | `#000000` | Post title |
| Accordion question | **`#fd9ed0`** | FAQ H4 only |

**Links:** `color: rgb(87,54,253)` = `#5736fd`, `text-decoration: none`, `font-weight: 400`. Every link sampled used this exact value, with no underline.

---

## 4. Images — corrected specs

Swept across the 10 most recent posts:

| Size | Count | Meaning |
|---|---|---|
| **1300×600** | 10 of 10 featured | **Featured image, unanimous** |
| **860×452** | 30 occurrences | **Body image, dominant** (matches the 860px container exactly) |
| 1300×600 in body | 4 | older posts |
| 786×1024 | 2 | outlier portrait, do not imitate |

**Featured image: 1300×600. Body images: 860×452.**

> `MUST-FOLLOW-RULES.md` §3 line 125 says *"1200×628 is common for ImpelHub"*. **That is wrong.** Zero of the 10 most recent posts use 1200×628; all 10 use 1300×600.

Body images render at exactly the 860px container width, so 860×452 is native resolution with no upscaling. Border-radius is `0px`. Landscape only.

---

## 4b. Featured image house style (verified 2026-09-11)

Two styles exist. **Style A is the current direction.**

**Style A - AI conceptual scene.** Example: post 12444 (`blog-h1.jpg`). Dark navy boardroom at night,
polished brass/gold machine as the central metaphor, labelled machine parts, red LED readout,
storm-lit city skyline through glass, a cast of executives reacting. Warm gold rim light against cool
blue ambient. Cinematic, photoreal, editorial quality. The metaphor carries the article's thesis
literally ("executives pouring money into a GTM machine whose output reads ERROR").

**Style B - plain stock.** Example: post 12330. Laptop on a desk, soft window light, muted greens,
shallow depth of field. Older and generic. Do not imitate for new posts.

Other alts confirm the Style A pattern: "Split scene: burnout smoke on left, on right a clean...",
"Founder beside a funnel dashboard".

**Always 1300x600.** Never reuse another post's image (MUST-FOLLOW-RULES section 3).

A worked example prompt, with negative prompt and a low-text fallback, is at
`clients/impelhub/output/research/featured-image-prompt-12478.md`.

**No image generation tool is available in this environment.** Do not promise a generated image.
Produce a generation prompt for the user instead, then handle resize, upload, `featured_media` and
alt text once they supply the file.

---

## 5. Elementor widgets in use

Only four widget types appear in article bodies:

- `heading.default`
- `text-editor.default`
- `image.default`
- `nested-accordion.default` ← FAQ

**Accordion history (confirms the standing rule):**

| Date | Post | Widget |
|---|---|---|
| 2026-04-28 | 12444 | `nested-accordion.default` |
| 2026-04-22 | 12433 | `nested-accordion.default` |
| 2026-04-17 | 12356 | `accordion.default` (old) |
| 2026-04-10 | 12330 | `accordion.default` (old) |
| 2026-03-30 and earlier ×6 | | `nested-accordion.default` |

8 of 10, including both most recent, use `nested-accordion.default`. The two `accordion.default` posts are an April blip. **Always use `nested-accordion.default`.**

---

## 6. TOC — CORRECTED 2026-09-10

**The earlier "Unicode arrow TOC" entry in this file and in `MUST-FOLLOW-RULES.md` was WRONG.**
It was inferred from an arrow character appearing somewhere in page HTML. Reference post 12433
contains **zero** Unicode arrows and uses `<ol>`, never `<ul>`.

The live TOC is a single `text-editor` widget holding a lavender box with a numbered list. There is
**no separate H3 "Table of Contents" heading widget**:

```html
<div style="background:#FBE9FF;border-radius:8px;padding:18px 24px;"><div style="font-weight:700;color:#0d0b1e;font-size:18px;margin-bottom:8px;">Table of Contents</div><ol style="margin:0;padding-left:20px;color:#0d0b1e;font-size:16px;line-height:1.8;"><li><a href="#anchor">Section title</a></li></ol></div>
```

Links inherit `#5736fd`; no inline link colour needed.

## 6a. THE H2 ACCENT BAR — easy to miss, very visible

Every H2 heading widget carries `_css_classes: "blog-title-h2"`. The theme then draws a purple bar
under the heading:

```css
.blog-title-h2 h2 { position: relative; padding-bottom: 10px; }
.blog-title-h2 h2::before { position: absolute; bottom: 0; left: 0;
                            width: 76px; height: 3px; background: #5736fd; content: ""; }
```

Omit the class and the bar disappears. This is a major part of the ImpelHub blog look and it is
invisible to a `getComputedStyle` sweep of the `h2` element itself, because the bar lives on a
pseudo-element driven by a class set in `_elementor_data`.

**Anchors use `css_id` on the heading widget, never `_element_id`.** The wrong key silently breaks
every TOC link.

## 6c. Never trust computed styles alone

Both of the errors above survived a full `getComputedStyle` audit. They were only caught by taking a
screenshot of a live post and looking at it. **Always render and look**, then measure.

## 6b. THE RENDERING RULE - `_elementor_data` IS THE POST

**Corrected 2026-09-10 after post 12478 rendered wrong.**

An ImpelHub post is NOT its `post_content`. It is its **`_elementor_data`** meta.
Elementor generates the per-post CSS **inline at render time from that JSON**. There are no
external `post-{id}.css` files on this install (both 12433 and 12478 return 404), so the styling
comes entirely from the widget settings inside `_elementor_data`.

Push Elementor-shaped HTML with `_elementor_data` empty and the post renders with **theme
defaults**: wrong heading sizes, wrong colours, wrong spacing. That is exactly what happened to
12478 on its first push.

`_elementor_data` **IS REST-writable** on ImpelHub. Send it as a JSON string in `meta`:

```json
"meta": {
  "_elementor_edit_mode": "builder",
  "_elementor_template_type": "wp-post",
  "_elementor_data": "<json string>"
}
```

This is the same approach the ChatSKU build scripts already use. **This is NOT like Virtina's
Thrive `_tve_updated_post` limit** - do not carry that assumption across; there it genuinely
cannot be written, here it can.

### The canonical widget settings (copied from 12433, verified in its inline CSS)

| Element | Settings |
|---|---|
| container | `content_width: full`, padding 0, **margin-top 35px** |
| H2 heading | `title_color #0d0b1e`, **26px**, weight **700**, line-height **1.35em** |
| H3 heading | `title_color #0d0b1e`, **20px**, weight **700**, line-height **1.4em** |
| text-editor | **16px**, line-height **1.8em** |
| image | `align: center` |
| nested-accordion | title/icon `#FD9ED0` hover+active, 20px, weight 400, lh 1.33em, padding 20/0/20/0, `title_space_between: 0`, header border-bottom 1px `#D5D8DC` |

Working builder: `clients/impelhub/output/research/build_elementor_12478.py`.

> **Body line-height correction.** This file previously recorded body line-height as 22.72px (1.42)
> from a computed-style reading. That measurement came from a paragraph outside a styled
> text-editor widget. Inside a text-editor widget the real value is **1.8em = 28.8px**, which is
> why list items measured 28.8px. Use **1.8em**.

> **Section spacing.** Containers carry **35px top margin**. This was never captured before and is
> a large part of why a REST-pushed post looks visually wrong even when the fonts are right.

---

## 7. What this means for REST publishing

1. Container width, body typography, link colour and image sizes are all reproducible through `post_content`.
2. **H2/H3 sizing is not.** It lives in Elementor widget settings. Expect a REST-pushed draft to render with theme-default headings until opened in Elementor.
3. This is the ImpelHub analogue of Virtina's Thrive `_tve_updated_post` limit: the REST API is not the whole rendering story. Report it as a manual step rather than claiming the live page will match.

---

## Re-verification

Re-run this extraction if the theme is updated or a redesign ships. Method: load a recent post in Chrome, `getComputedStyle` on `p`, `h1`–`h4`, `a`, `li` inside `.elementor-{postid}`, then sweep `/wp-json/wp/v2/posts` for image dimensions and `data-widget_type` values.
