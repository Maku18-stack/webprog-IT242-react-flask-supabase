import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client

app = Flask(__name__)
CORS(app)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY env vars.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
TABLE = "guestbook"

@app.get("/")
def home():
    return jsonify({"status": "ok", "message": "Guestbook API running"})

@app.get("/guestbook")
def get_entries():
    resp = supabase.table(TABLE).select("*").order("created_at", desc=True).execute()
    return jsonify(resp.data), 200

@app.post("/guestbook")
def add_entry():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not message:
        return jsonify({"error": "name and message are required"}), 400

    resp = supabase.table(TABLE).insert({"name": name, "message": message}).execute()
    return jsonify(resp.data), 201

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)