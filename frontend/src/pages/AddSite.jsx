import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { sitesApi } from '../services/api'
import { AlertCircle, CheckCircle } from 'lucide-react'

export default function AddSite() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    url: '',
    name: '',
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      // Extract domain from URL
      const urlObj = new URL(formData.url.startsWith('http') ? formData.url : `https://${formData.url}`)
      const domain = urlObj.hostname

      await sitesApi.create({
        url: urlObj.href,
        domain: domain,
        name: formData.name || domain,
      })

      setSuccess(true)
      setTimeout(() => {
        navigate('/sites')
      }, 1500)
    } catch (err) {
      setError(err.response?.data?.detail || 'サイトの登録に失敗しました')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-900">サイトを追加</h2>
        <p className="mt-2 text-gray-600">SEO分析を行うウェブサイトを登録します</p>
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

      {success && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6 flex items-start">
          <CheckCircle className="h-5 w-5 text-green-400 mr-3 mt-0.5" />
          <div>
            <h3 className="text-sm font-medium text-green-800">成功</h3>
            <p className="mt-1 text-sm text-green-700">サイトを登録しました。サイト一覧にリダイレクトします...</p>
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit} className="bg-white shadow rounded-lg p-6">
        <div className="space-y-6">
          <div>
            <label htmlFor="url" className="block text-sm font-medium text-gray-700 mb-2">
              サイトURL <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              id="url"
              required
              value={formData.url}
              onChange={(e) => setFormData({ ...formData, url: e.target.value })}
              placeholder="https://example.com"
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
            />
            <p className="mt-1 text-sm text-gray-500">
              分析するウェブサイトのURLを入力してください
            </p>
          </div>

          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
              サイト名（任意）
            </label>
            <input
              type="text"
              id="name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              placeholder="例: 私のブログ"
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
            />
            <p className="mt-1 text-sm text-gray-500">
              空欄の場合はドメイン名が使用されます
            </p>
          </div>

          <div className="flex justify-end space-x-3">
            <button
              type="button"
              onClick={() => navigate('/sites')}
              className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              キャンセル
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? '登録中...' : 'サイトを登録'}
            </button>
          </div>
        </div>
      </form>
    </div>
  )
}
