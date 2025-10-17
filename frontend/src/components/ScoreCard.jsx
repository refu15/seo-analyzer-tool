import React from 'react'

export default function ScoreCard({ title, score, maxScore = 100, color = 'blue' }) {
  const percentage = (score / maxScore) * 100

  const getColorClasses = () => {
    if (percentage >= 80) return 'text-green-600 bg-green-100'
    if (percentage >= 60) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  const getProgressColor = () => {
    if (percentage >= 80) return 'bg-green-500'
    if (percentage >= 60) return 'bg-yellow-500'
    return 'bg-red-500'
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-sm font-medium text-gray-500 mb-2">{title}</h3>
      <div className={`inline-flex items-center justify-center w-16 h-16 rounded-full ${getColorClasses()} mb-3`}>
        <span className="text-2xl font-bold">{score}</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2.5">
        <div
          className={`h-2.5 rounded-full transition-all duration-500 ${getProgressColor()}`}
          style={{ width: `${percentage}%` }}
        ></div>
      </div>
      <p className="mt-2 text-xs text-gray-500">{percentage.toFixed(0)}%</p>
    </div>
  )
}
