import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import SiteList from './pages/SiteList'
import AddSite from './pages/AddSite'
import SiteDetail from './pages/SiteDetail'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="sites" element={<SiteList />} />
        <Route path="sites/add" element={<AddSite />} />
        <Route path="sites/:siteId" element={<SiteDetail />} />
      </Route>
    </Routes>
  )
}

export default App
