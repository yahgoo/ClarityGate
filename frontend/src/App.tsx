import { useState } from 'react';
import type { AnalysisResponse, Finding } from './types';
import { analyzeSpec } from './api';

const SAMPLE_SPEC = `# Login Requirements

The system shall authenticate users via email and password.
The system should support password reset.
The system may log failed attempts.
The system shall lock accounts after 5 failed attempts within 10 minutes.
`;

type Severity = 'defect' | 'clarification' | 'info';

const SEVERITY_LABELS: Record<Severity, string> = {
  defect: 'Defect',
  clarification: 'Clarification',
  info: 'Info',
};

export default function App() {
  const [filename, setFilename] = useState('requirements.md');
  const [rawText, setRawText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [severityFilter, setSeverityFilter] = useState<Severity | 'all'>('all');

  const handleAnalyze = async () => {
    if (!rawText.trim()) {
      setError('Please paste requirements text before analyzing.');
      return;
    }
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await analyzeSpec(filename.trim() || 'requirements.md', rawText);
      setResult(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Unable to reach the ClarityGate backend. Is it running on localhost:8000?',
      );
    } finally {
      setLoading(false);
    }
  };

  const filteredFindings: Finding[] = result
    ? severityFilter === 'all'
      ? result.findings
      : result.findings.filter((f) => f.severity === severityFilter)
    : [];

  return (
    <div className="app">
      <header className="header">
        <h1 className="header-title">ClarityGate</h1>
        <span className="header-subtitle">Requirements Quality Gate</span>
      </header>

      <main className="main">
        {/* Left panel: Import */}
        <section className="panel panel-import">
          <h2 className="panel-title">Import Spec</h2>
          <label className="field-label" htmlFor="filename">
            Filename
          </label>
          <input
            id="filename"
            className="input"
            type="text"
            value={filename}
            onChange={(e) => setFilename(e.target.value)}
            placeholder="requirements.md"
          />
          <label className="field-label" htmlFor="spec-text">
            Requirements Markdown
          </label>
          <textarea
            id="spec-text"
            className="textarea"
            value={rawText}
            onChange={(e) => setRawText(e.target.value)}
            placeholder={SAMPLE_SPEC}
            rows={14}
          />
          <button
            className="btn btn-primary"
            onClick={handleAnalyze}
            disabled={loading}
          >
            {loading ? 'Analyzing…' : 'Analyze'}
          </button>
        </section>

        {/* Right panel: Results */}
        <section className="panel panel-results">
          {error && (
            <div className="alert alert-error">
              <strong>Error:</strong> {error}
            </div>
          )}

          {!result && !error && !loading && (
            <div className="empty-state">
              <p>Paste a requirements spec and click <strong>Analyze</strong> to see quality results.</p>
            </div>
          )}

          {loading && (
            <div className="empty-state">
              <p>Running deterministic checks…</p>
            </div>
          )}

          {result && (
            <>
              {/* Score card */}
              <div className={`score-card score-${result.verdict.toLowerCase()}`}>
                <div className="score-number">{result.score}</div>
                <div className="score-meta">
                  <span className={`verdict-badge verdict-${result.verdict.toLowerCase()}`}>
                    {result.verdict}
                  </span>
                  <span className="tier-label">Tier: {result.tier}</span>
                </div>
              </div>

              {/* Stats row */}
              <div className="stats-row">
                <div className="stat">
                  <span className="stat-value">{result.requirement_count}</span>
                  <span className="stat-label">Requirements</span>
                </div>
                <div className="stat stat-defect">
                  <span className="stat-value">{result.defects}</span>
                  <span className="stat-label">Defects</span>
                </div>
                <div className="stat stat-clarification">
                  <span className="stat-value">{result.clarifications}</span>
                  <span className="stat-label">Clarifications</span>
                </div>
                <div className="stat stat-info">
                  <span className="stat-value">{result.infos}</span>
                  <span className="stat-label">Info</span>
                </div>
              </div>

              {/* Findings */}
              <div className="findings-section">
                <div className="findings-header">
                  <h3>Findings ({filteredFindings.length})</h3>
                  <select
                    className="select"
                    value={severityFilter}
                    onChange={(e) => setSeverityFilter(e.target.value as Severity | 'all')}
                  >
                    <option value="all">All severities</option>
                    <option value="defect">Defects</option>
                    <option value="clarification">Clarifications</option>
                    <option value="info">Info</option>
                  </select>
                </div>

                {filteredFindings.length === 0 ? (
                  <p className="no-findings">No findings for this filter.</p>
                ) : (
                  <ul className="findings-list">
                    {filteredFindings.map((f, i) => (
                      <li key={`${f.check_id}-${f.line_number}-${i}`} className={`finding finding-${f.severity}`}>
                        <div className="finding-top">
                          <span className={`badge badge-${f.severity}`}>
                            {SEVERITY_LABELS[f.severity as Severity] ?? f.severity}
                          </span>
                          <span className="finding-check">{f.check_id}</span>
                          <span className="finding-line">Line {f.line_number}</span>
                        </div>
                        <p className="finding-message">{f.message}</p>
                        {f.suggested_rewrite && (
                          <code className="finding-suggestion">{f.suggested_rewrite}</code>
                        )}
                      </li>
                    ))}
                  </ul>
                )}
              </div>

              {/* Requirements list */}
              <details className="details-block">
                <summary>Parsed Requirements ({result.requirements.length})</summary>
                <ul className="req-list">
                  {result.requirements.map((r) => (
                    <li key={r.line_number} className="req-item">
                      <span className="req-line">L{r.line_number}</span>
                      <span className="req-text">{r.raw_text}</span>
                    </li>
                  ))}
                </ul>
              </details>

              {/* Report preview */}
              <details className="details-block">
                <summary>Full Report (Markdown)</summary>
                <pre className="report-pre">{result.report_markdown}</pre>
              </details>
            </>
          )}
        </section>
      </main>
    </div>
  );
}
