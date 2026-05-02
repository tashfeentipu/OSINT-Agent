"use client";

import { useState } from "react";

import { ThreatDashboardData, ThreatViewModel } from "@/lib/transform";

type Props = {
  data: ThreatDashboardData;
};

function copyText(value: string): void {
  void navigator.clipboard.writeText(value);
}

function Card({ item, index }: { item: ThreatViewModel; index: number }) {
  const severityClass = item.riskLevel.toLowerCase();
  const [open, setOpen] = useState(false);

  return (
    <article className="card glassCard reveal" style={{ animationDelay: `${index * 90}ms` }}>
      <div className="row">
        <h3>{item.source}</h3>
        <span className={`badge ${severityClass}`}>{item.riskLevel}</span>
      </div>

      <p className="summary">{item.summary}</p>

      <div className="subsection">
        <h4>Key Insights</h4>
        <ul className="insights">
          {item.insights.map((insight) => (
            <li key={insight}>{insight}</li>
          ))}
        </ul>
      </div>

      <div className="subsection">
        <h4>Structured Data</h4>
        <div className="dataGrid">
          <div className="dataCell"><strong>Threat Type</strong><span>{item.threatType}</span></div>
          <div className="dataCell"><strong>Risk Confidence</strong><span>{item.confidenceScore.toFixed(2)}</span></div>
          <div className="dataCell"><strong>Analysis Confidence</strong><span>{item.analysisConfidence.toFixed(2)}</span></div>
          <div className="dataCell"><strong>Entities</strong><span>{item.entities.join(", ") || "None"}</span></div>
        </div>
      </div>

      <div className={open ? "deepDive open" : "deepDive"}>
        <button
          className="deepDiveToggle"
          type="button"
          onClick={() => setOpen((prev) => !prev)}
          aria-expanded={open}
        >
          {open ? "Hide Deep Dive" : "Show Deep Dive"}
        </button>
        <div className="deepDiveContent">
          <p>{item.deepDive}</p>
          <p className="meta">Transparency: {item.transparencyNote}</p>
          <p className="meta">Recommended Action: {item.action}</p>
        </div>
      </div>

      <div className="actions">
        <button onClick={() => copyText(item.summary)} className="btnSecondary" type="button">Copy Summary</button>
        <button onClick={() => copyText(item.action)} className="btnSecondary" type="button">Copy Action</button>
      </div>
    </article>
  );
}

export default function ThreatDashboard({ data }: Props) {
  return (
    <>
      <section className="card hero glassCard reveal">
        <h1>AI Threat Intelligence</h1>
        <p className="lead">{data.headerSummary}</p>
        <p className="meta">Generated: {new Date(data.generatedAt).toLocaleString()} | Total: {data.totalItems}</p>
        <div className="actions">
          <button className="btnPrimary" type="button" onClick={() => window.location.reload()}>Regenerate Response</button>
          <button className="btnSecondary" type="button" onClick={() => copyText(data.headerSummary)}>Copy Header</button>
        </div>
      </section>

      <section className="card glassCard reveal">
        <h2>Key Insights</h2>
        <ul className="insightCards">
          {data.keyInsights.map((insight) => (
            <li key={insight}>{insight}</li>
          ))}
        </ul>
      </section>

      <section className="grid">
        {data.items.map((item, index) => (
          <Card key={`${item.source}-${index}`} item={item} index={index} />
        ))}
      </section>

      <section className="card glassCard reveal">
        <h2>Sources</h2>
        <ul className="insights">
          {Array.from(new Set(data.items.map((item) => item.source))).map((source) => (
            <li key={source}>{source}</li>
          ))}
        </ul>
      </section>
    </>
  );
}
