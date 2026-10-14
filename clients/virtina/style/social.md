# Social — Virtina (LinkedIn + Instagram)

Every Virtina blog post becomes one **social pack**: a LinkedIn caption, an Instagram caption, and one
square poster image both platforms share. The copywriter writes a JSON pack.
`social/social_pipeline.py` renders the image, gates the copy, and posts it. Limits below are enforced by
the `qa` command, so a pack that breaks them cannot be published.

The format copies Virtina's existing feed (reference: instagram.com/virtinapro, post "Your Customers Are
Leaving. Do You Know Why?", Oct 2026). Match it. Do not invent a different format.

## Source of truth

Write only from `clients/virtina/output/social/_source/{wp_post_id}.json` (the fetched article).

- Every figure, percentage, and dollar amount must appear in the article. QA rejects any that do not.
- Never add a claim, example, client name, or statistic the article does not contain.
- Do not quote more than 15 consecutive words from the article. Rephrase.

## Caption (same structure on both platforms)

This is the house pattern. Keep the order and the emoji markers exactly:

```
🚨 {hook question or blunt statement, one line}

{one or two short sentences that set up the problem}

Here are {N} {things} {that ...}:

1️⃣ {Point name}
{One sentence, 20 words or fewer.}

2️⃣ {Point name}
{One sentence.}

... (3 to 5 points, matching the cards on the image)

💡 {The good news / the takeaway, one or two sentences}

👉 Read the full article {to learn / for ...}:
{canonical_url}
```

- Emoji: only 🚨, 1️⃣ to 5️⃣, 💡 and 👉, each used as shown. No other emoji.
- The article URL goes in the caption body, on its own line, on both platforms.
- No em dashes, no exclamation marks, no semicolons.
- Second person, active voice, contractions fine. Sentences of 20 words or fewer.
- No hype or filler words (full banned list in `clients/virtina/social.json`), no "vendor", no "reach out".
- Never promotional: no "our guide", "check out our", "read our". Never name a competitor agency.

LinkedIn: 600 to 2,200 characters including hashtags, first line 210 or fewer, 3 to 8 hashtags.
Instagram: 2,200 characters or fewer, first line 125 or fewer, 5 to 10 hashtags.
The two captions may be near-identical. Vary the hook line and the hashtag mix.
Hashtags: lowercase, letters and digits only, in the `hashtags` array, not typed into the caption.

## Images (1080 x 1080)

Slide 1 is always type `poster`. A carousel adds 2 to 6 `point` slides after it (`headline` 44 chars,
`body` 170 chars, `alt` unique per slide), one per numbered caption point. Use a single poster by default
and a carousel when each point needs a full sentence. Text on images is plain text: no emoji, no URL.

| Field | What it is | Limit |
|---|---|---|
| `headline_top` | white line above the main headline; sets up the tension | 34 chars |
| `headline_main` | big yellow line; the punch | 26 chars |
| `sub` | one white line under the headline, e.g. "5 checks to run before Black Friday" | 58 chars |
| `cards` | 3 to 5 callout cards, same points and order as the caption's numbered list | |
| `cards[].label` | card title | 20 chars |
| `cards[].detail` | card subtitle | 34 chars |
| `alt` | describes the image for screen readers | 20 to 120 chars |

- `headline_top` + `headline_main` read as one thought. Reference: "Your Customers Are Leaving." /
  "Do You Know Why?"
- Headlines are Title Case on the image (this is the one place Title Case is used). Cards are sentence case.
- If the renderer reports "text does not fit", shorten the text. Never ask for a smaller font.

## Pack file

Save to `clients/virtina/output/social/{slug}-{YYYY-MM-DD}.json`.

```json
{
  "client": "virtina",
  "slug": "ecommerce-ux-problems",
  "date": "2026-10-07",
  "wp_post_id": 43123,
  "canonical_url": "https://virtina.com/ecommerce-ux-problems/",
  "title": "Ecommerce UX Problems That Drive Customers Away",
  "approved": false,
  "linkedin": {
    "post": "🚨 Getting traffic but not enough sales?\n\n...\n\n👉 Read the full article to learn what could be hurting your store:\nhttps://virtina.com/ecommerce-ux-problems/",
    "hashtags": ["ecommerce", "ecommerceux", "conversionrate"]
  },
  "instagram": {
    "caption": "🚨 ...",
    "hashtags": ["ecommerce", "ecommerceux", "uxdesign", "webdesign", "ecommercetips"]
  },
  "slides": [
    {
      "type": "poster",
      "headline_top": "Your Customers Are Leaving.",
      "headline_main": "Do You Know Why?",
      "sub": "5 ecommerce UX problems that quietly cost you sales",
      "cards": [
        {"label": "Search", "detail": "No results"},
        {"label": "Product page", "detail": "Missing details"}
      ],
      "alt": "..."
    }
  ]
}
```

`slug`, `wp_post_id`, `canonical_url`, and `title` are copied exactly from the source file.
Never write a `state` key, the pipeline owns it.

## What the rendered poster is, and is not

The renderer draws the brand frame: blue background, white and yellow headline, numbered callout cards,
the Virtina logo and www.virtina.com. It cannot draw the illustrated scene (person, screens, props) that
Virtina's hand-made posts have. If a scene image is supplied at
`clients/virtina/output/social/slides/{pack name}/scene.png`, the renderer places it behind the cards.

## Publishing rules

- A pack is only posted once its article is live. While the WordPress post is a draft the pack is held.
- `auto_approve` is `true`: once the article is live and QA passes, the pack is posted with no approval step.
- Each channel is posted at most once per pack. The result is recorded in the pack's `state`.
