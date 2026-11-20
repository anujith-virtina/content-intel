"""Add visible byline + published/updated dates (AEO/GEO gate item 9) to ChatSKU 4427
and ECM 284726; add Article + BreadcrumbList JSON-LD to ECM (Yoast outputs none there).
Usage: python add_byline_dates_2026_11_20.py fetch|build|push
"""
import sys, json, base64, subprocess, re, os, datetime, uuid
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "clients", "_fix-2026-11-20-byline")
os.makedirs(OUT, exist_ok=True)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"

def env():
    e = {}
    for l in open(os.path.join(ROOT, ".env"), encoding="utf-8"):
        l = l.strip()
        if l and not l.startswith("#") and "=" in l:
            k, v = l.split("=", 1); e[k.strip()] = v.strip().strip('"').strip("'")
    return e
E = env()
SITES = {
 "chatsku": ("https://chatsku.com", 4427, E["CHATSKU_WP_USERNAME"], E["CHATSKU_WP_APP_PASSWORD"]),
 "ecm": ("https://eldercarematters.com", 284726, E["ECM_WP_USERNAME"], E["ECM_WP_APP_PASSWORD"]),
}
def curl(site, path, method="GET", body_file=None):
    base, pid, u, p = SITES[site]
    auth = base64.b64encode(f"{u}:{p}".encode()).decode()
    cfg = os.path.join(OUT, f"_hdr_{site}.txt")
    open(cfg, "w").write(f'header = "Authorization: Basic {auth}"\n')
    cmd = ["curl", "-s", "-X", method, "-A", UA, "-K", cfg, "-H", "Content-Type: application/json", base + path]
    if body_file: cmd[1:1] = ["--data-binary", "@" + body_file]
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=180)
    finally:
        os.remove(cfg)
    return r.stdout.decode("utf-8", "ignore")

def nice(d):  # 2026-11-20T12:00:00 -> November 20, 2026
    dt = datetime.datetime.fromisoformat(d[:19]); return dt.strftime("%B ") + str(dt.day) + dt.strftime(", %Y")

def byline(name, pub, mod, color="#555"):
    upd = f' &middot; Updated <time datetime="{mod[:10]}">{nice(mod)}</time>'
    return (f'<p class="post-byline" style="font-size:14px;color:{color};margin:0 0 18px;">'
            f'By {name} &middot; Published <time datetime="{pub[:10]}">{nice(pub)}</time>{upd}</p>')

mode = sys.argv[1]
if mode == "fetch":
    for s, (base, pid, _, _) in SITES.items():
        raw = curl(s, f"/wp-json/wp/v2/posts/{pid}?context=edit")
        open(os.path.join(OUT, f"{s}-live.json"), "w", encoding="utf-8").write(raw)
        d = json.loads(raw)
        print(s, d["status"], d["date"], d["modified"], d["link"], "cats", d.get("categories"),
              "content", len(d["content"]["raw"]), "eldata", len((d.get("meta") or {}).get("_elementor_data") or ""))
elif mode == "build":
    # ChatSKU: html widget at the top of the first container/column
    d = json.load(open(os.path.join(OUT, "chatsku-live.json"), encoding="utf-8"))
    el = json.loads(d["meta"]["_elementor_data"])
    assert "post-byline" not in d["meta"]["_elementor_data"], "already has byline"
    w = {"id": uuid.uuid4().hex[:7], "elType": "widget", "widgetType": "html", "elements": [],
         "settings": {"html": byline("ChatSKU Team", d["date"], d["modified"])}}
    node = el[0]
    while node["elements"] and node["elements"][0].get("elType") in ("section", "column", "container"):
        node = node["elements"][0]
    first = node["elements"][0] if node["elements"] else {}
    print("chatsku inserting before:", first.get("widgetType"), str(first.get("settings", {}).get("title", ""))[:60])
    node["elements"].insert(0, w)
    json.dump({"meta": {"_elementor_data": json.dumps(el, ensure_ascii=False)}},
              open(os.path.join(OUT, "chatsku-payload.json"), "w", encoding="utf-8"), ensure_ascii=False)
    # ECM: byline at top of content + Article/Breadcrumb JSON-LD at end
    d = json.load(open(os.path.join(OUT, "ecm-live.json"), encoding="utf-8"))
    c = d["content"]["raw"]
    assert "post-byline" not in c, "already has byline"
    c = re.sub(r"<!--(?!\s*/?wp:).*?-->", "", c, flags=re.S)  # Wordfence: strip non-block comments
    title = re.sub(r"<[^>]+>", "", d["title"]["raw"])
    org = {"@type": "Organization", "name": "ElderCareMatters.com", "url": "https://eldercarematters.com/"}
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": title, "datePublished": d["date_gmt"] + "Z", "dateModified": d["modified_gmt"] + "Z",
         "author": {"@type": "Organization", "name": "ElderCareMatters Editorial Team", "url": "https://eldercarematters.com/"},
         "publisher": org, "mainEntityOfPage": d["link"], "url": d["link"]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://eldercarematters.com/"},
            {"@type": "ListItem", "position": 2, "name": "Family Caregiving", "item": "https://eldercarematters.com/category/family-caregiving/"},
            {"@type": "ListItem", "position": 3, "name": title, "item": d["link"]}]}]}
    c = byline("ElderCareMatters Editorial Team", d["date"], d["modified"]) + "\n" + c + \
        '\n<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>\n"
    json.dump({"content": c}, open(os.path.join(OUT, "ecm-payload.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print("ecm content", len(d["content"]["raw"]), "->", len(c), "| title:", title)
elif mode == "push":
    for s, (base, pid, _, _) in SITES.items():
        r = curl(s, f"/wp-json/wp/v2/posts/{pid}", "POST", os.path.join(OUT, f"{s}-payload.json"))
        try: j = json.loads(r); print(s, "ok", j.get("id"), j.get("status"), j.get("modified"))
        except Exception: print(s, "ERR", r[:300])
    print(curl("chatsku", "/wp-json/elementor/v1/cache", "DELETE")[:100])
