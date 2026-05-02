export type ThreatItem = {
  source: string;
  text: string;
  analysis: {
    threat_type: string;
    entities: string[];
    risk_indicators: string[];
    confidence_score: number;
    transparency_note: string;
  };
  risk: {
    risk_level: "Low" | "Medium" | "High";
    confidence_score: number;
  };
  report: {
    summary: string;
    recommended_action: string;
  };
};

export type ThreatResponse = {
  generated_at: string;
  total_items: number;
  results: ThreatItem[];
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";

export async function fetchThreats(): Promise<ThreatResponse> {
  const res = await fetch(`${API_BASE}/threats?limit=12`, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`Failed to fetch threats: ${res.status}`);
  }
  return res.json();
}
