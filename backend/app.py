import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client

app = Flask(__name__)
CORS(app)

# 🔹 Read environment variables (Render / local)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY")

# 🔹 Connect to Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

TABLE = "guestbook"


# ✅ Home route (for testing)
@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "message": "Guestbook API running"
    })


# ✅ GET all guestbook entries
@app.route("/guestbook", methods=["GET"])
def get_entries():
    response = (
        supabase.table(TABLE)
        .select("created_at,id,message,name")
        .order("created_at", desc=True)
        .execute()
    )
    return jsonify(response.data), 200


# ✅ POST new entry
@app.route("/guestbook", methods=["POST"])
def add_entry():
    data = request.get_json(silent=True) or {}

    name = (data.get("name") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not message:
        return jsonify({"error": "name and message are required"}), 400

    response = supabase.table(TABLE).insert({
        "name": name,
        "message": message
    }).execute()

    return jsonify(response.data), 201


# ✅ PUT update entry (optional)
@app.route("/guestbook/<entry_id>", methods=["PUT"])
def update_entry(entry_id):
    data = request.get_json(silent=True) or {}

    response = (
        supabase.table(TABLE)
        .update(data)
        .eq("id", entry_id)
        .execute()
    )

    return jsonify(response.data), 200


# ✅ DELETE entry (optional)
@app.route("/guestbook/<entry_id>", methods=["DELETE"])
def delete_entry(entry_id):
    response = (
        supabase.table(TABLE)
        .delete()
        .eq("id", entry_id)
        .execute()
    )

    return jsonify(response.data), 200


# ✅ Run server (Render compatible)
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)