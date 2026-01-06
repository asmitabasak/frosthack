import requests
import socket
import time

API_URL = "http://localhost:8000"

def simulate_safe_traffic():
    print("Simulating benign traffic...")
    try:
        res = requests.post(f"{API_URL}/simulate/traffic")
        print(f"Safe Traffic: {res.json()}")
    except Exception as e:
        print(f"Error simulating traffic: {e}")

def simulate_ssh_attack():
    print("Simulating SSH Brute Force Attack on Honeypot (Port 2222)...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost', 2222))
        s.close()
        print("Attack sent!")
    except Exception as e:
        print(f"SSH Attack failed: {e}")

def simulate_http_attack():
    print("Simulating Malicious HTTP Request on Honeypot (Port 8080)...")
    try:
        requests.get("http://localhost:8080/admin/login?payload=malicious")
        print("HTTP Attack sent!")
    except Exception as e:
        print(f"HTTP Attack failed: {e}")

if __name__ == "__main__":
    print("--- Starting Simulation ---")
    simulate_safe_traffic()
    time.sleep(1)
    simulate_ssh_attack()
    time.sleep(1)
    simulate_http_attack()
    print("--- Simulation Complete ---")
    print("Check Mobile App or GET /alerts to verify.")