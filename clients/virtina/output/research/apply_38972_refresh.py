# -*- coding: utf-8 -*-
"""Apply the 2026-09-08 refresh to live post 38972 (virtina.com).

    https://virtina.com/woocommerce-dropshipping-plugins/
    target keyword: "woocommerce dropship plugin", currently position 7

DRY RUN by default. Pass 'publish' to write.

What it does:
  1. drop plugin entries that research confirmed are dead
  2. renumber the survivors so the list is contiguous again
  3. fix the count everywhere it is stated (H1, Yoast, the table heading)
  4. splice in any new sections written as BLOCK fragments
  5. rebuild the Table of Contents to match
  6. verify, then push

Safety, because this page is LIVE and ranking at position 7:
  * source of truth is the on-disk backup, never a re-read of a half-edited page
  * status / categories / featured_media are never sent
  * the body goes through Thrive's own endpoint, which is the ONLY thing that
    writes tve_updated_post. The core REST meta route accepts it and silently
    discards it (verified 2026-09-07 on post 37791)
  * read-back compares sha256 of what we sent against what stuck
"""
import os, sys, re, io, json, base64, hashlib, urllib.request, html as _html

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from thrive_edit_lib import block_bounds, integrity, DIV_OPEN, DIV_CLOSE

ROOT = r"C:\content-intel"
BK = os.path.join(ROOT, r"clients\virtina\output\backups\post-38972-tve_updated_post-2026-09-08.html")
BLOCKS = os.path.join(ROOT, r"clients\virtina\output\drafts\woocommerce-dropship-blocks-2026-09-08.html")
PREVIEW = os.path.join(ROOT, r"clients\virtina\output\research\_38972_final_preview.html")
POST_ID = 38972
DRY = "publish" not in sys.argv

# Cut list, from the 2026-09-08 verification. Each has a reason, because a
# "Top N (Updated 2026)" list that recommends a dead or miscategorised tool costs
# more trust than a missing keyword does.
CUT_PLUGINS = [
    "Beeketing",      # WP.org plugin last updated 2019-12-19; beeketing.com now 301s to shopbase.com
    "Ezusy",          # domain does not resolve (DNS ENOTFOUND)
    "Cartflows",      # category error: it is a funnel and checkout builder, no supplier or fulfilment function
    "Modalyst",       # dropped WooCommerce; lists Shopify/Wix/BigCommerce/Alibaba only, /woocommerce/ 404s
    "Zendrop",        # dropped WooCommerce; Shopify, Wix, TikTok Shop, ClickFunnels only
    "AliNext Lite",   # DUPLICATE of Ali2Woo, same plugin (slug ali2woo-lite), listed twice
    "NextsChain",     # serves ScaleOrder content, could not be verified as a distinct product
    "WooDropship",    # zombie: blog stops Jul 2023, no current pricing. NOTE: post 31786 still
                      # recommends it, so that page needs the same correction.
]
# Renames verified 2026-09-08. Applied to the surviving entries.
RENAMES = {
    "WooShark WooCommerce Dropshipping": "SharkDropship",   # renamed
    "AutoD": "AutoDS",                                      # the page had the name wrong
}
NEW_TITLE = "Top 17 WooCommerce Dropship Plugins, Verified for 2026"
YOAST_TITLE = "Top 17 WooCommerce Dropship Plugins (2026) | Virtina"
YOAST_DESC = ("We checked every WooCommerce dropship plugin on this list in September 2026 and cut "
              "8 that are dead, duplicated, or no longer support WooCommerce. Here are the 17 left.")
YOAST_FOCUS = "woocommerce dropship plugin"

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


def plugin_entries(s):
    """Every numbered plugin H3 with its balanced enclosing content box."""
    out = []
    for m in re.finditer(r'<h3[^>]*>(.*?)</h3>', s, re.S | re.I):
        t = re.sub(r'\s+', ' ', _html.unescape(re.sub('<[^>]+>', '', m.group(1)))).strip()
        if re.match(r'^\d+\.', t):
            b = block_bounds(s, m.start())
            if b:
                name = re.sub(r'^\d+\.\s*', '', t)
                out.append({"label": t, "name": name, "start": b[0], "end": b[1]})
    return out


_H3 = re.compile('(<h3[^>]*>)(.*?)(</h3>)', re.S | re.I)


def set_number(block, n, name):
    """Rewrite the entry's H3 to '<n>. <name>'. Replaces the WHOLE inner content,
    because some headings wrap their text in a nested <a> or <span>."""
    return _H3.sub(lambda m: f'{m.group(1)}{n}. {name}{m.group(3)}', block, count=1)


def load_blocks():
    if not os.path.exists(BLOCKS):
        return {}
    raw = io.open(BLOCKS, encoding="utf-8").read()
    return {m.group(1).strip(): m.group(2).strip()
            for m in re.finditer(r'<!--\s*BLOCK id=([a-z0-9-]+)\s*-->(.*?)<!--\s*/BLOCK\s*-->',
                                 raw, re.S | re.I)}


def main():
    src = io.open(BK, encoding="utf-8").read()
    print(f"source (backup): {len(src)} chars, divs "
          f"{len(DIV_OPEN.findall(src))}/{len(DIV_CLOSE.findall(src))}")

    ents = plugin_entries(src)
    print(f"  plugin entries found: {len(ents)}")
    if not ents:
        raise SystemExit("BLOCKING: no plugin entries located")

    if not CUT_PLUGINS:
        print("\n  CUT_PLUGINS is empty. Fill it from the research verdicts before publishing.")
        for e in ents:
            print(f"     {e['label']}")
        if not DRY:
            raise SystemExit("BLOCKING: refusing to publish with no cut list decided")
        return

    keep = [e for e in ents if not any(c.lower() in e["name"].lower() for c in CUT_PLUGINS)]
    dropped = [e["name"] for e in ents if e not in keep]
    print(f"  cutting {len(dropped)}: {dropped}")
    print(f"  keeping {len(keep)}")

    # rebuild the plugin run in order, renumbered
    head = src[:ents[0]["start"]]
    tail = src[ents[-1]["end"]:]
    run = "".join(set_number(src[e["start"]:e["end"]], i, RENAMES.get(e["name"], e["name"]))
                  for i, e in enumerate(keep, 1))
    out = head + run + tail

    blocks = load_blocks()
    if blocks:
        print(f"  blocks available: {sorted(blocks)}")

    # ---- drop the market-statistics block -------------------------------
    # All five figures failed verification on 2026-09-08. The $365.67bn number is
    # Grand View's 2025 figure labelled 2024, the $802.33bn apparel figure is
    # untraceable and mis-scoped, and three firms' 2025 estimates span a 60%
    # range. Virtina's rules require a named, dated source per figure, so the
    # whole block goes rather than shipping numbers we cannot stand behind.
    mstart = out.find('<div class="thrv_wrapper thrv_text_element" id="global-dropshipping-market-trends">')
    mend = out.find('id="role-of-dropshipping-plugins-in-a-woocommerce-website"')
    if mstart != -1 and mend != -1:
        mend = out.rfind('<div', 0, mend)
        seg = out[mstart:mend]
        if len(re.findall(r'<div\b', seg)) == len(re.findall(r'</div\s*>', seg)):
            out = out[:mstart] + out[mend:]
            print(f"  removed unsourced market-statistics block ({len(seg)} chars)")
        else:
            raise SystemExit("BLOCKING: market block span is not balanced, refusing to cut")
    else:
        print("  market-statistics block not found (already removed?)")

    # ---- TOC repairs -----------------------------------------------------
    # This href is missing its '#', so it points at a nonexistent external host
    # and has been sending readers off-site.
    if 'href="http://best-woocommerce-dropshipping-plugins"' in out:
        out = out.replace('href="http://best-woocommerce-dropshipping-plugins"',
                          'href="#best-woocommerce-dropshipping-plugins"')
        print("  fixed broken TOC anchor (was http://, now #)")
    # drop the TOC entry for the section we just removed
    li = re.search(r'<li[^>]*>(?:(?!</li>).)*?href="#global-dropshipping-market-trends".*?</li>',
                   out, re.S | re.I)
    if li:
        out = out[:li.start()] + out[li.end():]
        print("  removed TOC entry for the deleted market section")

    # ---- rebuild the plugin list inside the Table of Contents ------------
    # The TOC carries its own copy of all 25 plugin names with the old numbers.
    # Cutting entries from the body without rebuilding this leaves the TOC
    # advertising plugins the page no longer covers.
    toc_anchor = out.find("1. AliDropship")
    if toc_anchor != -1:
        ul_start = out.rfind("<ul", 0, toc_anchor)
        ul_end = out.find("</ul>", toc_anchor) + 5
        seg = out[ul_start:ul_end]
        lis = re.findall(r'<li\b.*?</li>', seg, re.S)
        if len(lis) >= len(ents):
            tmpl = lis[0]
            kept_names = [RENAMES.get(e["name"], e["name"]) for e in keep]
            # The visible label lives inside the list item's
            # tcb-styled-list-icon-text span, after the icon markup. Replace only
            # that span's contents so the icon, the <br> and every data-css token
            # survive untouched.
            LABEL = re.compile(
                r'(<span class="[^"]*tcb-styled-list-icon-text[^"]*"[^>]*>)(.*?)(</span>)', re.S)
            if not LABEL.search(tmpl):
                raise SystemExit("BLOCKING: cannot locate the TOC label node, refusing to guess")
            new_lis = [LABEL.sub(lambda m: f"{m.group(1)}{i}. {name}<br>{m.group(3)}", tmpl, count=1)
                       for i, name in enumerate(kept_names, 1)]
            first = seg.find(lis[0])
            last = seg.rfind(lis[-1]) + len(lis[-1])
            rebuilt = seg[:first] + "".join(new_lis) + seg[last:]
            out = out[:ul_start] + rebuilt + out[ul_end:]
            print(f"  rebuilt TOC plugin list: {len(lis)} -> {len(new_lis)} entries")

    # ---- prune the comparison table --------------------------------------
    # The table carries its own row per plugin. Cutting entries from the body
    # without pruning here leaves the table recommending tools the page just
    # dropped, which is worse than not having pruned at all.
    cut_names = {"Beeketing", "Ezusy", "Cartflows", "Modalyst", "Zendrop",
                 "AliNext Lite", "NextsChain", "WooDropship"}
    # The table markup is stored HTML-ESCAPED inside the Thrive meta
    # (&lt;tr&gt;&lt;td&gt;...), so it has to be matched in that form. A literal
    # <tr> search silently finds nothing and prunes nothing.
    removed_rows = 0
    for row in re.findall(r'&lt;tr&gt;.*?&lt;/tr&gt;', out, re.S | re.I):
        cell = re.search(r'&lt;td&gt;(.*?)&lt;/td&gt;', row, re.S | re.I)
        if not cell:
            continue
        label = re.sub(r'\s+', ' ', _html.unescape(re.sub('<[^>]+>', '', cell.group(1)))).strip()
        if any(c.lower() in label.lower() for c in cut_names):
            out = out.replace(row, "", 1)
            removed_rows += 1
            print(f"     pruned table row: {label}")
    print(f"  comparison table: {removed_rows} row(s) removed")
    if removed_rows != len(cut_names):
        print(f"     NOTE: {len(cut_names)} plugins were cut but {removed_rows} rows matched")
    # the table uses short names; apply the same renames
    out = re.sub(r'(&lt;td&gt;)\s*WooShark\s*(&lt;/td&gt;)', r'\1SharkDropship\2', out)
    out = re.sub(r'(&lt;td&gt;)\s*AutoD\s*(&lt;/td&gt;)', r'\1AutoDS\2', out)

    # ---- fix the FAQ example that names a dead plugin --------------------
    # The "are there free plugins?" answer used Ezusy as its example, and the
    # same sentence is duplicated inside the FAQPage JSON-LD. Ezusy's domain no
    # longer resolves. Ali2Woo is on the list, free, and was updated 2026-09-07.
    dead_example = "Ezusy, for example, provides a free version for AliExpress product imports."
    live_example = "Ali2Woo, for example, provides a free version for AliExpress product imports."
    if dead_example in out:
        n_ex = out.count(dead_example)
        out = out.replace(dead_example, live_example)
        print(f"  replaced dead plugin named in the FAQ example ({n_ex} place(s), incl. schema)")

    # ---- verification note ----------------------------------------------
    # The page ranks at 7 for "woocommerce dropship plugin" while never using the
    # phrase once. This paragraph fixes that AND earns it, by stating what the
    # 2026 check actually found. Clones the page's own content-box tokens; no new
    # data-css is invented.
    n = len(keep)
    note = (
        '<div class="thrv_wrapper thrv_contentbox_shortcode thrv-content-box tve-elem-default-pad" '
        'data-css="tve-u-190e3829613" style="" id="verified-2026">\n'
        '\t<div class="tve-content-box-background" style="" data-css="tve-u-190e37dda6d"></div>\n'
        '\t<div class="tve-cb"><div class="thrv_wrapper thrv_text_element" id="">'
        '<h2 class="" data-css="tve-u-194a8b075f1">What changed in the 2026 check</h2></div>'
        '<div class="thrv_wrapper thrv_text_element"><p dir="ltr" style="">'
        '<span style="font-size: 16px !important;">'
        'Every WooCommerce dropship plugin on this page was re-checked in September 2026. '
        'Eight entries came off the list. Two had shut down, two no longer support WooCommerce, '
        'one appeared twice under an old name and a current one, and one was never a dropship '
        'plugin at all. That leaves the ' + str(n) + ' below.'
        '</span></p><p dir="ltr" style=""><span style="font-size: 16px !important;">'
        'We mention it because most lists of this kind are never re-checked. If a dropship plugin '
        'here stops supporting WooCommerce, it comes off at the next review rather than sitting '
        'here collecting clicks.'
        '</span></p></div></div>\n</div>')
    marker = '<div class="thrv_wrapper thrv_contentbox_shortcode thrv-content-box tve-elem-default-pad" data-css="tve-u-190e3829613" style="" id="role-of-dropshipping-plugins-in-a-woocommerce-website">'
    if marker in out and 'id="verified-2026"' not in out:
        out = out.replace(marker, note + marker, 1)
        print("  inserted the 2026 verification note (carries the exact keyword)")

    # ---- fix an editorial instruction left in public alt text --------------
    bad_alt = "Just update the previous image by addingb these also AutoDS, CJdropshipping ,Printify, Zendrop"
    if bad_alt in out:
        out = out.replace(bad_alt,
                          "WooCommerce dropship plugin logos including AutoDS, CJdropshipping and "
                          "Printify shown together on a product comparison graphic")
        print("  replaced leftover editorial note that was published as image alt text")

    # count corrections
    out = re.sub(r'\b25 Popular\b', f'{n} Popular', out)
    out = re.sub(r'\bTop 20 WooCommerce Dropshipping Plugins\b',
                 f'Top {n} WooCommerce Dropship Plugins', out)

    probs = integrity(src, out)
    if probs:
        raise SystemExit(f"BLOCKING: integrity failed: {probs}")
    print(f"  integrity CLEAN | {len(src)} -> {len(out)} chars")
    io.open(PREVIEW, "w", encoding="utf-8").write(out)

    if DRY:
        print("\nDRY RUN. Nothing pushed. Preview:", PREVIEW)
        return

    H = headers()
    tcb = urllib.request.urlopen(urllib.request.Request(
        f"https://virtina.com/wp-json/tcb/v1/posts/{POST_ID}/content",
        data=json.dumps({"tve_content": out}).encode("utf-8"),
        headers=H, method="POST"), timeout=300)
    print("THRIVE push:", tcb.status)

    payload = {"content": out, "meta": {"_yoast_wpseo_focuskw": YOAST_FOCUS}}
    if NEW_TITLE:
        payload["title"] = NEW_TITLE
    if YOAST_TITLE:
        payload["meta"]["_yoast_wpseo_title"] = YOAST_TITLE
    if YOAST_DESC:
        payload["meta"]["_yoast_wpseo_metadesc"] = YOAST_DESC
    urllib.request.urlopen(urllib.request.Request(
        f"https://virtina.com/wp-json/wp/v2/posts/{POST_ID}",
        data=json.dumps(payload).encode("utf-8"), headers=H, method="POST"), timeout=300)

    back = json.load(urllib.request.urlopen(urllib.request.Request(
        f"https://virtina.com/wp-json/wp/v2/posts/{POST_ID}?context=edit",
        headers=H), timeout=300))
    live = back["meta"]["tve_updated_post"]
    print("  sha match:", hashlib.sha256(live.encode()).hexdigest() ==
          hashlib.sha256(out.encode()).hexdigest())
    print("  status  :", back["status"], "| cats:", back.get("categories"),
          "| featured:", back.get("featured_media"))
    print("  focus kw:", back["meta"].get("_yoast_wpseo_focuskw"))


if __name__ == "__main__":
    main()
