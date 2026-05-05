import { ThreatItem, ThreatResponse } from "@/lib/api";

export type ThreatViewModel = {
  source: string;
  riskLevel: "Low" | "Medium" | "High";
  summary: string;
  action: string;
  threatType: string;
  insights: string[];
  entities: string[];
  confidenceScore: number;
  analysisConfidence: number;
  transparencyNote: string;
  deepDive: string;
};

export type ThreatDashboardData = {
  generatedAt: string;
  totalItems: number;
  headerSummary: string;
  keyInsights: string[];
  items: ThreatViewModel[];
};

function toPercent(value: number): string {
  return `${Math.round(value * 100)}%`;
}

function toInsightItems(item: ThreatItem): string[] {
  const indicators = item.analysis.risk_indicators.slice(0, 3);
  const entities = item.analysis.entities.slice(0, 2);

  const insights: string[] = [];
  insights.push(`Type: ${item.analysis.threat_type}`);
  insights.push(`Risk: ${item.risk.risk_level} (${toPercent(item.risk.confidence_score)})`);

  if (indicators.length > 0) {
    insights.push(`Indicators: ${indicators.join(", ")}`);
  }
  if (entities.length > 0) {
    insights.push(`Entities: ${entities.join(", ")}`);
  }

  return insights;
}

function buildDeepDive(item: ThreatItem): string {
  const raw = item.text?.trim() || "No deep-dive content available.";
  return raw.length > 500 ? `${raw.slice(0, 500)}...` : raw;
}

export function transformThreatResponse(data: ThreatResponse): ThreatDashboardData {
  const items: ThreatViewModel[] = data.results.map((item) => ({
    source: item.source,
    riskLevel: item.risk.risk_level,
    summary: item.report.summary,
    action: item.report.recommended_action,
    threatType: item.analysis.threat_type,
    insights: toInsightItems(item),
    entities: item.analysis.entities,
    confidenceScore: item.risk.confidence_score,
    analysisConfidence: item.analysis.confidence_score,
    transparencyNote: item.analysis.transparency_note,
    deepDive: buildDeepDive(item),
  }));

  const highCount = items.filter((item) => item.riskLevel === "High").length;
  const mediumCount = items.filter((item) => item.riskLevel === "Medium").length;
  const headerSummary = `${highCount} high-risk and ${mediumCount} medium-risk intelligence items detected across ${data.total_items} sources.`;

  const keyInsights: string[] = [
    `Most frequent threat category: ${items[0]?.threatType ?? "unknown"}`,
    `Average risk confidence: ${toPercent(items.reduce((sum, item) => sum + item.confidenceScore, 0) / Math.max(items.length, 1))}`,
    `Sanitization enabled for sensitive fields before analysis.`,
  ];

  return {
    generatedAt: data.generated_at,
    totalItems: data.total_items,
    headerSummary,
    keyInsights,
    items,
  };
}
