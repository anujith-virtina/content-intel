# -*- coding: utf-8 -*-
"""8-gram dedup audit: "Is your ERP export AI-agent-friendly? A 10-minute
self-check" (erp-export-ai-agent-ready) vs every live + draft ChatSKU post.

Adapted from dedup_audit_evolution.py (post 1820) / the dedup_glossary.py
pattern referenced in the published-posts-inventory for post 2129. Same
approach: normalize to lowercase alnum tokens, build 8-word shingles from
the draft, fetch every post's raw content via context=edit, and report any
shared shingle. Zero verbatim 8-gram overlap is the standard
(MUST-FOLLOW-RULES.md section 1D).

NOT RUN in this session -- no code-execution tool available. Run in a
Python environment with `requests` and CHATSKU_WP_USERNAME /
CHATSKU_WP_APP_PASSWORD set (present in project .env as of 2026-08-17)
before treating this post's dedup check as complete.
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

DRAFT_PATH = r"C:\content-intel\clients\chatsku\output\drafts\erp-export-ai-agent-ready-2026-08-17.md"
NEW_POST_SLUG = "erp-export-ai-agent-ready"  # excluded from comparison once it exists live

def norm(t):
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"&[a-z]+;", " ", t)
    t = re.sub(r"[^a-z0-9 ]", " ", t.lower())
    return re.sub(r"\s+", " ", t).strip()

def grams(t, n=8):
    w = t.split()
    return set(tuple(w[i:i + n]) for i in range(len(w) - n + 1))

d = Path(DRAFT_PATH).read_text(encoding="utf-8")
d = re.sub(r"^---.*?---\s*", "", d, count=1, flags=re.S)   # strip frontmatter
d = re.sub(r"```.*?```\s*", "", d, flags=re.S)               # strip SEO meta fence
d = re.sub(r"<!--.*?-->\s*", "", d, flags=re.S)              # strip self-check comment
d = re.sub(r"^\[(?:FEATURED IMAGE|BODY IMAGE \d+)[^\n]*\]\s*$", "", d, flags=re.M)  # strip image notes
dg = grams(norm(d))
print("Draft 8-grams:", len(dg))

posts = []
for st in ("publish", "draft"):
    p = 1
    while True:
        u = f"https://chatsku.com/wp-json/wp/v2/posts?status={st}&per_page=50&page={p}&context=edit&_fields=id,slug,content"
        try:
            b = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=40, context=ctx).read())
        except Exception as e:
            print(f"  stopped fetching status={st} page={p}: {e}")
            break
        if not b:
            break
        posts += [(x["id"], x.get("slug", "?"), x.get("content", {}).get("raw") or x.get("content", {}).get("rendered", "")) for x in b]
        p += 1
print("Fetched", len(posts), "posts")

worst = 0
for pid, slug, c in posts:
    if slug == NEW_POST_SLUG:
        continue
    ov = dg & grams(norm(c))
    if ov:
        worst = max(worst, len(ov))
        print(f"  OVERLAP {len(ov)} post {pid} ({slug})")
        for g in list(ov)[:5]:
            print("     ", " ".join(g))

print("RESULT: CLEAN, 0 overlap" if worst == 0 else f"RESULT: max overlap {worst}")
