# Virtina blog design system

Extracted from the reference post the client pointed to on 2026-09-08:
**https://virtina.com/gated-catalog-ai-visibility/** (post 42491). That post is the
correct house style. **Do not edit it.** A copy of its markup is saved as
`clients/virtina/output/research/_REFERENCE-42491-tve.html`.

## The thing I got wrong

Virtina's blog body is **NOT** built from Thrive content-box widgets. The entire
article is **one Thrive WP-shortcode wrapper containing raw HTML**, and the visual
design comes from **inline styles on plain `<div>` boxes**, not from Thrive
`data-css` tokens.

Wrapper the body lives inside:

```html
<div class="thrv_wrapper tve_wp_shortcode">
  <div class="tve_shortcode_raw" style="display: none">___TVE_SHORTCODE_RAW__ …HTML-escaped article… </div>
  …rendered copy…
</div>
```

Building sections as `thrv_contentbox_shortcode` widgets, as I did on posts 37791
and 38972, produces a completely different look: wrong spacing, no coloured box,
headings that fall back to defaults. That is what "you made it worse" meant.

## The box system

Every section is a rounded, tinted box. Same geometry throughout:

```
border-radius: 20px;  padding: 30px;  margin: 0 0 28px 0;
```

| Box | Background | Heading | Body text |
|---|---|---|---|
| **Summary** | `linear-gradient(rgba(0,213,192,0.28),rgba(0,213,192,0.28))` | `color:#43627f; font-size:30px` | `font-size:16px; line-height:1.75` |
| **Body section** (most common, 6 uses) | `linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13))` | `color:#43627f; font-size:30px` | `font-size:16px; line-height:1.75` |
| **Neutral / alternate** (2 uses) | `linear-gradient(rgba(241,243,250,0.5),rgba(241,243,250,0.5))` | `color:#43627f; font-size:30px` | `font-size:16px; line-height:1.75` |
| **Conclusion** | solid `#00d5c0` | `color:#ffffff; font-size:30px` | `color:#ffffff; font-size:16px; line-height:1.75` |

### Summary box, exact

```html
<div style="background: linear-gradient(rgba(0,213,192,0.28),rgba(0,213,192,0.28)); border-radius: 20px; padding: 30px; margin: 0 0 28px 0;">
<h2 dir="ltr" style="color: #43627f; font-size: 30px;">Summary</h2>
<p dir="ltr" style="font-size: 16px; line-height: 1.75;">…</p>
</div>
```

### Body section, exact

```html
<div style="background: linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13)); border-radius: 20px; padding: 30px; margin: 0 0 28px 0;">
<h2 id="section-anchor" style="color: #43627f; font-size: 30px;">Heading as a question?</h2>
<p dir="ltr" style="font-size: 16px; line-height: 1.75;">…</p>
</div>
```

### Conclusion box, exact

```html
<div style="background: #00d5c0; border-radius: 20px; padding: 30px; margin: 0 0 28px 0;">
<h2 id="conclusion" style="color: #ffffff; font-size: 30px;">Conclusion</h2>
<p style="color: #ffffff; font-size: 16px; line-height: 1.75;">…</p>
</div>
```

### Table of contents, exact

```html
<h3>Table of Contents</h3>
<ul style="list-style: none!important; padding-left: 0!important; margin: 0 0 1.5em 0!important;">
<li style="list-style: none!important; padding: 8px 0 8px 32px!important; position: relative!important; line-height: 1.5!important; margin: 0!important;">
<a style="color: #00a0e2!important; text-decoration: none!important; font-family: metropolis,arial!important; font-size: 16px!important; font-weight: 500!important;" href="#section-anchor">Section title</a>
</li>
</ul>
```

## Type and colour

- Font family throughout: **metropolis**, fallback arial
- H2: **30px**, `#43627f` (slate blue), weight 700. White `#ffffff` inside the Conclusion box.
- Body: **16px**, `line-height: 1.75`, `#2b3d4f`
- Internal links: `#00a0e2`, and Virtina's rules add `style="outline: none;"` with no `target`
- Section anchors sit as `id` on the `<h2>`, and the TOC links to them

## Rules for editing

1. **Match this box system.** Never introduce Thrive content-box widgets into a blog body.
2. **Keep the geometry identical** across boxes: 20px radius, 30px padding, 28px bottom margin.
3. **Body sections alternate** between the blue tint and the neutral tint; the Summary is teal-tinted and the Conclusion is solid teal.
4. Write the article as raw HTML inside the existing shortcode wrapper. Do not add new Thrive elements around it.
5. Verify by loading the live URL and comparing a new box against an existing one, not by checking markup validity. See [[feedback_thrive_render_check]].
