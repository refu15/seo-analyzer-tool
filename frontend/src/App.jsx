import { Routes, Route } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import Layout from './components/Layout'
import ProtectedRoute from './components/ProtectedRoute'
import Login from './pages/Login'
import Signup from './pages/Signup'
import Dashboard from './pages/Dashboard'
import SiteList from './pages/SiteList'
import AddSite from './pages/AddSite'
import SiteDetail from './pages/SiteDetail'

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />

        <Route path="/" element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }>
          <Route index element={<Dashboard />} />
          <Route path="sites" element={<SiteList />} />
          <Route path="sites/add" element={<AddSite />} />
          <Route path="sites/:siteId" element={<SiteDetail />} />
        </Route>
      </Routes>
    </AuthProvider>
  )
}

export default App
