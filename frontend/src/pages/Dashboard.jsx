import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { sitesApi } from '../services/api'
import { Globe, TrendingUp, AlertCircle } from 'lucide-react'

export default function Dashboard() {
  const [sites, setSites] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchSites()
  }, [])

  const fetchSites = async () => {
    try {
      const response = await sitesApi.getAll()
      setSites(response.data)
    } catch (err) {
      setError('サイト一覧の取得に失敗しました')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600 bg-green-100'
    if (score >= 60) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
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
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-900">ダッシュボード</h2>
        <p className="mt-2 text-gray-600">登録されているサイトのSEO状況を確認できます</p>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6 flex items-start">
          <AlertCircle className="h-5 w-5 text-red-400 mr-3 mt-0.5" />
          <div>
            <h3 className="text-sm font-medium text-red-800">エラー</h3>
            <p className="mt-1 text-sm text-red-700">{error}</p>
          </div>
        </div>
      )}

      {sites.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-lg shadow">
          <Globe className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">サイトが登録されていません</h3>
          <p className="mt-1 text-sm text-gray-500">最初のサイトを追加して分析を開始しましょう</p>
          <div className="mt-6">
            <Link
              to="/sites/add"
              className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700"
            >
              サイトを追加
            </Link>
          </div>
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {sites.map((site) => (
            <Link
              key={site.id}
              to={`/sites/${site.id}`}
              className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow p-6"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 truncate">
                    {site.name || site.domain}
                  </h3>
                  <p className="mt-1 text-sm text-gray-500 truncate">{site.domain}</p>
                </div>
                {site.latest_score !== null && (
                  <div className={`ml-4 inline-flex items-center justify-center w-12 h-12 rounded-full ${getScoreColor(site.latest_score)}`}>
                    <span className="text-lg font-bold">{Math.round(site.latest_score)}</span>
                  </div>
                )}
              </div>

              <div className="mt-4 flex items-center text-sm text-gray-500">
                <TrendingUp className="h-4 w-4 mr-1" />
                {site.last_analyzed_at ? (
                  <span>最終分析: {new Date(site.last_analyzed_at).toLocaleDateString('ja-JP')}</span>
                ) : (
                  <span>未分析</span>
                )}
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
