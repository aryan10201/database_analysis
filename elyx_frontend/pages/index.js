import { useEffect, useState } from "react";
import Navbar from "@/components/Navbar";
import { generateJourney, healthCheck } from "@/lib/api";
import Link from "next/link";

export default function Home() {
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState("");
  const [systemStatus, setSystemStatus] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    // Check system health on load
    checkSystemHealth();
  }, []);

  const checkSystemHealth = async () => {
    try {
      const response = await healthCheck();
      setSystemStatus(response.data);
      setError("");
    } catch (err) {
      console.error("Failed to check system health:", err);
      setError(`System health check failed: ${err.message || 'Unknown error'}`);
    }
  };

  const runJourneyGeneration = async () => {
    try {
      setBusy(true);
      setMsg("Generating 8-month journey...");
      setError("");
      console.log("Starting journey generation...");
      
      const res = await generateJourney();
      console.log("Journey generation completed:", res.data);
      
      setMsg(`Journey generated successfully! ${res.data.storage_summary.conversations_stored} conversations, ${res.data.storage_summary.decisions_stored} decisions, ${res.data.storage_summary.health_events_stored} health events stored.`);
      
      // Refresh system health after generation
      checkSystemHealth();
        
    } catch (e) {
      console.error("Journey generation failed:", e);
      const errorMessage = e.response?.data?.detail || e.message || 'Unknown error';
      setError(`Failed to generate journey: ${errorMessage}`);
      setMsg("");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div>
      <Navbar />
      <main className="max-w-5xl mx-auto p-6 space-y-6">
        <h1 className="text-2xl font-bold">Elyx Member Journey</h1>
        
        <div className="card space-y-3">
          <p className="opacity-80">Generate a complete 8-month health optimization journey using local AI.</p>
          <button className="btn" onClick={runJourneyGeneration} disabled={busy}>
            {busy ? "Generating..." : "Generate Journey"}
          </button>
          {msg && <p className="text-sm text-green-600">{msg}</p>}
          {error && (
            <div className="text-sm text-red-600 bg-red-50 p-3 rounded border border-red-200">
              <p className="font-medium">Error:</p>
              <p>{error}</p>
              <p className="mt-2 text-xs">
                Make sure your backend is running at http://localhost:8080 and Groq API is available. Check the browser console for more details.
              </p>
            </div>
          )}
        </div>

        <div className="grid md:grid-cols-3 gap-4">
          <Link href="/journey" className="card hover:shadow-md transition">
            <h2 className="font-semibold">Journey Visualization →</h2>
            <p className="text-sm opacity-70">Timeline & team metrics</p>
          </Link>
          <Link href="/chat" className="card hover:shadow-md transition">
            <h2 className="font-semibold">Chat View →</h2>
            <p className="text-sm opacity-70">WhatsApp-style messages</p>
          </Link>
          <Link href="/timeline" className="card hover:shadow-md transition">
            <h2 className="font-semibold">Timeline →</h2>
            <p className="text-sm opacity-70">Weekly adherence & events</p>
          </Link>
        </div>

        {systemStatus && (
          <div className="card space-y-4">
            <h3 className="font-semibold text-lg">System Status</h3>
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <p><span className="font-medium">Groq Status:</span> 
                  <span className={`ml-2 px-2 py-1 rounded text-xs ${systemStatus.groq ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    {systemStatus.groq ? 'Available' : 'Not Available'}
                  </span>
                </p>
                <p><span className="font-medium">Available Models:</span> {systemStatus.models_available?.join(", ") || "None"}</p>
              </div>
              <div>
                <p><span className="font-medium">AI Service:</span> Groq API</p>
                <p><span className="font-medium">Cost:</span> Free tier (rate limited)</p>
                <p><span className="font-medium">Database:</span> SQLite</p>
              </div>
            </div>
          </div>
        )}

        <div className="card space-y-4">
          <h3 className="font-semibold text-lg">About the System</h3>
          <div className="space-y-2 text-sm">
            <p>• <strong>AI Generation:</strong> Uses Groq API with Llama3 model for conversation generation</p>
            <p>• <strong>Complete Journey:</strong> Creates 8 months of realistic health coaching conversations</p>
            <p>• <strong>Decision Tracking:</strong> Links every health decision back to specific conversations</p>
            <p>• <strong>Team Metrics:</strong> Tracks hours spent by doctors, coaches, and other team members</p>
            <p>• <strong>Fast AI:</strong> Groq's ultra-fast inference for quick generation</p>
          </div>
        </div>

        {error && !systemStatus && (
          <div className="text-sm text-yellow-600 bg-yellow-50 p-3 rounded border border-yellow-200">
            <p className="font-medium">System Status:</p>
            <p>Unable to check system health. The backend may not be running or Groq API may not be available.</p>
            <p className="mt-2 text-xs">
              To resolve: Start the backend with <code>uvicorn app.main:app --reload --port 8080</code> and ensure your Groq API key is configured
            </p>
          </div>
        )}
      </main>
    </div>
  );
}
