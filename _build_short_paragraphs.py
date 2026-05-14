import requests, base64, re
import urllib3
urllib3.disable_warnings()

username = 'anujith'
password = 'Mibz 1h3E jWRi bfJs WAXZ rwrM'
creds = base64.b64encode(f'{username}:{password}'.encode()).decode()
headers = {'Authorization': f'Basic {creds}', 'Content-Type': 'application/json'}

# ── helpers ────────────────────────────────────────────────
TOC_LI = '<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;"><svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span><a href="{anchor}" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">{text}</a></li>'
def toc_li(anchor, text): return TOC_LI.format(anchor=anchor, text=text)

IMG_W = '<span data-image-caption="" data-image-display="block" data-image-id="{mid}" data-image-size="full" data-init-width="670" data-init-height="352" class="tve_image_frame" style="width:670px;"><img class="tve_image wp-image-{mid}" alt="{alt}" width="670" height="352" src="{src}" data-id="{mid}" style="width:670px;"/></span>'
def img(mid, alt, src): return IMG_W.format(mid=mid, alt=alt, src=src)

S  = 'font-size:16px;line-height:1.75;'
def p(*sentences):   return '\n'.join(f'<p dir="ltr" style="{S}">{s}</p>' for s in sentences)
def pw(*sentences):  return '\n'.join(f'<p style="color:#ffffff;{S}">{s}</p>' for s in sentences)
def h2(id_, t):      return f'<h2 id="{id_}" style="color:#43627f;font-size:30px;">{t}</h2>'
def h3(t):           return f'<h3 style="color:#43627f;font-size:23px;">{t}</h3>'
def il(url, t):      return f'<a href="{url}" style="outline: none;">{t}</a>'
def el(url, t):      return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{t}</a>'

def bul(label, body):
    c = '<span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span>'
    t = f'<span style="font-size:16px;line-height:1.75;color:#2d3e50;"><strong>{label}</strong> {body}</span>'
    return f'<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;">{c}{t}</li>'
def ul(items): return '<ul style="list-style:none;padding-left:4px;margin:8px 0 16px 0;">\n' + '\n'.join(items) + '\n</ul>'

def wrap(bg, inner): return f'<div style="background:{bg};border-radius:20px;padding:30px;margin:0 0 28px 0;">{inner}\n</div>'
BG_TEAL  = 'linear-gradient(rgba(0,213,192,0.28),rgba(0,213,192,0.28))'
BG_LIGHT = 'linear-gradient(rgba(241,243,250,0.5),rgba(241,243,250,0.5))'
BG_BLUE  = 'linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13))'
BG_SOLID = '#00d5c0'

FAQ_T = '<details class="vfaq" style="background:transparent;margin-top:7px;"><summary style="cursor:pointer;padding:17px;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:12px;background:rgba(245,245,245,0.5);"><span style="font-size:16px;font-weight:600;color:#43627f;line-height:2;flex:1;">{q}</span><svg viewBox="0 0 24 24" width="17" height="17" style="fill:#50565f;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg"><path d="M16,12A2,2 0 0,1 18,10A2,2 0 0,1 20,12A2,2 0 0,1 18,14A2,2 0 0,1 16,12M8,12A2,2 0 0,1 10,10A2,2 0 0,1 12,12A2,2 0 0,1 10,14A2,2 0 0,1 8,12M0,12A2,2 0 0,1 2,10A2,2 0 0,1 4,12A2,2 0 0,1 2,14A2,2 0 0,1 0,12Z"/></svg></summary><div class="vfaq-answer" style="padding:30px 22px;background:#fff;">{a}</div></details>'
def faq(q, a): return FAQ_T.format(q=q, a=a)

# ── LINKS ──────────────────────────────────────────────────
L = {
    'woo_guide'    : il('https://virtina.com/woocommerce-guide/', 'what WooCommerce offers'),
    'b2b_perf'     : il('https://virtina.com/woocommerce-b2b-performance-fix/', 'WooCommerce B2B performance'),
    'checklist'    : il('https://virtina.com/ecommerce-website-migration-checklist/', 'migration checklist'),
    'hpos'         : il('https://virtina.com/woocommerce-hpos-migration/', 'WooCommerce order storage'),
    'plugins'      : il('https://virtina.com/woocommerce-issues-killing-conversions/', 'plugin conflicts'),
    'woo_dev'      : il('https://virtina.com/woocommerce-development/', 'WooCommerce developer'),
    'woo_platform' : il('https://virtina.com/woocommerce/', 'WooCommerce platform'),
    'woo_seo'      : il('https://virtina.com/woocommerce-seo-made-easy/', 'WooCommerce SEO'),
    'b2b'          : il('https://virtina.com/b2b-ecommerce/', 'B2B eCommerce on WooCommerce'),
    'integrations' : il('https://virtina.com/ecommerce-integrations/', 'custom integrations'),
    'storeleads'   : el('https://storeleads.app/reports/volusion', "StoreLeads' 2026 tracking data"),
    'steva'        : el('https://steva.co/volusion-review/', 'compromised in a single breach, with estimated damages of $133.89 million'),
}

# ══════════════════════════════════════════════════════════
# CONTENT — max 2-3 sentences per <p> tag
# ══════════════════════════════════════════════════════════
parts = []

# ── SUMMARY ────────────────────────────────────────────────
parts.append(wrap(BG_TEAL,
    '<h2 dir="ltr" style="color:#43627f;font-size:30px;">Summary</h2>\n' +
    p('You opened a billing notification one morning.') +
    p('Your Volusion plan had upgraded itself overnight. The price jumped from $35 to $79.') +
    p('No email. No warning. That moment is why Volusion merchants leave.') +
    p('This article covers what is actually happening on Volusion and what migrating to WooCommerce genuinely involves. Including the parts that are harder than the marketing makes them sound.')
))

# ── INTRODUCTION ───────────────────────────────────────────
parts.append(wrap(BG_LIGHT,
    '<h2 style="color:#43627f;font-size:30px;">Introduction</h2>\n' +
    p('The billing surprise is not a bug.') +
    p("Volusion's Personal plan caps annual sales at $50,000. The Professional plan caps at $100,000.") +
    p('Cross either limit and your account upgrades automatically. No warning email. No consent required.') +
    p('Merchants have reported charges jumping 600% in a few weeks. Some have had revenue held during disputes.') +
    p('The pricing model does not grow with you. It extracts more from you as you grow.') +
    p("If you're reading this, you already know something is off. Maybe it's the billing. Maybe it's a missing integration.") +
    p("Maybe it's the question that started in 2020 when Volusion filed for Chapter 11: should my business be built on this?") +
    p("This piece is for that moment. When you want someone to be straight with you about what moving to WooCommerce actually takes.")
))

# ── TOC ────────────────────────────────────────────────────
toc_items = '\n'.join([
    toc_li('#walls',           'Why do Volusion merchants keep hitting a wall?'),
    toc_li('#decision',        'When does Volusion frustration turn into a decision to leave?'),
    toc_li('#migration',       'What does the migration to WooCommerce actually involve?'),
    toc_li('#what-you-gain',   'What does WooCommerce give you that Volusion cannot?'),
    toc_li('#people-also-ask', 'People also ask'),
    toc_li('#conclusion',      'Conclusion'),
    toc_li('#faq',             'Frequently asked questions'),
])
parts.append('<h3>Table of Contents</h3>\n<ul style="list-style:none!important;padding-left:0!important;margin:0 0 1.5em 0!important;">\n' + toc_items + '\n</ul>')

# ── SECTION 1: WALLS ───────────────────────────────────────
parts.append(wrap(BG_BLUE,
    h2('walls', 'Why do Volusion merchants keep hitting a wall?') + '\n' +
    p('Because the platform was built for small stores that stay small.') +
    p('When your store grows, the walls appear.') +
    p('The sales cap hits first. You pay a monthly fee expecting that to be your monthly fee.') +
    p(f'Then you cross $50,000 in annual sales. Volusion upgrades you to the Professional plan at $79 a month. No warning email.') +
    p(f'Cross $100,000 and you\'re on the Business tier at $299. Bandwidth overages add $7 per gigabyte on top.') +
    p(f'The plan price was never the real price. To understand {L["woo_guide"]}, you first need to see the full cost of staying on Volusion.') +
    p('Merchants describe charges that "just kept skyrocketing." Billing jumps hit without notice.') +
    img('42179', 'Online store owner frustrated at computer screen after discovering unexpected eCommerce platform billing charges and automatic plan upgrades', 'https://virtina.com/wp-content/uploads/2026/05/volusion-woocommerce-migration-section1-670x352-2.jpg') + '\n' +
    p("The integration ceiling is a different kind of frustration. Volusion's app marketplace has roughly 80 apps.") +
    p('One developer reviewing the platform called the API something no agency wants to build on.') +
    p('The proprietary structure makes custom work prohibitively expensive.') +
    p("When you need a tool Volusion doesn't support and no developer will build it, you're stuck.") +
    p("For a growing store, that's not a minor inconvenience. It's a ceiling.") +
    p('The SEO picture is harder than it looks from inside the platform.') +
    p('Volusion has no native blogging capability. That cuts off content-driven organic traffic entirely.') +
    p('URL canonicalization issues confuse crawlers. Schema markup support is limited.') +
    p("These are structural problems that are hard to diagnose until you've left and seen what's possible elsewhere.") +
    p('For B2B merchants, the picture is worse.') +
    p('Volusion has no native tiered pricing, no customer roles, and no quote workflows.') +
    p(f'Wholesale operations need customer-specific pricing and quote request tools. Volusion has no path forward for either.') +
    p(f'The {L["b2b_perf"]} story is a separate conversation. But the contrast with Volusion starts here.') +
    p("These aren't feature gaps that might close in a future update. They are architectural limits of a platform that filed for Chapter 11 bankruptcy in June 2020.") +
    p(f'{L["storeleads"]} puts Volusion at 3,526 active stores as of May 2026.') +
    p("That's down from 13,889 in Q1 2020. A 75% contraction in six years.") +
    p("The platform is losing 40 stores for every 2 it gains.")
))

# ── SECTION 2: DECISION ────────────────────────────────────
parts.append(wrap(BG_BLUE,
    h2('decision', 'When does Volusion frustration turn into a decision to leave?') + '\n' +
    p('The decision rarely arrives as a sudden realization. It accumulates.') +
    p('One support ticket goes unanswered. One integration turns out not to exist.') +
    p('One billing surprise hits at a bad time.') +
    p('Then a competitor who migrated to WooCommerce six months ago starts outranking you.') +
    p("They're running automations you can't replicate. They're selling wholesale at prices you can't offer.") +
    p("That's when it tips.") +
    p('For many merchants, the 2020 bankruptcy was a quiet turning point.') +
    p('Volusion entered Chapter 11 in June 2020. The company continued operating and emerged from bankruptcy.') +
    p("But the question it raised doesn't go away. Do you want your business depending on this platform?") +
    p('Some merchants left immediately. Others stayed and are still running fine.') +
    p('"I stayed because leaving seemed hard" is different from "I stayed because the platform works for me."') +
    p("If you're reading this, you know which one applies to you.") +
    p('The 2019 data breach is a second data point.') +
    p(f'Credit card data from 239,000 customers across 6,589 Volusion stores was {L["steva"]}.') +
    p('The breach was not disclosed publicly for months.') +
    p("As a merchant, you were liable for your customers' experience. But the vulnerability was not in your control.") +
    p("On Volusion, your data lives on Volusion's servers.") +
    p("Full data ownership, where your database lives on your own host, is one of the things WooCommerce gives you.") +
    p('The decision to migrate is not a verdict on the years you spent on Volusion.') +
    p('The platform worked for a generation of small stores. The question is whether it fits where your business is going.') +
    p(f'A thorough {L["checklist"]} will save you from the most common missteps before you touch a single file.')
))

# ── SECTION 3: MIGRATION ───────────────────────────────────
migration_bullets = ul([
    bul('Store design.', 'Zero carries over. Your Volusion theme does not translate to WordPress. Treat this as a redesign from scratch.'),
    bul('Payment gateways.', "Stripe, PayPal, Square, and most major processors have official WooCommerce extensions. But you're setting them up from new API keys."),
    bul('Tax rules and shipping zones.', 'Both must be rebuilt inside WooCommerce. There is no shortcut.'),
    bul('SEO plugin and meta fields.', 'WooCommerce has no native meta field management. Install Yoast or RankMath before anything goes live.'),
])

parts.append(wrap(BG_BLUE,
    h2('migration', 'What does the migration to WooCommerce actually involve?') + '\n' +
    p('Most migration guides skip the hard parts. Here is what actually happens.') +
    p('It starts with an export. Go to Admin, then Data Management, then Export.') +
    p('Pull products, customers, and orders. Volusion produces CSV files.') +
    p('The data is there. But field names differ between Volusion and WooCommerce.') +
    p("Variant structures don't map one-to-one. Custom fields you built in Volusion have no automatic equivalent.") +
    p('Plan 1-3 days just for data cleanup.') +
    p('Document every live URL on your Volusion store before you start.') +
    p("That list becomes your redirect map. If you don't create it now, you'll rebuild it from memory later.") +
    p('WooCommerce is self-hosted. You are now choosing and managing your own server.') +
    p('A managed host like WP Engine, Kinsta, or Cloudways removes most of the burden. But the choice matters.') +
    p('WooCommerce performance lives and dies on your hosting environment.') +
    p("Get it wrong and you'll spend months debugging slowness that is actually a server problem.") +
    p("Don't treat hosting as a commodity decision.") +
    p('Migrate the data in a test run first.') +
    p('Tools like LitExtension and Cart2Cart start around $69 for basic catalogs.') +
    p('Run the test on a subset of products first. Check variant mapping, prices, and customer records.') +
    p("Fix what's wrong before running the full migration.") +
    p('Here is what does not migrate and requires a manual rebuild:') +
    migration_bullets + '\n' +
    p('The 301 redirect mapping is the highest-risk step. It is also the most commonly skipped.') +
    p('Volusion URLs follow one structure. WooCommerce URLs follow a different one.') +
    p('Every URL that changes needs a redirect pointing to its WooCommerce equivalent.') +
    p('Missing redirects mean Google treats the new pages as brand new.') +
    p('You start from zero on pages that took years to rank.') +
    p(f'Map every page before DNS cutover. Implement redirects before anything goes live.') +
    p(f'Check Google Search Console for crawl errors 4-6 weeks after launch. A dedicated {L["hpos"]} setup also needs attention if your store has a large order history.') +
    img('42180', 'eCommerce team planning platform migration steps on whiteboard, mapping out product data transfer and 301 redirect strategy', 'https://virtina.com/wp-content/uploads/2026/05/volusion-woocommerce-migration-section2-670x352-2.jpg') + '\n' +
    p("The honest part: WooCommerce is not simpler than Volusion. It's more powerful and more flexible.") +
    p('But those things come with more responsibility.') +
    p('Plugin selection has no guardrails. The 60,000-plugin library makes choosing wrong easy.') +
    p(f'{L["plugins"]} are a real operational headache.') +
    p('You are now responsible for hosting management, plugin updates, security patching, and performance tuning.') +
    p('None of those were your job on Volusion.') +
    p(f'For most stores, a {L["woo_dev"]} is not optional for redirects, theme build, and integration setup.') +
    p('For small stores with simple catalogs, automated tools handle the data transfer. Everything else benefits from professional help.') +
    p('Timeline: small-to-mid stores typically take 1-3 weeks.') +
    p('Larger stores with complex catalogs or significant SEO footprints should budget 4-8 weeks.') +
    p('The data transfer is the fastest part. Design, redirects, and integration rebuilds take most of the time.')
))

# ── SECTION 4: WHAT YOU GAIN ───────────────────────────────
parts.append(wrap(BG_BLUE,
    h2('what-you-gain', 'What does WooCommerce give you that Volusion cannot?') + '\n' +
    p('No sales caps. That is the first answer.') +
    p('No automatic plan upgrades because you crossed a revenue threshold.') +
    p('No bandwidth overage fees at $7 a gigabyte.') +
    p('Your monthly cost is your hosting plan plus the extensions you choose.') +
    p('The pricing model does not work against you as your store grows.') +
    img('42181', 'eCommerce store owner reviewing improved sales analytics dashboard on laptop after successful migration from Volusion to WooCommerce', 'https://virtina.com/wp-content/uploads/2026/05/volusion-woocommerce-migration-section3-670x352-2.jpg') + '\n' +
    p("The 60,000-plugin library means the integration you couldn't find in Volusion's 80-app marketplace almost certainly exists.") +
    p('Klaviyo, Mailchimp, QuickBooks, Xero, NetSuite, ShipStation, Stripe, Authorize.net: all have official WooCommerce extensions.') +
    p("The API is open. Developers will build on it. Agencies know it.") +
    p(f"That changes what's possible for your store's custom requirements. If you want to understand the full scope of the {L['woo_platform']}, the extension library is the place to start.") +
    p('Data ownership changes the risk picture.') +
    p('Your database lives on your server.') +
    p('No third party can lock your account, freeze your funds, or shut down your store.') +
    p("For merchants who built contingency plans after Volusion's 2020 bankruptcy, this is a material difference in business continuity.") +
    p(f'{L["woo_seo"]} control is a step change from what Volusion offers.') +
    p('Clean URL structures. Native blogging via WordPress. Full schema markup through Yoast or RankMath.') +
    p('WordPress powers 43% of all websites for a reason.') +
    p('The SEO tooling is mature and built for content-driven acquisition.') +
    p("For stores limited by Volusion's SEO ceiling, this is often the most tangible post-migration win.") +
    p('For B2B merchants, the contrast is sharpest.') +
    p(f'{L["b2b"]} includes tiered pricing by customer role, wholesale registration workflows, and quote request tools.') +
    p('Plugins like B2BKing, WholesaleX, and Wholesale Suite handle the wholesale layer.') +
    p("None of those exist natively in Volusion.") +
    p("For a distributor or manufacturer running wholesale alongside retail, Volusion's flat product model is not a minor inconvenience.") +
    p("It's a structural dead end.")
))

# ── PEOPLE ALSO ASK ────────────────────────────────────────
paa = (
    h3('Is Volusion still in business?') +
    p('Yes. Volusion filed for Chapter 11 bankruptcy in June 2020 and continued operating under restructured ownership.') +
    p('It emerged from bankruptcy and is still active.') +
    p("But the platform has contracted sharply. From 13,889 active stores in 2020 to 3,526 as of May 2026. That's a 75% decline in six years.") +
    p('The platform still processes orders. But investment in new features has been limited. Third-party agency support has declined significantly.') +

    h3('How long does a Volusion to WooCommerce migration take?') +
    p('For a small to mid-size store with a straightforward catalog, the migration typically takes 1-3 weeks.') +
    p('Larger stores with custom features, extensive SKU catalogs, or significant SEO footprints should budget 4-8 weeks.') +
    p('The data transfer is the faster part.') +
    p('Design rebuild, redirect mapping, and integration reconfiguration take the most time.') +
    p('Rushing any of those three phases creates problems that are much slower to fix after launch.') +

    h3('Will I lose my SEO rankings if I migrate from Volusion to WooCommerce?') +
    p('Not if the 301 redirects are implemented correctly before DNS cutover.') +
    p('Every Volusion URL that changes needs a redirect pointing to its WooCommerce equivalent.') +
    p('If redirects are missing, Google treats the new URLs as new pages and traffic drops.') +
    p("With a complete redirect map in place, most stores recover to pre-migration ranking levels within a few months.") +
    p("Many see improvement because WooCommerce's URL structure and schema capabilities are stronger than Volusion's.") +

    h3('How much does migrating from Volusion to WooCommerce cost?') +
    p('Automated data transfer tools start around $69 for basic migrations. That covers the data only.') +
    p('Not design, redirects, or configuration.') +
    p('A full migration with a new theme, redirect mapping, plugin selection, and testing requires developer time.') +
    p('The total cost scales with store size and catalog complexity.') +
    p('For stores on the Volusion Professional or Business plan, the ongoing savings from eliminating plan fees often offset the migration investment within the first year.')
)
parts.append(wrap(BG_LIGHT,
    '<h2 id="people-also-ask" style="color:#43627f;font-size:30px;">People also ask</h2>\n' + paa
))

# ── CONCLUSION ─────────────────────────────────────────────
parts.append(wrap(BG_SOLID,
    '<h2 id="conclusion" style="color:#ffffff;font-size:30px;">Conclusion</h2>\n' +
    pw("This isn't about WooCommerce being a perfect platform. It isn't.") +
    pw("You'll manage your own hosting, make your own plugin choices, and carry more operational responsibility than you did on Volusion.") +
    pw('Those are real costs.') +
    pw('The question is simpler than it looks.') +
    pw("Are you trading a managed simplicity that has stopped working for you, for a complexity you can actually control?") +
    pw("If your store is at $30,000 in annual sales with no integration ambitions, Volusion may still work.") +
    pw("But if you've hit the sales caps and run into the integration dead ends, migration is a project with a defined scope and a defined end date.") +
    pw("It's not a catastrophe. It's a decision.") +
    pw("The merchant is the one who decides.") +
    pw("But if you're planning a migration and want a team that has done this before, Virtina's WooCommerce migration team has run this project hundreds of times.") +
    pw('The conversation is worth having before you build the plan.')
))

# ── FAQ ────────────────────────────────────────────────────
parts.append('<h2 id="faq" style="color:#43627f;font-size:30px;">Frequently asked questions</h2>')
parts.append('<div>\n' +
faq('Can I keep my Volusion store live while I build the WooCommerce store?',
    p('Yes. Build and test the WooCommerce store on a staging URL while your Volusion store stays live.') +
    p('Only cut over DNS when the WooCommerce store is fully tested, redirect-mapped, and approved.') +
    p('The DNS propagation window is typically a few hours. That is your only real downtime.') +
    p('Keep your Volusion account active for at least 30 days post-launch so you can reference order history.')
) + '\n' +
faq('What happens to my customer passwords during migration?',
    p("Volusion stores passwords in a proprietary hashed format. That format cannot be converted to WooCommerce's format.") +
    p('Customer accounts migrate with names, addresses, and order history intact. Passwords do not.') +
    p('After migration, customers receive a password reset prompt on first login.') +
    p("Tell your customers in advance via email before the cutover. It prevents a flood of support tickets.")
) + '\n' +
faq('Do I need a developer to migrate from Volusion to WooCommerce?',
    p(f'For a simple store with a basic catalog and no {L["integrations"]}, automated tools like LitExtension can handle the data transfer.') +
    p('But theme rebuild, 301 redirect implementation, SEO plugin configuration, and custom functionality require technical judgment.') +
    p('For any store with a meaningful SEO footprint or B2B pricing requirements, a WooCommerce developer is not optional.') +
    p('Getting the redirect map wrong creates problems that take longer to fix than the original migration.')
) + '\n' +
faq('What happens to my Volusion payment processing after migration?',
    p("Volusion's own payment gateway charges maintenance fees ranging from 1.25% to 0.35% on top of standard processing fees.") +
    p('On WooCommerce you choose your own gateway.') +
    p('Stripe, PayPal, Square, and Authorize.net all have official WooCommerce extensions.') +
    p("If you were on Volusion Payments, re-establish merchant processing with an independent gateway before go-live.")
) + '\n' +
faq('What data can I actually export from Volusion before I leave?',
    p('Via Admin, then Data Management, then Export, you can pull products, customer accounts, order history, and category structure in CSV format.') +
    p('Store settings, custom fields with no WooCommerce equivalent, and theme assets do not transfer.') +
    p('Screenshot or export all active SEO meta titles and descriptions before you leave.') +
    p("You'll need them to restore your meta data inside WooCommerce's SEO plugin once the migration is complete.")
) + '\n</div>')

# ══════════════════════════════════════════════════════════
# ASSEMBLE + SELF-CHECK + PUSH
# ══════════════════════════════════════════════════════════
content = '\n\n'.join(parts)

words = len(re.findall(r'\w+', re.sub(r'<[^>]+>', '', content)))
ext   = re.findall(r'href="(https?://(?!virtina\.com)[^"]+)"', content)
int_  = re.findall(r'href="(https?://virtina\.com[^"]+)"', content)
em    = re.findall(r'—|&mdash;', content)
h2ids = re.findall(r'<h2[^>]*id="([^"]+)"', content)
toc_a = [a[1:] for a in re.findall(r'href="(#[^"]+)"', content)]
miss  = [a for a in toc_a if a not in h2ids]

# Check paragraph length (sentences per <p>)
paras = re.findall(r'<p[^>]*>(.*?)</p>', content, re.DOTALL)
long_paras = [(i+1, len(re.findall(r'[.!?]', re.sub(r'<[^>]+>','',p)))) for i,p in enumerate(paras) if len(re.findall(r'[.!?]', re.sub(r'<[^>]+>','',p))) > 3]

print(f'Words: {words}')
print(f'External links: {len(ext)} {ext}')
print(f'Internal links: {len(int_)}')
print(f'Em dashes: {len(em)}')
print(f'TOC-H2 mismatch: {miss}')
print(f'Long paragraphs (>3 end-punctuation): {long_paras}')

payload = {'content': content, 'status': 'draft'}
r = requests.post('https://virtina.com/wp-json/wp/v2/posts/42177', headers=headers, json=payload, timeout=60, verify=False)
print(f'\nPATCH: {r.status_code} | status={r.json().get("status")}')
