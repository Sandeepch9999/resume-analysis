import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const Login = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await login(email, password)
      navigate('/dashboard')
    } catch (err) {
      // Better error handling
      const errorMsg = err.message || 
                      err.response?.data?.detail || 
                      'Login failed. Please check your credentials and try again.'
      setError(errorMsg)
      console.error('Login error details:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-primary-100 dark:from-gray-900 dark:to-gray-800 px-4">
      <div className="max-w-md w-full bg-white/70 dark:bg-gray-800/70 backdrop-blur-xl rounded-xl p-6 border border-white/50 dark:border-gray-700/50 shadow-xl">
        <h1 className="text-3xl font-bold text-center mb-6 text-primary-600 dark:text-primary-400">
          Welcome Back
        </h1>
        
        {/* Demo Credentials Card */}
        <div className="mb-6 p-4 bg-primary-50/80 dark:bg-primary-900/30 backdrop-blur-sm rounded-lg border border-primary-200/50 dark:border-primary-800/50">
          <h3 className="text-sm font-semibold text-primary-800 dark:text-primary-200 mb-2">
            Demo Credentials
          </h3>
          <div className="text-sm text-primary-700 dark:text-primary-300 space-y-1">
            <p><strong>Email:</strong> demo@project.com</p>
            <p><strong>Password:</strong> Demo@123</p>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {error && (
            <div className="p-3 bg-red-100 dark:bg-red-900/30 border border-red-300 dark:border-red-700 rounded-lg text-red-700 dark:text-red-300 text-sm">
              {error}
            </div>
          )}

          <div>
            <label className="block text-sm font-medium mb-2">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="input-field"
              placeholder="Enter your email"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="input-field"
              placeholder="Enter your password"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn-primary w-full"
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <p className="mt-4 text-center text-sm text-gray-600 dark:text-gray-400">
          Don't have an account?{' '}
          <Link to="/register" className="text-primary-600 dark:text-primary-400 hover:underline">
            Register here
          </Link>
        </p>
      </div>
    </div>
  )
}

export default Login

