import axios from 'axios'

// FIX 1: Use 'VITE_API_BASE_URL' (to match Vercel) instead of 'VITE_API_URL'
// FIX 2: Add '/api' to the end, because your Backend Swagger docs show all routes start with /api
const getBaseUrl = () => {
  // Check if we are in production (Vercel) or local
  const url = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
  
  // Remove trailing slash if it exists to avoid double slashes
  const cleanUrl = url.endsWith('/') ? url.slice(0, -1) : url;
  
  // Append /api
  return `${cleanUrl}/api`;
}

const api = axios.create({
  baseURL: getBaseUrl(),
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests if available
const token = localStorage.getItem('token')
if (token) {
  api.defaults.headers.common['Authorization'] = `Bearer ${token}`
}

export default api