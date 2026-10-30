import json,base64,urllib.request,re,sys
env={}
for l in open(r'C:\content-intel\.env',encoding='utf-8'):
    if '=' in l and not l.startswith('#'):
        k,v=l.strip().split('=',1); env[k]=v.strip().strip('"').strip("'")
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
H={'Authorization':'Basic '+base64.b64encode((env['CHATSKU_WP_USERNAME']+':'+env['CHATSKU_WP_APP_PASSWORD']).encode()).decode(),'User-Agent':UA}
import time
def get(u):
    for a in range(5):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=120))
        except Exception as e: print('retry',a,e); time.sleep(5)
    raise SystemExit('live fetch failed')
live=get('https://chatsku.com/wp-json/wp/v2/posts/3798?context=edit')
src=open('revision_3811.html',encoding='utf-8').read()
def sec(c,name):
    m=re.search(r'<h2>'+name+r'</h2>(.*?)(?=<h2>|\Z)',c,re.S); return m.group(1) if m else ''
concl=sec(src,'Conclusion').strip(); faq=sec(src,'Frequently Asked Questions').strip()
# FAQ -> (question, answer html)
pairs=[]
for part in re.split(r'(?=<a tabindex="0">)',faq):
    m=re.match(r'<a tabindex="0">(.*?)</a>(.*)',part,re.S)
    if m:
        ans=''.join(re.findall(r'<p[^>]*>.*?</p>',m.group(2),re.S)).strip()
        pairs.append((re.sub(r'\s+',' ',m.group(1)).strip(), ans))
paras=re.findall(r'<p[^>]*>.*?</p>',concl,re.S)
paras=[re.sub(r'\s+style="[^"]*"','',x) for x in paras]
import secrets
gid=lambda: secrets.token_hex(4)
def heading(t,color='#1a1a2e',align='left',level='h2'):
    s={'title':t,'align':align,'title_color':color,'typography_typography':'custom','typography_font_size':{'size':28 if level=='h2' else 22,'unit':'px'}}
    if level!='h2': s['header_size']=level
    return {'id':gid(),'elType':'widget','widgetType':'heading','elements':[],'settings':s}
def text(html,dark=False):
    if dark: html=re.sub(r'<p>','<p style="color:#aaaacc;text-align:center;font-size:18px;max-width:720px;margin:0 auto 14px auto;">',html)
    return {'id':gid(),'elType':'widget','widgetType':'text-editor','elements':[],'settings':{'editor':html}}
def button(t,url):
    return {'id':gid(),'elType':'widget','widgetType':'button','elements':[],'settings':{'text':t,'link':{'url':url,'is_external':'','nofollow':''},'align':'center','background_color':'#e94560','button_text_color':'#ffffff','border_radius':{'size':6,'unit':'px'},'_margin':{'unit':'px','top':'20','right':'0','bottom':'0','left':'0','isLinked':False}}}
def accordion(ps):
    return {'id':gid(),'elType':'widget','widgetType':'accordion','elements':[],'settings':{'tabs':[{'_id':gid(),'tab_title':q,'tab_content':a} for q,a in ps]}}
def section(widgets,bg,concl_=False):
    pad={'top':'20','bottom':'30','unit':'px'} if concl_ else {'top':'60','bottom':'60','unit':'px'}
    return {'id':gid(),'elType':'section','isInner':False,'settings':{'background_background':'classic','background_color':bg,'padding':pad},
            'elements':[{'id':gid(),'elType':'column','isInner':False,'settings':{'_column_size':100,'width':'100','padding':{'unit':'px','top':'20','right':'20','bottom':'20','left':'20','isLinked':True}},'elements':widgets}]}
new_concl=section([heading('Conclusion',color='#ffffff',align='center'),text(''.join(paras),dark=True),button('See the feature list','https://chatsku.com/features/')],'#1a1a2e',True)
new_faq=section([heading('Frequently Asked Questions'),accordion(pairs)],'#f9f9fb')
data=json.loads(live['meta']['_elementor_data'])
idx_c=[i for i,s in enumerate(data) if any(w.get('widgetType')=='heading' and w['settings'].get('title')=='Conclusion' for w in s['elements'][0]['elements'])]
idx_f=[i for i,s in enumerate(data) if any(w.get('widgetType')=='heading' and w['settings'].get('title')=='Frequently Asked Questions' for w in s['elements'][0]['elements'])]
assert len(idx_c)==1 and len(idx_f)==1, (idx_c,idx_f)
data[idx_c[0]]=new_concl; data[idx_f[0]]=new_faq
print('conclusion paras:',len(paras),'| FAQ items:',len(pairs))
for q,_ in pairs: print(' -',q)
if 'publish' in sys.argv:
    body=json.dumps({'meta':{'_elementor_data':json.dumps(data,ensure_ascii=False),'_elementor_edit_mode':'builder','_elementor_template_type':'wp-post'}}).encode()
    req=urllib.request.Request('https://chatsku.com/wp-json/wp/v2/posts/3798',data=body,method='POST',headers={**H,'Content-Type':'application/json'})
    r=json.load(urllib.request.urlopen(req,timeout=90))
    print('updated',r['id'],r['status'])
    try: urllib.request.urlopen(urllib.request.Request('https://chatsku.com/wp-json/elementor/v1/cache',headers=H,method='DELETE'),timeout=60); print('cache cleared')
    except Exception as e: print('cache err',e)
