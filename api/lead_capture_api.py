#!/usr/bin/env python3
"""Local-only lead capture API for the bizElev8 marketing site.

It intentionally has no email transport. A lead is accepted only after it has
been durably stored with its audit event in one SQLite transaction. Email
delivery can be enabled later with company-owned SMTP credentials.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
import time
import uuid
from collections import defaultdict, deque
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock

HOST = os.environ.get("LEAD_CAPTURE_HOST", "127.0.0.1")
PORT = int(os.environ.get("LEAD_CAPTURE_PORT", "3900"))
DATA_DIR = Path(os.environ.get("LEAD_CAPTURE_DATA_DIR", "/var/lib/bizelev8-leads"))
MAX_BODY = 8192
WINDOW_SECONDS = 600
LIMITS = {"demo": 5, "partner": 3, "newsletter": 10}
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
FORM_TYPES = set(LIMITS)
rate_lock = Lock()
rates: dict[tuple[str, str], deque[float]] = defaultdict(deque)


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def setup_storage() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(DATA_DIR, 0o700)
    with sqlite3.connect(DATA_DIR / "leads.db") as db:
        db.execute("""CREATE TABLE IF NOT EXISTS leads (
          id TEXT PRIMARY KEY, form_type TEXT NOT NULL, name TEXT, email TEXT NOT NULL,
          company TEXT, team_size TEXT, industry TEXT, goal TEXT, country TEXT,
          partnership_type TEXT, message TEXT, ip_hash TEXT NOT NULL,
          created_at TEXT NOT NULL, user_agent TEXT, consent INTEGER NOT NULL
        )""")
        db.execute("CREATE INDEX IF NOT EXISTS idx_leads_created ON leads(created_at)")
        db.execute("CREATE INDEX IF NOT EXISTS idx_leads_email ON leads(email)")
        db.execute("""CREATE TABLE IF NOT EXISTS audit_events (
          event_id INTEGER PRIMARY KEY AUTOINCREMENT, lead_id TEXT NOT NULL,
          event_type TEXT NOT NULL, created_at TEXT NOT NULL,
          FOREIGN KEY(lead_id) REFERENCES leads(id)
        )""")


def clean(value: object, maximum: int = 1000) -> str:
    if not isinstance(value, str):
        return ""
    return "".join(ch for ch in value.strip() if ch >= " " and ch != "\x7f")[:maximum]


def validate(form_type: str, body: dict) -> tuple[dict | None, str | None]:
    email = clean(body.get("email"), 254).lower()
    if not EMAIL_RE.fullmatch(email):
        return None, "email"
    result = {"email": email, "consent": body.get("consent") is True}
    if not result["consent"]:
        return None, "consent"
    required = ["name", "company"] if form_type in {"demo", "partner"} else []
    for field in required:
        value = clean(body.get(field), 100)
        if len(value) < 2:
            return None, field
        result[field] = value
    for field, limit in (("teamSize", 40), ("industry", 100), ("goal", 100), ("country", 100), ("partnershipType", 100), ("message", 1000)):
        result[field] = clean(body.get(field), limit)
    return result, None


def limited(ip: str, form_type: str) -> bool:
    moment = time.monotonic()
    key = (ip, form_type)
    with rate_lock:
        queue = rates[key]
        while queue and queue[0] <= moment - WINDOW_SECONDS:
            queue.popleft()
        if len(queue) >= LIMITS[form_type]:
            return True
        queue.append(moment)
    return False


def append_jsonl(name: str, record: dict) -> None:
    path = DATA_DIR / name
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, separators=(",", ":")) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.chmod(path, 0o600)


def save_lead(form_type: str, lead: dict, ip: str, user_agent: str) -> str:
    identifier = str(uuid.uuid4())
    record = {
        "id": identifier, "form_type": form_type, "name": lead.get("name", ""),
        "email": lead["email"], "company": lead.get("company", ""),
        "team_size": lead.get("teamSize", ""), "industry": lead.get("industry", ""),
        "goal": lead.get("goal", ""), "country": lead.get("country", ""),
        "partnership_type": lead.get("partnershipType", ""), "message": lead.get("message", ""),
        "ip_hash": hashlib.sha256(ip.encode()).hexdigest(), "created_at": now_iso(),
        "user_agent": user_agent[:160], "consent": int(lead["consent"]),
    }
    # Lead and audit record are one SQLite transaction, so a successful response
    # cannot create a lead without its audit event (or vice versa).
    with sqlite3.connect(DATA_DIR / "leads.db") as db:
        db.execute("""INSERT INTO leads VALUES (:id,:form_type,:name,:email,:company,:team_size,
          :industry,:goal,:country,:partnership_type,:message,:ip_hash,:created_at,:user_agent,:consent)""", record)
        db.execute("INSERT INTO audit_events(lead_id,event_type,created_at) VALUES(?,?,?)",
                   (identifier, "lead_created", record["created_at"]))
    return identifier


class Handler(BaseHTTPRequestHandler):
    server_version = "Bizelev8LeadCapture/1.0"

    def log_message(self, format: str, *args: object) -> None:
        return

    def respond(self, status: int, body: dict) -> None:
        encoded = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self) -> None:
        if self.path == "/api/health":
            return self.respond(200, {"status": "ok", "email_delivery": "disabled"})
        self.respond(404, {"error": "not_found"})

    def do_POST(self) -> None:
        match = re.fullmatch(r"/api/leads/(demo|partner|newsletter)", self.path)
        if not match:
            return self.respond(404, {"error": "not_found"})
        if self.headers.get("Content-Length") is None or int(self.headers.get("Content-Length", "0")) > MAX_BODY:
            return self.respond(413, {"error": "payload_too_large"})
        try:
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        except (ValueError, UnicodeDecodeError):
            return self.respond(400, {"error": "invalid_json"})
        if not isinstance(body, dict):
            return self.respond(400, {"error": "invalid_payload"})
        form_type, ip = match.group(1), self.client_address[0]
        if limited(ip, form_type):
            return self.respond(429, {"error": "rate_limited", "retry_after_seconds": WINDOW_SECONDS})
        if clean(body.get("_hp"), 100):
            append_jsonl("spam.ndjson", {"created_at": now_iso(), "form_type": form_type, "reason": "honeypot"})
            return self.respond(202, {"status": "accepted"})
        loaded_at = body.get("loaded_at")
        if not isinstance(loaded_at, (int, float)) or time.time() - loaded_at < 2:
            return self.respond(400, {"error": "invalid_submission"})
        user_agent = clean(self.headers.get("User-Agent"), 160)
        if not user_agent:
            return self.respond(400, {"error": "invalid_submission"})
        lead, field = validate(form_type, body)
        if field:
            return self.respond(400, {"error": "invalid_field", "field": field})
        identifier = save_lead(form_type, lead, ip, user_agent)
        self.respond(201, {"id": identifier, "status": "created"})


if __name__ == "__main__":
    setup_storage()
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
