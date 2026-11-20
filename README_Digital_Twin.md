# Localhost Web Digital Twin Dashboard

**Location:** `G:\1. 2026-2027\1. Project Work\3. Durga\15. Camreea robot\Digital_Twin_Dashboard\`

---

## 1. Overview
This is a **Single-Window Web Digital Twin Dashboard** designed to run locally on your laptop / PC.

* **ZERO Code Changes Needed**: You do **NOT** need to re-upload or touch the code on either ESP32 microcontroller!
* **Live Video Streaming**: Real-time MJPEG feed directly from the ESP32-CAM.
* **Physics Digital Twin Model**: Animated 2D/3D robot chassis with rotating wheels, directional movement indicators, and headlight beams.
* **Virtual 16x2 LCD Hardware Mirror**: An exact green dot-matrix mirror displaying:
  * Line 0: `T:28C:L  H:65%:N`
  * Line 1: `G:0450N FN P:NO ` (switches to `*CRITICAL: FIRE*` or `PERSON DETECTED!`)
* **Real-Time Telemetry Gauges**: Live Temperature, Humidity, Gas Level, Flame status, and Person Presence.
* **Actuator Control Deck**: Touch D-Pad and Keyboard Controls ($W, A, S, D$, Space to Stop, Square Patrol).

---

## 2. Two Ways to Launch (Pick Either)

### Method 1: Instant Launch (No Python Needed!)
1. Connect your Laptop to the Mobile Hotspot (`projectiotb`).
2. Double-click the file:
   📂 `G:\1. 2026-2027\1. Project Work\3. Durga\15. Camreea robot\Digital_Twin_Dashboard\Launch_Digital_Twin.html`
3. It will open directly in Google Chrome!
4. In the top-right box, confirm your Camera IP (e.g. `192.168.43.52`) and click **Connect**.
5. Everything is live!

---

### Method 2: Localhost Server (`http://localhost:5000`)
1. Open terminal in `Digital_Twin_Dashboard/` and run:
   ```bash
   pip install flask
   python digital_twin_server.py
   ```
2. Open your browser and go to:
   $$\text{http://localhost:5000}$$
3. The server automatically sniffs all UDP broadcast packets from the ESP32-CAM on Port 4210 and updates live!
