import React, { useState, useEffect } from 'react';
import { format } from 'date-fns';
import { fetchJourneyTimeline, fetchDecisionContext } from '../lib/api';

const JourneyTimeline = ({ memberId }) => {
  const [journeyData, setJourneyData] = useState(null);
  const [selectedDecision, setSelectedDecision] = useState(null);
  const [decisionContext, setDecisionContext] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadJourneyData();
  }, [memberId]);

  const loadJourneyData = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetchJourneyTimeline(memberId);
      setJourneyData(response.data.timeline);
    } catch (err) {
      console.error('Failed to load journey data:', err);
      setError(err.message || 'Failed to load journey data');
    } finally {
      setLoading(false);
    }
  };

  const loadDecisionContext = async (decisionId) => {
    try {
      setSelectedDecision(decisionId);
      const response = await fetchDecisionContext(decisionId);
      setDecisionContext(response.data);
    } catch (err) {
      console.error('Failed to load decision context:', err);
      alert('Failed to load decision context');
    }
  };

  const getMonthName = (month) => {
    const months = [
      'January', 'February', 'March', 'April', 
      'May', 'June', 'July', 'August'
    ];
    return months[month - 1] || `Month ${month}`;
  };

  const getEventIcon = (eventType) => {
    switch (eventType) {
      case 'diagnostic_test':
        return '🔬';
      case 'plan_modification':
        return '📋';
      case 'exercise_update':
        return '💪';
      case 'travel':
        return '✈️';
      default:
        return '📅';
    }
  };

  const getDecisionIcon = (decisionType) => {
    switch (decisionType) {
      case 'diagnostic_test':
        return '🔍';
      case 'exercise_plan':
        return '🏃';
      case 'nutrition_plan':
        return '🥗';
      case 'medication':
        return '💊';
      default:
        return '✅';
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center text-red-600 p-4">
        <p>{error}</p>
        <button 
          onClick={loadJourneyData}
          className="mt-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Retry
        </button>
      </div>
    );
  }

  if (!journeyData) {
    return <div className="text-center text-gray-600 p-4">No timeline data available</div>;
  }

  return (
    <div className="max-w-7xl mx-auto p-6">
      <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">
        Rohan's 8-Month Health Journey
      </h2>

      {/* Month Navigation */}
      <div className="flex justify-center mb-8">
        <div className="flex space-x-2">
          {[1, 2, 3, 4, 5, 6, 7, 8].map((month) => (
            <button
              key={month}
              onClick={() => setSelectedDecision(null)} // Clear selected decision when month changes
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                selectedDecision === null // Check if no decision is selected
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              {getMonthName(month)}
            </button>
          ))}
        </div>
      </div>

      {/* Timeline */}
      <div className="relative">
        {/* Timeline Line */}
        <div className="absolute left-8 top-0 bottom-0 w-0.5 bg-gray-300"></div>

        {/* Timeline Items */}
        <div className="space-y-8">
          {[1, 2, 3, 4, 5, 6, 7, 8].map((month) => {
            const monthData = journeyData.metrics?.find(m => m.month === month);
            const monthEvents = journeyData.health_events?.filter(e => e.month === month) || [];
            const monthDecisions = journeyData.decisions?.filter(d => d.month === month) || [];
            const monthConversations = journeyData.conversations?.filter(c => c.month === month) || [];

            if (selectedDecision && selectedDecision !== null) { // Only show if a decision is selected
              return null;
            }

            return (
              <div key={month} className="relative">
                {/* Month Header */}
                <div className="flex items-center mb-6">
                  <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold text-lg z-10 relative">
                    {month}
                  </div>
                  <div className="ml-6">
                    <h3 className="text-2xl font-bold text-gray-900">
                      {getMonthName(month)}
                    </h3>
                    {monthData && (
                      <p className="text-gray-600">
                        Adherence: {(monthData.adherence_estimate * 100).toFixed(0)}% | 
                        Hours: {monthData.hours_committed.toFixed(1)}h
                      </p>
                    )}
                  </div>
                </div>

                {/* Month Content */}
                <div className="ml-24 space-y-6">
                  {/* Health Events */}
                  {monthEvents.map((event) => (
                    <div key={event.id} className="bg-white p-4 rounded-lg shadow-md border-l-4 border-green-500">
                      <div className="flex items-center mb-2">
                        <span className="text-2xl mr-3">{getEventIcon(event.event_type)}</span>
                        <h4 className="text-lg font-semibold text-gray-900">{event.title}</h4>
                      </div>
                      <p className="text-gray-600 text-sm mb-2">
                        {format(new Date(event.date), 'MMM dd, yyyy')}
                      </p>
                      <p className="text-gray-700">{event.details.description}</p>
                    </div>
                  ))}

                  {/* Decisions */}
                  {monthDecisions.map((decision) => (
                    <div key={decision.id} className="bg-white p-4 rounded-lg shadow-md border-l-4 border-blue-500">
                      <div className="flex items-center mb-2">
                        <span className="text-2xl mr-3">{getDecisionIcon(decision.decision_type)}</span>
                        <h4 className="text-lg font-semibold text-gray-900">{decision.title}</h4>
                      </div>
                      <p className="text-gray-600 text-sm mb-2">
                        {format(new Date(decision.date), 'MMM dd, yyyy')} | 
                        Confidence: {(decision.confidence_score * 100).toFixed(0)}%
                      </p>
                      <p className="text-gray-700 mb-3">{decision.reason}</p>
                      <button
                        onClick={() => loadDecisionContext(decision.id)}
                        className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                      >
                        View Decision Context →
                      </button>
                    </div>
                  ))}

                  {/* Conversation Summary */}
                  {monthConversations.length > 0 && (
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <h4 className="text-lg font-semibold text-gray-900 mb-2">
                        💬 Communication Summary
                      </h4>
                      <p className="text-gray-600 text-sm">
                        {monthConversations.length} messages exchanged | 
                        {monthConversations.filter(c => c.sender === 'Rohan Patel').length} from Rohan | 
                        {monthConversations.filter(c => c.sender !== 'Rohan Patel').length} from team
                      </p>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Decision Context Modal */}
      {decisionContext && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-xl font-bold text-gray-900">
                  Decision Context: {decisionContext.decision.title}
                </h3>
                <button
                  onClick={() => setDecisionContext(null)}
                  className="text-gray-400 hover:text-gray-600 text-2xl"
                >
                  ×
                </button>
              </div>

              <div className="space-y-4">
                <div className="bg-blue-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-blue-900 mb-2">Decision Details</h4>
                  <p className="text-blue-800">{decisionContext.decision.reason}</p>
                  <p className="text-blue-600 text-sm mt-2">
                    Confidence: {(decisionContext.decision.confidence_score * 100).toFixed(0)}%
                  </p>
                </div>

                {decisionContext.triggered_conversation && (
                  <div className="bg-green-50 p-4 rounded-lg">
                    <h4 className="font-semibold text-green-900 mb-2">Triggering Message</h4>
                    <div className="bg-white p-3 rounded border">
                      <p className="text-sm text-gray-600 mb-1">
                        {decisionContext.triggered_conversation.sender} • 
                        {format(new Date(decisionContext.triggered_conversation.date), 'MMM dd, yyyy HH:mm')}
                      </p>
                      <p className="text-green-800">{decisionContext.triggered_conversation.text}</p>
                    </div>
                  </div>
                )}

                {decisionContext.supporting_conversations.length > 0 && (
                  <div className="bg-yellow-50 p-4 rounded-lg">
                    <h4 className="font-semibold text-yellow-900 mb-2">Supporting Conversations</h4>
                    <div className="space-y-2 max-h-64 overflow-y-auto">
                      {decisionContext.supporting_conversations.map((conv) => (
                        <div key={conv.id} className="bg-white p-3 rounded border">
                          <p className="text-sm text-gray-600 mb-1">
                            {conv.sender} • {format(new Date(conv.date), 'MMM dd, yyyy HH:mm')}
                          </p>
                          <p className="text-yellow-800">{conv.text}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default JourneyTimeline;
