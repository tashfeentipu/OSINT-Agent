import ThreatDashboard from "@/components/ThreatDashboard";
import { fetchThreats } from "@/lib/api";
import { transformThreatResponse } from "@/lib/transform";

export default async function HomePage() {
  const response = await fetchThreats();
  const dashboardData = transformThreatResponse(response);

  return (
    <main>
      <ThreatDashboard data={dashboardData} />
    </main>
  );
}
