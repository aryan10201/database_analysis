import { useEffect, useState } from "react";
import Navbar from "@/components/Navbar";
import MessageBubble from "@/components/MessageBubble";
import { fetchConversations } from "@/lib/api";

export default function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [limit, setLimit] = useState(100);
  const [filter, setFilter] = useState("all");
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadMessages();
  }, [limit]);

  const loadMessages = async () => {
    try {
      setLoading(true);
      setError("");
      const res = await fetchConversations(1); // Use member ID 1 instead of limit
      setMessages(res.data.conversations || []);
    } catch (err) {
      console.error("Failed to load messages:", err);
      setError(`Failed to load messages: ${err.message || 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };

  const filteredMessages = messages.filter(msg => {
    if (filter === "all") return true;
    if (filter === "member" && msg.sender === "Rohan") return true;
    if (filter === "team" && msg.sender !== "Rohan") return true;
    if (filter === "weekly-reports" && msg.tags?.includes("weekly-report")) return true;
    if (filter === "questions" && msg.tags?.includes("member-question")) return true;
    if (filter === "replies" && msg.tags?.includes("team-reply")) return true;
    
    if (searchTerm && !msg.text.toLowerCase().includes(searchTerm.toLowerCase())) return false;
    return true;
  });

  const getFilterCount = (filterType) => {
    if (filterType === "all") return messages.length;
    if (filterType === "member") return messages.filter(m => m.sender === "Rohan").length;
    if (filterType === "team") return messages.filter(m => m.sender !== "Rohan").length;
    if (filterType === "weekly-reports") return messages.filter(m => m.tags?.includes("weekly-report")).length;
    if (filterType === "questions") return messages.filter(m => m.tags?.includes("member-question")).length;
    if (filterType === "replies") return messages.filter(m => m.tags?.includes("team-reply")).length;
    return 0;
  };

  if (loading) {
    return (
      <div className="h-screen flex flex-col">
        <Navbar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading messages...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen flex flex-col">
      <Navbar />
      <div className="flex-1 overflow-y-auto max-w-4xl mx-auto w-full p-4">
        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-800 font-medium">Error loading messages:</p>
            <p className="text-red-600 text-sm">{error}</p>
            <button 
              onClick={loadMessages}
              className="mt-2 px-3 py-1 bg-red-100 text-red-800 rounded text-sm hover:bg-red-200"
            >
              Try Again
            </button>
          </div>
        )}

        <div className="sticky top-0 bg-white p-4 rounded-lg shadow-sm mb-4 z-10">
          <div className="flex flex-wrap items-center gap-4 mb-3">
            <label className="flex items-center gap-2">
              <span className="text-sm font-medium">Load</span>
              <select 
                className="border rounded px-2 py-1 text-sm" 
                value={limit} 
                onChange={e=>setLimit(parseInt(e.target.value))}
              >
                {[50, 100, 200, 500, 1000].map(v => <option key={v} value={v}>{v}</option>)}
              </select>
              <span className="text-sm opacity-70">messages</span>
            </label>
            
            <div className="flex items-center gap-2">
              <span className="text-sm font-medium">Filter:</span>
              <select 
                className="border rounded px-2 py-1 text-sm" 
                value={filter} 
                onChange={e=>setFilter(e.target.value)}
              >
                <option value="all">All ({getFilterCount("all")})</option>
                <option value="member">Member ({getFilterCount("member")})</option>
                <option value="team">Team ({getFilterCount("team")})</option>
                <option value="weekly-reports">Weekly Reports ({getFilterCount("weekly-reports")})</option>
                <option value="questions">Questions ({getFilterCount("questions")})</option>
                <option value="replies">Replies ({getFilterCount("replies")})</option>
              </select>
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium">Search:</span>
            <input
              type="text"
              placeholder="Search in messages..."
              className="border rounded px-3 py-1 text-sm flex-1"
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
            />
          </div>
        </div>

        <div className="space-y-4">
          {filteredMessages.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              {messages.length === 0 ? (
                <div>
                  <p className="text-lg font-medium mb-2">No messages available</p>
                  <p className="text-sm mb-4">You need to run the simulation first to generate conversation data.</p>
                  <a href="/" className="text-blue-600 hover:underline">Go to Home Page</a>
                </div>
              ) : (
                <div>
                  <p>No messages found matching your criteria.</p>
                  <p className="text-sm mt-1">Try adjusting the filter or search terms.</p>
                </div>
              )}
            </div>
          ) : (
            filteredMessages.map((m) => (
              <MessageBubble
                key={m.id}
                sender={m.sender}
                role={m.role}
                text={m.text}
                time={`${new Date(m.date).toLocaleDateString()} ${m.time}`}
                mine={m.sender === "Rohan"}
                tags={m.tags}
                relatesTo={m.relates_to}
              />
            ))
          )}
        </div>

        <div className="mt-6 text-center text-sm text-gray-500">
          Showing {filteredMessages.length} of {messages.length} messages
        </div>
      </div>
    </div>
  );
}
