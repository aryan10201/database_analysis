import { useEffect, useMemo, useState } from "react";
import Navbar from "@/components/Navbar";
import { fetchJourneyTimeline, fetchConversations } from "@/lib/api";

export default function TimelinePage() {
  const [journeyData, setJourneyData] = useState(null);
  const [selectedMonth, setSelectedMonth] = useState(null);
  const [monthConversations, setMonthConversations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadJourneyData();
  }, []);

  const loadJourneyData = async () => {
    try {
      setLoading(true);
      setError("");
      const res = await fetchJourneyTimeline(1); // Default to member ID 1
      setJourneyData(res.data.timeline);
    } catch (err) {
      console.error("Failed to load journey data:", err);
      setError(`Failed to load journey data: ${err.message || 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };

  const loadMonthConversations = async (month) => {
    try {
      setSelectedMonth(month);
      const res = await fetchConversations(1, month);
      setMonthConversations(res.data.conversations || []);
    } catch (err) {
      console.error("Failed to load month conversations:", err);
    }
  };

  const getAdherenceColor = (adherence) => {
    if (adherence >= 0.7) return "text-green-600";
    if (adherence >= 0.5) return "text-yellow-600";
    return "text-red-600";
  };

  const getAdherenceLabel = (adherence) => {
    if (adherence >= 0.7) return "Excellent";
    if (adherence >= 0.5) return "Good";
    return "Needs Improvement";
  };

  if (loading) {
    return (
      <div className="h-screen flex flex-col">
        <Navbar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading journey data...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div>
      <Navbar />
      <main className="max-w-6xl mx-auto p-6">
        <h1 className="text-2xl font-bold mb-4">Journey Timeline</h1>
        
        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-800 font-medium">Error loading journey data:</p>
            <p className="text-red-600 text-sm">{error}</p>
            <button 
              onClick={loadJourneyData}
              className="mt-2 px-3 py-1 bg-red-100 text-red-800 rounded text-sm hover:bg-red-200"
            >
              Try Again
            </button>
          </div>
        )}

        {journeyData && (
          <div className="card mb-6">
            <h2 className="font-semibold text-lg mb-3">Journey Overview</h2>
            <div className="grid md:grid-cols-3 gap-4 text-sm">
              <div>
                <p><span className="font-medium">Total Conversations:</span> {journeyData.conversations?.length || 0}</p>
                <p><span className="font-medium">Total Decisions:</span> {journeyData.decisions?.length || 0}</p>
              </div>
              <div>
                <p><span className="font-medium">Health Events:</span> {journeyData.health_events?.length || 0}</p>
                <p><span className="font-medium">Team Metrics:</span> {journeyData.team_metrics?.length || 0}</p>
              </div>
              <div>
                <p><span className="font-medium">Duration:</span> 8 months</p>
                <p><span className="font-medium">Member:</span> Rohan Patel</p>
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {[1, 2, 3, 4, 5, 6, 7, 8].map((month) => (
            <div key={month} className="card hover:shadow-md transition">
              <div className="flex items-center justify-between mb-3">
                <h2 className="font-semibold text-sm">
                  Month {month}
                </h2>
                <button 
                  className="btn text-xs px-3 py-1" 
                  onClick={() => loadMonthConversations(month)}
                >
                  Details
                </button>
              </div>
              <div className="space-y-2">
                <div className="text-xs opacity-70">
                  📅 Month {month} of 8
                </div>
                {journeyData?.conversations?.filter(c => c.month === month) && (
                  <div className="text-xs opacity-70">
                    💬 {journeyData.conversations.filter(c => c.month === month).length} conversations
                  </div>
                )}
                {journeyData?.decisions?.filter(d => d.month === month) && (
                  <div className="text-xs opacity-70">
                    🎯 {journeyData.decisions.filter(d => d.month === month).length} decisions
                  </div>
                )}
                {journeyData?.health_events?.filter(e => e.month === month) && (
                  <div className="text-xs opacity-70">
                    🏥 {journeyData.health_events.filter(e => e.month === month).length} health events
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        {selectedMonth && monthConversations.length > 0 && (
          <div className="mt-8">
            <h2 className="text-xl font-semibold mb-4">Month {selectedMonth} Conversations</h2>
            <div className="space-y-3">
              {monthConversations.map((conversation, index) => (
                <div key={index} className="card p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-medium text-sm">{conversation.sender}</span>
                    <span className="text-xs opacity-70">Week {conversation.week_number}</span>
                  </div>
                  <p className="text-sm">{conversation.text}</p>
                  {conversation.tags && conversation.tags.length > 0 && (
                    <div className="mt-2 flex flex-wrap gap-1">
                      {conversation.tags.map((tag, tagIndex) => (
                        <span key={tagIndex} className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">
                          {tag}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {selectedMonth && monthConversations.length === 0 && (
          <div className="mt-8 text-center text-gray-500">
            <p>No conversations found for Month {selectedMonth}</p>
            <p className="text-sm">Try generating a journey first from the home page.</p>
          </div>
        )}
      </main>
    </div>
  );
}
