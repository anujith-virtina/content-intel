# -*- coding: utf-8 -*-
"""Audit 2: what can an AI agent actually read on a real B2B product page?

For each reachable catalog: find one real product URL from the site's own sitemap
(declared in robots.txt), fetch that single page, and record what a retrieval
system would actually get.

Checks, all of them things an agent needs before it can shortlist you:
  * did the page even load for a non-browser client
  * schema.org Product markup present (JSON-LD or microdata)
  * price present in markup, and price present in structured data
  * availability / stock present
  * a manufacturer part number or GTIN present
  * spec values in HTML text vs only in a linked PDF
  * how much of the page is JS-dependent (near-empty HTML body)

One product page per host. Public pages only.
"""
import urllib.request, urllib.error, re, json, io, time, gzip

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

HOSTS = ["grainger.com", "mcmaster.com", "mscdirect.com", "zoro.com",
         "globalindustrial.com", "digikey.com", "mouser.com", "newark.com",
         "ferguson.com", "borderstates.com", "rexelusa.com", "kaman.com",
         "sonepar.com"]

PRODUCT_HINT = re.compile(r'/(product|products|prd|p|item|itm|catalog|catalogue|shop|buy|detail|sku|part|parts)[/-]', re.I)


def get(url, timeout=35):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept-Encoding": "gzip, identity"})
    r = urllib.request.urlopen(req, timeout=timeout)
    raw = r.read()
    if r.headers.get("Content-Encoding") == "gzip":
        try:
            raw = gzip.decompress(raw)
        except Exception:
            pass
    return r.status, raw.decode("utf-8", "ignore"), r.geturl()


def sitemaps_from_robots(host):
    for scheme in ("https://www.", "https://"):
        try:
            _, txt, _ = get(scheme + host + "/robots.txt")
            sm = re.findall(r'(?im)^\s*sitemap:\s*(\S+)', txt)
            if sm:
                return sm
        except Exception:
            continue
    return []


def find_product_url(host):
    """Walk at most 2 sitemap levels looking for something product-shaped."""
    seen = 0
    queue = sitemaps_from_robots(host)[:6]
    while queue and seen < 12:
        sm = queue.pop(0)
        seen += 1
        try:
            if sm.endswith('.gz'):
                req = urllib.request.Request(sm, headers={"User-Agent": UA})
                body = gzip.decompress(urllib.request.urlopen(req, timeout=45).read()).decode('utf-8','ignore')
            else:
                _, body, _ = get(sm, timeout=45)
        except Exception:
            continue
        locs = re.findall(r'<loc>\s*([^<\s]+)\s*</loc>', body)
        if not locs:
            continue
        if sm.endswith(".xml") and any(l.endswith(".xml") or ".xml" in l for l in locs[:5]):
            nested = [l for l in locs if PRODUCT_HINT.search(l) or "product" in l.lower()]
            queue = (nested or locs)[:3] + queue
            continue
        prods = [l for l in locs if PRODUCT_HINT.search(l)]
        if prods:
            return prods[len(prods) // 2]
    return None


def analyse(html):
    low = html.lower()
    body = re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>', ' ', html)
    text = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', body)).strip()
    jsonld = re.findall(r'(?is)<script[^>]+application/ld\+json[^>]*>(.*?)</script>', html)
    types = set()
    price_in_sd = avail_in_sd = gtin_in_sd = False
    for blk in jsonld:
        try:
            data = json.loads(blk.strip())
        except Exception:
            for m in re.finditer(r'"@type"\s*:\s*"([^"]+)"', blk):
                types.add(m.group(1))
            if '"price"' in blk:
                price_in_sd = True
            if "availability" in blk.lower():
                avail_in_sd = True
            if re.search(r'"(gtin\d*|mpn|sku)"', blk, re.I):
                gtin_in_sd = True
            continue
        for obj in (data if isinstance(data, list) else [data]):
            if isinstance(obj, dict):
                t = obj.get("@type")
                if isinstance(t, list):
                    types.update(t)
                elif t:
                    types.add(t)
                s = json.dumps(obj).lower()
                price_in_sd |= '"price"' in s
                avail_in_sd |= "availability" in s
                gtin_in_sd |= bool(re.search(r'"(gtin\d*|mpn|sku)"', s))
    return {
        "html_bytes": len(html),
        "visible_words": len(text.split()),
        "jsonld_blocks": len(jsonld),
        "schema_types": sorted(types)[:8],
        "has_Product_schema": any("product" in t.lower() for t in types),
        "price_in_structured_data": price_in_sd,
        "availability_in_structured_data": avail_in_sd,
        "mpn_or_gtin_in_structured_data": gtin_in_sd,
        "microdata_itemprop": low.count("itemprop=") > 0,
        "price_text_anywhere": bool(re.search(r'[$£€]\s?\d', text)),
        "stock_words": bool(re.search(r'\b(in stock|out of stock|availability|lead time|ships in|backorder)\b', text, re.I)),
        "login_or_quote_wall": bool(re.search(r'\b(sign in to see|log in for pric|request a quote|call for pric|price on request)\b', text, re.I)),
        "spec_table_rows": len(re.findall(r'<tr\b', body, re.I)),
        "pdf_links": len(re.findall(r'href="[^"]+\.pdf', html, re.I)),
    }


def main():
    out = {}
    for host in HOSTS:
        rec = {"host": host}
        try:
            url = find_product_url(host)
        except Exception as e:
            url = None
            rec["sitemap_error"] = repr(e)[:70]
        if not url:
            rec["status"] = "no product URL found via sitemap"
            out[host] = rec
            print(f"{host:22} no product URL from sitemap")
            time.sleep(2)
            continue
        rec["product_url"] = url
        try:
            st, html, final = get(url, timeout=45)
            rec["http"] = st
            rec.update(analyse(html))
            print(f"{host:22} {st} words={rec['visible_words']:5} "
                  f"Product-schema={rec['has_Product_schema']!s:5} "
                  f"price_sd={rec['price_in_structured_data']!s:5} "
                  f"stock={rec['stock_words']!s:5} wall={rec['login_or_quote_wall']!s:5}")
        except urllib.error.HTTPError as e:
            rec["http"] = e.code
            rec["status"] = "blocked"
            print(f"{host:22} HTTP {e.code} on the product page")
        except Exception as e:
            rec["status"] = repr(e)[:70]
            print(f"{host:22} ERR {repr(e)[:50]}")
        out[host] = rec
        time.sleep(3)

    io.open(r"C:\content-intel\clients\chatsku\output\research\agent_audit_product.json",
            "w", encoding="utf-8").write(json.dumps(out, indent=1))
    ok = [r for r in out.values() if r.get("http") == 200]
    print(f"\nproduct pages fetched: {len(ok)}/{len(HOSTS)}")
    if ok:
        def pct(k):
            n = sum(1 for r in ok if r.get(k))
            return f"{n}/{len(ok)}"
        for k in ("has_Product_schema", "price_in_structured_data",
                  "availability_in_structured_data", "mpn_or_gtin_in_structured_data",
                  "price_text_anywhere", "stock_words", "login_or_quote_wall"):
            print(f"   {k:34} {pct(k)}")


if __name__ == "__main__":
    main()
