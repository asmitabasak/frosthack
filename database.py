import sqlite3
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

DATABASE_NAME = "smarthome.db"

def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS devices
                 (id TEXT PRIMARY KEY, ip_address TEXT, device_type TEXT, risk_score INTEGER, status TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS alerts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, severity TEXT, description TEXT, source TEXT)''')
    conn.commit()
    conn.close()

# --- Pydantic Models ---
class Device(BaseModel):
    id: str
    ip_address: str
    device_type: str = "Unknown"
    risk_score: int = 0
    status: str = "Active"

class Alert(BaseModel):
    id: Optional[int] = None
    timestamp: str
    severity: str
    description: str
    source: str

# --- CRUD Operations ---
def add_device(device: Device):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT OR REPLACE INTO devices VALUES (?, ?, ?, ?, ?)",
                  (device.id, device.ip_address, device.device_type, device.risk_score, device.status))
        conn.commit()
    finally:
        conn.close()

def get_devices() -> List[Device]:
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM devices")
    rows = c.fetchall()
    conn.close()
    return [Device(id=row[0], ip_address=row[1], device_type=row[2], risk_score=row[3], status=row[4]) for row in rows]

def add_alert(alert: Alert):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO alerts (timestamp, severity, description, source) VALUES (?, ?, ?, ?)",
                  (alert.timestamp, alert.severity, alert.description, alert.source))
        conn.commit()
    finally:
        conn.close()

def get_alerts() -> List[Alert]:
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM alerts ORDER BY id DESC LIMIT 50")
    rows = c.fetchall()
    conn.close()
    return [Alert(id=row[0], timestamp=row[1], severity=row[2], description=row[3], source=row[4]) for row in rows]