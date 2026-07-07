"""
Duplicate-content audit for ChatSKU.
Pulls every post (publish + draft) from the WP REST API, extracts plaintext,
and runs an 8-word verbatim shingle overlap of the two new posts
(Magento 1056, WooCommerce 685) against every OTHER post. Enforces
MUST-FOLLOW-RULES section 1D. Also fetches the Magento + WooCommerce Solutions
pages to check blog-vs-page cannibalization.
Read-only. No writes to WordPress.
"""
import json, re, os, ssl, base64, urllib.request, urllib.parse
from collections import defaultdict

_ssl = ssl._create_unverified_context()
_env = r"C:\content-intel\.env"
if os.path.exists(_env):
    for ln in open(_env):
        ln = ln.strip()
        if ln and not ln.startswith("#") and "=" in ln:
            k, v = ln.split("=", 1); os.environ.setdefault(k.strip(), v.strip())
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
AUTH = base64.b64encode(f"{os.environ['CHATSKU_WP_USERNAME']}:{os.environ['CHATSKU_WP_APP_PASSWORD']}".encode()).decode()
H = {"Authorization": f"Basic {AUTH}", "User-Agent": UA}
BASE = "https://chatsku.com/wp-json/wp/v2"

STOP_HTML = re.compile(r"<[^>]+>")
def plain(html):
    html = re.sub(r"<script.*?</script>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<style.*?</style>", " ", html, flags=re.S | re.I)
    txt = STOP_HTML.sub(" ", html)
    txt = (txt.replace("&amp;", "&").replace("&#8217;", "'").replace("&#8220;", '"')
              .replace("&#8221;", '"').replace("&nbsp;", " ").replace("&#8211;", "-"))
    return txt

WORD = re.compile(r"[a-z0-9']+")
def toks(txt):
    return WORD.findall(txt.lower())

def shingles(tokens, n=8):
    return {" ".join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)}

def get_all_posts():
    out = {}
    for status in ("publish", "draft", "pending", "future", "private"):
        page = 1
        while True:
            url = f"{BASE}/posts?" + urllib.parse.urlencode(
                {"status": status, "per_page": 100, "page": page, "context": "edit", "_fields": "id,slug,title,content"})
            try:
                req = urllib.request.Request(url, headers=H)
                with urllib.request.urlopen(req, timeout=40, context=_ssl) as r:
                    data = json.loads(r.read())
            except Exception as e:
                break
            if not data:
                break
            for p in data:
                out[p["id"]] = {"slug": p.get("slug", ""),
                                "title": plain(p.get("title", {}).get("rendered", "")).strip(),
                                "text": plain(p.get("content", {}).get("rendered", ""))}
            if len(data) < 100:
                break
            page += 1
    return out

print("Fetching all posts via REST (publish + draft + others)...")
posts = get_all_posts()
print(f"Fetched {len(posts)} posts total.")

# Optional: override a post's text with a LOCAL draft (verify a rewrite pre-push)
LOCAL_OVERRIDE = {
    1056: r"C:\content-intel\clients\chatsku\output\drafts\magento-b2b-chatbot-integration-2026-07-06.md",
}
for pid, path in LOCAL_OVERRIDE.items():
    if os.environ.get("USE_LOCAL") and os.path.exists(path):
        raw = open(path, encoding="utf-8").read()
        raw = re.sub(r'^---\n.*?\n---\n', '', raw, count=1, flags=re.S)
        raw = re.sub(r'^### SECTION: .*$', ' ', raw, flags=re.M)
        if pid in posts:
            posts[pid]["text"] = plain(raw)
            print(f"  [override] post {pid} text loaded from local draft ({len(toks(posts[pid]['text']))}w)")
for pid, p in sorted(posts.items()):
    tk = toks(p["text"])
    print(f"  {pid:>5}  {len(tk):>5}w  {p['slug'][:52]}")

# precompute shingles
sh = {pid: shingles(toks(p["text"])) for pid, p in posts.items()}

TARGETS = {1056: "Magento integration (NEW)", 685: "WooCommerce (NEW)"}
GENERIC_OK = 0  # report everything, judge manually

for tid, label in TARGETS.items():
    if tid not in posts:
        print(f"\n!! target {tid} not found"); continue
    print("\n" + "=" * 72)
    print(f"TARGET {tid}: {label}  ({len(toks(posts[tid]['text']))} words, {len(sh[tid])} 8-grams)")
    print("=" * 72)
    any_overlap = False
    for pid, p in sorted(posts.items()):
        if pid == tid:
            continue
        common = sh[tid] & sh[pid]
        if common:
            any_overlap = True
            print(f"\n  vs {pid} ({p['slug'][:50]}): {len(common)} shared 8-word sequence(s)")
            for c in sorted(common):
                print(f"      >> \"{c}\"")
    if not any_overlap:
        print("\n  No 8-word verbatim overlap with ANY other post. CLEAN.")

# ---- Solutions-page cannibalization (blog vs product page) ----
print("\n" + "=" * 72)
print("BLOG vs SOLUTIONS PAGE overlap (cannibalization check)")
print("=" * 72)
PAGES = {"magento-b2b-chatbot": 1056, "b2b-chatbot-for-woocommerce": None}
def fetch_page_text(slug):
    for kind in ("pages", "posts"):
        url = f"{BASE}/{kind}?" + urllib.parse.urlencode({"slug": slug, "_fields": "id,slug,content"})
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=40, context=_ssl) as r:
                d = json.loads(r.read())
            if d:
                return plain(d[0].get("content", {}).get("rendered", ""))
        except Exception:
            pass
    return ""
for slug, tid in PAGES.items():
    if tid is None:
        continue
    ptxt = fetch_page_text(slug)
    if not ptxt:
        print(f"  [{slug}] page text not retrievable via REST (skip)"); continue
    psh = shingles(toks(ptxt))
    common = sh[tid] & psh
    print(f"  blog {tid} vs /{slug}/ page ({len(toks(ptxt))} words): {len(common)} shared 8-grams")
    for c in sorted(common):
        print(f"      >> \"{c}\"")
print("\nDONE.")
