"use client";

import { useMemo, useState } from "react";

import { ThreatDashboardData, ThreatViewModel } from "@/lib/transform";

type TabName = "Overview" | "Details" | "Sources";

type Props = {
  data: ThreatDashboardData;
};

function copyText(value: string): void {
  void navigator.clipboard.writeText(value);
}

function Card({ item, index }: { item: ThreatViewModel; index: number }) {
  const [open, setOpen] = useState(false);

  return (
    <article className="card reveal" style={{ animationDelay: `${index * 90}ms` }}>
      <div className="row">
        <h3 className="title">{item.source}</h3>
        <span className={`badge ${item.riskLevel.toLowerCase()}`}>{item.riskLevel}</span>
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

      <div className="actions">
        <button onClick={() => copyText(item.summary)} className="btnSecondary" type="button">Copy Summary</button>
        <button onClick={() => copyText(item.action)} className="btnSecondary" type="button">Copy Action</button>
        <button onClick={() => setOpen((prev) => !prev)} className="btnGhost" type="button">
          {open ? "Hide Deep Dive" : "Show Deep Dive"}
        </button>
      </div>

      {open ? (
        <div className="deepDive">
          <p>{item.deepDive}</p>
          <p className="meta">Transparency: {item.transparencyNote}</p>
          <p className="meta">Recommended Action: {item.action}</p>
        </div>
      ) : null}
    </article>
  );
}

export default function ThreatDashboard({ data }: Props) {
  const [tab, setTab] = useState<TabName>("Overview");

  const sources = useMemo(() => Array.from(new Set(data.items.map((item) => item.source))), [data.items]);

  return (
    <>
      <section className="card hero reveal">
        <h1>AI Threat Intelligence</h1>
        <p className="lead">{data.headerSummary}</p>
        <p className="meta">Generated: {new Date(data.generatedAt).toLocaleString()} | Total: {data.totalItems}</p>
        <div className="actions">
          <button className="btnPrimary" type="button" onClick={() => window.location.reload()}>Regenerate Response</button>
          <button className="btnSecondary" type="button" onClick={() => copyText(data.headerSummary)}>Copy Header</button>
        </div>
      </section>

      <section className="tabs reveal">
        {(["Overview", "Details", "Sources"] as TabName[]).map((tabName) => (
          <button
            key={tabName}
            type="button"
            className={tabName === tab ? "tab active" : "tab"}
            onClick={() => setTab(tabName)}
          >
            {tabName}
          </button>
        ))}
      </section>

      {tab === "Overview" ? (
        <section className="card reveal">
          <h2>Key Insights</h2>
          <ul className="insights">
            {data.keyInsights.map((insight) => (
              <li key={insight}>{insight}</li>
            ))}
          </ul>
        </section>
      ) : null}

      {tab === "Details" ? (
        <section className="grid">
          {data.items.map((item, index) => (
            <Card key={`${item.source}-${index}`} item={item} index={index} />
          ))}
        </section>
      ) : null}

      {tab === "Sources" ? (
        <section className="card reveal">
          <h2>Sources</h2>
          <ul className="insights">
            {sources.map((source) => (
              <li key={source}>{source}</li>
            ))}
          </ul>
        </section>
      ) : null}
    </>
  );
}
