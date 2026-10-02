#!/usr/bin/env python3
"""No-email integration tests for lead_capture_api.py."""
from __future__ import annotations
import json, os, subprocess, sys, tempfile, time, urllib.error, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PORT = "3911"

def request(path, payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(f"http://127.0.0.1:{PORT}{path}", data=data, headers={"Content-Type":"application/json", "User-Agent":"lead-capture-test/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=3) as res:
            return res.status, json.loads(res.read())
    except urllib.error.HTTPError as err:
        return err.code, json.loads(err.read())

with tempfile.TemporaryDirectory() as temp:
    env = os.environ | {"LEAD_CAPTURE_PORT": PORT, "LEAD_CAPTURE_DATA_DIR": temp}
    proc = subprocess.Popen([sys.executable, str(ROOT / "lead_capture_api.py")], env=env)
    try:
        for _ in range(30):
            try:
                if request("/api/health")[0] == 200: break
            except OSError: time.sleep(.1)
        assert request("/api/health") == (200, {"status":"ok", "email_delivery":"disabled"})
        base = {"email":"lead@example.com", "loaded_at":time.time()-3, "_hp":""}
        status, payload = request("/api/leads/newsletter", base | {"consent":True})
        assert status == 201 and payload["status"] == "created"
        assert (Path(temp) / "leads.db").is_file()
        assert request("/api/leads/newsletter", base | {"_hp":"bot"})[0] == 202
        assert request("/api/leads/demo", base | {"name":"A", "company":"B", "consent":True})[0] == 400
        assert request("/api/leads/demo", base | {"name":"Ada Lee", "company":"Acme", "consent":"yes"})[0] == 400
        assert request("/api/leads/demo", base | {"name":"Ada Lee", "company":"Acme", "consent":True})[0] == 201
        assert request("/api/leads/partner", base | {"name":"Ada Lee", "company":"Acme", "consent":False})[0] == 400
        assert request("/api/leads/newsletter", base | {"consent":False})[0] == 400
    finally:
        proc.terminate(); proc.wait(timeout=5)
print("lead capture integration tests passed (no email sent)")
