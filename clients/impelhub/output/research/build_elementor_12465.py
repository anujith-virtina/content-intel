#!/usr/bin/env python3
"""
Build and push _elementor_data JSON for ImpelHub post 12465.
Structure modelled EXACTLY on live post 12433 (product-market fit signals).
Confirmed CSS from post 12433 live page:
  Container: --display:flex;--margin-top:35px;--margin-bottom:0px  (no gap/flex_size/width_laptop)
  H2: font-size:26px;font-weight:700;line-height:1.35em;color:#0d0b1e
  H3: font-size:20px;font-weight:700;line-height:1.4em;color:#0d0b1e  (no blog-title-h2 class)
  Text editor: font-size:16px;line-height:1.8em
  TOC/callout: inline HTML in text-editor widget (not Elementor callout container)
  n-accordion: custom_css copied from post 12433 live data (#FD9ED0 pink)
"""
import os, sys, json, base64, random
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

env_path = Path(r"C:\content-intel\.env")
if env_path.exists():
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

import requests, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

USER = os.environ.get("IMPELHUB_WP_USERNAME", "")
PASS = os.environ.get("IMPELHUB_WP_APP_PASSWORD", "")
WP_BASE = "https://impelhub.com/wp-json/wp/v2"
POST_ID = 12465

auth_b64 = base64.b64encode(f"{USER}:{PASS}".encode()).decode()
AUTH = {"Authorization": f"Basic {auth_b64}"}
SESS = requests.Session()
SESS.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
    "Origin": "https://impelhub.com",
    "Referer": f"https://impelhub.com/wp-admin/post.php?post={POST_ID}&action=edit",
})

# ---- ID generator -------------------------------------------------------
_used = set()
def uid():
    while True:
        v = ''.join(random.choices('0123456789abcdef', k=8))
        if v not in _used:
            _used.add(v)
            return v

# ---- Colors -------------------------------------------------------------
BRAND = "#5736fd"        # ImpelHub purple
HEAD_COLOR = "#0d0b1e"   # heading color — confirmed from post 12433 live CSS
CALLOUT_BG = "#FBE9FF"   # TOC / Related Reading background
ACCORDION_COLOR = "#FD9ED0"  # n-accordion pink — confirmed from post 12433

# ---- Element builders (exact match to post 12433) ----------------------

def container(elements, margin_top=35):
    """Container exactly as post 12433 generates: only margin-top, no gap/flex_size/width_laptop."""
    s = {
        "content_width": "full",
        "padding": {"unit":"px","top":"0","right":"0","bottom":"0","left":"0","isLinked":True},
        "margin": {"unit":"px","top":str(margin_top),"right":"0","bottom":"0","left":"0","isLinked":False},
    }
    return {"id":uid(),"elType":"container","settings":s,"elements":elements,"isInner":False}

def h2(title, anchor=None):
    """H2 — confirmed from post 12433 live CSS: 26px/700/1.35em/#0d0b1e, blog-title-h2 class."""
    s = {
        "title": title,
        "header_size": "h2",
        "_css_classes": "blog-title-h2",
        "title_color": HEAD_COLOR,
        "typography_typography": "custom",
        "typography_font_size": {"unit":"px","size":26,"sizes":[]},
        "typography_font_weight": "700",
        "typography_line_height": {"unit":"em","size":1.35,"sizes":[]},
    }
    if anchor:
        s["css_id"] = anchor
    return {"id":uid(),"elType":"widget","widgetType":"heading","settings":s,"elements":[]}

def h3(title, anchor=None):
    """H3 — confirmed from post 12433 live CSS: 20px/700/1.4em/#0d0b1e, NO blog-title-h2 class."""
    s = {
        "title": title,
        "header_size": "h3",
        "title_color": HEAD_COLOR,
        "typography_typography": "custom",
        "typography_font_size": {"unit":"px","size":20,"sizes":[]},
        "typography_font_weight": "700",
        "typography_line_height": {"unit":"em","size":1.4,"sizes":[]},
    }
    if anchor:
        s["css_id"] = anchor
    return {"id":uid(),"elType":"widget","widgetType":"heading","settings":s,"elements":[]}

def te(html):
    """Text editor — confirmed from post 12433: 16px/1.8em, no widget margins."""
    return {"id":uid(),"elType":"widget","widgetType":"text-editor","settings":{
        "editor": html,
        "typography_typography": "custom",
        "typography_font_size": {"unit":"px","size":16,"sizes":[]},
        "typography_line_height": {"unit":"em","size":1.8,"sizes":[]},
    },"elements":[]}

def img(url, alt, media_id=0):
    return {"id":uid(),"elType":"widget","widgetType":"image","settings":{
        "image": {"url":url,"id":media_id,"alt":alt},
        "image_size": "full",
        "align": "center",
        "_css_classes": "blog-body-image",
    },"elements":[]}

def btn(text, url):
    return {"id":uid(),"elType":"widget","widgetType":"button","settings":{
        "text": text,
        "link": {"url":url,"is_external":False,"nofollow":False},
        "background_color": BRAND,
        "button_text_color": "#ffffff",
        "border_radius": {"unit":"px","top":"4","right":"4","bottom":"4","left":"4","isLinked":True},
        "size": "md",
    },"elements":[]}

def styled_box(title, html_body):
    """Inline styled box (TOC, Related Reading) — post 12433 TOC has empty settings {}, just editor content."""
    inner = (
        f'<div style="background:{CALLOUT_BG};border-radius:8px;padding:18px 24px;">'
        f'<div style="font-weight:700;color:{HEAD_COLOR};font-size:18px;margin-bottom:8px;">{title}</div>'
        f'{html_body}'
        f'</div>'
    )
    return {"id":uid(),"elType":"widget","widgetType":"text-editor",
            "settings":{"editor": inner},"elements":[]}

def n_accordion(qas):
    """n-accordion — exact custom_css copied verbatim from live post 12433."""
    items = [{"_id": uid(), "item_title": q} for q, a in qas]
    elems = [
        {"id": uid(), "elType": "container", "settings": {"content_width": "full"},
         "elements": [te(a)]}
        for q, a in qas
    ]
    css = (
        "selector { --n-accordion-title-hover-color: #FD9ED0; --n-accordion-title-active-color: #FD9ED0; "
        "--n-accordion-title-justify-content: space-between; --n-accordion-title-flex-grow: 1; "
        "--n-accordion-title-icon-order: initial; --n-accordion-border-radius: 0px 0px 0px 0px; "
        "--n-accordion-padding: 20px 0px 20px 0px; }\n"
        "selector .e-n-accordion-item-title-text { color: #FD9ED0 !important; font-size: 20px; "
        "font-weight: 400; line-height: 1.33em; flex: 1 1 auto; }\n"
        "selector .e-n-accordion-item-title-icon { color: #FD9ED0 !important; order: 0 !important; margin-left: auto; }\n"
        "selector .e-n-accordion-item-title-header { order: 0 !important; flex: 1 1 auto; }\n"
        "selector .e-n-accordion-item-title-icon svg { fill: #FD9ED0 !important; }\n"
        "selector > .e-n-accordion > .e-n-accordion-item > .e-n-accordion-item-title "
        "{ border-style: solid; border-width: 0px 0px 1px 0px; border-color: #D5D8DC; padding: 20px 0px; }\n"
        "selector > .e-n-accordion > .e-n-accordion-item[open] > .e-n-accordion-item-title "
        "{ border-style: none; }\n"
        "selector .e-n-accordion-item .e-con { padding: 0px 0px 20px 0px; }\n"
        "selector .elementor-widget-text-editor p "
        "{ color: #333333; font-size: 15px; font-weight: 400; line-height: 1.42em; font-family: Inter, sans-serif; }"
    )
    return {"id": uid(), "elType": "widget", "widgetType": "nested-accordion",
            "settings": {
                "items": items, "title_tag": "h4",
                "title_hover_color": ACCORDION_COLOR, "title_active_color": ACCORDION_COLOR,
                "title_typography_typography": "custom",
                "title_typography_font_size": {"unit":"px","size":20,"sizes":[]},
                "title_typography_font_weight": "400",
                "title_typography_line_height": {"unit":"em","size":1.33,"sizes":[]},
                "icon_color": ACCORDION_COLOR, "icon_hover_color": ACCORDION_COLOR,
                "icon_active_color": ACCORDION_COLOR,
                "icon_size": {"unit":"px","size":15,"sizes":[]},
                "border_radius": {"unit":"px","top":"0","right":"0","bottom":"0","left":"0","isLinked":True},
                "padding": {"unit":"px","top":"20","right":"0","bottom":"20","left":"0","isLinked":False},
                "title_space_between": {"unit":"px","size":0,"sizes":[]},
                "title_distance_from_content": {"unit":"px","size":0,"sizes":[]},
                "header_border_border": "solid",
                "header_border_width": {"unit":"px","top":"0","right":"0","bottom":"1","left":"0","isLinked":False},
                "header_border_color": "#D5D8DC",
                "custom_css": css,
            },
            "elements": elems}

# ---- Content ------------------------------------------------------------

TOC_BODY = (
    '<ol style="margin:0;padding-left:20px;color:#0d0b1e;font-size:16px;line-height:1.8;">'
    '<li><a href="#tldr">TL;DR: Key Takeaways</a></li>'
    '<li><a href="#why-churn-diagnosis-beats-tactics">Why diagnosis comes before any tactic</a></li>'
    '<li><a href="#three-root-causes">The three root causes of early-stage churn</a></li>'
    '<li><a href="#decision-branch-fit">Branch 1: Is this a wrong-fit customer problem?</a></li>'
    '<li><a href="#decision-branch-onboarding">Branch 2: Is this an onboarding failure?</a></li>'
    '<li><a href="#decision-branch-product">Branch 3: Is this a real product gap?</a></li>'
    '<li><a href="#sequence-and-hiring">When to hire for retention, and when not to</a></li>'
    '<li><a href="#related-reading">Related reading</a></li>'
    '<li><a href="#conclusion">The sequence is the strategy</a></li>'
    '<li><a href="#faq">FAQ</a></li>'
    '</ol>'
)

TLDR_HTML = (
    f'<p><span style="color:{BRAND};">&#8594;</span> Churn has three root causes: wrong-fit customers, onboarding failure, and a real product gap. Each requires a completely different fix.</p>'
    f'<p><span style="color:{BRAND};">&#8594;</span> 60&#8211;70% of annual SaaS churn happens in the first 90 days. That number tells you where to look first.</p>'
    f'<p><span style="color:{BRAND};">&#8594;</span> Before you hire a CS manager, build a retention process, or fix the product: run the diagnostic. Sequence is everything.</p>'
    f'<p><span style="color:{BRAND};">&#8594;</span> If your monthly churn is above 3.5%, you do not have a retention problem. You have a diagnosis problem.</p>'
    f'<p><span style="color:{BRAND};">&#8594;</span> Involuntary churn (failed payments) accounts for 20&#8211;40% of total churn and is the easiest fix. Check it today.</p>'
    f'<p><span style="color:{BRAND};">&#8594;</span> The goal is not to keep every customer. It is to keep the right customers. ICP tightening reduces churn without adding headcount.</p>'
)

RR_BODY = (
    '<ul style="margin:0;padding-left:20px;color:#0d0b1e;font-size:16px;line-height:1.8;">'
    f'<li><a href="https://impelhub.com/blog/product-market-fit-signals-b2b-saas/" style="color:{BRAND};">Confirm your ICP before you blame churn: Product-Market Fit Signals: 10 Markers B2B SaaS Founders Should Pass Before Scaling</a></li>'
    f'<li><a href="https://impelhub.com/blog/when-to-hire-first-sales-rep-b2b-saas/" style="color:{BRAND};">The sales rep readiness playbook: When to Hire Your First Sales Rep in B2B SaaS</a></li>'
    '</ul>'
)

FAQ_QAS = [
    ("What is a good B2B SaaS churn rate for an early-stage company?",
     "<p>The average monthly churn benchmark for B2B SaaS is around 3.5%. Top performers stay below 2% monthly. At seed stage, monthly churn above 5% is a diagnostic signal, not just a retention problem to fix. It usually points to ICP mismatch rather than anything a retention campaign can solve. Run the root cause diagnostic before investing in any retention tactic.</p>"),
    ("How do I know if my churn is a product problem or a fit problem?",
     "<p>The timing and engagement depth tell you. If churned customers were in-ICP, completed onboarding, reached the activation event, and still left after month three, it is a product gap. If they churned within 60 days without activating, it is a fit or onboarding problem. Wrong-fit customers churn early and shallow. Product-gap customers churn late and deep, after real usage.</p>"),
    ("Should I hire a customer success manager to reduce churn?",
     "<p>Not until you have run the three-question CS hire test and confirmed that your root cause is onboarding failure or a product gap, not ICP mismatch. A CS hire does not fix a fit problem. Most early-stage founders make this hire before the root cause is confirmed and then wonder why churn does not improve. Diagnose first. Hire second.</p>"),
    ("What is involuntary churn and how do I fix it?",
     "<p>Involuntary churn is failed payment churn: expired cards, insufficient funds, bank declines. It accounts for 20&#8211;40% of total churn in most SaaS businesses and is the fastest, cheapest fix available. Set up a dunning email sequence (3&#8211;4 automated emails triggered by a failed charge) and enable a card updater through your payment processor. This takes one afternoon and can recover a significant portion of churned revenue with no product work required.</p>"),
    ("How do I calculate time-to-value (TTV) for my product?",
     "<p>TTV is the time between a customer&#8217;s first login and the activation event: the single action most strongly correlated with 90-day retention. Find your activation event first by segmenting retained versus churned customers on individual actions and identifying which action most cleanly separates the two groups. Then measure how many days it takes a new customer to reach that action. Reducing TTV is the fastest structural fix for onboarding-driven churn.</p>"),
    ("When should I start worrying about net revenue retention (NRR)?",
     "<p>NRR becomes your primary metric once you have 20 or more customers and some expansion revenue to track. Pre-$1M ARR, focus on gross logo retention first. NRR matters when expansion revenue from existing customers is large enough to offset churned logos. Until then, churn rate and 90-day cohort retention are the numbers that matter most.</p>"),
]

# ---- Build JSON ---------------------------------------------------------

data = [
    # 1. TL;DR
    container([
        h2("TL;DR: Key Takeaways", anchor="tldr"),
        te(TLDR_HTML),
    ]),

    # 2. Table of Contents — inline styled box matching post 12433 TOC
    container([
        styled_box("Table of Contents", TOC_BODY),
    ]),

    # 3. Why diagnosis comes before any tactic
    container([
        h2("Why diagnosis comes before any tactic", anchor="why-churn-diagnosis-beats-tactics"),
        te("<p>Tactics applied to the wrong root cause do not reduce churn. They burn time and money while the real problem compounds. That is the dirty secret behind most failed retention programs at early-stage companies.</p>"
           "<p>You have probably tried at least two of the standard moves: an onboarding checklist, an NPS survey, a check-in email sequence. They did not move the number. Not because you executed poorly. Because you were treating a symptom, not the cause.</p>"),
        h3("The tactic trap: why most churn advice is backwards"),
        te("<p>Most churn articles hand you a list: improve onboarding, run QBRs, build a health score dashboard. Every item on that list assumes you already know which problem you have. You do not. Not yet.</p>"
           "<p>The churn root cause analysis comes first. Every other move is a guess until you have run it. Acquiring a new customer costs at least 5x more than retaining one. That ratio makes getting the diagnosis right worth more than any individual tactic.</p>"),
        h3("What the 90-day churn signal tells you"),
        te("<p>Here is your first diagnostic signal: when does most of your churn happen? Research consistently shows that 60&#8211;70% of annual SaaS churn occurs inside the first 90 days. Churn concentrated at that scale tells you the problem is upstream: fit or onboarding, not deep product functionality.</p>"
           "<p>If your churn is spread evenly across the customer lifecycle, the hypothesis shifts. Customers who stuck around for six months and then left usually had the right fit and completed onboarding. Something else failed them. That is where the product gap hypothesis earns serious consideration.</p>"
           "<p>The 90-day window is your first filter. Use it before you do anything else.</p>"),
    ]),

    # 4. Three root causes
    container([
        h2("The three root causes of early-stage churn", anchor="three-root-causes"),
        te("<p>Every B2B SaaS churn problem traces back to one of three root causes. They look similar on the surface. They require completely different responses.</p>"),
        h3("Root cause 1: wrong-fit customers"),
        te("<p>Wrong-fit customers churn because your product was never the right solution for their actual problem. They may have looked like your ICP at the point of sale. They were not. The symptom: churn concentrated in the first 60 days, support tickets about use cases your product was not built for, and exit surveys that say &#8220;not what we expected.&#8221;</p>"
           "<p>This is a top-of-funnel problem, not a retention problem. Hiring a CS manager to fix it is like hiring a doctor to fix a broken supply chain. The fix happens upstream.</p>"),
        h3("Root cause 2: onboarding failure (they never got value)"),
        te("<p>Onboarding failure means your customer had the right problem, your product solves it, but they never reached the moment where that became obvious to them. They churned not because the product failed, but because they never experienced it succeeding. This is far more fixable than a product gap.</p>"
           "<p>The signal: good-fit customers who churned within 90 days. Customers who opened onboarding emails but never completed setup. Low engagement in the first two weeks despite a clean contract.</p>"),
        h3("Root cause 3: a real product gap"),
        te("<p>A product gap means your customer was in-ICP, completed onboarding, activated, and still left. They needed something your product does not yet deliver at the depth or breadth they require. This is the hardest root cause to confirm and the most expensive to fix. But it is also the most specific, which makes it actionable once confirmed.</p>"
           "<p>One more thing to check before you run any of the three branches: voluntary vs involuntary churn. Involuntary churn&#8212;failed payments and expired cards&#8212;accounts for 20&#8211;40% of total churn in most early-stage SaaS businesses. Fix billing recovery first. It takes one afternoon and can recover a meaningful slice of churned revenue with zero product or CS work required.</p>"),
    ]),

    # 5. Image 1
    container([
        img("https://impelhub.com/wp-content/uploads/2026/06/PLACEHOLDER-analytics-dashboard.jpg",
            "Founder reviewing business analytics dashboard to diagnose B2B SaaS churn root cause"),
    ], margin_top=20),

    # 6. Branch 1: fit problem
    container([
        h2("Branch 1: is this a wrong-fit customer problem?", anchor="decision-branch-fit"),
        te("<p>ICP drift is the most common and least diagnosed churn driver at the seed to Series A stage. If your monthly churn is above 5% and most of it lands in the first 60 days, ICP mismatch is the most likely culprit. Run this check before anything else in Branch 1.</p>"),
        h3("How to tell if ICP drift is your churn driver"),
        te(f'<p>Pull your last 10&#8211;15 churned customers. Score each one against your current ICP definition: company size, industry, buying role, job-to-be-done, budget range. Be honest. Would you take this customer today?</p>'
           f'<p>If 60% or more of your churned accounts score outside your ICP, the problem is acquisition. Your sales motion is accepting customers it should not. Check your <a href="https://impelhub.com/blog/product-market-fit-signals-b2b-saas/" style="color:{BRAND};font-weight:500;">product-market fit signal checklist</a> to confirm whether your ICP definition itself needs tightening before you change the sales filter.</p>'
           f'<p>Three signals that confirm a fit problem: churned customers cite use cases your product was not designed for, they generated above-average support volume per dollar of ACV, and they never reached the activation event that retained customers typically hit in the first two weeks.</p>'),
        h3("The fix: tighten before you scale"),
        te("<p>The fix for a fit problem is not a retention program. It is tighter acquisition criteria. Add a qualification gate at the discovery call stage. Define the two or three ICP attributes that most strongly predict 90-day retention, and make those non-negotiables in your sales process.</p>"
           "<p>Research consistently shows that companies with tightly scored ICP criteria have churn rates 30&#8211;40% lower than those running with loosely defined customer profiles. You do not need more customers. You need the right ones. Tightening here improves customer health scores, reduces support load, and compounds into cleaner NRR metrics within two to three quarters.</p>"
           "<p>One wrong-fit customer costs you the sale commission, the implementation cost, the support hours, and the reference damage when they leave loudly. The cost of one bad fit is not one lost logo. It is the compounding drag it creates before it finally churns.</p>"),
    ]),

    # 7. Branch 2: onboarding failure
    container([
        h2("Branch 2: is this an onboarding failure?", anchor="decision-branch-onboarding"),
        te("<p>Onboarding failure is the most fixable churn driver for early-stage SaaS with genuine product-market fit. If your in-ICP customers churn before they reach their first key outcome, this branch is yours.</p>"),
        h3("The time-to-value test"),
        te("<p>Time-to-value (TTV) is the gap between a customer&#8217;s first login and the moment they complete the one action that most strongly predicts 90-day retention. That action is your activation event. You may not know what it is yet. Find it first.</p>"
           "<p>Segment your retained customers versus churned customers on a single action: completing setup, running their first report, inviting a team member. The action that cleanly separates retained from churned is your activation event. Companies with TTV under seven days see roughly 50% lower churn rates than those where first value takes two weeks or more.</p>"
           "<p>If you do not have enough data to run this segmentation reliably, call your last five retained customers and your last five churned customers. Ask both groups to describe the first time the product felt useful. The difference in that story is your TTV problem in plain language.</p>"),
        h3("What a minimal onboarding fix actually looks like"),
        te(f'<p>You do not need an onboarding platform or a CS team to fix this. You need one thing: redesign the first session to front-load the activation event. Remove every step that does not lead to it. Cut setup friction. Automate the pre-work where possible.</p>'
           f'<p>For high-ACV customers ($1,000 or more per month per seat), add a single human touchpoint in the first 14 days. A 20-minute call at day seven, with the specific goal of getting them to the activation event during that call, is worth more than any onboarding email sequence. You should look at <a href="https://impelhub.com/blog/feature-prioritization-business-growth/" style="color:{BRAND};font-weight:500;">feature prioritization for retention</a> to identify which features should be surfaced first in that session.</p>'
           f'<p>Do not hire a CS manager to fix an onboarding problem until you have validated the minimal fix. A founder personally running 10&#8211;15 of these calls provides more diagnostic signal than a CS hire in the first three months.</p>'),
    ]),

    # 8. Branch 3: product gap
    container([
        h2("Branch 3: is this a real product gap?", anchor="decision-branch-product"),
        te("<p>A confirmed product gap is actually good news. It is the most specific churn problem you can have, which means it is the most actionable. The diagnostic is clear: if churned customers were inside your ICP, completed onboarding, reached the activation event, and still left after month three, there is a real product gap.</p>"),
        h3("How to tell product gap from fit problem"),
        te("<p>The distinguishing factor is timing and depth of engagement. Wrong-fit customers churn early and shallow: they never activated, never generated meaningful usage, and often cannot articulate what they wanted instead. Product-gap churn is late and deep: the customer used the product regularly, derived some value, and still left because the product did not go far enough for their use case.</p>"
           "<p>Exit interview signals that confirm a product gap: &#8220;We outgrew it,&#8221; &#8220;We needed [specific feature] that wasn&#8217;t there,&#8221; or &#8220;It worked for X but not for Y.&#8221; These customers were not disappointed. They were limited. That is a different conversation entirely.</p>"
           "<p>Use a Feature Gap Analysis to map these requests against your ICP&#8217;s documented jobs-to-be-done. Group the gaps by frequency and by ACV of the customers requesting them. That prioritization tells you what to build next, and what to deliberately not build, with more precision than any product roadmap debate.</p>"),
        h3("The dangerous middle: when the product works but not enough"),
        te("<p>There is a version of the product gap problem that is more dangerous than a clean feature miss: the product works for a narrow use case and churns for everything beyond it. Founders here get stuck in a rebuild loop, adding features indefinitely to chase a broader ICP, while their actual high-retention segment is the narrow one they already serve well.</p>"
           "<p>The right move is often the counterintuitive one: re-scope the ICP to match what the product already solves deeply. You are not narrowing. You are precision-targeting. Customers in that focused segment will have stronger customer health scores, lower support loads, and better expansion revenue potential than a broadly targeted base that half-fits your product.</p>"),
    ]),

    # 9. When to hire
    container([
        h2("When to hire for retention, and when not to", anchor="sequence-and-hiring"),
        te("<p>The customer success hiring trigger is one of the most mis-timed decisions in early-stage SaaS. Most founders hire a CS manager before they know which root cause they are solving. That hire then fails to move the churn number, because no CS hire fixes a fit problem or a product gap.</p>"),
        h3("The three-question CS hire test"),
        te(f'<p>Before you post the job description, answer three questions. All three must be yes. One no and you are not ready.</p>'
           f'<p>First: is your root cause onboarding failure or product gap, not ICP mismatch? A fit problem requires a tighter acquisition filter. CS cannot fix that.</p>'
           f'<p>Second: is your monthly churn above 3% and your ACV above $500 per month? Below those numbers, a manual founder-led process beats a CS hire on both cost and signal.</p>'
           f'<p>Third: do you have 10 or more customers who activated and are still churning? Below that threshold, you do not have enough signal to know what you are hiring CS to solve. Review the <a href="https://impelhub.com/blog/when-to-hire-first-sales-rep-b2b-saas/" style="color:{BRAND};font-weight:500;">first sales hire readiness criteria</a> for parallel logic on timing a role before you are ready for it.</p>'),
        h3("What to do before you hire"),
        te(f'<p>Three things you can do now, without a CS hire, that will move the number. First: set up a dunning email sequence for involuntary churn. Failed payment recovery alone can recover 20&#8211;40% of churned revenue with a one-time setup.</p>'
           f'<p>Second: add an activation event tracker to your CRM. Tag every customer with the date they hit the activation event. Your 90-day cohort analysis becomes precise and your intervention points become obvious.</p>'
           f'<p>Third: run a week-two check-in call personally for your next 10 new customers. The signal from those calls is worth more than any customer health score dashboard you could buy. When you do eventually scale past these manual systems, monitoring <a href="https://impelhub.com/blog/ai-sales-analytics-churn-cltv/" style="color:{BRAND};font-weight:500;">customer lifetime value signals</a> during this manual phase gives you the CLTV and expansion revenue baselines you need to size the CS investment correctly.</p>'),
    ]),

    # 10. Image 2
    container([
        img("https://impelhub.com/wp-content/uploads/2026/06/PLACEHOLDER-startup-team-planning.jpg",
            "Small startup team in planning meeting deciding when to hire first customer success manager for B2B SaaS"),
    ], margin_top=20),

    # 11. Related Reading — inline styled box, same pattern as TOC
    container([
        h2("Related Reading", anchor="related-reading"),
        styled_box("Related Reading", RR_BODY),
    ]),

    # 12. Conclusion + CTA
    container([
        h2("The sequence is the strategy", anchor="conclusion"),
        te("<p>Most founders treat churn as a retention problem. It is a diagnosis problem. The tactic you need depends entirely on the root cause you have. Apply the wrong tactic to the wrong cause and you spend the quarter on work that cannot move the number.</p>"
           "<p>Run the 90-day filter first. Sort voluntary from involuntary churn. Then walk the three branches: fit, onboarding, product. Each one has a distinct signal pattern and a distinct fix sequence. The diagnostic is fast. A few hours of data and five customer calls will get you to the right branch.</p>"
           "<p>Stop guessing at symptoms. Diagnose the root cause. Your move.</p>"),
        btn("Pinpoint your #1 growth lever",
            "https://impelhub.com/find-out-where-your-business-should-focus-next-for-growth-in-just-3-minutes/"),
    ]),

    # 13. FAQ
    container([
        h2("Frequently Asked Questions (FAQs)", anchor="faq"),
        n_accordion(FAQ_QAS),
    ]),
]

elementor_json = json.dumps(data, ensure_ascii=False)
print(f"Elementor JSON built: {len(elementor_json):,} chars, {len(data)} top-level sections")

out = Path(r"C:\content-intel\clients\impelhub\output\research\post12465_elementor_data.json")
out.write_text(elementor_json, encoding="utf-8")
print(f"Saved locally: {out}")

print(f"\nPATCHing post {POST_ID}...")
payload = {
    "meta": {
        "_elementor_data": elementor_json,
        "_elementor_edit_mode": "builder",
        "_elementor_template_type": "wp-post",
    },
    "excerpt": "Most early-stage B2B SaaS founders fix the wrong churn problem. Diagnose root cause first: ICP fit, onboarding failure, or product gap. Then fix in sequence.",
}
r = SESS.post(
    f"{WP_BASE}/posts/{POST_ID}",
    headers={**AUTH, "Content-Type": "application/json"},
    json=payload, timeout=180, verify=False
)
print(f"PATCH status: {r.status_code}")
if r.status_code in (200, 201):
    d = r.json()
    meta = d.get("meta", {})
    ed_len = len(meta.get("_elementor_data", ""))
    print(f"  _elementor_edit_mode = {repr(meta.get('_elementor_edit_mode',''))}")
    print(f"  _elementor_data length returned = {ed_len}")
    print(f"  Post status = {d.get('status')}")
    print(f"  Post link = {d.get('link')}")
    if ed_len > 1000:
        print("  SUCCESS")
    else:
        print(f"  WARNING - data seems short: {ed_len} chars")
else:
    print(f"FAILED: {r.text[:1000]}")
