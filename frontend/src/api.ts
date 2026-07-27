import type { AnalysisResponse } from './types';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export async function analyzeSpec(
  filename: string,
  rawText: string,
): Promise<AnalysisResponse> {
  const response = await fetch(`${API_BASE}/api/specs`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ filename, raw_text: rawText }),
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(
      `Analysis failed (${response.status}): ${detail || response.statusText}`,
    );
  }

  return response.json() as Promise<AnalysisResponse>;
}
