from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "tracking.db"

def _connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("""
      CREATE TABLE IF NOT EXISTS dispatches(
        id INTEGER PRIMARY KEY,
        tracking_id TEXT NOT NULL UNIQUE,
        order_id TEXT NOT NULL,
        recipient TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
      )
    """)
    return conn

def register(tracking_id: str, order_id: str, recipient: str, status="PREPARED"):
    now = datetime.now().isoformat(timespec="seconds")
    with _connect() as conn:
        conn.execute(
            """INSERT INTO dispatches(tracking_id,order_id,recipient,status,created_at,updated_at)
               VALUES(?,?,?,?,?,?)
               ON CONFLICT(tracking_id) DO UPDATE SET status=excluded.status,updated_at=excluded.updated_at""",
            (tracking_id, order_id, recipient, status, now, now),
        )

def list_recent(limit=100):
    with _connect() as conn:
        return [dict(row) for row in conn.execute("SELECT * FROM dispatches ORDER BY id DESC LIMIT ?", (limit,))]
