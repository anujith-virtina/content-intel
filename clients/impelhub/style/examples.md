# Examples — ImpelHub

## Reference post (structural gold standard)
Post ID 12356 — "The Rise of Fractional Leadership: When B2B Startups Should Hire Fractional CTO, CMO or CFO"
Full HTML: `clients/impelhub/reference/post-12356-working.html`
Live URL: https://impelhub.com/blog/fractional-leadership-b2b-startups-cto-cmo-cfo/

Pattern-match this post's:
- TL;DR block at top with colored arrows (→ in #5736fd)
- Table of Contents with anchor links, same arrow style
- H2 section structure with id attributes for TOC anchor targeting
- H3 subheadings inside H2 sections
- Elementor image widgets after heavy content sections
- "Related Reading" callout box with background
- Conclusion section
- FAQ accordion (Elementor accordion widget)

## All existing posts
Full inventory at: `clients/impelhub/reference/published-posts-inventory.md`
50 posts published between September 2024 and April 2026. Grouped by topic cluster for uniqueness checking.

## Signature ImpelHub opening hooks
- "Most B2B founders confuse [X] with [Y]. They [common mistake]. The two solve different problems."
- "Force without control rarely finishes the job."
- "Stop chasing [low-impact thing]. Start [high-leverage thing]."
- "When AI levels the playing field, [unique angle] becomes the edge."

## Signature ImpelHub close patterns
- "If you're a Guardian of Growth, your job is to filter out the noise. Here's the one move worth making this quarter: [specific action]"
- "Stop debating. Ship the plan."
- "Your move."

## TL;DR block pattern (from reference post)
```html
<h2 class="elementor-heading-title elementor-size-default">TL;DR: Key Takeaways</h2>
...
<p><span style="color:#5736fd;">→</span> [Takeaway 1]</p>
<p><span style="color:#5736fd;">→</span> [Takeaway 2]</p>
```

## TOC pattern (from reference post)
```html
<h3 class="elementor-heading-title elementor-size-default">Table of Contents</h3>
...
<p><span style="color:#5736fd;">→</span> <a href="#anchor" style="color:#5736fd;text-decoration:none;">Section Title</a></p>
```

## Internal link style (from reference post)
```html
<a href="https://impelhub.com/blog/..." style="color:#5736fd;font-weight:500;">anchor text</a>
```

## FAQ pattern
Elementor accordion widget. Each FAQ item is an accordion tab with question as title and answer as content.
