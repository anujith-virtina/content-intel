# CMS — ImpelHub

## Platform
WordPress + Elementor (confirmed via class inspection of live posts: .elementor-element, .elementor-widget, .elementor-section, .elementor-container, .elementor-widget-text-editor, .elementor-heading-title)

Hosting: WP Rocket detected (cache may delay preview — allow 30 seconds)
REST API base: https://impelhub.com/wp-json/wp/v2

## Authentication
Basic Auth with WordPress Application Password.
Required env vars (separate from Virtina and ChatSKU):
- IMPELHUB_WP_USERNAME
- IMPELHUB_WP_APP_PASSWORD

DO NOT reuse Virtina or ChatSKU credentials.

## Publishing rules
- Status always: 'draft' (never auto-publish)
- Format: standard Elementor container/widget HTML structure
- Featured image: featured_media field with real uploaded media ID, never 0
- Yoast SEO meta fields populated where REST allows
- WP Rocket cache may delay preview; allow 30 seconds before fetching preview URL

## Elementor HTML pattern (from reference post 12356)
ImpelHub posts use Elementor containers with this structure:

```html
<div data-elementor-type="wp-post" data-elementor-id="{id}" class="elementor elementor-{id}" data-elementor-post-type="post">
  <div class="elementor-element elementor-element-{id} e-con-full e-flex e-con e-parent" data-element_type="container">
    <!-- heading widget -->
    <div class="elementor-element elementor-widget elementor-widget-heading" data-widget_type="heading.default">
      <h2 class="elementor-heading-title elementor-size-default">Section Heading</h2>
    </div>
    <!-- text widget -->
    <div class="elementor-element elementor-widget elementor-widget-text-editor" data-widget_type="text-editor.default">
      <p>Body text here.</p>
    </div>
  </div>
</div>
```

## ImpelHub arrow style (confirmed from live posts)
- Arrows: Unicode → wrapped in `<span style="color:#5736fd;">→</span>`
- Links: `style="color:#5736fd;"` and optionally `style="color:#5736fd;font-weight:500;"`
- TOC links: `style="color:#5736fd;text-decoration:none;"`

## ImpelHub brand colors
- Primary accent: #5736fd (purple/violet) — confirmed from inline styles in reference post 12356
- Secondary: not confirmed from CSS; verify via browser dev tools on live site

## Image sourcing
Pexels API primary (PEXELS_API_KEY env var, shared across clients).

Topic keyword library for ImpelHub:
- Founder/CEO scenes: 'founder laptop strategy', 'CEO desk decision', 'startup founder office'
- Growth/strategy: 'business strategy whiteboard', 'growth dashboard analytics', 'business meeting decision'
- Data/AI: 'AI business intelligence', 'business analytics dashboard', 'data driven business'
- Team/execution: 'startup team execution', 'business team planning', 'growth team meeting'
- Competition: 'competitive analysis business', 'market research desk', 'business intelligence screens'

## CTA conventions
End every ImpelHub blog with one of:
- "Pinpoint your #1 growth lever" → https://impelhub.com/find-out-where-your-business-should-focus-next-for-growth-in-just-3-minutes/
- "Get your custom playbook in 10 days" → https://impelhub.com/contact/
- "See how ImpelHub filters decisions" → https://impelhub.com/how-impelhub-works/
- "Read the ImpelHub Startup Playbook" → https://impelhub.com/wp-content/uploads/2025/05/impelhub-startup-growth-strategies-playbook.pdf
