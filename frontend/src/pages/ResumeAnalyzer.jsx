import { useState, useEffect } from 'react'
import api from '../services/api'

const ResumeAnalyzer = () => {
  const [resumes, setResumes] = useState([])
  const [jobDescriptions, setJobDescriptions] = useState([])
  const [selectedResume, setSelectedResume] = useState('')
  const [selectedJD, setSelectedJD] = useState('')
  const [jdTitle, setJdTitle] = useState('')
  const [jdCompany, setJdCompany] = useState('')
  const [jdDescription, setJdDescription] = useState('')
  const [uploading, setUploading] = useState(false)
  const [analyzing, setAnalyzing] = useState(false)
  const [analysisResult, setAnalysisResult] = useState(null)
  const [error, setError] = useState('')
  const [showJDForm, setShowJDForm] = useState(false)

  useEffect(() => {
    fetchResumes()
    fetchJobDescriptions()
  }, [])

  const fetchResumes = async () => {
    try {
      const response = await api.get('/resumes/')
      setResumes(response.data)
    } catch (error) {
      console.error('Failed to fetch resumes:', error)
    }
  }

  const fetchJobDescriptions = async () => {
    try {
      const response = await api.get('/job-descriptions/')
      setJobDescriptions(response.data)
    } catch (error) {
      console.error('Failed to fetch job descriptions:', error)
    }
  }

  const handleFileUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    const validExtensions = ['.pdf', '.docx', '.doc']
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase()
    if (!validExtensions.includes(fileExtension)) {
      setError('Only PDF and DOCX files are supported')
      return
    }

    setUploading(true)
    setError('')

    try {
      const formData = new FormData()
      formData.append('file', file)

      await api.post('/resumes/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      await fetchResumes()
      setError('')
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to upload resume')
    } finally {
      setUploading(false)
    }
  }

  const handleCreateJD = async (e) => {
    e.preventDefault()
    setError('')

    try {
      await api.post('/job-descriptions/', {
        title: jdTitle,
        company: jdCompany,
        description: jdDescription,
      })

      await fetchJobDescriptions()
      setJdTitle('')
      setJdCompany('')
      setJdDescription('')
      setShowJDForm(false)
      setError('')
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create job description')
    }
  }

  const handleAnalyze = async () => {
    if (!selectedResume || !selectedJD) {
      setError('Please select both a resume and a job description')
      return
    }

    setAnalyzing(true)
    setError('')
    setAnalysisResult(null)

    try {
      const response = await api.post('/analysis/analyze', {
        resume_id: parseInt(selectedResume),
        job_description_id: parseInt(selectedJD),
      })

      setAnalysisResult(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to analyze resume')
    } finally {
      setAnalyzing(false)
    }
  }

  return (
    <div className="min-h-screen p-6">
      <div className="container mx-auto max-w-6xl">
        <h1 className="text-3xl font-bold mb-8">Resume Analyzer</h1>

        {error && (
          <div className="mb-6 p-4 bg-red-100 dark:bg-red-900/30 border border-red-300 dark:border-red-700 rounded-lg text-red-700 dark:text-red-300">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Resume Upload Section */}
          <div className="glass-card">
            <h2 className="text-xl font-semibold mb-4">Upload Resume</h2>
            <div className="mb-4">
              <label className="block text-sm font-medium mb-2">Upload PDF or DOCX</label>
              <input
                type="file"
                accept=".pdf,.docx,.doc"
                onChange={handleFileUpload}
                disabled={uploading}
                className="input-field"
              />
              {uploading && <p className="mt-2 text-sm text-gray-600">Uploading...</p>}
            </div>

            <div className="mt-4">
              <label className="block text-sm font-medium mb-2">Select Resume</label>
              <select
                value={selectedResume}
                onChange={(e) => setSelectedResume(e.target.value)}
                className="input-field"
              >
                <option value="">Select a resume</option>
                {resumes.map((resume) => (
                  <option key={resume.id} value={resume.id}>
                    {resume.filename}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Job Description Section */}
          <div className="glass-card">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold">Job Description</h2>
              <button
                onClick={() => setShowJDForm(!showJDForm)}
                className="btn-secondary text-sm"
              >
                {showJDForm ? 'Cancel' : '+ New JD'}
              </button>
            </div>

            {showJDForm ? (
              <form onSubmit={handleCreateJD} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Job Title</label>
                  <input
                    type="text"
                    value={jdTitle}
                    onChange={(e) => setJdTitle(e.target.value)}
                    className="input-field"
                    placeholder="e.g., Senior Software Engineer"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Company</label>
                  <input
                    type="text"
                    value={jdCompany}
                    onChange={(e) => setJdCompany(e.target.value)}
                    className="input-field"
                    placeholder="Company name (optional)"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Description</label>
                  <textarea
                    value={jdDescription}
                    onChange={(e) => setJdDescription(e.target.value)}
                    className="input-field"
                    rows="6"
                    placeholder="Paste job description here..."
                    required
                  />
                </div>
                <button type="submit" className="btn-primary w-full">
                  Create Job Description
                </button>
              </form>
            ) : (
              <div>
                <label className="block text-sm font-medium mb-2">Select Job Description</label>
                <select
                  value={selectedJD}
                  onChange={(e) => setSelectedJD(e.target.value)}
                  className="input-field"
                >
                  <option value="">Select a job description</option>
                  {jobDescriptions.map((jd) => (
                    <option key={jd.id} value={jd.id}>
                      {jd.title} {jd.company ? `- ${jd.company}` : ''}
                    </option>
                  ))}
                </select>
              </div>
            )}
          </div>
        </div>

        {/* Analyze Button */}
        <div className="mt-6 text-center">
          <button
            onClick={handleAnalyze}
            disabled={analyzing || !selectedResume || !selectedJD}
            className="btn-primary text-lg px-8 py-3 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {analyzing ? 'Analyzing...' : 'Analyze Resume'}
          </button>
        </div>

        {/* Analysis Results */}
        {analysisResult && (
          <div className="mt-8 glass-card">
            <h2 className="text-2xl font-bold mb-6">Analysis Results</h2>

            {/* Match Score */}
            <div className="mb-6 p-6 bg-gradient-to-r from-primary-50 to-primary-100 dark:from-primary-900/30 dark:to-primary-800/30 rounded-lg">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Match Score</p>
                  <p className="text-4xl font-bold text-primary-600 dark:text-primary-400">
                    {analysisResult.similarity_score.toFixed(1)}%
                  </p>
                </div>
                <div className="text-right">
                  <p className="text-sm text-gray-600 dark:text-gray-400">Status</p>
                  <p className={`text-2xl font-bold ${
                    analysisResult.match_status === 'Good Match' ? 'text-green-600 dark:text-green-400' :
                    analysisResult.match_status === 'Partial Match' ? 'text-yellow-600 dark:text-yellow-400' :
                    'text-red-600 dark:text-red-400'
                  }`}>
                    {analysisResult.match_status}
                  </p>
                </div>
              </div>
            </div>

            {/* Skills Analysis */}
            {analysisResult.skills && analysisResult.skills.length > 0 && (
              <div className="mb-6">
                <h3 className="text-xl font-semibold mb-4">Skills Analysis</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <h4 className="font-medium text-green-600 dark:text-green-400 mb-2">Present Skills</h4>
                    <div className="flex flex-wrap gap-2">
                      {analysisResult.skills
                        .filter(s => s.is_present)
                        .map((skill) => (
                          <span key={skill.id} className="px-3 py-1 bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300 rounded-full text-sm">
                            {skill.skill_name}
                          </span>
                        ))}
                    </div>
                  </div>
                  <div>
                    <h4 className="font-medium text-red-600 dark:text-red-400 mb-2">Missing Skills</h4>
                    <div className="flex flex-wrap gap-2">
                      {analysisResult.skills
                        .filter(s => s.is_required && !s.is_present)
                        .map((skill) => (
                          <span key={skill.id} className="px-3 py-1 bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-300 rounded-full text-sm">
                            {skill.skill_name}
                          </span>
                        ))}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Correction Suggestions */}
            {analysisResult.correction_suggestions && (
              <div className="mb-6">
                <h3 className="text-xl font-semibold mb-4">Correction Suggestions</h3>
                <div className="p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg">
                  <pre className="whitespace-pre-wrap text-sm text-gray-700 dark:text-gray-300">
                    {analysisResult.correction_suggestions}
                  </pre>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default ResumeAnalyzer

