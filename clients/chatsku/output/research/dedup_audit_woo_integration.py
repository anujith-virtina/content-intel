"""
Dedup audit for the NEW post: woocommerce-b2b-chatbot-integration (2026-07-14).
Pulls every ChatSKU post via REST (publish + draft + others), extracts plaintext,
parses the NEW local draft (plain <h2> HTML format), and runs 8-word verbatim
shingle overlap of the NEW draft against every live post. Enforces MUST-FOLLOW §1D.
Read-only. No writes to WordPress.
"""
import json, re, os, ssl, base64, urllib.request, urllib.parse
from pathlib import Path

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
def toks(txt): return WORD.findall(txt.lower())
def shingles(tokens, n=8): return {" ".join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)}

def get_all_posts():
    out = {}
    for status in ("publish", "draft", "pending", "future", "private"):
        page = 1
        while True:
            url = f"{BASE}/posts?" + urllib.parse.urlencode(
                {"status": status, "per_page": 100, "page": page, "context": "edit",
                 "_fields": "id,slug,title,content"})
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=40, context=_ssl) as r:
                    data = json.loads(r.read())
            except Exception:
                break
            if not data: break
            for p in data:
                out[p["id"]] = {"slug": p.get("slug", ""),
                                "text": plain(p.get("content", {}).get("rendered", ""))}
            if len(data) < 100: break
            page += 1
    return out

# ---- new draft (plain <h2> HTML) ----
DRAFT = r"C:\content-intel\clients\chatsku\output\drafts\woocommerce-b2b-integration-guide-2026-07-14.md"
raw = Path(DRAFT).read_text(encoding="utf-8")
raw = re.sub(r'^---\n.*?\n---\n', '', raw, count=1, flags=re.S)   # strip frontmatter
raw = re.sub(r'<!--.*?-->', ' ', raw, flags=re.S)                  # strip image-placement comments
new_text = plain(raw)
new_sh = shingles(toks(new_text))
print(f"NEW draft: {len(toks(new_text))} words, {len(new_sh)} 8-grams")

print("Fetching all posts via REST...")
posts = get_all_posts()
print(f"Fetched {len(posts)} posts.\n")

any_overlap = False
for pid, p in sorted(posts.items()):
    common = new_sh & shingles(toks(p["text"]))
    if common:
        any_overlap = True
        print(f"vs {pid} ({p['slug'][:50]}): {len(common)} shared 8-gram(s)")
        for c in sorted(common):
            print(f"    >> \"{c}\"")
if not any_overlap:
    print("RESULT: 0 verbatim 8-word overlap with ANY live/draft ChatSKU post. CLEAN.")
else:
    print("\nRESULT: OVERLAP FOUND — reword before publishing.")
