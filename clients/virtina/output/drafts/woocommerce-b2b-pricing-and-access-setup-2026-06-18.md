---
title: WooCommerce B2B Configuration: A Step-by-Step Guide to Pricing Rules, Customer Groups, and Catalog Access
client: virtina
date: 2026-06-18
topic: WooCommerce B2B store configuration (pricing rules, customer groups, catalog access)
audience: WooCommerce B2B store owners and developers setting up or fixing pricing/access configuration
stage: draft
slug: woocommerce-b2b-pricing-and-access-setup
format: Format A (standard explanatory)
word_count: 2580
---

<!-- FEATURED IMAGE PLACEHOLDER
Dimensions required: 1309x500 px exactly, JPEG quality 82, under 200KB
Subject: WooCommerce B2B admin dashboard on a desktop screen showing customer group settings and pricing rule fields (per topic keyword library: "office team meeting computers")
Source priority: Pexels API > Openverse (source=stocksnap) > Wikimedia Commons
Alt text (80-150 chars): "WooCommerce admin dashboard showing B2B customer group settings and tiered pricing rule configuration fields"
-->

<h1>WooCommerce B2B configuration: a step-by-step guide to pricing rules, customer groups, and catalog access</h1>

<p><strong>By Gigi JK</strong> | WooCommerce, B2B eCommerce | Updated June 18, 2026</p>

<!-- SUMMARY BLOCK (Template A) -->
<div style="background:linear-gradient(rgba(0,213,192,0.28),rgba(0,213,192,0.28));border-radius:20px;padding:30px;margin:0 0 28px 0;">
<h2 dir="ltr" style="color:#43627f;font-size:30px;">Summary</h2>
<p dir="ltr" style="font-size:16px;line-height:1.75;">WooCommerce does not handle B2B pricing, customer groups, or catalog access out of the box. Each piece needs its own setup: role-based pricing, tiered discounts, minimum order quantities, quote requests, tax exemption, and catalog visibility.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">This guide covers all six areas with named plugins and real admin-panel steps. It also compares B2BKing, Wholesale Suite, and WooCommerce.com's native B2B Pricing extension. You'll leave with a working setup path, not a stack of generic advice.</p>
</div>

<!-- INTRODUCTION BLOCK (Template B) -->
<div style="background:linear-gradient(rgba(241,243,250,0.5),rgba(241,243,250,0.5));border-radius:20px;padding:30px;margin:0 0 28px 0;">
<h2 style="color:#43627f;font-size:30px;">Introduction</h2>
<p dir="ltr" style="font-size:16px;line-height:1.75;">A B2B buyer expects different prices, different minimums, and sometimes a different catalog than a retail shopper sees. Default WooCommerce gives every visitor the same price, the same checkout, and the same product list. Closing that gap takes deliberate configuration, not a single toggle.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Most WooCommerce B2B guides either pitch one plugin or stay vague about admin steps. This one names three plugin paths and compares what each actually supports. It walks through dashboard-level settings for customer groups, tiered pricing, MOQ, quote requests, tax exemption, and catalog visibility.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Net payment terms and the customer self-service portal are covered elsewhere on this site. They're linked where relevant, so this guide stays focused on pricing and access mechanics.</p>
</div>

<!-- TABLE OF CONTENTS (Template C, from toc-working-template.html) -->
<h3 style="color:#43627f;font-size:22px;">Table of Contents</h3>
<ul style="list-style:none!important;padding-left:0!important;margin:0 0 1.5em 0!important;">
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#customer-groups-pricing" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">How do you set up customer groups and role-based pricing?</a></li>
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#tiered-pricing-rules" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">How do tiered and quantity-based pricing rules work?</a></li>
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#minimum-order-quantity" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">How do you enforce minimum order quantities?</a></li>
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#quote-request-workflows" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">What is a quote request workflow and when do you need one?</a></li>
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#tax-exemption-handling" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">How do you handle tax exemption certificates?</a></li>
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#catalog-visibility-rules" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">What catalog visibility rules should you use?</a></li>
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#plugin-comparison" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">Which B2B pricing plugin should you choose?</a></li>
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#people-also-ask" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">People also ask</a></li>
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#conclusion" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">Conclusion</a></li>
<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="#faq" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">Frequently asked questions</a></li>
</ul>

<!-- SECTION: customer groups and role-based pricing -->
<div style="background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));border-radius:20px;padding:30px;margin:0 0 28px 0;">
<h2 id="customer-groups-pricing" style="color:#43627f;font-size:30px;">How do you set up customer groups and role-based pricing in WooCommerce?</h2>
<p dir="ltr" style="font-size:16px;line-height:1.75;">You set up customer groups and role-based pricing in WooCommerce with a dedicated B2B plugin. The core platform has no native concept of a wholesale role with its own price list. Three plugins dominate this space: B2BKing, Wholesale Suite, and WooCommerce.com's own B2B Pricing extension.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">B2BKing creates custom user roles, such as wholesale, distributor, or VIP. It lets you set group-specific price rules and hidden catalogs from one settings screen. Wholesale Suite takes a narrower approach.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">It adds a single "Wholesale Customer" role with its own price field per product. This is simpler to configure but less flexible for multiple B2B tiers.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">WooCommerce.com's native extension integrates with your existing customer roles. It fits well if you already use WooCommerce.com extensions.</p>

<h3 style="color:#43627f;font-size:22px;">Which plugin should you pick for customer groups</h3>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Pick B2BKing if you need multiple buyer tiers, like distributor, retailer, and VIP, each with its own price list. Pick Wholesale Suite if you have one wholesale tier and want the fastest path to a working price difference.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Pick the native extension if you already pay for WooCommerce.com extensions and want first-party support.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Plugin conflicts are common once two or three of these run together. Most stores configuring this for the first time bring in a <a href="https://virtina.com/platforms/woocommerce-development-services/" style="outline: none;">WooCommerce development company</a> to test the combination before launch.</p>

<h3 style="color:#43627f;font-size:22px;">How new accounts get assigned to a group</h3>
<p dir="ltr" style="font-size:16px;line-height:1.75;">New B2B accounts get assigned to a group through a registration form, an admin approval step, or both together. B2BKing supports a gated registration flow. A new account sits in pending status until staff approve it and assign a role.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Wholesale Suite is simpler here too. New users pick "Wholesale Customer" at signup, then wait for manual approval before the wholesale price shows.</p>

<h3 style="color:#43627f;font-size:22px;">Setting the actual role-based price</h3>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Once a plugin is active, role-based pricing works the same way across all three. You set a base retail price on the product.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Then add a second price field or discount tied to the buyer's role. A distributor role might see 20% off, while a VIP retailer might see a flat unit price.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">The discount applies the moment that buyer logs in, before checkout. This is also the layer where role-based pricing connects to your broader integration work. Most ERPs store customer-specific price lists that need to sync into whichever plugin you choose.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Price lists often live in a separate system. <a href="https://virtina.com/woocommerce-erp-integration/" style="outline: none;">ERP integration</a> keeps that pricing data and your records in sync.</p>
</div>

<!-- SECTION: tiered and quantity-based pricing -->
<div style="background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));border-radius:20px;padding:30px;margin:0 0 28px 0;">
<h2 id="tiered-pricing-rules" style="color:#43627f;font-size:30px;">How do tiered and quantity-based pricing rules work in WooCommerce?</h2>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Tiered and quantity-based pricing rules in WooCommerce work by attaching discount breakpoints to a product or category. The unit price drops as order quantity rises. A buyer ordering 10 units pays one price, and the same buyer ordering 100 units pays less per unit.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">B2BKing and Wholesale Suite both support this through a rules table inside the product or a global rule set. You define a quantity range and a price or percentage discount for that range.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">A typical setup looks like this: 1 to 9 units at full price, 10 to 49 units at 8% off. 50 to 99 units land at 15% off, and 100-plus units at 22% off.</p>

<h3 style="color:#43627f;font-size:22px;">Setting up a tier table step by step</h3>
<ul style="list-style:none;padding-left:4px;margin:8px 0 16px 0;">
<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>1. Install the plugin.</strong> Install your chosen pricing plugin and activate the tiered pricing module.</span></li>
<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>2. Open the right scope.</strong> Open the product, or the category for bulk rule application, that you want to configure.</span></li>
<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>3. Add a rule row.</strong> Add a new pricing rule row for each quantity break point.</span></li>
<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>4. Enter the break point.</strong> Enter the minimum quantity and a fixed price or percentage discount per row.</span></li>
<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>5. Assign the audience.</strong> Assign the rule to a specific customer group, or leave it open to all B2B buyers.</span></li>
<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>6. Test the math.</strong> Save the rule, then test the cart at each tier to confirm the numbers are right.</span></li>
</ul>
</div>

<!-- BODY IMAGE 1 -->
<!-- BODY IMAGE PLACEHOLDER
Dimensions required: 670x352 px exactly
Subject: close-up of a laptop screen displaying a WooCommerce tiered pricing rules table with quantity breakpoints and percentage discounts (keyword: "working typing computer desk")
Alt text (80-150 chars): "Laptop screen showing WooCommerce tiered pricing rules table with quantity breakpoints and percentage discounts"
-->

<div style="background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));border-radius:20px;padding:30px;margin:0 0 28px 0;">
<h3 style="color:#43627f;font-size:22px;">Category-level versus product-level tiers</h3>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Category-level tiers save setup time when every product in a line shares the same discount structure. Product-level tiers give you precision when certain SKUs carry tighter margins.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Most manufacturers and distributors mix both: a baseline category discount, with product-level overrides on high-margin or low-stock items. Quantity discounts, volume pricing, and wholesale pricing are the terms you'll see most in these plugin settings.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">If your store also runs a <a href="https://virtina.com/b2b-ecommerce-marketplace-on-woocommerce/" style="outline: none;">B2B eCommerce marketplace</a> with multiple seller catalogs, tier rules need to apply consistently. Cover every vendor's products, not just your own.</p>

<h3 style="color:#43627f;font-size:22px;">A worked example with real numbers</h3>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Picture a distributor selling industrial fasteners at $2.50 per unit retail. A B2BKing tier rule might set three breakpoints. 50 to 199 units at $2.20, 200 to 499 units at $1.95, and 500-plus units at $1.70.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">A buyer ordering 600 units pays $1,020 instead of $1,500 at the retail rate. That's the kind of math your tier table needs to model correctly before launch.</p>
</div>

<!-- SECTION: minimum order quantity -->
<div style="background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));border-radius:20px;padding:30px;margin:0 0 28px 0;">
<h2 id="minimum-order-quantity" style="color:#43627f;font-size:30px;">How do you enforce minimum order quantities on a WooCommerce store?</h2>
<p dir="ltr" style="font-size:16px;line-height:1.75;">You enforce minimum order quantities on a WooCommerce store with a plugin. WooCommerce core has no built-in MOQ field on the product or cart level. B2BKing and Wholesale Suite both include MOQ settings, and smaller MOQ-only plugins exist too.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">The setting itself is simple once a plugin is active. You define a minimum unit count on the product, for example a SKU that cannot be ordered below 25 units. The plugin then blocks checkout until the cart meets that threshold.</p>

<h3 style="color:#43627f;font-size:22px;">MOQ at the product level versus the order level</h3>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Product-level MOQ stops a buyer from ordering fewer than a set number of units of one SKU. Order-level MOQ is a separate setting. It blocks checkout unless the full cart reaches a minimum dollar amount, regardless of which products fill it.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Distributors selling individual SKUs in bulk usually need product-level MOQ. Manufacturers who want every order to clear a freight-efficient threshold need order-level MOQ. Sometimes both rules run together.</p>

<h3 style="color:#43627f;font-size:22px;">What happens when a buyer falls short</h3>
<p dir="ltr" style="font-size:16px;line-height:1.75;">A good MOQ setup doesn't just block the buyer with an error message. It shows the exact quantity needed to reach the minimum and lets them adjust the cart in place. Generic error messages with no path forward are a common cause of cart abandonment here.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Most plugins let you customize this message per product or per customer group. A distributor account might see "add 15 more units to reach your 50-unit minimum." A guest browsing the same SKU sees a generic notice instead.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">That small difference in messaging often decides whether the buyer finishes the order or abandons the cart.</p>
</div>

<!-- SECTION: quote request workflows -->
<div style="background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));border-radius:20px;padding:30px;margin:0 0 28px 0;">
<h2 id="quote-request-workflows" style="color:#43627f;font-size:30px;">What is a WooCommerce quote request workflow and when do you need one?</h2>
<p dir="ltr" style="font-size:16px;line-height:1.75;">A WooCommerce quote request workflow replaces direct checkout with a request-for-quote form. You need one whenever pricing depends on negotiation, custom specs, or freight that can't be calculated automatically.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Industrial buyers and custom-spec manufacturers rarely want to pay instantly online. They want a human-reviewed quote first.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">B2BKing includes a built-in RFQ module. It converts specific products, categories, or entire customer groups to quote-only instead of buy-now.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Wholesale Suite has lighter quote functionality. Some stores pair WooCommerce with a dedicated chat-based quoting layer for faster turnaround.</p>

<h3 style="color:#43627f;font-size:22px;">Configuring which products go through RFQ</h3>
<p dir="ltr" style="font-size:16px;line-height:1.75;">You can run RFQ at three different scopes. The narrowest is a single product flagged quote-only. The widest is a customer group rule that hides the buy button across the board.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Most B2B stores mix all three scopes. Custom or high-cost items go to quote, while standard SKUs stay on direct checkout.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">If your sales team is buried in manual quote requests, a <a href="https://virtina.com/b2b-quote-chatbot/" style="outline: none;">B2B quoting tool</a> can route and qualify requests first. That cuts response time from days to minutes.</p>

<h3 style="color:#43627f;font-size:22px;">What a quote request form should capture</h3>
<p dir="ltr" style="font-size:16px;line-height:1.75;">A working RFQ form captures more than name and email. It needs the requested SKU and quantity, the buyer's account ID, any custom specification notes, and a target delivery date.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Missing any of these fields costs you time. Your sales team spends the first email just asking for information the form should have collected.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Pre-filling fields with account data speeds this up further. A logged-in buyer's form can pull their company name, shipping address, and price tier automatically. That leaves only the SKU, quantity, and notes to fill in by hand.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Some B2B buyers also want self-service order history and reorder tools alongside the quote option. Virtina's guide to a <a href="https://virtina.com/woocommerce-b2b-customer-portal/" style="outline: none;">WooCommerce B2B customer portal</a> covers that account-side experience in more depth.</p>
</div>

<!-- SECTION: tax exemption handling -->
<div style="background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));border-radius:20px;padding:30px;margin:0 0 28px 0;">
<h2 id="tax-exemption-handling" style="color:#43627f;font-size:30px;">How do you handle tax exemption certificates for B2B buyers in WooCommerce?</h2>
<p dir="ltr" style="font-size:16px;line-height:1.75;">You handle tax exemption certificates for B2B buyers in WooCommerce by attaching an exemption flag to the account. That flag connects to your tax calculation plugin, so qualified buyers are never charged sales tax at checkout.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">This requires either a tax plugin like TaxJar or Avalara, or the exemption fields built into B2BKing. The certificate itself still needs to be collected and verified outside the cart.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">This usually happens through document upload during registration or a manual approval step. The plugin's job is enforcing the exemption at checkout, not validating the certificate's legitimacy.</p>

<h3 style="color:#43627f;font-size:22px;">Where the certificate upload should live</h3>
<p dir="ltr" style="font-size:16px;line-height:1.75;">The cleanest setup puts certificate upload on the registration form, gated behind admin approval before the account can order. This keeps unverified buyers from checking out tax-free while the certificate sits unreviewed in an inbox.</p>

<h3 style="color:#43627f;font-size:22px;">Common tax exemption mistakes</h3>
<p dir="ltr" style="font-size:16px;line-height:1.75;">The most frequent failure is applying the exemption without re-verifying expiration dates. Exemption certificates expire, often annually, and a static flag on an account doesn't track that.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Build a recurring reminder into your approval workflow instead of a one-time checkbox.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Tax exemption and payment terms often get configured by the same team in the same sprint. Both affect what a buyer sees at checkout. If your store still defaults every account to pay-now, Virtina's guide to <a href="https://virtina.com/woocommerce-b2b-net-payment-terms/" style="outline: none;">WooCommerce net payment terms</a> covers that separately.</p>
</div>

<!-- SECTION: catalog visibility rules -->
<div style="background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));border-radius:20px;padding:30px;margin:0 0 28px 0;">
<h2 id="catalog-visibility-rules" style="color:#43627f;font-size:30px;">What catalog visibility rules should a WooCommerce B2B store use?</h2>
<p dir="ltr" style="font-size:16px;line-height:1.75;">A WooCommerce B2B store should use catalog visibility rules that hide prices, the buy button, or the entire catalog. These rules apply to guests and non-approved accounts.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">WooCommerce core supports a basic version natively, through Catalog Visibility settings per product. Full B2B control, including a login wall over the whole store, still needs a plugin like B2BKing.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Native WooCommerce lets you mark products as hidden, search-results-only, or shop-only. This controls where a product appears, but it doesn't touch pricing visibility or require login.</p>

<h3 style="color:#43627f;font-size:22px;">Three levels of catalog restriction</h3>
<p dir="ltr" style="font-size:16px;line-height:1.75;">The lightest restriction hides prices and the buy button from guests while still showing products and descriptions. This is useful for SEO, since pages stay indexable.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">The middle restriction requires login to see any price, showing guests a request-access message instead. The strictest restriction hides the entire catalog behind a login wall, blocking even product browsing until an account is approved.</p>

<h3 style="color:#43627f;font-size:22px;">Picking the right level for your store</h3>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Choose price-hiding-only if organic search traffic and product discoverability matter to your funnel. Choose full catalog gating if your pricing is customer-specific enough to create channel conflict if shown publicly.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Most manufacturers land in the middle: visible catalog, hidden price, login required to see numbers.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">A properly configured catalog with clear visibility rules also helps AI shopping agents understand what you sell. That benefit is covered in more depth in Virtina's guide on <a href="https://virtina.com/ecommerce-store-agent-ready/" style="outline: none;">building a store AI shopping agents can read</a>.</p>
</div>

<!-- BODY IMAGE 2 -->
<!-- BODY IMAGE PLACEHOLDER
Dimensions required: 670x352 px exactly
Subject: WooCommerce store admin screen showing catalog visibility settings with a hidden price toggle for guest users (keyword: "ecommerce dashboard laptop")
Alt text (80-150 chars): "WooCommerce admin screen showing catalog visibility settings with hidden price toggle for guest user accounts"
-->

<!-- SECTION: plugin comparison -->
<div style="background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));border-radius:20px;padding:30px;margin:0 0 28px 0;">
<h2 id="plugin-comparison" style="color:#43627f;font-size:30px;">Which B2B pricing plugin should you choose: B2BKing, Wholesale Suite, or native B2B Pricing?</h2>
<p dir="ltr" style="font-size:16px;line-height:1.75;">The right B2B pricing plugin depends on your buyer tiers and how much you want in one place. B2BKing covers the most ground in a single plugin. Wholesale Suite is the simplest path for one wholesale tier.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">The native extension fits stores already committed to WooCommerce.com. Price is a secondary factor worth weighing too.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">B2BKing and Wholesale Suite both carry one-time or annual license costs that scale with site count. The native extension bundles into your existing WooCommerce.com subscription. That can simplify procurement for finance teams that prefer fewer vendors.</p>

<table style="border-collapse:collapse;width:100%;font-size:15px;margin:20px 0;">
<thead>
<tr>
<th style="background:#43627f;color:#fff;padding:10px 14px;text-align:left;">Plugin</th>
<th style="background:#43627f;color:#fff;padding:10px 14px;text-align:left;">Pricing model support</th>
<th style="background:#43627f;color:#fff;padding:10px 14px;text-align:left;">MOQ support</th>
<th style="background:#43627f;color:#fff;padding:10px 14px;text-align:left;">Quote/RFQ support</th>
<th style="background:#43627f;color:#fff;padding:10px 14px;text-align:left;">Best for</th>
</tr>
</thead>
<tbody>
<tr style="background:#f4f6f9;">
<td style="padding:10px 14px;border-bottom:1px solid #dde0e6;">B2BKing</td>
<td style="padding:10px 14px;border-bottom:1px solid #dde0e6;">Role-based, tiered, and quantity pricing across multiple buyer tiers</td>
<td style="padding:10px 14px;border-bottom:1px solid #dde0e6;">Yes, product and order level</td>
<td style="padding:10px 14px;border-bottom:1px solid #dde0e6;">Yes, built-in RFQ module with group-level rules</td>
<td style="padding:10px 14px;border-bottom:1px solid #dde0e6;">Multi-tier stores needing pricing, MOQ, and quoting in one plugin</td>
</tr>
<tr style="background:#ffffff;">
<td style="padding:10px 14px;border-bottom:1px solid #dde0e6;">Wholesale Suite</td>
<td style="padding:10px 14px;border-bottom:1px solid #dde0e6;">Single wholesale role with per-product pricing and basic tiers</td>
<td style="padding:10px 14px;border-bottom:1px solid #dde0e6;">Yes, product level</td>
<td style="padding:10px 14px;border-bottom:1px solid #dde0e6;">Limited, lighter quote functionality</td>
<td style="padding:10px 14px;border-bottom:1px solid #dde0e6;">Stores with one wholesale tier wanting the simplest setup</td>
</tr>
<tr style="background:#f4f6f9;">
<td style="padding:10px 14px;border-bottom:1px solid #dde0e6;">Native B2B Pricing extension</td>
<td style="padding:10px 14px;border-bottom:1px solid #dde0e6;">Role-based pricing tied to existing WooCommerce customer roles</td>
<td style="padding:10px 14px;border-bottom:1px solid #dde0e6;">No native MOQ field</td>
<td style="padding:10px 14px;border-bottom:1px solid #dde0e6;">No built-in RFQ</td>
<td style="padding:10px 14px;border-bottom:1px solid #dde0e6;">Stores already on WooCommerce.com wanting first-party integration</td>
</tr>
</tbody>
</table>
<p dir="ltr" style="font-size:14px;line-height:1.6;color:#6e6e6e;margin:4px 0 16px 0;">Plugin capabilities compared as of June 2026, based on each vendor's published feature documentation.</p>

<p dir="ltr" style="font-size:16px;line-height:1.75;">Whichever plugin you choose, configuration mistakes here tend to surface later as performance problems. Stacking three or four plugins to cover pricing, MOQ, and quoting is a common cause of slow checkout.</p>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Virtina's <a href="https://virtina.com/woocommerce-b2b-performance-fix/" style="outline: none;">WooCommerce B2B performance guide</a> covers those issues directly. If you'd rather skip the trial-and-error, you can <a href="https://virtina.com/get-in-touch/" style="outline: none;">talk to Virtina's team</a> about configuring these settings end to end.</p>
</div>

<!-- PAA BLOCK (Template H) -->
<div style="background:linear-gradient(rgba(241,243,250,0.5),rgba(241,243,250,0.5));border-radius:20px;padding:30px;margin:0 0 28px 0;">
<h2 id="people-also-ask" style="color:#43627f;font-size:30px;">People also ask</h2>
<h3 style="color:#43627f;font-size:22px;">Can WooCommerce hide prices from guests natively?</h3>
<p dir="ltr" style="font-size:16px;line-height:1.75;">WooCommerce's native Catalog Visibility setting controls where a product appears, not whether its price shows. Hiding prices from guests requires a plugin like B2BKing or a role-based pricing extension on top of core WooCommerce.</p>
<h3 style="color:#43627f;font-size:22px;">Do you need a plugin for minimum order quantities?</h3>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Yes. WooCommerce core has no MOQ field on products or cart rules. Enforcing a minimum unit count requires a dedicated plugin such as B2BKing or Wholesale Suite.</p>
<h3 style="color:#43627f;font-size:22px;">Can one WooCommerce store run both retail and B2B pricing at once?</h3>
<p dir="ltr" style="font-size:16px;line-height:1.75;">Yes, and this is the most common setup among manufacturing and distribution clients. Role-based pricing plugins show retail prices to guests while applying B2B discounts only to approved, logged-in accounts.</p>
</div>

<!-- CONCLUSION BLOCK (Template I) -->
<div style="background:#00d5c0;border-radius:20px;padding:30px;margin:0 0 28px 0;">
<h2 id="conclusion" style="color:#ffffff;font-size:30px;">Conclusion</h2>
<p style="color:#ffffff;font-size:16px;line-height:1.75;">WooCommerce can run a serious B2B operation, but only once you configure it deliberately. That means customer groups, tiered pricing, MOQ, quote requests, tax exemption, and catalog visibility, all six. None of these arrive working out of the box.</p>
<p style="color:#ffffff;font-size:16px;line-height:1.75;">Stacking the wrong plugin combination creates more cleanup work than starting with the right one. Start with the plugin decision, then work through each configuration area in the order this guide covers it.</p>
<p style="color:#ffffff;font-size:16px;line-height:1.75;">If your team would rather hand this off, Virtina can configure these settings end to end. That includes connecting them to your existing pricing data and ERP.</p>
</div>

<!-- FAQ ACCORDION (Template J) -->
<h2 id="faq" style="color:#43627f;font-size:30px;">Frequently asked questions</h2>
<div>
<details class="vfaq" style="background:transparent;margin-top:7px;"><summary style="cursor:pointer;padding:17px;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:12px;background:rgba(245,245,245,0.5);"><span style="font-size:16px;font-weight:600;color:#43627f;line-height:2;flex:1;">Which plugin should you use for B2B pricing on WooCommerce?</span><svg viewBox="0 0 24 24" width="17" height="17" style="fill:#50565f;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg"><path d="M16,12A2,2 0 0,1 18,10A2,2 0 0,1 20,12A2,2 0 0,1 18,14A2,2 0 0,1 16,12M8,12A2,2 0 0,1 10,10A2,2 0 0,1 12,12A2,2 0 0,1 10,14A2,2 0 0,1 8,12M0,12A2,2 0 0,1 2,10A2,2 0 0,1 4,12A2,2 0 0,1 2,14A2,2 0 0,1 0,12Z"/></svg></summary><div class="vfaq-answer" style="padding:30px 22px;background:#fff;"><p dir="ltr" style="font-size:16px;line-height:1.75;">Use B2BKing if you need multiple buyer tiers with different pricing, MOQ, and quote workflows. Use Wholesale Suite if you only need one wholesale tier. Use the native extension if you already run WooCommerce.com extensions.</p></div></details>
<details class="vfaq" style="background:transparent;margin-top:7px;"><summary style="cursor:pointer;padding:17px;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:12px;background:rgba(245,245,245,0.5);"><span style="font-size:16px;font-weight:600;color:#43627f;line-height:2;flex:1;">Can WooCommerce hide prices from guests natively?</span><svg viewBox="0 0 24 24" width="17" height="17" style="fill:#50565f;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg"><path d="M16,12A2,2 0 0,1 18,10A2,2 0 0,1 20,12A2,2 0 0,1 18,14A2,2 0 0,1 16,12M8,12A2,2 0 0,1 10,10A2,2 0 0,1 12,12A2,2 0 0,1 10,14A2,2 0 0,1 8,12M0,12A2,2 0 0,1 2,10A2,2 0 0,1 4,12A2,2 0 0,1 2,14A2,2 0 0,1 0,12Z"/></svg></summary><div class="vfaq-answer" style="padding:30px 22px;background:#fff;"><p dir="ltr" style="font-size:16px;line-height:1.75;">No. Native Catalog Visibility settings control where a product appears, not whether the price displays. Hiding prices from guests requires a B2B plugin layered on top of core WooCommerce.</p></div></details>
<details class="vfaq" style="background:transparent;margin-top:7px;"><summary style="cursor:pointer;padding:17px;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:12px;background:rgba(245,245,245,0.5);"><span style="font-size:16px;font-weight:600;color:#43627f;line-height:2;flex:1;">Do you need a plugin for minimum order quantities?</span><svg viewBox="0 0 24 24" width="17" height="17" style="fill:#50565f;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg"><path d="M16,12A2,2 0 0,1 18,10A2,2 0 0,1 20,12A2,2 0 0,1 18,14A2,2 0 0,1 16,12M8,12A2,2 0 0,1 10,10A2,2 0 0,1 12,12A2,2 0 0,1 10,14A2,2 0 0,1 8,12M0,12A2,2 0 0,1 2,10A2,2 0 0,1 4,12A2,2 0 0,1 2,14A2,2 0 0,1 0,12Z"/></svg></summary><div class="vfaq-answer" style="padding:30px 22px;background:#fff;"><p dir="ltr" style="font-size:16px;line-height:1.75;">Yes, WooCommerce has no built-in MOQ field. You need a plugin such as B2BKing or Wholesale Suite. It enforces minimum unit counts at the product or order level.</p></div></details>
<details class="vfaq" style="background:transparent;margin-top:7px;"><summary style="cursor:pointer;padding:17px;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:12px;background:rgba(245,245,245,0.5);"><span style="font-size:16px;font-weight:600;color:#43627f;line-height:2;flex:1;">How do tiered pricing rules differ from a flat wholesale discount?</span><svg viewBox="0 0 24 24" width="17" height="17" style="fill:#50565f;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg"><path d="M16,12A2,2 0 0,1 18,10A2,2 0 0,1 20,12A2,2 0 0,1 18,14A2,2 0 0,1 16,12M8,12A2,2 0 0,1 10,10A2,2 0 0,1 12,12A2,2 0 0,1 10,14A2,2 0 0,1 8,12M0,12A2,2 0 0,1 2,10A2,2 0 0,1 4,12A2,2 0 0,1 2,14A2,2 0 0,1 0,12Z"/></svg></summary><div class="vfaq-answer" style="padding:30px 22px;background:#fff;"><p dir="ltr" style="font-size:16px;line-height:1.75;">A flat wholesale discount applies one percentage off regardless of order size. Tiered pricing applies different discounts at different quantity breakpoints. A 10-unit order and a 100-unit order get different per-unit prices.</p></div></details>
<details class="vfaq" style="background:transparent;margin-top:7px;"><summary style="cursor:pointer;padding:17px;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:12px;background:rgba(245,245,245,0.5);"><span style="font-size:16px;font-weight:600;color:#43627f;line-height:2;flex:1;">What is the difference between a quote request workflow and standard checkout?</span><svg viewBox="0 0 24 24" width="17" height="17" style="fill:#50565f;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg"><path d="M16,12A2,2 0 0,1 18,10A2,2 0 0,1 20,12A2,2 0 0,1 18,14A2,2 0 0,1 16,12M8,12A2,2 0 0,1 10,10A2,2 0 0,1 12,12A2,2 0 0,1 10,14A2,2 0 0,1 8,12M0,12A2,2 0 0,1 2,10A2,2 0 0,1 4,12A2,2 0 0,1 2,14A2,2 0 0,1 0,12Z"/></svg></summary><div class="vfaq-answer" style="padding:30px 22px;background:#fff;"><p dir="ltr" style="font-size:16px;line-height:1.75;">Standard checkout lets a buyer pay immediately at a fixed, calculated price. A quote request workflow routes the order to a human for custom pricing or freight calculation first. Payment happens only after that review.</p></div></details>
<details class="vfaq" style="background:transparent;margin-top:7px;"><summary style="cursor:pointer;padding:17px;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:12px;background:rgba(245,245,245,0.5);"><span style="font-size:16px;font-weight:600;color:#43627f;line-height:2;flex:1;">How do you verify a tax exemption certificate is still valid?</span><svg viewBox="0 0 24 24" width="17" height="17" style="fill:#50565f;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg"><path d="M16,12A2,2 0 0,1 18,10A2,2 0 0,1 20,12A2,2 0 0,1 18,14A2,2 0 0,1 16,12M8,12A2,2 0 0,1 10,10A2,2 0 0,1 12,12A2,2 0 0,1 10,14A2,2 0 0,1 8,12M0,12A2,2 0 0,1 2,10A2,2 0 0,1 4,12A2,2 0 0,1 2,14A2,2 0 0,1 0,12Z"/></svg></summary><div class="vfaq-answer" style="padding:30px 22px;background:#fff;"><p dir="ltr" style="font-size:16px;line-height:1.75;">The plugin itself doesn't verify legitimacy. Build a manual review step into account approval. Set a recurring reminder to recheck expiration dates, since most exemption certificates expire annually.</p></div></details>
<details class="vfaq" style="background:transparent;margin-top:7px;"><summary style="cursor:pointer;padding:17px;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:12px;background:rgba(245,245,245,0.5);"><span style="font-size:16px;font-weight:600;color:#43627f;line-height:2;flex:1;">Should you hide your entire catalog or just hide prices?</span><svg viewBox="0 0 24 24" width="17" height="17" style="fill:#50565f;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg"><path d="M16,12A2,2 0 0,1 18,10A2,2 0 0,1 20,12A2,2 0 0,1 18,14A2,2 0 0,1 16,12M8,12A2,2 0 0,1 10,10A2,2 0 0,1 12,12A2,2 0 0,1 10,14A2,2 0 0,1 8,12M0,12A2,2 0 0,1 2,10A2,2 0 0,1 4,12A2,2 0 0,1 2,14A2,2 0 0,1 0,12Z"/></svg></summary><div class="vfaq-answer" style="padding:30px 22px;background:#fff;"><p dir="ltr" style="font-size:16px;line-height:1.75;">Hide prices only if product discoverability and SEO matter to your funnel. Hide the entire catalog if your pricing is customer-specific enough to create channel conflict if shown publicly.</p></div></details>
<details class="vfaq" style="background:transparent;margin-top:7px;"><summary style="cursor:pointer;padding:17px;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:12px;background:rgba(245,245,245,0.5);"><span style="font-size:16px;font-weight:600;color:#43627f;line-height:2;flex:1;">Does WooCommerce B2B configuration affect how AI shopping tools read your store?</span><svg viewBox="0 0 24 24" width="17" height="17" style="fill:#50565f;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg"><path d="M16,12A2,2 0 0,1 18,10A2,2 0 0,1 20,12A2,2 0 0,1 18,14A2,2 0 0,1 16,12M8,12A2,2 0 0,1 10,10A2,2 0 0,1 12,12A2,2 0 0,1 10,14A2,2 0 0,1 8,12M0,12A2,2 0 0,1 2,10A2,2 0 0,1 4,12A2,2 0 0,1 2,14A2,2 0 0,1 0,12Z"/></svg></summary><div class="vfaq-answer" style="padding:30px 22px;background:#fff;"><p dir="ltr" style="font-size:16px;line-height:1.75;">Yes. Clear, consistent customer group and catalog rules make it easier for AI shopping agents to understand what you sell. That topic is covered in Virtina's guide on building an AI-agent-ready store.</p></div></details>
</div>

<!-- AUTHOR BIO (Template K) -->
<p dir="ltr" style="font-size:16px;line-height:1.75;"><strong>Gigi JK</strong> is the founder of Virtina, an eCommerce solutions partner. Virtina has helped 1,000+ B2B and B2C brands strategize, optimize, and solve problems across WooCommerce, Magento, BigCommerce, and Shopify. Gigi specializes in B2B configuration, replatforming, and performance fixes for manufacturers, distributors, and wholesalers.</p>
