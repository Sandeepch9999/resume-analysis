import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { ThemeProvider } from './context/ThemeContext'
import { AuthProvider, useAuth } from './context/AuthContext'
import ProtectedRoute from './components/ProtectedRoute'
import Header from './components/Header'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import ResumeAnalyzer from './pages/ResumeAnalyzer'
import JobPreparation from './pages/JobPreparation'
import JobPreparationPlan from './pages/JobPreparationPlan'
import Reports from './pages/Reports'
import Profile from './pages/Profile'

const AppRoutes = () => {
  const { user } = useAuth()

  return (
    <Routes>
      <Route
        path="/login"
        element={user ? <Navigate to="/dashboard" replace /> : <Login />}
      />
      <Route
        path="/register"
        element={user ? <Navigate to="/dashboard" replace /> : <Register />}
      />
      <Route
        path="/"
        element={<Navigate to={user ? "/dashboard" : "/login"} replace />}
      />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <>
              <Header />
              <Dashboard />
            </>
          </ProtectedRoute>
        }
      />
      <Route
        path="/resume-analyzer"
        element={
          <ProtectedRoute>
            <>
              <Header />
              <ResumeAnalyzer />
            </>
          </ProtectedRoute>
        }
      />
      <Route
        path="/job-preparation"
        element={
          <ProtectedRoute>
            <>
              <Header />
              <JobPreparation />
            </>
          </ProtectedRoute>
        }
      />
      <Route
        path="/job-preparation-plan"
        element={
          <ProtectedRoute>
            <>
              <Header />
              <JobPreparationPlan />
            </>
          </ProtectedRoute>
        }
      />
      <Route
        path="/reports"
        element={
          <ProtectedRoute>
            <>
              <Header />
              <Reports />
            </>
          </ProtectedRoute>
        }
      />
      <Route
        path="/profile"
        element={
          <ProtectedRoute>
            <>
              <Header />
              <Profile />
            </>
          </ProtectedRoute>
        }
      />
    </Routes>
  )
}

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <Router>
          <AppRoutes />
        </Router>
      </AuthProvider>
    </ThemeProvider>
  )
}

export default App

