# Post 37791 refresh - how to apply

Everything is written and verified. One blocker stands in the way, and it cannot be
solved over the REST API.

## The blocker

The live page renders from Thrive's `tve_updated_post` meta. That key is **readable**
over REST on virtina.com but **not writable**: a POST with a changed value returns
HTTP 200 and the stored value does not change. Verified 2026-09-07 by writing a
distinct value and re-reading it.

`title`, `post_content` and the Yoast fields DO write. That means a REST push can only
half-update the page, giving it a new headline over the old body. Do not do that.
The page was pushed, found to be half-updated, and **fully restored** to its
pre-session state the same day.

## The finished content

`clients/virtina/output/drafts/best-ecommerce-websites-FINAL-37791-2026-09-07.html`

108,337 chars. Verified: divs balanced, every anchor id preserved, 0 em dashes,
0 vendor/competitor links, 0 invented `data-css` tokens, 2 inline-styled tables,
12 internal links all live-200-checked.

## Option A, WP CLI (preferred)

    wp post meta delete 37791 tve_updated_post

WordPress then falls back to `post_content`. So first put the finished markup into
`post_content`, then clear the meta:

    python clients/virtina/output/research/apply_37791_refresh.py publish
    wp post meta delete 37791 tve_updated_post

Order matters. The script writes `post_content` (and the title and Yoast fields);
clearing the meta is what makes it render.

## Option B, Thrive editor

Open post 37791 in Thrive Architect and paste the sections in by hand, using the
finished file as the source. Slow, and the tables will need rebuilding as Thrive
elements.

## Also apply with it

- Title: `Top 10 online shopping sites in the world, plus 11 eCommerce websites worth knowing`
- Yoast title: `Top 10 Online Shopping Sites in the World (2026) | Virtina`
- Yoast description: `See the top 10 online shopping sites in the world, ranked by monthly visits (Semrush, July 2026), plus why Taobao and JD.com never appear in traffic lists.`
- Yoast focus keyword: `top 10 online shopping sites in world` (currently empty)

## Rollback

`clients/virtina/output/backups/post-37791-*-2026-09-07.*` holds the Thrive meta,
both CSS metas, `post_content` and the full JSON as they were before any change.

## Separate issue, needs a decision

15 injected/paid vendor links sit in this page's Thrive markup, 14 of them inside
`<h2>` tags, most as empty anchors wrapping a space. The same footprint appears on
**7 other posts**: 37847, 36981, 37296, 36161, 37745, 36887, 36423. Roughly 135
hidden anchors in total, all pointing at virtocommerce, sharetribe, webkul,
cedcommerce, yo-kart and bigcommerce. The refresh strips them from 37791. The other
seven are untouched and need a decision from the site owner.
