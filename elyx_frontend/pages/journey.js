import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import Navbar from '../components/Navbar';
import JourneyTimeline from '../components/JourneyTimeline';
import TeamMetricsDashboard from '../components/TeamMetricsDashboard';
import { generateJourney } from '../lib/api';

const JourneyPage = () => {
  const [memberId, setMemberId] = useState(1); // Default to first member
  const [activeTab, setActiveTab] = useState('timeline');
  const [loading, setLoading] = useState(false);

  const generateJourneyHandler = async () => {
    try {
      setLoading(true);
      const response = await generateJourney();
      
      if (response.data) {
        alert('Journey generated successfully! Refresh the page to view the new data.');
        window.location.reload();
      } else {
        alert('Error: Failed to generate journey');
      }
    } catch (error) {
      console.error('Error generating journey:', error);
      alert(`Error generating journey: ${error.response?.data?.detail || error.message || 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>Rohan's Health Journey - Elyx Life</title>
        <meta name="description" content="Comprehensive visualization of Rohan's 8-month health optimization journey" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gray-50">
        <Navbar />
        
        <main className="pt-20">
          {/* Header Section */}
          <div className="bg-white shadow-sm border-b">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
              <div className="flex flex-col md:flex-row md:items-center md:justify-between">
                <div>
                  <h1 className="text-4xl font-bold text-gray-900">
                    Rohan's Health Journey
                  </h1>
                  <p className="mt-2 text-lg text-gray-600">
                    Comprehensive visualization of an 8-month health optimization journey with decision tracking
                  </p>
                </div>
                
                <div className="mt-4 md:mt-0">
                  <button
                    onClick={generateJourneyHandler}
                    disabled={loading}
                    className={`px-6 py-3 rounded-lg font-medium text-white transition-colors ${
                      loading
                        ? 'bg-gray-400 cursor-not-allowed'
                        : 'bg-blue-600 hover:bg-blue-700'
                    }`}
                  >
                    {loading ? 'Generating...' : 'Generate New Journey'}
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Tab Navigation */}
          <div className="bg-white border-b">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <nav className="flex space-x-8">
                <button
                  onClick={() => setActiveTab('timeline')}
                  className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                    activeTab === 'timeline'
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  Journey Timeline
                </button>
                <button
                  onClick={() => setActiveTab('metrics')}
                  className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                    activeTab === 'metrics'
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  Team Metrics
                </button>
              </nav>
            </div>
          </div>

          {/* Content */}
          <div className="py-8">
            {activeTab === 'timeline' ? (
              <JourneyTimeline memberId={memberId} />
            ) : (
              <TeamMetricsDashboard memberId={memberId} />
            )}
          </div>

          {/* Information Section */}
          <div className="bg-blue-50 border-t">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
              <div className="text-center">
                <h2 className="text-3xl font-bold text-gray-900 mb-6">
                  Journey Features
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                  <div className="text-center">
                    <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center text-white text-2xl mx-auto mb-4">
                      📊
                    </div>
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">
                      Decision Tracking
                    </h3>
                    <p className="text-gray-600">
                      Click on any decision to see the exact conversations that led to it, providing complete traceability.
                    </p>
                  </div>
                  
                  <div className="text-center">
                    <div className="w-16 h-16 bg-green-600 rounded-full flex items-center justify-center text-white text-2xl mx-auto mb-4">
                      🕒
                    </div>
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">
                      Timeline Visualization
                    </h3>
                    <p className="text-gray-600">
                      Month-by-month breakdown of health events, decisions, and progress metrics.
                    </p>
                  </div>
                  
                  <div className="text-center">
                    <div className="w-16 h-16 bg-purple-600 rounded-full flex items-center justify-center text-white text-2xl mx-auto mb-4">
                      👥
                    </div>
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">
                      Team Performance
                    </h3>
                    <p className="text-gray-600">
                      Track hours spent by doctors, coaches, and other team members across the journey.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </>
  );
};

export default JourneyPage;
