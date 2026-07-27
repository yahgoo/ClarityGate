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

export async function applyRewrite(
  specId: number,
  lineNumber: number,
  rewrittenText: string,
): Promise<AnalysisResponse> {
  const response = await fetch(`${API_BASE}/api/specs/${specId}/rewrites`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ line_number: lineNumber, rewritten_text: rewrittenText }),
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(
      `Rewrite failed (${response.status}): ${detail || response.statusText}`,
    );
  }

  return response.json() as Promise<AnalysisResponse>;
}

export async function removeRewrite(
  specId: number,
  lineNumber: number,
): Promise<AnalysisResponse> {
  const response = await fetch(
    `${API_BASE}/api/specs/${specId}/rewrites/${lineNumber}`,
    { method: 'DELETE' },
  );

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(
      `Remove rewrite failed (${response.status}): ${detail || response.statusText}`,
    );
  }

  return response.json() as Promise<AnalysisResponse>;
}

export async function resetRewrites(
  specId: number,
): Promise<AnalysisResponse> {
  const response = await fetch(`${API_BASE}/api/specs/${specId}/rewrites`, {
    method: 'DELETE',
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(
      `Reset rewrites failed (${response.status}): ${detail || response.statusText}`,
    );
  }

  return response.json() as Promise<AnalysisResponse>;
}
