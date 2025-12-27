import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../services/api'
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalResumes: 0,
    totalJDs: 0,
    totalAnalyses: 0,
    avgMatchScore: 0,
  })
  const [recentResults, setRecentResults] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const [resumesRes, jdsRes, resultsRes] = await Promise.all([
        api.get('/api/resumes/'),
        api.get('/api/job-descriptions/'),
        api.get('/api/analysis/results'),
      ])

      const resumes = resumesRes.data
      const jds = jdsRes.data
      const results = resultsRes.data

      setStats({
        totalResumes: resumes.length,
        totalJDs: jds.length,
        totalAnalyses: results.length,
        avgMatchScore: results.length > 0
          ? results.reduce((sum, r) => sum + r.similarity_score, 0) / results.length
          : 0,
      })

      setRecentResults(results.slice(0, 5))
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const getMatchColor = (status) => {
    switch (status) {
      case 'Good Match':
        return 'text-green-600 dark:text-green-400'
      case 'Partial Match':
        return 'text-yellow-600 dark:text-yellow-400'
      case 'Poor Match':
        return 'text-red-600 dark:text-red-400'
      default:
        return 'text-gray-600 dark:text-gray-400'
    }
  }

  const chartData = [
    { name: 'Good Match', value: recentResults.filter(r => r.match_status === 'Good Match').length },
    { name: 'Partial Match', value: recentResults.filter(r => r.match_status === 'Partial Match').length },
    { name: 'Poor Match', value: recentResults.filter(r => r.match_status === 'Poor Match').length },
  ]

  const COLORS = ['#10b981', '#f59e0b', '#ef4444']

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen p-6">
      <div className="container mx-auto">
        <h1 className="text-3xl font-bold mb-8">Dashboard</h1>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="glass-card">
            <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">Total Resumes</h3>
            <p className="text-3xl font-bold text-primary-600 dark:text-primary-400">{stats.totalResumes}</p>
          </div>
          <div className="glass-card">
            <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">Job Descriptions</h3>
            <p className="text-3xl font-bold text-primary-600 dark:text-primary-400">{stats.totalJDs}</p>
          </div>
          <div className="glass-card">
            <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">Total Analyses</h3>
            <p className="text-3xl font-bold text-primary-600 dark:text-primary-400">{stats.totalAnalyses}</p>
          </div>
          <div className="glass-card">
            <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">Avg Match Score</h3>
            <p className="text-3xl font-bold text-primary-600 dark:text-primary-400">
              {stats.avgMatchScore.toFixed(1)}%
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Chart */}
          <div className="glass-card">
            <h2 className="text-xl font-semibold mb-4">Match Status Distribution</h2>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={chartData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>

          {/* Recent Results */}
          <div className="glass-card">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold">Recent Analyses</h2>
              <Link to="/reports" className="text-primary-600 dark:text-primary-400 hover:underline">
              View All
            </Link>
            </div>
            <div className="space-y-3">
              {recentResults.length === 0 ? (
                <p className="text-gray-500 dark:text-gray-400">No analyses yet. Start analyzing!</p>
              ) : (
                recentResults.map((result) => (
                  <div key={result.id} className="p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                    <div className="flex justify-between items-center">
                      <div>
                        <p className="font-medium">Analysis #{result.id}</p>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          Score: {result.similarity_score.toFixed(1)}%
                        </p>
                      </div>
                      <span className={`font-semibold ${getMatchColor(result.match_status)}`}>
                        {result.match_status}
                      </span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="mt-8 glass-card">
          <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Link
              to="/resume-analyzer"
              className="p-4 bg-primary-50 dark:bg-primary-900/30 rounded-lg hover:bg-primary-100 dark:hover:bg-primary-900/50 transition-colors text-center"
            >
              <h3 className="font-semibold text-primary-700 dark:text-primary-300">Analyze Resume</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">Upload and analyze your resume</p>
            </Link>
            <Link
              to="/job-preparation"
              className="p-4 bg-primary-50 dark:bg-primary-900/30 rounded-lg hover:bg-primary-100 dark:hover:bg-primary-900/50 transition-colors text-center"
            >
              <h3 className="font-semibold text-primary-700 dark:text-primary-300">Job Preparation</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">Get personalized preparation roadmap</p>
            </Link>
            <Link
              to="/reports"
              className="p-4 bg-primary-50 dark:bg-primary-900/30 rounded-lg hover:bg-primary-100 dark:hover:bg-primary-900/50 transition-colors text-center"
            >
              <h3 className="font-semibold text-primary-700 dark:text-primary-300">View Reports</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">See all your analysis reports</p>
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard

