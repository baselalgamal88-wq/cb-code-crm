#!/usr/bin/env python3
"""Encrypt a daily market brief for the app.

Team brief (everyone signed in sees it):
  MARKET_KEY=<base64 key> python3 tools/market_encrypt.py brief.json
  -> market/<date>.bin and market/latest.bin, and the date is added to market/index.json
Managers-only part (only Basel sees it, e.g. notes from the internal Leaders & Managers group):
  MARKET_MGR_KEY=<base64 key> python3 tools/market_encrypt.py --managers managers.json
  -> market/<date>.mgr.bin and market/latest.mgr.bin

Files are AES-256-GCM (12-byte IV + ciphertext). Keys are never stored in this repository:
the app reads the team key from Firestore settings/market (signed-in team only) and the
managers key from admin/market (Basel only).
"""
import base64, json, os, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def main():
    args = sys.argv[1:]
    mgr = bool(args) and args[0] == "--managers"
    if mgr: args = args[1:]
    env = "MARKET_MGR_KEY" if mgr else "MARKET_KEY"
    if len(args) != 1 or not os.environ.get(env):
        sys.exit("usage: MARKET_KEY=... market_encrypt.py brief.json | MARKET_MGR_KEY=... market_encrypt.py --managers managers.json")
    key = base64.b64decode(os.environ[env])
    raw = open(args[0], "rb").read()
    doc = json.loads(raw)  # must be valid JSON with a "date" (YYYY-MM-DD)
    date = doc["date"]
    iv = os.urandom(12)
    blob = iv + AESGCM(key).encrypt(iv, json.dumps(doc, ensure_ascii=False).encode("utf-8"), None)
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "market")
    ext = ".mgr.bin" if mgr else ".bin"
    for name in (date + ext, "latest" + ext):
        open(os.path.join(root, name), "wb").write(blob)
    if mgr:
        print("wrote managers part", date, len(blob), "bytes")
        return
    ip = os.path.join(root, "index.json")
    idx = json.load(open(ip)) if os.path.exists(ip) else {"dates": []}
    idx["dates"] = sorted(set(idx.get("dates", []) + [date]), reverse=True)[:60]
    json.dump(idx, open(ip, "w"), indent=1)
    print("wrote", date, len(blob), "bytes")

if __name__ == "__main__":
    main()
