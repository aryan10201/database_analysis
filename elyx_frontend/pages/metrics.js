import { useEffect, useState } from "react";
import Navbar from "@/components/Navbar";
import MetricCard from "@/components/MetricCard";
import { fetchTeamMetrics } from "@/lib/api";

export default function MetricsPage() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadTeamMetrics();
  }, []);

  const loadTeamMetrics = async () => {
    try {
      setLoading(true);
      setError("");
      const res = await fetchTeamMetrics(1); // Default to member ID 1
      setMetrics(res.data.team_metrics || []);
    } catch (err) {
      console.error("Failed to load team metrics:", err);
      setError(`Failed to load team metrics: ${err.message || 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="h-screen flex flex-col">
        <Navbar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading team metrics...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div>
        <Navbar />
        <main className="max-w-5xl mx-auto p-6">
          <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-800 font-medium">Error loading team metrics:</p>
            <p className="text-red-600 text-sm">{error}</p>
            <button 
              onClick={loadTeamMetrics}
              className="mt-2 px-3 py-1 bg-red-100 text-red-800 rounded text-sm hover:bg-red-200"
            >
              Try Again
            </button>
          </div>
        </main>
      </div>
    );
  }

  if (!metrics || metrics.length === 0) {
    return (
      <div>
        <Navbar />
        <main className="max-w-5xl mx-auto p-6">
          <div className="text-center text-gray-500">
            <p>No team metrics found</p>
            <p className="text-sm">Try generating a journey first from the home page.</p>
          </div>
        </main>
      </div>
    );
  }

  const formatLabel = (key) => {
    return key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
  };

  const getMetricIcon = (key) => {
    const icons = {
      doctor_hours: "👨‍⚕️",
      coach_hours: "🏃‍♂️",
      nutritionist_hours: "🥗",
      physio_hours: "💪",
      concierge_hours: "🎯",
      total_interventions: "🔬"
    };
    return icons[key] || "📊";
  };

  const getMetricDescription = (key) => {
    const descriptions = {
      doctor_hours: "Medical consultation and review time",
      coach_hours: "Performance coaching and training sessions",
      nutritionist_hours: "Diet planning and nutritional guidance",
      physio_hours: "Physical therapy and rehabilitation",
      concierge_hours: "Coordination and member support",
      total_interventions: "Total medical and lifestyle interventions"
    };
    return descriptions[key] || "";
  };

  // Aggregate metrics across all months
// Aggregate metrics across all months safely
const aggregatedMetrics = metrics.reduce((acc, monthData) => {
  if (monthData.metrics) {   // ✅ guard against null
    Object.entries(monthData.metrics).forEach(([key, value]) => {
      if (!acc[key]) acc[key] = 0;
      acc[key] += value;
    });
  }
  return acc;
}, {});

const entries = Object.entries(aggregatedMetrics);


  return (
    <div>
      <Navbar />
      <main className="max-w-5xl mx-auto p-6 space-y-6">
        <div>
          <h1 className="text-2xl font-bold mb-2">Team Metrics Dashboard</h1>
          <p className="text-gray-600">Team effort tracking and intervention monitoring for Rohan Patel's 8-month health journey</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {entries.map(([k, v]) => (
            <div key={k} className="card hover:shadow-md transition">
              <div className="flex items-center gap-3 mb-3">
                <span className="text-2xl">{getMetricIcon(k)}</span>
                <div>
                  <p className="text-sm text-gray-600">{formatLabel(k)}</p>
                  <p className="text-2xl font-bold">{k.includes('hours') ? `${v}h` : v}</p>
                </div>
              </div>
              <p className="text-xs text-gray-500">{getMetricDescription(k)}</p>
            </div>
          ))}
        </div>

        <div className="card bg-blue-50 border-blue-200">
          <h2 className="font-semibold text-lg mb-3 text-blue-800">📈 8-Month Journey Summary</h2>
          <div className="grid md:grid-cols-2 gap-4 text-sm">
            <div>
              <p><span className="font-medium">Total Team Hours:</span> {entries.reduce((sum, [k, v]) => k.includes('hours') ? sum + v : sum, 0).toFixed(1)}h</p>
              <p><span className="font-medium">Average Monthly Hours:</span> {(entries.reduce((sum, [k, v]) => k.includes('hours') ? sum + v : sum, 0) / 8).toFixed(1)}h/month</p>
            </div>
            <div>
              <p><span className="font-medium">Intervention Rate:</span> {aggregatedMetrics.total_interventions || 0} over 8 months</p>
              <p><span className="font-medium">Most Active Team:</span> {entries.filter(([k, v]) => k.includes('hours')).sort(([,a], [,b]) => b - a)[0]?.[0]?.replace('_hours', '').replace('_', ' ') || 'N/A'}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <h2 className="font-semibold text-lg mb-3">📅 Monthly Breakdown</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {metrics.map((monthData, index) => (
  <div key={index} className="p-3 bg-gray-50 rounded">
    <h3 className="font-medium text-sm mb-2">Month {monthData.month}</h3>
    <div className="space-y-1 text-xs">
      {monthData.metrics
        ? Object.entries(monthData.metrics).map(([key, value]) => (
            <div key={key} className="flex justify-between">
              <span>{formatLabel(key)}:</span>
              <span className="font-medium">{key.includes('hours') ? `${value}h` : value}</span>
            </div>
          ))
        : <p className="text-gray-400 italic">No metrics for this month</p>
      }
    </div>
  </div>
))}

          </div>
        </div>
      </main>
    </div>
  );
}
