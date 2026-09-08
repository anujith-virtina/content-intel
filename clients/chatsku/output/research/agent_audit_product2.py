# -*- coding: utf-8 -*-
"""Audit 2b: widen the product-page sample.

Where the sitemap route found nothing, take one product link off the homepage
instead. Same single-page analysis, merged into the same results file so the
post's numbers come from one dataset.
"""
import urllib.request, urllib.error, re, json, io, time, gzip
from urllib.parse import urljoin, urlparse

import agent_audit_product as A   # reuse get() and analyse()

RESULTS = r"C:\content-intel\clients\chatsku\output\research\agent_audit_product.json"

PROD = re.compile(r'/(product|products|prd|item|itm|catalog|catalogue|detail|sku|part)[/-][^"\'#?]{3,}', re.I)


def homepage_product_link(host):
    for scheme in ("https://www.", "https://"):
        try:
            st, html, final = A.get(scheme + host + "/", timeout=40)
        except Exception:
            continue
        hrefs = re.findall(r'href="([^"]+)"', html)
        cands = []
        for h in hrefs:
            if h.startswith(("mailto:", "tel:", "javascript:")):
                continue
            full = urljoin(final, h)
            if urlparse(full).netloc.replace("www.", "") != host:
                continue
            if PROD.search(urlparse(full).path):
                cands.append(full)
        if cands:
            # prefer the deepest path, most likely an actual product
            cands.sort(key=lambda u: len(urlparse(u).path), reverse=True)
            return cands[0]
    return None


def main():
    out = json.load(io.open(RESULTS, encoding="utf-8"))
    todo = [h for h, r in out.items() if r.get("http") != 200]
    print("retrying:", todo)
    for host in todo:
        url = None
        try:
            url = homepage_product_link(host)
        except Exception as e:
            print(f"{host:22} homepage error {repr(e)[:50]}")
        if not url:
            print(f"{host:22} no product link on homepage either")
            time.sleep(2)
            continue
        try:
            st, html, final = A.get(url, timeout=45)
            rec = {"host": host, "product_url": url, "http": st, "via": "homepage"}
            rec.update(A.analyse(html))
            out[host] = rec
            print(f"{host:22} {st} words={rec['visible_words']:5} "
                  f"Product-schema={rec['has_Product_schema']!s:5} "
                  f"price_sd={rec['price_in_structured_data']!s:5} "
                  f"stock={rec['stock_words']!s:5} wall={rec['login_or_quote_wall']!s:5}")
        except urllib.error.HTTPError as e:
            out[host] = {"host": host, "product_url": url, "http": e.code, "status": "blocked", "via": "homepage"}
            print(f"{host:22} HTTP {e.code}")
        except Exception as e:
            print(f"{host:22} ERR {repr(e)[:50]}")
        time.sleep(3)

    io.open(RESULTS, "w", encoding="utf-8").write(json.dumps(out, indent=1))
    ok = [r for r in out.values() if r.get("http") == 200]
    print(f"\nproduct pages analysed: {len(ok)}/{len(out)}")
    for k in ("has_Product_schema", "price_in_structured_data",
              "availability_in_structured_data", "mpn_or_gtin_in_structured_data",
              "price_text_anywhere", "stock_words", "login_or_quote_wall"):
        n = sum(1 for r in ok if r.get(k))
        print(f"   {k:34} {n}/{len(ok)}")
    thin = [r for r in ok if r.get("visible_words", 0) < 250]
    print(f"   pages under 250 visible words        {len(thin)}/{len(ok)}")
    for r in ok:
        print(f"      {r['host']:22} {r.get('visible_words'):5} words, "
              f"{r.get('jsonld_blocks')} json-ld, {r.get('spec_table_rows')} table rows")


if __name__ == "__main__":
    main()
