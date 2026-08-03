import React, { useState } from 'react';
import { matchJobs, splitJobDescriptions } from '../services/api';

export default function JobMatcher({ onSelectJob }) {
  const [resume, setResume] = useState('');
  const [jobsRaw, setJobsRaw] = useState('');
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function handleMatch() {
    setError('');
    const jobs = splitJobDescriptions(jobsRaw);
    if (!resume.trim() || !jobs.length) {
      setError('Please enter both your resume and at least one job description.');
      return;
    }
    setLoading(true);
    try {
      const results = await matchJobs(resume, jobs);
      setMatches(results);
    } catch (e) {
      setError(e?.response?.data?.detail || 'Something went wrong. Check your API key.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="panel">
      <div className="field">
        <label>Your resume / candidate profile</label>
        <textarea
          rows={6}
          value={resume}
          onChange={(e) => setResume(e.target.value)}
          placeholder="Paste your resume or a summary of your skills and experience..."
        />
      </div>
      <div className="field">
        <label>Job listings (separate multiple jobs with --- on its own line)</label>
        <textarea
          rows={8}
          value={jobsRaw}
          onChange={(e) => setJobsRaw(e.target.value)}
          placeholder="Paste job descriptions here. Separate multiple jobs with:&#10;---"
        />
      </div>
      {error && <p className="error">{error}</p>}
      <button className="btn primary" onClick={handleMatch} disabled={loading}>
        {loading ? 'Matching…' : 'Find Matches →'}
      </button>

      {matches.length > 0 && (
        <div className="results">
          <h3>{matches.length} match{matches.length !== 1 ? 'es' : ''} found</h3>
          {matches.map((m, i) => (
            <div key={i} className={`job-card ${i === 0 ? 'featured' : ''}`}>
              {i === 0 && <span className="best-badge">Best match</span>}
              <div className="job-header">
                <div>
                  <div className="job-title">{m.title}</div>
                  <div className="job-company">{m.company}</div>
                </div>
                <div className="score-wrap">
                  <span className={`score ${m.score >= 80 ? 'high' : 'mid'}`}>
                    {Math.round(m.score)}%
                  </span>
                  <div className="bar">
                    <div className="fill" style={{ width: `${m.score}%` }} />
                  </div>
                </div>
              </div>
              <div className="tags">
                {m.skills.map((s, j) => <span key={j} className="tag">{s}</span>)}
              </div>
              <p className="reason">{m.reason}</p>
              {m.gap && <p className="gap">⚠ Gap: {m.gap}</p>}
              <div className="card-actions">
                <button className="btn sm" onClick={() => onSelectJob('cover', m)}>
                  Cover Letter
                </button>
                <button className="btn sm" onClick={() => onSelectJob('prep', m)}>
                  Interview Prep
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
