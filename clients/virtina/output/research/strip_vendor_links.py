# -*- coding: utf-8 -*-
"""Remove injected/paid vendor links from Thrive markup without touching copy.

Two shapes exist on post 37791:
  1. Empty anchors wrapping only whitespace/&nbsp; -> delete the whole anchor.
  2. Anchors wrapping real text, including whole H2 headings such as
     <a href="bigcommerce...">5. Target</a> -> UNWRAP, keeping the inner text
     exactly. Deleting these would delete the heading.

Never touches virtina.com links or the retail brand links on surviving sections.
"""
import re

VENDOR_DOMAINS = [
    "virtocommerce.com",
    "sharetribe.com",
    "webkul.com",
    "cedcommerce.com",
    "yo-kart.com",
    "bigcommerce.com",
    "shopify.com",
]

_ANCHOR = re.compile(r'<a\b([^>]*)>(.*?)</a>', re.S | re.I)


def _is_vendor(attrs):
    m = re.search(r'href="([^"]*)"', attrs, re.I)
    if not m:
        return False
    href = m.group(1).lower()
    if "virtina.com" in href:
        return False
    return any(d in href for d in VENDOR_DOMAINS)


def strip(markup):
    """Returns (new_markup, report)."""
    report = {"unwrapped": [], "deleted": 0, "kept_text_chars": 0}

    def repl(m):
        attrs, inner = m.group(1), m.group(2)
        if not _is_vendor(attrs):
            return m.group(0)
        visible = re.sub(r'<[^>]+>', '', inner)
        visible = visible.replace('&nbsp;', ' ').replace(' ', ' ')
        if visible.strip() == '':
            report["deleted"] += 1
            return ''                      # invisible link, remove entirely
        report["unwrapped"].append(visible.strip()[:40])
        report["kept_text_chars"] += len(inner)
        return inner                       # keep the words, drop the link

    out = _ANCHOR.sub(repl, markup)
    return out, report


def verify(before, after, report):
    """Structural guards. Returns list of problems, empty if clean."""
    problems = []
    # no vendor href may survive
    for d in VENDOR_DOMAINS:
        n = len(re.findall(re.escape(d), after, re.I))
        if n:
            problems.append(f"{d} still present {n}x")
    # heading text must be byte-identical after stripping tags
    def headings(s):
        return [re.sub(r'\s+', ' ', re.sub('<[^>]+>', '', h)).strip()
                for h in re.findall(r'<h2[^>]*>(.*?)</h2>', s, re.S | re.I)]
    hb, ha = headings(before), headings(after)
    if hb != ha:
        diff = [(x, y) for x, y in zip(hb, ha) if x != y]
        problems.append(f"H2 TEXT CHANGED: {diff[:3]}")
    # div balance must be untouched
    ob = len(re.findall(r'<div\b', before, re.I)), len(re.findall(r'</div\s*>', before, re.I))
    oa = len(re.findall(r'<div\b', after, re.I)), len(re.findall(r'</div\s*>', after, re.I))
    if ob != oa:
        problems.append(f"div counts changed {ob} -> {oa}")
    # no data-css invented
    if set(re.findall(r'data-css="([^"]+)"', after)) - set(re.findall(r'data-css="([^"]+)"', before)):
        problems.append("invented data-css tokens")
    return problems
