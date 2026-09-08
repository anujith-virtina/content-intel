# -*- coding: utf-8 -*-
"""Second pass on live post 38972: add 5 verified plugins and a dated price table.

Runs on the CURRENT LIVE content, not the morning backup, because the first pass
(cut 8 dead plugins, removed the unsourced market block, fixed the TOC) is
already published. Re-basing on the old backup would silently revert it.

DRY RUN by default. Pass 'publish' to write.
"""
import os, sys, re, io, json, base64, hashlib, urllib.request, html as _html

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from thrive_edit_lib import block_bounds, DIV_OPEN, DIV_CLOSE
from build_entry_markup import (build_entry, build_pricing_section,
                                parse_entries, parse_pricing_intro)

ROOT = r"C:\content-intel"
SRC_TXT = os.path.join(ROOT, r"clients\virtina\output\drafts\dropship-new-entries-2026-09-08.txt")
PREVIEW = os.path.join(ROOT, r"clients\virtina\output\research\_38972_additions_preview.html")
POST_ID = 38972
DRY = "publish" not in sys.argv

# Verified on the vendors' own pricing pages, 2026-09-08. Anything that could not
# be verified is named in the intro copy instead of being estimated here.
PRICES = [
    ("AliDropship Woo", "$89 one-time"),
    ("Dropified", "$50 a month, or $500 a year"),
    ("Spocket", "Starter $39.99, Professional $59.99, Empire $99.99, Unicorn $299.99 a month"),
    ("Syncee", "Free, Basic $39.99, Pro $59.99, Business $99.99 a month"),
    ("Importify", "Basic $14.95, Premium $27.95, Gold $37.95 a month"),
    ("Doba", "Limited $28.66, Basic $56.99, Standard $142.66 a month, Enterprise custom"),
    ("Wholesale2b", "Basic $20, Professional $59, Premium $99 per user a month"),
    ("AppScenic", "Free, Standard $39, Pro $79, Elite $99 a month"),
    ("Printful", "Free, Growth $24.99 a month, Enterprise custom"),
    ("Printify", "Free, Premium from $39 a month, Enterprise custom"),
    ("Dropshipping for WooCommerce (OPMC)", "Shown as INR 7,575 a year on 8 September 2026, USD price unconfirmed"),
]

# link notes the creator flagged, all verified 200 with no redirect on 2026-09-08
LINKS = {
    "/woocommerce-plugin-development/": "WooCommerce plugin development",
    "/platforms/woocommerce-development-services/": "WooCommerce development services",
    "/how-to-set-up-woocommerce-for-dropshipping/": "set up WooCommerce for dropshipping",
    "/woocommerce-dropshipping-guide/": "WooCommerce dropshipping guide",
    "/woocommerce-guide/": "WooCommerce guide",
}

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")


def headers():
    e = {}
    for ln in io.open(os.path.join(ROOT, ".env"), encoding="utf-8"):
        ln = ln.strip()
        if ln and "=" in ln and not ln.startswith("#"):
            k, v = ln.split("=", 1)
            e[k.strip()] = v.strip()
    tok = base64.b64encode(f"{e['WP_USERNAME']}:{e['WP_APP_PASSWORD']}".encode()).decode()
    return {"User-Agent": UA, "Content-Type": "application/json",
            "Authorization": "Basic " + tok}


def linkify(text):
    """Turn the creator's [link: /path/] notes into Virtina's internal link markup."""
    def rep(m):
        path = m.group(1).strip()
        anchor = LINKS.get(path)
        if not anchor:
            raise SystemExit(f"BLOCKING: unverified link path in copy: {path}")
        return ""
    # the note sits at the end of a sentence; convert to a real trailing link
    out = re.sub(r'\s*\[link:\s*([^\]]+)\]', rep, text)
    return out.strip()


def trailing_link(text):
    m = re.search(r'\[link:\s*([^\]]+)\]', text)
    if not m:
        return None
    path = m.group(1).strip()
    if path not in LINKS:
        raise SystemExit(f"BLOCKING: unverified link path in copy: {path}")
    return path


def main():
    H = headers()
    live = json.load(urllib.request.urlopen(urllib.request.Request(
        f"https://virtina.com/wp-json/wp/v2/posts/{POST_ID}?context=edit",
        headers=H), timeout=300))
    src = live["meta"]["tve_updated_post"]
    print(f"live source: {len(src)} chars, divs "
          f"{len(DIV_OPEN.findall(src))}/{len(DIV_CLOSE.findall(src))}")

    existing = [re.sub(r'\s+', ' ', _html.unescape(re.sub('<[^>]+>', '', m.group(1)))).strip()
                for m in re.finditer(r'<h3[^>]*>(.*?)</h3>', src, re.S | re.I)]
    numbered = [t for t in existing if re.match(r'^\d+\.', t)]
    print(f"  existing numbered entries: {len(numbered)}")
    if len(numbered) != 17:
        raise SystemExit(f"BLOCKING: expected 17 entries from the first pass, found {len(numbered)}")

    ents = parse_entries(SRC_TXT)
    heading, paras = parse_pricing_intro(SRC_TXT)
    print(f"  new entries to add: {len(ents)} | pricing paragraphs: {len(paras)}")

    # build the new entry markup, numbered on from 17
    blocks = []
    for i, (name, qas) in enumerate(ents, start=len(numbered) + 1):
        clean = []
        for q, a in qas:
            path = trailing_link(a)
            a = linkify(a)
            if path:
                a += f'  See our {LINKS[path]}: {path}'
            clean.append((q, a))
        blocks.append(build_entry(i, name, clean))
    new_run = "".join(blocks)

    # insert after the last existing entry
    last = None
    for m in re.finditer(r'<h3[^>]*>(.*?)</h3>', src, re.S | re.I):
        t = re.sub(r'\s+', ' ', _html.unescape(re.sub('<[^>]+>', '', m.group(1)))).strip()
        if re.match(r'^\d+\.', t):
            last = m
    b = block_bounds(src, last.start())
    out = src[:b[1]] + new_run + src[b[1]:]
    print(f"  inserted {len(ents)} entries after #{len(numbered)}")

    # pricing section, straight after the plugin list
    pricing = build_pricing_section(heading, [linkify(p) for p in paras], PRICES)
    out = out[:b[1] + len(new_run)] + pricing + out[b[1] + len(new_run):]
    print(f"  inserted the dated pricing section ({len(PRICES)} verified prices)")

    n = len(numbered) + len(ents)
    out = re.sub(r'\b17 Popular\b', f'{n} Popular', out)

    # Pre-existing em dashes in the ChinaDS entry. Virtina's rules ban them, so
    # they are a standing violation that predates this pass. Repair rather than
    # loosen the guard: an em dash between clauses becomes a comma.
    if "—" in out:
        before = out.count("—")
        out = re.sub(r'\s*—\s*', ', ', out)
        out = re.sub(r',\s*,', ',', out)
        print(f"  repaired {before} pre-existing em dash(es)")

    # guards
    if len(DIV_OPEN.findall(out)) != len(DIV_CLOSE.findall(out)):
        raise SystemExit("BLOCKING: div imbalance")
    invented = set(re.findall(r'data-css="([^"]+)"', out)) - set(re.findall(r'data-css="([^"]+)"', src))
    if invented:
        raise SystemExit(f"BLOCKING: invented data-css {sorted(invented)[:4]}")
    if "\u2014" in out or "&mdash;" in out:
        raise SystemExit("BLOCKING: em dash")
    if "[link:" in out:
        raise SystemExit("BLOCKING: an unconverted [link:] note survived into the markup")
    print(f"  checks OK | {len(src)} -> {len(out)} chars | new total {n} plugins")
    io.open(PREVIEW, "w", encoding="utf-8").write(out)

    if DRY:
        print("\nDRY RUN. Nothing pushed. Preview:", PREVIEW)
        return

    tcb = urllib.request.urlopen(urllib.request.Request(
        f"https://virtina.com/wp-json/tcb/v1/posts/{POST_ID}/content",
        data=json.dumps({"tve_content": out}).encode("utf-8"),
        headers=H, method="POST"), timeout=300)
    print("THRIVE push:", tcb.status)
    urllib.request.urlopen(urllib.request.Request(
        f"https://virtina.com/wp-json/wp/v2/posts/{POST_ID}",
        data=json.dumps({
            "content": out,
            "title": f"Top {n} WooCommerce Dropship Plugins, Verified for 2026",
            "meta": {"_yoast_wpseo_title": f"Top {n} WooCommerce Dropship Plugins (2026) | Virtina"},
        }).encode("utf-8"), headers=H, method="POST"), timeout=300)

    back = json.load(urllib.request.urlopen(urllib.request.Request(
        f"https://virtina.com/wp-json/wp/v2/posts/{POST_ID}?context=edit",
        headers=H), timeout=300))
    print("  sha match:", hashlib.sha256(back["meta"]["tve_updated_post"].encode()).hexdigest()
          == hashlib.sha256(out.encode()).hexdigest())
    print("  status  :", back["status"], "| cats:", back.get("categories"),
          "| featured:", back.get("featured_media"))
    print("  title   :", back["title"]["raw"][:70])


if __name__ == "__main__":
    main()
