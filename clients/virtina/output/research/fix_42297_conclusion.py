"""
Fix conclusion + add woocommerce-development service page link + add missing blog link.
"""
import os, re, requests, urllib3
from dotenv import load_dotenv

urllib3.disable_warnings()
load_dotenv()

WP_BASE = "https://virtina.com"
WP_USER = os.getenv("WP_USERNAME")
WP_PASS = os.getenv("WP_APP_PASSWORD")
POST_ID = 42297

orig_put = requests.put
requests.put = lambda *a, **kw: orig_put(*a, **{**kw, "verify": False})

with open(r"C:\content-intel\clients\virtina\output\research\_42297_fixed.txt", encoding="utf-8") as f:
    content = f.read()
print(f"Loaded {len(content)} chars")

applied = 0

# FIX 1 — Replace bloated 5-paragraph conclusion with tight 2-paragraph version
old_conclusion = '''<div style="background:#00d5c0;border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 id="conclusion" style="color:#ffffff;font-size:30px;">Conclusion</h2>
<p style="color:#ffffff;font-size:16px;line-height:1.75;">B2B buyers at manufacturers and distributors are not abandoning your WooCommerce store because they don't want to buy. They're leaving because your checkout doesn't match how they are required to pay. The fix requires a real implementation decision.</p>
<p style="color:#ffffff;font-size:16px;line-height:1.75;">Plugin-based credit works for known buyer bases at low volume. Financed net terms eliminates your credit risk and pays you upfront. A PO gateway connected to your ERP is the right architecture for manufacturers on formal PO cycles.</p>
<p style="color:#ffffff;font-size:16px;line-height:1.75;">Pick the model that fits your operation, not the one that's easiest to install.</p>
<p style="color:#ffffff;font-size:16px;line-height:1.75;">Getting net terms right means more than choosing a plugin. The credit policy, approval workflow, ERP connection, and dunning sequence must all be in place before the first net terms order lands. That is exactly the kind of implementation Virtina handles for B2B manufacturers and distributors.</p>
<p style="color:#ffffff;font-size:16px;line-height:1.75;">If you're connecting net terms to an ERP or building a multi-tier approval workflow, contact us to talk through your setup.</p>
</div>'''

new_conclusion = '''<div style="background:#00d5c0;border-radius:20px;padding:30px;margin:0 0 28px 0;"><h2 id="conclusion" style="color:#ffffff;font-size:30px;">Conclusion</h2>
<p style="color:#ffffff;font-size:16px;line-height:1.75;">Pick the model that fits your operation. Build the credit policy, approval workflow, and dunning sequence before the first net terms order lands. The implementation determines whether net terms drives revenue or creates credit risk.</p>
<p style="color:#ffffff;font-size:16px;line-height:1.75;">Virtina implements net payment terms for B2B manufacturers and distributors on WooCommerce, from plugin setup through full ERP integration. <a href="https://virtina.com/woocommerce-development/" style="color:#ffffff;text-decoration:underline;">Talk to our WooCommerce team</a> about your setup.</p>
</div>'''

if old_conclusion in content:
    content = content.replace(old_conclusion, new_conclusion, 1)
    print("  APPLIED: Conclusion trimmed from 5 paragraphs to 2 + WooCommerce service link added")
    applied += 1
else:
    print("  MISS: Conclusion block not matched exactly — trying regex")
    pat = re.compile(
        r'<div style="background:#00d5c0[^"]*"[^>]*><h2 id="conclusion".*?</div>',
        re.DOTALL
    )
    new_content, n = pat.subn(new_conclusion, content, count=1)
    if n:
        content = new_content
        print(f"  APPLIED: Conclusion replaced (regex, {n} match)")
        applied += 1
    else:
        print("  MISS: Conclusion regex also failed")

# FIX 2 — Add Volusion-to-WooCommerce migration link in the Introduction section
# Natural hook: the sentence about B2B buyers not working with default checkout
old_intro_link = ('your checkout doesn’t match how they are required to pay. The fix requires a real implementation decision.')
# That's in the old conclusion — it's gone now. Find a natural spot in the body.
# Target: the paragraph about ERP connection in Model C — add volusion migration as related reading
old_model_c_para = ('This model requires an ERP connection and involves the longest DSO of the three. It is the best match for manufacturers and distributors whose enterprise buyers are on formal PO cycles. If you\'re running Model C, your net terms setup is only as good as your <a href="https://virtina.com/woocommerce-erp-integration/" style="outline: none;">WooCommerce ERP integration</a>.')

new_model_c_para = ('This model requires an ERP connection and involves the longest DSO of the three. It is the best match for manufacturers and distributors whose enterprise buyers are on formal PO cycles. If you\'re running Model C, your net terms setup is only as good as your <a href="https://virtina.com/woocommerce-erp-integration/" style="outline: none;">WooCommerce ERP integration</a>. If you’re still on Volusion, read our <a href="https://virtina.com/volusion-to-woocommerce-migration/" style="outline: none;">Volusion to WooCommerce migration guide</a> before planning net terms.')

if old_model_c_para in content:
    content = content.replace(old_model_c_para, new_model_c_para, 1)
    print("  APPLIED: Volusion migration link added in Model C paragraph")
    applied += 1
else:
    # Try with smart apostrophe in "you're"
    old_alt = old_model_c_para.replace("you're", "you’re")
    if old_alt in content:
        new_alt = new_model_c_para.replace("you're", "you’re")
        content = content.replace(old_alt, new_alt, 1)
        print("  APPLIED: Volusion migration link added (smart apostrophe variant)")
        applied += 1
    else:
        print("  MISS: Model C paragraph not found for Volusion link")

print(f"\n{applied} fixes applied")

# Verify
print("\n[LINK COUNT]")
internal = re.findall(r'href="https://virtina\.com/', content)
external = re.findall(r'target="_blank"', content)
woo_dev = 'woocommerce-development' in content
volusion_link = 'volusion-to-woocommerce-migration' in content
print(f"  Internal links: {len(internal)}")
print(f"  External links: {len(external)}")
print(f"  WooCommerce service page linked: {woo_dev}")
print(f"  Volusion migration post linked: {volusion_link}")

print("\n[CONCLUSION CHECK]")
conc = re.search(r'id="conclusion".*?</div>', content, re.DOTALL)
if conc:
    conc_text = re.sub(r'<[^>]+>', '', conc.group())
    words = len(conc_text.split())
    paras = len(re.findall(r'<p ', conc.group()))
    print(f"  Conclusion: {paras} paragraphs, ~{words} words")
    if paras <= 2 and words <= 80:
        print("  PASS: Conclusion is short and tight")
    else:
        print("  WARN: Still long")

print("\n[EM DASH CHECK]")
em = [i+1 for i, l in enumerate(content.split('\n')) if chr(0x2014) in l]
print(f"  Em dashes: {em if em else 'none'}")

with open(r"C:\content-intel\clients\virtina\output\research\_42297_fixed.txt", "w", encoding="utf-8") as f:
    f.write(content)
print(f"\nSaved ({len(content)} chars)")

print(f"PUTting to post {POST_ID}...")
resp = requests.put(
    f"{WP_BASE}/wp-json/wp/v2/posts/{POST_ID}",
    auth=(WP_USER, WP_PASS),
    json={"content": content, "status": "draft"}
)
print(f"HTTP {resp.status_code}")
if resp.status_code in (200, 201):
    print(f"Modified: {resp.json().get('modified', '')}")
    print("DONE")
else:
    print("ERROR:", resp.text[:400])
