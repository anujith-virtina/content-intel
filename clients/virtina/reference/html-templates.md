---
title: Virtina HTML Templates
source: Extracted from post 42108 (verified working reference, May 2026)
last_updated: 2026-05-08
---

# Virtina HTML Templates

Every template below was extracted from post ID 42108 — the verified working reference. **Copy exactly. Never improvise structure or inline styles.**

Replace `{{PLACEHOLDER}}` tokens with actual content. Do not change any tag names, class names, style attributes, or structural nesting.

---

## Template A — Summary block

```html
<div style="background:linear-gradient(rgba(0,213,192,0.28),rgba(0,213,192,0.28));border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 dir="ltr" style="color:#43627f;font-size:30px;">Summary</h2>
<p dir="ltr" style="font-size:16px;line-height:1.75;">{{SUMMARY_TEXT}}</p>
</div>
```

---

## Template B — Introduction block

```html
<div style="background:linear-gradient(rgba(241,243,250,0.5),rgba(241,243,250,0.5));border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 style="color:#43627f;font-size:30px;">Introduction</h2>
<p dir="ltr" style="font-size:16px;line-height:1.75;">{{INTRO_PARAGRAPH_1}}</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">{{INTRO_PARAGRAPH_2}}</p>
</div>
```

---

## Template C — Table of Contents

The `<h3>` and `<ul>` must NOT be inside a section `<div>` wrapper — place them directly after the Introduction div.

```html
<h3>Table of Contents</h3>
<ul style="list-style:none!important;padding-left:0!important;margin:0 0 1.5em 0!important;">
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#{{ANCHOR_ID}}" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">{{ITEM_TEXT}}</a></li>
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#{{ANCHOR_ID}}" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">{{ITEM_TEXT}}</a></li>
</ul>
```

Rules:
- Add one `<li>` per body H2. Always include entries for `#people-also-ask`, `#conclusion`, `#faq`.
- `!important` with NO SPACE before — `list-style:none!important` not `list-style:none !important`
- SVG path is the right-arrow icon. Never replace with Unicode `→` or any other char.

---

## Template D — Body H2 section (with wrapper div)

```html
<div style="background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 id="{{ANCHOR_ID}}" style="color:#43627f;font-size:30px;">{{HEADING}}</h2>
<p dir="ltr" style="font-size:16px;line-height:1.75;">{{PARAGRAPH_TEXT}}</p>
</div>
```

For sections with sub-headings (H3):
```html
<div style="background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 id="{{ANCHOR_ID}}" style="color:#43627f;font-size:30px;">{{HEADING}}</h2>
<p dir="ltr" style="font-size:16px;line-height:1.75;">{{PARAGRAPH_TEXT}}</p>
<h3><span style="font-weight: normal;"><span>{{SUBHEADING}}</span></span></h3>
<p dir="ltr" style="font-size:16px;line-height:1.75;">{{PARAGRAPH_TEXT}}</p>
</div>
```

H3 pattern (verified from agentic-ai-in-ecommerce-ai-agents, May 2026 — newer standard):
- `<h3><span style="font-weight: normal;"><span>TEXT</span></span></h3>`
- NO inline styles on the `<h3>` tag itself
- The theme CSS handles color and size
- This replaces the older `<h3 style="color:#43627f;font-size:23px;">` pattern from post 42108

---

## Template E — Body paragraph (standalone, outside section div)

```html
<p dir="ltr" style="font-size:16px;line-height:1.75;">{{PARAGRAPH_TEXT}}</p>
```

---

## Template F — Body bullet list

Place inside the section `<div>`. Use for ALL body bullet lists. Never use default `<ul><li>` without this pattern.

```html
<ul style="list-style:none;padding-left:4px;margin:8px 0 16px 0;">
<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>{{BOLD_LABEL}}.</strong> {{ITEM_TEXT}}</span></li>
<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>{{BOLD_LABEL}}.</strong> {{ITEM_TEXT}}</span></li>
</ul>
```

Critical values (read from brand-teal.txt and body-font-size.txt before use):
- Circle `background-color`: `#43627f` (Virtina slate — NOT `#00d5c0`, NOT `#16afa0`)
- Text `font-size`: `16px` (must match body paragraph)
- Text `line-height`: `1.75`
- Text `color`: `#2d3e50`

Safe body-only regex (excludes TOC `<ul>` which has `!important`):
```python
body_ul_re = re.compile(r'<ul\s+style="(?![^"]*!important)[^"]*"[^>]*>.*?</ul>', re.DOTALL)
```

---

## Template N — Comparison table

Use for any plugin/platform/option comparison. Requires full inline styles — no bare `<table>` tags.

```html
<table data-rows="{{ROW_COUNT}}" data-cols="{{COL_COUNT}}" data-v="middle" style="width:100%;border-collapse:collapse;margin:16px 0;">
<thead>
<tr>
<th data-direction="" style="background:#43627f;color:#ffffff;padding:10px 14px;text-align:left;font-weight:600;"><p style="font-size:16px;line-height:1.75;"><strong>{{HEADER_1}}</strong></p></th>
<th data-direction="" style="background:#43627f;color:#ffffff;padding:10px 14px;text-align:left;font-weight:600;"><p style="font-size:16px;line-height:1.75;"><strong>{{HEADER_2}}</strong></p></th>
</tr>
</thead>
<tbody>
<tr>
<td data-th="{{HEADER_1}}" style="background:#f4f6f9;padding:10px 14px;border-bottom:1px solid #dde0e6;vertical-align:top;"><p style="font-size:16px;line-height:1.75;">{{CELL}}</p></td>
<td data-th="{{HEADER_2}}" style="background:#f4f6f9;padding:10px 14px;border-bottom:1px solid #dde0e6;vertical-align:top;"><p style="font-size:16px;line-height:1.75;">{{CELL}}</p></td>
</tr>
<tr>
<td data-th="{{HEADER_1}}" style="background:#ffffff;padding:10px 14px;border-bottom:1px solid #dde0e6;vertical-align:top;"><p style="font-size:16px;line-height:1.75;">{{CELL}}</p></td>
<td data-th="{{HEADER_2}}" style="background:#ffffff;padding:10px 14px;border-bottom:1px solid #dde0e6;vertical-align:top;"><p style="font-size:16px;line-height:1.75;">{{CELL}}</p></td>
</tr>
</tbody>
</table>
<p dir="ltr" style="font-size:14px;line-height:1.6;color:#6e6e6e;margin:4px 0 16px 0;">{{TABLE_CAPTION}}</p>
```

Rules:
- `<th>` always: `background:#43627f;color:#ffffff;padding:10px 14px;text-align:left;font-weight:600;`
- Odd data rows: `background:#f4f6f9;padding:10px 14px;border-bottom:1px solid #dde0e6;vertical-align:top;`
- Even data rows: `background:#ffffff;padding:10px 14px;border-bottom:1px solid #dde0e6;vertical-align:top;`
- All cell content wrapped in `<p style="font-size:16px;line-height:1.75;">` tags
- Add `data-th="{{HEADER_NAME}}"` on every `<td>` matching its column header
- Always follow the table with a caption `<p>` in 14px grey (`color:#6e6e6e`) noting the data date
- Source: verified from post 42108 API response (May 2026)

---

## Template G — Body image block

```html
<span style="display:block;margin:20px 0;"><img alt="{{ALT_TEXT}}" data-id="{{MEDIA_ID}}" width="670" data-init-width="670" height="352" data-init-height="352" title="" loading="lazy" src="{{IMAGE_URL}}" data-width="670" data-height="352" style="aspect-ratio: auto 670 / 352;max-width:100%;"></span>
```

Rules:
- `{{ALT_TEXT}}`: 80–150 chars, descriptive, includes 1–2 article keywords
- `{{MEDIA_ID}}`: the WordPress media ID returned by POST /wp/v2/media
- `{{IMAGE_URL}}`: must begin with `https://virtina.com/wp-content/uploads/`
- Place between sections, never between intro and TOC

---

## Template H — People Also Ask block

```html
<div style="background:linear-gradient(rgba(241,243,250,0.5),rgba(241,243,250,0.5));border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 id="people-also-ask" style="color:#43627f;font-size:30px;">People also ask</h2>
<h3><span style="font-weight: normal;"><span>{{PAA_QUESTION_1}}</span></span></h3>
<p dir="ltr" style="font-size:16px;line-height:1.75;">{{PAA_ANSWER_1}}</p>
<h3><span style="font-weight: normal;"><span>{{PAA_QUESTION_2}}</span></span></h3>
<p dir="ltr" style="font-size:16px;line-height:1.75;">{{PAA_ANSWER_2}}</p>
<h3><span style="font-weight: normal;"><span>{{PAA_QUESTION_3}}</span></span></h3>
<p dir="ltr" style="font-size:16px;line-height:1.75;">{{PAA_ANSWER_3}}</p>
</div>
```

Include 3–4 questions. Each answer 2–4 sentences. Questions should match real search queries.

---

## Template I — Conclusion block

```html
<div style="background:#00d5c0;border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 id="conclusion" style="color:#ffffff;font-size:30px;">Conclusion</h2>
<p style="color:#ffffff;font-size:16px;line-height:1.75;">{{CONCLUSION_PARAGRAPH_1}}</p>
<p style="color:#ffffff;font-size:16px;line-height:1.75;">{{CONCLUSION_PARAGRAPH_2}}</p>
</div>
```

Note: Conclusion box has white text on solid `#00d5c0` teal background — all `<p>` must have `color:#ffffff`.

---

## Template J — FAQ accordion item

The FAQ section uses `<details>` elements. Wrap all items in a containing `<div>`:

```html
<h2 id="faq" style="color:#43627f;font-size:30px;">Frequently Asked Questions</h2>
<div>
<details class="vfaq" style="background:transparent;margin-top:7px;"><summary style="cursor:pointer;padding:17px;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:12px;background:rgba(245,245,245,0.5);"><span style="font-size:16px;font-weight:600;color:#43627f;line-height:2;flex:1;">{{FAQ_QUESTION}}</span><svg viewBox="0 0 24 24" width="17" height="17" style="fill:#50565f;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg"><path d="M16,12A2,2 0 0,1 18,10A2,2 0 0,1 20,12A2,2 0 0,1 18,14A2,2 0 0,1 16,12M8,12A2,2 0 0,1 10,10A2,2 0 0,1 12,12A2,2 0 0,1 10,14A2,2 0 0,1 8,12M0,12A2,2 0 0,1 2,10A2,2 0 0,1 4,12A2,2 0 0,1 2,14A2,2 0 0,1 0,12Z"/></svg></summary><div class="vfaq-answer" style="padding:30px 22px;background:#fff;"><p dir="ltr" style="font-size:16px;line-height:1.75;">{{FAQ_ANSWER}}</p></div></details>
</div>
```

Repeat `<details>...</details>` for each Q&A (6–8 total). Use `margin-top:7px` on each.

---

## Template K — Author bio block

```html
<p dir="ltr" style="font-size:16px;line-height:1.75;"><strong>{{AUTHOR_NAME}}</strong> {{AUTHOR_BIO}}</p>
```

---

## Template L — Internal link (virtina.com)

```html
<a href="{{VIRTINA_URL}}" style="outline: none;">{{LINK_TEXT}}</a>
```

No `target` attribute. No `rel` attribute. Opens in same tab.

Examples of valid internal URLs:
- `https://virtina.com/platforms/woocommerce-development-services/`
- `https://virtina.com/ecommerce-integration/`
- `https://virtina.com/b2b-ecommerce-development/`

---

## Template M — External link

```html
<a href="{{EXTERNAL_URL}}" target="_blank" rel="noopener noreferrer">{{LINK_TEXT}}</a>
```

Max 2 external links per article. Never link to competitor domains (shopify.com, bigcommerce.com, etc.).
