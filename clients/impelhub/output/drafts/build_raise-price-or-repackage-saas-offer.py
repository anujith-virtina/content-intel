# -*- coding: utf-8 -*-
"""Build the ImpelHub Elementor HTML for: raise price or repackage the offer."""
import io, json, random, re, sys

PURPLE = "#5736fd"
random.seed(20260910)

def eid():
    return "%08x" % random.getrandbits(32)

def container(inner, bg=False, extra=""):
    settings = ' data-settings="{&quot;background_background&quot;:&quot;classic&quot;}"' if bg else ""
    return (
        '<div class="elementor-element elementor-element-%s e-con-full e-flex e-con e-parent" '
        'data-id="%s" data-element_type="container" data-e-type="container"%s%s>%s</div>'
        % (eid(), eid(), settings, extra, inner)
    )

def heading(tag, text, anchor=None):
    cls = "blog-title-h2 " if tag == "h2" else ""
    idattr = ' id="%s"' % anchor if anchor else ""
    return (
        '<div class="elementor-element elementor-element-%s %selementor-widget elementor-widget-heading" '
        'data-id="%s" data-element_type="widget" data-e-type="widget"%s data-widget_type="heading.default">'
        '<%s class="elementor-heading-title elementor-size-default">%s</%s></div>'
        % (eid(), cls, eid(), idattr, tag, text, tag)
    )

def text(html):
    return (
        '<div class="elementor-element elementor-element-%s elementor-widget elementor-widget-text-editor" '
        'data-id="%s" data-element_type="widget" data-e-type="widget" data-widget_type="text-editor.default">'
        '%s</div>' % (eid(), eid(), html)
    )

def arrow(body):
    return '<p><span style="color:%s;">→</span> %s</p>' % (PURPLE, body)

def toclink(anchor, label):
    return ('<p><span style="color:%s;">→</span> '
            '<a href="#%s" style="color:%s;text-decoration:none;">%s</a></p>'
            % (PURPLE, anchor, PURPLE, label))

def ilink(url, label):
    return '<a href="%s" style="color:%s;font-weight:500;">%s</a>' % (url, PURPLE, label)

def rr(url, label):
    return ('<p><span style="color:%s;">→</span> '
            '<a href="%s" style="color:%s;text-decoration:none;">%s</a></p>'
            % (PURPLE, url, PURPLE, label))

# ---------------------------------------------------------------- accordion
MINUS = ('<svg aria-hidden="true" class="e-font-icon-svg e-fas-minus" viewBox="0 0 448 512" '
         'xmlns="http://www.w3.org/2000/svg"><path d="M416 208H32c-17.67 0-32 14.33-32 32v32c0 '
         '17.67 14.33 32 32 32h384c17.67 0 32-14.33 32-32v-32c0-17.67-14.33-32-32-32z"></path></svg>')
PLUS = ('<svg aria-hidden="true" class="e-font-icon-svg e-fas-plus" viewBox="0 0 448 512" '
        'xmlns="http://www.w3.org/2000/svg"><path d="M416 208H272V64c0-17.67-14.33-32-32-32h-32c-17.67 '
        '0-32 14.33-32 32v144H32c-17.67 0-32 14.33-32 32v32c0 17.67 14.33 32 32 32h144v144c0 17.67 '
        '14.33 32 32 32h32c17.67 0 32-14.33 32-32V304h144c17.67 0 32-14.33 32-32v-32c0-17.67-14.33-32-32-32z">'
        '</path></svg>')

def accordion(items):
    out = []
    for i, (q, a) in enumerate(items, start=1):
        iid = "e-n-accordion-item-%d" % (7100 + i)
        is_open = (i == 1)
        out.append(
            '<details id="%s" class="e-n-accordion-item"%s>'
            '<summary class="e-n-accordion-item-title" data-accordion-index="%d" tabindex="%d" '
            'aria-expanded="%s" aria-controls="%s">'
            '<span class="e-n-accordion-item-title-header">'
            '<h4 class="e-n-accordion-item-title-text"> %s </h4></span>'
            '<span class="e-n-accordion-item-title-icon">'
            '<span class="e-opened">%s</span><span class="e-closed">%s</span></span>'
            '</summary>'
            '<div role="region" aria-labelledby="%s" class="elementor-element elementor-element-%s '
            'e-con-full e-flex e-con e-parent" data-id="%s" data-element_type="container" '
            'data-e-type="container">%s</div></details>'
            % (iid, " open" if is_open else "", i, 0 if is_open else -1,
               "true" if is_open else "false", iid, q, MINUS, PLUS, iid,
               eid(), eid(), text(a))
        )
    settings = ("{&quot;default_state&quot;:&quot;expanded&quot;,&quot;max_items_expended&quot;:"
                "&quot;one&quot;,&quot;n_accordion_animation_duration&quot;:{&quot;unit&quot;:"
                "&quot;ms&quot;,&quot;size&quot;:400,&quot;sizes&quot;:[]}}")
    return ('<div class="elementor-element elementor-element-%s elementor-widget elementor-widget-n-accordion" '
            'data-id="%s" data-element_type="widget" data-e-type="widget" data-settings="%s" '
            'data-widget_type="nested-accordion.default">'
            '<div class="e-n-accordion" aria-label="Accordion. Open links with Enter or Space, close with '
            'Escape, and navigate with Arrow Keys">%s</div></div>'
            % (eid(), eid(), settings, "".join(out)))

# ---------------------------------------------------------------- links
L_PMF   = "https://impelhub.com/blog/product-market-fit-signals-b2b-saas/"
L_ICP   = "https://impelhub.com/blog/icp-grading/"
L_METR  = "https://impelhub.com/blog/growth-metrics-that-matter-by-stage/"
L_GTM   = "https://impelhub.com/blog/gtm-vs-growth-strategy/"
L_REP   = "https://impelhub.com/blog/when-to-hire-first-sales-rep-b2b-saas/"
L_FEAT  = "https://impelhub.com/blog/feature-prioritization-business-growth/"
L_COORD = "https://impelhub.com/blog/coordinated-growth-vs-brute-force-scaling/"
L_QUIZ  = ("https://impelhub.com/find-out-where-your-business-should-focus-next-for-growth-"
           "in-just-3-minutes/")

TOC = [
    ("difference",   "What is the real difference between price and packaging?"),
    ("symptoms",     "How do I tell which one is actually broken?"),
    ("value-metric", "What is a value metric, and why does it decide everything?"),
    ("order",        "If both are broken, which do I fix first?"),
    ("existing",     "Do I apply the change to existing customers or only new ones?"),
    ("evidence",     "What evidence do I need before I move?"),
    ("mistakes",     "What do founders get wrong when they finally act?"),
    ("conclusion",   "Conclusion"),
    ("faq",          "Frequently asked questions"),
]

blocks = []

# ---- TL;DR
blocks.append(container(
    heading("h2", "TL;DR: Key takeaways", "tldr") +
    text("".join([
        arrow("Price is the number a customer pays. Packaging is what that number buys. "
              "Most revenue leaks live in packaging."),
        arrow("Raising price on a broken package converts a pricing problem into a churn problem."),
        arrow("Your value metric is the fastest diagnostic. Check whether your heaviest users pay the most."),
        arrow("Fix packaging first, then price. Reversing that order is the expensive mistake."),
        arrow("Grandfathering is a revenue decision, not a courtesy. Decide it on purpose."),
        arrow("No trustworthy public benchmark exists for this call. Every widely quoted figure "
              "traces back to a vendor."),
    ]))
))

# ---- TOC
blocks.append(container(
    heading("h3", "Table of Contents") +
    text("".join(toclink(a, l) for a, l in TOC)),
    bg=True
))

# ---- Intro
blocks.append(container(text(
    "<p>Revenue is flat. Deals close, but at numbers that feel low. Someone on the board says "
    "the word underpriced.</p>"
    "<p>So you open the pricing page and start typing bigger numbers. That is the reflex, and it "
    "is usually the wrong one. The number is rarely the part that is broken.</p>"
    "<p>This is a decision filter for the two levers founders confuse. One is price. One is "
    "packaging.</p>"
    "<p>They fail differently and they show different symptoms. They also carry very different "
    "risk to your existing base.</p>"
)))

# ---- S1
blocks.append(container(
    heading("h2", "What is the real difference between price and packaging?", "difference") +
    text(
        "<p>Price is the number a customer pays, and packaging is what that number buys.</p>"
        "<p>Packaging covers four things:</p>"
        "<ul>"
        "<li>Which features sit in which tier</li>"
        "<li>What unit you charge against</li>"
        "<li>Where the usage limits fall</li>"
        "<li>What triggers an upgrade</li>"
        "</ul>"
        "<p>Price is one variable. Packaging is the structure that variable sits inside.</p>"
        "<p>Change the price and every customer feels the same thing, a bigger invoice. Change the "
        "packaging and different customers feel completely different things. That asymmetry is the "
        "whole decision.</p>"
    ) +
    heading("h3", "Where founders blur the two") +
    text(
        "<p>The blur happens because both show up on the same page. Your pricing page displays "
        "three columns, and founders read the whole grid as pricing.</p>"
        "<p>The columns are packaging. Only the numbers at the top are price. When a prospect says "
        "you are expensive, ask which part they meant.</p>"
        "<p>Half the time they mean the price is high. The other half they mean the tier they need "
        "is stuffed with things they will never open.</p>"
    ) +
    heading("h3", "Why the distinction changes the fix") +
    text(
        "<p>A price change is reversible in practice. A packaging change is not, because you have "
        "moved features between tiers and told customers what they now belong to.</p>"
        "<p>That makes packaging the slower, heavier decision. It also makes it the more durable "
        "one. A repackage that fixes the upgrade path keeps paying you every renewal cycle.</p>"
    )
))

# image slot 1
blocks.append("<!--IMG-SLOT-1-->")

# ---- S2
blocks.append(container(
    heading("h2", "How do I tell which one is actually broken?", "symptoms") +
    text(
        "<p>Read the shape of your losses, because price failures and packaging failures leave "
        "different fingerprints.</p>"
        "<p>Price failures show up at the moment of decision. Packaging failures show up after "
        "the sale, in usage and in renewal conversations. Sort your last twenty lost or shrinking "
        "accounts into those two buckets before you touch anything.</p>"
    ) +
    heading("h3", "Symptoms that point at price") +
    text(
        "<p>These all cluster around the close:</p>"
        "<ul>"
        "<li>Deals stall at procurement, not at evaluation</li>"
        "<li>Your discount rate creeps up quarter after quarter</li>"
        "<li>Reps win by dropping the number, not by changing the scope</li>"
        "<li>Win rates are healthy but average contract value is flat</li>"
        "</ul>"
        "<p>If most of your evidence sits here, you have a price problem. It may be that the price "
        "is too high for the segment. It may also be that it is too low to be believed.</p>"
    ) +
    heading("h3", "Symptoms that point at packaging") +
    text(
        "<p>These cluster after the signature:</p>"
        "<ul>"
        "<li>Customers ask to buy one feature and refuse the tier it lives in</li>"
        "<li>Your most active accounts sit on your cheapest plan</li>"
        "<li>Nobody ever upgrades without a rep pushing them</li>"
        "<li>Sales writes custom scope on more than a third of deals</li>"
        "</ul>"
        "<p>That last one is the loudest signal. When reps rebuild the offer deal by deal, the "
        "standard package does not match the market.</p>"
        "<p>The same pattern appears when a company mistakes a structural gap for a demand gap. "
        "That trap is covered in our breakdown of "
        + ilink(L_GTM, "GTM versus growth strategy") + ".</p>"
    )
))

# ---- S3
blocks.append(container(
    heading("h2", "What is a value metric, and why does it decide everything?", "value-metric") +
    text(
        "<p>A value metric is the unit you charge against, and it decides whether your revenue "
        "grows when your customer succeeds.</p>"
        "<p>Seats, records, jobs run, gigabytes stored, transactions processed. Pick one and you "
        "have chosen who pays more over time. Pick badly and you have capped yourself.</p>"
    ) +
    heading("h3", "Signs your value metric is wrong") +
    text(
        "<p>Run one query. Rank your accounts by product usage, then rank them by what they pay. "
        "If those two lists disagree badly, the metric is wrong.</p>"
        "<p>The classic failure is seat-based pricing on a product that gets more valuable through "
        "automation. Your best customer automates the work, removes seats, and pays you less for "
        "getting more value. No price increase repairs that.</p>"
        "<p>The mirror failure is charging on a unit the buyer cannot forecast. Finance will not "
        "approve a line item they cannot predict, so deals die in review.</p>"
    ) +
    heading("h3", "Why this is a segmentation question first") +
    text(
        "<p>Different segments derive value from different units. A ten-person team and a "
        "four-hundred-person team rarely share a value metric.</p>"
        "<p>That is why this work starts with who you serve, not with what you charge. If your "
        "segments are fuzzy, tighten them first using an " + ilink(L_ICP, "ICP grading rubric") +
        ". Packaging built on a fuzzy segment definition will drift again within two quarters.</p>"
    )
))

# image slot 2
blocks.append("<!--IMG-SLOT-2-->")

# ---- S4
blocks.append(container(
    heading("h2", "If both are broken, which do I fix first?", "order") +
    text(
        "<p>Fix packaging first, then price. The order is not a preference, it is a consequence of "
        "how the two interact.</p>"
        "<p>Packaging sets what a customer receives. Price sets what they pay for it. You cannot "
        "know the right number until you know what the number buys.</p>"
    ) +
    heading("h3", "The sequence that works") +
    text(
        "<p>Run it in four moves, in this order:</p>"
        "<ol>"
        "<li>Choose the value metric</li>"
        "<li>Rebuild the tiers around it</li>"
        "<li>Set limits so the upgrade trigger is obvious</li>"
        "<li>Set the numbers</li>"
        "</ol>"
        "<p>Most of the revenue gain arrives in move three. When the upgrade trigger is obvious, "
        "expansion stops depending on a rep remembering to ask.</p>"
        "<p>Give the new structure one full renewal cycle before you touch price again. You need "
        "clean data on how the package behaves on its own.</p>"
    ) +
    heading("h3", "What happens if you reverse it") +
    text(
        "<p>Reversing the order is how a pricing project becomes a retention project.</p>"
        "<p>You raise the number on a package that already frustrated people. Customers who were "
        "tolerating a bad fit now have a reason to act on it. Churn arrives one or two quarters "
        "later, so the connection to the price change is easy to miss.</p>"
        "<p>The damage compounds because the churn looks like a product problem.</p>"
        "<p>Teams then ship features to fix a structural issue. That misdiagnosis is the subject of "
        "our piece on " + ilink(L_FEAT, "feature optimization and retention") + ".</p>"
    )
))

# ---- S5
blocks.append(container(
    heading("h2", "Do I apply the change to existing customers or only new ones?", "existing") +
    text(
        "<p>Start with new logos, then migrate the existing base deliberately and in waves.</p>"
        "<p>New customers give you clean signal with no switching cost and no broken promise. You "
        "learn whether the structure sells before you ask anyone to accept a change.</p>"
        "<p>Running both at once means you cannot tell which cohort produced which result. That "
        "makes the whole exercise unreadable.</p>"
    ) +
    heading("h3", "Grandfathering as a decision, not a courtesy") +
    text(
        "<p>Grandfathering feels generous, so founders do it by default. Do it on purpose instead, "
        "because a permanent legacy tier is a permanent operational cost.</p>"
        "<p>Three workable positions exist:</p>"
        "<ul>"
        "<li>Grandfather forever on price, but not on new features</li>"
        "<li>Grandfather for a fixed window, usually twelve to eighteen months</li>"
        "<li>Migrate everyone at renewal, with real notice</li>"
        "</ul>"
        "<p>Pick one and write it down before the first customer asks. Deciding this live, on a "
        "call, is how exceptions become policy.</p>"
    ) +
    heading("h3", "Who tells the customer, and when") +
    text(
        "<p>Your team tells them, before the invoice does. A repackage that a customer discovers "
        "from a billing email reads as a bait and switch.</p>"
        "<p>Segment the message. Accounts that gain from the new structure need a short note. "
        "Accounts that lose access to something need a conversation and an option.</p>"
    )
))

# ---- S6
blocks.append(container(
    heading("h2", "What evidence do I need before I move?", "evidence") +
    text(
        "<p>You need three inputs, and none of them is a willingness-to-pay survey.</p>"
        "<p>Surveys ask people to predict their own behaviour about money. That prediction is "
        "unreliable, and it is most unreliable exactly where the stakes are highest.</p>"
    ) +
    heading("h3", "Three inputs that beat a survey") +
    text(
        "<p>Start with your own transaction record. It already contains the answer.</p>"
        "<ul>"
        "<li>Discount data by segment, which shows where your list price is fiction</li>"
        "<li>Usage against paid tier, which exposes a broken value metric in one chart</li>"
        "<li>Lost-deal reasons written by the rep at the time, not recalled later</li>"
        "</ul>"
        "<p>Add one qualitative layer. Interview ten customers who upgraded and ten who did not. "
        "Ask what changed in their business, not what they would pay.</p>"
    ) +
    heading("h3", "Why there is no benchmark to copy") +
    text(
        "<p>There is no neutral public dataset on this decision. Treat that as a finding, not as a "
        "gap in your research.</p>"
        "<p>We looked. The widely repeated figures on pricing and retention trace back to billing "
        "vendors, pricing consultancies, and venture funds. Each has a commercial interest in the "
        "answer, and none publishes the underlying sample.</p>"
        "<p>So we quote none of them here. Argue from your own transaction data instead, and from "
        "the mechanism. Your own numbers are the only ones that describe your buyers.</p>"
    ) +
    heading("h3", "What stage you are at changes the answer") +
    text(
        "<p>Before repeatable fit, packaging is a guess. You do not have enough patterns to "
        "structure tiers around, so keep the offer simple and learn.</p>"
        "<p>Confirm the pattern first using " + ilink(L_PMF, "product-market fit signals") +
        ", then package. And read the result against the right yardstick, because "
        + ilink(L_METR, "growth metrics by stage") + " differ sharply between startup and "
        "scale-up.</p>"
    )
))

# image slot 3
blocks.append("<!--IMG-SLOT-3-->")

# ---- S7
blocks.append(container(
    heading("h2", "What do founders get wrong when they finally act?", "mistakes") +
    text(
        "<p>They change too much at once, then cannot read the result.</p>"
        "<p>Picture one release that moves the value metric, redraws three tiers, and lifts price. "
        "It produces a single outcome with four possible causes. You have spent the experiment and "
        "learned nothing.</p>"
    ) +
    heading("h3", "Changing everything in one release") +
    text(
        "<p>Sequence the moves so each one is readable. Metric, then tiers, then limits, then "
        "price.</p>"
        "<p>Yes, it is slower. It is also the only version where you know what worked. Speed to ROI "
        "comes from making the right call once, not from shipping four changes in a week.</p>"
    ) +
    heading("h3", "Letting the discount rate hide the real price") +
    text(
        "<p>Your list price is not your price if you discount most deals. Founders raise list, reps "
        "discount harder, and realised price does not move.</p>"
        "<p>Measure realised price per account before and after. If the gap between list and "
        "realised is widening, the problem is the package or the segment, not the number.</p>"
    ) +
    heading("h3", "Treating it as a one-time project") +
    text(
        "<p>Packaging drifts because your product ships and your market moves. A structure built "
        "two years ago describes a company that no longer exists.</p>"
        "<p>Put it on a cycle. Review the value metric annually, the tier limits every six months, "
        "and the discount data every quarter.</p>"
    )
))

# ---- Related reading
blocks.append(container(
    heading("h3", "Related Reading") +
    text(
        rr(L_REP, "When to hire your first sales rep in B2B SaaS") +
        rr(L_COORD, "Coordinated growth versus brute-force scaling")
    ),
    bg=True
))

# ---- Conclusion
blocks.append(container(
    heading("h2", "Conclusion", "conclusion") +
    text(
        "<p>The instinct to raise price is usually a symptom, not a strategy. It is the fastest "
        "lever within reach, which is exactly why it gets pulled first.</p>"
        "<p>Do the boring diagnostic instead. Sort your losses by where they happened, then rank usage "
        "against spend. Then read what your discount rate has been telling you.</p>"
        "<p>Then move in order. Metric, tiers, limits, number. New logos before the installed base, "
        "with the grandfathering rule written down in advance.</p>"
        "<p>Stop debating. Ship the plan.</p>"
    )
))

# ---- FAQ
FAQ = [
    ("Is a price increase ever the right first move?",
     "<p>Yes, in one situation. Your packaging already matches how customers get value, and your "
     "discount rate is low and stable. Then the number is genuinely the constrained variable.</p>"
     "<p>That is rarer than founders expect. Check the usage-against-spend chart before you accept "
     "that you are in it.</p>"),
    ("How much can we raise price without triggering churn?",
     "<p>No honest general number exists, and anyone quoting one is guessing on your behalf.</p>"
     "<p>Tolerance depends on switching cost, contract length, and how visible your line item is in "
     "the customer's budget. Test on new logos and read the win rate before you touch renewals.</p>"),
    ("Should we publish prices on the website?",
     "<p>Publish when your packaging is stable and self-selection is possible. Hide prices only "
     "while scope genuinely varies per deal.</p>"
     "<p>Hidden pricing is often a packaging confession. If you cannot publish a number, it is "
     "usually because you have not decided what a tier contains.</p>"),
    ("How many tiers should we have?",
     "<p>Enough that each one has a distinct buyer, and no more. Most B2B SaaS companies land on "
     "three plus an enterprise conversation.</p>"
     "<p>The test is not the count. It is whether a prospect can pick their tier in under a minute "
     "without help.</p>"),
    ("What if a competitor just undercut us?",
     "<p>Do not match on price by reflex. A competitor's number reflects their cost base, their "
     "funding, and their segment, none of which are yours.</p>"
     "<p>Check whether you are losing deals to them or just hearing about them. Those are different "
     "problems with different fixes.</p>"),
    ("Who should own pricing and packaging internally?",
     "<p>One named owner, usually the founder or the head of product, with finance and sales as "
     "required inputs.</p>"
     "<p>Shared ownership is how packaging decisions stall. Someone has to be able to say no to a "
     "one-off exception and make it stick.</p>"),
]
blocks.append(container(
    heading("h2", "Frequently asked questions", "faq") + accordion(FAQ)
))

# ---- CTA
blocks.append(container(
    text(
        "<p>You do not have unlimited quarters to test this. Price, packaging, or something further "
        "upstream could be holding revenue flat.</p>"
        "<p>Find out which, before you commit a quarter to the wrong one.</p>"
        "<p>" + ilink(L_QUIZ, "Pinpoint your #1 growth lever") + " in three minutes.</p>"
    ),
    bg=True
))

html = ('<div data-elementor-type="wp-post" data-elementor-id="NEWID" class="elementor elementor-NEWID '
        'elementor-bc-flex-widget" data-elementor-post-type="post">' + "".join(blocks) + '</div>')

with io.open(sys.argv[1], "w", encoding="utf-8") as f:
    f.write(html)
print("bytes", len(html))
