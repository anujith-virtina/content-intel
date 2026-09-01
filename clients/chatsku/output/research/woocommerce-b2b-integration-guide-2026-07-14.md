---
title: Research notes — ChatSKU + WooCommerce B2B: the full integration guide
client: chatsku
date: 2026-07-14
topic: ChatSKU + WooCommerce B2B technical integration (REST API, plugin data flow)
slug: woocommerce-b2b-integration-guide
stage: research
---

# Research: ChatSKU + WooCommerce B2B: the full integration guide

## Mandatory-rules and uniqueness check (completed)

Read in full before research: `clients/chatsku/MUST-FOLLOW-RULES.md`, `clients/chatsku/reference/published-posts-inventory.md`, `clients/chatsku/style/voice.md`, `style/audience.md`, `style/brand.md`. Also fetched the two live sibling posts directly (685, 1056) rather than relying on inventory summaries alone, per the brief's instruction.

**Topic uniqueness:** No existing ChatSKU post covers WooCommerce technical integration (REST API mechanics, plugin data architecture). Post 685 is the only WooCommerce post and it is a general how-to. Confirmed not duplicated.

**Angle uniqueness:** This post's angle — "how ChatSKU actually reads a WooCommerce B2B store's catalog and pricing data, plugin by plugin" — does not exist anywhere in the inventory. It mirrors the role post 1056 plays for Magento (technical integration companion) rather than post 685's role (general how-to/why).

**Slug:** Proposed `woocommerce-b2b-chatbot-integration` (mirrors `magento-b2b-chatbot-integration` naming pattern). Does not collide with existing slug `b2b-chatbot-for-woocommerce` (post 685) or any other slug in the inventory.

**Topic gaps list** in the inventory also names "customer groups / tiered pricing for B2B WooCommerce" as an open gap — this post directly fills it.

## What post 685 already owns (avoid re-covering this ground)

Fetched live from https://chatsku.com/b2b-chatbot-for-woocommerce/. Post 685 (Format B, Conversational Q&A + How-To, June 29 2026) covers:

- Definitional framing: what is a B2B chatbot for WooCommerce, why B2B WooCommerce needs it more than B2C
- 6 capabilities list (SKU questions, customer-specific pricing, quotes in chat, large-catalog discovery, after-hours capture, routing to sales)
- Generic 7-step deploy checklist (export CSV, choose platform, connect pricing, configure RFQ routing, add script, test, go live) — **not API-level detail**
- Plugin landscape mentioned only by name (B2BKing, Wholesale Suite, B2B for WooCommerce) with no technical detail on how each stores or exposes data
- Cost tiers: generic $50-500/mo, B2B-aware $200-2,000/mo, custom $20K-100K
- Worked ROI: 4,200-SKU store, $750 AOV, 980 after-hours visitors, 1.6% to 3.4% conversion, $158,760/yr gain
- 7-point readiness checklist, 7-Q FAQ (B2BKing/Wholesale Suite compatibility, site speed, login pricing, quote/order creation, mobile, variations, PDF catalogs)
- External sources: Gartner 67% rep-free (2026), WooCommerce product CSV importer/exporter docs

**Conclusion:** post 685 never opens the REST API, never names an endpoint, never explains how B2BKing/Wholesale Suite/WholesaleX/Addify actually store pricing data, and never discusses auth, webhooks, sync-vs-live-query, or headless considerations. That entire layer is open.

## What post 1056 (Magento) already owns — mirror its role, not its content

Fetched live from https://chatsku.com/magento-b2b-chatbot-integration/. Post 1056 (Format B, How-To, July 6 2026) is the integration-intent companion to WooCommerce's how-to post — structurally: what integration means, why native B2B needs it more, 5 data items ChatSKU reads (H3 subheads), 7-step API HowTo (generate token, sync SKUs, map shared catalogs, configure quote flow, embed script, live test, deploy), does-it-replace-native question, deploy time, cost tiers ($50-500 / $200-2,000 / $30K-150K), worked ROI (18,000 SKU, $1,800 AOV, 1,500 sessions, 1.8% to 3.6%, $583,200/yr), FAQ on Open Source vs Adobe Commerce, REST/GraphQL, Hyva/headless, multi-store.

**Key structural fact for this new post:** Magento B2B is a single native module (Adobe Commerce B2B) with one API surface (REST/GraphQL) covering company accounts, shared catalogs, negotiable quotes. WooCommerce has **no native B2B layer at all** — B2B is bolted on entirely through third-party plugins, each with a different data architecture. This is the genuine structural difference that should drive this post's unique technical content: Magento integration = "read one native API." WooCommerce integration = "read the core WooCommerce API, then figure out which of several possible plugin-specific pricing layers is doing the group/tiered pricing, because they don't all store or expose it the same way."

## Verified technical facts — WooCommerce REST API

Source: [WooCommerce REST API | WooCommerce developer docs](https://developer.woocommerce.com/docs/apis/rest-api/) (official, primary, current as of 2026).

- Current base path: `/wp-json/wc/v3/` (e.g., `https://yourstore.com/wp-json/wc/v3/products`). Older documentation references `/wc-api/v3/` — that is a legacy pre-JSON-API path; current implementations use the WordPress REST API namespace.
- Auth: consumer key + consumer secret, generated in WooCommerce > Settings > Advanced > REST API, with read/write permission scoping per key. Basic Auth over HTTPS is the recommended method; query-string credentials are documented as a local-testing-only fallback (exposes keys in server logs on production).
- Requires WooCommerce 3.5+, WordPress 4.4+, pretty permalinks enabled.
- Core resource endpoints: products, product variations, product categories, product attributes, customers, orders, coupons, refunds, webhooks, taxes, reports.
- Product endpoint exposes: `sku`, `regular_price`, `sale_price`, `stock_quantity`, `manage_stock`, categories, attributes, and (via a sub-resource) variations for variable products.
- Customer endpoint (`/wp-json/wc/v3/customers`) exposes billing/shipping data, order history, total spend — but **does not expose WordPress user role** as a field.
- Webhooks are supported for `product.created/updated/deleted`, `order.created/updated/deleted`, `customer.created/updated/deleted`, `coupon.created/updated/deleted`, plus custom topics tied to WordPress hooks — this is the mechanism for live sync rather than polling.

## Verified technical fact — the role gap (load-bearing finding for this post)

Source: [Users – REST API Handbook, developer.wordpress.org](https://developer.wordpress.org/rest-api/reference/users/) and a GitHub issue thread on the woocommerce-rest-api repo confirming role is read-only via WooCommerce's own API.

- A WordPress user's **role** (the field B2B pricing plugins key their group/tier logic to) is exposed by the core WordPress REST API at `/wp-json/wp/v2/users`, not by the WooCommerce customer endpoint.
- WooCommerce's REST API documentation issue tracker confirms the `roles` field, where present, is read-only through WooCommerce's own customer resource.
- **Practical implication for an integration:** reading a WooCommerce B2B buyer's identity and their price tier requires querying two separate API surfaces: the WordPress core users endpoint for role/group membership, and the product/postmeta layer (via WooCommerce or WP REST API) for the role-keyed price itself. This is genuinely different from Magento B2B, where company account and shared-catalog pricing live behind one native API. [unverified: exact meta key naming conventions vary per plugin and are not always documented publicly — flagged below]

## Verified technical facts — B2B pricing plugins (data architecture, not endorsement)

### B2BKing
Source: [Does B2BKing have a REST API?](https://woocommerce-b2b-plugin.com/docs/does-b2bking-have-a-rest-api-wp-and-woo-apis/) (vendor documentation, primary for their own product).

- B2BKing has **no dedicated API of its own**. All data (customer groups, tiered prices, group prices) is stored as standard WordPress/WooCommerce post and user metadata, so it is readable and writable through the existing WP REST API and WooCommerce REST API.
- Group prices and tiered prices are saved as **product/post metadata** — editable via either the WooCommerce or WordPress REST API.
- Dynamic pricing rules are stored as a custom post type, exposed at `/wp-json/wp/v2/b2bking_rule`.
- Fixed-price rules can be bulk-created via the WP REST API, which the vendor documentation frames explicitly as useful for syncing from an ERP or external system.

### Wholesale Suite
Source: [Wholesale Suite API Overview](https://wholesalesuiteplugin.com/kb/wholesale-suite-api/) (vendor documentation, primary).

- Unlike B2BKing, Wholesale Suite ships **its own dedicated REST namespaces**: `wholesale/v1/` and `wwlc/v1`.
- These expose wholesale products, wholesale variations, wholesale roles (which users get which pricing/product visibility), and wholesale leads — all as separate CRUD-capable resources, authenticated the same way as core WordPress REST API (key-based auth).
- This is a structurally different integration path than B2BKing: an integration built for one plugin's data model won't automatically read the other's, even though both plugins solve "role-based pricing."

### WholesaleX
- Adds role-based and quantity/tiered pricing, cart-level role discounts, 16+ dynamic discount rule types. [unverified] — no public documentation surfaced describing a dedicated REST API or endpoint namespace comparable to Wholesale Suite's; pricing data likely also lives as product/postmeta (consistent with the WordPress plugin convention B2BKing uses), but this could not be independently confirmed from public docs at time of research.

### Addify — B2B for WooCommerce / Role Based Pricing for WooCommerce
Source: general vendor and marketplace listings (Addify store, WooCommerce.com marketplace listing).

- Role/customer-group based pricing configurable per product or per category, plus bulk CSV import/export of pricing rules.
- No public API documentation found describing REST endpoints; likely follows the same postmeta convention as the other plugins, but this is [unverified].

**Net technical finding:** WooCommerce B2B pricing data is not uniform. Most plugins (B2BKing, likely WholesaleX, likely Addify) piggyback on core WP/WC metadata and are reachable through the standard REST API once you know the meta keys. One major plugin (Wholesale Suite) ships a dedicated namespace instead. A real integration has to detect which plugin (or combination) is active and adapt, which is exactly the kind of plumbing a buyer-facing catalog assistant handles so the store owner doesn't have to. This is a strong, genuinely new technical narrative thread not used in 685 or 1056.

## Data ChatSKU must read to answer a WooCommerce B2B buyer (data flow map)

Synthesized from the WooCommerce REST API docs + plugin docs above, and structurally parallel to (but distinct from) 1056's 5-item Magento list:

1. **Product catalog and variations** — SKU, title, attributes, variation matrix, via `/wp-json/wc/v3/products` and `/products/{id}/variations`.
2. **Stock and lead-time data** — `stock_quantity`, `manage_stock`, backorder status, same product endpoint.
3. **Buyer identity and role/group** — via `/wp-json/wp/v2/users`, since the WooCommerce customer endpoint doesn't expose role.
4. **Role- or tier-keyed pricing** — plugin-dependent: postmeta (B2BKing-style) or a plugin's own namespace (Wholesale Suite-style).
5. **Quote/RFQ state** — WooCommerce doesn't natively support quotes; this lives entirely inside whichever B2B plugin is installed, usually as a custom post type or order-status extension (e.g., "quote requested" as a custom order status).
6. **MOQ (minimum order quantity) rules** — plugin-specific, typically stored as product-level meta or a dynamic rule tied to role + quantity, not a native WooCommerce field.

## Deployment/technical setup facts

- WooCommerce stores overwhelmingly still run traditional WordPress + WooCommerce (one industry estimate: roughly 97-98% non-headless vs. a small but growing headless/decoupled share) [unverified, secondary-source aggregation, treat as directional not precise].
- Headless/decoupled WooCommerce (React/Next.js frontend, WooCommerce as backend via REST/GraphQL) is a small but reportedly fast-growing segment. [unverified — figures come from marketing-agency blogs, not a primary WooCommerce source; do not cite a specific multiplier in the post].
- For a script-tag deployment (ChatSKU's standard model), embed location differs from Magento: WooCommerce runs on WordPress themes, so the script goes in the theme's footer via a hook (or a plugin like a header/footer script injector) rather than a layout XML file. For headless builds, the script would need to be added directly to the custom frontend's shell component instead of a WordPress theme file.
- Sync vs. live query: because catalog and stock change constantly, a live-query model (calling the REST API at time of buyer question) avoids stale pricing, while webhooks (`product.updated`, `order.updated`) support a cache-and-refresh model for performance. This distinction was not discussed in 685 (which only mentioned CSV export) and is a legitimate technical differentiator.

## ROI stat sourcing (for worked example — must differ from 685 and 1056)

- Reusing Gartner's 67% B2B-buyer rep-free preference stat is permitted by the brief and already used across the site consistently; retain for continuity but do not re-verify further (already vetted in prior posts).
- **New worked-example numbers proposed** (illustrative, not attributed to a real client — matches the disclosure convention used in 685/1056):
  - Distributor scenario: 9,500 SKUs across categories, WooCommerce + B2BKing stack
  - After-hours sessions/month: 1,150
  - AOV: $980
  - Conversion before: 1.5% -> after: 3.2%
  - Orders before: ~17/mo -> after: ~37/mo
  - Monthly revenue before: ~$16,660 -> after: ~$36,260
  - Annual gain: ~$235,200
  - These numbers are distinct from 685 (4,200 SKU / $750 AOV / 1.6%->3.4% / $158,760) and 1056 (18,000 SKU / $1,800 AOV / 1.8%->3.6% / $583,200) in every input variable.

## Data points

| Stat | Value | Source | Date |
|------|-------|--------|------|
| WooCommerce REST API base path | `/wp-json/wc/v3/` | [WooCommerce developer docs](https://developer.woocommerce.com/docs/apis/rest-api/) | 2026 |
| Auth method | Consumer key/secret, Basic Auth over HTTPS | [WooCommerce developer docs](https://developer.woocommerce.com/docs/apis/rest-api/) | 2026 |
| Customer endpoint excludes role | Confirmed, role lives in `/wp/v2/users` | [WP REST API Users reference](https://developer.wordpress.org/rest-api/reference/users/) | 2026 |
| B2BKing has no dedicated API | Confirmed — uses WP/WC metadata | [B2BKing docs](https://woocommerce-b2b-plugin.com/docs/does-b2bking-have-a-rest-api-wp-and-woo-apis/) | 2026 |
| B2BKing dynamic rules endpoint | `/wp-json/wp/v2/b2bking_rule` | [B2BKing docs](https://woocommerce-b2b-plugin.com/docs/does-b2bking-have-a-rest-api-wp-and-woo-apis/) | 2026 |
| Wholesale Suite dedicated namespaces | `wholesale/v1/`, `wwlc/v1` | [Wholesale Suite API overview](https://wholesalesuiteplugin.com/kb/wholesale-suite-api/) | 2026 |
| Gartner rep-free preference | 67% of B2B buyers prefer a rep-free path for at least part of the purchase | Gartner, 2026 (already used sitewide) | 2026 |
| WooCommerce market share | 20-33% depending on measurement methodology | [Multiple aggregator estimates] | 2026 [unverified — wide variance across sources, do not cite a single precise figure] |

## Conflicts and disagreements

- **WooCommerce market share:** sources range from ~20% (top 1M sites, BuiltWith-style traffic-weighted) to ~33% (all online stores, broader crawl). **What's actually true:** genuinely methodology-dependent; safest is to avoid a precise percentage in the post or caveat it heavily, since none of these are a single authoritative primary source (no official WooCommerce/Automattic market-share release found).
- **Headless WooCommerce adoption rate:** claims of "3x growth by 2027" and "82% custom themes" come from marketing-agency blogs (Blacksmith, Crocoblock, dk-gupta), not primary WooCommerce data. **What's actually true:** unresolved; treat as directional color at most, flag `[unverified]`, and consider omitting specific multipliers from the final draft.
- **WholesaleX and Addify API architecture:** no primary vendor documentation found describing dedicated endpoints (unlike Wholesale Suite, which explicitly documents its own namespace). **What's actually true:** unresolved; the safest defensible claim is that these plugins "store pricing as product data, most commonly as metadata" without asserting an unverified specific endpoint.

## Competitive scan (top-ranking WooCommerce B2B integration content)

1. Various "WooCommerce B2B plugin comparison" listicles (Addify, B2BKing, WholesaleX vendor blogs) — angle: feature comparison to sell their own plugin. Gap: none discuss integrating an external AI/chat layer on top, none discuss REST API mechanics for a third-party service.
2. Virtina's own "WooCommerce B2B Configuration Guide 2026" (virtina.com) — angle: how a store owner configures B2B pricing/access directly (not an integration guide for an external tool). Gap: doesn't overlap with ChatSKU's integration angle; different audience intent (setup vs. connecting a chat layer). Not a competitor to link, but useful to know it exists (Virtina is ChatSKU's parent company per brand.md, so no cross-linking needed but also nothing to avoid duplicating on the ChatSKU side since audiences/intents differ).
3. General "WooCommerce REST API tutorial" developer content (Cloudways, various dev blogs) — angle: generic API usage for developers building custom integrations. Gap: none are B2B-specific or chatbot/catalog-assistant specific.

No existing content anywhere (not just on chatsku.com) combines WooCommerce REST API mechanics + B2B pricing plugin data architecture + AI catalog assistant integration in one piece. That is the gap.

## The gap

> Every WooCommerce B2B chatbot article (including ChatSKU's own post 685) treats "connect your pricing" as a single generic step. In reality, WooCommerce has no native B2B layer at all — pricing logic lives inside whichever third-party plugin the store runs, and those plugins store and expose that data in genuinely different ways (postmeta vs. dedicated REST namespace). An integration guide that actually explains this, plugin by plugin, doesn't exist yet.

## Recommended angle

> Position this as the technical-integration companion to post 685 (mirroring 1056's relationship to Magento): open with the fact that WooCommerce B2B isn't one native system but a patchwork of plugins, walk through exactly what ChatSKU reads from the core WooCommerce REST API vs. what it reads from whichever B2B plugin is active (B2BKing, Wholesale Suite, WholesaleX, Addify), and give a concrete API-level integration flow (auth, endpoints, sync vs. webhook) rather than a generic deploy checklist.

## Couldn't find

- No official WooCommerce/Automattic-published market-share figure — all figures are third-party estimates with real methodology disagreement. Recommend omitting a specific percentage from the final draft or using a heavily caveated range.
- No public API documentation for WholesaleX or Addify's B2B for WooCommerce plugin describing dedicated endpoints or exact meta key names. Recommend describing their data model at the "stored as product data" level of generality rather than asserting specifics.
- Exact B2BKing meta key names (e.g., a literal `_b2bking_group_price` string) were not confirmed in public-facing documentation — the vendor doc confirms the storage mechanism (post/product metadata) but not the literal key. Do not invent a specific meta key name in the draft.
- No primary, dated statistic on headless WooCommerce adoption rate from an authoritative source (only marketing-agency blog estimates). Recommend leaving specific growth multipliers out of the final piece.

## Sources

- [WooCommerce REST API | WooCommerce developer docs](https://developer.woocommerce.com/docs/apis/rest-api/) — official, primary, 2026. **Strongest source, use as the article's cited external authority.**
- [Authentication | WooCommerce developer docs](https://developer.woocommerce.com/docs/apis/rest-api/authentication/) — official, primary, 2026
- [Users – REST API Handbook, developer.wordpress.org](https://developer.wordpress.org/rest-api/reference/users/) — official WordPress core docs, primary, 2026
- [Does B2BKing have a REST API? WP and WOO APIs — B2BKing](https://woocommerce-b2b-plugin.com/docs/does-b2bking-have-a-rest-api-wp-and-woo-apis/) — vendor documentation, primary for their own product, 2026
- [Wholesale Suite API Overview](https://wholesalesuiteplugin.com/kb/wholesale-suite-api/) — vendor documentation, primary for their own product, 2026
- [WooCommerce Role Based Pricing: Everything You Need to Know — B2BKing](https://woocommerce-b2b-plugin.com/woocommerce-role-based-pricing-prices-by-user-role/) — vendor blog, secondary
- [Role Based Pricing for WooCommerce — Addify](https://addify.store/product/woocommerce-role-based-pricing/) — vendor listing, secondary
- [WholesaleX — WordPress.org plugin page](https://wordpress.org/plugins/wholesalex/) — plugin directory listing, secondary
- https://chatsku.com/b2b-chatbot-for-woocommerce/ — live ChatSKU post 685, read in full for differentiation mapping
- https://chatsku.com/magento-b2b-chatbot-integration/ — live ChatSKU post 1056, read in full for structural mirroring
- Multiple secondary aggregator sources on WooCommerce market share (Redstag Fulfillment, Colorlib, Mobiloud, Cloudways, Statista topic page) — read for context, not cited with precision due to methodology conflicts

