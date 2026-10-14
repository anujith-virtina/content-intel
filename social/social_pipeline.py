"""Blog post -> LinkedIn + Instagram pipeline.

  fetch   <post_id>   pull the article from WordPress, write the source file the copywriter reads
  render  <pack.json> draw the 1080x1350 carousel slides + a contact sheet + a readable .md preview
  preview <pack.json> one HTML page showing the post as it sits in a LinkedIn and an Instagram feed
  qa      <pack.json> blocking copy gates (voice, lengths, hashtags, numbers traceable to the article)
  approve <pack.json> mark a pack as cleared to post
  publish <pack.json> post to LinkedIn and Instagram (--dry-run prints the plan, sends nothing)
  sweep               publish every pack whose article has gone live and that has not been posted yet
  check               show which credentials are present

Per-client settings live in clients/{client}/social.json. Secrets live in .env.
"""
import argparse
import base64
import glob
import html
import json
import os
import re
import sys
import time
import urllib.parse

import requests
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
W = H = 1080


def load_env():
    env = {}
    for line in open(os.path.join(PROJ, '.env'), encoding='utf-8'):
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip().strip('"')
    return env


def load_cfg(client):
    with open(os.path.join(PROJ, 'clients', client, 'social.json'), encoding='utf-8') as f:
        return json.load(f)


def social_dir(client):
    return os.path.join(PROJ, 'clients', client, 'output', 'social')


def read_pack(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def write_pack(path, pack):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(pack, f, indent=2, ensure_ascii=False)


def wp_auth(cfg, env):
    raw = '%s:%s' % (env[cfg['wp']['username_env']], env[cfg['wp']['password_env']])
    return {'Authorization': 'Basic ' + base64.b64encode(raw.encode()).decode(), 'User-Agent': UA}


def wp_post(cfg, env, post_id):
    r = requests.get('%s/wp-json/wp/v2/posts/%s?context=edit' % (cfg['wp']['site'], post_id),
                     headers=wp_auth(cfg, env), timeout=60)
    r.raise_for_status()
    return r.json()


def to_text(markup):
    markup = re.sub(r'<(style|script)\b.*?</\1>', ' ', markup, flags=re.S | re.I)
    markup = re.sub(r'<!--.*?-->', ' ', markup, flags=re.S)
    markup = re.sub(r'</(p|li|h[1-6]|tr|div|summary|details)>', '\n', markup, flags=re.I)
    return re.sub(r'[ \t]+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', markup))).strip()


# ---------------------------------------------------------------- fetch

def cmd_fetch(a):
    cfg, env = load_cfg(a.client), load_env()
    p = wp_post(cfg, env, a.post_id)
    body = p['content'].get('raw') or p['content']['rendered']
    headings = [to_text(h) for h in re.findall(r'<h[23][^>]*>.*?</h[23]>', body, flags=re.S | re.I)]
    src = {
        'wp_post_id': p['id'], 'status': p['status'], 'slug': p['slug'], 'canonical_url': p['link'],
        'title': to_text(p['title'].get('raw') or p['title']['rendered']),
        'headings': headings, 'text': to_text(body),
    }
    out = os.path.join(social_dir(a.client), '_source')
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, '%s.json' % p['id'])
    write_pack(path, src)
    print('source: %s\nstatus: %s\nurl:    %s\nwords:  %d' % (path, p['status'], p['link'], len(src['text'].split())))


# ---------------------------------------------------------------- render

def font(cfg, weight, size):
    return ImageFont.truetype(os.path.join(HERE, 'fonts', cfg['fonts'][weight]), size)


def wrap(draw, text, fnt, width):
    lines, cur = [], ''
    for word in text.split():
        trial = (cur + ' ' + word).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    return lines + [cur] if cur else lines


def fit(draw, cfg, text, weight, sizes, width, max_lines):
    """Largest size at which the text wraps into max_lines with no word wider than the column."""
    for size in sizes:
        fnt = font(cfg, weight, size)
        lines = wrap(draw, text, fnt, width)
        if len(lines) <= max_lines and all(draw.textlength(l, font=fnt) <= width for l in lines):
            return fnt, lines
    raise ValueError('text does not fit on the slide, shorten it: %r' % text)


def centered(draw, y, text, fnt, fill, shadow=None):
    if shadow:
        draw.text((W / 2, y + 5), text, font=fnt, fill=shadow, anchor='ma')
    draw.text((W / 2, y), text, font=fnt, fill=fill, anchor='ma')
    return y + int(fnt.size * 1.16)


def background(cfg):
    c = cfg['colors']
    top, bot = Image.new('RGB', (W, H), c['bg_top']), Image.new('RGB', (W, H), c['bg_bottom'])
    img = Image.composite(bot, top, Image.linear_gradient('L').resize((W, H)))
    if c.get('glow'):
        box = [-120, -520, W + 120, 520] if c.get('glow_at', 'top') == 'top' else [120, 200, W - 120, H - 200]
        glow = Image.new('L', (W, H), 0)
        ImageDraw.Draw(glow).ellipse(box, fill=150)
        img.paste(Image.new('RGB', (W, H), c['glow']), mask=glow.filter(ImageFilter.GaussianBlur(90 if box[0] > 0 else 40)))
    return img


def brand_logo(cfg, width):
    logo = Image.open(os.path.join(HERE, cfg['logo'])).convert('RGBA')
    logo = logo.crop(logo.getbbox())
    logo = logo.resize((width, round(logo.height * width / logo.width)), Image.LANCZOS)
    if cfg.get('logo_white'):
        white = Image.new('RGBA', logo.size, '#ffffff')
        white.putalpha(logo.getchannel('A'))
        return white
    return logo


def lockup(img, d, cfg):
    """Logo (and site address, if the brand uses one) centred at the bottom of every slide."""
    logo = brand_logo(cfg, cfg.get('logo_width', 290))
    label = cfg.get('site_label')
    y = (944 if label else 1000 - logo.height // 2)
    img.paste(logo, ((W - logo.width) // 2, y), logo)
    if label:
        d.text((W / 2, y + logo.height + 6), label, font=font(cfg, 'medium', 24), fill=cfg['colors']['headline'], anchor='ma')


def card_box(d, c, x, y, w, h):
    if c.get('card_shadow'):
        d.rounded_rectangle([x, y + 8, x + w, y + h + 8], radius=24, fill=c['card_shadow'])
    d.rounded_rectangle([x, y, x + w, y + h], radius=24, fill=c['card'], outline=c.get('card_outline'), width=3)


def badge(d, cfg, cx, cy, r, text, size):
    c = cfg['colors']
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c['badge'], outline=c.get('badge_outline'), width=3)
    d.text((cx, cy), text, font=font(cfg, 'extrabold', size), fill=c.get('badge_text', '#ffffff'), anchor='mm')


def draw_poster(cfg, slide, scene=None):
    """House poster: two-tone headline, numbered callout cards, logo lockup."""
    c = cfg['colors']
    img = background(cfg)
    d = ImageDraw.Draw(img)
    col = W - 120

    f, lines = fit(d, cfg, slide['headline_top'], 'extrabold', range(60, 39, -2), col, 1)
    y = centered(d, 58, lines[0], f, c['headline'], c.get('text_shadow'))
    f, lines = fit(d, cfg, slide['headline_main'], 'extrabold', range(104, 59, -4), col, 1)
    y = centered(d, y - 6, lines[0], f, c['accent'], c.get('text_shadow'))
    f, lines = fit(d, cfg, slide['sub'], 'medium', range(34, 25, -2), col, 1)
    y = centered(d, y + 8, lines[0], f, c.get('sub', c['headline']))

    top, bottom = y + 26, 922
    if scene:
        art = Image.open(scene).convert('RGBA')
        k = max(W / art.width, (bottom - top) / art.height)
        art = art.resize((round(art.width * k), round(art.height * k)), Image.LANCZOS)
        img.paste(art, ((W - art.width) // 2, top + (bottom - top - art.height) // 2), art)

    cards = slide['cards']
    ch, gap, cw = 100, 18, 880
    x = (W - cw) // 2
    y = top + (bottom - top - (len(cards) * ch + (len(cards) - 1) * gap)) // 2
    f_lab, f_det = font(cfg, 'semibold', 32), font(cfg, 'regular', 25)
    for i, card in enumerate(cards, 1):
        for text, fnt in ((card['label'], f_lab), (card['detail'], f_det)):
            if d.textlength(text, font=fnt) > cw - 136:
                raise ValueError('text does not fit on the card, shorten it: %r' % text)
        card_box(d, c, x, y, cw, ch)
        badge(d, cfg, x + 54, y + 50, 32, str(i), 34)
        d.text((x + 112, y + 12), card['label'], font=f_lab, fill=c['card_title'])
        d.text((x + 112, y + 56), card['detail'], font=f_det, fill=c['card_text'])
        y += ch + gap
    lockup(img, d, cfg)
    return img


def draw_point(cfg, slide, number, total):
    """Carousel follow-on slide: one numbered point in the same frame as the poster."""
    c = cfg['colors']
    img = background(cfg)
    d = ImageDraw.Draw(img)
    col = W - 200
    badge(d, cfg, W // 2, 190, 78, str(number), 84)
    f, lines = fit(d, cfg, slide['headline'], 'extrabold', range(76, 51, -4), col, 3)
    y = 310
    for line in lines:
        y = centered(d, y, line, f, c['accent'], c.get('text_shadow'))
    f, lines = fit(d, cfg, slide['body'], 'medium', range(42, 31, -2), col, 7)
    y += 30
    for line in lines:
        y = centered(d, y, line, f, c['headline']) + 8
    d.text((W - 60, 60), '%d / %d' % (number + 1, total), font=font(cfg, 'semibold', 26), fill=c.get('sub', c['headline']), anchor='ra')
    lockup(img, d, cfg)
    return img


# ---- story slides: product-screen mockups instead of one repeated poster

UI = {'screen': '#ffffff', 'bar': '#eef2f7', 'ink': '#1d2a3f', 'muted': '#6b7a90', 'buyer': '#e4ebf5',
      'general': '#f1f2f4', 'bad': '#e94560', 'good': '#16a594', 'field': '#f4f7fb', 'line': '#d5dde8'}


def story_head(img, d, cfg, slide, number, total, y=64):
    """White headline (1-2 lines) + optional amber accent line + page counter."""
    c = cfg['colors']
    if number:
        d.text((W - 56, 40), '%d / %d' % (number, total), font=font(cfg, 'semibold', 26), fill=c.get('sub', c['headline']), anchor='ra')
    try:
        f, lines = fit(d, cfg, slide['headline'], 'extrabold', range(62, 49, -2), W - (220 if number else 120), 1)
    except ValueError:
        f, lines = fit(d, cfg, slide['headline'], 'extrabold', range(62, 41, -2), W - 220, 2)
    for line in lines:
        y = centered(d, y, line, f, c['headline'])
    if slide.get('accent'):
        f, lines = fit(d, cfg, slide['accent'], 'extrabold', range(66, 43, -2), W - 140, 1)
        y = centered(d, y, lines[0], f, c['accent'])
    return y


def mark(d, cx, cy, r, good):
    """Drawn check or cross in a filled circle (no emoji on images)."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=UI['good'] if good else UI['bad'])
    k = r * 0.45
    if good:
        d.line([(cx - k, cy + 1), (cx - k * 0.2, cy + k * 0.8), (cx + k, cy - k * 0.7)], fill='#ffffff', width=max(3, r // 5), joint='curve')
    else:
        d.line([(cx - k, cy - k), (cx + k, cy + k)], fill='#ffffff', width=max(3, r // 5))
        d.line([(cx - k, cy + k), (cx + k, cy - k)], fill='#ffffff', width=max(3, r // 5))


def draw_chat(cfg, slide, number, total):
    """A chat window on a light screen: buyer bubble right, assistant answers left."""
    c = cfg['colors']
    img = background(cfg)
    d = ImageDraw.Draw(img)
    y = story_head(img, d, cfg, slide, number, total)
    x0, x1, limit = 80, W - 80, 912
    big = len(slide['messages']) == 1
    # measure on a scratch canvas, then size the window to its content and centre it
    content = chat_body(ImageDraw.Draw(Image.new('RGB', (W, H))), cfg, slide, x0, x1, 0, big) + 30
    room = limit - (y + 30)
    if content > room:
        raise ValueError('chat does not fit on the slide (%d px over), shorten: %r' % (content - room, slide['headline']))
    top = y + 30 + (room - content) // 2
    bottom = top + content
    d.rounded_rectangle([x0 + 8, top + 14, x1 + 8, bottom + 14], radius=34, fill='#030a17')
    d.rounded_rectangle([x0, top, x1, bottom], radius=34, fill=UI['screen'])
    d.rounded_rectangle([x0, top, x1, top + 64], radius=34, fill=UI['bar'])
    d.rectangle([x0, top + 34, x1, top + 64], fill=UI['bar'])
    for i, col in enumerate(('#ff6159', '#ffbd2e', '#28c941')):
        d.ellipse([x0 + 30 + i * 30, top + 24, x0 + 46 + i * 30, top + 40], fill=col)
    d.text((W / 2, top + 32), slide.get('screen', 'Product questions'), font=font(cfg, 'semibold', 24), fill=UI['muted'], anchor='mm')
    chat_body(d, cfg, slide, x0, x1, top, big)
    lockup(img, d, cfg)
    return img


def chat_body(d, cfg, slide, x0, x1, top, big):
    """Draws the bubbles from top; returns the content height."""
    c = cfg['colors']
    f_msg, f_who, f_tag = font(cfg, 'regular', 34 if big else 27), font(cfg, 'semibold', 22), font(cfg, 'semibold', 21)
    bw, pad, yy, lh = int((x1 - x0) * 0.8), 22 if big else 20, top + 90, 46 if big else 37
    for m in slide['messages']:
        lines = wrap(d, m['text'], f_msg, bw - 2 * pad)
        h = len(lines) * lh + 2 * pad - 4
        if m['who'] == 'buyer':
            bx = x1 - 36 - min(bw, max(d.textlength(l, font=f_msg) for l in lines) + 2 * pad)
            fill, ink = UI['buyer'], UI['ink']
        else:
            who = 'Catalog assistant' if m['who'] == 'catalog' else 'General assistant'
            d.text((x0 + 40, yy), who, font=f_who, fill=UI['good'] if m['who'] == 'catalog' else UI['muted'])
            yy += 34
            bx = x0 + 36
            fill, ink = (c['bg_top'], '#ffffff') if m['who'] == 'catalog' else (UI['general'], UI['ink'])
        bwid = min(bw, max(d.textlength(l, font=f_msg) for l in lines) + 2 * pad)
        d.rounded_rectangle([bx, yy, bx + bwid, yy + h], radius=24, fill=fill)
        for i, l in enumerate(lines):
            d.text((bx + pad, yy + pad - 4 + i * lh), l, font=f_msg, fill=ink)
        yy += h + 14
        if m.get('tag'):
            good = m['who'] == 'catalog'
            tw = d.textlength(m['tag'], font=f_tag)
            mark(d, bx + 16, yy + 16, 15, good)
            d.text((bx + 40, yy + 16), m['tag'], font=f_tag, fill=UI['good'] if good else UI['bad'], anchor='lm')
            yy += 44
        yy += 18
    if slide.get('typing'):
        for who, col, fill, dot in (('General assistant', UI['muted'], UI['general'], '#9aa6b8'),
                                    ('Catalog assistant', UI['good'], c['bg_top'], '#4eddcc')):
            d.text((x0 + 40, yy), who + ' is typing', font=f_who, fill=col)
            d.rounded_rectangle([x0 + 36, yy + 32, x0 + 156, yy + 92], radius=24, fill=fill)
            for i in range(3):
                d.ellipse([x0 + 62 + i * 26, yy + 54, x0 + 78 + i * 26, yy + 70], fill=dot)
            yy += 116
    return yy - top


def draw_split(cfg, slide, number, total):
    """Two panels side by side, e.g. the same part at two prices."""
    c = cfg['colors']
    img = background(cfg)
    d = ImageDraw.Draw(img)
    y = story_head(img, d, cfg, slide, number, total)
    top, bottom, gap = y + 40, (720 if slide.get('footer') else 900), 30
    pw = (W - 120 - gap) // 2
    light = is_light(c['card'])
    for i, side in enumerate((slide['left'], slide['right'])):
        x = 60 + i * (pw + gap)
        hi = i == 1
        if light:  # white-card brands: muted dark panel on the left, the brand card on the right
            fill, outline, ink, rule = (c['card'], None, c['card_title'], '#e3e8f2') if hi else (c['bg_bottom'], '#ffffff', c['headline'], '#3b5bc4')
            big_ink, txt = (c.get('badge', c['card_title']) if hi else c['headline']), (c['card_text'] if hi else c['headline'])
        else:
            fill, outline, ink, rule = c['card'], (c['card_outline'] if hi else '#3a4d6e'), c['headline'], '#2a3d60'
            big_ink, txt = (c['accent'] if hi else c['headline']), c.get('sub', c['headline'])
        if light and hi and c.get('card_shadow'):
            d.rounded_rectangle([x, top + 10, x + pw, bottom + 10], radius=30, fill=c['card_shadow'])
        d.rounded_rectangle([x, top, x + pw, bottom], radius=30, fill=fill, outline=outline, width=4 if hi else 3)
        d.text((x + pw / 2, top + 54), side['title'], font=font(cfg, 'semibold', 34), fill=ink, anchor='mm')
        d.line([(x + 40, top + 100), (x + pw - 40, top + 100)], fill=rule, width=2)
        mid = (top + 100 + bottom) / 2
        if side.get('big'):
            f, _ = fit(d, cfg, side['big'], 'extrabold', range(130, 59, -6), pw - 60, 1)
            d.text((x + pw / 2, mid - (40 if side.get('text') else 0)), side['big'], font=f, fill=big_ink, anchor='mm')
        if side.get('text'):
            f, lines = fit(d, cfg, side['text'], 'medium', range(30, 23, -1), pw - 70, 4)
            ty = mid + (40 if side.get('big') else -len(lines) * 20)
            for l in lines:
                d.text((x + pw / 2, ty), l, font=f, fill=txt, anchor='ma')
                ty += int(f.size * 1.3)
    if slide.get('footer'):
        f, lines = fit(d, cfg, slide['footer'], 'medium', range(32, 25, -1), W - 160, 2)
        fy = bottom + 36
        for l in lines:
            fy = centered(d, fy, l, f, c['headline']) + 4
    lockup(img, d, cfg)
    return img


def draw_form(cfg, slide, number, total):
    """A filled-in request-for-quote card with a sent confirmation."""
    c = cfg['colors']
    img = background(cfg)
    d = ImageDraw.Draw(img)
    y = story_head(img, d, cfg, slide, number, total)
    x0, x1, top = 150, W - 150, y + 34
    fields = slide['fields']
    step = 92 if cfg.get('site_label') else 104
    bottom = top + 100 + len(fields) * step + 96
    d.rounded_rectangle([x0 + 8, top + 14, x1 + 8, bottom + 14], radius=30, fill='#030a17')
    d.rounded_rectangle([x0, top, x1, bottom], radius=30, fill=UI['screen'])
    d.text((x0 + 40, top + 34), slide['title'], font=font(cfg, 'extrabold', 34), fill=UI['ink'])
    fy = top + 100
    f_lab, f_val = font(cfg, 'semibold', 21), font(cfg, 'medium', 27)
    for fld in fields:
        if d.textlength(fld['value'], font=f_val) > x1 - x0 - 110:
            raise ValueError('form value does not fit, shorten it: %r' % fld['value'])
        d.text((x0 + 40, fy), fld['label'].upper(), font=f_lab, fill=UI['muted'])
        d.rounded_rectangle([x0 + 40, fy + 30, x1 - 40, fy + 86], radius=12, fill=UI['field'], outline=UI['line'], width=2)
        d.text((x0 + 60, fy + 58), fld['value'], font=f_val, fill=UI['ink'], anchor='lm')
        fy += step
    d.rounded_rectangle([x0 + 40, fy + 4, x1 - 40, fy + 66], radius=14, fill=UI['bad'])
    d.text((W / 2, fy + 35), slide['button'], font=font(cfg, 'semibold', 28), fill='#ffffff', anchor='mm')
    if slide.get('note'):
        f = font(cfg, 'semibold', 30)
        tw = d.textlength(slide['note'], font=f)
        ny = bottom + 54
        mark(d, (W - tw) / 2 - 10, ny, 20, True)
        d.text(((W - tw) / 2 + 22, ny), slide['note'], font=f, fill=c.get('card_outline') or c['headline'], anchor='lm')
    lockup(img, d, cfg)
    return img


def draw_statement(cfg, slide, number, total):
    """Typographic closer: kicker, two big lines, a muted sub line."""
    c = cfg['colors']
    img = background(cfg)
    d = ImageDraw.Draw(img)
    if number:
        d.text((W - 56, 40), '%d / %d' % (number, total), font=font(cfg, 'semibold', 26), fill=c.get('sub', c['headline']), anchor='ra')
    # two outlined speech bubbles as a quiet motif
    for bx, by, s, col in ((96, 170, 1.0, '#2a3d60'), (W - 300, 230, 0.8, c.get('card_outline', c['accent']))):
        w, h = 200 * s, 120 * s
        d.rounded_rectangle([bx, by, bx + w, by + h], radius=int(34 * s), outline=col, width=4)
        d.polygon([(bx + 40 * s, by + h - 2), (bx + 40 * s, by + h + 34 * s), (bx + 80 * s, by + h - 2)], fill=col)
    y = 330
    f = font(cfg, 'semibold', 36)
    y = centered(d, y, slide['kicker'], f, c.get('card_outline', c['accent'])) + 20
    for key, col in (('line1', c['headline']), ('line2', c['accent'])):
        try:
            fnt, lines = fit(d, cfg, slide[key], 'extrabold', range(76, 47, -2), W - 110, 1)
        except ValueError:
            fnt, lines = fit(d, cfg, slide[key], 'extrabold', range(76, 47, -2), W - 120, 2)
        for l in lines:
            y = centered(d, y, l, fnt, col)
    if slide.get('sub'):
        try:
            fnt, lines = fit(d, cfg, slide['sub'], 'medium', range(34, 25, -1), W - 140, 1)
        except ValueError:
            fnt, lines = fit(d, cfg, slide['sub'], 'medium', range(34, 25, -1), W - 200, 2)
        y += 30
        for l in lines:
            y = centered(d, y, l, fnt, c.get('sub', c['headline'])) + 4
    lockup(img, d, cfg)
    return img


def is_light(hex_color):
    r, g, b = (int(hex_color.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
    return r * 0.299 + g * 0.587 + b * 0.114 > 160


def draw_search(cfg, slide, number, total):
    """A search results page: query bar, then results each with a verdict tag."""
    img = background(cfg)
    d = ImageDraw.Draw(img)
    y = story_head(img, d, cfg, slide, number, total)
    x0, x1 = 80, W - 80
    f_q, f_site, f_title, f_snip, f_tag = (font(cfg, 'medium', 28), font(cfg, 'regular', 21), font(cfg, 'semibold', 29),
                                           font(cfg, 'regular', 23), font(cfg, 'semibold', 22))
    tw = x1 - x0 - 90

    def body(dd, top):
        yy = top + 34
        dd.rounded_rectangle([x0 + 40, yy, x1 - 40, yy + 66], radius=33, fill='#ffffff', outline=UI['line'], width=2)
        cx, cy = x0 + 82, yy + 31
        dd.ellipse([cx - 13, cy - 13, cx + 9, cy + 9], outline=UI['muted'], width=4)
        dd.line([(cx + 6, cy + 6), (cx + 18, cy + 18)], fill=UI['muted'], width=5)
        dd.text((x0 + 112, yy + 33), slide['query'], font=f_q, fill=UI['ink'], anchor='lm')
        yy += 100
        for res in slide['results']:
            dd.text((x0 + 45, yy), res['site'], font=f_site, fill=UI['muted'])
            yy += 32
            for l in wrap(dd, res['title'], f_title, tw):
                dd.text((x0 + 45, yy), l, font=f_title, fill='#1a0dab')
                yy += 38
            for l in wrap(dd, res['snippet'], f_snip, tw):
                dd.text((x0 + 45, yy + 4), l, font=f_snip, fill='#4d5156')
                yy += 32
            if res.get('tag'):
                good = res.get('good', False)
                mark(dd, x0 + 61, yy + 26, 15, good)
                dd.text((x0 + 85, yy + 26), res['tag'], font=f_tag, fill=UI['good'] if good else UI['bad'], anchor='lm')
                yy += 48
            yy += 26
        return yy - top

    content = body(ImageDraw.Draw(Image.new('RGB', (W, H))), 0) + 4
    room = 912 - (y + 30)
    if content > room:
        raise ValueError('search slide does not fit (%d px over), shorten: %r' % (content - room, slide['headline']))
    top = y + 30 + (room - content) // 2
    d.rounded_rectangle([x0 + 8, top + 14, x1 + 8, top + content + 14], radius=34, fill='#030a17' if not is_light(cfg['colors']['card']) else cfg['colors'].get('card_shadow') or '#030a17')
    d.rounded_rectangle([x0, top, x1, top + content], radius=34, fill=UI['screen'])
    body(d, top)
    lockup(img, d, cfg)
    return img


STORY = {'chat': draw_chat, 'split': draw_split, 'form': draw_form, 'statement': draw_statement, 'search': draw_search}


def slide_paths(pack_path, pack):
    d = os.path.join(os.path.dirname(pack_path), 'slides', os.path.splitext(os.path.basename(pack_path))[0])
    return [os.path.join(d, 'slide-%02d.jpg' % (i + 1)) for i in range(len(pack['slides']))]


def cmd_render(a):
    pack = read_pack(a.pack)
    cfg = load_cfg(pack['client'])
    paths = slide_paths(a.pack, pack)
    os.makedirs(os.path.dirname(paths[0]), exist_ok=True)
    total = len(pack['slides'])
    scene = os.path.join(os.path.dirname(paths[0]), 'scene.png')
    imgs = []
    for i, (slide, path) in enumerate(zip(pack['slides'], paths)):
        if slide['type'] == 'poster':
            img = draw_poster(cfg, slide, scene if os.path.exists(scene) else None)
        elif slide['type'] in STORY:
            img = STORY[slide['type']](cfg, slide, i + 1 if i else 0, total)
        else:
            img = draw_point(cfg, slide, i, total)
        img.save(path, 'JPEG', quality=93)
        imgs.append(img)
    cols = min(4, total)
    rows = -(-total // cols)
    sheet = Image.new('RGB', (cols * 280 + 20, rows * 280 + 20), '#888888')
    for i, img in enumerate(imgs):
        sheet.paste(img.resize((270, 270)), (15 + (i % cols) * 280, 15 + (i // cols) * 280))
    sheet_path = os.path.join(os.path.dirname(paths[0]), 'contact-sheet.png')
    sheet.save(sheet_path)
    write_preview(a.pack, pack)
    print('slides: %d -> %s\nsheet:  %s' % (total, os.path.dirname(paths[0]), sheet_path))


def tags(t):
    return ' '.join('#' + x.lstrip('#') for x in t)


def linkedin_text(pack):
    return pack['linkedin']['post'].strip() + '\n\n' + tags(pack['linkedin']['hashtags'])


def instagram_text(pack):
    return pack['instagram']['caption'].strip() + '\n\n' + tags(pack['instagram']['hashtags'])


def write_preview(pack_path, pack):
    lines = ['---', 'title: "%s - social pack"' % pack['title'].replace('"', "'"), 'client: %s' % pack['client'],
             'date: %s' % pack['date'], 'slug: %s' % pack['slug'], 'stage: social',
             'wp_post_id: %s' % pack['wp_post_id'], 'canonical_url: "%s"' % pack['canonical_url'],
             'approved: %s' % str(bool(pack.get('approved'))).lower(), '---', '',
             '## LinkedIn', '', linkedin_text(pack), '', '## Instagram', '', instagram_text(pack), '',
             '## Poster', '']
    for s in pack['slides']:
        if s['type'] == 'poster':
            lines += ['%s / %s' % (s['headline_top'], s['headline_main']), s['sub'], '']
            lines += ['%d. %s: %s' % (i, k['label'], k['detail']) for i, k in enumerate(s['cards'], 1)]
        elif s['type'] == 'point':
            lines += ['', '**%s** %s' % (s['headline'], s['body'])]
        else:
            lines += ['', '**%s** (%s)' % (s['type'], ' / '.join(t for _, k, t in slide_copy({'slides': [s]})))]
    with open(os.path.splitext(pack_path)[0] + '.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')


# ---------------------------------------------------------------- preview

PREVIEW = """<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s - social preview</title>
<style>
body{margin:0;background:#eef0f2;font-family:-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:#1d2226}
main{display:flex;flex-wrap:wrap;gap:32px;justify-content:center;padding:32px 16px}
section{width:100%%;max-width:480px}
h2{font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:#667;margin:0 0 10px}
.card{background:#fff;border:1px solid #dcdfe3;border-radius:10px;overflow:hidden}
.head{display:flex;align-items:center;gap:10px;padding:12px 14px}
.av{width:40px;height:40px;border-radius:50%%;background:%(primary)s;color:#fff;font-weight:700;display:grid;place-items:center}
.name{font-weight:600;font-size:14px}.meta{font-size:12px;color:#778}
.text{padding:0 14px 12px;font-size:14px;line-height:1.45;white-space:pre-wrap;overflow-wrap:anywhere}
.fold{display:-webkit-box;-webkit-box-orient:vertical;overflow:hidden}
.li .fold{-webkit-line-clamp:3}.ig .fold{-webkit-line-clamp:2}
.more{border:0;background:none;color:#667;font:inherit;font-size:13px;padding:0 14px 12px;cursor:pointer}
.strip{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:2px;background:#000}
.strip img{width:100%%;flex:0 0 100%%;scroll-snap-align:start;display:block}
.hint{font-size:12px;color:#778;padding:8px 14px}
.comment{margin:10px 14px 14px;padding:10px 12px;background:#f2f4f6;border-radius:8px;font-size:13px;overflow-wrap:anywhere}
.tag{color:#0a66c2}
</style>
<main>
<section class="li"><h2>LinkedIn feed</h2><div class="card">
<div class="head"><div class="av">V</div><div><div class="name">%(name)s</div><div class="meta">Company page - now</div></div></div>
<div class="text fold">%(li)s</div><button class="more">...see more</button>
<div class="strip">%(imgs)s</div>
</div></section>
<section class="ig"><h2>Instagram feed</h2><div class="card">
<div class="head"><div class="av">V</div><div class="name">%(handle)s</div></div>
<div class="strip">%(imgs)s</div>
<div class="text fold"><b>%(handle)s</b> %(ig)s</div><button class="more">more</button>
</div></section>
</main>
<script>
document.querySelectorAll('.more').forEach(function(b){b.onclick=function(){b.previousElementSibling.classList.remove('fold');b.remove()}})
</script>
"""


def cmd_preview(a):
    pack = read_pack(a.pack)
    cfg = load_cfg(pack['client'])
    paths = slide_paths(a.pack, pack)
    if not all(os.path.exists(p) for p in paths):
        sys.exit('render the pack first')

    def rich(text):
        return re.sub(r'(#[a-z0-9]+)', r'<span class="tag">\1</span>', html.escape(text))

    imgs = ''.join('<img alt="%s" src="data:image/jpeg;base64,%s">' % (
        html.escape(s['alt']), base64.b64encode(open(p, 'rb').read()).decode()) for p, s in zip(paths, pack['slides']))
    out = os.path.join(os.path.dirname(paths[0]), 'preview.html')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(PREVIEW % {
            'title': html.escape(pack['title']), 'primary': cfg['colors']['bg_top'], 'name': cfg['name'],
            'handle': cfg['instagram_handle'], 'li': rich(linkedin_text(pack)),
            'ig': rich(instagram_text(pack)),
            'imgs': imgs, 'n': len(paths)})
    print('preview: ' + out)
    if a.open:
        os.startfile(out)


# ---------------------------------------------------------------- qa

EMOJI = re.compile('[\U0001F000-\U0001FAFF☀-➿⬀-⯿️⃣]')
HOUSE_EMOJI = re.compile('\U0001F6A8|[1-9]️⃣|\U0001F4A1|\U0001F449')  # the caption markers in social.md
URL = re.compile(r'https?://\S+|www\.\S+', re.I)
NUM = re.compile(r'\$?\d[\d,]*(?:\.\d+)?%?')
LIMITS = {'headline_top': 34, 'headline_main': 26, 'sub': 58, 'label': 20, 'detail': 34, 'headline': 44, 'body': 170,
          'accent': 30, 'text': 120, 'tag': 26, 'screen': 30, 'title': 24, 'big': 8, 'footer': 110, 'value': 40,
          'button': 28, 'note': 40, 'kicker': 30, 'line1': 32, 'line2': 32,
          'query': 40, 'site': 30, 'snippet': 110, 'result_title': 60}
REQUIRED = {'poster': ('headline_top', 'headline_main', 'sub'), 'point': ('headline', 'body'), 'chat': ('headline',),
            'split': ('headline',), 'search': ('headline', 'query'), 'form': ('headline', 'title', 'button'), 'statement': ('kicker', 'line1', 'line2')}
NOT_DRAWN = ('type', 'alt', 'who', 'typing', 'good')


def slide_copy(pack):
    """(label, field, text) for every string drawn on an image."""
    out = []

    def walk(label, node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k in NOT_DRAWN:
                    continue
                if isinstance(v, str):
                    field = 'result_title' if k == 'title' and ' results ' in label else k
                    out.append(('%s %s' % (label, k), field, v))
                else:
                    walk('%s %s' % (label, k), v)
        elif isinstance(node, list):
            for j, v in enumerate(node, 1):
                walk('%s %d' % (label, j), v)

    for i, s in enumerate(pack['slides'], 1):
        for k in REQUIRED.get(s.get('type'), ()):
            if k not in s:
                out.append(('slide %d %s' % (i, k), k, ''))
        walk('slide %d' % i, s)
    return out


def qa(pack, cfg, source):
    r = cfg['rules']
    fails = []

    def need(ok, msg):
        if not ok:
            fails.append(msg)

    captions = [('linkedin.post', pack['linkedin']['post']), ('instagram.caption', pack['instagram']['caption'])]
    drawn = slide_copy(pack)
    for label, text in captions:
        allowed = HOUSE_EMOJI.sub('', text) if r.get('caption_emoji') else text
        need(not EMOJI.search(allowed), '%s: emoji not allowed here' % label)
        need(pack['canonical_url'] in text, '%s: article URL missing' % label)
    for label, field, text in drawn:
        need(text.strip(), '%s: empty' % label)
        need(len(text) <= LIMITS.get(field, 170), '%s: %d chars, max %d' % (label, len(text), LIMITS.get(field, 170)))
        need(not EMOJI.search(text), '%s: emoji cannot be drawn on the image' % label)
        need(not URL.search(text), '%s: URL on the image' % label)

    src = (source['title'] + ' ' + source['text']).replace(',', '') if source else None
    for label, text in captions + [(l, t) for l, _, t in drawn]:
        for bad in ('—', '&mdash;', '&#8212;', '&#x2014;'):
            need(bad not in text, '%s: em dash' % label)
        need('!' not in text, '%s: exclamation mark' % label)
        need(';' not in text, '%s: semicolon' % label)
        plain = HOUSE_EMOJI.sub('', URL.sub('', text))
        low = plain.lower()
        for word in r['banned']:
            need(not re.search(r'(?<![a-z])%s(?![a-z])' % re.escape(word), low), '%s: banned phrase "%s"' % (label, word))
        for n in NUM.findall(plain) if src else []:
            bare = n.replace(',', '')
            digits = re.sub(r'\D', '', bare)
            if len(digits) < 2 and '%' not in bare and '$' not in bare:
                continue  # single-digit counts ("5 checks") are structure, not claims
            need(bare in src or bare.strip('$%') in src, '%s: figure %s is not in the article' % (label, n))

    li, ig = pack['linkedin'], pack['instagram']
    body = linkedin_text(pack)
    lo, hi = r['linkedin_chars']
    need(lo <= len(body) <= hi, 'linkedin: %d chars, want %d-%d' % (len(body), lo, hi))
    hook = li['post'].strip().split('\n')[0]
    need(len(hook) <= r['linkedin_hook_chars'], 'linkedin: hook line is %d chars, max %d' % (len(hook), r['linkedin_hook_chars']))
    a, b = r['linkedin_hashtags']
    need(a <= len(li['hashtags']) <= b, 'linkedin: %d hashtags, want %d-%d' % (len(li['hashtags']), a, b))

    need(len(instagram_text(pack)) <= 2200, 'instagram: caption over 2200 chars')
    first = ig['caption'].strip().split('\n')[0]
    need(len(first) <= r['instagram_hook_chars'], 'instagram: first line is %d chars, max %d' % (len(first), r['instagram_hook_chars']))
    a, b = r['instagram_hashtags']
    need(a <= len(ig['hashtags']) <= b, 'instagram: %d hashtags, want %d-%d' % (len(ig['hashtags']), a, b))
    for t in li['hashtags'] + ig['hashtags']:
        need(re.fullmatch(r.get('hashtag_pattern', '[a-z0-9]+'), t), 'hashtag %r breaks the house hashtag style' % t)
    need('#' not in li['post'] + ig['caption'], 'hashtags belong in the hashtags array, not the caption text')

    s = pack['slides']
    need(1 <= len(s) <= r.get('max_slides', 7), 'slides: %d, max %d' % (len(s), r.get('max_slides', 7)))
    need(all(x.get('type') in REQUIRED for x in s), 'slides: unknown slide type (use %s)' % ', '.join(REQUIRED))
    need(s[0].get('type') != 'point', 'slides: the first slide is the cover, it cannot be a point slide')
    a, b = r['cards']
    for x in s:
        if x.get('type') == 'poster':
            need(a <= len(x.get('cards', [])) <= b, 'poster: %d cards, want %d-%d' % (len(x.get('cards', [])), a, b))
    alts = [x.get('alt', '') for x in s]
    need(all(20 <= len(x) <= 120 for x in alts), 'slides: every slide needs alt text of 20-120 chars')
    need(len(set(alts)) == len(alts), 'slides: alt text is repeated')
    return fails


def load_source(pack):
    path = os.path.join(social_dir(pack['client']), '_source', '%s.json' % pack['wp_post_id'])
    return read_pack(path) if os.path.exists(path) else None


def cmd_qa(a):
    pack = read_pack(a.pack)
    source = load_source(pack)
    if not source:
        sys.exit('QA cannot run: no source file for post %s. Run fetch first.' % pack['wp_post_id'])
    fails = qa(pack, load_cfg(pack['client']), source)
    for f in fails:
        print('FAIL  ' + f)
    print('QA %s (%d issue%s)' % ('FAILED' if fails else 'PASSED', len(fails), '' if len(fails) == 1 else 's'))
    sys.exit(1 if fails else 0)


def cmd_approve(a):
    pack = read_pack(a.pack)
    pack['approved'] = True
    write_pack(a.pack, pack)
    write_preview(a.pack, pack)
    print('approved: ' + a.pack)


# ---------------------------------------------------------------- publish

def creds(cfg, env, channel):
    got = {k: env.get(v) or os.environ.get(v) for k, v in cfg[channel]['env'].items()}
    return got, [cfg[channel]['env'][k] for k, v in got.items() if not v]


def li_escape(text):
    # LinkedIn "little text" reserves these; unescaped parentheses silently truncate a post.
    return re.sub(r'([\\|{}@\[\]()<>*_~])', r'\\\1', text)


def post_linkedin(cfg, c, pack, paths):
    hdr = {'Authorization': 'Bearer ' + c['token'], 'X-Restli-Protocol-Version': '2.0.0',
           'LinkedIn-Version': cfg['linkedin']['api_version'], 'Content-Type': 'application/json'}
    org = 'urn:li:organization:' + c['org_id']
    images = []
    for path, slide in zip(paths, pack['slides']):
        r = requests.post('https://api.linkedin.com/rest/images?action=initializeUpload', headers=hdr,
                          json={'initializeUploadRequest': {'owner': org}}, timeout=60)
        r.raise_for_status()
        v = r.json()['value']
        with open(path, 'rb') as f:
            requests.put(v['uploadUrl'], headers={'Authorization': 'Bearer ' + c['token']}, data=f.read(),
                         timeout=120).raise_for_status()
        images.append({'id': v['image'], 'altText': slide['alt']})
    r = requests.post('https://api.linkedin.com/rest/posts', headers=hdr, timeout=60, json={
        'author': org, 'commentary': li_escape(linkedin_text(pack)), 'visibility': 'PUBLIC',
        'distribution': {'feedDistribution': 'MAIN_FEED', 'targetEntities': [], 'thirdPartyDistributionChannels': []},
        'content': {'media': images[0]} if len(images) == 1 else {'multiImage': {'images': images}},
        'lifecycleState': 'PUBLISHED', 'isReshareDisabledByAuthor': False})
    if r.status_code != 201:
        raise RuntimeError('LinkedIn post failed %s: %s' % (r.status_code, r.text[:400]))
    urn = r.headers['x-restli-id']
    state = {'post_urn': urn, 'url': 'https://www.linkedin.com/feed/update/%s/' % urn}
    return state


def wp_upload(cfg, env, path, name):
    h = wp_auth(cfg, env)
    h.update({'Content-Type': 'image/jpeg', 'Content-Disposition': 'attachment; filename="%s"' % name})
    with open(path, 'rb') as f:
        r = requests.post(cfg['wp']['site'] + '/wp-json/wp/v2/media', headers=h, data=f.read(), timeout=120)
    r.raise_for_status()
    return r.json()['source_url']


def post_instagram(cfg, env, c, pack, paths, state):
    # Instagram only ingests images from a public URL, so the slides are hosted in the client's media library.
    urls = state.setdefault('hosted', [])
    for i, path in enumerate(paths[len(urls):], len(urls) + 1):
        urls.append(wp_upload(cfg, env, path, 'social-%s-%02d.jpg' % (pack['slug'], i)))
    base = '%s/%s' % (cfg['instagram']['graph_host'], cfg['instagram']['api_version'])
    tok = {'access_token': c['token']}

    def call(method, path, **params):
        r = requests.request(method, '%s/%s' % (base, path), data=dict(params, **tok) if method == 'POST' else None,
                             params=dict(params, **tok) if method == 'GET' else None, timeout=120)
        if r.status_code != 200:
            raise RuntimeError('Instagram %s failed %s: %s' % (path, r.status_code, r.text[:400]))
        return r.json()

    if len(urls) == 1:
        box = call('POST', c['user_id'] + '/media', image_url=urls[0], caption=instagram_text(pack))['id']
    else:
        kids = [call('POST', c['user_id'] + '/media', image_url=u, is_carousel_item='true')['id'] for u in urls]
        box = call('POST', c['user_id'] + '/media', media_type='CAROUSEL', children=','.join(kids),
                   caption=instagram_text(pack))['id']
    for _ in range(20):
        status = call('GET', box, fields='status_code')['status_code']
        if status == 'FINISHED':
            break
        if status == 'ERROR':
            raise RuntimeError('Instagram rejected the media container')
        time.sleep(3)
    media = call('POST', c['user_id'] + '/media_publish', creation_id=box)['id']
    state.update({'media_id': media, 'url': call('GET', media, fields='permalink').get('permalink')})
    return state


def publish(pack_path, dry_run, only=None):
    """Returns a list of human-readable outcome lines. Never posts a channel twice."""
    pack = read_pack(pack_path)
    cfg, env = load_cfg(pack['client']), load_env()
    state = pack.setdefault('state', {})
    channels = [ch for ch in ('linkedin', 'instagram') if (not only or ch in only) and cfg[ch]['enabled']]
    todo = [ch for ch in channels if not state.get(ch, {}).get('url')]
    if not todo:
        return ['already posted: ' + ', '.join(channels)]

    blockers = []
    source = load_source(pack)
    fails = qa(pack, cfg, source) if source else ['no source file, run fetch']
    if fails:
        blockers.append('QA: ' + '; '.join(fails[:3]))
    paths = slide_paths(pack_path, pack)
    if not all(os.path.exists(p) for p in paths):
        blockers.append('slides not rendered')
    if not (pack.get('approved') or cfg['auto_approve']):
        blockers.append('not approved')
    live = wp_post(cfg, env, pack['wp_post_id'])
    if live['status'] != 'publish':
        blockers.append('article is still "%s" in WordPress, its link would not resolve' % live['status'])
    elif live['link'] != pack['canonical_url']:
        blockers.append('article URL changed to %s, update the pack' % live['link'])
    ready = {}
    for ch in todo:
        c, missing = creds(cfg, env, ch)
        if missing:
            blockers.append('%s: missing %s in .env' % (ch, ', '.join(missing)))
        ready[ch] = c
    if blockers:
        return ['HELD  ' + b for b in blockers]
    if dry_run:
        return ['DRY RUN, would post %d image(s) to: %s' % (len(paths), ', '.join(todo))]

    out = []
    for ch in todo:
        try:
            if ch == 'linkedin':
                state[ch] = post_linkedin(cfg, ready[ch], pack, paths)
            else:
                state[ch] = post_instagram(cfg, env, ready[ch], pack, paths, state.setdefault(ch, {}))
            out.append('POSTED %s: %s' % (ch, state[ch]['url']))
        except Exception as e:  # one channel failing must not stop the other
            out.append('ERROR %s: %s' % (ch, e))
        write_pack(pack_path, pack)  # after every channel, so a crash can never cause a double post
    return out


def cmd_publish(a):
    lines = publish(a.pack, a.dry_run, a.only)
    print('\n'.join(lines))
    sys.exit(1 if any(l.startswith(('HELD', 'ERROR')) for l in lines) else 0)


def cmd_sweep(a):
    packs = sorted(glob.glob(os.path.join(social_dir(a.client), '*.json')))
    if not packs:
        print('no packs in ' + social_dir(a.client))
    for path in packs:
        print(os.path.basename(path))
        for line in publish(path, a.dry_run):
            print('  ' + line)


def cmd_check(a):
    cfg, env = load_cfg(a.client), load_env()
    for ch in ('linkedin', 'instagram'):
        _, missing = creds(cfg, env, ch)
        print('%-10s %s' % (ch, 'ready' if not missing else 'MISSING ' + ', '.join(missing)))
    print('auto_approve: %s' % cfg['auto_approve'])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--client', default='virtina')
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('fetch'); p.add_argument('post_id'); p.set_defaults(fn=cmd_fetch)
    for name, fn in (('render', cmd_render), ('qa', cmd_qa), ('approve', cmd_approve)):
        p = sub.add_parser(name); p.add_argument('pack'); p.set_defaults(fn=fn)
    p = sub.add_parser('preview'); p.add_argument('pack'); p.add_argument('--open', action='store_true')
    p.set_defaults(fn=cmd_preview)
    p = sub.add_parser('publish'); p.add_argument('pack'); p.add_argument('--dry-run', action='store_true')
    p.add_argument('--only', nargs='+', choices=['linkedin', 'instagram']); p.set_defaults(fn=cmd_publish)
    p = sub.add_parser('sweep'); p.add_argument('--dry-run', action='store_true'); p.set_defaults(fn=cmd_sweep)
    p = sub.add_parser('check'); p.set_defaults(fn=cmd_check)
    a = ap.parse_args()
    a.fn(a)


if __name__ == '__main__':
    main()
