# SmartHome Shield - Agentic AI IoT Security

A Proof of Concept (PoC) for an edge-based IoT security system powered by Agentic AI.
Designed to detect threats, deploy deception (honeypots), and provide real-time visibility via a mobile app.

## Project Structure
- `backend/`: FastAPI application (Edge Core + Policy Engine + Honeypots)
- `mobile/`: Expo React Native Application (User Dashboard)

## Features
- **Agentic AI Policy Engine**: Observe -> Analyze -> Decide -> Act loop.
- **Deception Layer**: Simulated SSH (Port 2222) and HTTP (Port 8080) honeypots.
- **Mobile Dashboard**: View devices, system status, and security alerts.
- **Autonomous Response**: AI automatically isolates high-risk devices.

## Setup Instructions

### Backend (Edge Core)
1. Navigate to `backend/`.
2. Create virtual env: `python -m venv venv`.
3. Install dependencies: `.\venv\Scripts\pip install -r requirements.txt`.
4. Run the server: `.\venv\Scripts\python -m uvicorn main:app --reload --port 8000`.

### Mobile App
1. Navigate to `mobile/`.
2. Install dependencies: `npm install`.
3. Start Expo: `npx expo start`.
4. Scan QR code (if on Android/iOS) or press `w` for Web.

## Demo / Simulation
To simulate traffic and attacks:
1. Ensure backend is running.
2. Run the simulation script:
   ```powershell
   cd backend
   ..\venv\Scripts\python demo_attack.py
   ```
3. Check the Mobile App "Alerts" tab or the "System Status".
4. You will see "Honeypot Triggered" alerts and high-risk devices.

## Architecture
- **Edge**: Python FastAPI + SQLite.
- **AI**: Custom Python class implementing decision loop.
- **Mobile**: React Native + Expo Router.