"""
========================================================================================
Project      : Single-Window Localhost Digital Twin Server
File         : digital_twin_server.py
Location     : G:\1. 2026-2027\1. Project Work\3. Durga\15. Camreea robot\Digital_Twin_Dashboard\
========================================================================================

Description:
  1. Automatically listens on UDP Port 4210 for incoming ESP32-CAM Person alerts and IP beacons.
  2. Serves the interactive Digital Twin Web Dashboard at http://localhost:5000.
  3. Completely standalone -- ZERO code changes required on either ESP32 microcontroller!

Run command:
  python digital_twin_server.py
========================================================================================
"""

from flask import Flask, jsonify, send_file, request
import socket
import threading
import time
import os

app = Flask(__name__)

# Shared Live Robot State
robot_state = {
    "camera_ip": "192.168.43.52",
    "person_detected": False,
    "last_seen_time": 0,
    "temperature": 28.0,
    "humidity": 65.0,
    "gas_level": 450,
    "flame_detected": False,
    "robot_action": "STOPPED",
    "total_alerts": 0
}

UDP_PORT = 4210

def udp_sniffer_thread():
    """Background thread that listens on UDP Port 4210 for broadcasts."""
    global robot_state
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    try:
        sock.bind(("", UDP_PORT))
        print(f"[*] UDP Sniffer active on Port {UDP_PORT}. Listening for ESP32 packets...")
    except Exception as e:
        print(f"[!] UDP Bind Error: {e}")
        return

    while True:
        try:
            data, addr = sock.recvfrom(1024)
            msg = data.decode('utf-8', errors='ignore').strip()
            sender_ip = addr[0]

            # Auto-discover camera IP
            robot_state["camera_ip"] = sender_ip

            if msg == "1" or "PERSON" in msg:
                robot_state["person_detected"] = True
                robot_state["last_seen_time"] = time.time()
                robot_state["total_alerts"] += 1
                print(f"[UDP ALERT] Person Detected from {sender_ip} (Alert #{robot_state['total_alerts']})")
            elif "CAM_IP:" in msg:
                clean_ip = msg.replace("CAM_IP:http://", "").replace("CAM_IP:", "").strip()
                robot_state["camera_ip"] = clean_ip

        except Exception as err:
            time.sleep(0.1)

# Watchdog to reset person presence after 3 seconds of silence
def watchdog_thread():
    global robot_state
    while True:
        if robot_state["person_detected"]:
            if time.time() - robot_state["last_seen_time"] > 3.0:
                robot_state["person_detected"] = False
                print("[WATCHDOG] Person Left View (Normalized to False)")
        time.sleep(0.5)

@app.route("/")
def index():
    html_path = os.path.join(os.path.dirname(__file__), "Launch_Digital_Twin.html")
    return send_file(html_path)

@app.route("/api/telemetry")
def get_telemetry():
    return jsonify(robot_state)

if __name__ == "__main__":
    # Start background threads
    t1 = threading.Thread(target=udp_sniffer_thread, daemon=True)
    t2 = threading.Thread(target=watchdog_thread, daemon=True)
    t1.start()
    t2.start()

    print("=" * 65)
    print("   ESP32 AI SURVEILLANCE ROBOT - DIGITAL TWIN LOCALHOST SERVER   ")
    print("=" * 65)
    print("Open this URL in Google Chrome:")
    print("  👉 http://localhost:5000")
    print("=" * 65)

    app.run(host="0.0.0.0", port=5000, debug=False)
