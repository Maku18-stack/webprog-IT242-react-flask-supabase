import { useEffect, useState } from "react";

const API_URL = import.meta.env.VITE_API_URL;

export default function Guestbook() {
  const [entries, setEntries] = useState([]);
  const [name, setName] = useState("");
  const [message, setMessage] = useState("");

  async function loadEntries() {
    const res = await fetch(`${API_URL}/guestbook`);
    const data = await res.json();
    setEntries(Array.isArray(data) ? data : []);
  }

  async function submit(e) {
    e.preventDefault();
    await fetch(`${API_URL}/guestbook`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, message }),
    });
    setName("");
    setMessage("");
    loadEntries();
  }

  useEffect(() => { loadEntries(); }, []);

  return (
    <div style={{ maxWidth: 600, margin: "40px auto", fontFamily: "Arial" }}>
      <h2>Guestbook</h2>
      <form onSubmit={submit} style={{ display: "grid", gap: 10 }}>
        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Name" />
        <textarea value={message} onChange={(e) => setMessage(e.target.value)} placeholder="Message" rows={4} />
        <button>Post</button>
      </form>
      <hr style={{ margin: "20px 0" }} />
      {entries.map((x) => (
        <div key={x.id} style={{ marginBottom: 12 }}>
          <b>{x.name}</b>
          <div>{x.message}</div>
          <small>{new Date(x.created_at).toLocaleString()}</small>
        </div>
      ))}
    </div>
  );
}