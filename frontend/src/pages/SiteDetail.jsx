import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { sitesApi, analysisApi } from '../services/api'
import ScoreCard from '../components/ScoreCard'
import ScoreBreakdown from '../components/ScoreBreakdown'
import LLMAnalysisSection from '../components/LLMAnalysisSection'
import ActionPlan from '../components/ActionPlan'
import AnalysisProgress from '../components/AnalysisProgress'
import { Play, ArrowLeft, AlertCircle, TrendingUp, CheckCircle, Clock, Code, FileText, Eye, Award, Info } from 'lucide-react'

export default function SiteDetail() {
  const { siteId } = useParams()
  const navigate = useNavigate()
  const [site, setSite] = useState(null)
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(true)
  const [analyzing, setAnalyzing] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchSiteData()
  }, [siteId])

  const fetchSiteData = async () => {
    try {
      const siteResponse = await sitesApi.getById(siteId)
      setSite(siteResponse.data)

      // Try to get latest analysis
      try {
        const analysisResponse = await analysisApi.getLatest(siteId)
        setAnalysis(analysisResponse.data)
      } catch (err) {
        // No analysis yet
        setAnalysis(null)
      }
    } catch (err) {
      setError('サイト情報の取得に失敗しました')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleRunAnalysis = async () => {
    setAnalyzing(true)
    setError(null)

    try {
      await analysisApi.runAnalysis(siteId)
      // Progress component will handle the rest
    } catch (err) {
      setError(err.response?.data?.detail || '分析の開始に失敗しました')
      console.error(err)
      setAnalyzing(false)
    }
  }

  const handleAnalysisComplete = async (analysisId) => {
    // Refresh data when analysis completes
    await fetchSiteData()
    setAnalyzing(false)
  }

  const handleAnalysisError = (errorMessage) => {
    setError(errorMessage)
    setAnalyzing(false)
  }

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-800'
      case 'medium':
        return 'bg-yellow-100 text-yellow-800'
      case 'low':
        return 'bg-green-100 text-green-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getDifficultyLabel = (difficulty) => {
    switch (difficulty) {
      case 'easy':
        return '簡易'
      case 'moderate':
        return '中程度'
      case 'complex':
        return '複雑'
      default:
        return difficulty
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!site) {
    return (
      <div className="text-center py-12">
        <AlertCircle className="mx-auto h-12 w-12 text-gray-400" />
        <h3 className="mt-2 text-sm font-medium text-gray-900">サイトが見つかりません</h3>
      </div>
    )
  }

  return (
    <div>
      {/* Header */}
      <div className="mb-8">
        <button
          onClick={() => navigate('/sites')}
          className="flex items-center text-gray-600 hover:text-gray-900 mb-4"
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          サイト一覧に戻る
        </button>
        <div className="flex justify-between items-start">
          <div>
            <h2 className="text-3xl font-bold text-gray-900">{site.name || site.domain}</h2>
            <p className="mt-2 text-gray-600">{site.url}</p>
          </div>
          <button
            onClick={handleRunAnalysis}
            disabled={analyzing}
            className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Play className="h-5 w-5 mr-2" />
            {analyzing ? '分析中...' : 'SEO分析を実行'}
          </button>
        </div>
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

      {analyzing && (
        <div className="mb-6">
          <AnalysisProgress
            siteId={siteId}
            onComplete={handleAnalysisComplete}
            onError={handleAnalysisError}
          />
        </div>
      )}

      {!analysis ? (
        <div className="text-center py-12 bg-white rounded-lg shadow">
          <TrendingUp className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">まだ分析が実行されていません</h3>
          <p className="mt-1 text-sm text-gray-500">「SEO分析を実行」ボタンをクリックして分析を開始してください</p>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Score Overview */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-6">総合SEOスコア</h3>
            <div className="flex items-center justify-center mb-6">
              <div className="relative">
                <div className="w-32 h-32 rounded-full bg-gradient-to-br from-primary-400 to-primary-600 flex items-center justify-center">
                  <div className="w-28 h-28 bg-white rounded-full flex items-center justify-center">
                    <span className="text-4xl font-bold text-gray-900">
                      {Math.round(analysis.analysis.total_score)}
                    </span>
                  </div>
                </div>
              </div>
            </div>
            <p className="text-center text-gray-600">100点満点中</p>
          </div>

          {/* Category Scores */}
          <div>
            <h3 className="text-xl font-bold text-gray-900 mb-4">カテゴリー別スコア</h3>
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              <ScoreCard
                title="技術的SEO"
                score={Math.round(analysis.analysis.technical_score)}
              />
              <ScoreCard
                title="コンテンツ品質"
                score={Math.round(analysis.analysis.content_score)}
              />
              <ScoreCard
                title="ユーザー体験"
                score={Math.round(analysis.analysis.user_experience_score)}
              />
              <ScoreCard
                title="権威性"
                score={Math.round(analysis.analysis.authority_score)}
              />
            </div>
          </div>

          {/* Score Breakdown */}
          {analysis.analysis.score_breakdown && (
            <ScoreBreakdown scoreBreakdown={analysis.analysis.score_breakdown} />
          )}

          {/* PageSpeed Scores */}
          {(analysis.analysis.pagespeed_mobile_score || analysis.analysis.pagespeed_desktop_score) && (
            <div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">PageSpeed スコア</h3>
              <div className="grid gap-4 md:grid-cols-2">
                {analysis.analysis.pagespeed_mobile_score && (
                  <ScoreCard
                    title="モバイル"
                    score={Math.round(analysis.analysis.pagespeed_mobile_score)}
                  />
                )}
                {analysis.analysis.pagespeed_desktop_score && (
                  <ScoreCard
                    title="デスクトップ"
                    score={Math.round(analysis.analysis.pagespeed_desktop_score)}
                  />
                )}
              </div>
            </div>
          )}

          {/* Core Web Vitals */}
          {analysis.core_web_vitals && (
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Core Web Vitals</h3>
              <div className="grid gap-4 md:grid-cols-3">
                {analysis.core_web_vitals.lcp && (
                  <div>
                    <p className="text-sm text-gray-500 mb-1">Largest Contentful Paint</p>
                    <p className="text-2xl font-bold">{analysis.core_web_vitals.lcp.toFixed(2)}s</p>
                    <p className="text-xs text-gray-400 mt-1">目標: 2.5s以下</p>
                  </div>
                )}
                {analysis.core_web_vitals.fid && (
                  <div>
                    <p className="text-sm text-gray-500 mb-1">First Input Delay</p>
                    <p className="text-2xl font-bold">{analysis.core_web_vitals.fid.toFixed(0)}ms</p>
                    <p className="text-xs text-gray-400 mt-1">目標: 100ms以下</p>
                  </div>
                )}
                {analysis.core_web_vitals.cls && (
                  <div>
                    <p className="text-sm text-gray-500 mb-1">Cumulative Layout Shift</p>
                    <p className="text-2xl font-bold">{analysis.core_web_vitals.cls.toFixed(3)}</p>
                    <p className="text-xs text-gray-400 mt-1">目標: 0.1以下</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Recommendations */}
          {analysis.recommendations && analysis.recommendations.length > 0 && (
            <div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">改善提案</h3>
              <div className="space-y-3">
                {analysis.recommendations.map((rec, index) => (
                  <div key={index} className="bg-white rounded-lg shadow p-4">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center mb-2">
                          <h4 className="text-lg font-semibold text-gray-900">{rec.title}</h4>
                          <span className={`ml-3 px-2 py-1 text-xs font-medium rounded ${getPriorityColor(rec.priority)}`}>
                            {rec.priority === 'high' ? '高' : rec.priority === 'medium' ? '中' : '低'}優先度
                          </span>
                        </div>
                        <p className="text-gray-600 mb-3">{rec.description}</p>
                        <div className="flex items-center space-x-4 text-sm text-gray-500">
                          <span>実装難度: {getDifficultyLabel(rec.difficulty)}</span>
                          <span>期待効果: +{rec.expected_impact}点</span>
                          <span className="text-blue-600">{rec.category}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* LLM-Powered Deep Analysis */}
          {(analysis.llm_technical_analysis || analysis.llm_content_analysis ||
            analysis.llm_ux_analysis || analysis.llm_authority_analysis) && (
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-6 mt-8">AI詳細分析</h2>
              <div className="space-y-6">
                <LLMAnalysisSection
                  category="technical"
                  analysis={analysis.llm_technical_analysis}
                  title="技術的SEO 詳細分析"
                  icon={Code}
                  color="border-blue-500"
                />
                <LLMAnalysisSection
                  category="content"
                  analysis={analysis.llm_content_analysis}
                  title="コンテンツSEO 詳細分析"
                  icon={FileText}
                  color="border-green-500"
                />
                <LLMAnalysisSection
                  category="ux"
                  analysis={analysis.llm_ux_analysis}
                  title="UX/UI SEO 詳細分析"
                  icon={Eye}
                  color="border-purple-500"
                />
                <LLMAnalysisSection
                  category="authority"
                  analysis={analysis.llm_authority_analysis}
                  title="権威性・信頼性 詳細分析"
                  icon={Award}
                  color="border-yellow-500"
                />
              </div>
            </div>
          )}

          {/* Action Plan */}
          {analysis.llm_action_plan && (
            <div className="mt-8">
              <ActionPlan actionPlan={analysis.llm_action_plan} />
            </div>
          )}
        </div>
      )}
    </div>
  )
}
