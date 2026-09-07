# -*- coding: utf-8 -*-
"""Apply the 2026-09-07 refresh to live post 37791 (virtina.com).

DRY RUN by default. Pass 'publish' to write.

What it does, in order:
  1. strip the 15 injected vendor links (empty anchors deleted, text anchors unwrapped)
  2. lift all 20 entry blocks out of the page, keyed by name
  3. drop the 4 retired entries
  4. rebuild the page: head matter -> methodology -> ranked table -> the ten
     ranked profiles in rank order -> differentiator -> financials -> regional
     H2 -> the 9 demoted entries as H3s -> what-it-means -> PAA -> conclusion -> FAQ
  5. renumber the ten H2s, demote the nine to H3 and strip their stale numbers,
     preserving every element id so in-page anchors keep working
  6. verify, then push

Safety, because this page is LIVE and ranking:
  * source of truth is the on-disk backup, never a re-read of a half-edited page
  * status / categories / featured_media are never sent, so they cannot be clobbered
  * writes tve_updated_post (what Thrive renders) and post_content (kept in sync)
  * read-back compares sha256 of what we sent against what stuck
"""
import os, sys, re, io, json, base64, hashlib, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from strip_vendor_links import strip as strip_vendor, verify as verify_strip
from thrive_edit_lib import entry_spans, integrity

ROOT = r"C:\content-intel"
BK = os.path.join(ROOT, r"clients\virtina\output\backups\post-37791-tve_updated_post-2026-09-07.html")
BLOCKS = os.path.join(ROOT, r"clients\virtina\output\drafts\best-ecommerce-websites-blocks-2026-09-07.html")
PREVIEW = os.path.join(ROOT, r"clients\virtina\output\research\_37791_final_preview.html")
POST_ID = 37791
DRY = "publish" not in sys.argv

NEW_TITLE = "Top 10 online shopping sites in the world, plus 11 eCommerce websites worth knowing"
YOAST_TITLE = "Top 10 Online Shopping Sites in the World (2026) | Virtina"
YOAST_DESC = ("See the top 10 online shopping sites in the world, ranked by monthly visits "
              "(Semrush, July 2026), plus why Taobao and JD.com never appear in traffic lists.")
YOAST_FOCUS = "top 10 online shopping sites in world"

CUT = ["4. Apple", "10. Shopify", "13. DoorDash", "18. Overstock"]

# rank -> which existing entry (by keyword in its heading) or which new block
RANKED = [
    (1,  "existing", "Amazon"),
    (2,  "block",    "entry-temu"),
    (3,  "existing", "AliExpress"),
    (4,  "existing", "Walmart"),
    (5,  "existing", "eBay"),
    (6,  "existing", "Etsy"),
    (7,  "existing", "Rakuten"),
    (8,  "existing", "Shein"),
    (9,  "block",    "entry-coupang"),
    (10, "block",    "entry-ozon"),
]
# demoted, in the order they should appear under "Regional and category leaders"
DEMOTED = ["Target", "Wayfair", "Chewy", "Sephora", "StockX", "ThredUp",
           "Zappos", "Newegg", "Best Buy"]

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")


def env():
    e = {}
    for ln in io.open(os.path.join(ROOT, ".env"), encoding="utf-8"):
        ln = ln.strip()
        if ln and "=" in ln and not ln.startswith("#"):
            k, v = ln.split("=", 1)
            e[k.strip()] = v.strip()
    return e


def headers():
    e = env()
    tok = base64.b64encode(f"{e['WP_USERNAME']}:{e['WP_APP_PASSWORD']}".encode()).decode()
    return {"User-Agent": UA, "Content-Type": "application/json",
            "Authorization": "Basic " + tok}


def load_blocks():
    raw = io.open(BLOCKS, encoding="utf-8").read()
    out = {}
    for m in re.finditer(r'<!--\s*BLOCK id=([a-z0-9-]+)\s*-->(.*?)<!--\s*/BLOCK\s*-->',
                         raw, re.S | re.I):
        out[m.group(1).strip()] = m.group(2).strip()
    if not out:
        raise SystemExit("BLOCKING: no BLOCK markers parsed")
    return out


# Some H2s wrap their text in a nested <a> or <span> (and one carries an empty
# href). Replacing only the first >...< left the original text inside the nested
# element and produced "Wayfair7. Wayfair". Replace the WHOLE inner content.
_H2 = re.compile('(<h2[^>]*>)(.*?)(</h2>)', re.S | re.I)


def set_h2_number(block, n, name):
    """Rewrite the entry's H2 to '<n>. <name>', keeping the opening tag as-is."""
    return _H2.sub(lambda m: f'{m.group(1)}{n}. {name}{m.group(3)}', block, count=1)


def demote_to_h3(block, name):
    """H2 -> H3 with the stale number dropped. Wrapper id and tokens untouched."""
    def repl(m):
        open_tag = m.group(1)
        open_tag = re.sub(r'^<h2', '<h3', open_tag)
        if 'style=' in open_tag:
            open_tag = re.sub(r'style="([^"]*)"',
                              lambda s: f'style="{s.group(1).rstrip("; ")};font-size:22px !important;"',
                              open_tag, count=1)
        else:
            open_tag = open_tag.replace('<h3', '<h3 style="font-size:22px !important;"', 1)
        return f'{open_tag}{name}</h3>'
    return _H2.sub(repl, block, count=1)


def main():
    src = io.open(BK, encoding="utf-8").read()
    print(f"source (backup): {len(src)} chars")

    # 1. strip injected vendor links
    work, rep = strip_vendor(src)
    probs = verify_strip(src, work, rep)
    if probs:
        raise SystemExit(f"BLOCKING: link strip failed: {probs}")
    print(f"  vendor links: {rep['deleted']} deleted, {len(rep['unwrapped'])} unwrapped "
          f"{rep['unwrapped']}")

    # 2. lift every entry out
    spans = entry_spans(work)
    if len(spans) != 20:
        raise SystemExit(f"BLOCKING: expected 20 entries, found {len(spans)}")
    head = work[:spans[0][1]]          # summary + intro + TOC
    tail = work[spans[-1][2]:]         # parent closing divs
    entries = {h: work[a:b] for h, a, b in spans}
    print(f"  lifted {len(entries)} entries | head {len(head)} chars | tail {len(tail)} chars")

    for c in CUT:
        if c not in entries:
            raise SystemExit(f"BLOCKING: cannot find entry to cut: {c}")
        del entries[c]
    print(f"  cut {len(CUT)}: {CUT} -> {len(entries)} remain")

    blocks = load_blocks()
    print(f"  blocks parsed: {len(blocks)}")

    def find_entry(keyword):
        for h in entries:
            if keyword.lower() in h.lower():
                return h
        return None

    # 3. head matter replacements
    for bid, needle in (("summary-fix", None), ("intro-fix", None)):
        pass  # handled below explicitly

    # 4. build the ranked run
    used = set()
    ranked_html = []
    for n, kind, ref in RANKED:
        if kind == "block":
            if ref not in blocks:
                raise SystemExit(f"BLOCKING: missing block {ref}")
            ranked_html.append(set_h2_number(blocks[ref], n, {
                "entry-temu": "Temu", "entry-coupang": "Coupang", "entry-ozon": "Ozon"}[ref]))
        else:
            h = find_entry(ref)
            if not h:
                raise SystemExit(f"BLOCKING: cannot find existing entry {ref}")
            used.add(h)
            blk = entries[h]
            if ref == "Rakuten" and "rewrite-rakuten" in blocks:
                # swap the body copy, keep wrapper/id/image
                blk = re.sub(r'(<div class="thrv_wrapper thrv_text_element">\s*<p dir="ltr".*?</div>)',
                             blocks["rewrite-rakuten"], blk, count=1, flags=re.S)
            ranked_html.append(set_h2_number(blk, n, ref))
    print(f"  ranked run assembled: {len(ranked_html)} entries")

    # 5. demoted run
    demoted_html = []
    for name in DEMOTED:
        h = find_entry(name)
        if not h:
            raise SystemExit(f"BLOCKING: cannot find entry to demote: {name}")
        used.add(h)
        demoted_html.append(demote_to_h3(entries[h], name))
    print(f"  demoted run assembled: {len(demoted_html)} entries")

    leftover = [h for h in entries if h not in used]
    if leftover:
        raise SystemExit(f"BLOCKING: entries neither ranked nor demoted: {leftover}")

    # 6. head matter: apply summary + intro replacements
    if "summary-fix" in blocks:
        head = re.sub(r'(<h2[^>]*>\s*Summary\s*</h2>\s*</div>)(.*?)(?=<div class="thrv_wrapper thrv_contentbox)',
                      lambda m: m.group(1) + blocks["summary-fix"], head, count=1, flags=re.S | re.I)
    if "intro-fix" in blocks:
        head = head + blocks["intro-fix"]
    print("  head matter updated (summary + intro)")

    out = (head
           + blocks.get("methodology", "")
           + blocks.get("top10", "")
           + "".join(ranked_html)
           + blocks.get("differentiator", "")
           + blocks.get("financials", "")
           + blocks.get("regional", "")
           + "".join(demoted_html)
           + blocks.get("what-it-means", "")
           + blocks.get("paa", "")
           + blocks.get("conclusion", "")
           + blocks.get("faq", "")
           + tail)

    # 7. verify
    probs = integrity(src, out)
    if probs:
        raise SystemExit(f"BLOCKING: integrity failed: {probs}")
    for d in ("virtocommerce", "sharetribe", "webkul", "cedcommerce", "yo-kart",
              "bigcommerce", "ecommerce-migration-services"):
        if d in out.lower():
            raise SystemExit(f"BLOCKING: '{d}' survived into final markup")
    if out.count("\u2014") or "&mdash;" in out:
        raise SystemExit("BLOCKING: em dash present")
    ids = re.findall(r'id="([^"]+)"', out)
    for need in ("amazon", "walmart", "ebay", "etsy", "rakuten", "shein", "target",
                 "wayfair", "chewy", "sephora", "stockx", "thredup", "zappos",
                 "newegg", "best-buy"):
        if need not in ids:
            raise SystemExit(f"BLOCKING: anchor id lost: {need}")
    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', out, re.S)
    print(f"  integrity CLEAN | divs balanced | ids preserved | H2 count {len(h2s)}")
    print(f"  {len(src)} -> {len(out)} chars")
    io.open(PREVIEW, "w", encoding="utf-8").write(out)

    if DRY:
        print("\nDRY RUN. Nothing pushed. Preview:", PREVIEW)
        return

    H = headers()
    payload = json.dumps({
        "title": NEW_TITLE,
        "content": out,
        "meta": {
            "tve_updated_post": out,
            "_yoast_wpseo_title": YOAST_TITLE,
            "_yoast_wpseo_metadesc": YOAST_DESC,
            "_yoast_wpseo_focuskw": YOAST_FOCUS,
        },
    }).encode("utf-8")
    r = urllib.request.urlopen(urllib.request.Request(
        f"https://virtina.com/wp-json/wp/v2/posts/{POST_ID}",
        data=payload, headers=H, method="POST"), timeout=300)
    print("\nPUSH status:", r.status)

    back = json.load(urllib.request.urlopen(urllib.request.Request(
        f"https://virtina.com/wp-json/wp/v2/posts/{POST_ID}?context=edit",
        headers=H), timeout=300))
    live = back["meta"]["tve_updated_post"]
    print("  tve sha match:",
          hashlib.sha256(live.encode()).hexdigest() == hashlib.sha256(out.encode()).hexdigest())
    print("  status  :", back["status"], "(must be publish)")
    print("  title   :", back["title"]["raw"][:78])
    print("  yoast   :", back["meta"].get("_yoast_wpseo_title"))
    print("  focus kw:", back["meta"].get("_yoast_wpseo_focuskw"))
    print("  cats    :", back.get("categories"), "| featured:", back.get("featured_media"))


if __name__ == "__main__":
    main()
