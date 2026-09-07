# -*- coding: utf-8 -*-
"""Helpers for surgically editing Thrive Architect markup on virtina.com.

Thrive nests <div> wrappers and carries a data-css attribute on almost every one.
Regex splicing across those boundaries corrupts the layout, so every operation
here works on BALANCED div blocks located from a heading.

Verified 2026-09-07 on post 37791: the live page renders from the meta key
`tve_updated_post` (no leading underscore) and that key IS REST-writable.
Always back up before writing. See clients/virtina/output/backups/.
"""
import re
import html as _html

DIV_OPEN = re.compile(r'<div\b', re.I)
DIV_CLOSE = re.compile(r'</div\s*>', re.I)
TOKEN = re.compile(r'<div\b|</div\s*>', re.I)


def heading_text(fragment):
    """Visible text of the first heading in a fragment."""
    m = re.search(r'<h([1-6])[^>]*>(.*?)</h\1>', fragment, re.S | re.I)
    if not m:
        return ''
    return re.sub(r'\s+', ' ', _html.unescape(re.sub('<[^>]+>', '', m.group(2)))).strip()


def block_bounds(s, inner_pos, require='thrv_contentbox_shortcode'):
    """Given a position inside the markup, walk BACKWARDS to the nearest
    enclosing <div ...> that is a Thrive content box, then forward to its
    matching </div>. Returns (start, end) covering the whole balanced block.
    """
    # find candidate opening divs before inner_pos, nearest first
    opens = [m.start() for m in DIV_OPEN.finditer(s, 0, inner_pos)]
    for start in reversed(opens):
        tag_end = s.find('>', start)
        if tag_end == -1:
            continue
        tag = s[start:tag_end + 1]
        # IMPORTANT: match the CONTENT BOX, not the inner text wrapper. Walking back
        # to the nearest thrv_wrapper lands inside the box and makes every span
        # straddle the boundary into the next entry, which silently shifts ids.
        if require not in tag:
            continue
        # walk forward counting depth
        depth = 0
        for m in TOKEN.finditer(s, start):
            if m.group(0).lower().startswith('<div'):
                depth += 1
            else:
                depth -= 1
                if depth == 0:
                    end = m.end()
                    if end > inner_pos:      # block must actually contain our position
                        return start, end
                    break
    return None


def find_entry(s, heading_startswith):
    """Locate a numbered entry block by its H2 text, e.g. '10. Shopify'.
    Returns (start, end, heading_text) or None.
    """
    for m in re.finditer(r'<h2[^>]*>(.*?)</h2>', s, re.S | re.I):
        t = re.sub(r'\s+', ' ', _html.unescape(re.sub('<[^>]+>', '', m.group(1)))).strip()
        if t.lower().startswith(heading_startswith.lower()):
            b = block_bounds(s, m.start())
            if b:
                return b[0], b[1], t
    return None


def list_entries(s):
    """Every H2 with the balanced block that encloses it."""
    out = []
    for m in re.finditer(r'<h2[^>]*>(.*?)</h2>', s, re.S | re.I):
        t = re.sub(r'\s+', ' ', _html.unescape(re.sub('<[^>]+>', '', m.group(1)))).strip()
        b = block_bounds(s, m.start())
        out.append({'heading': t, 'h2_at': m.start(),
                    'block': b, 'size': (b[1] - b[0]) if b else None})
    return out


def integrity(before, after, allow_delta=None):
    """Cheap structural guards. Returns a list of problems, empty if clean."""
    problems = []
    ob, cb = len(DIV_OPEN.findall(before)), len(DIV_CLOSE.findall(before))
    oa, ca = len(DIV_OPEN.findall(after)), len(DIV_CLOSE.findall(after))
    if ob != cb:
        problems.append(f"SOURCE already unbalanced: {ob} <div> vs {cb} </div>")
    if oa != ca:
        problems.append(f"RESULT unbalanced: {oa} <div> vs {ca} </div>")
    # every data-css token in the result must have existed in the source
    src_css = set(re.findall(r'data-css="([^"]+)"', before))
    new_css = set(re.findall(r'data-css="([^"]+)"', after))
    invented = new_css - src_css
    if invented:
        problems.append(f"invented data-css ids (Thrive will not style these): {sorted(invented)[:5]}")
    return problems


def sibling_run_end(s, start):
    """From `start` (an opening <div>), consume consecutive SIBLING balanced div
    blocks and return the offset just past the last one.

    A Thrive "entry" (heading + body + image) is not one container: it is a run of
    sibling wrappers. The run ends where the next token at depth 0 is a </div>
    belonging to the PARENT, which is how the final entry on the page terminates.
    """
    pos = start
    n = len(s)
    while True:
        while pos < n and s[pos].isspace():
            pos += 1
        if pos >= n or not s.startswith('<div', pos):
            return pos
        depth = 0
        m_end = None
        for m in TOKEN.finditer(s, pos):
            if m.group(0).lower().startswith('<div'):
                depth += 1
            else:
                depth -= 1
                if depth == 0:
                    m_end = m.end()
                    break
        if m_end is None:
            return pos
        pos = m_end


def entry_spans(s):
    """Every numbered entry as (heading, start, end), boundaries balanced."""
    import re as _re
    ents = [e for e in list_entries(s) if _re.match(r'^\d+\.', e['heading']) and e['block']]
    out = []
    for i, e in enumerate(ents):
        start = e['block'][0]
        end = ents[i + 1]['block'][0] if i + 1 < len(ents) else sibling_run_end(s, start)
        out.append((e['heading'], start, end))
    return out
