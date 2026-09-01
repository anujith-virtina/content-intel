import re

with open(r"C:\content-intel\clients\virtina\output\research\_42297_fixed.txt", encoding="utf-8") as f:
    c = f.read()

# PAA-2: find paragraph starting with "They refer"
idx = c.find("They refer to the same concept")
if idx >= 0:
    chunk = c[idx:idx+600]
    print("PAA-2 para repr:")
    print(repr(chunk[:400]))
    print()

# FAQ-2: find answer inside the 'different customer groups' FAQ
idx2 = c.find("Can I offer different net terms")
if idx2 >= 0:
    chunk2 = c[idx2:idx2+1200]
    ans_start = chunk2.find("vfaq-answer")
    if ans_start >= 0:
        ans = chunk2[ans_start:ans_start+600]
        print("FAQ-2 answer repr:")
        print(repr(ans[:400]))
