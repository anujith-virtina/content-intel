"""
STEP 1: Measure post 42297 against all 10 SEO/LLM content rules.
Reports exact violation counts before any rewrite.
"""
import os, re, sys
import requests, urllib3
from dotenv import load_dotenv

urllib3.disable_warnings()
load_dotenv()

orig_get = requests.get
requests.get = lambda *a, **kw: orig_get(*a, **{**kw, "verify": False})

WP_BASE = "https://virtina.com"
WP_USER = os.getenv("WP_USERNAME")
WP_PASS = os.getenv("WP_APP_PASSWORD")
POST_ID = 42297

# ── FETCH ──────────────────────────────────────────────────────────────────────
resp = requests.get(
    f"{WP_BASE}/wp-json/wp/v2/posts/{POST_ID}?context=edit",
    auth=(WP_USER, WP_PASS)
)
if resp.status_code != 200:
    print(f"FETCH FAILED: {resp.status_code}")
    sys.exit(1)

raw = resp.json()["content"]["raw"]
print(f"Fetched {len(raw)} chars from post {POST_ID}")

# ── HELPERS ────────────────────────────────────────────────────────────────────
SENTENCE_END = re.compile(r'(?<=[.!?])\s+(?=[A-Z"])')

def count_sentences(text):
    text = text.strip()
    if not text:
        return 0
    parts = SENTENCE_END.split(text)
    return max(1, len(parts))

def count_words(text):
    return len(text.split())

def strip_tags(html):
    return re.sub(r'<[^>]+>', '', html)

def extract_paragraphs(html):
    """Extract all <p> tags that are body content (not inside table cells or TOC)."""
    # Get all <p>...</p> blocks
    paras = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
    results = []
    for p in paras:
        text = strip_tags(p).strip()
        if len(text) < 10:  # skip trivial
            continue
        results.append(text)
    return results

def extract_sentences(paragraphs):
    """Flat list of all sentences across all paragraphs."""
    sents = []
    for p in paragraphs:
        for s in SENTENCE_END.split(p.strip()):
            s = s.strip()
            if s:
                sents.append(s)
    return sents

def find_inter_header_blocks(html):
    """Find text blocks between H2/H3 headers and measure word counts."""
    # Split by H2 or H3 tags
    segments = re.split(r'<h[23][^>]*>.*?</h[23]>', html, flags=re.DOTALL)
    blocks = []
    for seg in segments:
        text = strip_tags(seg).strip()
        wc = count_words(text)
        if wc > 50:  # ignore tiny separator segments
            blocks.append(wc)
    return blocks

BANNED_PHRASES = [
    "in today's fast-paced world",
    "it's important to note",
    "when it comes to",
    "in conclusion",
    "let's explore",
    "many businesses find that",
    "in this article, we will",
    "furthermore",
    "moreover",
    "additionally",
    "revolutionary",
    "game-changing",
    "cutting-edge",
    "transform your",
    "unlock value",
    "synergize",
    "delve",
    "leverage",
    "navigate",
    "realm",
    "landscape",
    "ecosystem",
]

# ── MEASURE ────────────────────────────────────────────────────────────────────
content_lower = raw.lower()
paragraphs = extract_paragraphs(raw)
sentences = extract_sentences(paragraphs)
inter_header_blocks = find_inter_header_blocks(raw)

paras_over_3_sent = [(p, count_sentences(p)) for p in paragraphs if count_sentences(p) > 3]
paras_over_60_words = [(p, count_words(p)) for p in paragraphs if count_words(p) > 60]
sents_over_25_words = [(s, count_words(s)) for s in sentences if count_words(s) > 25]
blocks_over_300 = [wc for wc in inter_header_blocks if wc > 300]

banned_found = {}
for phrase in BANNED_PHRASES:
    count = content_lower.count(phrase.lower())
    if count > 0:
        banned_found[phrase] = count

em_dashes = raw.count('—') + raw.count('&mdash;') + raw.count('&#8212;') + raw.count('&#x2014;')

has_faq = 'class="vfaq"' in raw
faq_count = len(re.findall(r'class="vfaq"', raw))
has_table = bool(re.search(r'<table\b', raw))
has_checklist = 'background-color:#43627f;border-radius:50%' in raw
has_example = any(phrase in content_lower for phrase in [
    'a typical pattern', 'a pattern common', 'for example', 'for instance',
    'one distributor', 'a wholesale operator'
])
has_infographic = 'infographic' in content_lower
body_images = re.findall(r'data-id="4229[3-5]"', raw)
featured_images = re.findall(r'data-id="42292"', raw)
internal_links = re.findall(r'<a\s[^>]*href="https://virtina\.com/', raw)
external_links = re.findall(r'<a\s[^>]*href="https?://(?!virtina\.com)[^"]+"\s[^>]*target="_blank"', raw)

total_text = strip_tags(raw)
total_words = count_words(total_text)

# ── REPORT ─────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("STEP 1 MEASUREMENT — POST 42297")
print("="*60)
print(f"\nTotal words:               {total_words}")
print(f"Total <p> count:           {len(paragraphs)}")
print(f"\n--- VIOLATIONS ---")
print(f"paragraphs_over_3_sentences: {len(paras_over_3_sent)}")
for p, n in paras_over_3_sent[:5]:
    print(f"  [{n} sent] {p[:80]}...")
print(f"\nparagraphs_over_60_words:    {len(paras_over_60_words)}")
for p, n in paras_over_60_words[:5]:
    print(f"  [{n} words] {p[:80]}...")
print(f"\nsentences_over_25_words:     {len(sents_over_25_words)}")
for s, n in sents_over_25_words[:8]:
    print(f"  [{n}w] {s[:100]}")
print(f"\nheader_blocks_over_300_words: {len(blocks_over_300)}")
for wc in blocks_over_300:
    print(f"  [{wc} words]")
print(f"\nbanned_phrase_occurrences:   {sum(banned_found.values())}")
for phrase, cnt in banned_found.items():
    print(f"  '{phrase}' x{cnt}")
print(f"\nem_dash_count:               {em_dashes}")
print(f"\n--- MANDATORY INCLUSIONS ---")
print(f"FAQ section:         {'YES (' + str(faq_count) + ' Q&As)' if has_faq else 'NO'}")
print(f"Comparison table:    {'YES' if has_table else 'NO'}")
print(f"Checklist:           {'YES' if has_checklist else 'NO'}")
print(f"Example/snippet:     {'YES' if has_example else 'NO'}")
print(f"Infographic:         {'YES' if has_infographic else 'NO'}")
print(f"Featured image:      {'YES' if featured_images else 'NO'}")
print(f"Body images:         {len(body_images)} (of 42293-42295)")
print(f"Internal links:      {len(internal_links)}")
print(f"External links:      {len(external_links)}")

print("\n--- ALL SENTENCES > 25 WORDS ---")
for s, n in sents_over_25_words:
    print(f"  [{n}w] {s}")
