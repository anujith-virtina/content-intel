# -*- coding: utf-8 -*-
"""Virtina pre-publish QA. Enforces MUST-FOLLOW-RULES sections 3, 4b, 5, 6, 7, 9."""
import re, sys, html, os

p = sys.argv[1]
h = open(p, encoding='utf-8').read()
fails = []; warns = []; oks = []
def F(m): fails.append(m)
def W(m): warns.append(m)
def O(m): oks.append(m)

body = re.sub(r'<style.*?</style>', '', h, flags=re.S | re.I)
body = re.sub(r'<!--.*?-->', '', body, flags=re.S)
txt = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', body)))
wc = len(txt.split())
# line 324 allows two bands: 1500-2500 standard, 2500-3500 pillar guide.
# Reference posts 42074 and 42108 ship at 3843 and 4127, so the site runs long.
_band = "standard" if wc < 2500 else ("pillar" if wc <= 3500 else "OVER")
(O if 1500 <= wc <= 3500 else F)("word count %d (%s band; 1500-2500 standard, 2500-3500 pillar)" % (wc, _band))

# ---------- headings ----------
h2 = [html.unescape(re.sub('<[^>]+>', '', m)).strip()
      for m in re.findall(r'<h2[^>]*>(.*?)</h2>', body, re.S | re.I)]
h3 = [html.unescape(re.sub('<[^>]+>', '', m)).strip()
      for m in re.findall(r'<h3[^>]*>(.*?)</h3>', body, re.S | re.I)]
# the rule counts H3 *subheadings inside H2 sections*; the TOC's own H3 is not one
h3body = [x for x in h3 if x.lower().strip(' :') != 'table of contents']
(O if len(h3body) >= 6 else F)("body H3 count %d (need >=6, TOC H3 excluded)" % len(h3body))

BADH3 = {'overview', 'background', 'introduction', 'summary'}
bad = [x for x in h3 if x.lower().strip(' :?') in BADH3]
(O if not bad else F)("banned generic H3 text: %s" % bad)

h2tags = re.findall(r'<h2([^>]*)>', body, re.I)
noid = [t for t in h2tags if 'id=' not in t.lower()]
(O if not noid else F)("H2 tags missing id attribute: %d" % len(noid))

ids = re.findall(r'<h2[^>]*id=["\']([^"\']+)["\']', body, re.I)
anchors = re.findall(r'<a[^>]*href=["\']#([^"\']+)["\']', body, re.I)
missing = [a for a in anchors if a not in ids]
(O if not missing else F)("TOC anchors with no matching H2 id: %s" % missing)

# ---------- 4b content standards ----------
pbody = re.sub(r'<(h[1-6])[^>]*>.*?</\1>', ' ', body, flags=re.S | re.I)
# drop the TOC block: a <p>/<div> carrying 3+ in-page anchors is navigation, not prose
def _is_toc(frag):
    return len(re.findall(r'href=.#', frag)) >= 3
pbody = ''.join('' if _is_toc(seg) else seg for seg in
                re.split(r'(<p[^>]*>.*?</p>|<div[^>]*>.*?</div>|<ul[^>]*>.*?</ul>|<ol[^>]*>.*?</ol>)', pbody, flags=re.S | re.I))
paras = re.findall(r'<p[^>]*>(.*?)</p>', pbody, re.S | re.I)
badp = 0; longs = []
for pr in paras:
    t = html.unescape(re.sub('<[^>]+>', '', pr)).strip()
    # a sentence can end .  ."  .'  .)  .”  so allow one closing mark after the stop
    t = re.sub(r'([.!?])["’”\')\]]+(\s)', r'\1\2', t)
    s = [x for x in re.split(r'(?<=[.!?])\s+', t) if len(x.split()) >= 4]
    if len(s) >= 4:
        badp += 1
    for x in s:
        if len(x.split()) > 20:
            longs.append((len(x.split()), x[:64]))
(O if badp == 0 else F)("paragraphs with 4+ sentences = %d" % badp)
msg = "sentences over 20 words = %d" % len(longs)
if longs:
    msg += "; worst %dw: %s" % (longs[0][0], longs[0][1])
(O if not longs else F)(msg)

# ---------- 7 banned characters ----------
ems = h.count(u'—') + h.count('&mdash;') + h.count('&#8212;') + h.count('&#x2014;')
(O if ems == 0 else F)("em dashes (all 4 forms) = %d" % ems)

# ---------- 3 images ----------
imgs = re.findall(r'<img[^>]*>', body, re.I)
for bad_src in ('source.unsplash.com', 'placehold.co'):
    (O if bad_src not in h else F)("forbidden image host %s" % bad_src)
if imgs:
    offsite = [i for i in imgs if 'src=' in i and 'virtina.com/wp-content/uploads/' not in i]
    (O if not offsite else F)("body images not on virtina uploads: %d" % len(offsite))
    noalt = [i for i in imgs if 'alt=' not in i.lower()]
    (O if not noalt else F)("images missing alt: %d" % len(noalt))
    alts = re.findall(r'<img[^>]*alt=["\']([^"\']*)["\']', body, re.I)
    badalt = [len(a) for a in alts if not (80 <= len(a) <= 150)]
    (O if not badalt else F)("alt text outside 80-150 chars: %s" % badalt)
    (O if len(set(alts)) == len(alts) else F)("duplicate alt text across images")
    (O if 2 <= len(imgs) <= 5 else W)("body image count %d (need 2-3, up to 5 pillar)" % len(imgs))
else:
    W("no <img> in draft (publisher inserts)")

# ---------- 6 links ----------
allhref = re.findall(r'<a\s[^>]*href=["\']([^"\']*)["\']', body, re.I)
internal = [u for u in allhref if 'virtina.com' in u]
external = [u for u in allhref if u.startswith('http') and 'virtina.com' not in u]
(O if 5 <= len(internal) <= 10 else F)("internal links = %d (need 5-10)" % len(internal))
(O if len(external) <= 2 else F)("external links = %d (max 2)" % len(external))

DEAD = ['/ecommerce-migration-services/', '/ecommerce-development-services/',
        '/ecommerce-seo-services/', '/contact/']
dh = [u for u in internal if any(x in u for x in DEAD)]
(O if not dh else F)("verified-dead paths linked: %s" % dh)

wcdev = [u for u in internal if '/woocommerce-development-services/' in u and '/platforms/' not in u]
(O if not wcdev else F)("non-/platforms/ woocommerce-development-services (301): %s" % wcdev)

COMP = ['shopify.com', 'bigcommerce.com', 'magento.com', 'adobe.com',
        'wix.com', 'squarespace.com', 'volusion.com']
ch = [u for u in allhref if any(c in u.lower() for c in COMP)]
(O if not ch else F)("competitor domains linked: %s" % ch)

placeholder = [u for u in allhref if u and not u.startswith('https://') and not u.startswith('#')]
(O if not placeholder else F)("placeholder/relative hrefs: %s" % placeholder)

pairs = re.findall(r'<a\s[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', body, re.S | re.I)
anch = [(u, html.unescape(re.sub('<[^>]+>', '', a)).strip()) for u, a in pairs if u.startswith('http')]
alist = [a for _, a in anch]
dupes = sorted({a for a in alist if alist.count(a) > 1})
(O if not dupes else F)("repeated anchor text: %s" % dupes)

lead = [a for a in alist if re.match(r'^(a|an|the)\s', a, re.I) or re.match(r'^\w+ing\s', a)]
(O if not lead else F)("anchors with leading article/gerund: %s" % lead)
(O if not [a for a in alist if a.lower() in ('click here', 'here', 'read more')] else F)("generic anchor text")

for u in external:
    tag = [t for t in re.findall(r'<a\s[^>]*>', body, re.I) if u in t]
    ok = all('target="_blank"' in t and 'noopener' in t and 'noreferrer' in t for t in tag) if tag else False
    (O if ok else F)("external target/rel on %s" % u[:46])

SERVICE = ['/platforms/', '-services/', '/get-in-touch/', '/ecommerce-cart-migration/', '/solutions/']
blogct = sum(1 for u in internal if not any(s in u for s in SERVICE))
(O if blogct >= 2 else F)("earlier-blog-post links = %d (need >=2)" % blogct)

# ---------- 4 TOC ----------
if 'href="#' in body:
    toc = re.search(r'<h3[^>]*>\s*Table of Contents\s*</h3>', body, re.I)
    (O if toc else W)("TOC heading is H3 'Table of Contents'")
    (O if '#00a0e2' in h else F)("TOC link color #00a0e2 present")
    (O if '<svg' in body.lower() else F)("TOC arrow is inline SVG")
    (O if u'→' not in txt else F)("Unicode arrow used instead of SVG")
    (O if 'thrv-styled_list' not in h else F)("Thrive thrv-styled_list markup (banned)")
    (O if ' !important' not in h else F)("space before !important (must be none)")

# ---------- 5 bullets ----------
if '<li' in body.lower():
    (O if '#43627f' in h else F)("bullet circle color #43627f present")
    (O if 'font-size:16px' in h.replace(' ', '') else F)("li font-size 16px present")

# ---------- Thrive serializer corruption ----------
(O if not re.search(r'(^|>)\s*(<<|>>)\s*(<|$)', body) else F)("orphan << or >> fragments")

bar = '=' * 66
print("\n%s\nVIRTINA QA  %s\n%s" % (bar, os.path.basename(p), bar))
for m in oks: print("  PASS  " + m)
for m in warns: print("  WARN  " + m)
for m in fails: print("  FAIL  " + m)
print("\nH2s (%d): %s" % (len(h2), " | ".join(h2[:14])))
print("H3s (%d)" % len(h3))
print("\nInternal links:")
for u, a in anch:
    if 'virtina.com' in u: print("   %-36r -> %s" % (a, u))
print("External links:")
for u, a in anch:
    if 'virtina.com' not in u: print("   %-36r -> %s" % (a, u))
print("\n%s\n%d FAIL, %d WARN, %d PASS\n%s" % (bar, len(fails), len(warns), len(oks), bar))
sys.exit(1 if fails else 0)
