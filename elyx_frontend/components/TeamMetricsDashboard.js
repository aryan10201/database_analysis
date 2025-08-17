import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { fetchTeamMetrics } from '../lib/api';

const TeamMetricsDashboard = ({ memberId }) => {
  const [metricsData, setMetricsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadTeamMetrics();
  }, [memberId]);

  const loadTeamMetrics = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetchTeamMetrics(memberId);
      setMetricsData(response.data.team_metrics || []);
    } catch (err) {
      console.error('Failed to load team metrics:', err);
      setError(err.message || 'Failed to load team metrics');
    } finally {
      setLoading(false);
    }
  };

  const getMonthName = (month) => {
    const months = [
      'January', 'February', 'March', 'April', 
      'May', 'June', 'July', 'August'
    ];
    return months[month - 1] || `Month ${month}`;
  };

  const getTotalHours = (metrics) => {
    return metrics.reduce((total, m) => {
      return total + m.doctor_hours + m.coach_hours + m.nutritionist_hours + m.physio_hours + m.concierge_hours;
    }, 0);
  };

  const getRoleBreakdown = (metrics) => {
    const totals = {
      doctor: 0,
      coach: 0,
      nutritionist: 0,
      physio: 0,
      concierge: 0
    };

    metrics.forEach(m => {
      totals.doctor += m.doctor_hours;
      totals.coach += m.coach_hours;
      totals.nutritionist += m.nutritionist_hours;
      totals.physio += m.physio_hours;
      totals.concierge += m.concierge_hours;
    });

    return Object.entries(totals).map(([role, hours]) => ({
      name: role.charAt(0).toUpperCase() + role.slice(1),
      value: hours,
      color: getRoleColor(role)
    }));
  };

  const getRoleColor = (role) => {
    const colors = {
      doctor: '#3B82F6',
      coach: '#10B981',
      nutritionist: '#F59E0B',
      physio: '#8B5CF6',
      concierge: '#EF4444'
    };
    return colors[role] || '#6B7280';
  };

  const getMonthlyData = () => {
    return metricsData?.map(m => ({
      month: getMonthName(m.month),
      monthNum: m.month,
      doctor: m.doctor_hours,
      coach: m.coach_hours,
      nutritionist: m.nutritionist_hours,
      physio: m.physio_hours,
      concierge: m.concierge_hours,
      total: m.doctor_hours + m.coach_hours + m.nutritionist_hours + m.physio_hours + m.concierge_hours
    }));
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
          onClick={loadTeamMetrics}
          className="mt-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Retry
        </button>
      </div>
    );
  }

  if (!metricsData || metricsData.length === 0) {
    return <div className="text-center text-gray-600 p-4">No team metrics available</div>;
  }

  const monthlyData = getMonthlyData();
  const roleBreakdown = getRoleBreakdown(metricsData);
  const totalHours = getTotalHours(metricsData);

  return (
    <div className="max-w-7xl mx-auto p-6">
      <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">
        Team Performance Dashboard
      </h2>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-blue-500">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Total Team Hours</h3>
          <p className="text-3xl font-bold text-blue-600">{totalHours.toFixed(1)}h</p>
          <p className="text-sm text-gray-600">Across 8 months</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-green-500">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Total Interventions</h3>
          <p className="text-3xl font-bold text-green-600">
            {metricsData.reduce((sum, m) => sum + m.total_interventions, 0)}
          </p>
          <p className="text-sm text-gray-600">Health interventions</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-purple-500">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Avg Monthly Hours</h3>
          <p className="text-3xl font-bold text-purple-600">{(totalHours / 8).toFixed(1)}h</p>
          <p className="text-sm text-gray-600">Per month</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-orange-500">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Active Months</h3>
          <p className="text-3xl font-bold text-orange-600">{metricsData.length}</p>
          <p className="text-sm text-gray-600">With activity</p>
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* Monthly Hours Chart */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">Monthly Team Hours</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={monthlyData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="doctor" fill="#3B82F6" name="Doctor" />
              <Bar dataKey="coach" fill="#10B981" name="Coach" />
              <Bar dataKey="nutritionist" fill="#F59E0B" name="Nutritionist" />
              <Bar dataKey="physio" fill="#8B5CF6" name="Physio" />
              <Bar dataKey="concierge" fill="#EF4444" name="Concierge" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Role Distribution Chart */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">Total Hours by Role</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={roleBreakdown}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {roleBreakdown.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Detailed Metrics Table */}
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-xl font-semibold text-gray-900">Detailed Monthly Breakdown</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Month
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Doctor
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Coach
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Nutritionist
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Physio
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Concierge
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Total
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Interventions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {monthlyData.map((month, index) => (
                <tr key={index} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {month.month}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {month.doctor.toFixed(1)}h
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {month.coach.toFixed(1)}h
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {month.nutritionist.toFixed(1)}h
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {month.physio.toFixed(1)}h
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {month.concierge.toFixed(1)}h
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-blue-600">
                    {month.total.toFixed(1)}h
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {metricsData.find(m => m.month === month.monthNum)?.total_interventions || 0}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Insights */}
      <div className="mt-8 bg-blue-50 p-6 rounded-lg">
        <h3 className="text-lg font-semibold text-blue-900 mb-3">Key Insights</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-blue-800">
          <div>
            <p><strong>Peak Activity:</strong> Month {monthlyData.reduce((max, m) => m.total > max.total ? m : max).monthNum} had the highest team engagement</p>
            <p><strong>Most Active Role:</strong> {roleBreakdown.reduce((max, r) => r.value > max.value ? r : max).name} with {roleBreakdown.reduce((max, r) => r.value > max.value ? r : max).value.toFixed(1)} total hours</p>
          </div>
          <div>
            <p><strong>Average Monthly Hours:</strong> {(totalHours / 8).toFixed(1)} hours per month</p>
            <p><strong>Total Interventions:</strong> {metricsData.reduce((sum, m) => sum + m.total_interventions, 0)} across the journey</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TeamMetricsDashboard;
