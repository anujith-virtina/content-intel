# -*- coding: utf-8 -*-
"""8-gram verbatim-overlap audit for the B2B shipping-costs draft against every ChatSKU post.

MUST-FOLLOW-RULES section 1D: "no 8-word sequence may appear verbatim in any
existing ChatSKU post." Publisher checks this before any PUT call.

Corpus = all live + draft posts pulled from the WP REST API (34 published + 2
drafts as of 2026-09-15), cached to JSON so repeat runs do not re-hit the site.
Also checks the adjacent problem pages this post must not re-type
(/passive-catalog/, /response-gap/), since the brief fences the freight angle
away from their framing.

Run:  python dedup_shipping.py
"""
import os, re, json, html, base64, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
try:
    import requests
except ImportError:
    print("BLOCKING: pip install requests"); raise SystemExit(1)

ENV_PATH = r"C:\content-intel\.env"
if os.path.exists(ENV_PATH):
    for ln in open(ENV_PATH, encoding="utf-8"):
        ln = ln.strip()
        if ln and not ln.startswith("#") and "=" in ln:
            k, v = ln.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
WP = "https://chatsku.com/wp-json/wp/v2"
AUTH = base64.b64encode(
    f"{os.environ['CHATSKU_WP_USERNAME']}:{os.environ['CHATSKU_WP_APP_PASSWORD']}".encode()).decode()
H = {"Authorization": f"Basic {AUTH}", "User-Agent": UA}
HG = {"User-Agent": UA}

BASE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(BASE, "shipping_dedup_corpus.json")
DRAFT = r"C:\content-intel\clients\chatsku\output\drafts\b2b-shipping-costs-2026-09-22.md"
N = 8


def norm(t):
    """HTML -> comparable word list. Strips tags/entities, lowercases, drops
    punctuation so paraphrase-by-punctuation does not hide a real collision."""
    t = re.sub(r"<script.*?</script>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    t = t.replace("\u2019", "'").replace("\u2014", " ").replace("\u2013", " ")
    t = re.sub(r"[^a-z0-9' ]+", " ", t.lower())
    return t.split()


def grams(words, n=N):
    return {" ".join(words[i:i + n]) for i in range(len(words) - n + 1)}


def build_corpus():
    if os.path.exists(CACHE):
        c = json.load(open(CACHE, encoding="utf-8"))
        print(f"corpus loaded from cache: {len(c)} documents")
        return c
    c = {}
    for page in range(1, 4):
        r = requests.get(f"{WP}/posts", headers=H, timeout=90, params={
            "per_page": 100, "page": page, "status": "any", "context": "edit",
            "_fields": "id,slug,status,content"})
        if r.status_code != 200:
            break
        d = r.json()
        if not d:
            break
        for x in d:
            c[f"post-{x['id']}"] = {
                "slug": x["slug"], "status": x["status"],
                "html": (x["content"].get("raw") or x["content"].get("rendered", ""))}
    # adjacent problem pages whose framing this post must not re-type
    for _slug in ("passive-catalog", "response-gap"):
        pr = requests.get(f"https://chatsku.com/{_slug}/", headers=HG, timeout=90)
        if pr.status_code == 200:
            m = re.search(r"<main.*?</main>", pr.text, flags=re.S)
            c[f"page-{_slug}"] = {"slug": _slug, "status": "publish",
                                  "html": m.group(0) if m else pr.text}
    json.dump(c, open(CACHE, "w", encoding="utf-8"))
    print(f"corpus fetched: {len(c)} documents -> {CACHE}")
    return c


def main():
    raw = open(DRAFT, encoding="utf-8").read()
    raw = re.sub(r"^---.*?---\s*", "", raw, count=1, flags=re.S)
    raw = re.split(r"\n##\s*Publishing metadata", raw)[0]
    raw = re.sub(r"^\[[A-Z][^\]]*\]\s*$", "", raw, flags=re.M)
    dw = norm(raw)
    dg = grams(dw)
    print(f"draft: {len(dw)} normalised words, {len(dg)} unique {N}-grams\n")

    corpus = build_corpus()
    total_hits, worst = 0, []
    for key, v in corpus.items():
        cg = grams(norm(v["html"]))
        both = dg & cg
        if both:
            total_hits += len(both)
            worst.append((len(both), key, v["slug"], sorted(both)[:12]))
    worst.sort(reverse=True)

    if not worst:
        print(f"PASS: 0 verbatim {N}-gram overlaps across {len(corpus)} documents.")
        return 0
    print(f"FAIL: {total_hits} overlapping {N}-gram(s) across {len(worst)} document(s).\n")
    for cnt, key, slug, ex in worst:
        print(f"  {cnt:4d}  {key}  /{slug}/")
        for e in ex:
            print(f"          \"{e}\"")
    print("\nReword every sequence listed above, then re-run.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
