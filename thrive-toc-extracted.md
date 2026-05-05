---
title: Thrive TOC — Extracted Structure and Colors
client: virtina
date: 2026-05-05
source: reference post 41576 (launching-fast-without-strategy-ecommerce-costs)
---

# Thrive TOC — Findings

## No shortcode found

The reference post `content.raw` contains PLAIN HTML for the TOC — no `[thrv_post_toc]`, `[thrive_table_of_contents]`, or other shortcode. Thrive Architect reads the plain HTML and overlays its visual layer on activation.

## Reference content.raw TOC format (exact)

```html
<h3>Table of Contents</h3>
<ul>
<li style=""><span style=""><a href="#section-anchor" style="outline: none;">Section Title</a></span></li>
<li><span><a href="#another-anchor" style="outline: none;">Another Section</a></span></li>
</ul>
```

Rules:
- Plain `<h3>` — NO inline style attribute
- `<ul>` — no style attribute
- First `<li>`: `style=""` and first `<span>`: `style=""` (empty, as Thrive generates)
- Subsequent `<li>` and `<span>`: no style attribute
- Every `<a>`: `style="outline: none;"` only — NO color, NO font-size, NO other styles
- Links open in same tab (no target attribute)

## Colors (from page CSS, 2026-05-05)

| Element | Color | Source |
|---|---|---|
| TOC link text | `#00a0e2` | Global `a { color: #00a0e2 }` rule — Thrive inherits this |
| TOC arrow icons (fill) | `rgb(67, 98, 127)` = `#43627f` | `--tcb-local-color-icon` on `tve-u-19a78073f6e`; SVG uses `fill: currentcolor` |
| CTA button ("TALK TO EXPERTS") | `linear-gradient(45deg, #00a0e2 0, #00f0d8 100%)` | `.header-cta p.p1.rq a` CSS rule |
| Brand primary | `#00A0E2` | `--vms-primary` CSS variable |
| Brand accent (teal) | `#00F0D8` | `--vms-accent` CSS variable |

## Why our previous TOC was wrong

Our hand-crafted TOC used inline SVG arrows and `color:#43627f` on links. This:
1. Overrides Thrive's visual layer — Thrive can't cleanly activate over non-standard HTML
2. Makes links appear dark slate instead of the global link blue `#00a0e2`
3. Inline SVGs with arbitrary structure conflict with Thrive's icon rendering engine (`.tcb-icon { fill: currentcolor }`)

## Correct approach

Use the exact reference `content.raw` format. When Thrive is activated:
- Thrive wraps the `<ul>` in its styled-list component (`thrv-styled_list`, `tcb-styled-list`)
- Arrows are added by Thrive's icon component with `data-icon-code="icon-arrow-right-solid"`
- Link color comes from global `a { color: #00a0e2 }` CSS
- Icon color comes from Thrive's `--tcb-local-color-icon` variable

## Thrive CSS architecture (key rules)

```css
/* Icon SVG fill = parent color property */
.tcb-icon { fill: currentcolor; }
svg.tcb-icon path:not([fill=none]) { fill: inherit !important; }

/* Styled list base */
.thrv-styled_list ul.tcb-styled-list { list-style: none; margin: 0 !important; padding: 0 !important; }
.tcb-styled-list-icon-text { display: block; z-index: 0; line-height: 2.3em; }

/* Link color within Thrive content — inherits global */
.tcb-styled-list a:not(.tcb-button-link) { font-size: inherit; }
a { color: #00a0e2; }  /* global */
```
