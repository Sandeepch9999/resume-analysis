import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'

const JobPreparation = () => {
  const [matchResults, setMatchResults] = useState([])
  const [selectedResult, setSelectedResult] = useState(null)
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    fetchMatchResults()
  }, [])

  const fetchMatchResults = async () => {
    try {
      const response = await api.get('/analysis/results')
      setMatchResults(response.data)
      if (response.data.length > 0 && !selectedResult) {
        setSelectedResult(response.data[0].id)
      }
    } catch (error) {
      console.error('Failed to fetch match results:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleViewResult = async (resultId) => {
    try {
      const response = await api.get(`/analysis/results/${resultId}`)
      setSelectedResult(resultId)
    } catch (error) {
      console.error('Failed to fetch result details:', error)
    }
  }

  const currentResult = matchResults.find(r => r.id === selectedResult)

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    )
  }

  if (matchResults.length === 0) {
    return (
      <div className="min-h-screen p-6">
        <div className="container mx-auto max-w-4xl">
          <h1 className="text-3xl font-bold mb-8">Job Preparation</h1>
          <div className="glass-card text-center py-12">
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              No analysis results found. Please analyze a resume first.
            </p>
            <button
              onClick={() => navigate('/resume-analyzer')}
              className="btn-primary"
            >
              Go to Resume Analyzer
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen p-6">
      <div className="container mx-auto max-w-6xl">
        <h1 className="text-3xl font-bold mb-8">Job Preparation</h1>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Results List */}
          <div className="lg:col-span-1">
            <div className="glass-card">
              <h2 className="text-xl font-semibold mb-4">Select Analysis</h2>
              <div className="space-y-2">
                {matchResults.map((result) => (
                  <button
                    key={result.id}
                    onClick={() => handleViewResult(result.id)}
                    className={`w-full text-left p-3 rounded-lg transition-colors ${
                      selectedResult === result.id
                        ? 'bg-primary-100 dark:bg-primary-900/30 border-2 border-primary-500'
                        : 'bg-gray-50 dark:bg-gray-700/50 hover:bg-gray-100 dark:hover:bg-gray-700'
                    }`}
                  >
                    <p className="font-medium">Analysis #{result.id}</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Score: {result.similarity_score.toFixed(1)}%
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">
                      {new Date(result.created_at).toLocaleDateString()}
                    </p>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Preparation Content */}
          <div className="lg:col-span-2">
            {currentResult ? (
              <div className="space-y-6">
                {/* Syllabus */}
                {currentResult.syllabus_items && currentResult.syllabus_items.length > 0 && (
                  <div className="glass-card">
                    <h2 className="text-2xl font-bold mb-4">Learning Syllabus</h2>
                    <div className="space-y-4">
                      {currentResult.syllabus_items.map((item, index) => (
                        <div
                          key={item.id}
                          className="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg"
                        >
                          <div className="flex items-start justify-between mb-2">
                            <h3 className="font-semibold text-lg">{item.topic}</h3>
                            <span className={`px-2 py-1 rounded text-xs font-medium ${
                              item.priority === 'High' ? 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-300' :
                              item.priority === 'Medium' ? 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-300' :
                              'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300'
                            }`}>
                              {item.priority} Priority
                            </span>
                          </div>
                          {item.description && (
                            <p className="text-gray-600 dark:text-gray-400">{item.description}</p>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Interview Questions */}
                {currentResult.interview_questions && currentResult.interview_questions.length > 0 && (
                  <div className="glass-card">
                    <h2 className="text-2xl font-bold mb-4">Interview Questions</h2>
                    <div className="space-y-4">
                      {currentResult.interview_questions.map((question) => (
                        <div
                          key={question.id}
                          className="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg"
                        >
                          <div className="flex items-start justify-between mb-2">
                            <p className="font-medium">{question.question}</p>
                            {question.category && (
                              <span className="ml-4 px-2 py-1 bg-primary-100 dark:bg-primary-900/30 text-primary-800 dark:text-primary-300 rounded text-xs font-medium whitespace-nowrap">
                                {question.category}
                              </span>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Learning Resources */}
                {currentResult.learning_resources && currentResult.learning_resources.length > 0 && (
                  <div className="glass-card">
                    <h2 className="text-2xl font-bold mb-4">Learning Resources</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {currentResult.learning_resources.map((resource) => (
                        <div
                          key={resource.id}
                          className="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                        >
                          <h3 className="font-semibold mb-2">{resource.title}</h3>
                          {resource.description && (
                            <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                              {resource.description}
                            </p>
                          )}
                          <div className="flex items-center justify-between">
                            {resource.resource_type && (
                              <span className="px-2 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-300 rounded text-xs">
                                {resource.resource_type}
                              </span>
                            )}
                            {resource.url && (
                              <a
                                href={resource.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-primary-600 dark:text-primary-400 hover:underline text-sm"
                              >
                                Visit Resource →
                              </a>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="glass-card text-center py-12">
                <p className="text-gray-600 dark:text-gray-400">
                  Select an analysis result to view preparation content
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default JobPreparation

