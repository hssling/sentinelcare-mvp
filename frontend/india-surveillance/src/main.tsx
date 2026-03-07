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
};

type Signal = {
  signal_id: string;
  title: string;
  scope: string;
  state?: string | null;
  district?: string | null;
  domain: string;
  deviation_class: string;
  severity: string;
  reports_linked: number;
  owner_role: string;
  next_action: string;
  status: string;
};

type Policy = {
  policy_id: string;
  title: string;
  state: string;
  validation_phase: string;
  approver: string;
  activation_scope: string;
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

function App() {
  const [overview, setOverview] = useState<Overview | null>(null);
  const [reports, setReports] = useState<Report[]>([]);
  const [signals, setSignals] = useState<Signal[]>([]);
  const [policies, setPolicies] = useState<Policy[]>([]);
  const [trace, setTrace] = useState<Trace | null>(null);
  const [integration, setIntegration] = useState<IntegrationProfile | null>(null);
  const [mode, setMode] = useState('loading');

  useEffect(() => {
    Promise.all([
      fetch(`${apiBase}/overview`).then((r) => r.json()),
      fetch(`${apiBase}/reports`).then((r) => r.json()),
      fetch(`${apiBase}/signals`).then((r) => r.json()),
      fetch(`${apiBase}/policies`).then((r) => r.json()),
      fetch(`${apiBase}/integration-profile`).then((r) => r.json()),
    ])
      .then(([overviewData, reportData, signalData, policyData, integrationData]) => {
        setOverview(overviewData);
        setReports(reportData);
        setSignals(signalData);
        setPolicies(policyData);
        setIntegration(integrationData);
        setMode('live-api');
        if (reportData.length > 0) {
          return fetch(`${apiBase}/trace/${reportData[0].report_id}`).then((r) => r.json()).then(setTrace);
        }
        return null;
      })
      .catch(() => setMode('api-unavailable'));
  }, []);

  const domainCounts = useMemo(() => {
    return reports.reduce<Record<string, number>>((acc, report) => {
      acc[report.domain] = (acc[report.domain] || 0) + 1;
      return acc;
    }, {});
  }, [reports]);

  return (
    <div className="page-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">India patient safety infrastructure</p>
          <h1>National Surveillance Command Surface</h1>
          <p className="lede">
            A federated surveillance, signal detection, investigation, governance, and learning system for medical errors and patient safety in India.
          </p>
        </div>
        <div className="hero-card">
          <span className="status-dot" />
          <strong>Mode: {mode === 'live-api' ? 'Live API demo' : 'API unavailable'}</strong>
          <p>{apiBase}</p>
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
        <Panel title="Incoming reports" subtitle="Facility-level intake and triage">
          {reports.map((report) => (
            <button key={report.report_id} className="report-card" onClick={() => fetch(`${apiBase}/trace/${report.report_id}`).then((r) => r.json()).then(setTrace)}>
              <div className="report-header">
                <span>{report.report_id}</span>
                <span className={`pill severity-${report.severity}`}>{report.severity}</span>
              </div>
              <strong>{report.domain.replace('_', ' ')}</strong>
              <p>{report.summary}</p>
              <small>{report.deviation_class.replace('_', ' ')} • {report.status}</small>
            </button>
          ))}
        </Panel>

        <Panel title="Active signal queue" subtitle="State and national surveillance attention">
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
        </Panel>
      </section>

      <section className="panel-grid">
        <Panel title="Event trace" subtitle="Explainable case progression from intake to closure">
          {trace ? (
            <>
              <div className="trace-meta">
                <h3>{trace.report_id}</h3>
                <p>{trace.facility} • {trace.state} • {trace.district}</p>
                <p>{trace.domain.replace('_', ' ')} • {trace.deviation_class.replace('_', ' ')} • {trace.severity}</p>
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
              <span key={domain} className="chip">{domain.replace('_', ' ')}: {count}</span>
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
