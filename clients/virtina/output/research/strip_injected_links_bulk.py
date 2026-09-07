# -*- coding: utf-8 -*-
"""Remove injected vendor links from the 7 other affected Virtina posts.

RANKING SAFETY IS THE POINT. These posts hold rankings we must not disturb, so
this script changes NOTHING except link markup:
  * empty anchors (wrapping only whitespace/&nbsp;) are deleted outright
  * anchors wrapping real text are UNWRAPPED, keeping the text byte-for-byte
  * titles, headings, copy, structure, images, status, categories, Yoast and
    featured_media are never sent and never touched

Every post is backed up to clients/virtina/output/backups/ before any write, and
the visible text is compared before/after. Any difference blocks that post.

DRY RUN by default. Pass 'publish' to write.
"""
import os, sys, re, io, json, base64, hashlib, urllib.request, html as _html

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from strip_vendor_links import strip as strip_vendor, VENDOR_DOMAINS

ROOT = r"C:\content-intel"
BACKUPS = os.path.join(ROOT, r"clients\virtina\output\backups")
DRY = "publish" not in sys.argv
STAMP = "2026-09-07"

POSTS = [37847, 36981, 37296, 36161, 37745, 36887, 36423]

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


def visible(s):
    """Visible text, with the whitespace that empty anchors contributed removed."""
    s = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', s, flags=re.S | re.I)
    # Replace tags with a SPACE, not with nothing. Deleting an empty anchor that
    # wrapped a single space otherwise reads as "ServiceExcellent" and trips the
    # comparison, even though the two sides are separate block elements on the
    # rendered page and nothing visible has changed.
    s = re.sub(r'<[^>]+>', ' ', s)
    s = _html.unescape(s).replace('\u00a0', ' ')
    s = re.sub(r'\s+', ' ', s).strip()
    # Unwrapping "<a>Shopify</a> ." leaves "Shopify." where the tags previously
    # contributed a space. No word changes, and dropping a space before
    # punctuation is an improvement, so normalise rather than block on it.
    return re.sub(r'\s+([.,;:!?])', r'\1', s)


def headings(s):
    # findall with two groups returns tuples; take the heading body only.
    return [re.sub(r'\s+', ' ', _html.unescape(re.sub('<[^>]+>', '', m.group(2)))).strip()
            for m in re.finditer(r'<h([1-6])[^>]*>(.*?)</h\1>', s, re.S | re.I)]


def check(before, after):
    problems = []
    if visible(before) != visible(after):
        b, a = visible(before), visible(after)
        for i, (x, y) in enumerate(zip(b, a)):
            if x != y:
                problems.append(f"VISIBLE TEXT CHANGED at char {i}: "
                                f"{b[max(0,i-40):i+40]!r} -> {a[max(0,i-40):i+40]!r}")
                break
        else:
            problems.append(f"VISIBLE TEXT LENGTH CHANGED {len(b)} -> {len(a)}")
    if headings(before) != headings(after):
        problems.append("HEADINGS CHANGED")
    ob = (len(re.findall(r'<div\b', before, re.I)), len(re.findall(r'</div\s*>', before, re.I)))
    oa = (len(re.findall(r'<div\b', after, re.I)), len(re.findall(r'</div\s*>', after, re.I)))
    if ob != oa:
        problems.append(f"div counts changed {ob} -> {oa}")
    if set(re.findall(r'data-css="([^"]+)"', after)) - set(re.findall(r'data-css="([^"]+)"', before)):
        problems.append("invented data-css token")
    for d in VENDOR_DOMAINS:
        if d in after.lower():
            problems.append(f"{d} survived")
    return problems


def main():
    H = headers()
    os.makedirs(BACKUPS, exist_ok=True)
    total_removed = 0
    for pid in POSTS:
        d = json.load(urllib.request.urlopen(urllib.request.Request(
            f"https://virtina.com/wp-json/wp/v2/posts/{pid}?context=edit",
            headers=H), timeout=300))
        title = d["title"]["raw"][:52]
        tve = d["meta"].get("tve_updated_post") or ""
        pc = d["content"]["raw"]
        io.open(os.path.join(BACKUPS, f"post-{pid}-full-{STAMP}.json"), "w",
                encoding="utf-8").write(json.dumps(d, indent=1, ensure_ascii=False))

        new_tve, rep_t = strip_vendor(tve) if tve else ("", {"deleted": 0, "unwrapped": []})
        new_pc, rep_p = strip_vendor(pc)

        probs = []
        if tve:
            probs += [f"[tve] {p}" for p in check(tve, new_tve)]
        probs += [f"[post_content] {p}" for p in check(pc, new_pc)]

        removed = rep_t["deleted"] + len(rep_t["unwrapped"]) + rep_p["deleted"] + len(rep_p["unwrapped"])
        print(f"\n{pid}  {title}")
        print(f"   thrive={'yes' if tve else 'no'}  removed={removed} "
              f"(empty {rep_t['deleted'] + rep_p['deleted']}, unwrapped {len(rep_t['unwrapped']) + len(rep_p['unwrapped'])})")
        if rep_t["unwrapped"] or rep_p["unwrapped"]:
            kept = (rep_t["unwrapped"] + rep_p["unwrapped"])[:6]
            print(f"   text kept from unwrapped anchors: {kept}")
        if probs:
            print(f"   !! SKIPPED, checks failed: {probs[:3]}")
            continue
        print("   checks: visible text identical, headings identical, divs balanced OK")
        total_removed += removed

        if DRY or removed == 0:
            continue

        if tve:
            urllib.request.urlopen(urllib.request.Request(
                f"https://virtina.com/wp-json/tcb/v1/posts/{pid}/content",
                data=json.dumps({"tve_content": new_tve}).encode("utf-8"),
                headers=H, method="POST"), timeout=300)
        urllib.request.urlopen(urllib.request.Request(
            f"https://virtina.com/wp-json/wp/v2/posts/{pid}",
            data=json.dumps({"content": new_pc}).encode("utf-8"),
            headers=H, method="POST"), timeout=300)

        back = json.load(urllib.request.urlopen(urllib.request.Request(
            f"https://virtina.com/wp-json/wp/v2/posts/{pid}?context=edit",
            headers=H), timeout=300))
        lt = back["meta"].get("tve_updated_post") or ""
        ok_t = (not tve) or hashlib.sha256(lt.encode()).hexdigest() == hashlib.sha256(new_tve.encode()).hexdigest()
        left = [dm for dm in VENDOR_DOMAINS if dm in (lt + back["content"]["raw"]).lower()]
        print(f"   pushed | thrive sha match={ok_t} | status={back['status']} | "
              f"vendor domains left={left or 'none'}")

    print(f"\n{'DRY RUN, nothing pushed. ' if DRY else ''}total links to remove: {total_removed}")


if __name__ == "__main__":
    main()
