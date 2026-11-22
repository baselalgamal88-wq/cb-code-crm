#!/usr/bin/env python3
"""Encrypt a daily market brief for the app.

Usage: MARKET_KEY=<base64 key> python3 tools/market_encrypt.py brief.json
Writes market/<date>.bin and market/latest.bin (AES-256-GCM: 12-byte IV + ciphertext)
and adds the date to market/index.json. The key is never stored in this repository:
the app reads it from Firestore (settings/market), which only signed-in team members can read.
"""
import base64, json, os, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def main():
    if len(sys.argv) != 2 or not os.environ.get("MARKET_KEY"):
        sys.exit("usage: MARKET_KEY=... python3 tools/market_encrypt.py brief.json")
    key = base64.b64decode(os.environ["MARKET_KEY"])
    raw = open(sys.argv[1], "rb").read()
    doc = json.loads(raw)  # must be valid JSON with a "date" (YYYY-MM-DD)
    date = doc["date"]
    iv = os.urandom(12)
    blob = iv + AESGCM(key).encrypt(iv, json.dumps(doc, ensure_ascii=False).encode("utf-8"), None)
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "market")
    for name in (date + ".bin", "latest.bin"):
        open(os.path.join(root, name), "wb").write(blob)
    ip = os.path.join(root, "index.json")
    idx = json.load(open(ip)) if os.path.exists(ip) else {"dates": []}
    idx["dates"] = sorted(set(idx.get("dates", []) + [date]), reverse=True)[:60]
    json.dump(idx, open(ip, "w"), indent=1)
    print("wrote", date, len(blob), "bytes")

if __name__ == "__main__":
    main()
