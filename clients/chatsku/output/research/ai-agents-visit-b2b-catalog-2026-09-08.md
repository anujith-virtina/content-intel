---
title: What AI agents actually get when they visit a real B2B catalog
client: chatsku
date: 2026-09-08
topic: A hands-on audit of 20 real B2B distributor catalogs, testing what an AI agent can reach and read
audience: Sales and ops leaders at B2B manufacturers, distributors and wholesalers
stage: research
slug: ai-agents-b2b-catalog-audit
---

# The audit

**This is first-party data. Every number below came from running two scripts against
20 real, public B2B distributor and manufacturer catalogs on 2026-09-08.** Nothing here
is borrowed from a vendor blog or an SEO listicle, and nothing is modelled or estimated.

Scripts, both re-runnable:
- `clients/chatsku/output/research/agent_audit_robots.py` -> `agent_audit_robots.json`
- `clients/chatsku/output/research/agent_audit_product.py` + `agent_audit_product2.py` -> `agent_audit_product.json`

## Catalogs tested (20)

Grainger, McMaster-Carr, Fastenal, MSC Industrial, Motion Industries, Applied Industrial,
Zoro, Global Industrial, DigiKey, Mouser, Newark, Allied Electronics, Ferguson, Wesco,
Border States, Rexel USA, Hisco, Kaman, Genuine Parts, Sonepar.

All are real distributors or manufacturers. None is a ChatSKU competitor.

## Method, and its limits, stated plainly

- One request per host for `robots.txt`. One product page per host, found from the site's
  own declared sitemap, or failing that from a product link on its homepage.
- Requests were sent with a **normal desktop browser User-Agent**, not a bot User-Agent.
  A crawler identifying honestly as GPTBot or ClaudeBot would very likely do worse, not better.
- **JavaScript was not executed.** This matters and must be stated in the post. Some AI
  crawlers do not run JS at all; others render. What we measured is what a non-rendering
  retrieval client receives.
- **n = 20 hosts, one product page each. This is an audit, not a statistical sample.**
  Report counts ("5 of 20"), never extrapolated percentages of the industry.
- Snapshot taken 2026-09-08. Sites change.

---

# Finding 1: nobody is blocking AI agents on purpose

Of the 13 catalogs whose `robots.txt` could be read, **zero blocked any of the 12 AI agents
tested**: GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-User, PerplexityBot,
Perplexity-User, Google-Extended, CCBot, Amazonbot, Bytespider, meta-externalagent.

Not one `Disallow: /` against any of them. The published policy is open.

# Finding 2: 7 of 20 refused the connection anyway

Seven hosts would not answer a plain automated request at all, before any question of content:

| Host | Result |
|---|---|
| Fastenal | HTTP 403 |
| Motion Industries | HTTP 403 |
| Applied Industrial | HTTP 403 |
| Wesco | HTTP 403 |
| Hisco | HTTP 403 |
| Allied Electronics | connection timeout |
| Genuine Parts | connection timeout |

This is the gap that matters. **The policy layer says yes and the edge layer says no.**
The bot protection sitting in front of these catalogs does not read robots.txt, and the
team that configured it is usually not the team that wrote the robots file.

# Finding 3: only 5 of 20 produced a product page an agent could read

Of the 13 that answered at all:

- **7 exposed no product URL** that could be found in their sitemap or in their homepage
  HTML: Grainger, DigiKey, Mouser, Newark, Border States, Rexel USA, Sonepar. Their
  navigation is rendered client-side, so a non-rendering client sees no path to a product.
- **1 returned HTTP 403 on the product page** after serving robots.txt fine: Ferguson.
- **5 served a readable product page**: McMaster-Carr, MSC Industrial, Zoro,
  Global Industrial, Kaman.

**So 5 of 20 catalogs gave an agent anything to read at product level.**

# Finding 4: what those 5 pages actually contained

| Catalog | Visible words | JSON-LD blocks | Product schema | Price in structured data | Availability | Spec table rows |
|---|---|---|---|---|---|---|
| McMaster-Carr | 115 | 0 | no | no | no | 0 |
| MSC Industrial | 75 | 0 | no | no | no | 0 |
| Zoro | 689 | 1 | **yes** | **yes** | **yes** | 0 |
| Global Industrial | 784 | 3 | no | **yes** | **yes** | 18 |
| Kaman | 1,721 | 1 | no | no | no | 25 |

Totals across the 5: schema.org `Product` markup on **1 of 5**. Price in structured data on
**2 of 5**. Availability in structured data on **2 of 5**. A manufacturer part number or GTIN
in structured data on **2 of 5**. Zero of the 5 showed a login or quote wall, so the missing
data is not being withheld deliberately. It simply is not in the HTML.

**Two of the five returned under 200 visible words.** McMaster-Carr at 115 and MSC at 75 are
JavaScript shells to a non-rendering client. A human sees a full product page. A retrieval
client sees almost nothing.

# The honest headline

**Not one catalog blocked an AI agent in robots.txt, and 15 of 20 still gave an agent nothing
usable at product level.** The failure is not policy. It is infrastructure and markup.

That framing is defensible, first-party, and reproducible by any reader who runs the scripts.

---

# Stat discipline for the post

- Use **counts, not percentages**: "5 of 20", not "25% of B2B catalogs". n is 20.
- **State the method in the body**, including that JavaScript was not executed and that a
  browser User-Agent was used. The limits are part of the credibility.
- **Do not name a catalog in a negative claim** unless the post is willing to defend it.
  Recommended: name the set of 20 up front so the work is verifiable, then report findings
  in aggregate and name a company only where the finding is positive (Zoro's structured data,
  Global Industrial's spec table, Kaman's page depth). Naming McMaster and MSC as "JS shells"
  invites a fight ChatSKU does not need, and their pages may render fine for agents that
  execute JS.
- **Do not claim this predicts lost revenue.** No conversion or GMV number can be derived
  from this dataset.
- Nothing here needs the banned figures from earlier posts, and none are used.

# Fencing against existing ChatSKU posts

- Post 2129 `/agentic-commerce-glossary/` owns protocol definitions. Do not define ACP/AP2/MCP/A2A.
- Post 2684 `/erp-export-ai-agent-ready/` owns the **ERP export file** audit: GTIN integrity,
  duplicate SKUs, UNSPSC vs ETIM, UOM, EDI. This post is about the **public website**, which is a
  different surface. Link once, do not rebuild the field-level checks.
- Post 2831 `/what-is-agentic-commerce/` owns the plain-English definition for non-technical
  owners. This post is for sales and ops leaders and assumes the definition. Link once.
- `/ai-ready-b2b-catalog-autonomous-buying/` owns the persuasive machine-readable business
  case. Link, never quote its unsourced $15T/90% figure.
- Posts 2468 and 2665 own search and retrieval mechanics inside ChatSKU's own product.
