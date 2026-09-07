# -*- coding: utf-8 -*-
"""Give the 6 retained entries on post 37791 the same sourced opening the new ones have.

Amazon, AliExpress, Walmart, eBay, Etsy and Shein kept their original 2024 copy
through the refresh: no figure, no source. Temu, Coupang, Ozon and Rakuten all
open with the metric and its source, so the page contradicted its own stated rule
that every number carries a source.

This PREPENDS one sourced paragraph to each of those six and leaves the existing
prose untouched below it, so nothing already ranking is removed.

Every figure here is from the same single metric the page ranks by
(Semrush Traffic Analytics, total monthly website visits, July 2026) or from the
company's own filing, named inline. No new claims.

DRY RUN by default. Pass 'publish' to write.
"""
import os, sys, re, io, json, base64, hashlib, urllib.request

ROOT = r"C:\content-intel"
POST_ID = 37791
DRY = "publish" not in sys.argv

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

P_OPEN = '<div class="thrv_wrapper thrv_text_element"><p dir="ltr" style=""><span style="font-size: 16px !important;">'
P_CLOSE = '</span></p></div>'

# id -> sourced opening paragraph
COPY = {
    "amazon": (
        "Amazon is the most-visited shopping site in the world, at 2.42B monthly visits in July 2026 "
        "on Semrush Traffic Analytics. Amazon.com, Inc. trades on the Nasdaq as AMZN and reported "
        "US$716.9B in net sales for FY2025 in its annual report on Form 10-K. It is the only site on "
        "this list that leads on both traffic and disclosed revenue."
    ),
    "aliexpress": (
        "AliExpress drew 699.81M monthly visits in July 2026 on Semrush Traffic Analytics, third on "
        "this list. It is Alibaba Group's cross-border marketplace, which is why its traffic is spread "
        "across many countries rather than concentrated in one. Read it as Alibaba's export shop "
        "window, not as the company's domestic business."
    ),
    "walmart": (
        "Walmart drew 562.88M monthly visits in July 2026 on Semrush Traffic Analytics. Walmart Inc. "
        "trades on the NYSE as WMT and reported US$150.4B in global eCommerce sales for FY2025. It is "
        "the clearest example on this list of physical stores being used as eCommerce infrastructure."
    ),
    "ebay": (
        "eBay drew 556.74M monthly visits in July 2026 on Semrush Traffic Analytics, close behind "
        "Walmart. eBay Inc. trades on the Nasdaq as EBAY and reported US$79.6B in gross merchandise "
        "volume for FY2025. Its traffic holds up because buyers arrive looking for specific items "
        "rather than browsing."
    ),
    "etsy": (
        "Etsy drew 372.66M monthly visits in July 2026 on Semrush Traffic Analytics. Etsy, Inc. trades "
        "on the Nasdaq as ETSY. It is the smallest company in this top ten by revenue and still "
        "outranks far larger retailers on traffic, which is what category focus buys you."
    ),
    "shein": (
        "Shein drew 321.71M monthly visits in July 2026 on Semrush Traffic Analytics. The group is "
        "headquartered in Singapore and listed in Hong Kong on 1 September 2026 under stock code "
        "00625, having reported US$41.8B in revenue. Its supply chain remains largely in China."
    ),
}


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


def main():
    H = headers()
    d = json.load(urllib.request.urlopen(urllib.request.Request(
        f"https://virtina.com/wp-json/wp/v2/posts/{POST_ID}?context=edit",
        headers=H), timeout=300))
    s = d["meta"]["tve_updated_post"]
    print(f"live thrive markup: {len(s)} chars")

    io.open(os.path.join(ROOT, r"clients\virtina\output\backups\post-37791-tve_pre-entrycopy.html"),
            "w", encoding="utf-8").write(s)

    out = s
    for sec, para in COPY.items():
        m = re.search(r'<div class="thrv_wrapper thrv_contentbox_shortcode[^"]*"[^>]*id="' + sec + r'"[^>]*>', out)
        if not m:
            raise SystemExit(f"BLOCKING: section #{sec} not found")
        # insert after the section's heading text element closes
        h = re.search(r'</h2>\s*</div>', out[m.end():])
        if not h:
            raise SystemExit(f"BLOCKING: no heading wrapper end in #{sec}")
        at = m.end() + h.end()
        if para[:40] in out:
            print(f"  #{sec:11} already present, skipping")
            continue
        out = out[:at] + P_OPEN + para + P_CLOSE + out[at:]
        print(f"  #{sec:11} sourced opening added ({len(para)} chars)")

    # guards
    if len(re.findall(r'<div\b', out)) != len(re.findall(r'</div\s*>', out)):
        raise SystemExit("BLOCKING: div imbalance")
    if set(re.findall(r'data-css="([^"]+)"', out)) - set(re.findall(r'data-css="([^"]+)"', s)):
        raise SystemExit("BLOCKING: invented data-css token")
    if "\u2014" in out or "&mdash;" in out:
        raise SystemExit("BLOCKING: em dash")
    for sec in COPY:
        if f'id="{sec}"' not in out:
            raise SystemExit(f"BLOCKING: lost anchor id {sec}")
    print(f"  checks OK | {len(s)} -> {len(out)} chars")

    if DRY:
        print("\nDRY RUN. Nothing pushed.")
        return

    urllib.request.urlopen(urllib.request.Request(
        f"https://virtina.com/wp-json/tcb/v1/posts/{POST_ID}/content",
        data=json.dumps({"tve_content": out}).encode("utf-8"),
        headers=H, method="POST"), timeout=300)
    urllib.request.urlopen(urllib.request.Request(
        f"https://virtina.com/wp-json/wp/v2/posts/{POST_ID}",
        data=json.dumps({"content": out}).encode("utf-8"),
        headers=H, method="POST"), timeout=300)

    back = json.load(urllib.request.urlopen(urllib.request.Request(
        f"https://virtina.com/wp-json/wp/v2/posts/{POST_ID}?context=edit",
        headers=H), timeout=300))
    live = back["meta"]["tve_updated_post"]
    print("\nPUSHED | sha match:",
          hashlib.sha256(live.encode()).hexdigest() == hashlib.sha256(out.encode()).hexdigest(),
          "| status:", back["status"])


if __name__ == "__main__":
    main()
