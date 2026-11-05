"""Route urllib.request.urlopen through curl (Cloudflare 403s Python's TLS fingerprint, curl passes)."""
import subprocess, tempfile, os, io, urllib.request, urllib.error
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

class _Resp(io.BytesIO):
    def __init__(self, b, status): super().__init__(b); self.status = status
    def __enter__(self): return self
    def __exit__(self, *a): return False

def urlopen(req, timeout=60, **kw):
    if isinstance(req, str): req = urllib.request.Request(req)
    cmd = ["curl", "-s", "-S", "--max-time", str(int(timeout)), "-X", req.get_method(), "-w", "\n%{http_code}", req.full_url]
    hdrs = dict(req.header_items())
    hdrs.setdefault("User-Agent", UA)
    if hdrs.get("User-agent"): hdrs["User-Agent"] = UA
    hdrs.pop("User-agent", None)
    for k, v in hdrs.items(): cmd += ["-H", f"{k}: {v}"]
    tmp = None
    if req.data is not None:
        tmp = tempfile.NamedTemporaryFile(delete=False); tmp.write(req.data); tmp.close()
        cmd += ["--data-binary", "@" + tmp.name]
    try:
        out = subprocess.run(cmd, capture_output=True, timeout=timeout + 30).stdout
    finally:
        if tmp: os.unlink(tmp.name)
    body, _, code = out.rpartition(b"\n")
    code = int(code or 0)
    if code >= 400 or code == 0:
        raise urllib.error.HTTPError(req.full_url, code, "curl", {}, io.BytesIO(body))
    return _Resp(body, code)

urllib.request.urlopen = urlopen
