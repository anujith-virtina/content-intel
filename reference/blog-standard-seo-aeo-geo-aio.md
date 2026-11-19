# Blog standard: SEO + AEO + GEO + AIO (all clients)

Standing instruction from the user (2026-11-19): every blog is written for classic search **and** AI answers.
Model article: https://www.accucia.com/blog/seo-is-no-longer-enough-aeo-geo-and-aio-in-2026 (structure only, never copy its text).

Client `MUST-FOLLOW-RULES.md` files still win on visual, format and voice rules. This file adds the search/AI layer on top.

## The four layers

| Layer | Goal | What it means in the post |
|---|---|---|
| **SEO** | Rank the page | One primary keyword in title, slug, H1, first 100 words, one H2; meta title ≤60, description 150–160; internal links to money pages; fast, crawlable HTML; descriptive alt text |
| **AEO** (answer engine) | Win the direct answer / snippet / PAA | Question-style H2s phrased the way people ask; first 1–2 sentences under each H2 answer it directly (40–60 words); People Also Ask block; FAQ of real questions with short answers |
| **GEO** (generative engine) | Get quoted and cited by ChatGPT, Claude, Perplexity, Gemini, AI Overviews | Specific, verifiable claims; statistics with named, linked sources and dates; clear attributable statements ("ChatSKU's view is…"); quotable lists and tables; brand/entity named consistently with a one-sentence entity definition |
| **AIO** (AI optimisation, implementation) | Make it machine-readable | Article + FAQPage schema (FAQ mirrored in JSON-LD), BreadcrumbList; semantic H2/H3 only; short declarative sentences; real author/reviewer and visible published + updated dates; one clear point of view per page |

## Required structure (in this order)

1. **H1** with the primary keyword.
2. **Quick Answer / Executive Summary**: 2–4 sentences that fully answer the title question. Liftable on its own.
3. **Key Takeaways**: 3–5 bullets, each starting with a bold lead phrase.
4. **Introduction**: the problem, who it is for, what the reader will be able to decide.
5. **Definitions** where terms are involved: one bolded sentence per term, then how they differ.
6. **Body H2s as questions**, each with a direct answer first, then detail, H3s for sub-points.
7. **At least one table** (comparison, checklist or decision matrix) with a dated source column where facts are cited.
8. **Practical checklist or steps** the reader can act on today.
9. **People Also Ask** (3–5).
10. **Conclusion** with one CTA (no inline promo links).
11. **FAQ** (4–8), each answer 1–3 sentences, opening with a direct word ("Yes", "No", "Start with…"). Mirrored in FAQPage schema.
12. Author/reviewer box, published date, last-updated date.

## Writing rules

- Sentences ≤20 words, paragraphs 1–3 sentences. Bullets only for genuinely list-shaped content; prose for reasoning.
- Every statistic: named source, link, date checked. No stat without a source. No invented numbers.
- Name the brand entity the same way every time; include one "X is a … that …" sentence.
- Do better than the model article: it cites no sources and has no updated date. We always cite and always date.
- Freshness: when a post is refreshed, update the visible "Updated" date and `dateModified`.

## QA gate before publish

- [ ] Quick Answer liftable without context
- [ ] Every H2 opens with a direct answer
- [ ] Key Takeaways present
- [ ] ≥1 table
- [ ] Every stat sourced + dated
- [ ] PAA + FAQ present, FAQ in JSON-LD
- [ ] Article + FAQPage + Breadcrumb schema valid
- [ ] Meta title/description lengths, keyword placement
- [ ] Published + updated dates and a real author visible
