import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || '';

const api = axios.create({ baseURL: API_BASE });

// Split raw text by --- delimiter into an array of job descriptions
export function splitJobDescriptions(raw) {
  return raw
    .split(/\n---\n|\n-{3,}\n/)
    .map((j) => j.trim())
    .filter(Boolean);
}

export async function matchJobs(resume, jobDescriptions) {
  const { data } = await api.post('/api/jobs/match', {
    resume,
    job_descriptions: jobDescriptions,
  });
  return data.matches;
}

export async function generateCoverLetter(profile, jobDescription, tone = 'professional') {
  const { data } = await api.post('/api/cover-letter/generate', {
    candidate_profile: profile,
    job_description: jobDescription,
    tone,
  });
  return data.cover_letter;
}

export async function generateInterviewPrep(profile, jobDescription) {
  const { data } = await api.post('/api/interview-prep/generate', {
    candidate_profile: profile,
    job_description: jobDescription,
  });
  return data.categories;
}
