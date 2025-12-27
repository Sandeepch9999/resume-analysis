import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import api from '../services/api'

const Reports = () => {
  const [results, setResults] = useState([])
  const [selectedResult, setSelectedResult] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchResults()
  }, [])

  const fetchResults = async () => {
    try {
      const response = await api.get('/api/analysis/results')
      setResults(response.data)
    } catch (error) {
      console.error('Failed to fetch results:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleViewDetails = async (resultId) => {
    try {
      const response = await api.get(`/api/analysis/results/${resultId}`)
      setSelectedResult(response.data)
    } catch (error) {
      console.error('Failed to fetch result details:', error)
    }
  }

  const getMatchColor = (status) => {
    switch (status) {
      case 'Good Match':
        return 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300 border-green-300 dark:border-green-700'
      case 'Partial Match':
        return 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-300 border-yellow-300 dark:border-yellow-700'
      case 'Poor Match':
        return 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-300 border-red-300 dark:border-red-700'
      default:
        return 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-300 border-gray-300 dark:border-gray-600'
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen p-6">
      <div className="container mx-auto max-w-6xl">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">Analysis Reports</h1>
          <Link to="/resume-analyzer" className="btn-primary">
            New Analysis
          </Link>
        </div>

        {results.length === 0 ? (
          <div className="glass-card text-center py-12">
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              No analysis reports found. Start analyzing resumes to see reports here.
            </p>
            <Link to="/resume-analyzer" className="btn-primary inline-block">
              Analyze Resume
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Results List */}
            <div className="lg:col-span-1">
              <div className="glass-card">
                <h2 className="text-xl font-semibold mb-4">All Reports</h2>
                <div className="space-y-2 max-h-[600px] overflow-y-auto">
                  {results.map((result) => (
                    <button
                      key={result.id}
                      onClick={() => handleViewDetails(result.id)}
                      className={`w-full text-left p-4 rounded-lg transition-colors border-2 ${
                        selectedResult?.id === result.id
                          ? 'bg-primary-100 dark:bg-primary-900/30 border-primary-500'
                          : 'bg-gray-50 dark:bg-gray-700/50 hover:bg-gray-100 dark:hover:bg-gray-700 border-transparent'
                      }`}
                    >
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-semibold">Report #{result.id}</span>
                        <span className={`px-2 py-1 rounded text-xs font-medium border ${getMatchColor(result.match_status)}`}>
                          {result.match_status}
                        </span>
                      </div>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        Score: <span className="font-semibold">{result.similarity_score.toFixed(1)}%</span>
                      </p>
                      <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">
                        {new Date(result.created_at).toLocaleString()}
                      </p>
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Report Details */}
            <div className="lg:col-span-2">
              {selectedResult ? (
                <div className="space-y-6">
                  {/* Header */}
                  <div className="glass-card">
                    <div className="flex items-center justify-between mb-4">
                      <h2 className="text-2xl font-bold">Report #{selectedResult.id}</h2>
                      <span className={`px-3 py-1 rounded-lg font-semibold border ${getMatchColor(selectedResult.match_status)}`}>
                        {selectedResult.match_status}
                      </span>
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <p className="text-sm text-gray-600 dark:text-gray-400">Match Score</p>
                        <p className="text-3xl font-bold text-primary-600 dark:text-primary-400">
                          {selectedResult.similarity_score.toFixed(1)}%
                        </p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600 dark:text-gray-400">Analysis Date</p>
                        <p className="text-lg font-semibold">
                          {new Date(selectedResult.created_at).toLocaleString()}
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Skills Breakdown */}
                  {selectedResult.skills && selectedResult.skills.length > 0 && (
                    <div className="glass-card">
                      <h3 className="text-xl font-semibold mb-4">Skills Analysis</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                          <h4 className="font-medium text-green-600 dark:text-green-400 mb-3">
                            Present Skills ({selectedResult.skills.filter(s => s.is_present).length})
                          </h4>
                          <div className="flex flex-wrap gap-2">
                            {selectedResult.skills
                              .filter(s => s.is_present)
                              .map((skill) => (
                                <span
                                  key={skill.id}
                                  className="px-3 py-1 bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300 rounded-full text-sm"
                                >
                                  {skill.skill_name}
                                </span>
                              ))}
                          </div>
                        </div>
                        <div>
                          <h4 className="font-medium text-red-600 dark:text-red-400 mb-3">
                            Missing Skills ({selectedResult.skills.filter(s => s.is_required && !s.is_present).length})
                          </h4>
                          <div className="flex flex-wrap gap-2">
                            {selectedResult.skills
                              .filter(s => s.is_required && !s.is_present)
                              .map((skill) => (
                                <span
                                  key={skill.id}
                                  className="px-3 py-1 bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-300 rounded-full text-sm"
                                >
                                  {skill.skill_name}
                                </span>
                              ))}
                          </div>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Correction Suggestions */}
                  {selectedResult.correction_suggestions && (
                    <div className="glass-card">
                      <h3 className="text-xl font-semibold mb-4">Correction Suggestions</h3>
                      <div className="p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg">
                        <pre className="whitespace-pre-wrap text-sm text-gray-700 dark:text-gray-300">
                          {selectedResult.correction_suggestions}
                        </pre>
                      </div>
                    </div>
                  )}

                  {/* Quick Links */}
                  <div className="glass-card">
                    <h3 className="text-xl font-semibold mb-4">Next Steps</h3>
                    <div className="flex space-x-4">
                      <Link
                        to="/job-preparation"
                        className="btn-primary"
                      >
                        View Job Preparation
                      </Link>
                      <Link
                        to="/resume-analyzer"
                        className="btn-secondary"
                      >
                        New Analysis
                      </Link>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="glass-card text-center py-12">
                  <p className="text-gray-600 dark:text-gray-400">
                    Select a report from the list to view details
                  </p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Reports

