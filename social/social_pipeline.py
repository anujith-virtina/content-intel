"""Blog post -> LinkedIn + Instagram pipeline.

  fetch   <post_id>   pull the article from WordPress, write the source file the copywriter reads
  render  <pack.json> draw the 1080x1350 carousel slides + a contact sheet + a readable .md preview
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
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
W, H = 1080, 1350
PAD = 96


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


def block(draw, xy, lines, fnt, fill, gap=1.22):
    x, y = xy
    step = int(fnt.size * gap)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y


def arrow(draw, x, y, size, fill):
    t = max(4, size // 7)
    draw.rectangle([x, y - t // 2, x + size, y + t // 2], fill=fill)
    draw.polygon([(x + size - size // 2, y - size // 2), (x + size + t, y), (x + size - size // 2, y + size // 2),
                  (x + size - size // 2 - t, y + size // 2 - t), (x + size - t * 2, y),
                  (x + size - size // 2 - t, y - size // 2 + t)], fill=fill)


def footer(draw, cfg, idx, total, fg, muted):
    c = cfg['colors']
    y = H - PAD - 34
    draw.text((PAD, y), cfg['wordmark'], font=font(cfg, 'extrabold', 34), fill=fg)
    if idx < total:
        arrow(draw, W - PAD - 64, y + 18, 56, c['accent'])
    label = '%d / %d' % (idx, total)
    f = font(cfg, 'semibold', 26)
    draw.text((W - PAD - 100 - draw.textlength(label, font=f), y + 4), label, font=f, fill=muted)


def draw_slide(cfg, slide, idx, total):
    c = cfg['colors']
    dark = slide['type'] in ('cover', 'cta')
    img = Image.new('RGB', (W, H), c['primary'] if dark else c['light'])
    d = ImageDraw.Draw(img)
    col = W - 2 * PAD
    d.rectangle([0, 0, W, 18], fill=c['accent'])

    if slide['type'] == 'cover':
        d.text((PAD, 170), slide['kicker'].upper(), font=font(cfg, 'bold', 30), fill=c['accent'])
        f, lines = fit(d, cfg, slide['headline'], 'extrabold', range(104, 59, -4), col, 6)
        y = block(d, (PAD, 250), lines, f, '#ffffff', 1.12)
        d.rectangle([PAD, y + 36, PAD + 120, y + 44], fill=c['accent'])
        if slide.get('sub'):
            f2, l2 = fit(d, cfg, slide['sub'], 'regular', range(40, 31, -2), col, 3)
            block(d, (PAD, y + 84), l2, f2, '#dbe4ec', 1.35)
        footer(d, cfg, idx, total, '#ffffff', '#b9c7d4')
    elif slide['type'] == 'point':
        d.text((PAD, 150), '%02d' % slide['number'], font=font(cfg, 'extrabold', 150), fill=c['link'])
        f, lines = fit(d, cfg, slide['headline'], 'bold', range(68, 47, -4), col, 4)
        y = block(d, (PAD, 380), lines, f, c['primary'], 1.16)
        f2, l2 = fit(d, cfg, slide['body'], 'regular', range(42, 33, -2), col, 9)
        block(d, (PAD, y + 44), l2, f2, c['text'], 1.42)
        footer(d, cfg, idx, total, c['primary'], '#8496a6')
    else:  # cta
        f, lines = fit(d, cfg, slide['headline'], 'extrabold', range(84, 55, -4), col, 5)
        y = block(d, (PAD, 300), lines, f, '#ffffff', 1.14)
        f2, l2 = fit(d, cfg, slide['body'], 'regular', range(42, 33, -2), col, 5)
        y = block(d, (PAD, y + 40), l2, f2, '#dbe4ec', 1.4)
        fp = font(cfg, 'bold', 34)
        label = slide.get('label') or cfg['cta_label']
        pw = d.textlength(label, font=fp) + 80
        d.rounded_rectangle([PAD, y + 56, PAD + pw, y + 146], radius=45, fill=c['accent'])
        d.text((PAD + 40, y + 82), label, font=fp, fill=c['primary_dark'])
        footer(d, cfg, idx, total, '#ffffff', '#b9c7d4')
    return img


def slide_paths(pack_path, pack):
    d = os.path.join(os.path.dirname(pack_path), 'slides', os.path.splitext(os.path.basename(pack_path))[0])
    return [os.path.join(d, 'slide-%02d.jpg' % (i + 1)) for i in range(len(pack['slides']))]


def cmd_render(a):
    pack = read_pack(a.pack)
    cfg = load_cfg(pack['client'])
    paths = slide_paths(a.pack, pack)
    os.makedirs(os.path.dirname(paths[0]), exist_ok=True)
    total = len(pack['slides'])
    imgs = []
    for i, (slide, path) in enumerate(zip(pack['slides'], paths), 1):
        img = draw_slide(cfg, slide, i, total)
        img.save(path, 'JPEG', quality=92)
        imgs.append(img)
    cols = min(4, total)
    rows = -(-total // cols)
    sheet = Image.new('RGB', (cols * 280 + 20, rows * 350 + 20), '#888888')
    for i, img in enumerate(imgs):
        sheet.paste(img.resize((270, 338)), (15 + (i % cols) * 280, 15 + (i // cols) * 350))
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
             '## LinkedIn', '', linkedin_text(pack), '', '**First comment:** ' + pack['linkedin']['first_comment'], '',
             '## Instagram', '', instagram_text(pack), '', '## Carousel slides', '']
    for i, s in enumerate(pack['slides'], 1):
        parts = [s.get('kicker'), s.get('headline'), s.get('sub'), s.get('body')]
        lines.append('%d. **%s** %s' % (i, s['type'], ' / '.join(p for p in parts if p)))
    with open(os.path.splitext(pack_path)[0] + '.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')


# ---------------------------------------------------------------- qa

EMOJI = re.compile('[\U0001F000-\U0001FAFF☀-➿⬀-⯿️]')
URL = re.compile(r'https?://|www\.|\b[a-z0-9-]+\.(com|io|net|org)\b', re.I)
NUM = re.compile(r'\$?\d[\d,]*(?:\.\d+)?%?')


def all_copy(pack):
    """(label, text) for every string a reader will see."""
    out = [('linkedin.post', pack['linkedin']['post']), ('instagram.caption', pack['instagram']['caption'])]
    for i, s in enumerate(pack['slides'], 1):
        for k in ('kicker', 'headline', 'sub', 'body', 'label'):
            if s.get(k):
                out.append(('slide %d %s' % (i, k), s[k]))
    return out


def qa(pack, cfg, source):
    r = cfg['rules']
    fails = []

    def need(ok, msg):
        if not ok:
            fails.append(msg)

    for label, text in all_copy(pack):
        for bad in ('—', '&mdash;', '&#8212;', '&#x2014;'):
            need(bad not in text, '%s: em dash' % label)
        need('!' not in text, '%s: exclamation mark' % label)
        need(';' not in text, '%s: semicolon' % label)
        need(not EMOJI.search(text), '%s: emoji' % label)
        low = text.lower()
        for word in r['banned']:
            need(not re.search(r'(?<![a-z])%s(?![a-z])' % re.escape(word), low), '%s: banned phrase "%s"' % (label, word))
        if source:
            src = source['text'].replace(',', '')
            for n in NUM.findall(text):
                bare = n.replace(',', '')
                digits = re.sub(r'\D', '', bare)
                if len(digits) < 2 and '%' not in bare and '$' not in bare:
                    continue  # single-digit counts ("5 reasons") are structure, not claims
                need(bare in src or bare.strip('$%') in src, '%s: figure %s is not in the article' % (label, n))

    li, ig = pack['linkedin'], pack['instagram']
    body = linkedin_text(pack)
    lo, hi = r['linkedin_chars']
    need(lo <= len(body) <= hi, 'linkedin: %d chars, want %d-%d' % (len(body), lo, hi))
    hook = li['post'].strip().split('\n')[0]
    need(len(hook) <= r['linkedin_hook_chars'], 'linkedin: hook line is %d chars, max %d' % (len(hook), r['linkedin_hook_chars']))
    need(not URL.search(li['post']), 'linkedin: link in the post body (belongs in the first comment)')
    need(pack['canonical_url'] in li['first_comment'], 'linkedin: first comment is missing the article URL')
    a, b = r['linkedin_hashtags']
    need(a <= len(li['hashtags']) <= b, 'linkedin: %d hashtags, want %d-%d' % (len(li['hashtags']), a, b))

    cap = instagram_text(pack)
    need(len(cap) <= 2200, 'instagram: caption %d chars, limit 2200' % len(cap))
    first = ig['caption'].strip().split('\n')[0]
    need(len(first) <= r['instagram_hook_chars'], 'instagram: first line is %d chars, max %d' % (len(first), r['instagram_hook_chars']))
    need(not URL.search(ig['caption']), 'instagram: URL in the caption (not clickable, use "link in bio")')
    need('link in bio' in ig['caption'].lower(), 'instagram: no "link in bio" call to action')
    a, b = r['instagram_hashtags']
    need(a <= len(ig['hashtags']) <= b, 'instagram: %d hashtags, want %d-%d' % (len(ig['hashtags']), a, b))
    for t in li['hashtags'] + ig['hashtags']:
        need(re.fullmatch(r'#?[a-z0-9]+', t), 'hashtag %r must be lowercase letters and digits only' % t)

    s = pack['slides']
    a, b = r['slides']
    need(a <= len(s) <= b, 'slides: %d, want %d-%d' % (len(s), a, b))
    need(s[0]['type'] == 'cover' and s[-1]['type'] == 'cta', 'slides: first must be cover, last must be cta')
    need(all(x['type'] == 'point' for x in s[1:-1]), 'slides: everything between cover and cta must be a point')
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
        'content': {'multiImage': {'images': images}},
        'lifecycleState': 'PUBLISHED', 'isReshareDisabledByAuthor': False})
    if r.status_code != 201:
        raise RuntimeError('LinkedIn post failed %s: %s' % (r.status_code, r.text[:400]))
    urn = r.headers['x-restli-id']
    state = {'post_urn': urn, 'url': 'https://www.linkedin.com/feed/update/%s/' % urn}
    r = requests.post('https://api.linkedin.com/rest/socialActions/%s/comments' % urllib.parse.quote(urn, safe=''),
                      headers=hdr, timeout=60,
                      json={'actor': org, 'object': urn, 'message': {'text': pack['linkedin']['first_comment']}})
    state['first_comment'] = 'posted' if r.status_code in (200, 201) else 'FAILED %s, add it by hand' % r.status_code
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

    kids = [call('POST', c['user_id'] + '/media', image_url=u, is_carousel_item='true')['id'] for u in urls]
    box = call('POST', c['user_id'] + '/media', media_type='CAROUSEL', children=','.join(kids),
               caption=instagram_text(pack))['id']
    for _ in range(20):
        status = call('GET', box, fields='status_code')['status_code']
        if status == 'FINISHED':
            break
        if status == 'ERROR':
            raise RuntimeError('Instagram rejected the carousel container')
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
        return ['DRY RUN, would post %d slides to: %s' % (len(paths), ', '.join(todo))]

    out = []
    for ch in todo:
        try:
            if ch == 'linkedin':
                state[ch] = post_linkedin(cfg, ready[ch], pack, paths)
            else:
                state[ch] = post_instagram(cfg, env, ready[ch], pack, paths, state.setdefault(ch, {}))
            out.append('POSTED %s: %s' % (ch, state[ch]['url']))
            if state[ch].get('first_comment', 'posted') != 'posted':
                out.append('  first comment ' + state[ch]['first_comment'])
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
    p = sub.add_parser('publish'); p.add_argument('pack'); p.add_argument('--dry-run', action='store_true')
    p.add_argument('--only', nargs='+', choices=['linkedin', 'instagram']); p.set_defaults(fn=cmd_publish)
    p = sub.add_parser('sweep'); p.add_argument('--dry-run', action='store_true'); p.set_defaults(fn=cmd_sweep)
    p = sub.add_parser('check'); p.set_defaults(fn=cmd_check)
    a = ap.parse_args()
    a.fn(a)


if __name__ == '__main__':
    main()
