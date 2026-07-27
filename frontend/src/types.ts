export interface Finding {
  line_number: number;
  type: string;
  severity: string;
  message: string;
  suggested_rewrite: string;
  check_id: string;
  category: string;
}

export interface Requirement {
  line_number: number;
  raw_text: string;
  statement: string;
  section: string | null;
  uppercase_keywords: string[];
  lowercase_keywords: string[];
}

export interface Rewrite {
  line_number: number;
  rewritten_text: string;
  applied_at: string;
}

export interface AnalysisResponse {
  spec_id: number;
  filename: string;
  raw_text: string;
  effective_markdown: string;
  created_at: string;
  requirements: Requirement[];
  findings: Finding[];
  rewrites: Rewrite[];
  score: number;
  tier: string;
  verdict: string;
  exit_code: number;
  requirement_count: number;
  defects: number;
  clarifications: number;
  infos: number;
  report_markdown: string;
}
