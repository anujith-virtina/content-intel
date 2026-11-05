# -*- coding: utf-8 -*-
"""Build the styled Virtina HTML for 'B2B store rebuild or AI chatbot' from the creator's markdown draft.
Output: clients/virtina/output/drafts/b2b-store-rebuild-or-ai-chatbot-2026-11-03.html
Templates follow clients/virtina/reference/html-templates.md. Body images use PENDING-bodyN placeholders."""
import os, re, html as H, json

ROOT = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(ROOT, '..', '..', '..', '..'))
SRC = os.path.join(PROJ, 'clients/virtina/output/drafts/b2b-store-rebuild-or-ai-chatbot-2026-11-03.md')
OUT = os.path.join(PROJ, 'clients/virtina/output/drafts/b2b-store-rebuild-or-ai-chatbot-2026-11-03.html')

ALTS = json.load(open(os.path.join(ROOT, 'b2b_rebuild_chatbot_alts.json')))

raw = open(SRC, encoding='utf-8').read()
body = raw.split('\n---\n', 1)[1] if raw.startswith('---') else raw
body = body.split('QA BLOCK (not for publication)')[0].rstrip().rstrip('-').rstrip()
lines = body.split('\n')

P = 'font-size:16px;line-height:1.75;'
BOX_BLUE = 'linear-gradient(rgba(0,160,226,0.13),rgba(0,160,226,0.13))'
BOX_GREY = 'linear-gradient(rgba(241,243,250,0.5),rgba(241,243,250,0.5))'
BOX_TEAL = 'linear-gradient(rgba(0,213,192,0.28),rgba(0,213,192,0.28))'
ARROW = '<svg viewBox="0 0 24 24" width="18" height="18" style="fill:#43627f;" xmlns="http://www.w3.org/2000/svg"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg>'
FAQ_ICON = '<svg viewBox="0 0 24 24" width="17" height="17" style="fill:#50565f;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg"><path d="M16,12A2,2 0 0,1 18,10A2,2 0 0,1 20,12A2,2 0 0,1 18,14A2,2 0 0,1 16,12M8,12A2,2 0 0,1 10,10A2,2 0 0,1 12,12A2,2 0 0,1 10,14A2,2 0 0,1 8,12M0,12A2,2 0 0,1 2,10A2,2 0 0,1 4,12A2,2 0 0,1 2,14A2,2 0 0,1 0,12Z"/></svg>'


def slug(s):
    s = re.sub(r'[^a-z0-9 ]', '', s.lower()); return re.sub(r'\s+', '-', s.strip())[:48].strip('-')


def inline(t, white=False):
    t = H.escape(t, quote=False)
    # internal link marker (already escaped brackets stay as text)
    def internal(m):
        anchor, purpose = m.group(1), m.group(2).strip()
        url = purpose.replace('purpose:', '').strip()
        return '<a href="https://virtina.com%s" style="outline: none;">%s</a>' % (url, anchor)
    t = re.sub(r'\[INTERNAL LINK: (.*?) \| purpose: (.*?)\]', internal, t)
    def external(m):
        anchor, url = m.group(1), m.group(2).strip()
        st = ' style="color:#ffffff;text-decoration:underline;"' if white else ''
        return '<a href="%s" target="_blank" rel="noopener noreferrer"%s>%s</a>' % (url, st, anchor)
    t = re.sub(r'\[EXTERNAL LINK: (.*?) \| url: (\S+) \| target=_blank rel=&quot;noopener noreferrer&quot;\]', external, t)
    t = re.sub(r'\[EXTERNAL LINK: (.*?) \| url: (\S+) \| target=_blank rel="noopener noreferrer"\]', external, t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    return t


def para(t, white=False):
    c = 'color:#ffffff;' if white else ''
    d = '' if white else ' dir="ltr"'
    return '<p%s style="%s%s">%s</p>' % (d, c, P, inline(t, white))


def bullets(items):
    out = ['<ul style="list-style:none;padding-left:4px;margin:8px 0 16px 0;">']
    for it in items:
        m = re.match(r'\*\*(.+?)\*\*:?\s*(.*)', it)
        if m:
            lab, rest = m.group(1).rstrip('.:'), m.group(2)
            txt = '<strong>%s.</strong> %s' % (H.escape(lab), inline(rest))
        else:
            txt = inline(it)
        out.append('<li style="display:flex;align-items:flex-start;gap:10px;padding:6px 0;"><span style="flex-shrink:0;margin-top:6px;width:9px;height:9px;background-color:#43627f;border-radius:50%;display:inline-block;"></span><span style="font-size:16px;line-height:1.75;color:#2d3e50;">' + txt + '</span></li>')
    out.append('</ul>')
    return '\n'.join(out)


def table(rows):
    hdr = [c.strip() for c in rows[0].strip('|').split('|')]
    data = [[c.strip() for c in r.strip('|').split('|')] for r in rows[2:]]
    o = ['<table data-rows="%d" data-cols="%d" data-v="middle" style="width:100%%;border-collapse:collapse;margin:16px 0;">' % (len(data) + 1, len(hdr)), '<thead>', '<tr>']
    for h in hdr:
        o.append('<th data-direction="" style="background:#43627f;color:#ffffff;padding:10px 14px;text-align:left;font-weight:600;"><p style="%s"><strong>%s</strong></p></th>' % (P, inline(h)))
    o += ['</tr>', '</thead>', '<tbody>']
    for i, r in enumerate(data):
        bg = '#f4f6f9' if i % 2 == 0 else '#ffffff'
        o.append('<tr>')
        for h, c in zip(hdr, r):
            cell = inline(c)
            if c == r[0]:
                cell = '<strong>%s</strong>' % cell
            o.append('<td data-th="%s" style="background:%s;padding:10px 14px;border-bottom:1px solid #dde0e6;vertical-align:top;"><p style="%s">%s</p></td>' % (H.escape(h), bg, P, cell))
        o.append('</tr>')
    o += ['</tbody>', '</table>',
          '<p dir="ltr" style="font-size:14px;line-height:1.6;color:#6e6e6e;margin:4px 0 16px 0;">Qualitative comparison for a B2B store with a product catalog. No figures are implied.</p>']
    return '\n'.join(o)


# ---- parse into blocks ----
blocks = []  # (kind, payload)
i = 0
cur = None
while i < len(lines):
    ln = lines[i].rstrip()
    i += 1
    if not ln.strip():
        continue
    m = re.match(r'\[(H2|H3): (.*)\]$', ln)
    if m:
        blocks.append((m.group(1), m.group(2))); continue
    if ln.startswith('[FEATURED IMAGE'):
        continue
    if ln.startswith('[SUMMARY]'):
        blocks.append(('SUMMARY', None)); continue
    if ln.startswith('[INTRODUCTION]'):
        blocks.append(('INTRO', None)); continue
    if ln.startswith('[TOC'):
        blocks.append(('TOC', None)); continue
    if ln.startswith('[BODY IMAGE'):
        blocks.append(('IMG', None)); continue
    if ln.startswith('[TABLE'):
        tb = []
        while i < len(lines) and (not lines[i].strip() or lines[i].lstrip().startswith('|')):
            if lines[i].strip():
                tb.append(lines[i].strip())
            i += 1
        blocks.append(('TABLE', tb)); continue
    if ln.startswith('[CTA button') or ln.startswith('[AUTHOR BIO'):
        blocks.append(('BIO' if ln.startswith('[AUTHOR') else 'SKIP', None)); continue
    if ln.lstrip().startswith('- '):
        items = [ln.lstrip()[2:]]
        while i < len(lines) and lines[i].lstrip().startswith('- '):
            items.append(lines[i].lstrip()[2:]); i += 1
        blocks.append(('UL', items)); continue
    if ln.startswith('**') and ln.endswith('**') and i < len(lines) and lines[i].strip() and not lines[i].startswith('['):
        # FAQ question line followed by answer line
        blocks.append(('FAQQ', (ln.strip('*'), lines[i].strip()))); i += 1; continue
    blocks.append(('P', ln))

h2s = [(b[1], 'faq' if b[1].lower().startswith('frequently asked') else slug(b[1])) for b in blocks if b[0] == 'H2']
ids = {t: s for t, s in h2s}
ids['Frequently asked questions'] = 'faq'

out = []
sec_open = None  # 'box' | 'conc' | 'sum' | 'intro' | 'faq'
img_n = 0
pending_img = False


def close():
    global sec_open
    if sec_open in ('box', 'conc', 'sum', 'intro'):
        out.append('</div>')
    if sec_open == 'faq':
        out.append('</div>')
    sec_open = None


for kind, pl in blocks:
    if kind == 'SUMMARY':
        close(); out.append('<div style="background:%s;border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 id="summary" dir="ltr" style="color:#43627f;font-size:30px;">Summary</h2>' % BOX_TEAL); sec_open = 'sum'
    elif kind == 'INTRO':
        close(); out.append('<div style="background:%s;border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 id="introduction" style="color:#43627f;font-size:30px;">Introduction</h2>' % BOX_GREY); sec_open = 'intro'
    elif kind == 'TOC':
        close()
        out.append('<h3 style="color:#43627f;font-size:22px;">Table of Contents</h3>')
        out.append('<ul style="list-style:none!important;padding-left:0!important;margin:0 0 1.5em 0!important;">')
        for t, s in h2s:
            out.append('<li style="list-style:none!important;padding:8px 0 8px 32px!important;position:relative!important;line-height:1.5!important;margin:0!important;"><span aria-hidden="true" style="position:absolute!important;left:0!important;top:8px!important;">%s</span><a href="#%s" style="color:#00a0e2!important;text-decoration:none!important;font-family:metropolis,arial!important;font-size:16px!important;font-weight:500!important;">%s</a></li>' % (ARROW, s, H.escape(t)))
        out.append('</ul>')
    elif kind == 'H2':
        close()
        s = ids[pl]
        if pl == 'Conclusion':
            out.append('<div style="background:#00d5c0;border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 id="conclusion" style="color:#ffffff;font-size:30px;">Conclusion</h2>'); sec_open = 'conc'
        elif pl.lower().startswith('frequently asked'):
            out.append('<h2 id="faq" style="color:#43627f;font-size:30px;">Frequently asked questions</h2>\n<div>'); sec_open = 'faq'
        else:
            bg = BOX_GREY if pl == 'People Also Ask' else BOX_BLUE
            sid = 'people-also-ask' if pl == 'People Also Ask' else s
            out.append('<div style="background:%s;border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 id="%s" style="color:#43627f;font-size:30px;">%s</h2>' % (bg, sid, H.escape(pl if pl != 'People Also Ask' else 'People also ask'))); sec_open = 'box'
    elif kind == 'H3':
        out.append('<h3 style="color:#43627f;font-size:22px;">%s</h3>' % H.escape(pl))
    elif kind == 'P':
        out.append(para(pl, white=(sec_open == 'conc')))
    elif kind == 'UL':
        out.append(bullets(pl))
    elif kind == 'TABLE':
        out.append(table(pl))
    elif kind == 'IMG':
        img_n += 1
        out.append('<span style="display:block;margin:20px 0;"><img alt="%s" data-id="PENDING" width="670" data-init-width="670" height="352" data-init-height="352" title="" loading="lazy" src="https://virtina.com/wp-content/uploads/PENDING-body%d.jpg" data-width="670" data-height="352" style="aspect-ratio: auto 670 / 352;max-width:100%%;"></span>' % (H.escape(ALTS['body%d' % img_n]), img_n))
    elif kind == 'FAQQ':
        q, a = pl
        out.append('<details class="vfaq" style="background:transparent;margin-top:7px;"><summary style="cursor:pointer;padding:17px;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:12px;background:rgba(245,245,245,0.5);"><span style="font-size:16px;font-weight:600;color:#43627f;line-height:2;flex:1;">%s</span>%s</summary><div class="vfaq-answer" style="padding:30px 22px;background:#fff;"><p dir="ltr" style="%s">%s</p></div></details>' % (H.escape(q), FAQ_ICON, P, inline(a)))
    elif kind == 'BIO':
        close()
        out.append('<p dir="ltr" style="%s"><strong>Virtina</strong> is an eCommerce web design and development company. It builds, redesigns, migrates and supports online stores on WooCommerce, Magento, Shopify, BigCommerce and other platforms. Its engineers lead the work, with a free initial review before any plan or price.</p>' % P)
close()
html_out = '\n'.join(out) + '\n'
open(OUT, 'w', encoding='utf-8').write(html_out)
print('wrote', OUT, len(html_out), 'chars; images', img_n, 'h2', len(h2s))
