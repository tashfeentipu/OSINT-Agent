"use client";

import { useEffect, useMemo, useState } from "react";

import ThreatDashboard from "@/components/ThreatDashboard";
import { getThreatStreamUrl, ThreatResponse } from "@/lib/api";
import { ThreatDashboardData, transformThreatResponse } from "@/lib/transform";

type ProgressEvent = {
  stage?: string;
  message?: string;
  item_index?: number;
  total_items?: number;
  source?: string;
};

export default function HomePage() {
  const [progress, setProgress] = useState<ProgressEvent[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [dashboardData, setDashboardData] = useState<ThreatDashboardData | null>(null);

  const latestProgress = useMemo(() => progress[progress.length - 1], [progress]);

  useEffect(() => {
    const stream = new EventSource(getThreatStreamUrl(12));

    stream.addEventListener("progress", (event) => {
      const message = JSON.parse((event as MessageEvent).data) as ProgressEvent;
      setProgress((prev) => [...prev, message]);
    });

    stream.addEventListener("result", (event) => {
      const data = JSON.parse((event as MessageEvent).data) as ThreatResponse;
      setDashboardData(transformThreatResponse(data));
    });

    stream.addEventListener("error", (event) => {
      try {
        const payload = JSON.parse((event as MessageEvent).data) as { message?: string };
        setError(payload.message ?? "Threat stream failed.");
      } catch {
        setError("Threat stream failed.");
      }
      stream.close();
    });

    stream.addEventListener("done", () => {
      stream.close();
    });

    stream.onerror = () => {
      setError("Connection to threat stream was interrupted.");
      stream.close();
    };

    return () => stream.close();
  }, []);

  if (error) {
    return (
      <main>
        <section className="card glassCard">
          <h1>AI Threat Intelligence</h1>
          <p className="lead">Failed to load threat stream.</p>
          <p className="meta">{error}</p>
          <button className="btnPrimary" type="button" onClick={() => window.location.reload()}>
            Retry
          </button>
        </section>
      </main>
    );
  }

  if (!dashboardData) {
    return (
      <main>
        <section className="card hero glassCard reveal">
          <h1>AI Threat Intelligence</h1>
          <p className="lead">{latestProgress?.message ?? "Initializing analysis pipeline..."}</p>
          <p className="meta">
            Stage: {latestProgress?.stage ?? "starting"}
            {latestProgress?.item_index && latestProgress?.total_items
              ? ` | Item ${latestProgress.item_index}/${latestProgress.total_items}`
              : ""}
          </p>
        </section>

        <section className="card glassCard reveal">
          <h2>Live Processing Log</h2>
          <ul className="insights">
            {progress.slice(-8).map((event, index) => (
              <li key={`${event.stage ?? "stage"}-${index}`}>
                [{event.stage ?? "progress"}] {event.message ?? "Working..."}
              </li>
            ))}
          </ul>
        </section>
      </main>
    );
  }

  return (
    <main>
      <ThreatDashboard data={dashboardData} />
    </main>
  );
}
