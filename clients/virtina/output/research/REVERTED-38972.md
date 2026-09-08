# Post 38972 — reverted 2026-09-08

The live page https://virtina.com/woocommerce-dropshipping-plugins/ was restored to
its pre-session state. Body verified byte-identical to
`backups/post-38972-tve_updated_post-2026-09-08.html` by sha256. Live check after
restore: 7,679 words, 25 plugins, 49 images, original H1, status publish, categories
and featured image untouched.

## Why the approach was wrong

This page is built in **Thrive Architect**. I edited its stored markup as raw HTML
from outside the builder.

Removing whole balanced blocks worked. **Generating new Thrive elements did not.**
Thrive's per-element styling lives in `data-css` tokens that its editor mints and
maintains alongside `tve_custom_css`. Cloning a token from a neighbouring element
produces markup that passes every structural check and still renders wrong, because
the token was authored for a different element in a different context.

The two visible failures were symptoms:
1. a table written with escaped entities rendered as literal `<table><tr>` text,
   because the container it went into does not decode entities
2. new entries rendered as oversized black text, because their elements carried no
   styling tokens

The cause was doing visual-builder work through an API with no knowledge of the
builder's styling model.

**Rule: do not generate new Thrive elements programmatically. Structural deletions of
whole balanced blocks are safe. New content belongs in the Thrive Architect editor.**

## The findings still stand and are worth applying

From `woocommerce-dropshipping-plugins-refresh-2026-09-08.md`, all verified 2026-09-08:

- **8 of the 25 listed plugins should go.** Beeketing (dead since 2019) and Ezusy
  (domain does not resolve); Modalyst and Zendrop (both dropped WooCommerce);
  CartFlows (a funnel builder, not a dropship plugin); AliNext Lite (the same plugin
  as Ali2Woo, listed twice); NextsChain (unverifiable); WooDropship (no activity
  since Jul 2023).
- **Renames:** WooShark is now SharkDropship. "AutoD" should read AutoDS.
- **All five market statistics fail verification.** The $365.67bn figure is Grand
  View's 2025 number labelled 2024, the $802.33bn apparel figure is untraceable and
  mis-scoped, and three firms' 2025 estimates span a 60% range.
- **The TOC has a broken link:** `http://best-woocommerce-dropshipping-plugins`,
  missing its `#`, sends readers to a nonexistent external host.
- **The page never uses its own target keyword.** "dropship plugin" appears 0 times
  against 36 uses of "dropshipping plugin". The Yoast focus keyword is empty.
- **An editorial instruction is published as image alt text:** "Just update the
  previous image by addingb these also AutoDS, CJdropshipping ,Printify, Zendrop".
- **No pricing anywhere**, while all five ranking competitors price every plugin.
  11 verified prices are in the research file, with the 4 unverifiable ones named.
- **5 plugins are missing**, all verified maintained: the official WooCommerce.com
  extension (OPMC, rated 2.7/5), ALD by VillaTheme (9,000+ installs), TMDS for Temu,
  DropshipMe and EPROLO. New copy for all five is in
  `../drafts/dropship-new-entries-2026-09-08.txt`.

Also: **post 31786 still recommends WooDropship**, so it needs the same correction.
