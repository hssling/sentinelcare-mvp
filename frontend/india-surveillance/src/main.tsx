import React, { useEffect, useMemo, useState } from 'react';
import ReactDOM from 'react-dom/client';
import './styles.css';

type Session = {
  access_token: string;
  token_type: string;
  expires_at: string;
  user: User;
};

type User = {
  user_id: string;
  name: string;
  role: string;
  state?: string | null;
  district?: string | null;
  facility_id?: string | null;
  department_id?: string | null;
  username?: string | null;
  is_active?: boolean;
};

type Facility = { facility_id: string; name: string; state: string; district: string };

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

type DashboardIndicator = { label: string; value: number; trend: string };
type DashboardAlert = { alert_id: string; severity: string; title: string; detail: string; owner_role: string };
type TrendPoint = { date: string; patient_days: number; near_misses: number; harm_events: number; severe_events: number };
type TrendSeries = { scope: string; points: TrendPoint[] };
type Dashboard = {
  scope: string;
  indicators: DashboardIndicator[];
  alerts: DashboardAlert[];
  submissions_pending_review: number;
  reports_open: number;
  trend?: TrendSeries | null;
};

type Department = { department_id: string; facility_id: string; name: string; category: string };
type DailySubmission = {
  submission_id: string;
  submission_date: string;
  facility_id: string;
  department_id: string;
  submitted_by: string;
  patient_days: number;
  near_misses: number;
  no_harm_events: number;
  harm_events: number;
  severe_events: number;
  medication_events: number;
  procedure_events: number;
  infection_events: number;
  diagnostic_events: number;
  escalation_required: boolean;
  notes: string;
  review_status: string;
  reviewed_by?: string | null;
};

type Report = {
  report_id: string;
  domain: string;
  deviation_class: string;
  severity: string;
  summary: string;
  status: string;
  assigned_to?: string | null;
};

type TraceStep = { step: string; finding: string; output: string };
type EventTrace = {
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

type StateCell = { state_cell_id: string; state: string; nodal_unit: string; lead_name: string; status: string; facilities_mapped: number };
type Policy = { policy_id: string; title: string; state: string; validation_phase: string; activation_scope: string };
type Notification = { notification_id: string; title: string; message: string; severity: string; status: string; created_at: string };
type AuditLog = { audit_id: string; created_at: string; action: string; entity_type: string; entity_id: string; detail: string; actor_user_id?: string | null };
type IntegrationProfile = { target_systems: string[]; input_modes: string[]; standards: string[]; privacy_controls: string[]; deployment_model: string };

const configuredApiBase = (import.meta as ImportMeta & { env: { VITE_INDIA_SURVEILLANCE_API_BASE?: string } }).env.VITE_INDIA_SURVEILLANCE_API_BASE;
const apiBase = window.location.protocol === 'https:' ? '/api' : (configuredApiBase || 'http://127.0.0.1:8010');
const sessionStorageKey = 'india-surveillance-session';
type InstallPromptEvent = Event & {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>;
};

async function api<T>(path: string, token?: string, options?: RequestInit): Promise<T> {
  const headers: HeadersInit = { 'Content-Type': 'application/json', ...(options?.headers || {}) };
  if (token) headers.Authorization = `Bearer ${token}`;
  const response = await fetch(`${apiBase}${path}`, { ...options, headers });
  if (!response.ok) {
    throw new Error(await response.text());
  }
  return response.json();
}

function parseError(error: unknown): string {
  if (!(error instanceof Error)) return 'Request failed';
  if (error.message.includes('Failed to fetch')) return 'Unable to reach the surveillance API';
  try {
    const parsed = JSON.parse(error.message);
    if (parsed.detail) return String(parsed.detail);
  } catch {
    return error.message;
  }
  return error.message;
}

function App() {
  const [session, setSession] = useState<Session | null>(() => {
    const raw = window.localStorage.getItem(sessionStorageKey);
    return raw ? JSON.parse(raw) as Session : null;
  });
  const [username, setUsername] = useState('tmk-ed');
  const [password, setPassword] = useState('pass123');
  const [loginError, setLoginError] = useState<string | null>(null);
  const [overview, setOverview] = useState<Overview | null>(null);
  const [dashboard, setDashboard] = useState<Dashboard | null>(null);
  const [facilities, setFacilities] = useState<Facility[]>([]);
  const [departments, setDepartments] = useState<Department[]>([]);
  const [submissions, setSubmissions] = useState<DailySubmission[]>([]);
  const [reports, setReports] = useState<Report[]>([]);
  const [stateCells, setStateCells] = useState<StateCell[]>([]);
  const [policies, setPolicies] = useState<Policy[]>([]);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [auditLogs, setAuditLogs] = useState<AuditLog[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [integrationProfile, setIntegrationProfile] = useState<IntegrationProfile | null>(null);
  const [selectedReportId, setSelectedReportId] = useState<string | null>(null);
  const [selectedTrace, setSelectedTrace] = useState<EventTrace | null>(null);
  const [traceError, setTraceError] = useState<string | null>(null);
  const [errorBanner, setErrorBanner] = useState<string | null>(null);
  const [lastSync, setLastSync] = useState<string | null>(null);
  const [installPrompt, setInstallPrompt] = useState<InstallPromptEvent | null>(null);
  const [form, setForm] = useState({
    department_id: '',
    patient_days: 100,
    near_misses: 0,
    no_harm_events: 0,
    harm_events: 0,
    severe_events: 0,
    medication_events: 0,
    procedure_events: 0,
    infection_events: 0,
    diagnostic_events: 0,
    escalation_required: false,
    notes: '',
  });
  const [userForm, setUserForm] = useState({
    name: '',
    username: '',
    password: 'pass123',
    role: 'facility_reporter',
    facility_id: '',
    department_id: '',
    state: '',
    district: '',
  });
  const [triageForm, setTriageForm] = useState({ status: 'triaged', assigned_to: '', state_cell: '' });

  const canCreateUsers = session?.user.role === 'facility_safety_officer' || session?.user.role === 'state_cell_analyst' || session?.user.role === 'national_analyst' || session?.user.role === 'governance_admin';
  const canManageReports = session?.user.role === 'facility_safety_officer' || session?.user.role === 'state_cell_analyst' || session?.user.role === 'national_analyst';
  const openReports = reports.filter((report) => report.status !== 'closed');
  const pendingSubmissions = submissions.filter((submission) => submission.review_status === 'submitted');
  const facilitySummary = useMemo(() => submissions.reduce((acc, item) => acc + item.near_misses + item.harm_events + item.severe_events, 0), [submissions]);

  const loadData = async (token: string) => {
    try {
      const [overviewData, facilitiesData, dashboardData, departmentsData, submissionsData, reportsData, stateCellsData, policiesData, notificationsData, usersData, auditData, integrationData] = await Promise.all([
        api<Overview>('/overview', token),
        api<Facility[]>('/facilities', token),
        api<Dashboard>('/dashboard', token),
        api<Department[]>('/departments', token),
        api<DailySubmission[]>('/daily-submissions', token),
        api<Report[]>('/reports', token),
        api<StateCell[]>('/state-cells', token),
        api<Policy[]>('/policies', token),
        api<Notification[]>('/notifications', token),
        api<User[]>('/users', token),
        api<AuditLog[]>('/audit-logs?limit=20', token).catch(() => []),
        api<IntegrationProfile>('/integration-profile', token),
      ]);
      setOverview(overviewData);
      setFacilities(facilitiesData);
      setDashboard(dashboardData);
      setDepartments(departmentsData);
      setSubmissions(submissionsData);
      setReports(reportsData);
      setStateCells(stateCellsData);
      setPolicies(policiesData);
      setNotifications(notificationsData);
      setUsers(usersData);
      setAuditLogs(auditData);
      setIntegrationProfile(integrationData);
      setForm((current) => ({ ...current, department_id: departmentsData[0]?.department_id || current.department_id }));
      setUserForm((current) => ({
        ...current,
        facility_id: session?.user.facility_id || current.facility_id,
        state: session?.user.state || current.state,
      }));
      setTriageForm((current) => ({
        ...current,
        assigned_to: current.assigned_to || session?.user.name || '',
        state_cell: current.state_cell || stateCellsData[0]?.nodal_unit || '',
      }));
      if (!selectedReportId && reportsData[0]) {
        setSelectedReportId(reportsData[0].report_id);
      }
      setErrorBanner(null);
      setLastSync(new Date().toLocaleString());
    } catch (error) {
      setErrorBanner(parseError(error));
    }
  };

  const loadTrace = async (token: string, reportId: string) => {
    try {
      const trace = await api<EventTrace>(`/trace/${reportId}`, token);
      setSelectedTrace(trace);
      setTraceError(null);
    } catch (error) {
      setSelectedTrace(null);
      setTraceError(parseError(error));
    }
  };

  useEffect(() => {
    if ('serviceWorker' in navigator) {
      void navigator.serviceWorker.register('/sw.js');
    }
    const handler = (event: Event) => {
      event.preventDefault();
      setInstallPrompt(event as InstallPromptEvent);
    };
    window.addEventListener('beforeinstallprompt', handler);
    return () => window.removeEventListener('beforeinstallprompt', handler);
  }, []);

  useEffect(() => {
    if (session) {
      window.localStorage.setItem(sessionStorageKey, JSON.stringify(session));
      void loadData(session.access_token);
    } else {
      window.localStorage.removeItem(sessionStorageKey);
    }
  }, [session]);

  useEffect(() => {
    if (session && selectedReportId) {
      void loadTrace(session.access_token, selectedReportId);
    }
  }, [session, selectedReportId]);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const nextSession = await api<Session>('/auth/login', undefined, { method: 'POST', body: JSON.stringify({ username, password }) });
      setSession(nextSession);
      setLoginError(null);
    } catch (error) {
      setLoginError(parseError(error));
    }
  };

  const submitDaily = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!session) return;
    await api<DailySubmission>('/daily-submissions', session.access_token, {
      method: 'POST',
      body: JSON.stringify({ submission_date: new Date().toISOString().slice(0, 10), ...form }),
    });
    await loadData(session.access_token);
  };

  const reviewSubmission = async (submissionId: string, reviewStatus: 'reviewed' | 'actioned') => {
    if (!session) return;
    await api(`/daily-submissions/${submissionId}/review`, session.access_token, {
      method: 'POST',
      body: JSON.stringify({ review_status: reviewStatus, reviewed_by: session.user.name, notes: `Marked ${reviewStatus}` }),
    });
    await loadData(session.access_token);
  };

  const acknowledgeNotification = async (notificationId: string, status: 'acknowledged' | 'closed') => {
    if (!session) return;
    await api(`/notifications/${notificationId}/acknowledge`, session.access_token, {
      method: 'POST',
      body: JSON.stringify({ status }),
    });
    await loadData(session.access_token);
  };

  const createUser = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!session) return;
    await api('/users', session.access_token, {
      method: 'POST',
      body: JSON.stringify(userForm),
    });
    setUserForm({ ...userForm, name: '', username: '', password: 'pass123', department_id: '' });
    await loadData(session.access_token);
  };

  const triageReport = async (reportId: string) => {
    if (!session) return;
    await api(`/reports/${reportId}/triage`, session.access_token, {
      method: 'POST',
      body: JSON.stringify(triageForm),
    });
    await loadData(session.access_token);
    await loadTrace(session.access_token, reportId);
  };

  const closeReport = async (reportId: string) => {
    if (!session) return;
    await api(`/reports/${reportId}/close`, session.access_token, {
      method: 'POST',
      body: JSON.stringify({ closure_note: `Closed by ${session.user.name} after review.` }),
    });
    await loadData(session.access_token);
    await loadTrace(session.access_token, reportId);
  };

  const triggerInstall = async () => {
    if (!installPrompt) return;
    await installPrompt.prompt();
    await installPrompt.userChoice;
    setInstallPrompt(null);
  };

  if (!session) {
    return (
      <div className="login-shell">
        <div className="login-panel">
          <p className="eyebrow">India patient safety surveillance</p>
          <h1>Facility and state login</h1>
          <p className="lede">Departments submit daily surveillance data. Facility, state, and national teams review trends, alerts, audits, and actions.</p>
          <form onSubmit={handleLogin} className="login-form">
            <label>Username<input value={username} onChange={(e) => setUsername(e.target.value)} /></label>
            <label>Password<input type="password" value={password} onChange={(e) => setPassword(e.target.value)} /></label>
            <button type="submit">Login</button>
          </form>
          <div className="demo-credentials">
            <strong>Seed accounts</strong>
            <small><code>tmk-ed</code>, <code>tmk-icu</code>, <code>ka-fso</code>, <code>state-ka</code>, <code>national</code>, <code>admin</code></small>
            <small>Password: <code>pass123</code></small>
          </div>
          {loginError && <p className="error-text">{loginError}</p>}
        </div>
      </div>
    );
  }

  return (
    <div className="page-shell">
      <header className="hero compact-hero">
        <div>
          <p className="eyebrow">Logged in as {session.user.role}</p>
          <h1>Safety surveillance command center</h1>
          <p className="lede">{session.user.name}</p>
        </div>
        <div className="hero-card">
          <strong>{session.user.facility_id || session.user.state || 'National scope'}</strong>
          <p>{lastSync ? `Last sync ${lastSync}` : apiBase}</p>
          <div className="action-row">
            {installPrompt && <button onClick={() => void triggerInstall()}>Install app</button>}
            <button onClick={() => void loadData(session.access_token)}>Refresh</button>
            <button onClick={() => setSession(null)}>Logout</button>
          </div>
        </div>
      </header>

      {errorBanner && <section className="error-banner">{errorBanner}</section>}

      {overview && dashboard && (
        <section className="metric-grid">
          <Metric label="Reports received" value={overview.reports_received} />
          <Metric label="Open reports" value={dashboard.reports_open} />
          <Metric label="Pending reviews" value={dashboard.submissions_pending_review} />
          <Metric label="Department signal load" value={facilitySummary} />
          <Metric label="Escalated signals" value={overview.escalated_signals} />
          <Metric label="Sentinel events" value={overview.sentinel_events} />
        </section>
      )}

      <section className="panel-grid panel-grid-wide">
        <Panel title="Operations queue" subtitle="Review pressure, open cases, and manager actions">
          <div className="chips">
            <span className="chip">Pending submissions: {pendingSubmissions.length}</span>
            <span className="chip">Open reports: {openReports.length}</span>
            <span className="chip">Notifications: {notifications.filter((item) => item.status !== 'closed').length}</span>
          </div>
          <div className="report-list">
            {reports.map((report) => (
              <button key={report.report_id} className={`report-card selectable ${selectedReportId === report.report_id ? 'selected' : ''}`} onClick={() => setSelectedReportId(report.report_id)}>
                <div className="report-header">
                  <span>{report.report_id}</span>
                  <span className={`pill severity-${report.severity}`}>{report.severity}</span>
                </div>
                <strong>{humanize(report.domain)} / {humanize(report.deviation_class)}</strong>
                <p>{report.summary}</p>
                <small>{report.status} | {report.assigned_to || 'unassigned'}</small>
              </button>
            ))}
          </div>
          {canManageReports && selectedReportId && (
            <div className="subsection action-block">
              <h3>Report action</h3>
              <div className="daily-form">
                <label>Status<select value={triageForm.status} onChange={(e) => setTriageForm({ ...triageForm, status: e.target.value })}><option value="triaged">Triaged</option><option value="investigating">Investigating</option></select></label>
                <label>Assigned to<input value={triageForm.assigned_to} onChange={(e) => setTriageForm({ ...triageForm, assigned_to: e.target.value })} /></label>
                <label>State cell<input value={triageForm.state_cell} onChange={(e) => setTriageForm({ ...triageForm, state_cell: e.target.value })} /></label>
              </div>
              <div className="action-row">
                <button onClick={() => void triageReport(selectedReportId)}>Save triage</button>
                <button onClick={() => void closeReport(selectedReportId)}>Close report</button>
              </div>
            </div>
          )}
        </Panel>

        <Panel title="Case trace" subtitle="Explainable path from intake to governance">
          {selectedTrace ? (
            <>
              <div className="trace-meta">
                <h3>{selectedTrace.report_id}</h3>
                <p>{selectedTrace.facility}, {selectedTrace.district}, {selectedTrace.state}</p>
                <div className="chips">
                  <span className="chip">{humanize(selectedTrace.domain)}</span>
                  <span className="chip">{humanize(selectedTrace.deviation_class)}</span>
                  <span className={`chip severity-${selectedTrace.severity}`}>{selectedTrace.severity}</span>
                </div>
              </div>
              <div className="trace-steps">
                {selectedTrace.trace_steps.map((step) => (
                  <div key={step.step} className="trace-step">
                    <strong>{humanize(step.step)}</strong>
                    <p>{step.finding}</p>
                    <small>{step.output}</small>
                  </div>
                ))}
              </div>
              <div className="trace-footer">
                <strong>Route</strong>
                <p>{selectedTrace.routed_to}</p>
                <strong>Closure requirement</strong>
                <p>{selectedTrace.closure_requirement}</p>
              </div>
            </>
          ) : (
            <p>{traceError || 'Select a report to inspect its explainable trace.'}</p>
          )}
        </Panel>
      </section>

      <section className="panel-grid">
        <Panel title="Daily surveillance feed" subtitle="Department-level reporting and review">
          {(session.user.role === 'facility_reporter' || session.user.role === 'facility_safety_officer') ? (
            <form className="daily-form" onSubmit={submitDaily}>
              <label>Department<select value={form.department_id} onChange={(e) => setForm({ ...form, department_id: e.target.value })}>{departments.map((d) => <option key={d.department_id} value={d.department_id}>{d.name}</option>)}</select></label>
              <label>Patient days<input type="number" value={form.patient_days} onChange={(e) => setForm({ ...form, patient_days: Number(e.target.value) })} /></label>
              <label>Near misses<input type="number" value={form.near_misses} onChange={(e) => setForm({ ...form, near_misses: Number(e.target.value) })} /></label>
              <label>No-harm events<input type="number" value={form.no_harm_events} onChange={(e) => setForm({ ...form, no_harm_events: Number(e.target.value) })} /></label>
              <label>Harm events<input type="number" value={form.harm_events} onChange={(e) => setForm({ ...form, harm_events: Number(e.target.value) })} /></label>
              <label>Severe events<input type="number" value={form.severe_events} onChange={(e) => setForm({ ...form, severe_events: Number(e.target.value) })} /></label>
              <label>Medication events<input type="number" value={form.medication_events} onChange={(e) => setForm({ ...form, medication_events: Number(e.target.value) })} /></label>
              <label>Diagnostic events<input type="number" value={form.diagnostic_events} onChange={(e) => setForm({ ...form, diagnostic_events: Number(e.target.value) })} /></label>
              <label>Notes<textarea value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} /></label>
              <label className="checkbox-row"><input type="checkbox" checked={form.escalation_required} onChange={(e) => setForm({ ...form, escalation_required: e.target.checked })} />Escalation required</label>
              <button type="submit">Submit daily surveillance</button>
            </form>
          ) : <p>This role reviews submissions rather than creating them.</p>}
        </Panel>

        <Panel title="Review worklist" subtitle="Submissions requiring action and manager closure">
          {submissions.map((submission) => (
            <div key={submission.submission_id} className="report-card">
              <div className="report-header">
                <span>{submission.submission_id}</span>
                <span className="pill">{submission.review_status}</span>
              </div>
              <strong>{departments.find((d) => d.department_id === submission.department_id)?.name || submission.department_id}</strong>
              <p>{submission.notes || 'No notes recorded.'}</p>
              <small>Near misses {submission.near_misses} | Harm {submission.harm_events} | Severe {submission.severe_events}</small>
              {(session.user.role === 'facility_safety_officer' || session.user.role === 'state_cell_analyst' || session.user.role === 'national_analyst') && (
                <div className="action-row">
                  <button onClick={() => void reviewSubmission(submission.submission_id, 'reviewed')}>Mark reviewed</button>
                  <button onClick={() => void reviewSubmission(submission.submission_id, 'actioned')}>Mark actioned</button>
                </div>
              )}
            </div>
          ))}
        </Panel>
      </section>

      <section className="panel-grid">
        <Panel title="Trend analytics" subtitle="Longitudinal burden, alerts, and signal velocity">
          {dashboard?.trend?.points?.length ? (
            <>
              <TrendChart points={dashboard.trend.points} />
              <div className="chips">
                {dashboard.indicators.map((indicator) => <span key={indicator.label} className="chip">{indicator.label}: {indicator.value}</span>)}
              </div>
            </>
          ) : <p>No trend data recorded yet.</p>}
        </Panel>

        <Panel title="Notifications and alerts" subtitle="Escalation messaging and signal attention">
          <div className="alert-stack">
            {dashboard?.alerts.map((alert) => (
              <div key={alert.alert_id} className="trace-step">
                <strong>{alert.title}</strong>
                <p>{alert.detail}</p>
                <small>{alert.owner_role} | {alert.severity}</small>
              </div>
            ))}
            {notifications.map((notification) => (
              <div key={notification.notification_id} className="trace-step">
                <strong>{notification.title}</strong>
                <p>{notification.message}</p>
                <small>{notification.status} | {new Date(notification.created_at).toLocaleString()}</small>
                <div className="action-row">
                  <button onClick={() => void acknowledgeNotification(notification.notification_id, 'acknowledged')}>Acknowledge</button>
                  <button onClick={() => void acknowledgeNotification(notification.notification_id, 'closed')}>Close</button>
                </div>
              </div>
            ))}
          </div>
        </Panel>
      </section>

      <section className="panel-grid">
        <Panel title="Governance and audit" subtitle="Policy state, audit trail, and operating context">
          <div className="subsection">
            <h3>Policies</h3>
            {policies.map((policy) => <div key={policy.policy_id} className="policy-row"><strong>{policy.title}</strong><small>{policy.state} | {policy.validation_phase}</small></div>)}
          </div>
          <div className="subsection">
            <h3>Audit trail</h3>
            {auditLogs.map((log) => <div key={log.audit_id} className="policy-row"><strong>{log.action}</strong><small>{log.entity_type}:{log.entity_id} | {log.detail}</small></div>)}
          </div>
          <div className="subsection">
            <h3>Integration profile</h3>
            {integrationProfile && (
              <div className="chips">
                <span className="chip">{integrationProfile.deployment_model}</span>
                {integrationProfile.standards.map((item) => <span key={item} className="chip">{item}</span>)}
              </div>
            )}
          </div>
        </Panel>

        <Panel title="Network and administration" subtitle="State cells, facility map, and account control">
          <div className="subsection">
            <h3>State cells</h3>
            {stateCells.map((cell) => <div key={cell.state_cell_id} className="policy-row"><strong>{cell.state}</strong><small>{cell.status} | {cell.facilities_mapped} facilities</small></div>)}
          </div>
          <div className="subsection">
            <h3>Facilities</h3>
            {facilities.map((facility) => <div key={facility.facility_id} className="policy-row"><strong>{facility.name}</strong><small>{facility.district}, {facility.state}</small></div>)}
          </div>
          {canCreateUsers && (
            <div className="subsection">
              <h3>Create user</h3>
              <form className="daily-form" onSubmit={createUser}>
                <label>Name<input value={userForm.name} onChange={(e) => setUserForm({ ...userForm, name: e.target.value })} /></label>
                <label>Username<input value={userForm.username} onChange={(e) => setUserForm({ ...userForm, username: e.target.value })} /></label>
                <label>Password<input value={userForm.password} onChange={(e) => setUserForm({ ...userForm, password: e.target.value })} /></label>
                <label>Role<select value={userForm.role} onChange={(e) => setUserForm({ ...userForm, role: e.target.value })}>
                  <option value="facility_reporter">Facility reporter</option>
                  <option value="facility_safety_officer">Facility safety officer</option>
                  <option value="district_reviewer">District reviewer</option>
                  <option value="state_cell_analyst">State cell analyst</option>
                  <option value="national_analyst">National analyst</option>
                  <option value="governance_admin">Governance admin</option>
                </select></label>
                <label>Facility<select value={userForm.facility_id} onChange={(e) => setUserForm({ ...userForm, facility_id: e.target.value })}><option value="">Select</option>{facilities.map((item) => <option key={item.facility_id} value={item.facility_id}>{item.name}</option>)}</select></label>
                <label>Department<select value={userForm.department_id} onChange={(e) => setUserForm({ ...userForm, department_id: e.target.value })}><option value="">Select</option>{departments.map((item) => <option key={item.department_id} value={item.department_id}>{item.name}</option>)}</select></label>
                <label>State<input value={userForm.state} onChange={(e) => setUserForm({ ...userForm, state: e.target.value })} /></label>
                <label>District<input value={userForm.district} onChange={(e) => setUserForm({ ...userForm, district: e.target.value })} /></label>
                <button type="submit">Create account</button>
              </form>
              <div className="user-list">
                {users.map((item) => <div key={item.user_id} className="policy-row"><strong>{item.username || item.name}</strong><small>{item.role} | {item.facility_id || item.state || 'national'}</small></div>)}
              </div>
            </div>
          )}
        </Panel>
      </section>
    </div>
  );
}

function humanize(value: string) {
  return value.replace(/_/g, ' ').replace(/\b\w/g, (char) => char.toUpperCase());
}

function Panel(props: { title: string; subtitle: string; children: React.ReactNode }) {
  return <div className="panel"><div className="panel-head"><h2>{props.title}</h2><p>{props.subtitle}</p></div>{props.children}</div>;
}

function Metric(props: { label: string; value: number }) {
  return <div className="metric-card"><span>{props.label}</span><strong>{props.value}</strong></div>;
}

function TrendChart(props: { points: TrendPoint[] }) {
  const width = 420;
  const height = 180;
  const maxValue = Math.max(1, ...props.points.map((point) => Math.max(point.near_misses, point.harm_events, point.severe_events)));
  const pathFor = (selector: (point: TrendPoint) => number) => props.points.map((point, index) => {
    const x = props.points.length === 1 ? width / 2 : (index / (props.points.length - 1)) * width;
    const y = height - (selector(point) / maxValue) * (height - 20);
    return `${index === 0 ? 'M' : 'L'} ${x} ${y}`;
  }).join(' ');

  return (
    <div className="trend-shell">
      <svg viewBox={`0 0 ${width} ${height}`} className="trend-chart">
        <path d={pathFor((point) => point.near_misses)} className="line near" />
        <path d={pathFor((point) => point.harm_events)} className="line harm" />
        <path d={pathFor((point) => point.severe_events)} className="line severe" />
      </svg>
      <div className="chips">
        <span className="chip">Near misses</span>
        <span className="chip">Harm events</span>
        <span className="chip">Severe events</span>
      </div>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')!).render(<React.StrictMode><App /></React.StrictMode>);
