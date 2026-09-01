---
title: Research — your B2B catalog is invisible to AI search
client: virtina
date: 2026-08-31
topic: Login-gated B2B catalogs and AI search visibility on WooCommerce
audience: B2B store owners and ecommerce managers on WooCommerce, $2M–$50M, who gated their catalog on purpose
stage: research
slug: gated-catalog-ai-visibility
uniqueness_audit: clients/virtina/output/research/uniqueness-audit-2026-08-31.md
competitor_analysis: clients/virtina/output/research/competitor-analysis-2026-08-31.md
---

# Research notes

## Verified facts (only these may be used)

### Google merchant listing structured data requires a real price
Source: https://developers.google.com/search/docs/appearance/structured-data/merchant-listing (fetched 2026-08-31)

Required properties: `name`, `image`, `offers`. Within `offers`: **`price`** (or `priceSpecification.price`) and
**`priceCurrency`** in ISO 4217. The documentation states merchant listings require **a price greater than zero**,
and that **"Only pages where a shopper can purchase a product are eligible for merchant listing experiences."**

**Why this matters for the post**: a quote-only B2B product page cannot produce a valid merchant listing. Not
because the markup is wrong, but because there is no price and no purchase path. This is the single hardest,
most citable fact in the article and it is stated by the platform itself rather than inferred.

**Caveat that must appear in-body**: Google's docs do **not** address login-gated pricing or quote-only products
directly. The conclusion that quote-only pages are ineligible follows from the stated requirements. Say that it
follows, do not claim Google says it.

### General Product structured data does not require price
Source: https://developers.google.com/search/docs/appearance/structured-data/product (fetched 2026-08-31)

The introductory product doc frames price as one of several possible enhancements, not a mandatory field. So
`Product` markup without a price is still valid markup. It just is not eligible for the merchant experiences.
Both facts are needed or the post overstates the problem.

## Rejected sources and claims

- **Forrester "one in five B2B sellers will face agent-led quote negotiations by end of 2026"** — appears in the
  Elogic post, attributed to Forrester, but the primary Forrester source was not located. **Do not cite.**
- **Any "% of B2B buyers now use AI" figure** — none survived verification, same finding as previous ChatSKU passes.
- **Vendor claims about ChatGPT/Claude crawler behaviour on gated catalogs** — the Pendium and Amplefound pages
  assert that gated catalogs render "a blank page or a sign-in screen" to scrapers. Mechanically obvious and
  uncontroversial, but no primary measurement. State it as mechanics, attach no statistic, cite nobody.
- **No dollar figure** for what gated invisibility costs. Do not invent one.

External link budget: **1 used** (Google merchant listing doc). Cap is 2.

## The core argument

Every AI-visibility article assumes a public catalog. B2B stores are the opposite by design, and the design is
usually correct: prices are negotiated per account, competitors shop your list, and MAP agreements bind you.

Four structural problems, none of which are fixed by better markup:

1. **Nothing to fetch.** A retrieval bot requesting a gated product URL gets a login screen. There is no partial
   credit and no rendering of the protected content.
2. **No price means no merchant listing.** Verified above. Quote-only pages fail a stated requirement.
3. **No purchase path.** "Request a quote" is not an offer an agent can evaluate or transact against.
4. **Tiered pricing has no honest schema representation.** One product with six negotiated prices does not fit
   a single `Offer`, and publishing a representative price misrepresents what any given buyer pays.

The reframe: this is not an SEO defect to patch. It is a commercial decision about which layer of your catalog
is public. Most B2B stores have never separated the two questions, so they gate everything by default.

## The three-layer answer (the post's spine)

- **Layer 1, public**: that the product exists. Name, specification, compatibility, application, materials,
  certifications, lead-time ranges, minimum order quantity. None of this is commercially sensitive and all of it
  is what an agent needs to shortlist you.
- **Layer 2, public but not priced**: commercial shape without numbers. That you sell in tiers, the tier
  structure, whether you do contract pricing, order minimums, who you sell to.
- **Layer 3, gated**: the account's actual negotiated price. Stays behind login, permanently and correctly.

Most stores currently draw the line above layer 1. Moving it down two layers costs nothing commercially and is
the entire fix.

## WooCommerce-specific mechanics (must stay accurate)

Verify each before writing; do not invent field names.

- WooCommerce has a per-product **catalog visibility** setting ("Shop and search results", "Shop only",
  "Search results only", "Hidden"). "Hidden" removes it from the site's own search and shop, which is a stronger
  gate than most owners realise they applied.
- Role-based pricing and catalog gating on WooCommerce is normally a **plugin** behaviour (B2BKing, Wholesale
  Suite, the native B2B Pricing extension), not core. Do not attribute plugin behaviour to WooCommerce core.
- WooCommerce outputs `Product` JSON-LD by default; when a product has no price, the offer data is incomplete.
  **Do not state a specific WooCommerce version behaviour that has not been checked.** Keep this general.
- `robots.txt` governs crawler access site-wide and is where AI user agents are allowed or blocked. Naming
  specific bot user-agent strings is safe only if not attached to claimed traffic numbers.

## Semantic terms to cover (10–15, naturally)

customer group pricing, tiered pricing, minimum order quantity, request a quote, RFQ, catalog visibility,
structured data, JSON-LD, schema markup, retrieval bot, crawler access, robots.txt, product attributes,
lead time, contract pricing, self-hosted storefront

## Internal link candidates (verify 200 before push)

- `/ecommerce-store-agent-ready/` — the public-catalog companion. Concede its territory in one sentence.
- `/woocommerce-b2b-pricing-and-access-setup/` — how the gating is configured. This post is what it costs.
- `/woocommerce-b2b-customer-portal/` — the self-service layer behind the gate.
- `/woocommerce-erp-integration/` — where authoritative product data actually lives.
- `/woocommerce-punchout-catalog-integration/` — the procurement-system counterpart to agent access.
- `/woocommerce-development-services/` — service page.
- `/get-in-touch/` — contact.

## Format

**Format E (contrarian thesis).** The thesis contradicts the prevailing "add schema and you are AI-ready"
advice and contradicts the reflex to gate everything. Format A was used on 42391/42393; E was last used on
42465 (2026-08-10) and 42441. Acceptable rotation given the thesis genuinely is contrarian, and B was used on
42441.
