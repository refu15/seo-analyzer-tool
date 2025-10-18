import { useEffect, useState } from 'react'
import { Loader2, CheckCircle, XCircle, AlertCircle } from 'lucide-react'
import { analysisApi } from '../services/api'

export default function AnalysisProgress({ siteId, onComplete, onError }) {
  const [progress, setProgress] = useState(null)
  const [polling, setPolling] = useState(true)

  useEffect(() => {
    if (!polling) return

    const pollProgress = async () => {
      try {
        const response = await analysisApi.getProgress(siteId)
        const progressData = response.data
        setProgress(progressData)

        // Stop polling if analysis is complete or failed
        if (progressData.status === 'completed') {
          setPolling(false)
          if (onComplete) {
            onComplete(progressData.analysis_id)
          }
        } else if (progressData.status === 'failed') {
          setPolling(false)
          if (onError) {
            onError(progressData.error_message)
          }
        }
      } catch (err) {
        console.error('Progress poll error:', err)
        console.error('Error details:', err.response?.data)

        // If we get a 404, it means no progress record exists yet
        // Continue polling for a bit
        if (err.response?.status === 404) {
          console.log('No progress record found yet, will continue polling...')
        } else {
          // For other errors, stop polling after 10 attempts
          console.error('Unexpected error polling progress')
        }
      }
    }

    // Poll immediately
    pollProgress()

    // Set up interval for polling (every 1 second)
    const interval = setInterval(pollProgress, 1000)

    return () => clearInterval(interval)
  }, [siteId, polling, onComplete, onError])

  if (!progress) {
    return (
      <div className="flex items-center justify-center py-8">
        <Loader2 className="h-8 w-8 text-primary-600 animate-spin" />
        <span className="ml-3 text-gray-700">分析を準備中...</span>
      </div>
    )
  }

  const getStatusIcon = () => {
    switch (progress.status) {
      case 'completed':
        return <CheckCircle className="h-8 w-8 text-green-600" />
      case 'failed':
        return <XCircle className="h-8 w-8 text-red-600" />
      case 'running':
      case 'pending':
        return <Loader2 className="h-8 w-8 text-primary-600 animate-spin" />
      default:
        return <AlertCircle className="h-8 w-8 text-gray-400" />
    }
  }

  const getStatusText = () => {
    switch (progress.status) {
      case 'completed':
        return '分析完了'
      case 'failed':
        return '分析失敗'
      case 'running':
        return '分析中'
      case 'pending':
        return '待機中'
      default:
        return '不明'
    }
  }

  const getStatusColor = () => {
    switch (progress.status) {
      case 'completed':
        return 'bg-green-50 border-green-200'
      case 'failed':
        return 'bg-red-50 border-red-200'
      case 'running':
      case 'pending':
        return 'bg-blue-50 border-blue-200'
      default:
        return 'bg-gray-50 border-gray-200'
    }
  }

  return (
    <div className={`border rounded-lg p-6 ${getStatusColor()}`}>
      <div className="flex items-center mb-4">
        {getStatusIcon()}
        <div className="ml-3">
          <h3 className="text-lg font-semibold text-gray-900">{getStatusText()}</h3>
          {progress.current_step && (
            <p className="text-sm text-gray-600 mt-1">{progress.current_step}</p>
          )}
        </div>
      </div>

      {/* Progress Bar */}
      {progress.status !== 'failed' && (
        <div className="mt-4">
          <div className="flex justify-between text-sm text-gray-600 mb-2">
            <span>進捗状況</span>
            <span>{progress.progress_percentage}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2.5">
            <div
              className={`h-2.5 rounded-full transition-all duration-300 ${
                progress.status === 'completed' ? 'bg-green-600' : 'bg-primary-600'
              }`}
              style={{ width: `${progress.progress_percentage}%` }}
            ></div>
          </div>
        </div>
      )}

      {/* Error Message */}
      {progress.status === 'failed' && progress.error_message && (
        <div className="mt-4 p-4 bg-red-100 border border-red-300 rounded-md">
          <p className="text-sm text-red-800">
            <strong>エラー:</strong> {progress.error_message}
          </p>
        </div>
      )}

      {/* Completion Message */}
      {progress.status === 'completed' && (
        <div className="mt-4 p-4 bg-green-100 border border-green-300 rounded-md">
          <p className="text-sm text-green-800">
            SEO分析が正常に完了しました。結果を確認してください。
          </p>
        </div>
      )}
    </div>
  )
}
