import { createContext, useContext, useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'

const AuthContext = createContext()

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [token, setToken] = useState(() => {
    return localStorage.getItem('token')
  })

  useEffect(() => {
    if (token) {
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`
      fetchUser()
    } else {
      setLoading(false)
    }
  }, [token])

  const fetchUser = async () => {
    try {
      // FIXED: Removed '/api' because api.js already adds it
      const response = await api.get('/auth/me') 
      setUser(response.data)
    } catch (error) {
      console.error('Failed to fetch user:', error)
      logout()
    } finally {
      setLoading(false)
    }
  }

  const login = async (email, password) => {
    try {
      // OAuth2PasswordRequestForm expects URL-encoded form data
      const params = new URLSearchParams()
      params.append('username', email)
      params.append('password', password)

      // FIXED: Removed '/api' 
      const response = await api.post('/auth/login', params.toString(), {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      })

      const { access_token } = response.data
      setToken(access_token)
      localStorage.setItem('token', access_token)
      api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
      
      await fetchUser()
      return response.data
    } catch (error) {
      console.error('Login error:', error)
      // Re-throw with better error message
      const errorMessage = error.response?.data?.detail || 
                           error.message || 
                           'Login failed. Please check your credentials and try again.'
      throw new Error(errorMessage)
    }
  }

  const register = async (email, password, fullName) => {
    // FIXED: Removed '/api' 
    const response = await api.post('/auth/register', {
      email,
      password,
      full_name: fullName,
    })

    // Auto login after registration
    await login(email, password)
    return response.data
  }

  const logout = () => {
    setToken(null)
    setUser(null)
    localStorage.removeItem('token')
    delete api.defaults.headers.common['Authorization']
  }

  return (
    <AuthContext.Provider value={{ user, login, register, logout, loading }}>
      {children}
    </AuthContext.Provider>
  )
}