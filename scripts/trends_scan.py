# -*- coding: utf-8 -*-
"""Google Trends scan for a client. Pulls related queries (top and rising) and momentum for each seed term.

Usage:
  python scripts/trends_scan.py --client virtina            # uses clients/virtina/trends-seeds.json
  python scripts/trends_scan.py --client chatsku --geo US --timeframe "today 12-m"

Writes clients/{client}/output/research/trends-scan-{YYYY-MM-DD}.json and .md.
Needs: pip install pytrends. Google Trends has low volume for niche B2B terms and returns noisy 'Breakout'
rising queries that are unrelated to the seed, so the trend-scout agent must filter and stay honest.
"""
import argparse, datetime, json, os, sys, time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def call(fn, tries=4):
    delay = 20
    for n in range(tries):
        try:
            return fn()
        except Exception as e:  # pytrends raises ResponseError on 429
            if n == tries - 1:
                return None
            time.sleep(delay)
            delay *= 2


def momentum(df, col):
    """Average of the last 4 weeks vs the 8 weeks before it, on the weekly series (None if no data)."""
    try:
        s = df[col].astype(float)
        if len(s) < 14 or s.sum() == 0:
            return None
        recent, prior = s.iloc[-4:].mean(), s.iloc[-12:-4].mean()
        return {'recent4w': round(recent, 1), 'prior8w': round(prior, 1),
                'change_pct': None if prior == 0 else round((recent - prior) / prior * 100, 1)}
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--client', required=True)
    ap.add_argument('--geo', default='US')
    ap.add_argument('--timeframe', default='today 12-m')
    ap.add_argument('--pause', type=float, default=7.0)
    a = ap.parse_args()
    seeds_path = os.path.join(ROOT, 'clients', a.client, 'trends-seeds.json')
    seeds = json.load(open(seeds_path, encoding='utf-8'))['seeds']
    from pytrends.request import TrendReq
    py = TrendReq(hl='en-US', tz=360, timeout=(10, 30))
    out = {'client': a.client, 'geo': a.geo, 'timeframe': a.timeframe,
           'date': datetime.date.today().isoformat(), 'seeds': []}
    for seed in seeds:
        print('seed:', seed, flush=True)
        rec = {'seed': seed, 'top': [], 'rising': [], 'momentum': None, 'error': None}
        ok = call(lambda: py.build_payload([seed], timeframe=a.timeframe, geo=a.geo))
        rq = call(lambda: py.related_queries())
        if rq and seed in rq:
            t, r = rq[seed].get('top'), rq[seed].get('rising')
            if t is not None:
                rec['top'] = t.head(8).to_dict('records')
            if r is not None:
                rec['rising'] = r.head(8).to_dict('records')
        else:
            rec['error'] = 'no related-query data (rate limit or too little volume)'
        time.sleep(a.pause)
        iot = call(lambda: py.interest_over_time())
        if iot is not None and seed in iot:
            rec['momentum'] = momentum(iot, seed)
        out['seeds'].append(rec)
        time.sleep(a.pause)
    base = os.path.join(ROOT, 'clients', a.client, 'output', 'research', 'trends-scan-%s' % out['date'])
    os.makedirs(os.path.dirname(base), exist_ok=True)
    json.dump(out, open(base + '.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    lines = ['---', 'title: Google Trends scan, %s' % a.client, 'client: %s' % a.client, 'date: %s' % out['date'],
             'stage: research', 'source: Google Trends via pytrends, geo %s, %s' % (a.geo, a.timeframe), '---', '',
             '# Google Trends scan (%s, %s, %s)' % (a.client, a.geo, a.timeframe), '',
             'Index values are relative (100 = peak for that seed alone). Niche B2B terms have low volume. ',
             'Rising queries marked Breakout are often unrelated noise: the trend-scout agent filters them.', '']
    for r in out['seeds']:
        lines.append('## %s' % r['seed'])
        lines.append('- Momentum (last 4 weeks vs prior 8): %s' % (r['momentum'] or 'no data'))
        lines.append('- Top related: %s' % ('; '.join('%s (%s)' % (x['query'], x['value']) for x in r['top']) or 'none'))
        lines.append('- Rising related: %s' % ('; '.join('%s (%s)' % (x['query'], x['value']) for x in r['rising']) or 'none'))
        if r['error']:
            lines.append('- Note: %s' % r['error'])
        lines.append('')
    open(base + '.md', 'w', encoding='utf-8').write('\n'.join(lines))
    print('wrote', base + '.json', 'and .md')


if __name__ == '__main__':
    sys.exit(main())
