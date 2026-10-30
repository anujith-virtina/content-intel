# Social — ChatSKU (LinkedIn + Instagram)

Every ChatSKU blog post becomes one **social pack**: a LinkedIn caption, an Instagram caption, and a
square image (a single poster, or a poster plus carousel slides). The copywriter writes a JSON pack.
`social/social_pipeline.py` renders the images, gates the copy, and posts it.

The format copies ChatSKU's existing feed (reference: instagram.com/chatsku, posts "Your buyer may not
call it what your catalog does" and "Can you kit this for us?", Oct 2026). Match it.

## Source of truth

Write only from `clients/chatsku/output/social/_source/{wp_post_id}.json` (the fetched article).

- Every figure, percentage, and dollar amount must appear in the article. QA rejects any that do not.
- Never add a claim, example, customer name, or statistic the article does not contain.
- Do not quote more than 15 consecutive words from the article. Rephrase.

## Caption (same structure on both platforms)

ChatSKU's feed is written **in the first person, as ChatSKU the AI catalog assistant** ("I help...",
"I believe...", "when I surface..."). Short, calm, no emoji. House pattern:

```
{Hook: one line. A buyer quote in "double quotes", or a blunt observation about the buyer.}

{One or two sentences on the buyer's situation.}

{One or two sentences on what I (ChatSKU) do about it, first person.}

{A closing question to the reader about their own buyers.}

Read the full article:
{canonical_url}
```

- No emoji at all. No em dashes, no exclamation marks, no semicolons.
- 60 to 130 words before the link line. Sentences of 20 words or fewer.
- ChatSKU itself is always an "AI catalog assistant", never a "chatbot". The word "chatbot" is allowed only for the generic product category the article discusses (e.g. "WooCommerce B2B chatbot").
- Never "AI-powered", never "solutions", never "replaces your sales team", never "schedule a demo".
- Never name a competitor (Drift, Intercom, Tidio, LiveChat, Zendesk).
- Vocabulary: catalog, buyer, quote, answers, after-hours.

LinkedIn: 300 to 1,500 characters including hashtags, first line 210 or fewer.
Instagram: first line 125 or fewer.
Hashtags: 3 to 5, CamelCase, in the `hashtags` array, not typed into the caption. The house set is
`Manufacturing`, `Distribution`, `B2BeCommerce`. Keep those three and add at most two topical ones.
The two captions may be near-identical. Vary the hook line.

## Images (1080 x 1080)

**Every post must look different from the one before it.** The user deleted a post (2026-10-14) because it
reused the previous post's poster-plus-numbered-points template. ChatSKU's real feed is visual storytelling:
product screens, a buyer's search failing, a catalog under a magnifying glass. So:

- Build the carousel as a short story from the article's own concrete example (a real buyer question,
  a real price pair, a real failure). Show it, do not list it.
- Prefer the story slide types (`chat`, `split`, `form`, `statement`) over `poster` + `point`. Mix at
  least three types per carousel.
- Never repeat the previous ChatSKU pack's cover type or slide sequence. Open the latest pack in
  `clients/chatsku/output/social/` and pick something else.
- Text on images is plain text: no emoji, no URL.

**Story slide types** (first slide may be any type except `point`; every slide needs a unique `alt`):

| Type | Fields |
|---|---|
| `chat` | `headline` (44), `accent` (30, amber line), `screen` (window title, 30), `messages`: list of `{who: buyer \| general \| catalog, text (120), tag (26, optional verdict under the bubble)}`, `typing` (true shows both assistants typing; good for a cover) |
| `split` | `headline`, `accent`, `left` / `right`: `{title (24), big (8, e.g. a price), text (120)}`, `footer` (110) |
| `form` | `headline`, `accent`, `title` (24), `fields`: list of `{label, value (40)}`, `button` (28), `note` (40) |
| `statement` | `kicker` (30), `line1` (32, white), `line2` (32, amber), `sub` (58) |
| `search` | `headline`, `accent`, `query` (40), `results`: list of `{site (30), title (60), snippet (110), tag (26), good}` |
| `phone` | `headline`, `accent`, `screen`, `rows`: list of `{kind: wallet \| divider \| field \| info \| total \| button, label, value}`, `notes`: list of `{text (40), good}` beside the phone |

Reference pack: `chatgpt-vs-catalog-chatbot-2026-10-14.json`. The older `poster` / `point` types below
are still valid when they really fit, but not twice in a row.

**`poster`**

| Field | What it is | Limit |
|---|---|---|
| `headline_top` | white line; sets up the tension | 34 chars |
| `headline_main` | amber line; the punch | 26 chars |
| `sub` | one muted line under the headline | 58 chars |
| `cards` | 3 to 5 outlined chips, the article's key points in order | |
| `cards[].label` | chip title | 20 chars |
| `cards[].detail` | chip subtitle | 34 chars |
| `alt` | describes the image | 20 to 120 chars |

**`point`** (carousel only)

| Field | Limit |
|---|---|
| `headline` | 44 chars |
| `body` | 170 chars |
| `alt` | 20 to 120 chars, unique per slide |

- Sentence case on images, matching the feed ("Real requests aren't always tidy.").
- If the renderer reports "text does not fit", shorten the text. Never ask for a smaller font.

## Pack file

Save to `clients/chatsku/output/social/{slug}-{YYYY-MM-DD}.json`.

```json
{
  "client": "chatsku",
  "slug": "...",
  "date": "YYYY-MM-DD",
  "wp_post_id": 0,
  "canonical_url": "https://chatsku.com/.../",
  "title": "...",
  "approved": false,
  "linkedin": {"post": "...", "hashtags": ["Manufacturing", "Distribution", "B2BeCommerce"]},
  "instagram": {"caption": "...", "hashtags": ["Manufacturing", "Distribution", "B2BeCommerce"]},
  "slides": [
    {"type": "poster", "headline_top": "...", "headline_main": "...", "sub": "...",
     "cards": [{"label": "...", "detail": "..."}], "alt": "..."},
    {"type": "point", "headline": "...", "body": "...", "alt": "..."}
  ]
}
```

`slug`, `wp_post_id`, `canonical_url`, and `title` are copied exactly from the source file.
Never write a `state` key, the pipeline owns it.

## Publishing rules

- A pack is only posted once its article is live. While the WordPress post is a draft the pack is held.
- `auto_approve` is `true`: once the article is live and QA passes, the pack is posted with no approval step.
- Each channel is posted at most once per pack. The result is recorded in the pack's `state`.
