import React, { useState } from 'react';
import { ChevronDown, ChevronUp, AlertCircle, CheckCircle, TrendingUp, Lightbulb } from 'lucide-react';

const LLMAnalysisSection = ({ category, analysis, title, icon: Icon, color }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  if (!analysis || Object.keys(analysis).length === 0) {
    return (
      <div className={`bg-white rounded-lg shadow p-6 border-l-4 ${color}`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            {Icon && <Icon className="w-6 h-6 text-gray-400" />}
            <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
          </div>
          <span className="text-sm text-gray-500">詳細分析が利用できません</span>
        </div>
        <p className="mt-2 text-sm text-gray-600">
          Anthropic API keyを設定すると、AIによる詳細な分析が利用可能になります。
        </p>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-lg shadow border-l-4 ${color}`}>
      {/* Header */}
      <div
        className="p-6 cursor-pointer hover:bg-gray-50 transition-colors"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            {Icon && <Icon className={`w-6 h-6 ${color.replace('border-', 'text-')}`} />}
            <div>
              <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
              {analysis.overall_assessment && (
                <p className="text-sm text-gray-600 mt-1">{analysis.overall_assessment}</p>
              )}
            </div>
          </div>
          {isExpanded ? (
            <ChevronUp className="w-5 h-5 text-gray-400" />
          ) : (
            <ChevronDown className="w-5 h-5 text-gray-400" />
          )}
        </div>
      </div>

      {/* Expanded Content */}
      {isExpanded && (
        <div className="px-6 pb-6 space-y-6 border-t border-gray-100">
          {/* Critical Issues */}
          {analysis.critical_issues && analysis.critical_issues.length > 0 && (
            <div className="mt-6">
              <h4 className="flex items-center text-md font-semibold text-red-700 mb-3">
                <AlertCircle className="w-5 h-5 mr-2" />
                重要な問題点
              </h4>
              <div className="space-y-3">
                {analysis.critical_issues.map((issue, idx) => (
                  <div key={idx} className="bg-red-50 rounded-lg p-4 border border-red-200">
                    <div className="flex items-start justify-between mb-2">
                      <h5 className="font-semibold text-red-900">{issue.issue}</h5>
                      <span className={`px-2 py-1 text-xs font-medium rounded ${
                        issue.impact === 'high' ? 'bg-red-200 text-red-800' :
                        issue.impact === 'medium' ? 'bg-yellow-200 text-yellow-800' :
                        'bg-blue-200 text-blue-800'
                      }`}>
                        影響度: {issue.impact === 'high' ? '高' : issue.impact === 'medium' ? '中' : '低'}
                      </span>
                    </div>
                    <p className="text-sm text-red-800 mb-2">{issue.explanation}</p>
                    <div className="bg-white rounded p-3 mt-2">
                      <p className="text-sm font-medium text-gray-700 mb-1">解決策:</p>
                      <p className="text-sm text-gray-600">{issue.solution}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Strengths */}
          {analysis.strengths && analysis.strengths.length > 0 && (
            <div>
              <h4 className="flex items-center text-md font-semibold text-green-700 mb-3">
                <CheckCircle className="w-5 h-5 mr-2" />
                優れている点
              </h4>
              <ul className="space-y-2">
                {analysis.strengths.map((strength, idx) => (
                  <li key={idx} className="flex items-start bg-green-50 rounded-lg p-3 border border-green-200">
                    <CheckCircle className="w-4 h-4 text-green-600 mr-2 mt-0.5 flex-shrink-0" />
                    <span className="text-sm text-green-900">{strength}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Improvements */}
          {analysis.improvements && analysis.improvements.length > 0 && (
            <div>
              <h4 className="flex items-center text-md font-semibold text-blue-700 mb-3">
                <TrendingUp className="w-5 h-5 mr-2" />
                改善提案
              </h4>
              <div className="space-y-4">
                {analysis.improvements.map((improvement, idx) => (
                  <div key={idx} className="bg-blue-50 rounded-lg p-4 border border-blue-200">
                    <div className="flex items-start justify-between mb-2">
                      <h5 className="font-semibold text-blue-900">{improvement.area}</h5>
                      <div className="flex gap-2">
                        <span className={`px-2 py-1 text-xs font-medium rounded ${
                          improvement.priority === 'high' ? 'bg-red-100 text-red-800' :
                          improvement.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          優先度: {improvement.priority === 'high' ? '高' : improvement.priority === 'medium' ? '中' : '低'}
                        </span>
                        <span className={`px-2 py-1 text-xs font-medium rounded ${
                          improvement.difficulty === 'easy' ? 'bg-green-100 text-green-800' :
                          improvement.difficulty === 'moderate' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-red-100 text-red-800'
                        }`}>
                          難易度: {improvement.difficulty === 'easy' ? '易' : improvement.difficulty === 'moderate' ? '中' : '難'}
                        </span>
                      </div>
                    </div>
                    <div className="space-y-2 text-sm">
                      <div>
                        <span className="font-medium text-blue-800">現状:</span>
                        <span className="text-blue-700 ml-2">{improvement.current_state}</span>
                      </div>
                      <div>
                        <span className="font-medium text-blue-800">推奨:</span>
                        <span className="text-blue-700 ml-2">{improvement.recommended_state}</span>
                      </div>
                      {improvement.implementation_steps && (
                        <div>
                          <span className="font-medium text-blue-800">実装手順:</span>
                          <ol className="list-decimal list-inside ml-2 mt-1 space-y-1">
                            {improvement.implementation_steps.map((step, stepIdx) => (
                              <li key={stepIdx} className="text-blue-700">{step}</li>
                            ))}
                          </ol>
                        </div>
                      )}
                      <div className="bg-white rounded p-2 mt-2">
                        <span className="font-medium text-gray-700">期待される効果:</span>
                        <span className="text-gray-600 ml-2">{improvement.expected_impact}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Professional Recommendations */}
          {analysis.professional_recommendations && analysis.professional_recommendations.length > 0 && (
            <div>
              <h4 className="flex items-center text-md font-semibold text-purple-700 mb-3">
                <Lightbulb className="w-5 h-5 mr-2" />
                プロからの推奨事項
              </h4>
              <ul className="space-y-2">
                {analysis.professional_recommendations.map((rec, idx) => (
                  <li key={idx} className="flex items-start bg-purple-50 rounded-lg p-3 border border-purple-200">
                    <Lightbulb className="w-4 h-4 text-purple-600 mr-2 mt-0.5 flex-shrink-0" />
                    <span className="text-sm text-purple-900">{rec}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Score Breakdown (if available) */}
          {analysis.technical_score_breakdown && (
            <div>
              <h4 className="text-md font-semibold text-gray-700 mb-3">詳細スコア</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {Object.entries(analysis.technical_score_breakdown).map(([key, value]) => (
                  <div key={key} className="bg-gray-50 rounded-lg p-3 border border-gray-200">
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-sm font-medium text-gray-700 capitalize">
                        {key.replace(/_/g, ' ')}
                      </span>
                      <span className={`text-lg font-bold ${
                        value.score >= 80 ? 'text-green-600' :
                        value.score >= 60 ? 'text-yellow-600' :
                        'text-red-600'
                      }`}>
                        {value.score}
                      </span>
                    </div>
                    <p className="text-xs text-gray-600">{value.note}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default LLMAnalysisSection;
