import React from "react";
import ReactDOM from "react-dom/client";
import { createClient } from "@supabase/supabase-js";
import "./styles.css";

type EventRow = {
  event_id: string;
  encounter_id: string;
  patient_id: string;
  event_type: string;
  source_system: string;
  event_time: string;
};

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

type AgentTaskRow = {
  task_id: string;
  owner_agent: string;
  task_name: string;
  status: string;
};

type DemoEvent = {
  event_id: string;
  encounter_id: string;
  patient_id: string;
  event_type: string;
  payload: Record<string, unknown>;
};

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnon = import.meta.env.VITE_SUPABASE_ANON_KEY;
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;
const supabase = supabaseUrl && supabaseAnon ? createClient(supabaseUrl, supabaseAnon) : null;

const AGENT_PURPOSE = [
  { id: "A", label: "Founder/Product Architect", purpose: "Scope and pilot priority checks." },
  { id: "B", label: "Clinical Knowledge Engineer", purpose: "Rules and policy context selection." },
  { id: "C", label: "Data/Interop Engineer", purpose: "Event normalization and mapping." },
  { id: "D", label: "Detection/ML Engineer", purpose: "Detection execution and risk aggregation." },
  { id: "E", label: "Safety/Red-Team Engineer", purpose: "False positive risk challenge." },
  { id: "F", label: "Application Engineer", purpose: "Alert routing and escalation path." },
  { id: "G", label: "DevSecOps/MLOps Engineer", purpose: "Audit and release-gate checks." },
  { id: "H", label: "Validation/Documentation Engineer", purpose: "Validation records and quality reports." },
];

const DEMO_EVENTS: DemoEvent[] = [
  {
    event_id: "evt-med-1",
    encounter_id: "enc-1001",
    patient_id: "pat-501",
    event_type: "order_created",
    payload: { allergy_conflict: true, renal_adjustment_required: true, dose_adjusted: false },
  },
  {
    event_id: "evt-lab-1",
    encounter_id: "enc-1001",
    patient_id: "pat-501",
    event_type: "lab_reported",
    payload: { critical_flag: true, acknowledged_at: null, minutes_since_reported: 40 },
  },
  {
    event_id: "evt-vitals-1",
    encounter_id: "enc-1001",
    patient_id: "pat-501",
    event_type: "vital_sign_observed",
    payload: { risk_score: 0.88, ews_score: 8, sepsis_bundle_due: true, sepsis_bundle_completed: false },
  },
];

function simulateAlerts(events: DemoEvent[]) {
  let med = 0;
  let crit = 0;
  let det = 0;
  for (const e of events) {
    if (e.event_type.startsWith("order") || e.event_type === "discharge_completed") {
      if (e.payload.allergy_conflict === true) med += 1;
      if (e.payload.renal_adjustment_required === true && e.payload.dose_adjusted === false) med += 1;
    }
    if (e.event_type === "lab_reported" && e.payload.critical_flag === true && e.payload.acknowledged_at == null) {
      crit += 1;
    }
    if (e.event_type === "vital_sign_observed") {
      if (Number(e.payload.risk_score || 0) >= 0.8 || Number(e.payload.ews_score || 0) >= 7) det += 1;
      if (e.payload.sepsis_bundle_due === true && e.payload.sepsis_bundle_completed === false) det += 1;
    }
  }
  const total = med + crit + det;
  return {
    totalAlerts: total,
    byDomain: {
      medication_safety: med,
      critical_result_closure: crit,
      deterioration_surveillance: det,
    },
    estimatedTasks: events.length * 16,
  };
}

function App() {
  const [alerts, setAlerts] = React.useState<AlertRow[]>([]);
  const [events, setEvents] = React.useState<EventRow[]>([]);
  const [tasks, setTasks] = React.useState<AgentTaskRow[]>([]);
  const [error, setError] = React.useState<string>("");
  const [source, setSource] = React.useState<"api" | "supabase" | "simulation">("simulation");
  const [apiReport, setApiReport] = React.useState<any | null>(null);

  const simulation = React.useMemo(() => simulateAlerts(DEMO_EVENTS), []);

  React.useEffect(() => {
    async function load() {
      if (apiBaseUrl) {
        try {
          const capability = await fetch(`${apiBaseUrl}/demo/capability-run`, { method: "POST" });
          if (capability.ok) {
            const report = await capability.json();
            setApiReport(report);
            setSource("api");
            return;
          }
        } catch {
          // fall through to supabase
        }
      }

      if (!supabase) {
        setError("API/Supabase not configured. Showing simulation mode.");
        setSource("simulation");
        return;
      }

      const [alertsRes, eventsRes, tasksRes] = await Promise.all([
        supabase
          .from("alerts")
          .select("id, patient_id, encounter_id, domain, alert_type, severity, status, generated_at")
          .order("generated_at", { ascending: false })
          .limit(25),
        supabase
          .from("events")
          .select("event_id, encounter_id, patient_id, event_type, source_system, event_time")
          .order("event_time", { ascending: false })
          .limit(25),
        supabase
          .from("agent_tasks")
          .select("task_id, owner_agent, task_name, status")
          .limit(80),
      ]);

      const firstError = alertsRes.error || eventsRes.error || tasksRes.error;
      if (firstError) {
        setError(`Supabase query failed (${firstError.message}). Showing simulation mode.`);
        setSource("simulation");
        return;
      }

      const loadedAlerts = alertsRes.data || [];
      const loadedEvents = eventsRes.data || [];
      const loadedTasks = tasksRes.data || [];
      setAlerts(loadedAlerts);
      setEvents(loadedEvents);
      setTasks(loadedTasks);
      setSource(loadedAlerts.length > 0 || loadedEvents.length > 0 ? "supabase" : "simulation");
    }

    void load();
  }, []);

  return (
    <main className="page">
      <section className="hero">
        <h1>SentinelCare Command Console</h1>
        <p>Input events -&gt; multi-agent analysis -&gt; routed outputs.</p>
      </section>

      <section className="banner">
        <strong>Mode:</strong>{" "}
        {source === "api"
          ? "Live API Orchestrated Demo"
          : source === "supabase"
            ? "Live Supabase Data"
            : "Simulation Demo Data"}
        {error ? <span className="error-inline"> | {error}</span> : null}
      </section>

      <section className="grid">
        <article className="card">
          <h2>Input Events</h2>
          <p>What the system ingests before analysis.</p>
          <table>
            <thead>
              <tr>
                <th>Event</th>
                <th>Type</th>
                <th>Patient</th>
                <th>Encounter</th>
              </tr>
            </thead>
            <tbody>
              {(source === "supabase" ? events : DEMO_EVENTS).slice(0, 8).map((e: any) => (
                <tr key={e.event_id}>
                  <td>{e.event_id}</td>
                  <td>{e.event_type}</td>
                  <td>{e.patient_id}</td>
                  <td>{e.encounter_id}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </article>

        <article className="card">
          <h2>Agent Analysis</h2>
          <p>Agents are orchestrated runtime modules, not autonomous clinical decision-makers.</p>
          <ul className="agent-list">
            {AGENT_PURPOSE.map((a) => (
              <li key={a.id}>
                <strong>{a.id}</strong> {a.label}: {a.purpose}
              </li>
            ))}
          </ul>
        </article>
      </section>

      <section className="grid">
        <article className="card">
          <h2>Outputs (Alerts)</h2>
          <p>Safety findings and escalation signals produced by analysis.</p>
          {source === "supabase" ? (
            <table>
              <thead>
                <tr>
                  <th>When</th>
                  <th>Domain</th>
                  <th>Type</th>
                  <th>Severity</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {alerts.slice(0, 10).map((a) => (
                  <tr key={a.id}>
                    <td>{new Date(a.generated_at).toLocaleString()}</td>
                    <td>{a.domain}</td>
                    <td>{a.alert_type}</td>
                    <td>{a.severity}</td>
                    <td>{a.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : source === "api" && apiReport ? (
            <div className="stat-grid">
              <div className="stat">
                <span>Total Alerts</span>
                <strong>{apiReport.alerts_generated || 0}</strong>
              </div>
              <div className="stat">
                <span>Medication</span>
                <strong>{apiReport.alerts_by_domain?.medication_safety || 0}</strong>
              </div>
              <div className="stat">
                <span>Critical Results</span>
                <strong>{apiReport.alerts_by_domain?.critical_result_closure || 0}</strong>
              </div>
              <div className="stat">
                <span>Deterioration</span>
                <strong>{apiReport.alerts_by_domain?.deterioration_surveillance || 0}</strong>
              </div>
            </div>
          ) : (
            <div className="stat-grid">
              <div className="stat">
                <span>Total Alerts</span>
                <strong>{simulation.totalAlerts}</strong>
              </div>
              <div className="stat">
                <span>Medication</span>
                <strong>{simulation.byDomain.medication_safety}</strong>
              </div>
              <div className="stat">
                <span>Critical Results</span>
                <strong>{simulation.byDomain.critical_result_closure}</strong>
              </div>
              <div className="stat">
                <span>Deterioration</span>
                <strong>{simulation.byDomain.deterioration_surveillance}</strong>
              </div>
            </div>
          )}
        </article>

        <article className="card">
          <h2>Execution Trace</h2>
          <p>Work volume and orchestration state across agents.</p>
          <div className="stat-grid">
            <div className="stat">
              <span>Tasks Executed</span>
              <strong>
                {source === "api"
                  ? apiReport?.tasks_generated || 0
                  : source === "supabase"
                    ? tasks.length
                    : simulation.estimatedTasks}
              </strong>
            </div>
            <div className="stat">
              <span>Agents Active</span>
              <strong>8</strong>
            </div>
            <div className="stat">
              <span>Human-in-loop</span>
              <strong>Enabled</strong>
            </div>
            <div className="stat">
              <span>Intervention Mode</span>
              <strong>Advisory + Escalation</strong>
            </div>
          </div>
        </article>
      </section>
    </main>
  );
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
