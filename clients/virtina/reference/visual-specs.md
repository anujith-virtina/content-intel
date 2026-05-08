---
title: Virtina Visual Specifications
source: Extracted from post 42108 (working reference, verified May 2026)
last_updated: 2026-05-08
---

# Virtina Visual Specifications

Extracted from post ID 42108 — the verified working reference. Every new post must match these specs exactly. Read clients/virtina/brand-teal.txt and body-font-size.txt for canonical hex/size values.

---

## A. Brand Colors

| Element | Hex | Notes |
|---|---|---|
| Bullet circle background | `#43627f` | Virtina slate — verified from 42108 body bullets and 42074 SVG fills |
| TOC SVG arrow fill | `#43627f` | Same slate as bullet circles |
| H2 heading text | `#43627f` | All H2 headings |
| H3 heading text | `#43627f` | All H3 headings |
| FAQ question text | `#43627f` | `<span>` inside `<summary>` |
| TOC link text | `#00a0e2` | Virtina link blue — `!important` required |
| Internal link text | `#00a0e2` | Applied via `style="outline: none;"` on `<a>` |
| Body paragraph text | `#2d3e50` | Explicit on bullet `<span>` text; body `<p>` inherits |
| Summary box background | `linear-gradient(rgba(0,213,192,0.28),rgba(0,213,192,0.28))` | Teal tint |
| Introduction box background | `linear-gradient(rgba(241,243,250,0.5),rgba(241,243,250,0.5))` | Light grey |
| Body section box background | `linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13))` | Light blue tint |
| PAA box background | `linear-gradient(rgba(241,243,250,0.5),rgba(241,243,250,0.5))` | Same as intro |
| Conclusion box background | `#00d5c0` | Solid bright teal — text is `#ffffff` |
| FAQ question background | `rgba(245,245,245,0.5)` | Inside `<summary>` |
| FAQ answer background | `#fff` | Inside `.vfaq-answer` div |
| FAQ chevron icon fill | `#50565f` | SVG in `<summary>` |

---

## B. Typography

| Element | Font-size | Font-weight | Line-height | Color |
|---|---|---|---|---|
| H1 | (Thrive default) | bold | — | — |
| H2 | `30px` | normal | — | `#43627f` |
| H3 | `23px` | normal | — | `#43627f` |
| Body paragraph | `16px` | normal | `1.75` | inherited |
| TOC link | `16px` | `500` | `1.5` | `#00a0e2` + `!important` |
| Bullet circle size | 9×9px | — | — | — |
| Bullet text span | `16px` | normal | `1.75` | `#2d3e50` |
| Bullet bold heading | (inline `<strong>`) | bold | — | inherits |
| FAQ question | `16px` | `600` | `2` | `#43627f` |
| FAQ answer | `16px` | normal | `1.75` | inherited |
| Conclusion text | `16px` | normal | `1.75` | `#ffffff` |
| Internal link | `16px` | normal | — | `#00a0e2` |

Font family on TOC links: `metropolis,arial` (set via `!important`).

---

## C. Spacing

| Element | Value |
|---|---|
| Section box border-radius | `20px` |
| Section box padding | `30px` |
| Section box bottom margin | `28px` (margin: `0 0 28px 0`) |
| Image span margin | `margin:20px 0` |
| Bullet `<ul>` margin | `8px 0 16px 0` |
| Bullet `<ul>` padding-left | `4px` |
| Bullet `<li>` padding | `6px 0` |
| Bullet `<li>` gap (flex) | `10px` |
| Bullet circle top offset | `margin-top:6px` |
| TOC `<ul>` bottom margin | `1.5em` |
| TOC `<li>` padding | `8px 0 8px 32px` |
| TOC arrow top | `top:8px` |
| FAQ item top margin | `margin-top:7px` |
| FAQ summary padding | `17px` |
| FAQ answer padding | `30px 22px` |

---

## D. Image Dimensions

| Type | Width | Height | Format | Max file size |
|---|---|---|---|---|
| Featured | 1309 px | 500 px | JPEG q82 | 200 KB |
| Body | 670 px | 352 px | JPEG q82 | 200 KB |

- Resize method: scale-to-cover + center-crop (Pillow `LANCZOS`)
- All body images must be the same dimensions — never mix sizes
- Wrapped in `<span style="display:block;margin:20px 0;">`
- `width="670" height="352"` attributes set explicitly on `<img>`
- `data-init-width`, `data-init-height`, `data-width`, `data-height` also set
- `style="aspect-ratio: auto 670 / 352;max-width:100%;"` on `<img>`
- `loading="lazy"` on all body images
- `data-id` set to the WordPress media ID

---

## E. Link Behavior

| Link type | Target | Rel | Style |
|---|---|---|---|
| Internal (virtina.com) | none (same tab) | none | `style="outline: none;"` |
| External | `_blank` | `noopener noreferrer` | — |
| TOC anchor | none (same page) | none | `color:#00a0e2!important` + font-family + font-weight |

Underline policy: `text-decoration:none!important` on TOC links. Internal body links do not explicitly set underline (Thrive default applies).

---

## F. Section Wrapper Reference

Each major section is wrapped in a styled `<div>`. From post 42108:

```
Summary:      background:linear-gradient(rgba(0,213,192,0.28),rgba(0,213,192,0.28));border-radius:20px;padding:30px;margin:0 0 28px 0
Introduction: background:linear-gradient(rgba(241,243,250,0.5),rgba(241,243,250,0.5));border-radius:20px;padding:30px;margin:0 0 28px 0
Body section: background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));border-radius:20px;padding:30px;margin:0 0 28px 0
PAA:          background:linear-gradient(rgba(241,243,250,0.5),rgba(241,243,250,0.5));border-radius:20px;padding:30px;margin:0 0 28px 0
Conclusion:   background:#00d5c0;border-radius:20px;padding:30px;margin:0 0 28px 0
```

FAQ items are `<details class="vfaq">` elements — no outer div wrapper needed.
