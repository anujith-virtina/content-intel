---
title: Featured image generation prompt — post 12478
client: impelhub
date: 2026-09-11
post_id: 12478
topic: Raise price or repackage the offer
stage: asset-spec
---

# Featured image — post 12478

**Required output: 1300 × 600 px, JPEG, landscape, under ~300 KB.**
That is the ImpelHub featured-image spec, unanimous across the 10 most recent posts.

## House style reference

Two styles exist on the blog. Use **Style A**, which is where the blog has moved.

| Style | Example | Look |
|---|---|---|
| **A — AI conceptual scene (use this)** | 12444 `blog-h1.jpg` | Dark navy boardroom, brass/gold machine, dramatic warm-vs-cold lighting, labelled machine parts, red LED readout, storm-lit city skyline through glass, cast of executives reacting. Cinematic, photoreal, heavy visual metaphor. |
| B — plain stock | 12330 | Laptop on a desk, soft window light, muted greens. Generic, older. |

## The article's thesis, which the image must carry

Price is the number a customer pays. Packaging is what that number buys. Raising the price on a
broken package converts a pricing problem into a churn problem. Fix packaging first, then price.

So the image should show **someone cranking PRICE up while the packaging behind them is visibly
broken** — not a generic "pricing" picture.

---

## PRIMARY PROMPT (paste into your image generator)

> Cinematic photoreal wide shot, 1300x600 landscape, dark navy executive boardroom at night, storm-lit
> city skyline through floor-to-ceiling glass. Centre: a large polished brass and glass machine on the
> boardroom table, engraved on its front with the words "THE PRICING ENGINE". On the left side of the
> machine a founder in a charcoal suit strains to turn an oversized gold dial labelled "PRICE",
> cranking it upward; the dial glows warm gold. On the right side of the machine sit three glass
> display cases labelled "GOOD", "BETTER", "BEST" — they are visibly mismatched: one case is
> overstuffed with brass feature tokens spilling over its rim, the middle case is nearly empty, and a
> crack runs down the third with tokens leaking out onto the table. A red LED ticker on the machine's
> base reads "CHURN RISK". Behind, on a wall screen, a line chart trends downward in red. Three
> executives in dark suits react with visible concern, one gesturing at the leaking case. Warm gold
> rim light on the machine against cool blue ambient light. Shallow depth of field, high detail,
> editorial magazine quality, no watermark.

**Negative prompt:** `text artifacts, garbled text, extra fingers, deformed hands, cartoon, flat
illustration, stock-photo handshake, logos, watermark`

Keep the readable words to the five labels above. Generators mangle long text, so if the output has
garbled lettering, regenerate rather than ship it.

---

## FALLBACK PROMPT (simpler, lower risk of text artifacts)

> Cinematic photoreal wide shot, 1300x600 landscape, dark navy boardroom at night, city skyline
> through glass. A brass balance scale dominates the frame on a walnut table. On the left pan: a
> single large glowing gold price tag. On the right pan: three stacked glass tier boxes, unevenly
> filled, one cracked and leaking small brass tokens. The scale tilts hard toward the price tag. A
> founder in a charcoal suit stands beside it, arms folded, studying the imbalance. Warm gold rim
> light against cool blue ambient light, shallow depth of field, editorial quality, no text, no
> watermark.

No lettering at all in this one, which removes the main failure mode.

---

## Alt text to use (114 chars, inside the 60–150 rule)

> Founder raising a pricing dial while mismatched product tier cases leak value, illustrating packaging versus price

## After you generate it

Send me the file and I will:
1. Resize/crop to exactly **1300 × 600** and compress under 300 KB
2. Upload to the ImpelHub media library
3. Set `featured_media` on post 12478 and write the alt text
4. Verify with a `context=edit` GET that it actually stuck

Do **not** reuse another post's image. Image reuse across posts is banned by
`clients/impelhub/MUST-FOLLOW-RULES.md` §3.
