# TOC Analysis — Reference Post 41576

## What renders it

**Thrive Architect widget** — specifically `thrv_wrapper thrv-styled_list` with `data-icon-code="icon-arrow-right-solid"`. The TOC sits inside a `thrv_contentbox_shortcode` (a Thrive content box).

## Raw Thrive HTML (from rendered page)

```html
<div class="thrv_wrapper thrv_contentbox_shortcode thrv-content-box tve-elem-default-pad" data-css="tve-u-19a78073f6a" style="">
  <div class="tve-content-box-background" data-css="tve-u-19a78073f6b" style=""></div>
  <div class="tve-cb">
    <div class="thrv_wrapper thrv_text_element">
      <h3 class="">Table of Contents</h3>
    </div>
    <div class="thrv_wrapper thrv-styled_list" data-icon-code="icon-arrow-right-solid" data-css="tve-u-19a78073f6c" style="">
      <ul class="tcb-styled-list">
        <li class="thrv-styled-list-item" data-css="tve-u-19a78073f6d" style="">
          <div class="tcb-styled-list-icon">
            <div class="thrv_wrapper thrv_icon ... tcb-local-vars-root tcb-icon-display" data-css="tve-u-19a78073f6e" style="">
              <svg class="tcb-icon" viewBox="0 0 24 24" data-id="icon-arrow-right-solid" data-name="">
                <path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"></path>
              </svg>
            </div>
          </div>
          <span class="thrv-advanced-inline-text ... tcb-styled-list-icon-text" data-css="tve-u-19a78073fba" style="">
            <a href="#section-anchor" class="tve-jump-scroll" style="outline: none;">Section Title</a>
          </span>
        </li>
        <!-- repeated for each section -->
      </ul>
    </div>
  </div>
</div>
```

## Key CSS from Thrive (tve-u-* selectors confirmed from Thrive stylesheet)

| Selector | Property | Value |
|---|---|---|
| `tve-u-19a78073f6e` (icon div) | `--tve-icon-size` | `18px` |
| `tve-u-19a78073f6e` | `fill` | `#43627f` |
| `tve-u-19a78073fba` (link span) | `color` | `#43627f` |
| `tve-u-19a78073fba` | `font-size` | `16px` |
| `tve-u-19a78073fba` | `line-height` | `2.3` |
| `tve-u-19a78073fba` | `font-weight` | `500` |
| `tve-u-19a78073f6c` (list wrapper) | `list-style` | `none` |
| `tve-u-19a78073f6c` | `padding` | `0` |
| `tve-u-19a78073f6c` | `margin` | `8px 0 16px 0` |
| `tve-u-19a78073f6d` (list item) | `display` | `flex` |
| `tve-u-19a78073f6d` | `align-items` | `flex-start` |
| `tve-u-19a78073f6d` | `gap` | `10px` |
| `tve-u-19a78073f6d` | `padding` | `4px 0` |
| `h3` in content box | `color` | `#43627f` |
| `h3` in content box | `font-size` | `23px` |

## REST API constraint

`wp_kses_post` strips all Thrive wrapper divs (`thrv_*`, `tcb-*`, `tve_*`) on save. The Thrive widget above **cannot** be submitted via REST API. Only the inline-SVG equivalent survives the filter.

This WordPress install has `wp:action-unfiltered-html` — meaning `<svg>` elements ARE preserved. Verified: the FAQ `<svg>` in post 42074 survived the PUT.

## Inline-SVG equivalent (what we submit via REST API)

```html
<h3 style="color:#43627f;font-size:23px;">Table of Contents</h3>
<ul style="list-style:none;padding:0;margin:8px 0 16px 0;">
<li style="display:flex;align-items:flex-start;gap:10px;padding:4px 0;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;flex-shrink:0;margin-top:4px;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg><a href="#section-anchor" style="color:#43627f;text-decoration:none;font-size:16px;line-height:2.3;font-weight:500;">Section Title</a></li>
<!-- repeat per section -->
<li style="display:flex;align-items:flex-start;gap:10px;padding:4px 0;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;flex-shrink:0;margin-top:4px;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg><a href="#conclusion" style="color:#43627f;text-decoration:none;font-size:16px;line-height:2.3;font-weight:500;">Conclusion</a></li>
<li style="display:flex;align-items:flex-start;gap:10px;padding:4px 0;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;flex-shrink:0;margin-top:4px;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg><a href="#faq" style="color:#43627f;text-decoration:none;font-size:16px;line-height:2.3;font-weight:500;">FAQ</a></li>
</ul>
```

When Thrive Architect is activated (manual step), it reads the saved plain HTML and rebuilds its visual layer — so this plain HTML correctly seeds the visual TOC.
