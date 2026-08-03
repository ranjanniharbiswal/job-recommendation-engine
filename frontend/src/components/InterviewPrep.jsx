import React, { useState } from 'react';
import { generateInterviewPrep } from '../services/api';

const CATEGORY_ICONS = {
  Behavioral: '🤝',
  Technical: '💻',
  Situational: '🧠',
};

export default function InterviewPrep({ prefill }) {
  const [profile, setProfile] = useState('');
  const [job, setJob] = useState(prefill ? `${prefill.title} at ${prefill.company}` : '');
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function handleGenerate() {
    setError('');
    if (!profile.trim() || !job.trim()) {
      setError('Please enter your background and the job role.');
      return;
    }
    setLoading(true);
    try {
      const result = await generateInterviewPrep(profile, job);
      setCategories(result);
    } catch (e) {
      setError(e?.response?.data?.detail || 'Something went wrong.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="panel">
      <div className="field">
        <label>Your background</label>
        <textarea
          rows={3}
          value={profile}
          onChange={(e) => setProfile(e.target.value)}
          placeholder="Your skills, experience, and career level..."
        />
      </div>
      <div className="field">
        <label>Job role</label>
        <textarea
          rows={3}
          value={job}
          onChange={(e) => setJob(e.target.value)}
          placeholder="Job title, company, and key requirements..."
        />
      </div>
      {error && <p className="error">{error}</p>}
      <button className="btn primary" onClick={handleGenerate} disabled={loading}>
        {loading ? 'Generating…' : 'Generate Questions →'}
      </button>

      {categories.length > 0 && (
        <div className="results">
          {categories.map((cat, i) => (
            <div key={i} className="category-section">
              <h3>{CATEGORY_ICONS[cat.name] || '❓'} {cat.name}</h3>
              <div className="question-list">
                {cat.questions.map((q, j) => (
                  <div key={j} className="question-item">{q}</div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
