"""
Build styled HTML for post 42074 — final complete version.
Colors from reference post 41576 Thrive CSS (extracted from live page).
Adds: FAQ accordion, two inline images, correct font sizes, meta tags.
"""

import json, re, os, sys

try:
    from bs4 import BeautifulSoup
except ImportError:
    os.system('pip install beautifulsoup4')
    from bs4 import BeautifulSoup

# ── Colors (exact from reference post 41576) ──────────────────────────────────
HEADING_COLOR = '#43627f'
H2_FONT       = '30px'
H3_FONT       = '23px'

SUMMARY_BOX     = 'background:linear-gradient(rgba(0,213,192,0.28),rgba(0,213,192,0.28));border-radius:20px;padding:30px;margin:0 0 28px 0;'
INTRO_BOX       = 'background:linear-gradient(rgba(241,243,250,0.5),rgba(241,243,250,0.5));border-radius:20px;padding:30px;margin:0 0 28px 0;'
BLUE_BOX        = 'background:linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13));border-radius:20px;padding:30px;margin:0 0 28px 0;'
GRAY_BOX        = 'background:linear-gradient(rgba(230,230,230,0.37),rgba(230,230,230,0.37));border-radius:20px;padding:30px;margin:0 0 28px 0;'
VLIGHT_BLUE_BOX = 'background:linear-gradient(rgba(0,160,226,0.08),rgba(0,160,226,0.08));border-radius:20px;padding:30px;margin:0 0 28px 0;'
CONCLUSION_BOX  = 'background:#00d5c0;border-radius:20px;padding:30px;margin:0 0 28px 0;'

SECTION_STYLES = {
    '__summary__':   SUMMARY_BOX,
    '__intro__':     INTRO_BOX,
    'the-60-second-self-audit':                                        BLUE_BOX,
    'hosting-and-server-configuration':                                GRAY_BOX,
    'b2b-caching-why-page-caching-fails-authenticated-buyers':         BLUE_BOX,
    'checkout-failures-and-how-to-diagnose-them':                      GRAY_BOX,
    'database-bottlenecks-hpos-autoload-bloat-and-action-scheduler':   BLUE_BOX,
    'erp-sync-the-most-misdiagnosed-culprit':                          GRAY_BOX,
    'fix-in-place-vs-replatform-how-to-make-the-call':                 VLIGHT_BLUE_BOX,
    'people-also-ask':                                                 INTRO_BOX,
    'conclusion':                                                      CONCLUSION_BOX,
}

TABLE_TH_STYLE = 'background:#43627f;color:#ffffff;padding:10px 14px;text-align:left;font-weight:600;'
TABLE_TD_EVEN  = 'background:#f4f6f9;padding:10px 14px;border-bottom:1px solid #dde0e6;vertical-align:top;'
TABLE_TD_ODD   = 'background:#ffffff;padding:10px 14px;border-bottom:1px solid #dde0e6;vertical-align:top;'

SVG_ICON = ('<svg viewBox="0 0 512 512" width="10" height="10" '
            'style="fill:#43627f;flex-shrink:0;margin-top:5px;" '
            'xmlns="http://www.w3.org/2000/svg">'
            '<path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512z"/></svg>')

# Arrow-right icon — 18px matches reference blog 41576 (tve-u-19a78073f6e: --tve-icon-size:18px)
# Note: used only in cms.md template reference; style_toc() builds its own inline arrow
ARROW_SVG = ('<svg viewBox="0 0 24 24" width="18" height="18" '
             'style="fill:#43627f;" '
             'xmlns="http://www.w3.org/2000/svg">'
             '<path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg>')

# Dots icon — 17px, color #50565f matches reference blog 41576 (.tve_toggle{color:#50565f;font-size:17px})
DOTS_SVG = ('<svg viewBox="0 0 24 24" width="17" height="17" '
            'style="fill:#50565f;flex-shrink:0;" '
            'xmlns="http://www.w3.org/2000/svg">'
            '<path d="M16,12A2,2 0 0,1 18,10A2,2 0 0,1 20,12A2,2 0 0,1 18,14A2,2 0 0,1 16,12'
            'M10,12A2,2 0 0,1 12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12'
            'M4,12A2,2 0 0,1 6,10A2,2 0 0,1 8,12A2,2 0 0,1 6,14A2,2 0 0,1 4,12Z"/></svg>')

# ── Images (from WP media library) ────────────────────────────────────────────
IMG1_HTML = (
    '<span style="display:block;margin:20px 0;">'
    '<img alt="B2B ecommerce analytics dashboard showing performance metrics and order processing speed" '
    'data-id="42088" width="670" data-init-width="1400" height="287" data-init-height="600" '
    'title="" loading="lazy" '
    'src="https://virtina.com/wp-content/uploads/2026/05/b2b-ecommerce-performance-dashboard-2026.jpg" '
    'data-width="670" data-height="287" style="aspect-ratio: auto 1400 / 600;max-width:100%;height:auto;">'
    '</span>'
)

IMG2_HTML = (
    '<span style="display:block;margin:20px 0;">'
    '<img alt="Server room infrastructure for WooCommerce database optimization and high-performance B2B ecommerce" '
    'data-id="42089" width="670" data-init-width="1400" height="383" data-init-height="800" '
    'title="" loading="lazy" '
    'src="https://virtina.com/wp-content/uploads/2026/05/woocommerce-server-database-optimization-2026.jpg" '
    'data-width="670" data-height="383" style="aspect-ratio: auto 1400 / 800;max-width:100%;height:auto;">'
    '</span>'
)

# ── FAQ style block — matches reference blog 41576 Thrive toggle CSS exactly ──
# Closed header: rgba(245,245,245,0.5) near-white (tve-u-19d0618d368 .thrv_toggle_title)
# Open header:   #00d5c0 teal (tve-u-19d0618d368 .thrv_toggle_title.tve-state-expanded)
# Question:      16px, #43627f (--tve-font-size:16px on container)
# Dots icon:     #50565f, 17px (tve-toggle-icon-right, icon on RIGHT)
# Answer:        padding 30px 22px, background #fff, text #6e6e6e at 15px
FAQ_STYLE = (
    '<style>'
    'details.vfaq>summary{list-style:none;}'
    'details.vfaq>summary::-webkit-details-marker{display:none;}'
    'details.vfaq[open]>summary{background:linear-gradient(#00d5c0,#00d5c0)!important;}'
    'details.vfaq .vfaq-answer p{font-size:15px!important;color:#6e6e6e!important;line-height:1.75!important;}'
    '</style>'
)

def make_faq_item(question, answer_html):
    # Reference blog 41576: question LEFT, dots icon RIGHT (tve-toggle-icon-right = flex-direction:row-reverse on DOM [icon,question])
    # We achieve same visual with: [question span flex:1] [dots icon] in justify-content:space-between
    return (
        f'<details class="vfaq" style="background:transparent;margin-top:7px;">'
        f'<summary style="cursor:pointer;padding:17px;list-style:none;'
        f'display:flex;align-items:center;justify-content:space-between;gap:12px;'
        f'background:rgba(245,245,245,0.5);">'
        f'<span style="font-size:16px;font-weight:600;color:{HEADING_COLOR};line-height:2;flex:1;">{question}</span>'
        f'{DOTS_SVG}'
        f'</summary>'
        f'<div class="vfaq-answer" style="padding:30px 22px;background:#fff;">'
        f'{answer_html}'
        f'</div>'
        f'</details>'
    )

# ── Load draft ─────────────────────────────────────────────────────────────────
with open(r'C:\content-intel\draft_post.json', 'r', encoding='utf-8') as f:
    draft = json.load(f)
raw_html = draft['content']['raw']

# ── Phase 1: BS4 — table styling ──────────────────────────────────────────────
soup = BeautifulSoup(raw_html, 'html.parser')

for table in soup.find_all('table'):
    all_rows  = table.find_all('tr')
    thead     = table.find('thead')
    tbody     = table.find('tbody')
    hrow      = thead.find('tr') if thead else (all_rows[0] if all_rows else None)
    hcells    = hrow.find_all(['th', 'td']) if hrow else []
    num_cols  = len(hcells)
    body_rows = tbody.find_all('tr') if tbody else all_rows[1:]

    table['data-rows'] = str(len(body_rows))
    table['data-cols'] = str(num_cols)
    table['data-v']    = 'middle'
    table['style']     = 'width:100%;border-collapse:collapse;margin:16px 0;'

    header_texts = []
    for i, th in enumerate(hcells):
        txt = th.get_text(strip=True)
        header_texts.append(txt)
        th['style'] = TABLE_TH_STYLE
        th['data-direction'] = ''
        th.clear()
        p = soup.new_tag('p')
        st = soup.new_tag('strong')
        st.string = txt
        p.append(st)
        th.append(p)
        if i == num_cols - 1:
            th['colspan'] = '1'
            th['rowspan'] = '1'

    for ri, tr in enumerate(body_rows):
        cells = tr.find_all(['td', 'th'])
        td_style = TABLE_TD_EVEN if ri % 2 == 0 else TABLE_TD_ODD
        for ci, td in enumerate(cells):
            txt = td.get_text(strip=True)
            td['style'] = td_style
            if ci < len(header_texts):
                td['data-th'] = header_texts[ci]
            if not td.find('p'):
                td.clear()
                p = soup.new_tag('p')
                p.string = txt
                td.append(p)
            if ci == len(cells) - 1:
                td['colspan'] = '1'
                td['rowspan'] = '1'

html = str(soup)

# ── Phase 2: String transforms ────────────────────────────────────────────────

# 2a-pre. Remove em-dash style ' - ' connectors outside <pre>/<code> blocks
def remove_emdashes(html_text):
    parts = re.split(r'(<(?:pre|code)[^>]*>.*?</(?:pre|code)>)', html_text, flags=re.DOTALL)
    out = []
    for i, part in enumerate(parts):
        if i % 2 == 0:
            part = part.replace(' - ', ', ')
        out.append(part)
    return ''.join(out)

html = remove_emdashes(html)

# 2a. H2 headings
def style_h2(m):
    tag   = m.group(0)
    h2_id = (re.search(r'id="([^"]*)"', tag) or re.search(r"id='([^']*)'", tag))
    h2_id = h2_id.group(1) if h2_id else ''
    color = '#ffffff' if h2_id == 'conclusion' else HEADING_COLOR
    style_val = f'color:{color};font-size:{H2_FONT};'
    if 'style=' in tag:
        tag = re.sub(r'style="[^"]*"', f'style="{style_val}"', tag)
    else:
        tag = tag[:-1] + f' style="{style_val}">'
    return tag

html = re.sub(r'<h2(?:\s[^>]*)?>',  style_h2, html)

# 2b. H3 headings (only those not inside FAQ section — we'll replace FAQ h3 separately)
def style_h3(m):
    tag = m.group(0)
    style_val = f'color:{HEADING_COLOR};font-size:{H3_FONT};'
    if 'style=' in tag:
        tag = re.sub(r'style="[^"]*"', f'style="{style_val}"', tag)
    else:
        tag = tag[:-1] + f' style="{style_val}">'
    return tag

html = re.sub(r'<h3(?:\s[^>]*)?>',  style_h3, html)

# 2c. Font size on ALL paragraphs
def style_p(m):
    tag = m.group(0)
    # Skip if already has font-size
    if 'font-size' in tag:
        return tag
    style_val = 'font-size:16px;line-height:1.75;'
    if 'style=' in tag:
        existing = re.search(r'style="([^"]*)"', tag)
        if existing:
            current = existing.group(1).rstrip(';')
            new_style = (current + ';' + style_val).lstrip(';')
            tag = re.sub(r'style="[^"]*"', f'style="{new_style}"', tag)
    else:
        tag = tag[:-1] + f' style="{style_val}">'
    return tag

html = re.sub(r'<p(?:\s[^>]*)?>',  style_p, html)

# 2d. SVG bullet icons — body bullets only (not TOC links); flex li + explicit 16px span
def add_svg_icons(html_text):
    pattern = re.compile(r'(<li style="">)(<span(?:\s[^>]*)?>)(.*?)(</span></li>)', re.DOTALL)
    def replacer(m):
        inner = m.group(3)
        if re.match(r'\s*<a\s', inner, re.IGNORECASE):
            return m.group(0)
        flex_li = '<li style="display:flex;align-items:flex-start;gap:8px;padding:4px 0;">'
        sized_span = '<span style="font-size:16px;line-height:1.75;">'
        return flex_li + SVG_ICON + sized_span + inner + '</span></li>'
    return pattern.sub(replacer, html_text)

html = add_svg_icons(html)

# 2e. Convert FAQ section H3/P pairs to accordion (must run before style_toc to avoid h3 clash)
# [moved below — see original 2e block]

# 2f. Insert image 1 before TOC <h3 — MUST run before style_toc so image lands OUTSIDE the box
img1_marker = '<h3'
idx = html.find(img1_marker)
if idx > 0:
    html = html[:idx] + IMG1_HTML + '\n' + html[idx:]

# 2g. Insert image 2 at start of Database bottlenecks section (after opening p)
db_section = 'id="database-bottlenecks-hpos-autoload-bloat-and-action-scheduler"'
idx = html.find(db_section)
if idx > 0:
    close_p = html.find('</p>', idx)
    if close_p > 0:
        html = html[:close_p+4] + '\n' + IMG2_HTML + html[close_p+4:]

# 2d2. Style TOC — matches reference blog 41576 exactly:
#   - .tcb-styled-list-icon-text: display:block; line-height:2.3em
#   - .thrv-styled-list-item: display:flex; align-items:flex-start; word-break:break-word
#   - Icon div: padding:10px (from .thrv-styled_list ul li div.thrv_icon)
#   - Arrow icon: 18px, #43627f (tve-u-19a78073f6e: --tve-icon-size:18px)
#   - Link text: font-size:16px (tve-u-19a78073fba), no line-height on <a> (on parent span)
def style_toc(html_text):
    toc_pat = re.compile(
        r'(<h3[^>]*>Table of Contents</h3>\s*)(<ul[^>]*>)(.*?)(</ul>)',
        re.DOTALL
    )
    def toc_replace(m):
        h3 = m.group(1)
        ul_body = m.group(3)
        def li_replace(lim):
            inner = lim.group(1)
            a = re.search(r'href="([^"]*)"[^>]*>(.*?)</a>', inner, re.DOTALL)
            if not a:
                return lim.group(0)
            href = a.group(1)
            text = re.sub(r'<[^>]+>', '', a.group(2)).strip()
            arrow = ('<svg viewBox="0 0 24 24" width="18" height="18" '
                     'style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg">'
                     '<path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg>')
            return (
                f'<li style="display:flex;align-items:flex-start;word-break:break-word;">'
                f'<span style="padding:10px;flex-shrink:0;box-sizing:content-box;">{arrow}</span>'
                f'<span style="display:block;line-height:2.3em;">'
                f'<a href="{href}" style="color:#43627f;text-decoration:none;'
                f'font-size:16px;font-weight:500;">{text}</a>'
                f'</span></li>'
            )
        styled = re.sub(r'<li[^>]*>(.*?)</li>', li_replace, ul_body, flags=re.DOTALL)
        return (h3
                + '<ul style="list-style:none;margin:0;padding:0;">'
                + styled + '</ul>')
    return toc_pat.sub(toc_replace, html_text)

html = style_toc(html)

# 2d3. Remove browser default bullets from remaining body <ul> — SVG icons handle visual bullet
def fix_ul_styles(html_text):
    return re.sub(
        r'<ul>',
        '<ul style="list-style:none;padding-left:4px;margin:8px 0 16px 0;">',
        html_text
    )

html = fix_ul_styles(html)

# 2e. Convert FAQ section H3/P pairs to <details>/<summary> accordion
def convert_faq(html_text):
    # Find FAQ section — from <h2 ... id="faq"> to end of string
    faq_start = re.search(r'<h2[^>]*id="faq"[^>]*>.*?</h2>', html_text, re.DOTALL)
    if not faq_start:
        return html_text

    pre = html_text[:faq_start.end()]
    faq_body = html_text[faq_start.end():]

    # Parse H3 questions + following paragraphs
    # Pattern: <h3 ...>Question?</h3> followed by one or more <p ...>...</p>
    # Also handle inline bold questions: <p ...><strong>Question?</strong></p>
    items = []
    remaining = faq_body

    item_pattern = re.compile(
        r'(<h3[^>]*>(?:\s*)(.*?)(?:\s*)</h3>\s*)((?:<p[^>]*>.*?</p>\s*)+)',
        re.DOTALL
    )
    # Also bold-question pattern
    bold_q_pattern = re.compile(
        r'(<p[^>]*><strong>(.*?)</strong></p>\s*)((?:<p[^>]*>.*?</p>\s*)+)',
        re.DOTALL
    )

    accordion_html = FAQ_STYLE + '\n<div style="margin-top:16px;">\n'

    pos = 0
    for m in item_pattern.finditer(faq_body):
        if m.start() > pos:
            # Check for bold-question in between
            between = faq_body[pos:m.start()]
            bq = bold_q_pattern.search(between)
            if bq:
                q = bq.group(2).strip()
                a = bq.group(3).strip()
                accordion_html += make_faq_item(q, a) + '\n'
        question    = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        answer_html = m.group(3).strip()
        accordion_html += make_faq_item(question, answer_html) + '\n'
        pos = m.end()

    # Any leftover (bold-question style)
    if pos < len(faq_body):
        leftover = faq_body[pos:]
        for bq in bold_q_pattern.finditer(leftover):
            q = bq.group(2).strip()
            a = bq.group(3).strip()
            accordion_html += make_faq_item(q, a) + '\n'

    accordion_html += '</div>'
    return pre + '\n' + accordion_html

html = convert_faq(html)

# ── Phase 3: Wrap sections in gray boxes ──────────────────────────────────────
def wrap_sections(html_text):
    parts = re.split(r'(<h2(?:\s[^>]*)?>.*?</h2>)', html_text, flags=re.DOTALL)
    result = []
    if parts[0].strip():
        result.append(parts[0])
    i = 1
    while i < len(parts):
        h2_tag  = parts[i]     if i   < len(parts) else ''
        content = parts[i+1]  if i+1 < len(parts) else ''
        i += 2
        if not h2_tag:
            break
        id_match  = re.search(r'id="([^"]*)"', h2_tag)
        dir_match = 'dir="ltr"' in h2_tag
        sec_id    = id_match.group(1) if id_match else ''
        if sec_id == 'faq':
            result.append(h2_tag + content)
            continue
        if dir_match and not sec_id:
            box = SECTION_STYLES['__summary__']
        elif not sec_id:
            box = SECTION_STYLES['__intro__']
        else:
            box = SECTION_STYLES.get(sec_id, BLUE_BOX)
        result.append(f'<div style="{box}">{h2_tag}{content}</div>')
    return '\n'.join(result)

html = wrap_sections(html)

# ── Phase 4: White text in conclusion box ─────────────────────────────────────
def fix_conclusion_text(html_text):
    def replacer(m):
        inner = m.group(0)
        inner = re.sub(r'style="([^"]*)"(?=[^>]*>)',
                       lambda s: f'style="{s.group(1).rstrip(";")};color:#ffffff;"',
                       inner)
        return inner
    # Only target <p style inside the conclusion div
    def fix_div(m):
        div = m.group(0)
        div = re.sub(r'(<p)(\s+style="[^"]*")',
                     r'\1 style="color:#ffffff;font-size:16px;line-height:1.75;"', div)
        return div
    return re.sub(
        r'<div style="background:#00d5c0[^"]*">.*?</div>',
        fix_div, html_text, flags=re.DOTALL
    )

html = fix_conclusion_text(html)

# ── Output ─────────────────────────────────────────────────────────────────────
output_path = r'C:\content-intel\clients\virtina\output\research\post42074_styled_content.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Written: {output_path}  ({len(html):,} chars)')
print(f'Summary teal    : {html.count("rgba(0,213,192")}')
print(f'Conclusion teal : {html.count("#00d5c0")}')
print(f'Blue boxes      : {html.count("rgba(0,160,226")}')
print(f'Gray boxes      : {html.count("rgba(230,230,230")}')
print(f'H2 color        : {html.count("#43627f")}')
print(f'SVG bullets     : {html.count("<svg viewBox=\"0 0 512 512\"")}')
print(f'FAQ accordions  : {html.count("<details class=\"vfaq\"")}')
print(f'Images          : {html.count("<img ")}')
print(f'Styled tables   : {html.count("data-rows=")}')
print(f'White text refs : {html.count("color:#ffffff")}')
