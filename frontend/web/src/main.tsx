import React from "react";
import ReactDOM from "react-dom/client";
import { createClient } from "@supabase/supabase-js";
import "./styles.css";

type AlertRow = {
  id: string;
  patient_id: string;
  encounter_id: string;
  domain: string;
  alert_type: string;
  severity: string;
  status: string;
  generated_at: string;
};

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnon = import.meta.env.VITE_SUPABASE_ANON_KEY;
const supabase = supabaseUrl && supabaseAnon ? createClient(supabaseUrl, supabaseAnon) : null;

function App() {
  const [alerts, setAlerts] = React.useState<AlertRow[]>([]);
  const [error, setError] = React.useState<string>("");

  React.useEffect(() => {
    async function load() {
      if (!supabase) {
        setError("Supabase env vars not configured.");
        return;
      }
      const { data, error } = await supabase
        .from("alerts")
        .select("id, patient_id, encounter_id, domain, alert_type, severity, status, generated_at")
        .order("generated_at", { ascending: false })
        .limit(25);
      if (error) {
        setError(error.message);
        return;
      }
      setAlerts(data || []);
    }
    void load();
  }, []);

  return (
    <main className="page">
      <section className="hero">
        <h1>SentinelCare Command Console</h1>
        <p>Live patient safety alerts from Supabase.</p>
      </section>
      {error ? <p className="error">{error}</p> : null}
      <section className="card">
        <h2>Recent Alerts</h2>
        <table>
          <thead>
            <tr>
              <th>When</th>
              <th>Domain</th>
              <th>Type</th>
              <th>Severity</th>
              <th>Status</th>
              <th>Patient</th>
              <th>Encounter</th>
            </tr>
          </thead>
          <tbody>
            {alerts.map((a) => (
              <tr key={a.id}>
                <td>{new Date(a.generated_at).toLocaleString()}</td>
                <td>{a.domain}</td>
                <td>{a.alert_type}</td>
                <td>{a.severity}</td>
                <td>{a.status}</td>
                <td>{a.patient_id}</td>
                <td>{a.encounter_id}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </main>
  );
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);

