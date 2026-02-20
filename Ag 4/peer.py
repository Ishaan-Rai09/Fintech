import argparse
import requests
import uuid
import threading
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Enable CORS for frontend interaction

# In-memory storage
NODE_ID = str(uuid.uuid4())[:8]
PEERS = set()
HISTORY = []

@app.route("/status", methods=["GET"])
def get_status():
    return jsonify({
        "node_id": NODE_ID,
        "peers": list(PEERS),
        "history_count": len(HISTORY)
    })

@app.route("/connect", methods=["POST"])
def connect_peer():
    data = request.json
    address = data.get("address")
    
    if not address:
        return jsonify({"status": "invalid address"})
        
    if address == f"http://localhost:{args.port}":
        return jsonify({"status": "cannot connect to self"})

    if address not in PEERS:
        PEERS.add(address)
        
        # Mutual connection: Send a handshake back
        try:
            requests.post(
                f"{address.rstrip('/')}/handshake",
                json={"address": f"http://localhost:{args.port}"},
                timeout=2
            )
        except Exception as e:
            print(f"Failed to handshake with {address}: {e}")
            
        return jsonify({"status": "connected", "peer": address})
    return jsonify({"status": "already connected"})

@app.route("/handshake", methods=["POST"])
def handshake():
    data = request.json
    address = data.get("address")
    if address and address not in PEERS and address != f"http://localhost:{args.port}":
        PEERS.add(address)
        return jsonify({"status": "handshake_accepted", "peer": address})
    return jsonify({"status": "handshake_ignored"})

@app.route("/receive", methods=["POST"])
def receive_message():
    msg = request.json
    # Avoid duplicate messages
    if any(m["msg_id"] == msg.get("msg_id") for m in HISTORY):
        return jsonify({"status": "duplicate"})
    
    HISTORY.append(msg)
    return jsonify({"status": "received"})

def broadcast_task(msg):
    for peer in list(PEERS):
        try:
            # Clean up address if needed
            url = f"{peer.rstrip('/')}/receive"
            requests.post(url, json=msg, timeout=2)
        except Exception as e:
            print(f"Failed to send to {peer}: {e}")

@app.route("/send", methods=["POST"])
def send_message():
    data = request.json
    msg = {
        "msg_id": str(uuid.uuid4())[:8],
        "timestamp": datetime.now().isoformat(),
        "sender": f"Node-{NODE_ID}",
        "content": data.get("content", "")
    }
    
    HISTORY.append(msg)
    # Run broadcast in background thread
    threading.Thread(target=broadcast_task, args=(msg,)).start()
    
    return jsonify({"status": "broadcast_started", "msg_id": msg["msg_id"]})

@app.route("/history", methods=["GET"])
def get_history():
    return jsonify(HISTORY)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    app.run(host="0.0.0.0", port=args.port, debug=False, threaded=True)
