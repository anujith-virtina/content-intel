# CMS — ChatSKU

## Platform
WordPress + Elementor 4.0.3 (NOT Thrive Architect — fully REST-API compatible, standard Gutenberg blocks)
Hosting: WP Engine
REST API base: https://chatsku.com/wp-json/wp/v2

## Authentication
Basic Auth with WordPress Application Password.

Required env vars (separate from Virtina):
- `CHATSKU_WP_USERNAME`
- `CHATSKU_WP_APP_PASSWORD`

DO NOT use Virtina's WP credentials. These are different sites.

## Publishing rules
- Status always: `draft` (never auto-publish)
- Format: standard Gutenberg blocks — no Thrive markup, no Thrive shortcodes
- Featured image: `featured_media` field with real uploaded media ID, never 0
- No manual Elementor editor handoff needed for text content (Gutenberg block content renders in Elementor's single-post template directly)
- Yoast SEO meta fields populated via REST API where supported

## Image specifications
- **Featured image**: 860 × 452 px (verified from post 151 — existing standard)
- **Body images**: 860 × 452 px (same dimensions as featured)
- File format: JPEG, quality 82
- Max file size: 200 KB
- Upload via POST /wp-json/wp/v2/media (multipart)
- Set alt_text via POST /wp-json/wp/v2/media/{id}

## Image sourcing
API priority: Pexels API (PEXELS_API_KEY env var — shared with Virtina) > Openverse (source=stocksnap filter) > Wikimedia Commons.

Topic keyword library for ChatSKU:
- Featured: `B2B sales team office`, `manufacturer office buyer`, `distributor warehouse desk`
- Catalog/data: `product catalog spreadsheet`, `inventory SKU computer office`
- Sales/buyer: `sales team computer screens`, `B2B sales conversation meeting`
- Quote/pricing: `business quote document desk`, `price negotiation business`
- Workflow/operations: `sales workflow team office`, `B2B order processing computer`
- After-hours: `laptop desk night working late`, `office empty after hours`

NEVER use: source.unsplash.com (deprecated), placehold.co, Pillow text-on-color cards. Use Openverse with short stock-photo-style queries + source=stocksnap filter.

## HTML structure for blog posts
ChatSKU uses Elementor, so the post content structure is much simpler than Virtina's Thrive markup. Standard HTML is fine:

```html
<h2>Section heading</h2>
<p>Body paragraph text at 16px, line-height 1.6.</p>
<ul>
  <li>Bullet item</li>
</ul>
```

No `!important` overrides, no SVG arrows, no complex CSS inline styles. Elementor renders standard Gutenberg block HTML without modification.

## CTA conventions
End every ChatSKU blog with one of these call-to-action patterns:

```html
<p><a href="https://chatsku.com/signup/">Start a free trial</a> — no credit card, live in hours.</p>
```
or:
```html
<p><a href="https://chatsku.com/demo/">See the live demo</a> and watch it answer real B2B catalog questions.</p>
```

## Yoast SEO fields
Set via REST API meta fields:
- `yoast_wpseo_title`: `{Title} | ChatSKU` (60 chars max)
- `yoast_wpseo_metadesc`: 150–160 chars
- `yoast_wpseo_focuskw`: primary keyword
