import { ThreatItem } from "@/lib/api";

type Props = {
  threat: ThreatItem;
};

function toPercent(value: number): string {
  return `${Math.round(value * 100)}%`;
}

export default function ThreatCard({ threat }: Props) {
  const severityClass = threat.risk.risk_level.toLowerCase();

  return (
    <article className="card">
      <div style={{ display: "flex", justifyContent: "space-between", gap: "0.75rem" }}>
        <strong>{threat.source}</strong>
        <span className={`badge ${severityClass}`}>{threat.risk.risk_level}</span>
      </div>
      <p>{threat.report.summary}</p>
      <p className="meta">Threat Type: {threat.analysis.threat_type}</p>
      <p className="meta">Risk Confidence: {toPercent(threat.risk.confidence_score)}</p>
      <p className="meta">Analysis Confidence: {toPercent(threat.analysis.confidence_score)}</p>
      <p className="meta">Recommended Action: {threat.report.recommended_action}</p>
    </article>
  );
}
