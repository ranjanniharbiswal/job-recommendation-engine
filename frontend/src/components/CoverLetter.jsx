import React, { useState } from 'react';
import { generateCoverLetter } from '../services/api';

export default function CoverLetter({ prefill }) {
  const [profile, setProfile] = useState('');
  const [job, setJob] = useState(prefill ? `${prefill.title} at ${prefill.company}` : '');
  const [tone, setTone] = useState('professional');
  const [letter, setLetter] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [copied, setCopied] = useState(false);

  async function handleGenerate() {
    setError('');
    if (!profile.trim() || !job.trim()) {
      setError('Please enter your profile and the job description.');
      return;
    }
    setLoading(true);
    try {
      const result = await generateCoverLetter(profile, job, tone);
      setLetter(result);
    } catch (e) {
      setError(e?.response?.data?.detail || 'Something went wrong.');
    } finally {
      setLoading(false);
    }
  }

  function handleCopy() {
    navigator.clipboard.writeText(letter);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  }

  return (
    <div className="panel">
      <div className="field">
        <label>Your profile</label>
        <textarea
          rows={4}
          value={profile}
          onChange={(e) => setProfile(e.target.value)}
          placeholder="Brief summary of your background, skills, and experience..."
        />
      </div>
      <div className="field">
        <label>Job title and description</label>
        <textarea
          rows={4}
          value={job}
          onChange={(e) => setJob(e.target.value)}
          placeholder="Job title, company, and key requirements..."
        />
      </div>
      <div className="field row">
        <label>Tone</label>
        <select value={tone} onChange={(e) => setTone(e.target.value)}>
          <option value="professional">Professional</option>
          <option value="enthusiastic">Enthusiastic</option>
          <option value="concise">Concise</option>
          <option value="creative">Creative</option>
        </select>
      </div>
      {error && <p className="error">{error}</p>}
      <button className="btn primary" onClick={handleGenerate} disabled={loading}>
        {loading ? 'Generating…' : 'Generate Cover Letter →'}
      </button>

      {letter && (
        <div className="output-section">
          <div className="output-header">
            <h3>Your cover letter</h3>
            <button className="btn sm" onClick={handleCopy}>
              {copied ? '✓ Copied' : 'Copy'}
            </button>
          </div>
          <div className="output-box">{letter}</div>
        </div>
      )}
    </div>
  );
}
