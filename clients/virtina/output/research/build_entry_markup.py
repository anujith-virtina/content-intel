# -*- coding: utf-8 -*-
"""Generate Thrive entry markup for post 38972 from the page's OWN template.

The plugin entries on that page are nested Thrive content boxes: an outer box
holding an H3 name, then one sub-box per question, each with a "⇨" H4 and one
paragraph. Hand-writing that markup is how layouts get broken, so this clones the
live template and swaps only the text nodes. Every data-css token comes from the
page; none is invented.

Content comes from the creator as plain structured text:

    ===PLUGIN===
    name: ...
    q: ...
    a: ...
    ===END===
"""
import io, re, html as _html

TEMPLATE = r"C:\content-intel\clients\virtina\output\research\_entry_template.html"

# tokens lifted from the live page, verified present in tve_custom_css
BOX = 'tve-u-190e3829613'      # outer entry content box
BOXBG = 'tve-u-1946a463c95'    # its background
SUBBOX = 'tve-u-194dbb8d41e'   # one q/a sub-box
SUBWRAP = 'tve-u-19200614771'  # text wrapper inside the sub-box


def _esc(t):
    return _html.escape(t, quote=False)


def build_entry(number, name, qas):
    """Return Thrive markup for one plugin entry."""
    subs = []
    for q, a in qas:
        subs.append(
            f'<div class="thrv_wrapper thrv_contentbox_shortcode thrv-content-box '
            f'tve-elem-default-pad" data-css="{SUBBOX}" style="">\n'
            f'\t<div class="tve-content-box-background"></div>\n'
            f'\t<div class="tve-cb"><div class="thrv_wrapper thrv_text_element" '
            f'data-css="{SUBWRAP}"><h4 class="" style="">'
            f'<strong><span style="">\u21e8&nbsp;</span></strong>'
            f'<span style="font-weight: normal;"><span style="">{_esc(q)}</span></span>'
            f'</h4></div>'
            f'<div class="thrv_wrapper thrv_text_element"><p>{_esc(a)}</p></div></div>\n'
            f'</div>')
    return (
        f'<div class="thrv_wrapper thrv_contentbox_shortcode thrv-content-box '
        f'tve-elem-default-pad" data-css="{BOX}" style="" id="">\n'
        f'\t<div class="tve-content-box-background" style="--tve-border-width: 0px; '
        f'border: none !important;" data-css="{BOXBG}"></div>\n'
        f'\t<div class="tve-cb"><div class="thrv_wrapper thrv_text_element" id="">'
        f'<h3 class="">{number}. {_esc(name)}</h3></div>'
        + "".join(subs) +
        '</div>\n</div>')


def parse_entries(path):
    raw = io.open(path, encoding="utf-8").read()
    out = []
    for blk in re.findall(r'===PLUGIN===(.*?)===END===', raw, re.S):
        name, qas, q = None, [], None
        for line in blk.splitlines():
            line = line.strip()
            if line.lower().startswith("name:"):
                name = line.split(":", 1)[1].strip()
            elif line.lower().startswith("q:"):
                q = line.split(":", 1)[1].strip()
            elif line.lower().startswith("a:") and q:
                qas.append((q, line.split(":", 1)[1].strip()))
                q = None
        if name and qas:
            out.append((name, qas))
    return out


def parse_pricing_intro(path):
    raw = io.open(path, encoding="utf-8").read()
    m = re.search(r'===PRICING-INTRO===(.*?)===END===', raw, re.S)
    if not m:
        return None, []
    heading, paras = None, []
    for line in m.group(1).splitlines():
        line = line.strip()
        if line.lower().startswith("heading:"):
            heading = line.split(":", 1)[1].strip()
        elif line.lower().startswith("a:"):
            paras.append(line.split(":", 1)[1].strip())
    return heading, paras


def build_pricing_section(heading, paras, rows, checked="8 September 2026"):
    """rows: list of (plugin, price).

    IMPORTANT, learned the hard way on 2026-09-08: write the table as LITERAL
    HTML here, not escaped entities. The page's original comparison table is
    stored escaped and renders fine because it lives in a widget that decodes
    entities on output. A plain thrv_text_element does NOT decode, so an escaped
    table published into one renders as visible "&lt;table&gt;&lt;tr&gt;" text to
    every reader. Match the container, not the neighbouring markup.
    """
    th = ('<tr><th>Dropship plugin</th>'
          '<th>Price, checked ' + checked + '</th></tr>')
    body = "".join(f'<tr><td>{_esc(p)}</td><td>{_esc(v)}</td></tr>' for p, v in rows)
    table = '<table><thead>' + th + '</thead><tbody>' + body + '</tbody></table>'
    ps = "".join(f'<p>{_esc(x)}</p>' for x in paras)
    return (
        f'<div class="thrv_wrapper thrv_contentbox_shortcode thrv-content-box '
        f'tve-elem-default-pad" data-css="{BOX}" style="" id="dropship-plugin-pricing">\n'
        f'\t<div class="tve-content-box-background" style="" data-css="{BOXBG}"></div>\n'
        f'\t<div class="tve-cb"><div class="thrv_wrapper thrv_text_element" id="">'
        f'<h2 class="">{_esc(heading)}</h2></div>'
        f'<div class="thrv_wrapper thrv_text_element">{ps}{table}</div>'
        f'</div>\n</div>')


if __name__ == "__main__":
    import sys
    src = sys.argv[1] if len(sys.argv) > 1 else \
        r"C:\content-intel\clients\virtina\output\drafts\dropship-new-entries-2026-09-08.txt"
    ents = parse_entries(src)
    print(f"parsed {len(ents)} plugin entries")
    for name, qas in ents:
        print(f"   {name[:44]:44} {len(qas)} q/a")
    h, ps = parse_pricing_intro(src)
    print(f"pricing intro: heading={h!r}, {len(ps)} paragraph(s)")
