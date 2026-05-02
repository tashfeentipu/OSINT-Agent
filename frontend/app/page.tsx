import ThreatCard from "@/components/ThreatCard";
import { fetchThreats } from "@/lib/api";

export default async function HomePage() {
  const data = await fetchThreats();

  return (
    <main>
      <section className="card" style={{ marginBottom: "1rem" }}>
        <h1 style={{ marginTop: 0 }}>AI Threat Intelligence</h1>
        <p className="meta">
          Generated: {new Date(data.generated_at).toLocaleString()} | Total Threats: {data.total_items}
        </p>
      </section>

      <section className="grid">
        {data.results.map((threat, index) => (
          <ThreatCard key={`${threat.source}-${index}`} threat={threat} />
        ))}
      </section>
    </main>
  );
}
