import { useState } from 'react'
import { ChevronDown, ChevronUp, Info, CheckCircle, XCircle, AlertCircle } from 'lucide-react'

export default function ScoreBreakdown({ scoreBreakdown }) {
  const [expandedCategories, setExpandedCategories] = useState({})

  if (!scoreBreakdown) return null

  const toggleCategory = (category) => {
    setExpandedCategories(prev => ({
      ...prev,
      [category]: !prev[category]
    }))
  }

  const getCategoryIcon = (category) => {
    const icons = {
      technical: '🔧',
      content: '📝',
      user_experience: '👤',
      authority: '⭐'
    }
    return icons[category] || '📊'
  }

  const getCategoryLabel = (category) => {
    const labels = {
      technical: '技術的SEO',
      content: 'コンテンツ品質',
      user_experience: 'ユーザー体験',
      authority: '権威性'
    }
    return labels[category] || category
  }

  const getStatusIcon = (status) => {
    const statusLower = status?.toLowerCase()
    if (statusLower === 'pass' || statusLower === 'optimal' || statusLower === 'excellent' || statusLower === 'good') {
      return <CheckCircle className="h-5 w-5 text-green-500" />
    } else if (statusLower === 'fail' || statusLower === 'missing' || statusLower === 'poor') {
      return <XCircle className="h-5 w-5 text-red-500" />
    } else {
      return <AlertCircle className="h-5 w-5 text-yellow-500" />
    }
  }

  const getStatusColor = (status) => {
    const statusLower = status?.toLowerCase()
    if (statusLower === 'pass' || statusLower === 'optimal' || statusLower === 'excellent' || statusLower === 'good') {
      return 'text-green-700 bg-green-50'
    } else if (statusLower === 'fail' || statusLower === 'missing' || statusLower === 'poor') {
      return 'text-red-700 bg-red-50'
    } else {
      return 'text-yellow-700 bg-yellow-50'
    }
  }

  const categories = ['technical', 'content', 'user_experience', 'authority']

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center mb-6">
        <Info className="h-6 w-6 text-blue-500 mr-2" />
        <h3 className="text-xl font-bold text-gray-900">スコア詳細内訳</h3>
      </div>

      <div className="space-y-4">
        {categories.map(category => {
          const categoryData = scoreBreakdown[category]
          if (!categoryData) return null

          const isExpanded = expandedCategories[category]

          return (
            <div key={category} className="border border-gray-200 rounded-lg overflow-hidden">
              {/* Category Header */}
              <button
                onClick={() => toggleCategory(category)}
                className="w-full px-4 py-4 bg-gray-50 hover:bg-gray-100 flex items-center justify-between transition-colors"
              >
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">{getCategoryIcon(category)}</span>
                  <div className="text-left">
                    <h4 className="font-semibold text-gray-900">{getCategoryLabel(category)}</h4>
                    <p className="text-sm text-gray-500">
                      {categoryData.score}点 / 100点 (重み: {(categoryData.weight * 100).toFixed(0)}%)
                    </p>
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  <div className="text-right">
                    <p className="text-sm text-gray-500">貢献度</p>
                    <p className="font-bold text-primary-600">{categoryData.contribution}点</p>
                  </div>
                  {isExpanded ? (
                    <ChevronUp className="h-5 w-5 text-gray-400" />
                  ) : (
                    <ChevronDown className="h-5 w-5 text-gray-400" />
                  )}
                </div>
              </button>

              {/* Category Details */}
              {isExpanded && categoryData.details && (
                <div className="px-4 py-4 bg-white">
                  <div className="space-y-3">
                    {Object.entries(categoryData.details).map(([key, detail]) => (
                      <div key={key} className={`p-3 rounded-lg border ${getStatusColor(detail.status)}`}>
                        <div className="flex items-start justify-between">
                          <div className="flex items-start space-x-3 flex-1">
                            {getStatusIcon(detail.status)}
                            <div className="flex-1">
                              <div className="flex items-center justify-between mb-1">
                                <h5 className="font-medium text-gray-900">{detail.description}</h5>
                                <span className="text-sm font-semibold">
                                  {detail.points_earned} / {detail.max_points}点
                                </span>
                              </div>
                              {detail.value && (
                                <p className="text-sm text-gray-600 mt-1">{detail.value}</p>
                              )}
                              <div className="mt-2">
                                <div className="w-full bg-gray-200 rounded-full h-2">
                                  <div
                                    className="bg-primary-600 h-2 rounded-full transition-all"
                                    style={{
                                      width: `${(detail.points_earned / detail.max_points) * 100}%`
                                    }}
                                  />
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )
        })}
      </div>

      {/* Summary */}
      <div className="mt-6 pt-6 border-t border-gray-200">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {categories.map(category => {
            const categoryData = scoreBreakdown[category]
            if (!categoryData) return null

            return (
              <div key={category} className="text-center">
                <p className="text-sm text-gray-500 mb-1">{getCategoryLabel(category)}</p>
                <p className="text-xl font-bold text-gray-900">{categoryData.contribution}点</p>
                <p className="text-xs text-gray-400">({(categoryData.weight * 100).toFixed(0)}%の重み)</p>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
