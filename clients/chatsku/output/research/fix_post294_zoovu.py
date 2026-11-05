"""Correct the Zoovu claims in published ChatSKU post 294 using Zoovu's own pages (checked 2026-11-05).
Usage: python fix_post294_zoovu.py        (dry run, prints the changes)
       python fix_post294_zoovu.py apply  (updates post 294 in place; status untouched; backup already saved)"""
import sys,os,json,re,base64,urllib.request,difflib
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import curlshim
BK=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','post294','post294_backup_2026-11-05.json')
d=json.load(open(BK,encoding='utf-8')); raw=d['content']['raw']; ed=d['meta']['_elementor_data']
def esc(s): return json.dumps(s,ensure_ascii=False)[1:-1].replace('/','\/')
TEXT=[("Combines 3D product configuration with conversational guided selling, a distinctive combination nothing else in this list offers.","Combines Visual CPQ (configure, price, quote) with guided selling, product finders and AI search in one suite."),
("Self-service RFQ product line built specifically for B2B manufacturers.","Self-service RFQ and bill-of-materials tools for B2B quoting."),
("Omnichannel reach across WhatsApp and Instagram beyond the website, something no other tool here explicitly offers.","Named integrations include Shopify Plus, WooCommerce, BigCommerce, SAP and HubSpot, according to Zoovu's integrations page (checked 2026-11-05)."),
("Thinner public documentation on hard numbers, pricing, deployment time, exact tiered-pricing mechanics, than Algolia, Coveo, or Bloomreach. Expect a sales call before you get specifics. No voice or image search. And the fit is narrow. A distributor selling straightforward SKUs with no configuration complexity will find this more tool than they need.","Pricing is not published, and Zoovu states an average launch of about six weeks for B2B Site Search (checked 2026-11-05), so plan for a project. The fit is narrow. A distributor selling straightforward SKUs with no configuration complexity may find the suite more than it needs."),
("Not publicly disclosed. Contact for quote.","A product fee plus a usage fee, with no prices published (checked 2026-11-05). Zoovu offers a Book a demo option.")]
CELLS={3:("Custom, no rate card","Product plus usage fee, no prices published"),4:("Limited, omnichannel","Many named, including WooCommerce and SAP"),5:("Not published","About 6 weeks average (B2B Site Search)"),6:("Implied, no detail","Not stated"),7:("Not a focus","Not stated"),8:("Text only","Voice and image not stated"),9:("Not disclosed","Search analytics listed")}
def fix(s,is_ed):
    f=esc if is_ed else (lambda x:x)
    a=s.find('"title":"Zoovu"') if is_ed else s.find('<h3>Zoovu</h3>')
    b=s.find('"title":"Coveo',a) if is_ed else s.find('<h3>Coveo',a)
    assert 0<a<b
    seg=s[a:b]
    for o,n in TEXT:
        assert seg.count(f(o))==1,('text',o[:40]); seg=seg.replace(f(o),f(n))
    s=s[:a]+seg+s[b:]
    # comparison table row for Zoovu
    td_open='<td style=\\"padding:8px 10px;border-bottom:1px solid #e0e0e0;\\">' if is_ed else '<td style="padding: 8px 10px; border-bottom: 1px solid #e0e0e0;">'
    td_close='<\/td>' if is_ed else '</td>'
    start=s.find(td_open+'Zoovu'+td_close)
    assert start>0,('row start',is_ed)
    end=s.find('<\/tr>' if is_ed else '</tr>',start)
    row=s[start:end]
    cells=re.findall(re.escape(td_open)+r'(.*?)'+re.escape(td_close),row,flags=re.S)
    assert len(cells)==10,(is_ed,len(cells),cells)
    for i,(o,n) in CELLS.items():
        assert cells[i]==f(o),(i,cells[i],o)
        cells[i]=f(n)
    newrow=''.join(td_open+c+td_close for c in cells)
    # keep any separators between cells (newlines) by rebuilding via sequential replace
    out=row; pos=0
    parts=re.split('('+re.escape(td_open)+r'.*?'+re.escape(td_close)+')',row,flags=re.S)
    k=0
    for j,p in enumerate(parts):
        if p.startswith(td_open):
            parts[j]=td_open+cells[k]+td_close; k+=1
    row2=''.join(parts)
    return s[:start]+row2+s[end:]
new_raw=fix(raw,False); new_ed=fix(ed,True)
json.loads(new_ed)  # must stay valid JSON
sm=lambda a,b:[l for l in difflib.unified_diff(re.sub(r'(</?(td|li|p|tr|h3)[^>]*>)',r'\n\1',a).split('\n'),re.sub(r'(</?(td|li|p|tr|h3)[^>]*>)',r'\n\1',b).split('\n'),lineterm='',n=0) if l[0] in '+-' and not l.startswith(('+++','---'))]
for l in sm(raw,new_raw): print(l[:170])
print('raw delta',len(new_raw)-len(raw),'| elementor delta',len(new_ed)-len(ed),'| elementor JSON ok')
if len(sys.argv)>1 and sys.argv[1]=='apply':
    env={}
    for l in open(r'C:\content-intel\.env',encoding='utf-8'):
        l=l.strip()
        if '=' in l and not l.startswith('#'): k,v=l.split('=',1); env[k]=v.strip().strip('"')
    A=base64.b64encode(f"{env['CHATSKU_WP_USERNAME']}:{env['CHATSKU_WP_APP_PASSWORD']}".encode()).decode()
    H={'Authorization':'Basic '+A,'Content-Type':'application/json'}
    live=json.load(urllib.request.urlopen(urllib.request.Request('https://chatsku.com/wp-json/wp/v2/posts/294?context=edit&_fields=id,status,modified,content',headers=H),timeout=90))
    if live['content']['raw']!=raw: sys.exit('ABORT: post 294 changed since the backup, re-fetch and re-run')
    p=json.load(urllib.request.urlopen(urllib.request.Request('https://chatsku.com/wp-json/wp/v2/posts/294',data=json.dumps({'content':new_raw,'meta':{'_elementor_data':new_ed}}).encode(),method='POST',headers=H),timeout=120))
    print('updated 294, status',p['status'],p['modified'])
    try: urllib.request.urlopen(urllib.request.Request('https://chatsku.com/wp-json/elementor/v1/cache',headers=H,method='DELETE'),timeout=60); print('cache cleared')
    except Exception as e: print('cache',e)
