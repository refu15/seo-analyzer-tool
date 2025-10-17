import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { sitesApi } from '../services/api'
import { Globe, Trash2, Eye, Plus } from 'lucide-react'

export default function SiteList() {
  const navigate = useNavigate()
  const [sites, setSites] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchSites()
  }, [])

  const fetchSites = async () => {
    try {
      const response = await sitesApi.getAll()
      setSites(response.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (siteId, siteName) => {
    if (!confirm(`「${siteName}」を削除してもよろしいですか？`)) {
      return
    }

    try {
      await sitesApi.delete(siteId)
      setSites(sites.filter(site => site.id !== siteId))
    } catch (err) {
      console.error(err)
      alert('削除に失敗しました')
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div>
      <div className="mb-8 flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">サイト一覧</h2>
          <p className="mt-2 text-gray-600">登録されているサイトの管理</p>
        </div>
        <Link
          to="/sites/add"
          className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700"
        >
          <Plus className="h-5 w-5 mr-2" />
          サイトを追加
        </Link>
      </div>

      {sites.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-lg shadow">
          <Globe className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">サイトが登録されていません</h3>
          <p className="mt-1 text-sm text-gray-500">最初のサイトを追加して分析を開始しましょう</p>
        </div>
      ) : (
        <div className="bg-white shadow overflow-hidden sm:rounded-lg">
          <ul className="divide-y divide-gray-200">
            {sites.map((site) => (
              <li key={site.id} className="px-6 py-4 hover:bg-gray-50">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center">
                      <Globe className="h-5 w-5 text-gray-400 mr-3" />
                      <div>
                        <h3 className="text-lg font-medium text-gray-900">
                          {site.name || site.domain}
                        </h3>
                        <p className="text-sm text-gray-500">{site.url}</p>
                      </div>
                    </div>
                    <div className="mt-2 flex items-center text-sm text-gray-500">
                      {site.latest_score !== null && (
                        <span className="mr-4">スコア: {Math.round(site.latest_score)}/100</span>
                      )}
                      {site.last_analyzed_at && (
                        <span>最終分析: {new Date(site.last_analyzed_at).toLocaleDateString('ja-JP')}</span>
                      )}
                    </div>
                  </div>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => navigate(`/sites/${site.id}`)}
                      className="inline-flex items-center px-3 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                    >
                      <Eye className="h-4 w-4 mr-1" />
                      詳細
                    </button>
                    <button
                      onClick={() => handleDelete(site.id, site.name || site.domain)}
                      className="inline-flex items-center px-3 py-2 border border-red-300 rounded-md text-sm font-medium text-red-700 bg-white hover:bg-red-50"
                    >
                      <Trash2 className="h-4 w-4 mr-1" />
                      削除
                    </button>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
