import React, { useState } from 'react';
import JobMatcher from './components/JobMatcher';
import CoverLetter from './components/CoverLetter';
import InterviewPrep from './components/InterviewPrep';
import './App.css';

const TABS = [
  { id: 'match', label: '🔍 Match Jobs' },
  { id: 'cover', label: '📝 Cover Letter' },
  { id: 'prep', label: '🎤 Interview Prep' },
];

export default function App() {
  const [activeTab, setActiveTab] = useState('match');
  const [prefill, setPrefill] = useState(null);

  function handleSelectJob(tab, job) {
    setPrefill(job);
    setActiveTab(tab);
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>AI Job Recommendation Engine</h1>
        <p>RAG-powered matching · Cover letter generation · Interview prep</p>
      </header>

      <nav className="tabs">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            className={`tab ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </nav>

      <main className="content">
        {activeTab === 'match' && <JobMatcher onSelectJob={handleSelectJob} />}
        {activeTab === 'cover' && <CoverLetter prefill={prefill} />}
        {activeTab === 'prep' && <InterviewPrep prefill={prefill} />}
      </main>
    </div>
  );
}
