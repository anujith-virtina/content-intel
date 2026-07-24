# -*- coding: utf-8 -*-
"""Build + publish (draft) the Virtina 'leaving Shopify' Format-B post.
Templates A-N from clients/virtina/reference/html-templates.md. Zero em dashes.
"""
import os, json, requests, html as _html

USER = os.environ["WP_USERNAME"]
APP = os.environ["WP_APP_PASSWORD"]
BASE = "https://virtina.com/wp-json/wp/v2"

SLATE = "#43627f"
SLUG = "leaving-shopify-ownership-risk"
TITLE = "Why smart business owners are leaving Shopify (even without a ban)"
PERMALINK = f"https://virtina.com/{SLUG}/"

MEDIA = {
    "featured": (42436, "https://virtina.com/wp-content/uploads/2026/07/leaving-shopify-worried-business-owner-featured.jpg",
                 "Worried small business owner at a desk with a laptop, weighing the risk of staying on Shopify and leaving Shopify for WooCommerce."),
    "shop": (42437, "https://virtina.com/wp-content/uploads/2026/07/business-owner-shop-ownership.jpg",
             "Small business owner working inside their own shop, the kind of merchant thinking about Shopify risk and owning their online store."),
    "cost": (42438, "https://virtina.com/wp-content/uploads/2026/07/business-owner-reviewing-costs.jpg",
             "Business owner reviewing store costs and numbers at a desk, comparing Shopify fees with owning a WooCommerce store."),
    "relaxed": (42439, "https://virtina.com/wp-content/uploads/2026/07/relaxed-business-owner-after-move.jpg",
                "Confident, relaxed business owner after moving from Shopify to WooCommerce and taking full ownership of her online store."),
    "info": (42440, "https://virtina.com/wp-content/uploads/2026/07/renting-vs-owning-online-store-infographic.jpg",
             "Infographic comparing renting your store on Shopify with owning it on WooCommerce across control, rules, costs and shutdown risk."),
}

# ---------- template helpers ----------
def P(t):
    return f'<p dir="ltr" style="font-size:16px;line-height:1.75;">{t}</p>\n'

def H3(t):
    return f'<h3 style="color:{SLATE};font-size:22px;">{t}</h3>\n'

def SECTION(anchor, heading, inner):
    return (f'<div style="background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));'
            f'border-radius:20px;padding:30px;margin:0 0 28px 0;">'
            f'<h2 id="{anchor}" style="color:{SLATE};font-size:30px;">{heading}</h2>\n{inner}</div>\n')

def BULLETS(items):
    # items: list of (bold_label_or_None, text)
    out = '<ul style="list-style:none;padding-left:4px;margin:8px 0 16px 0;">\n'
    for label, text in items:
        lead = f'<strong>{label}.</strong> ' if label else ''
        out += ('<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;">'
                '<span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;'
                'border-radius:50%;display:inline-block;"></span>'
                f'<span style="font-size:16px;line-height:1.75;color:#2d3e50;">{lead}{text}</span></li>\n')
    out += '</ul>\n'
    return out

def IMG(key):
    mid, url, alt = MEDIA[key]
    return (f'<span style="display:block;margin:20px 0;"><img alt="{alt}" data-id="{mid}" width="670" '
            f'data-init-width="670" height="352" data-init-height="352" title="" loading="lazy" src="{url}" '
            f'data-width="670" data-height="352" style="aspect-ratio: auto 670 / 352;max-width:100%;"></span>\n')

def IL(url, text):
    return f'<a href="{url}" style="outline: none;">{text}</a>'

def XL(url, text):
    return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{text}</a>'

def TH(*hs):
    cells = ''.join(f'<th data-direction="" style="background:#43627f;color:#ffffff;padding:10px 14px;'
                    f'text-align:left;font-weight:600;"><p style="font-size:16px;line-height:1.75;">'
                    f'<strong>{h}</strong></p></th>' for h in hs)
    return f'<tr>{cells}</tr>'

def TR(cells, headers, odd):
    bg = "#f4f6f9" if odd else "#ffffff"
    tds = ''.join(f'<td data-th="{headers[i]}" style="background:{bg};padding:10px 14px;'
                  f'border-bottom:1px solid #dde0e6;vertical-align:top;">'
                  f'<p style="font-size:16px;line-height:1.75;">{c}</p></td>' for i, c in enumerate(cells))
    return f'<tr>{tds}</tr>'

def TABLE(headers, rows, caption):
    thead = f'<thead>{TH(*headers)}</thead>'
    body = ''.join(TR(r, headers, i % 2 == 0) for i, r in enumerate(rows))
    return (f'<table data-rows="{len(rows)+1}" data-cols="{len(headers)}" data-v="middle" '
            f'style="width:100%;border-collapse:collapse;margin:16px 0;">{thead}<tbody>{body}</tbody></table>\n'
            f'<p dir="ltr" style="font-size:14px;line-height:1.6;color:#6e6e6e;margin:4px 0 16px 0;">{caption}</p>\n')

# ---------- links ----------
VAPE = "https://virtina.com/shopify-vape-store-woocommerce-migration/"
L_NICHE = IL("https://virtina.com/woocommerce-niche-ecommerce-2025/", "WooCommerce for niche businesses")
L_VAPE1 = IL(VAPE, "Shopify's vape ban")
L_VAPE2 = IL(VAPE, "vape merchants on Shopify")
L_SVW = IL("https://virtina.com/shopify-vs-woocommerce/", "Shopify vs WooCommerce")
L_MIGRATE = IL("https://virtina.com/migrate-to-woocommerce/", "WooCommerce migration")
L_WOODEV = IL("https://virtina.com/platforms/woocommerce-development-services/", "WooCommerce development")
L_SHOPMIG = IL("https://virtina.com/shopify-migration-services/", "Shopify migration services")
L_GUIDE = IL("https://virtina.com/woocommerce-migration-guide/", "WooCommerce migration guide")
L_CASE = IL("https://virtina.com/case-study/b2b-ecommerce-fruitful-grind-case-study/", "B2B store case study")
L_CONTACT = IL("https://virtina.com/get-in-touch/", "Virtina migration team")
X_AG = XL("https://oag.ca.gov/news/press-releases/co-leading-bipartisan-coalition-attorney-general-bonta-calls-shopify-crack-down", "state attorneys general")

# ---------- build content ----------
c = ""

# Summary (Template A)
c += ('<div style="background:linear-gradient(rgba(0,213,192,0.28),rgba(0,213,192,0.28));border-radius:20px;'
      'padding:30px;margin:0 0 28px 0;"><h2 dir="ltr" style="color:#43627f;font-size:30px;">Summary</h2>\n'
      + P("More business owners are leaving Shopify for WooCommerce to stop renting their store and start owning it. "
          "On Shopify, your store, your customer list, and your catalog all sit on rented land. One rule change or "
          "one account review can take you offline.")
      + P("This guide explains the risk in plain language. It covers what ownership really means, what it costs, "
          "and how a move protects the business you built.")
      + '</div>\n')

# Introduction (Template B) - candle scenario
intro = "".join([
    P("Picture a small candle brand. The owner, we'll call her Maria, built it from her kitchen table."),
    P("Three good years. Steady sales, repeat customers, and a holiday season that pays for the whole year."),
    P("One Tuesday morning, she opens her email. Her Shopify account is \"under review.\""),
    P("A single customer complaint triggered it. Her store is offline while they look into it."),
    P("She calls support. They're polite. They tell her to wait three to five business days."),
    P("Meanwhile her checkout is dark. Orders stop. Her biggest season starts in a week."),
    P("Maria didn't break any rules. She got no real warning. She just woke up locked out of the business she built."),
    P("This isn't a rare nightmare. Store reviews, holds, and sudden policy changes hit Shopify merchants every day. Most owners never see it coming."),
    P("That's why more owners are quietly moving off Shopify. Not because Shopify is evil. Because they want to own their store, not rent it."),
    P("If you've ever felt one email away from losing everything, this guide is for you. We'll keep it plain."),
    P("No tech talk. Just straight answers about control, cost, and peace of mind."),
])
c += ('<div style="background:linear-gradient(rgba(241,243,250,0.5),rgba(241,243,250,0.5));border-radius:20px;'
      'padding:30px;margin:0 0 28px 0;"><h2 style="color:#43627f;font-size:30px;">Introduction</h2>\n' + intro + '</div>\n')

# TOC (Template C)
toc_items = [
    ("own-your-store", "What does it mean to own your online store?"),
    ("what-can-go-wrong", "What can go wrong when you don't own your store?"),
    ("why-woocommerce", "Why are more owners moving to WooCommerce in 2026?"),
    ("renting-vs-owning", "Renting vs owning your online store"),
    ("is-it-harder", "Isn't WooCommerce harder to set up than Shopify?"),
    ("what-moving-looks-like", "What does moving to WooCommerce look like?"),
    ("cost-comparison", "How much does WooCommerce cost compared to Shopify?"),
    ("who-is-moving", "What kinds of businesses are moving to WooCommerce?"),
    ("signs-to-leave", "Signs it might be time to leave Shopify"),
    ("people-also-ask", "People also ask"),
    ("conclusion", "Conclusion"),
    ("faq", "Frequently asked questions"),
]
arrow = ('<span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;">'
         '<svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg">'
         '<path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg></span>')
c += '<h3 style="color:#43627f;font-size:22px;">Table of Contents</h3>\n'
c += '<ul style="list-style:none!important;padding-left:0!important;margin:0 0 1.5em 0!important;">\n'
for anchor, text in toc_items:
    c += ('<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;'
          f'line-height:1.5!important;margin:0!important;">{arrow}'
          f'<a href="#{anchor}" style="color:#00a0e2!important;text-decoration:none!important;'
          f'font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">{text}</a></li>\n')
c += '</ul>\n'

# Section 1: own your store
s1 = (P("Owning your online store means it lives on space you control. It does not sit on a platform that can switch you off.")
      + P("On Shopify, you rent all of it. Your shop runs on their land, under their rules.")
      + P("Think of a shop inside a shopping mall. The mall handles the lights, the security, and the foot traffic.")
      + P("That's easy and comfortable. But the mall owner sets the hours. They can raise your rent, or end your lease.")
      + P("Owning your store is more like owning the building your shop sits in. You still pay for upkeep and repairs.")
      + P("But no landlord can lock your door over a complaint.")
      + H3("Why does this matter when things go wrong?")
      + P("Here's the truth. When someone else controls your door, one dispute can close you.")
      + P("When you own the building, every problem is yours to fix on your own terms.")
      + P("That gap feels invisible on a good day. It feels enormous on your busiest one.")
      + P(f"Owning your store outright is the whole point of moving. That's exactly why {L_NICHE} has become such a popular choice."))
c += SECTION("own-your-store", "What does it mean to \"own\" your online store?", s1)
c += IMG("shop")

# Section 2: what can go wrong (5 H3s)
s2 = (P("Plenty can go wrong, and most of it happens without warning. When you rent, the platform holds the keys. Here are five real risks every Shopify owner carries, even the ones making great money.")
      + H3("1. Shopify can shut down your store overnight")
      + P("Your store can go offline fast, sometimes over a single complaint or a flagged payment. Account reviews and holds are routine. While you wait, orders stop and customers see an error page.")
      + P("You did nothing wrong, but the outcome is the same. No store, no sales, no say in the timeline.")
      + H3("2. Shopify can drop entire product categories")
      + P("Shopify can decide a whole type of product is no longer welcome. Every seller in that group loses their store.")
      + P("This isn't a guess. It already happened.")
      + P(f"In mid-2026, Shopify told vape and e-cigarette sellers to remove their products within about two weeks or lose their accounts. The move followed public pressure from {X_AG} across dozens of states. You can read the full story of {L_VAPE1} and how those owners scrambled to move.")
      + P("The lesson isn't about vaping. It's that a platform can retire your entire category on short notice. If it can happen to them, it can happen to any product a rule-maker decides to target.")
      + H3("3. Shopify can raise prices whenever they want")
      + P("Your monthly cost is set by Shopify, not by you. Plans, app fees, and extra charges can climb as you grow. You either pay the new price or pack up and leave.")
      + P("Renters don't set the rent. That's the deal you accept the day you sign up.")
      + H3("4. Shopify can change the rules on how you sell")
      + P("The fine print can shift at any time. What you sell, how you take payment, which tools you use, all of it can change with an update. You find out after the fact.")
      + P("Not anymore, once you own your store. The rules become yours.")
      + H3("5. If Shopify has an outage, your business goes down with them")
      + P("When Shopify's systems go down, thousands of stores go dark at the same moment, including yours. You can't fix it. You can only wait and watch sales slip away.")
      + P("Owning your store spreads that risk. If one part fails, you have options and people who answer to you."))
c += SECTION("what-can-go-wrong", "What can go wrong when you don't own your store?", s2)

# Section 3: why woocommerce
s3 = (P("Owners are moving because WooCommerce hands them control that Shopify keeps for itself. WooCommerce is software you own and run on space you rent from a hosting company. No single company can flip a switch and end your business.")
      + P("Here's what draws people over, in plain terms.")
      + BULLETS([
          ("You own everything", "Your customer list, your orders, and your product photos are yours to keep and move."),
          ("No one can shut you down", "There's no central landlord to suspend your account over a complaint."),
          ("You can sell anything legal", "No category police deciding your product is suddenly off-limits."),
          ("You pay for what you use", "Your costs stay predictable instead of climbing with every plan tier."),
          ("Your business is worth more", "A store you fully own is an asset you can sell one day, not a lease you rent."),
      ])
      + P(f"Want the honest head-to-head? Our {L_SVW} breakdown weighs both without the hype."))
c += SECTION("why-woocommerce", "Why are more business owners moving to WooCommerce in 2026?", s3)

# Section 4: renting vs owning (table + infographic)
t1 = TABLE(["Renting from Shopify", "Owning with WooCommerce"],
           [["Shopify can pause your store", "Only you decide when your store runs"],
            ["Pay Shopify every month, forever", "Pay hosting monthly, keep the rest"],
            ["Shopify holds your customer data", "Your customer list stays yours"],
            ["Shopify sets the rules", "You set the rules"],
            ["Fees climb higher as you grow", "Costs stay steady and predictable"],
            ["Locked into Shopify's apps", "Choose any tools you want"],
            ["Fine print can change anytime", "You control your own setup"]],
           "Renting vs owning your online store, in plain business terms. Virtina, July 2026.")
s4 = (P("The difference comes down to who holds control when it counts. Renting is fast and hands-off, but the platform decides your fate. Owning takes a bit more setup, and then the business answers to you.")
      + P("Here's the side-by-side in plain business terms.")
      + t1
      + IMG("info")
      + P(f"If that table makes you pause, you're not alone. Most owners never think about it until something breaks. A {L_MIGRATE} partner is how they take the keys back."))
c += SECTION("renting-vs-owning", "What's the difference between renting and owning your online store?", s4)

# Section 5: is it harder
s5 = (P("No, not when someone sets it up for you. Shopify feels easy because it's like renting a furnished apartment. Everything's already in place, so you never see the wiring.")
      + P("WooCommerce with a partner like Virtina feels just as simple to run. The difference is that you own the place at the end, furniture and all. You don't touch code, and you don't become a tech person.")
      + H3("What does a partner handle for you?")
      + P("We handle the building, the moving, and the testing so you don't have to learn any of it. Your job is to keep selling while we do the heavy lifting behind the scenes.")
      + P(f"That includes the full build, moving your products and customers, and checking that every page and button works. Our {L_WOODEV} team does this every week. Our {L_SHOPMIG} are built for exactly this kind of move.")
      + P("No coding skills needed on your side. You stay the owner, not the operator."))
c += SECTION("is-it-harder", "Isn't WooCommerce harder to set up than Shopify?", s5)

# Section 6: what moving looks like
s6 = (P("The move is a guided project, and your current store keeps selling the whole time. You don't flip a switch and hope. You build the new store quietly, then go live when it's ready.")
      + P("Here's the path, step by step.")
      + BULLETS([
          ("Step 1", "A short call with a WooCommerce partner. About 30 minutes, no commitment."),
          ("Step 2", "They review your Shopify store and map out a plan."),
          ("Step 3", "They build your new store while your Shopify shop keeps running."),
          ("Step 4", "They move your products, customers, and past orders across."),
          ("Step 5", "They test everything, then switch your new store on."),
          ("Step 6", "Your web address stays the same. Customers notice nothing except a faster site."),
      ])
      + P(f"Most moves take three to six weeks. Urgent ones move faster. Our {L_GUIDE} walks through the same path in more detail."))
c += SECTION("what-moving-looks-like", "What does moving from Shopify to WooCommerce actually look like?", s6)
c += IMG("relaxed")

# Section 7: cost
t2 = TABLE(["3-year total", "Shopify (plan, apps, sale fees)", "WooCommerce (build, hosting, tools)"],
           [["Small store", "about $3,500 to $5,000", "about $3,500 to $4,500"],
            ["Growing store", "about $8,000 to $10,000", "about $6,500 to $8,500"],
            ["Larger store", "about $18,000 to $24,000", "about $11,000 to $16,000"]],
           "Illustrative three-year ranges, not price quotes. Normal card-processing fees apply on both platforms. Virtina estimates, July 2026.")
s7 = (P("Over a year or more, WooCommerce usually costs less, and the price is easier to predict. Shopify charges you every month, plus app fees, plus extra charges on many sales. Those numbers keep climbing as you grow.")
      + P("WooCommerce works differently. You pay a one-time cost to build the store, then a monthly hosting bill and a few optional tools. You own what you paid for.")
      + H3("A simple three-year comparison")
      + P("Here's a rough picture for three store sizes. These are typical ranges, not quotes, and both platforms still pay normal card fees on top.")
      + t2
      + P("Small stores often land close on cost, but you gain ownership. Growing stores usually save real money, because Shopify's app and sale fees add up fast."))
c += SECTION("cost-comparison", "How much does WooCommerce actually cost compared to Shopify?", s7)
c += IMG("cost")

# Section 8: who is moving
s8 = (P("Mostly owners who've outgrown \"small side hustle\" and want to protect what they've built. These aren't tech companies. They're regular businesses with real customers and real revenue on the line.")
      + P("We see the same faces again and again.")
      + BULLETS([
          ("Family-run product brands", "Candles, jewelry, food, crafts, and home goods."),
          ("Small makers and distributors", "Businesses that hold stock and ship orders."),
          ("Specialty sellers", "Owners of supplements, wellness products, and other goods a platform might restrict."),
          ("Anyone who's scaled up", "Stores past the beginner stage that can't afford a surprise shutdown."),
      ])
      + P(f"That last group learned the hard way. When {L_VAPE2} lost their stores, plenty of other owners realized their category could be next. You can see how one growing brand made the move in our {L_CASE}.")
      + H3("Is Shopify ever still the right choice?")
      + P("Yes, sometimes it is. If you're just testing an idea with a handful of products, Shopify's speed is hard to beat. If you only resell other people's goods and lean on a few apps, the rented setup may suit you fine.")
      + P("The move makes sense once your store becomes the business, not the experiment. That's when ownership starts to matter more than convenience."))
c += SECTION("who-is-moving", "What kinds of businesses are moving to WooCommerce?", s8)

# Section 9: signs (checklist)
s9 = (P("If a few of these sound familiar, it's worth a serious look. This is a quick gut-check, not a test. Read the list and count your yeses.")
      + BULLETS([
          (None, "Your Shopify bill has grown past $200 a month."),
          (None, "You worry about Shopify shutting you down over a rule change."),
          (None, "You want to sell products Shopify might not allow."),
          (None, "You feel locked in and unsure how to leave."),
          (None, "You want to own your business, not rent it."),
          (None, "You're paying extra fees on sales, on top of the subscription."),
          (None, "You need features Shopify's apps just don't offer."),
          (None, "You want a business you could sell someday."),
      ])
      + P(f"Three or more yeses? It's worth a real conversation. Our {L_CONTACT} will tell you honestly whether a move fits your store."))
c += SECTION("signs-to-leave", "Signs it might be time to leave Shopify", s9)

# People also ask (Template H)
paa = ('<div style="background:linear-gradient(rgba(241,243,250,0.5),rgba(241,243,250,0.5));border-radius:20px;'
       'padding:30px;margin:0 0 28px 0;"><h2 id="people-also-ask" style="color:#43627f;font-size:30px;">People also ask</h2>\n')
paa += H3("Can Shopify really shut down my store without warning?")
paa += P("Yes, an account review or policy flag can take your store offline while Shopify investigates. You may not get a warning first. That's the trade-off of running on a platform you don't own.")
paa += H3("Is leaving Shopify for WooCommerce worth it for a small store?")
paa += P("It can be, if you value ownership and predictable costs over pure convenience. Very small or test stores may stay on Shopify happily. Once your store becomes your livelihood, owning it usually wins.")
paa += H3("Will I lose sales during the move to WooCommerce?")
paa += P("No, a proper move keeps your Shopify store selling until the new one is ready. You only switch over once everything is tested. Done right, your customers never notice a gap.")
paa += '</div>\n'
c += paa

# Conclusion (Template I)
c += ('<div style="background:#00d5c0;border-radius:20px;padding:30px;margin:0 0 28px 0;">'
      '<h2 id="conclusion" style="color:#ffffff;font-size:30px;">Conclusion</h2>\n'
      '<p style="color:#ffffff;font-size:16px;line-height:1.75;">Remember Maria and her candle brand. Her store didn\'t disappear because she failed. It disappeared because someone else changed the rules and held the keys.</p>\n'
      '<p style="color:#ffffff;font-size:16px;line-height:1.75;">Your store shouldn\'t vanish over a policy update you never saw coming. When you own it, that fear goes away. You decide when your store runs, who your customers belong to, and how you grow.</p>\n'
      '<p style="color:#ffffff;font-size:16px;line-height:1.75;">We\'ve helped more than 1,000 online stores fix what\'s broken and move platforms without losing sales. If you\'re ready to own the business you built, let\'s talk about your move.</p>\n'
      '</div>\n')

# FAQ (Template J)
faqs = [
    ("Will my customers see any changes when I move?",
     "No, your customers keep shopping as normal, usually on a faster site. The look, the products, and the checkout carry over. Most people never realize anything changed behind the scenes."),
    ("Will my website look the same?",
     "Yes, we can rebuild your store to match your current look, or improve it if you'd like. Your brand, colors, and product pages stay yours. Nothing about your identity has to change."),
    ("Can I keep my web address and domain name?",
     "Yes, your domain name moves with you and stays exactly the same. Customers use the same web address they always have. You never lose the name you've built trust around."),
    ("What happens to my Shopify subscription when I move?",
     "You keep it running until your new store is live and tested, then you cancel it. There's no risky overlap where you're offline. You stop paying Shopify only after you're safely moved."),
    ("How long can I run both stores at once during the move?",
     "You can run both for the full length of the project, usually three to six weeks. Your Shopify store keeps selling the whole time. We switch over only when the new store is ready."),
    ("Do I need to know anything technical?",
     "No, you don't need any tech skills to make this move. Your partner handles the building, moving, and testing. Your job is to keep running your business as usual."),
    ("What if something breaks after the move?",
     "We test everything before launch and stay with you after go-live to fix anything that comes up. Support doesn't end at the switch. You're never left alone with a problem."),
    ("How much will this really cost?",
     "It depends on your store's size, but most owners find WooCommerce cheaper over a year or more. You pay a one-time build cost, then predictable hosting. The savings grow as your store grows."),
]
c += '<h2 id="faq" style="color:#43627f;font-size:30px;">Frequently asked questions</h2>\n<div>\n'
for q, a in faqs:
    c += ('<details class="vfaq" style="background:transparent;margin-top:7px;"><summary style="cursor:pointer;'
          'padding:17px;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:12px;'
          'background:rgba(245,245,245,0.5);"><span style="font-size:16px;font-weight:600;color:#43627f;'
          f'line-height:2;flex:1;">{q}</span><svg viewBox="0 0 24 24" width="17" height="17" '
          'style="fill:#50565f;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg"><path d="M16,12A2,2 0 0,1 18,10A2,2 0 0,1 20,12A2,2 0 0,1 18,14A2,2 0 0,1 16,12M8,12A2,2 0 0,1 10,10A2,2 0 0,1 12,12A2,2 0 0,1 10,14A2,2 0 0,1 8,12M0,12A2,2 0 0,1 2,10A2,2 0 0,1 4,12A2,2 0 0,1 2,14A2,2 0 0,1 0,12Z"/></svg></summary>'
          f'<div class="vfaq-answer" style="padding:30px 22px;background:#fff;"><p dir="ltr" '
          f'style="font-size:16px;line-height:1.75;">{a}</p></div></details>\n')
c += '</div>\n'

# Author bio (Template K)
c += ('<p dir="ltr" style="font-size:16px;line-height:1.75;"><strong>The Virtina team</strong> builds, fixes, and '
      'moves ecommerce stores for B2B and B2C brands across more than ten platforms. We\'ve helped over 1,000 '
      'businesses stop the bleeding and own what they\'ve built.</p>\n')

# ---------- JSON-LD schema ----------
META_DESC = "Worried Shopify could pause your store overnight? See why smart business owners are leaving Shopify for WooCommerce to own their store, data and customers."
faq_ld = [{"@type": "Question", "name": q,
           "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]
schema = {
    "@context": "https://schema.org",
    "@graph": [
        {"@type": "Article", "headline": TITLE, "description": META_DESC,
         "image": MEDIA["featured"][1], "datePublished": "2026-07-24", "dateModified": "2026-07-24",
         "author": {"@type": "Organization", "name": "Virtina", "url": "https://virtina.com/"},
         "publisher": {"@type": "Organization", "name": "Virtina",
                       "logo": {"@type": "ImageObject", "url": "https://virtina.com/wp-content/uploads/2021/06/virtina-logo.png"}},
         "mainEntityOfPage": {"@type": "WebPage", "@id": PERMALINK}},
        {"@type": "FAQPage", "mainEntity": faq_ld},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://virtina.com/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://virtina.com/resources/blog/"},
            {"@type": "ListItem", "position": 3, "name": TITLE, "item": PERMALINK}]},
    ],
}
c += '<script type="application/ld+json">' + json.dumps(schema) + '</script>\n'

# save local copy
import sys
here = os.path.dirname(os.path.abspath(__file__))
open(os.path.join(here, "leaving-shopify-ownership-risk-2026-07-24.html"), "w", encoding="utf-8").write(c)
print("content length:", len(c), "chars")
if "publish" not in sys.argv:
    print("DRY RUN (build only). Pass 'publish' to POST.")
    raise SystemExit(0)

# ---------- publish (draft) ----------
payload = {
    "title": TITLE,
    "slug": SLUG,
    "status": "draft",
    "content": c,
    "excerpt": META_DESC,
    "featured_media": MEDIA["featured"][0],
    "categories": [79, 99],  # WooCommerce, Shopify
    "meta": {"yoast_wpseo_title": "Why Owners Are Leaving Shopify for WooCommerce | Virtina",
             "yoast_wpseo_metadesc": META_DESC},
}
r = requests.post(f"{BASE}/posts", json=payload, auth=(USER, APP), timeout=120)
print("POST status:", r.status_code)
if r.status_code not in (200, 201):
    print(r.text[:2000]); raise SystemExit(1)
j = r.json()
print("POST_ID:", j["id"])
print("PREVIEW:", j.get("link"))
print("SLUG:", j.get("slug"))
open(os.path.join(here, "publish_result.json"), "w").write(json.dumps({"id": j["id"], "link": j.get("link"), "slug": j.get("slug")}))
