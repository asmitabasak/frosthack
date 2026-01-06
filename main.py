from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import init_db, get_devices, get_alerts, add_device, add_alert, Device, Alert
import threading
import time
import random 

from core.engine import start_ai_engine
from core.honeypots import start_honeypots

app = FastAPI(title="SmartHome Shield Edge API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()
    threading.Thread(target=start_ai_engine, daemon=True).start()
    threading.Thread(target=start_honeypots, daemon=True).start()
    print("SmartHome Shield Security Core Started")

@app.get("/")
def read_root():
    return {"status": "running", "system": "SmartHome Shield"}

@app.get("/devices", response_model=list[Device])
def list_devices():
    return get_devices()

@app.get("/alerts", response_model=list[Alert])
def list_alerts():
    return get_alerts()

@app.post("/device/{device_id}/isolate")
def isolate_device(device_id: str):
    # Logic to isolate device (mocked for now)
    # 1. Update DB status
    # 2. Add Firewall rule
    devices = get_devices()
    target = next((d for d in devices if d.id == device_id), None)
    if not target:
        raise HTTPException(status_code=404, detail="Device not found")
    
    target.status = "Isolated"
    add_device(target) # Update
    
    # Log alert
    add_alert(Alert(
        timestamp=str(datetime.now()),
        severity="High",
        description=f"Device {device_id} manually isolated by user",
        source="MobileApp"
    ))
    return {"status": "isolated", "device_id": device_id}

# --- Simulation Endpoints (For usage in PoC) ---
from datetime import datetime

@app.post("/simulate/traffic")
def simulate_traffic():
    # Helper to generate fake traffic for demo
    # Create a random device
    dev_id = f"dev_{random.randint(1000, 9999)}"
    new_device = Device(
        id=dev_id,
        ip_address=f"192.168.1.{random.randint(2, 254)}",
        device_type=random.choice(["Camera", "Thermostat", "SmartBulb", "Speaker"]),
        risk_score=random.randint(0, 10),
        status="Active"
    )
    add_device(new_device)
    return {"message": "Simulated device traffic", "device": new_device}