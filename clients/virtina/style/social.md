# Social — Virtina (LinkedIn + Instagram)

Every Virtina blog post becomes one **social pack**: a LinkedIn post, an Instagram caption, and one
carousel that both platforms share. The copywriter writes a JSON pack. `social/social_pipeline.py`
renders the slides, gates the copy, and posts it. Limits below are enforced by the `qa` command, so a
pack that breaks them cannot be published.

## Source of truth

Write only from `clients/virtina/output/social/_source/{wp_post_id}.json` (the fetched article).

- Every figure, percentage, and dollar amount must appear in the article. QA rejects any that do not.
- Never add a claim, example, client name, or statistic the article does not contain.
- Do not quote more than 15 consecutive words from the article. Rephrase.

## Voice

Same voice as the blog (`voice.md`, `brand.md`), tightened for a feed:

- Second person, active voice, contractions fine. Sentences of 20 words or fewer.
- Open with a concrete situation or a specific claim from the article, never a question like "Did you know".
- One idea per paragraph, blank line between paragraphs.
- No em dashes, no exclamation marks, no semicolons, no emoji.
- No hype or filler words (full banned list in `clients/virtina/social.json`), no "vendor", no "reach out".
- Never promotional: no "our guide", "check out our", "read our". Say what the article covers.
- Never name a competitor agency.

## LinkedIn post

- 900 to 2,000 characters including hashtags. Aim for 1,200 to 1,800.
- First line is the hook and must be 210 characters or fewer (it is all that shows before "see more").
- No link and no domain name in the post body. The link goes in `first_comment`.
- End on a soft line that points to the first comment, for example "Full breakdown in the first comment."
- `first_comment`: one plain sentence plus the article URL.
- 3 to 5 hashtags, lowercase, letters and digits only.
- A short list of parallel items is fine. Use a hyphen and a space, never a bullet character.

## Instagram caption

- First line 125 characters or fewer (all that shows before "more").
- 3 to 6 short paragraphs. The carousel carries the detail, the caption frames it.
- No URL (captions are not clickable). Must include the words "link in bio".
- 5 to 10 hashtags, lowercase, letters and digits only. Mix broad (`ecommerce`, `b2becommerce`) and
  specific (`woocommerce`, `magento`, `checkoutoptimization`).

## Carousel slides (1080 x 1350, shared by both platforms)

5 to 9 slides: one `cover`, three to seven `point`, one `cta`.

| Type | Fields | Limits |
|---|---|---|
| `cover` | `kicker`, `headline`, `sub` (optional), `alt` | kicker 30 chars, headline 70, sub 110 |
| `point` | `number`, `headline`, `body`, `alt` | headline 60 chars, body 200 |
| `cta` | `headline`, `body`, `alt`, `label` (optional) | headline 60 chars, body 140 |

- Sentence case everywhere. The renderer uppercases the kicker itself.
- Each point slide must stand alone: someone who sees only that slide still learns one thing.
- Point `number` runs 1, 2, 3 in order.
- The `cta` slide states what the full article adds. It must work on both platforms, so do not write
  "link in bio" or "first comment" on a slide.
- `alt`: 20 to 120 characters, describes what the slide says, unique per slide.
- If the renderer reports "text does not fit", shorten the text. Never ask for a smaller font.

## Pack file

Save to `clients/virtina/output/social/{slug}-{YYYY-MM-DD}.json`.

```json
{
  "client": "virtina",
  "slug": "customer-payment-declined-guide",
  "date": "2026-10-06",
  "wp_post_id": 43089,
  "canonical_url": "https://virtina.com/customer-payment-declined-guide/",
  "title": "Why did my customer's payment get declined?",
  "approved": false,
  "linkedin": {
    "post": "Hook line.\n\nParagraph.\n\nFull breakdown in the first comment.",
    "hashtags": ["woocommerce", "ecommerce", "onlinepayments"],
    "first_comment": "The full guide: https://virtina.com/customer-payment-declined-guide/"
  },
  "instagram": {
    "caption": "Hook line.\n\nParagraph.\n\nLink in bio for the full guide.",
    "hashtags": ["woocommerce", "ecommerce", "onlinepayments", "smallbusiness", "checkout"]
  },
  "slides": [
    {"type": "cover", "kicker": "WooCommerce payments", "headline": "...", "sub": "...", "alt": "..."},
    {"type": "point", "number": 1, "headline": "...", "body": "...", "alt": "..."},
    {"type": "cta", "headline": "...", "body": "...", "alt": "..."}
  ]
}
```

`slug`, `wp_post_id`, `canonical_url`, and `title` are copied exactly from the source file.
Always write `"approved": false`. Never write a `state` key, the pipeline owns it.

## Publishing rules

- A pack is only posted once its article is live. While the WordPress post is a draft the pack is held.
- A pack is only posted once approved (`approve` command), unless `auto_approve` is `true` in `social.json`.
- Each channel is posted at most once per pack. The result is recorded in the pack's `state`.
- Instagram needs a public image URL, so slides are uploaded to the virtina.com media library at post time.
