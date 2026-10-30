# -*- coding: utf-8 -*-
"""Standalone readability report for a ChatSKU draft.

Same maths as the gate inside build_ai_replace_reps_post.py, but it prints the
offending sentences instead of stopping at the first failure, so a draft can be
fixed in one pass rather than one sentence at a time.

Thresholds are calibrated against the live ChatSKU corpus (2026-09-18), not
guessed: median Flesch across 38 posts is 61.9, the best plain-language posts
reach 71-75 (ai-chatbot-buyers-guide 75.2, what-is-agentic-commerce 74.1).

Run:  python readability_check.py <draft.md>
"""
import re, sys, html as _html

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

FLESCH_MIN = 70.0
ASL_MAX = 15.0
SENT_MAX = 25

TOO_TECHNICAL = [r"\bembedding", r"\bvector\b", r"\bretrieval", r"\bRAG\b", r"\bBM25\b",
                 r"\bschema\b", r"\bAPI\b", r"\bendpoint", r"\bJSON\b", r"\bparse",
                 r"\bmachine-readable", r"\blatency", r"\binference", r"\bLLM\b",
                 r"\balgorithm", r"\btaxonom", r"\bnormalis|\bnormaliz", r"\bmiddleware",
                 r"\bwebhook", r"\bstructured data", r"\bingest"]


def syllables(word):
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    return max(1, len(re.findall(r"[aeiouy]{1,2}", w)))


def main(path):
    raw = open(path, encoding="utf-8").read()
    raw = re.sub(r"^---.*?---\s*", "", raw, count=1, flags=re.S)
    raw = re.split(r"\n##\s*Publishing (?:notes|metadata)", raw)[0]
    raw = re.sub(r"<!--.*?-->", " ", raw, flags=re.S)
    raw = re.sub(r"^\[[A-Z][^\]]*\]\s*$", "", raw, flags=re.M)

    # Tables, lists and headings are structure, not prose. Counting them drags the
    # average around and hides the sentences that actually need fixing.
    prose = re.sub(r"<(table|ul|ol)[^>]*>.*?</\1>", " ", raw, flags=re.S | re.I)
    prose = re.sub(r"<h[1-6][^>]*>.*?</h[1-6]>", " ", prose, flags=re.S | re.I)
    prose = _html.unescape(re.sub(r"<[^>]+>", " ", prose))
    prose = re.sub(r"\s+", " ", prose).strip()

    # `(?<=[.!?])\s+` never splits on `." It's`: the char before the space is the
    # quote, not the period. That false-positived a 28-word 'sentence' that was three.
    sents = [s.strip() for s in re.split(r'(?:(?<=[.!?])|(?<=[.!?]")|(?<=[.!?]\u201d))\s+', prose)
             if len(s.split()) >= 3]
    words = re.findall(r"[A-Za-z']+", prose)
    if not sents or not words:
        print("no prose found")
        return 1
    syl = sum(syllables(w) for w in words)
    asl = len(words) / len(sents)
    asw = syl / len(words)
    flesch = 206.835 - 1.015 * asl - 84.6 * asw

    print(f"words {len(words)} | sentences {len(sents)}")
    print(f"Flesch Reading Ease : {flesch:6.1f}   (need >= {FLESCH_MIN})")
    print(f"avg sentence length : {asl:6.1f}   (need <= {ASL_MAX})")
    print(f"avg syllables/word  : {asw:6.2f}")

    fails = 0
    if flesch < FLESCH_MIN:
        fails += 1
        print(f"\nFAIL Flesch {flesch:.1f} < {FLESCH_MIN}")
    if asl > ASL_MAX:
        fails += 1
        print(f"\nFAIL average sentence {asl:.1f} > {ASL_MAX}")

    long_s = [s for s in sents if len(s.split()) > SENT_MAX]
    if long_s:
        fails += 1
        print(f"\nFAIL {len(long_s)} sentence(s) over {SENT_MAX} words:")
        for s in long_s:
            print(f"  [{len(s.split()):2d}] {s}")

    tech = sorted({m.group(0) for p in TOO_TECHNICAL for m in re.finditer(p, raw, re.I)})
    if tech:
        fails += 1
        print(f"\nFAIL technical vocabulary: {tech}")

    # Not blocking, but the words most likely to be worth swapping.
    poly = sorted({w.lower() for w in words if syllables(w) >= 5})
    if poly:
        print(f"\nlong words to review ({len(poly)}): {', '.join(poly[:20])}")

    # The 15 longest sentences, so a near-miss draft can be tightened deliberately.
    print("\nlongest sentences:")
    for s in sorted(sents, key=lambda x: -len(x.split()))[:15]:
        print(f"  [{len(s.split()):2d}] {s[:120]}")

    print("\n" + ("PASS" if not fails else f"{fails} CHECK(S) FAILED"))
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
