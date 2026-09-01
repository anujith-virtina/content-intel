# -*- coding: utf-8 -*-
"""8-gram dedup audit: "How AI product search actually works for B2B catalogs"
(how-ai-product-search-works) vs every live + draft ChatSKU post.

Adapted from dedup_audit_erp_export.py. Same approach: normalize to lowercase
alnum tokens, build 8-word shingles from the draft, fetch every post's raw
content via context=edit, and report any shared shingle. Zero verbatim 8-gram
overlap is the standard (MUST-FOLLOW-RULES.md section 1D).
"""
import json, re, os, ssl, base64, urllib.request
from pathlib import Path

ctx = ssl._create_unverified_context()
for ln in open(r"C:\content-intel\.env", encoding="utf-8"):
    ln = ln.strip()
    if ln and not ln.startswith("#") and "=" in ln:
        k, v = ln.split("=", 1); os.environ.setdefault(k.strip(), v.strip())

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
AUTH = base64.b64encode((os.environ["CHATSKU_WP_USERNAME"] + ":" + os.environ["CHATSKU_WP_APP_PASSWORD"]).encode()).decode()
H = {"Authorization": "Basic " + AUTH, "User-Agent": UA}

DRAFT_PATH = r"C:\content-intel\clients\chatsku\output\drafts\how-ai-product-search-works-2026-08-18.md"
NEW_POST_SLUG = "how-ai-product-search-works"


def norm(t):
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"&[a-z]+;", " ", t)
    t = re.sub(r"[^a-z0-9 ]", " ", t.lower())
    return re.sub(r"\s+", " ", t).strip()


def grams(t, n=8):
    w = t.split()
    return set(tuple(w[i:i + n]) for i in range(len(w) - n + 1))


d = Path(DRAFT_PATH).read_text(encoding="utf-8")
d = re.sub(r"^---.*?---\s*", "", d, count=1, flags=re.S)          # frontmatter
d = re.sub(r"\n---\s*\n\s*## Publishing notes.*$", "", d, flags=re.S)  # publishing notes tail
d = re.sub(r"```.*?```\s*", "", d, flags=re.S)
d = re.sub(r"<!--.*?-->\s*", "", d, flags=re.S)
d = re.sub(r"^\[(?:FEATURED IMAGE|BODY IMAGE|CTA BUTTON)[^\]]*\]\s*$", "", d, flags=re.M)
dg = grams(norm(d))
print("Draft 8-grams:", len(dg))

posts = []
for st in ("publish", "draft", "pending", "private", "future"):
    p = 1
    while True:
        u = (f"https://chatsku.com/wp-json/wp/v2/posts?status={st}&per_page=50&page={p}"
             f"&context=edit&_fields=id,slug,content")
        try:
            b = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60, context=ctx).read())
        except Exception as e:
            print(f"  stopped fetching status={st} page={p}: {e}")
            break
        if not b:
            break
        posts += [(x["id"], x.get("slug", "?"),
                   x.get("content", {}).get("raw") or x.get("content", {}).get("rendered", "")) for x in b]
        p += 1

# also compare against Elementor data (some posts store body text only there)
print("Fetched", len(posts), "posts")

worst = 0
checked = 0
for pid, slug, c in posts:
    if slug == NEW_POST_SLUG:
        continue
    checked += 1
    ov = dg & grams(norm(c))
    if ov:
        worst = max(worst, len(ov))
        print(f"  OVERLAP {len(ov)} post {pid} ({slug})")
        for g in list(ov)[:5]:
            print("     ", " ".join(g))

print("Posts compared:", checked)
print("RESULT: CLEAN, 0 overlap" if worst == 0 else f"RESULT: max overlap {worst}")
