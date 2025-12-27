import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'

const Profile = () => {
  const { user } = useAuth()
  const [resumes, setResumes] = useState([])
  const [jobDescriptions, setJobDescriptions] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchUserData()
  }, [])

  const fetchUserData = async () => {
    try {
      const [resumesRes, jdsRes] = await Promise.all([
        api.get('/api/resumes/'),
        api.get('/api/job-descriptions/'),
      ])
      setResumes(resumesRes.data)
      setJobDescriptions(jdsRes.data)
    } catch (error) {
      console.error('Failed to fetch user data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteResume = async (resumeId) => {
    if (!window.confirm('Are you sure you want to delete this resume?')) return

    try {
      // Note: Delete endpoint would need to be added to backend
      // For now, just show a message
      alert('Delete functionality would be implemented here')
    } catch (error) {
      console.error('Failed to delete resume:', error)
    }
  }

  const handleDeleteJD = async (jdId) => {
    if (!window.confirm('Are you sure you want to delete this job description?')) return

    try {
      await api.delete(`/api/job-descriptions/${jdId}`)
      await fetchUserData()
    } catch (error) {
      console.error('Failed to delete job description:', error)
      alert('Failed to delete job description')
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
        <h1 className="text-3xl font-bold mb-8">Profile</h1>

        {/* User Info */}
        <div className="glass-card mb-6">
          <h2 className="text-xl font-semibold mb-4">Account Information</h2>
          <div className="space-y-3">
            <div>
              <label className="text-sm font-medium text-gray-600 dark:text-gray-400">Email</label>
              <p className="text-lg">{user?.email}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-600 dark:text-gray-400">Full Name</label>
              <p className="text-lg">{user?.full_name || 'Not set'}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-600 dark:text-gray-400">Member Since</label>
              <p className="text-lg">
                {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
              </p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Resumes */}
          <div className="glass-card">
            <h2 className="text-xl font-semibold mb-4">My Resumes ({resumes.length})</h2>
            <div className="space-y-3 max-h-[400px] overflow-y-auto">
              {resumes.length === 0 ? (
                <p className="text-gray-500 dark:text-gray-400">No resumes uploaded yet</p>
              ) : (
                resumes.map((resume) => (
                  <div
                    key={resume.id}
                    className="p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg flex items-center justify-between"
                  >
                    <div>
                      <p className="font-medium">{resume.filename}</p>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        Uploaded: {new Date(resume.uploaded_at).toLocaleDateString()}
                      </p>
                    </div>
                    <button
                      onClick={() => handleDeleteResume(resume.id)}
                      className="text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 text-sm"
                    >
                      Delete
                    </button>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Job Descriptions */}
          <div className="glass-card">
            <h2 className="text-xl font-semibold mb-4">My Job Descriptions ({jobDescriptions.length})</h2>
            <div className="space-y-3 max-h-[400px] overflow-y-auto">
              {jobDescriptions.length === 0 ? (
                <p className="text-gray-500 dark:text-gray-400">No job descriptions created yet</p>
              ) : (
                jobDescriptions.map((jd) => (
                  <div
                    key={jd.id}
                    className="p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg flex items-center justify-between"
                  >
                    <div>
                      <p className="font-medium">{jd.title}</p>
                      {jd.company && (
                        <p className="text-sm text-gray-600 dark:text-gray-400">{jd.company}</p>
                      )}
                      <p className="text-xs text-gray-500 dark:text-gray-500">
                        Created: {new Date(jd.created_at).toLocaleDateString()}
                      </p>
                    </div>
                    <button
                      onClick={() => handleDeleteJD(jd.id)}
                      className="text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 text-sm"
                    >
                      Delete
                    </button>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Profile

