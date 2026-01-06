import time
import random
import threading
from database import add_alert, get_devices, add_device, Device, Alert
from datetime import datetime

class PolicyEngine:
    def __init__(self):
        self.running = False
        self.lock = threading.Lock()

    def start(self):
        self.running = True
        print("LOG [AI]: Policy Engine Started (Observe -> Analyze -> Decide -> Act)")
        while self.running:
            self.cycle()
            time.sleep(10)  # Run cycle every 10 seconds for PoC

    def cycle(self):
        # 1. OBSERVE
        devices = get_devices()
        print(f"LOG [AI]: Observing {len(devices)} devices...")

        for device in devices:
            if device.status == "Isolated":
                continue # Skip already isolated devices
            
            # 2. ANALYZE
            # In a real system, we'd analyze packet stats. Here we simulate risk analysis.
            # If risk score is high, we take action.
            risk_score = device.risk_score
            
            # Simulate dynamic risk assessment (random fluctuation for demo)
            # But mostly rely on Honeypot hits (external trigger) or specific rules.
            # Example Rule: If device type is 'Unknown' and risk > 5, flag it.
            
            if device.device_type == "Unknown" and risk_score > 5:
                print(f"LOG [AI]: High risk detected for Unknown device {device.ip_address}")
            
            # 3. DECIDE & ACT
            if risk_score >= 8:
                self.isolate_device(device)
            elif risk_score >= 5:
                self.warn_user(device)

    def isolate_device(self, device: Device):
        print(f"LOG [AI]: [DECISION] ISOLATE device {device.id} (Score: {device.risk_score})")
        device.status = "Isolated"
        add_device(device)
        add_alert(Alert(
            timestamp=str(datetime.now()),
            severity="Critical",
            description=f"Auto-Isolation: Device {device.ip_address} exceeded risk threshold.",
            source="AI_Policy_Engine"
        ))

    def warn_user(self, device: Device):
        # Avoid spamming alerts in real app, simplified for PoC
        print(f"LOG [AI]: [DECISION] WARN user about {device.id}")
        add_alert(Alert(
            timestamp=str(datetime.now()),
            severity="Medium",
            description=f"Suspicious behavior detected from {device.ip_address}.",
            source="AI_Policy_Engine"
        ))

engine = PolicyEngine()

def start_ai_engine():
    engine.start()