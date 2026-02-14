from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json

BASE = Path(__file__).parent
DATA_FILE = BASE / "messages.json"
STATIC_DIR = BASE / "static"

app = Flask(__name__, static_folder=str(STATIC_DIR), static_url_path="")
CORS(app)

def load_messages():
    if not DATA_FILE.exists():
        return []
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))

def save_messages(msgs):
    DATA_FILE.write_text(json.dumps(msgs, ensure_ascii=False, indent=2), encoding="utf-8")

@app.route("/api/messages", methods=["GET"])
def api_get_messages():
    return jsonify(load_messages())

@app.route("/api/messages", methods=["POST"])
def api_post_message():
    payload = request.get_json(silent=True) or {}
    msgs = load_messages()
    msgs.append({
        "from": payload.get("from", "Anonymous"),
        "to": payload.get("to", ""),
        "message": payload.get("message", ""),
        "response": payload.get("response", "")
    })
    save_messages(msgs)
    return jsonify({"status": "ok"}), 201

# Serve frontend
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and (STATIC_DIR / path).exists():
        return send_from_directory(STATIC_DIR, path)
    return send_from_directory(STATIC_DIR, "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)