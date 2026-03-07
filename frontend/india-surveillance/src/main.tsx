import React, { useEffect, useMemo, useState } from 'react';
import ReactDOM from 'react-dom/client';
import './styles.css';

type AnyObj = Record<string, any>;
const env = (import.meta as ImportMeta & { env: { VITE_INDIA_SURVEILLANCE_API_BASE?: string } }).env;
const apiBase = window.location.protocol === 'https:' ? '/api' : (env.VITE_INDIA_SURVEILLANCE_API_BASE || 'http://127.0.0.1:8010');
const sessionKey = 'india-surveillance-session';

async function api<T>(path: string, token?: string, options?: RequestInit): Promise<T> {
  const headers: HeadersInit = { 'Content-Type': 'application/json', ...(options?.headers || {}) };
  if (token) headers.Authorization = `Bearer ${token}`;
  const response = await fetch(`${apiBase}${path}`, { ...options, headers });
  if (!response.ok) throw new Error(await response.text());
  return response.json();
}

function parseError(error: unknown): string {
  if (!(error instanceof Error)) return 'Request failed';
  if (error.message.includes('Failed to fetch')) return 'Unable to reach the surveillance API';
  try { return JSON.parse(error.message).detail || error.message; } catch { return error.message; }
}

function humanize(value: string) { return value.replace(/_/g, ' ').replace(/\b\w/g, (m) => m.toUpperCase()); }

function App() {
  const [session, setSession] = useState<any>(() => {
    const raw = window.localStorage.getItem(sessionKey); return raw ? JSON.parse(raw) : null;
  });
  const [username, setUsername] = useState('tmk-ed');
  const [password, setPassword] = useState('pass123');
  const [loginError, setLoginError] = useState('');
  const [errorBanner, setErrorBanner] = useState('');
  const [notice, setNotice] = useState('');
  const [installPrompt, setInstallPrompt] = useState<any>(null);
  const [activeView, setActiveView] = useState('dashboard');
  const [data, setData] = useState<AnyObj>({ facilities: [], departments: [], submissions: [], reports: [], eventCases: [], notifications: [], policies: [], auditLogs: [], users: [], stateCells: [], aiCatalog: [], aiConfigs: [] });
  const [trace, setTrace] = useState<any>(null);
  const [selectedReportId, setSelectedReportId] = useState('');
  const [aiResult, setAiResult] = useState<any>(null);
  const [reportSearch, setReportSearch] = useState('');
  const [reportSeverity, setReportSeverity] = useState('all');
  const [caseSearch, setCaseSearch] = useState('');
  const [caseSeverity, setCaseSeverity] = useState('all');
  const [dailyForm, setDailyForm] = useState<any>({ department_id: '', patient_days: 100, admissions: 30, discharges: 25, critical_results_count: 0, near_misses: 0, no_harm_events: 0, harm_events: 0, severe_events: 0, medication_events: 0, procedure_events: 0, infection_events: 0, diagnostic_events: 0, staffing_shortfall_flag: false, crowding_flag: false, system_downtime_flag: false, escalation_required: false, notes: '' });
  const [caseForm, setCaseForm] = useState<any>({ department_id: '', event_timestamp: new Date().toISOString().slice(0, 16), encounter_setting: 'emergency', shift: 'morning', patient_age_band: '18-44', patient_sex: 'female', domain: 'medication', deviation_class: 'contradiction', process_stage: '', event_type: '', actual_harm: '', potential_harm: '', severity_level: 'moderate', event_summary: '', what_was_expected: '', what_happened: '', immediate_action_taken: '', evidence_source: 'manual narrative' });
  const [caseReview, setCaseReview] = useState<any>({ triage_status: 'triaged', owner_assigned: '', investigation_method: 'desk review', root_cause_category: '', corrective_action: '', preventive_action: '', closure_status: 'open', closure_quality_rating: '' });
  const [triage, setTriage] = useState<any>({ status: 'triaged', assigned_to: '', state_cell: '' });
  const [userForm, setUserForm] = useState<any>({ name: '', username: '', password: 'pass123', role: 'facility_reporter', facility_id: '', department_id: '', state: '', district: '' });
  const [aiConfig, setAiConfig] = useState<any>({ provider: 'openai', label: 'Primary AI workflow', model: 'gpt-4.1-mini', api_key: '', base_url: '' });
  const [aiAssist, setAiAssist] = useState<any>({ case_id: '', event_summary: '', what_happened: '', immediate_action_taken: '' });

  const role = session?.user?.role || '';
  const canManageReports = ['facility_safety_officer', 'state_cell_analyst', 'national_analyst'].includes(role);
  const canReviewCases = ['facility_safety_officer', 'district_reviewer', 'state_cell_analyst', 'national_analyst'].includes(role);
  const canSubmitCases = ['facility_reporter', 'facility_safety_officer', 'district_reviewer', 'state_cell_analyst', 'national_analyst'].includes(role);
  const canCreateUsers = ['facility_safety_officer', 'state_cell_analyst', 'national_analyst', 'governance_admin'].includes(role);
  const provider = useMemo(() => data.aiCatalog.find((item: any) => item.provider === aiConfig.provider), [data.aiCatalog, aiConfig.provider]);
  const filteredReports = useMemo(() => (data.reports || []).filter((report: any) => {
    const matchesSearch = !reportSearch || `${report.report_id} ${report.summary} ${report.domain} ${report.deviation_class}`.toLowerCase().includes(reportSearch.toLowerCase());
    const matchesSeverity = reportSeverity === 'all' || report.severity === reportSeverity;
    return matchesSearch && matchesSeverity;
  }), [data.reports, reportSearch, reportSeverity]);
  const filteredCases = useMemo(() => (data.eventCases || []).filter((item: any) => {
    const matchesSearch = !caseSearch || `${item.case_id} ${item.event_summary} ${item.domain} ${item.deviation_class}`.toLowerCase().includes(caseSearch.toLowerCase());
    const matchesSeverity = caseSeverity === 'all' || item.severity_level === caseSeverity;
    return matchesSearch && matchesSeverity;
  }), [data.eventCases, caseSearch, caseSeverity]);

  async function load(token: string) {
    try {
      const [overview, dashboard, facilities, departments, submissions, reports, eventCases, notifications, policies, auditLogs, users, stateCells, integrationProfile, aiInfo] = await Promise.all([
        api('/overview', token), api('/dashboard', token), api('/facilities', token), api('/departments', token), api('/daily-submissions', token), api('/reports', token), api('/event-cases', token), api('/notifications', token), api('/policies', token), api('/audit-logs?limit=20', token).catch(() => []), api('/users', token), api('/state-cells', token), api('/integration-profile', token), api('/ai/providers', token),
      ]);
      setData({ overview, dashboard, facilities, departments, submissions, reports, eventCases, notifications, policies, auditLogs, users, stateCells, integrationProfile, aiCatalog: aiInfo.catalog, aiConfigs: aiInfo.configs });
      setSelectedReportId((current) => current || reports[0]?.report_id || '');
      setDailyForm((f: any) => ({ ...f, department_id: f.department_id || departments[0]?.department_id || '' }));
      setCaseForm((f: any) => ({ ...f, department_id: f.department_id || departments[0]?.department_id || '' }));
      setUserForm((f: any) => ({ ...f, facility_id: f.facility_id || session?.user?.facility_id || '', state: f.state || session?.user?.state || '' }));
      setAiAssist((f: any) => ({ ...f, case_id: f.case_id || eventCases[0]?.case_id || '' }));
      setErrorBanner('');
      setNotice('');
    } catch (error) { setErrorBanner(parseError(error)); }
  }

  useEffect(() => {
    if ('serviceWorker' in navigator) void navigator.serviceWorker.register('/sw.js');
    const handler = (event: Event) => { event.preventDefault(); setInstallPrompt(event); };
    window.addEventListener('beforeinstallprompt', handler);
    return () => window.removeEventListener('beforeinstallprompt', handler);
  }, []);

  useEffect(() => {
    if (!session) { window.localStorage.removeItem(sessionKey); return; }
    window.localStorage.setItem(sessionKey, JSON.stringify(session));
    void load(session.access_token);
  }, [session]);

  useEffect(() => {
    if (!session || !selectedReportId) return;
    void api(`/trace/${selectedReportId}`, session.access_token).then(setTrace).catch((error) => setErrorBanner(parseError(error)));
  }, [session, selectedReportId]);

  async function doLogin(event: React.FormEvent) {
    event.preventDefault();
    try { setSession(await api('/auth/login', undefined, { method: 'POST', body: JSON.stringify({ username, password }) })); setLoginError(''); }
    catch (error) { setLoginError(parseError(error)); }
  }

  async function submitDaily(event: React.FormEvent) {
    event.preventDefault(); if (!session) return;
    await api('/daily-submissions', session.access_token, { method: 'POST', body: JSON.stringify({ submission_date: new Date().toISOString().slice(0, 10), ...dailyForm }) });
    setNotice('Daily surveillance submission recorded.');
    await load(session.access_token);
  }
  async function submitCase(event: React.FormEvent) {
    event.preventDefault(); if (!session) return;
    await api('/event-cases', session.access_token, { method: 'POST', body: JSON.stringify({ ...caseForm, event_timestamp: new Date(caseForm.event_timestamp).toISOString() }) });
    setNotice('Event case created.');
    setActiveView('cases');
    await load(session.access_token);
  }
  async function reviewSubmission(id: string, status: string) {
    if (!session) return; await api(`/daily-submissions/${id}/review`, session.access_token, { method: 'POST', body: JSON.stringify({ review_status: status, reviewed_by: session.user.name, notes: `Marked ${status}` }) }); setNotice(`Submission marked ${status}.`); await load(session.access_token);
  }
  async function reviewCase(id: string) {
    if (!session) return; await api(`/event-cases/${id}/review`, session.access_token, { method: 'POST', body: JSON.stringify(caseReview) }); setNotice('Case review saved.'); await load(session.access_token);
  }
  async function triageReport(id: string) {
    if (!session) return; await api(`/reports/${id}/triage`, session.access_token, { method: 'POST', body: JSON.stringify(triage) }); setNotice('Report triage updated.'); await load(session.access_token);
  }
  async function closeReport(id: string) {
    if (!session) return; await api(`/reports/${id}/close`, session.access_token, { method: 'POST', body: JSON.stringify({ closure_note: `Closed by ${session.user.name}` }) }); setNotice('Report closed.'); await load(session.access_token);
  }
  async function createUser(event: React.FormEvent) {
    event.preventDefault(); if (!session) return;
    await api('/users', session.access_token, { method: 'POST', body: JSON.stringify(userForm) }); setNotice('User account created.'); setUserForm((f: any) => ({ ...f, name: '', username: '', department_id: '' })); await load(session.access_token);
  }
  async function acknowledge(id: string, status: string) {
    if (!session) return; await api(`/notifications/${id}/acknowledge`, session.access_token, { method: 'POST', body: JSON.stringify({ status }) }); setNotice(`Notification ${status}.`); await load(session.access_token);
  }
  async function saveAiConfig(event: React.FormEvent) {
    event.preventDefault(); if (!session) return;
    await api('/ai/providers', session.access_token, { method: 'POST', body: JSON.stringify(aiConfig) }); setNotice('AI provider configuration saved.'); setAiConfig((f: any) => ({ ...f, api_key: '' })); await load(session.access_token);
  }
  async function runAiAssist(event: React.FormEvent) {
    event.preventDefault(); if (!session) return;
    setAiResult(await api('/ai/assist', session.access_token, { method: 'POST', body: JSON.stringify(aiAssist) })); setNotice('AI assistance completed.'); await load(session.access_token);
  }

  if (!session) return <div className="login-shell"><div className="login-panel"><p className="eyebrow">India patient safety surveillance</p><h1>Facility and state login</h1><p className="lede">Departments submit daily data. Managers review cases, CAPA, analytics, and AI-assisted classification.</p><form onSubmit={doLogin} className="login-form"><label>Username<input value={username} onChange={(e) => setUsername(e.target.value)} /></label><label>Password<input type="password" value={password} onChange={(e) => setPassword(e.target.value)} /></label><button type="submit">Login</button></form><div className="demo-credentials"><strong>Seed accounts</strong><small><code>tmk-ed</code>, <code>tmk-icu</code>, <code>ka-fso</code>, <code>state-ka</code>, <code>national</code>, <code>admin</code></small><small>Password: <code>pass123</code></small></div>{loginError && <p className="error-text">{loginError}</p>}</div></div>;

  return <div className="page-shell">
    <header className="hero compact-hero"><div><p className="eyebrow">Logged in as {role}</p><h1>Safety surveillance command center</h1><p className="lede">{session.user.name}</p></div><div className="hero-card"><strong>{session.user.facility_id || session.user.state || 'National scope'}</strong><p>{apiBase}</p><div className="action-row">{installPrompt && <button onClick={() => (installPrompt as any).prompt()}>Install app</button>}<button onClick={() => void load(session.access_token)}>Refresh</button><button onClick={() => setSession(null)}>Logout</button></div></div></header>
    {errorBanner && <section className="error-banner">{errorBanner}</section>}
    {notice && <section className="success-banner">{notice}</section>}
    <nav className="view-nav">
      {[
        ['dashboard', 'Dashboard'],
        ['submissions', 'Submissions'],
        ['cases', 'Cases'],
        ['ai', 'AI'],
        ['governance', 'Governance'],
      ].map(([key, label]) => <button key={key} className={`view-tab ${activeView === key ? 'active' : ''}`} onClick={() => setActiveView(key)}>{label}</button>)}
    </nav>
    {data.dashboard && <section className="metric-grid">{data.dashboard.indicators.slice(0, 6).map((item: any) => <Metric key={item.label} label={item.label} value={item.value} />)}</section>}

    {activeView === 'dashboard' && <section className="panel-grid panel-grid-wide">
      <Panel title="Operations queue" subtitle="Submissions, reports, and high-risk cases needing attention"><div className="chips"><span className="chip">Pending submissions: {data.submissions.filter((x: any) => x.review_status === 'submitted').length}</span><span className="chip">Open reports: {data.reports.filter((x: any) => x.status !== 'closed').length}</span><span className="chip">Open cases: {data.eventCases.filter((x: any) => x.closure_status !== 'closed').length}</span><span className="chip">High-risk cases: {data.eventCases.filter((x: any) => ['severe', 'sentinel'].includes(x.severity_level)).length}</span></div><div className="report-filters"><label>Search<input value={reportSearch} onChange={(e) => setReportSearch(e.target.value)} placeholder="ID, domain, summary" /></label><label>Severity<select value={reportSeverity} onChange={(e) => setReportSeverity(e.target.value)}><option value="all">All</option><option value="moderate">Moderate</option><option value="severe">Severe</option><option value="sentinel">Sentinel</option></select></label></div><div className="report-list">{filteredReports.map((report: any) => <button key={report.report_id} className={`report-card selectable ${selectedReportId === report.report_id ? 'selected' : ''}`} onClick={() => setSelectedReportId(report.report_id)}><div className="report-header"><span>{report.report_id}</span><span className={`pill severity-${report.severity}`}>{report.severity}</span></div><strong>{humanize(report.domain)} / {humanize(report.deviation_class)}</strong><p>{report.summary}</p><small>{report.status} | {report.assigned_to || 'unassigned'}</small></button>)}</div>{canManageReports && selectedReportId && <div className="subsection action-block"><h3>Report action</h3><div className="daily-form"><label>Status<select value={triage.status} onChange={(e) => setTriage({ ...triage, status: e.target.value })}><option value="triaged">Triaged</option><option value="investigating">Investigating</option></select></label><label>Assigned to<input value={triage.assigned_to} onChange={(e) => setTriage({ ...triage, assigned_to: e.target.value })} /></label><label>State cell<input value={triage.state_cell} onChange={(e) => setTriage({ ...triage, state_cell: e.target.value })} /></label></div><div className="action-row"><button onClick={() => void triageReport(selectedReportId)}>Save triage</button><button onClick={() => void closeReport(selectedReportId)}>Close report</button></div></div>}</Panel>
      <Panel title="Case trace" subtitle="Explainable report path with governance context">{trace ? <><div className="trace-meta"><h3>{trace.report_id}</h3><p>{trace.facility}, {trace.district}, {trace.state}</p></div><div className="trace-steps">{trace.trace_steps.map((step: any) => <div key={step.step} className="trace-step"><strong>{humanize(step.step)}</strong><p>{step.finding}</p><small>{step.output}</small></div>)}</div></> : <p>Select a report to inspect its trace.</p>}</Panel>
    </section>}

    {activeView === 'submissions' && <section className="panel-grid">
      <Panel title="Daily surveillance feed" subtitle="Operational burden and denominator reporting">{['facility_reporter', 'facility_safety_officer'].includes(role) ? <form className="daily-form" onSubmit={submitDaily}><label>Department<select value={dailyForm.department_id} onChange={(e) => setDailyForm({ ...dailyForm, department_id: e.target.value })}>{data.departments.map((d: any) => <option key={d.department_id} value={d.department_id}>{d.name}</option>)}</select></label><label>Patient days<input type="number" value={dailyForm.patient_days} onChange={(e) => setDailyForm({ ...dailyForm, patient_days: Number(e.target.value) })} /></label><label>Admissions<input type="number" value={dailyForm.admissions} onChange={(e) => setDailyForm({ ...dailyForm, admissions: Number(e.target.value) })} /></label><label>Near misses<input type="number" value={dailyForm.near_misses} onChange={(e) => setDailyForm({ ...dailyForm, near_misses: Number(e.target.value) })} /></label><label>Harm events<input type="number" value={dailyForm.harm_events} onChange={(e) => setDailyForm({ ...dailyForm, harm_events: Number(e.target.value) })} /></label><label>Severe events<input type="number" value={dailyForm.severe_events} onChange={(e) => setDailyForm({ ...dailyForm, severe_events: Number(e.target.value) })} /></label><label>Notes<textarea value={dailyForm.notes} onChange={(e) => setDailyForm({ ...dailyForm, notes: e.target.value })} /></label><label className="checkbox-row"><input type="checkbox" checked={dailyForm.escalation_required} onChange={(e) => setDailyForm({ ...dailyForm, escalation_required: e.target.checked })} />Escalation required</label><button type="submit">Submit daily surveillance</button></form> : <p>This role reviews submissions rather than creating them.</p>}</Panel>
      <Panel title="Review worklist" subtitle="Daily submissions requiring manager action">{data.submissions.map((item: any) => <div key={item.submission_id} className="report-card"><div className="report-header"><span>{item.submission_id}</span><span className="pill">{item.review_status}</span></div><strong>{data.departments.find((d: any) => d.department_id === item.department_id)?.name || item.department_id}</strong><p>{item.notes || 'No notes recorded.'}</p><small>PD {item.patient_days} | Admissions {item.admissions} | Near misses {item.near_misses}</small>{canManageReports && <div className="action-row"><button onClick={() => void reviewSubmission(item.submission_id, 'reviewed')}>Mark reviewed</button><button onClick={() => void reviewSubmission(item.submission_id, 'actioned')}>Mark actioned</button></div>}</div>)}</Panel>
    </section>}

    {activeView === 'cases' && <section className="panel-grid">
      <Panel title="Event-level case intake" subtitle="National learning dataset and CAPA-ready case creation">{canSubmitCases ? <form className="daily-form" onSubmit={submitCase}><label>Department<select value={caseForm.department_id} onChange={(e) => setCaseForm({ ...caseForm, department_id: e.target.value })}>{data.departments.map((d: any) => <option key={d.department_id} value={d.department_id}>{d.name}</option>)}</select></label><label>Event time<input type="datetime-local" value={caseForm.event_timestamp} onChange={(e) => setCaseForm({ ...caseForm, event_timestamp: e.target.value })} /></label><label>Domain<select value={caseForm.domain} onChange={(e) => setCaseForm({ ...caseForm, domain: e.target.value })}><option value="medication">Medication</option><option value="diagnostic">Diagnostic</option><option value="procedure">Procedure</option><option value="deterioration">Deterioration</option><option value="lab_radiology">Lab/Radiology</option><option value="care_transition">Care transition</option><option value="documentation_communication">Documentation/Communication</option><option value="device_equipment">Device/Equipment</option><option value="operational">Operational</option></select></label><label>Deviation<select value={caseForm.deviation_class} onChange={(e) => setCaseForm({ ...caseForm, deviation_class: e.target.value })}><option value="omission">Omission</option><option value="contradiction">Contradiction</option><option value="harmful_delay">Harmful delay</option><option value="sequencing_mismatch">Sequencing mismatch</option><option value="closure_failure">Closure failure</option></select></label><label>Process stage<input value={caseForm.process_stage} onChange={(e) => setCaseForm({ ...caseForm, process_stage: e.target.value })} /></label><label>Event type<input value={caseForm.event_type} onChange={(e) => setCaseForm({ ...caseForm, event_type: e.target.value })} /></label><label>Summary<textarea value={caseForm.event_summary} onChange={(e) => setCaseForm({ ...caseForm, event_summary: e.target.value })} /></label><label>What happened<textarea value={caseForm.what_happened} onChange={(e) => setCaseForm({ ...caseForm, what_happened: e.target.value })} /></label><label>Immediate action<textarea value={caseForm.immediate_action_taken} onChange={(e) => setCaseForm({ ...caseForm, immediate_action_taken: e.target.value })} /></label><label>Actual harm<input value={caseForm.actual_harm} onChange={(e) => setCaseForm({ ...caseForm, actual_harm: e.target.value })} /></label><label>Potential harm<input value={caseForm.potential_harm} onChange={(e) => setCaseForm({ ...caseForm, potential_harm: e.target.value })} /></label><button type="submit">Create event case</button></form> : <p>This role can review cases but not create them.</p>}</Panel>
      <Panel title="Event-case review and CAPA" subtitle="Investigation ownership, corrective action, and closure quality"><div className="report-filters"><label>Search<input value={caseSearch} onChange={(e) => setCaseSearch(e.target.value)} placeholder="Case ID, domain, summary" /></label><label>Severity<select value={caseSeverity} onChange={(e) => setCaseSeverity(e.target.value)}><option value="all">All</option><option value="moderate">Moderate</option><option value="severe">Severe</option><option value="sentinel">Sentinel</option></select></label></div>{filteredCases.map((item: any) => <div key={item.case_id} className="report-card"><div className="report-header"><span>{item.case_id}</span><span className={`pill severity-${item.severity_level}`}>{item.severity_level}</span></div><strong>{humanize(item.domain)} / {humanize(item.deviation_class)}</strong><p>{item.event_summary}</p><small>{item.triage_status} | {item.owner_assigned || 'unassigned'} | {item.closure_status}</small>{item.ai_summary && <p className="ai-summary">AI: {item.ai_summary}</p>}{canReviewCases && <div className="subsection action-block"><div className="daily-form"><label>Triage<select value={caseReview.triage_status} onChange={(e) => setCaseReview({ ...caseReview, triage_status: e.target.value })}><option value="triaged">Triaged</option><option value="investigating">Investigating</option><option value="actioned">Actioned</option><option value="closed">Closed</option></select></label><label>Owner<input value={caseReview.owner_assigned} onChange={(e) => setCaseReview({ ...caseReview, owner_assigned: e.target.value })} /></label><label>Root cause<input value={caseReview.root_cause_category} onChange={(e) => setCaseReview({ ...caseReview, root_cause_category: e.target.value })} /></label><label>Corrective<textarea value={caseReview.corrective_action} onChange={(e) => setCaseReview({ ...caseReview, corrective_action: e.target.value })} /></label><label>Preventive<textarea value={caseReview.preventive_action} onChange={(e) => setCaseReview({ ...caseReview, preventive_action: e.target.value })} /></label></div><div className="action-row"><button onClick={() => void reviewCase(item.case_id)}>Save case review</button></div></div>}</div>)}</Panel>
    </section>}

    {activeView === 'ai' && <section className="panel-grid">
      <Panel title="Trend analytics" subtitle="National learning indicators and domain burden">{data.dashboard?.trend?.points?.length ? <><TrendChart points={data.dashboard.trend.points} /><div className="chips">{(data.dashboard.trend.domain_breakdown || []).map((x: any) => <span key={x.domain} className="chip">{humanize(x.domain)}: {x.count}</span>)}</div></> : <p>No trend data recorded yet.</p>}</Panel>
      <Panel title="AI configuration and assistance" subtitle="User-supplied API keys, model routing, and case classification"><div className="subsection"><h3>Configured providers</h3><div className="report-list">{data.aiConfigs.map((cfg: any) => <div key={cfg.config_id} className="report-card"><strong>{humanize(cfg.provider)} / {cfg.model}</strong><small>{cfg.api_key_masked} | {cfg.is_active ? 'active' : 'inactive'}</small></div>)}</div></div><div className="subsection"><h3>Add or update provider</h3><form className="daily-form" onSubmit={saveAiConfig}><label>Provider<select value={aiConfig.provider} onChange={(e) => { const match = data.aiCatalog.find((x: any) => x.provider === e.target.value); setAiConfig({ provider: e.target.value, label: match?.label || e.target.value, model: match?.supported_models?.[0] || '', api_key: '', base_url: match?.default_base_url || '' }); }}>{data.aiCatalog.map((item: any) => <option key={item.provider} value={item.provider}>{item.label}</option>)}</select></label><label>Label<input value={aiConfig.label} onChange={(e) => setAiConfig({ ...aiConfig, label: e.target.value })} /></label><label>Model<input value={aiConfig.model} onChange={(e) => setAiConfig({ ...aiConfig, model: e.target.value })} /></label><label>API key<input type="password" value={aiConfig.api_key} onChange={(e) => setAiConfig({ ...aiConfig, api_key: e.target.value })} /></label><button type="submit">Save provider</button></form>{provider && <div className="chips"><a className="chip link-chip" href={provider.auth_url} target="_blank" rel="noreferrer">API keys</a><a className="chip link-chip" href={provider.docs_url} target="_blank" rel="noreferrer">Docs</a></div>}</div><div className="subsection"><h3>AI assist</h3><form className="daily-form" onSubmit={runAiAssist}><label>Case<select value={aiAssist.case_id} onChange={(e) => { const item = data.eventCases.find((x: any) => x.case_id === e.target.value); setAiAssist({ case_id: e.target.value, event_summary: item?.event_summary || '', what_happened: item?.what_happened || '', immediate_action_taken: item?.corrective_action || '' }); }}>{data.eventCases.map((item: any) => <option key={item.case_id} value={item.case_id}>{item.case_id}</option>)}</select></label><label>Summary<textarea value={aiAssist.event_summary} onChange={(e) => setAiAssist({ ...aiAssist, event_summary: e.target.value })} /></label><label>What happened<textarea value={aiAssist.what_happened} onChange={(e) => setAiAssist({ ...aiAssist, what_happened: e.target.value })} /></label><button type="submit">Run AI assist</button></form>{aiResult && <div className="trace-step"><strong>{humanize(aiResult.provider)} / {aiResult.model}</strong><p>{aiResult.summary}</p><small>Confidence {Math.round(aiResult.confidence * 100)}%</small><pre className="json-block">{JSON.stringify(aiResult.structured_fields, null, 2)}</pre></div>}</div></Panel>
    </section>}

    {activeView === 'governance' && <section className="panel-grid">
      <Panel title="Notifications and alerts" subtitle="Escalation messaging, policy exceptions, and queue attention"><div className="alert-stack">{(data.dashboard?.alerts || []).map((alert: any) => <div key={alert.alert_id} className="trace-step"><strong>{alert.title}</strong><p>{alert.detail}</p><small>{alert.owner_role} | {alert.severity}</small></div>)}{data.notifications.map((note: any) => <div key={note.notification_id} className="trace-step"><strong>{note.title}</strong><p>{note.message}</p><small>{note.status}</small><div className="action-row"><button onClick={() => void acknowledge(note.notification_id, 'acknowledged')}>Acknowledge</button><button onClick={() => void acknowledge(note.notification_id, 'closed')}>Close</button></div></div>)}</div></Panel>
      <Panel title="Governance, network, and administration" subtitle="Policies, audits, state cells, facilities, and live account management"><div className="subsection"><h3>Policies</h3>{data.policies.map((p: any) => <div key={p.policy_id} className="policy-row"><strong>{p.title}</strong><small>{p.state} | {p.validation_phase}</small></div>)}</div><div className="subsection"><h3>Audit trail</h3>{data.auditLogs.map((log: any) => <div key={log.audit_id} className="policy-row"><strong>{log.action}</strong><small>{log.entity_type}:{log.entity_id} | {log.detail}</small></div>)}</div><div className="subsection"><h3>State cells</h3>{data.stateCells.map((cell: any) => <div key={cell.state_cell_id} className="policy-row"><strong>{cell.state}</strong><small>{cell.status} | {cell.facilities_mapped} facilities</small></div>)}</div>{canCreateUsers && <div className="subsection"><h3>Create user</h3><form className="daily-form" onSubmit={createUser}><label>Name<input value={userForm.name} onChange={(e) => setUserForm({ ...userForm, name: e.target.value })} /></label><label>Username<input value={userForm.username} onChange={(e) => setUserForm({ ...userForm, username: e.target.value })} /></label><label>Password<input value={userForm.password} onChange={(e) => setUserForm({ ...userForm, password: e.target.value })} /></label><label>Role<select value={userForm.role} onChange={(e) => setUserForm({ ...userForm, role: e.target.value })}><option value="facility_reporter">Facility reporter</option><option value="facility_safety_officer">Facility safety officer</option><option value="district_reviewer">District reviewer</option><option value="state_cell_analyst">State cell analyst</option><option value="national_analyst">National analyst</option><option value="governance_admin">Governance admin</option></select></label><label>Facility<select value={userForm.facility_id} onChange={(e) => setUserForm({ ...userForm, facility_id: e.target.value })}><option value="">Select</option>{data.facilities.map((item: any) => <option key={item.facility_id} value={item.facility_id}>{item.name}</option>)}</select></label><label>Department<select value={userForm.department_id} onChange={(e) => setUserForm({ ...userForm, department_id: e.target.value })}><option value="">Select</option>{data.departments.map((item: any) => <option key={item.department_id} value={item.department_id}>{item.name}</option>)}</select></label><button type="submit">Create account</button></form><div className="user-list">{data.users.map((item: any) => <div key={item.user_id} className="policy-row"><strong>{item.username || item.name}</strong><small>{item.role} | {item.facility_id || item.state || 'national'}</small></div>)}</div></div>}</Panel>
    </section>}
  </div>;
}

function Panel(props: { title: string; subtitle: string; children: React.ReactNode }) { return <div className="panel"><div className="panel-head"><h2>{props.title}</h2><p>{props.subtitle}</p></div>{props.children}</div>; }
function Metric(props: { label: string; value: number }) { return <div className="metric-card"><span>{props.label}</span><strong>{props.value}</strong></div>; }
function TrendChart(props: { points: any[] }) {
  const width = 420; const height = 180;
  const maxValue = Math.max(1, ...props.points.map((p) => Math.max(p.near_misses, p.harm_events, p.severe_events, p.event_cases)));
  const pathFor = (selector: (point: any) => number) => props.points.map((point, index) => { const x = props.points.length === 1 ? width / 2 : (index / (props.points.length - 1)) * width; const y = height - (selector(point) / maxValue) * (height - 20); return `${index === 0 ? 'M' : 'L'} ${x} ${y}`; }).join(' ');
  return <div className="trend-shell"><svg viewBox={`0 0 ${width} ${height}`} className="trend-chart"><path d={pathFor((p) => p.near_misses)} className="line near" /><path d={pathFor((p) => p.harm_events)} className="line harm" /><path d={pathFor((p) => p.severe_events)} className="line severe" /><path d={pathFor((p) => p.event_cases)} className="line case" /></svg><div className="chips"><span className="chip">Near misses</span><span className="chip">Harm events</span><span className="chip">Severe events</span><span className="chip">Event cases</span></div></div>;
}

ReactDOM.createRoot(document.getElementById('root')!).render(<React.StrictMode><App /></React.StrictMode>);
