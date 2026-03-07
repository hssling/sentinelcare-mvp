import React, { useEffect, useMemo, useState } from 'react';
import ReactDOM from 'react-dom/client';
import './styles.css';

type Overview = {
  reporting_period: string;
  facilities_onboarded: number;
  states_covered: number;
  reports_received: number;
  open_investigations: number;
  escalated_signals: number;
  sentinel_events: number;
  validation_phase: string;
};

type Report = {
  report_id: string;
  facility_id: string;
  patient_context: string;
  domain: string;
  deviation_class: string;
  severity: string;
  summary: string;
  immediate_action: string;
  status: string;
  assigned_to?: string | null;
  state_cell?: string | null;
  closure_note?: string | null;
};

type Signal = {
  signal_id: string;
  title: string;
  scope: string;
  domain: string;
  deviation_class: string;
  severity: string;
  owner_role: string;
  next_action: string;
  status: string;
};

type Policy = {
  policy_id: string;
  title: string;
  state: string;
  validation_phase: string;
  activation_scope: string;
};

type User = {
  user_id: string;
  name: string;
  role: string;
  state?: string | null;
};

type StateCell = {
  state_cell_id: string;
  state: string;
  nodal_unit: string;
  lead_name: string;
  status: string;
  facilities_mapped: number;
};

type TraceStep = { step: string; finding: string; output: string };
type Trace = {
  report_id: string;
  facility: string;
  state: string;
  district: string;
  domain: string;
  deviation_class: string;
  severity: string;
  validation_phase: string;
  active_policy_version: string;
  trace_steps: TraceStep[];
  routed_to: string;
  closure_requirement: string;
};

type IntegrationProfile = {
  target_systems: string[];
  input_modes: string[];
  standards: string[];
  privacy_controls: string[];
  deployment_model: string;
};

const apiBase = (import.meta as ImportMeta & { env: { VITE_INDIA_SURVEILLANCE_API_BASE?: string } }).env.VITE_INDIA_SURVEILLANCE_API_BASE || 'http://127.0.0.1:8010';

async function getJson<T>(path: string, userId?: string): Promise<T> {
  const headers: HeadersInit = userId ? { 'x-demo-user': userId } : {};
  const response = await fetch(`${apiBase}${path}`, { headers });
  if (!response.ok) {
    throw new Error(`Request failed: ${path}`);
  }
  return response.json();
}

function App() {
  const [overview, setOverview] = useState<Overview | null>(null);
  const [reports, setReports] = useState<Report[]>([]);
  const [signals, setSignals] = useState<Signal[]>([]);
  const [policies, setPolicies] = useState<Policy[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [stateCells, setStateCells] = useState<StateCell[]>([]);
  const [trace, setTrace] = useState<Trace | null>(null);
  const [integration, setIntegration] = useState<IntegrationProfile | null>(null);
  const [activeUser, setActiveUser] = useState('demo-national');
  const [mode, setMode] = useState('loading');

  const refresh = async (userId: string) => {
    const [overviewData, reportData, signalData, policyData, integrationData, userData, stateCellData] = await Promise.all([
      getJson<Overview>('/overview', userId),
      getJson<Report[]>('/reports', userId),
      getJson<Signal[]>('/signals', userId),
      getJson<Policy[]>('/policies', userId),
      getJson<IntegrationProfile>('/integration-profile', userId),
      getJson<User[]>('/users', userId),
      getJson<StateCell[]>('/state-cells', userId),
    ]);
    setOverview(overviewData);
    setReports(reportData);
    setSignals(signalData);
    setPolicies(policyData);
    setIntegration(integrationData);
    setUsers(userData);
    setStateCells(stateCellData);
    if (reportData.length > 0) {
      setTrace(await getJson<Trace>(`/trace/${reportData[0].report_id}`, userId));
    }
  };

  useEffect(() => {
    refresh(activeUser)
      .then(() => setMode('live-api'))
      .catch(() => setMode('api-unavailable'));
  }, [activeUser]);

  const domainCounts = useMemo(() => reports.reduce<Record<string, number>>((acc, report) => {
    acc[report.domain] = (acc[report.domain] || 0) + 1;
    return acc;
  }, {}), [reports]);

  const handleTriage = async (reportId: string) => {
    await fetch(`${apiBase}/reports/${reportId}/triage`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-demo-user': activeUser },
      body: JSON.stringify({ status: 'investigating', assigned_to: 'State surveillance reviewer', state_cell: 'Pilot state cell' }),
    });
    await refresh(activeUser);
    setTrace(await getJson<Trace>(`/trace/${reportId}`, activeUser));
  };

  const handleClose = async (reportId: string) => {
    await fetch(`${apiBase}/reports/${reportId}/close`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-demo-user': activeUser },
      body: JSON.stringify({ closure_note: 'Closed after state-cell review and CAPA registration.' }),
    });
    await refresh(activeUser);
    setTrace(await getJson<Trace>(`/trace/${reportId}`, activeUser));
  };

  return (
    <div className="page-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">India patient safety infrastructure</p>
          <h1>National Surveillance Command Surface</h1>
          <p className="lede">A federated surveillance, signal detection, investigation, governance, and learning system for medical errors and patient safety in India.</p>
        </div>
        <div className="hero-card">
          <span className="status-dot" />
          <strong>Mode: {mode === 'live-api' ? 'Live API demo' : 'API unavailable'}</strong>
          <p>{apiBase}</p>
          <label className="selector-label">
            Demo role
            <select value={activeUser} onChange={(e) => setActiveUser(e.target.value)}>
              {users.map((user) => <option key={user.user_id} value={user.user_id}>{user.name} ({user.role})</option>)}
            </select>
          </label>
        </div>
      </header>

      {overview && (
        <section className="metric-grid">
          <Metric label="Facilities onboarded" value={overview.facilities_onboarded} />
          <Metric label="States covered" value={overview.states_covered} />
          <Metric label="Reports received" value={overview.reports_received} />
          <Metric label="Open investigations" value={overview.open_investigations} />
          <Metric label="Escalated signals" value={overview.escalated_signals} />
          <Metric label="Sentinel events" value={overview.sentinel_events} />
        </section>
      )}

      <section className="panel-grid">
        <Panel title="Incoming reports" subtitle="Facility-level intake, triage, and state-cell actions">
          {reports.map((report) => (
            <div key={report.report_id} className="report-card">
              <div className="report-header">
                <span>{report.report_id}</span>
                <span className={`pill severity-${report.severity}`}>{report.severity}</span>
              </div>
              <strong>{report.domain.replace(/_/g, ' ')}</strong>
              <p>{report.summary}</p>
              <small>{report.deviation_class.replace(/_/g, ' ')} • {report.status}{report.assigned_to ? ` • ${report.assigned_to}` : ''}</small>
              <div className="action-row">
                <button onClick={() => getJson<Trace>(`/trace/${report.report_id}`, activeUser).then(setTrace)}>Trace</button>
                <button onClick={() => handleTriage(report.report_id)}>Triage</button>
                <button onClick={() => handleClose(report.report_id)}>Close</button>
              </div>
            </div>
          ))}
        </Panel>

        <Panel title="State cells and active signal queue" subtitle="Operational layers for pilot-state surveillance">
          <div className="subsection">
            <h3>State cells</h3>
            {stateCells.map((cell) => (
              <div key={cell.state_cell_id} className="policy-row">
                <strong>{cell.state}</strong>
                <small>{cell.status} • {cell.facilities_mapped} mapped facilities • {cell.lead_name}</small>
              </div>
            ))}
          </div>
          <div className="subsection">
            <h3>Signals</h3>
            {signals.map((signal) => (
              <div key={signal.signal_id} className="signal-card">
                <div className="report-header">
                  <span>{signal.signal_id}</span>
                  <span className={`pill severity-${signal.severity}`}>{signal.status}</span>
                </div>
                <strong>{signal.title}</strong>
                <p>{signal.next_action}</p>
                <small>{signal.scope} • {signal.owner_role}</small>
              </div>
            ))}
          </div>
        </Panel>
      </section>

      <section className="panel-grid">
        <Panel title="Event trace" subtitle="Explainable case progression from intake to closure">
          {trace ? (
            <>
              <div className="trace-meta">
                <h3>{trace.report_id}</h3>
                <p>{trace.facility} • {trace.state} • {trace.district}</p>
                <p>{trace.domain.replace(/_/g, ' ')} • {trace.deviation_class.replace(/_/g, ' ')} • {trace.severity}</p>
              </div>
              <div className="trace-steps">
                {trace.trace_steps.map((step) => (
                  <div key={step.step} className="trace-step">
                    <strong>{step.step}</strong>
                    <p>{step.finding}</p>
                    <small>{step.output}</small>
                  </div>
                ))}
              </div>
              <div className="trace-footer">
                <p><strong>Routed to:</strong> {trace.routed_to}</p>
                <p><strong>Closure requirement:</strong> {trace.closure_requirement}</p>
                <p><strong>Policy context:</strong> {trace.active_policy_version}</p>
              </div>
            </>
          ) : <p>No trace loaded.</p>}
        </Panel>

        <Panel title="Governance and integration" subtitle="Validation state, policies, and system readiness">
          <div className="subsection">
            <h3>Policies</h3>
            {policies.map((policy) => (
              <div key={policy.policy_id} className="policy-row">
                <strong>{policy.title}</strong>
                <small>{policy.state} • {policy.validation_phase} • {policy.activation_scope}</small>
              </div>
            ))}
          </div>
          {integration && (
            <div className="subsection">
              <h3>Integration profile</h3>
              <ul>
                {integration.target_systems.map((item) => <li key={item}>{item}</li>)}
              </ul>
            </div>
          )}
        </Panel>
      </section>

      <section className="panel-grid">
        <Panel title="Cross-domain patterning" subtitle="Shared surveillance semantics">
          <div className="chips">
            {Object.entries(domainCounts).map(([domain, count]) => (
              <span key={domain} className="chip">{domain.replace(/_/g, ' ')}: {count}</span>
            ))}
          </div>
          <p className="footnote">All event records are normalized to domain, deviation class, severity, process stage, and closure workflow.</p>
        </Panel>
        <Panel title="Scale design" subtitle="Built for phased roll-out across India">
          <ol className="ordered">
            <li>Sentinel facility network</li>
            <li>State patient safety intelligence cells</li>
            <li>National benchmarking and rapid alerts</li>
            <li>ABDM and HIS integration at scale</li>
          </ol>
        </Panel>
      </section>
    </div>
  );
}

function Panel(props: { title: string; subtitle: string; children: React.ReactNode }) {
  return (
    <div className="panel">
      <div className="panel-head">
        <h2>{props.title}</h2>
        <p>{props.subtitle}</p>
      </div>
      {props.children}
    </div>
  );
}

function Metric(props: { label: string; value: number }) {
  return (
    <div className="metric-card">
      <span>{props.label}</span>
      <strong>{props.value}</strong>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
