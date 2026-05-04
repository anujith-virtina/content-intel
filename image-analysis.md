# Image Analysis — Reference Post 41576

## Featured / Hero Image

**Where it lives:** Theme-rendered — NOT inside `post_content`. Set via the `featured_media` field (WordPress attachment ID) in the REST API payload. The theme outputs it as `<div class="post-thumbnail">`.

**Rendered HTML:**
```html
<div class="post-thumbnail">
  <picture class="attachment-post-thumbnail size-post-thumbnail wp-post-image" decoding="async">
    <source type="image/webp" srcset="https://virtina.com/wp-content/uploads/2026/03/launching-ft.jpg.webp 1309w, .../launching-ft-300x115.jpg.webp 300w, .../launching-ft-1024x391.jpg.webp 1024w, .../launching-ft-768x293.jpg.webp 768w" sizes="(max-width: 1309px) 100vw, 1309px"/>
    <img data-no-lazy="" fetchpriority="high" width="1309" height="500"
         src="https://virtina.com/wp-content/uploads/2026/03/launching-ft.jpg"
         alt="Team launching an eCommerce site while unresolved checkout, payment, and integration issues appear on screen."
         decoding="async"
         srcset="https://virtina.com/wp-content/uploads/2026/03/launching-ft.jpg 1309w, .../launching-ft-300x115.jpg 300w, .../launching-ft-1024x391.jpg 1024w, .../launching-ft-768x293.jpg 768w"
         sizes="(max-width: 1309px) 100vw, 1309px"/>
  </picture>
</div>
```

**Key attributes:**
- `width="1309" height="500"` — always 1309×500
- `fetchpriority="high"` — hero gets high priority
- `data-no-lazy=""` — bypasses lazy load (hero image loads immediately)
- Set via REST API: `"featured_media": {attachment_id}`
- **Cannot use a placehold.co URL** — must be a real WordPress attachment ID

## Body / Section Images

**Where they live:** Inside `post_content`, wrapped in `<span>`. Thrive Architect renders them via `thrv_image` wrapper in the visual editor, but the inner `<span><img>` survives `wp_kses_post`.

**Rendered HTML (from reference):**
```html
<span>
  <img decoding="async"
       alt="Realistic eCommerce dashboard showing high traffic, low conversion..."
       data-id="41607"
       width="670"
       data-init-width="768"
       height="352"
       data-init-height="404"
       title=""
       loading="lazy"
       data-width="670"
       data-height="352"
       style="aspect-ratio: auto 768 / 404;"
       src="https://virtina.com/wp-content/uploads/2026/03/img1.jpg"
       data-lazy-srcset="https://virtina.com/wp-content/uploads/2026/03/img1.jpg 768w, .../img1-300x158.jpg 300w"
       data-lazy-sizes="auto, (max-width: 670px) 100vw, 670px"/>
</span>
```

**Key attributes:**
- `width="670" height="352"` — display dimensions
- `data-init-width="768" data-init-height="404"` — original upload dimensions (Thrive stores these)
- `data-width="670" data-height="352"` — Thrive display override
- `style="aspect-ratio: auto 768 / 404;"` — uses original upload ratio, not display ratio
- `loading="lazy"` — all body images are lazy-loaded
- Wrapped in `<span>` (not `<figure>`, not `<div>`)

## Simplified REST API version (what to submit)

For real images (with WordPress attachment ID):
```html
<span><img alt="{{ALT_TEXT}}" data-id="{{ATTACHMENT_ID}}" width="670" data-init-width="{{ORIG_W}}" height="352" data-init-height="{{ORIG_H}}" title="" loading="lazy" src="{{IMAGE_URL}}" data-width="670" data-height="352" style="aspect-ratio: auto {{ORIG_W}} / {{ORIG_H}};"></span>
```

For placeholder (layout preview only):
```html
<span><img alt="{{ALT_TEXT}}" width="670" height="352" loading="lazy" src="https://placehold.co/670x352" data-width="670" data-height="352" style="aspect-ratio: auto 670 / 352;"></span>
```

## Required dimensions (both articles)

| Usage | Width | Height | Set via |
|---|---|---|---|
| Featured/hero image | 1309 | 500 | `featured_media` attachment ID |
| Body section images | 670 | 352 | `<span><img>` in content |

## Important constraint

Featured image **cannot** be a placehold.co URL. It must be a real WordPress media library attachment ID. Body images can use placehold.co for layout validation, but real images need to be uploaded to WordPress first to get their attachment IDs.
