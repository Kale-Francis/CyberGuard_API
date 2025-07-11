import React, { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [anomalies, setAnomalies] = useState([]);
  const [log, setLog] = useState({ ip: "", port: "", protocol: "" });

  const login = async () => {
    const res = await axios.post("http://localhost:3000/login", { email: "admin@example.com", password: "your_password" });
    localStorage.setItem("token", res.data.token);
    setToken(res.data.token);
  };

  const ingestLog = async () => {
    await axios.post("http://localhost:3000/logs", log, { headers: { Authorization: `Bearer ${token}` } });
    alert("Log ingested");
  };

  const fetchAnomalies = async () => {
    const res = await axios.get("http://localhost:3000/anomalies", { headers: { Authorization: `Bearer ${token}` } });
    setAnomalies(res.data);
  };

  useEffect(() => {
    if (token) fetchAnomalies();
  }, [token]);

  return (
    <div style={{ padding: "20px" }}>
      <h1>CyberGuard Dashboard</h1>
      {!token ? (
        <button onClick={login}>Login</button>
      ) : (
        <>
          <div>
            <input placeholder="IP" value={log.ip} onChange={(e) => setLog({ ...log, ip: e.target.value })} />
            <input placeholder="Port" type="number" value={log.port} onChange={(e) => setLog({ ...log, port: e.target.value })} />
            <input placeholder="Protocol" value={log.protocol} onChange={(e) => setLog({ ...log, protocol: e.target.value })} />
            <button onClick={ingestLog}>Ingest Log</button>
          </div>
          <button onClick={fetchAnomalies}>Refresh Anomalies</button>
          <h3>Anomalies:</h3>
          <ul>
            {anomalies.map((a, i) => <li key={i}>{JSON.stringify(a)}</li>)}
          </ul>
        </>
      )}
    </div>
  );
}

export default App;