---
title: Thrive TOC Arrow Spec — Reference post 41576
client: virtina
date: 2026-05-05
source: ref41576_full_page.html (scraped rendered Thrive HTML)
---

# Arrow

**Type:** Inline SVG element — NOT Unicode, NOT CSS pseudo-element.

**Full SVG markup (from Thrive rendered HTML):**
```html
<svg class="tcb-icon" viewBox="0 0 24 24" data-id="icon-arrow-right-solid" data-name="">
  <path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"></path>
</svg>
```

**Arrow color:** Thrive applies color via JavaScript at page load using CSS variable
`--tcb-local-color-icon: rgb(67, 98, 127)` on the icon wrapper div.
The static HTML has `style=""` (empty) on the wrapper — fill is JS-applied.
User-confirmed rendered appearance: teal, matching brand CTA button (#00a0e2).
**Use `#00a0e2` for all inline-style reproductions.**

**Rendered Thrive wrapper around arrow (full):**
```html
<div class="tcb-styled-list-icon">
  <div class="thrv_wrapper thrv_icon tve_no_drag tcb-no-delete tcb-no-clone tcb-no-save tcb-icon-inherit-style tcb-local-vars-root tcb-icon-display" data-css="tve-u-19a78073f6e" style="">
    <svg class="tcb-icon" viewBox="0 0 24 24" data-id="icon-arrow-right-solid" data-name="">
      <path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"></path>
    </svg>
  </div>
</div>
```

# TOC link text

| Property | Value | Source |
|---|---|---|
| font-family | `metropolis, arial` | `body { font-family: metropolis, arial }` |
| font-size | `16px` | `[data-css=tve-u-19a78073fba] { font-size:16px!important }` |
| font-weight | `500` | applied via inline or Thrive override |
| color | `#00a0e2` | global `a { color: #00a0e2 }` |
| line-height | `2.3em` | `.tcb-styled-list-icon-text { line-height:2.3em }` |
| text-decoration | none | via `style="outline: none;"` on `<a>` + browser default |

# Why bullets appear instead of arrows

The Thrive CSS `.thrv-styled_list ul.tcb-styled-list { list-style:none }` only fires when
the `<ul>` has class `tcb-styled-list`. Our plain `<ul>` from content.raw has no class,
so the browser renders default disc bullets. Thrive adds the class and arrows via JavaScript
on page load (requires Thrive activation). Without activation, bullets show.

# Fix: inline-styled TOC

For posts not yet activated in Thrive, use this inline-styled structure to reproduce
the Thrive TOC appearance independent of Thrive's JS/CSS:

```html
<h3>Table of Contents</h3>
<ul style="list-style:none!important;padding-left:0!important;margin:0 0 1.5em 0!important;">
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;">
<span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#00a0e2;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span>
<a href="#anchor-id" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">Section title</a>
</li>
</ul>
```

Note: When Thrive Architect is activated on the post, it will re-render the TOC using its
own styled-list component, replacing this inline version. The inline version is for
pre-activation preview accuracy only.
