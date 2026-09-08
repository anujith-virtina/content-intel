# -*- coding: utf-8 -*-
"""Audit 1: do real B2B distributor catalogs let AI agents in at all?

Reads each site's robots.txt and records the rule that applies to each named AI
crawler. Public data, one request per host. No crawling beyond robots.txt.

Result feeds the ChatSKU post on what actually happens when AI agents meet a real
B2B catalog. Every number in that post has to come from a run of this file.
"""
import urllib.request, urllib.error, re, json, io, time, sys

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

# Real, public B2B distributor and manufacturer catalogs. Not ChatSKU competitors.
SITES = [
    "grainger.com", "mcmaster.com", "fastenal.com", "mscdirect.com",
    "motionindustries.com", "applied.com", "zoro.com", "globalindustrial.com",
    "digikey.com", "mouser.com", "newark.com", "alliedelec.com",
    "ferguson.com", "wesco.com", "borderstates.com", "rexelusa.com",
    "hisco.com", "kaman.com", "genuineparts.com", "sonepar.com",
]

# The agents that actually matter for agentic commerce right now.
AGENTS = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-User",
          "PerplexityBot", "Perplexity-User", "Google-Extended", "CCBot",
          "Amazonbot", "Bytespider", "meta-externalagent"]


def fetch(url, timeout=30):
    r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=timeout)
    return r.status, r.read().decode("utf-8", "ignore")


def parse_groups(txt):
    """robots.txt -> {user-agent(lower): [rule lines]}"""
    groups, current = {}, []
    for raw in txt.splitlines():
        line = raw.split("#")[0].strip()
        if not line:
            continue
        if ":" not in line:
            continue
        field, value = line.split(":", 1)
        field, value = field.strip().lower(), value.strip()
        if field == "user-agent":
            ua = value.lower()
            if ua not in groups:
                groups[ua] = []
            current = groups[ua]
        elif field in ("disallow", "allow") and current is not None:
            current.append((field, value))
    return groups


def verdict(groups, agent):
    """What this robots.txt says for one agent. Explicit rules beat the wildcard."""
    a = agent.lower()
    if a in groups:
        rules = groups[a]
        if any(f == "disallow" and v == "/" for f, v in rules):
            return "BLOCKED"
        if not rules:
            return "allowed (empty group)"
        return "allowed with path limits" if rules else "allowed"
    if "*" in groups:
        rules = groups["*"]
        if any(f == "disallow" and v == "/" for f, v in rules):
            return "blocked by wildcard"
        return "not named, wildcard applies"
    return "not named, no wildcard"


def main():
    out = {}
    for host in SITES:
        rec = {"host": host}
        got = None
        for scheme in ("https://www.", "https://"):
            try:
                st, txt = fetch(scheme + host + "/robots.txt")
                if st == 200 and len(txt) < 400000:
                    got = txt
                    rec["robots_url"] = scheme + host + "/robots.txt"
                    break
            except Exception as e:
                rec["error"] = repr(e)[:80]
            time.sleep(1)
        if got is None:
            rec["status"] = "unreachable"
            out[host] = rec
            print(f"{host:24} UNREACHABLE {rec.get('error','')[:50]}")
            time.sleep(2)
            continue
        groups = parse_groups(got)
        rec["bytes"] = len(got)
        rec["named_agents"] = sorted(g for g in groups if g != "*")
        rec["verdicts"] = {a: verdict(groups, a) for a in AGENTS}
        blocked = [a for a in AGENTS if rec["verdicts"][a] in ("BLOCKED", "blocked by wildcard")]
        rec["blocked_count"] = len(blocked)
        rec["blocked"] = blocked
        out[host] = rec
        print(f"{host:24} {len(got):6}B  ua-groups={len(groups):3}  AI agents blocked: "
              f"{len(blocked):2}/{len(AGENTS)}  {','.join(blocked[:5])}")
        time.sleep(2)

    io.open(r"C:\content-intel\clients\chatsku\output\research\agent_audit_robots.json",
            "w", encoding="utf-8").write(json.dumps(out, indent=1))
    ok = [r for r in out.values() if "verdicts" in r]
    print(f"\nreachable: {len(ok)}/{len(SITES)}")
    if ok:
        for a in AGENTS:
            n = sum(1 for r in ok if r["verdicts"][a] in ("BLOCKED", "blocked by wildcard"))
            print(f"   {a:20} blocked on {n}/{len(ok)} catalogs")


if __name__ == "__main__":
    main()
