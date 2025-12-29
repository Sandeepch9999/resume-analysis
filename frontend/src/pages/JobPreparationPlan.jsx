import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'

const JobPreparationPlan = () => {
  const [jobDescriptions, setJobDescriptions] = useState([])
  const [matchResults, setMatchResults] = useState([])
  const [selectedJD, setSelectedJD] = useState('')
  const [selectedMatchResult, setSelectedMatchResult] = useState('')
  const [jdText, setJdText] = useState('')
  const [loading, setLoading] = useState(false)
  const [plan, setPlan] = useState(null)
  const [error, setError] = useState('')
  const [plans, setPlans] = useState([])
  const navigate = useNavigate()

  useEffect(() => {
    fetchJobDescriptions()
    fetchMatchResults()
    fetchPlans()
  }, [])

  const fetchJobDescriptions = async () => {
    try {
      const response = await api.get('/job-descriptions/')
      setJobDescriptions(response.data)
    } catch (error) {
      console.error('Failed to fetch job descriptions:', error)
    }
  }

  const fetchMatchResults = async () => {
    try {
      const response = await api.get('/analysis/results')
      setMatchResults(response.data)
    } catch (error) {
      console.error('Failed to fetch match results:', error)
    }
  }

  const fetchPlans = async () => {
    try {
      const response = await api.get('/job-preparation-plan/')
      setPlans(response.data)
    } catch (error) {
      console.error('Failed to fetch plans:', error)
    }
  }

  const handleCreatePlan = async () => {
    if (!selectedJD && !jdText.trim()) {
      setError('Please select a job description or enter job description text')
      return
    }

    setLoading(true)
    setError('')
    setPlan(null)

    try {
      const requestData = {}
      
      if (selectedJD) {
        requestData.job_description_id = parseInt(selectedJD)
      } else {
        requestData.job_description_text = jdText
      }

      if (selectedMatchResult) {
        requestData.match_result_id = parseInt(selectedMatchResult)
      }

      const response = await api.post('/job-preparation-plan/', requestData)
      setPlan(response.data)
      await fetchPlans()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create preparation plan')
    } finally {
      setLoading(false)
    }
  }

  const handleViewPlan = async (planId) => {
    try {
      const response = await api.get(`/job-preparation-plan/${planId}`)
      setPlan(response.data)
    } catch (error) {
      setError('Failed to load plan')
    }
  }

  return (
    <div className="min-h-screen p-6">
      <div className="container mx-auto max-w-6xl">
        <h1 className="text-3xl font-bold mb-8">Job Preparation Plan</h1>

        {error && (
          <div className="mb-6 p-4 bg-red-100 dark:bg-red-900/30 border border-red-300 dark:border-red-700 rounded-lg text-red-700 dark:text-red-300">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Create Plan Section */}
          <div className="lg:col-span-1">
            <div className="glass-card mb-6">
              <h2 className="text-xl font-semibold mb-4">Create New Plan</h2>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Select Job Description</label>
                  <select
                    value={selectedJD}
                    onChange={(e) => {
                      setSelectedJD(e.target.value)
                      setJdText('')
                    }}
                    className="input-field"
                  >
                    <option value="">Or enter text below</option>
                    {jobDescriptions.map((jd) => (
                      <option key={jd.id} value={jd.id}>
                        {jd.title} {jd.company ? `- ${jd.company}` : ''}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Or Enter Job Description</label>
                  <textarea
                    value={jdText}
                    onChange={(e) => {
                      setJdText(e.target.value)
                      setSelectedJD('')
                    }}
                    className="input-field"
                    rows="4"
                    placeholder="Paste job description here..."
                    disabled={!!selectedJD}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Select Analysis (Optional)</label>
                  <select
                    value={selectedMatchResult}
                    onChange={(e) => setSelectedMatchResult(e.target.value)}
                    className="input-field"
                  >
                    <option value="">None</option>
                    {matchResults.map((result) => (
                      <option key={result.id} value={result.id}>
                        Analysis #{result.id} - {result.match_status}
                      </option>
                    ))}
                  </select>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    Select to use missing skills from analysis
                  </p>
                </div>

                <button
                  onClick={handleCreatePlan}
                  disabled={loading || (!selectedJD && !jdText.trim())}
                  className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? 'Creating Plan...' : 'Generate Plan'}
                </button>
              </div>
            </div>

            {/* Saved Plans */}
            {plans.length > 0 && (
              <div className="glass-card">
                <h2 className="text-xl font-semibold mb-4">Saved Plans</h2>
                <div className="space-y-2 max-h-[400px] overflow-y-auto">
                  {plans.map((savedPlan) => (
                    <button
                      key={savedPlan.id}
                      onClick={() => handleViewPlan(savedPlan.id)}
                      className={`w-full text-left p-3 rounded-lg transition-colors ${
                        plan?.id === savedPlan.id
                          ? 'bg-primary-100 dark:bg-primary-900/30 border-2 border-primary-500'
                          : 'bg-gray-50 dark:bg-gray-700/50 hover:bg-gray-100 dark:hover:bg-gray-700'
                      }`}
                    >
                      <p className="font-medium">{savedPlan.title}</p>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {savedPlan.total_estimated_days} days
                      </p>
                      <p className="text-xs text-gray-500 dark:text-gray-500">
                        {new Date(savedPlan.created_at).toLocaleDateString()}
                      </p>
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Plan Display */}
          <div className="lg:col-span-2">
            {plan ? (
              <div className="space-y-6">
                {/* Plan Header */}
                <div className="glass-card">
                  <h2 className="text-2xl font-bold mb-2">{plan.title}</h2>
                  {plan.description && (
                    <p className="text-gray-600 dark:text-gray-400 mb-4">{plan.description}</p>
                  )}
                  <div className="flex items-center space-x-4">
                    <div className="px-4 py-2 bg-primary-100 dark:bg-primary-900/30 rounded-lg">
                      <p className="text-sm text-gray-600 dark:text-gray-400">Total Duration</p>
                      <p className="text-xl font-bold text-primary-600 dark:text-primary-400">
                        {plan.total_estimated_days} days
                      </p>
                    </div>
                    <div className="px-4 py-2 bg-primary-100 dark:bg-primary-900/30 rounded-lg">
                      <p className="text-sm text-gray-600 dark:text-gray-400">Phases</p>
                      <p className="text-xl font-bold text-primary-600 dark:text-primary-400">
                        {plan.phases.length}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Phases Timeline */}
                <div className="space-y-6">
                  {plan.phases.map((phase, index) => (
                    <div key={phase.id} className="phase-card">
                      <div className="flex items-start space-x-4">
                        {/* Phase Number Badge */}
                        <div className="flex-shrink-0">
                          <div className="w-12 h-12 rounded-full bg-primary-600 dark:bg-primary-500 text-gray-900 flex items-center justify-center font-bold text-lg">
                            {phase.phase_number}
                          </div>
                        </div>

                        {/* Phase Content */}
                        <div className="flex-1">
                          <div className="flex items-center justify-between mb-2">
                            <h3 className="text-xl font-semibold">{phase.phase_name}</h3>
                            {phase.estimated_days && (
                              <span className="ios-badge">
                                {phase.estimated_days} days
                              </span>
                            )}
                          </div>
                          {phase.description && (
                            <p className="text-gray-600 dark:text-gray-400 mb-4">{phase.description}</p>
                          )}

                          {/* Topics */}
                          <div className="space-y-3">
                            {phase.topics.map((topic) => (
                              <div
                                key={topic.id}
                                className="topic-card"
                              >
                                <div className="flex items-start justify-between mb-2">
                                  <h4 className="font-semibold text-lg">{topic.topic_name}</h4>
                                  {topic.estimated_hours && (
                                    <span className="text-sm text-gray-500 dark:text-gray-400">
                                      ~{topic.estimated_hours}h
                                    </span>
                                  )}
                                </div>
                                {topic.description && (
                                  <p className="text-gray-600 dark:text-gray-400 mb-2">
                                    {topic.description}
                                  </p>
                                )}
                                {topic.practice_tasks && (
                                  <div className="mt-2 p-2 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded">
                                    <p className="text-sm font-medium text-yellow-800 dark:text-yellow-300 mb-1">
                                      Practice:
                                    </p>
                                    <p className="text-sm text-yellow-700 dark:text-yellow-400">
                                      {topic.practice_tasks}
                                    </p>
                                  </div>
                                )}
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="glass-card text-center py-12">
                <p className="text-gray-600 dark:text-gray-400">
                  Create a new preparation plan or select a saved plan to view
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default JobPreparationPlan

