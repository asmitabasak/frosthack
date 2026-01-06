import socket
import threading
from datetime import datetime
from database import add_alert, Alert, get_devices, add_device, Device

# Mock honeypot services
# In a real RPi environment, specific ports like 22, 23, 80 would be redirected here.
# For PoC/Windows, we bind to high ports 2222 (SSH), 8080 (HTTP).

class HoneypotManager:
    def __init__(self):
        self.running = False
    
    def start(self):
        self.running = True
        threading.Thread(target=self.start_ssh_honeypot, daemon=True).start()
        threading.Thread(target=self.start_http_honeypot, daemon=True).start()
        print("LOG [Honeypot]: Services Started (SSH:2222, HTTP:8080)")

    def start_ssh_honeypot(self):
        host = '0.0.0.0'
        port = 2222
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((host, port))
            s.listen(5)
            while self.running:
                client_sock, address = s.accept()
                print(f"LOG [Honeypot]: SSH Connection attempt from {address}")
                self.log_attack(address[0], "SSH", "Attempted login on honeypot port 2222")
                client_sock.close()
        except Exception as e:
            print(f"LOG [Honeypot]: SSH Error {e}")

    def start_http_honeypot(self):
        host = '0.0.0.0'
        port = 8080
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((host, port))
            s.listen(5)
            while self.running:
                client_sock, address = s.accept()
                request = client_sock.recv(1024).decode('utf-8', errors='ignore')
                print(f"LOG [Honeypot]: HTTP Request from {address}")
                self.log_attack(address[0], "HTTP", f"Suspicious HTTP Request")
                
                # Send fake response
                response = "HTTP/1.1 200 OK\n\n<html><body>Login Page</body></html>"
                client_sock.sendall(response.encode('utf-8'))
                client_sock.close()
        except Exception as e:
            print(f"LOG [Honeypot]: HTTP Error {e}")

    def log_attack(self, ip, service, desc):
        # 1. Alert
        add_alert(Alert(
            timestamp=str(datetime.now()),
            severity="High",
            description=f"Honeypot Triggered ({service}) by {ip}: {desc}",
            source="Honeypot"
        ))
        
        # 2. Update Risk Score of device if known
        devices = get_devices()
        target = next((d for d in devices if d.ip_address == ip), None)
        if target:
            target.risk_score = 10 # Instant max risk
            target.status = "Flagged"
            add_device(target)
            print(f"LOG [Honeypot]: Existing device {target.id} flagged as attacker!")
        else:
            # Register new "Attacker" device
            new_dev = Device(
                id=f"attacker_{ip}",
                ip_address=ip,
                device_type="Unknown/Attacker",
                risk_score=10,
                status="Flagged"
            )
            add_device(new_dev)
            print(f"LOG [Honeypot]: New attacker registered {ip}")

manager = HoneypotManager()

def start_honeypots():
    manager.start()