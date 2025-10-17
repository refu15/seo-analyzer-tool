import React, { useState } from 'react';
import { Calendar, Target, TrendingUp, Zap, Clock, BarChart } from 'lucide-react';

const ActionPlan = ({ actionPlan }) => {
  const [activeTab, setActiveTab] = useState('priority');

  if (!actionPlan || Object.keys(actionPlan).length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">アクションプラン</h3>
        <p className="text-sm text-gray-600">
          Anthropic API keyを設定すると、AIによる包括的なアクションプランが利用可能になります。
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow">
      {/* Header */}
      <div className="p-6 border-b border-gray-200">
        <h2 className="text-2xl font-bold text-gray-900 mb-2 flex items-center">
          <Target className="w-6 h-6 mr-2 text-blue-600" />
          90日間アクションプラン
        </h2>
        {actionPlan.executive_summary && (
          <p className="text-gray-700 leading-relaxed">{actionPlan.executive_summary}</p>
        )}
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="flex space-x-4 px-6">
          <button
            onClick={() => setActiveTab('priority')}
            className={`py-4 px-3 font-medium text-sm border-b-2 transition-colors ${
              activeTab === 'priority'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <span className="flex items-center">
              <TrendingUp className="w-4 h-4 mr-2" />
              優先アクション
            </span>
          </button>
          <button
            onClick={() => setActiveTab('timeline')}
            className={`py-4 px-3 font-medium text-sm border-b-2 transition-colors ${
              activeTab === 'timeline'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <span className="flex items-center">
              <Calendar className="w-4 h-4 mr-2" />
              タイムライン
            </span>
          </button>
          <button
            onClick={() => setActiveTab('quick-wins')}
            className={`py-4 px-3 font-medium text-sm border-b-2 transition-colors ${
              activeTab === 'quick-wins'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <span className="flex items-center">
              <Zap className="w-4 h-4 mr-2" />
              クイックウィン
            </span>
          </button>
        </nav>
      </div>

      {/* Content */}
      <div className="p-6">
        {/* Priority Actions Tab */}
        {activeTab === 'priority' && (
          <div className="space-y-4">
            {actionPlan.priority_actions && actionPlan.priority_actions.length > 0 ? (
              actionPlan.priority_actions.map((action, idx) => (
                <div
                  key={idx}
                  className={`border rounded-lg p-5 ${
                    action.priority === 'critical' ? 'border-red-300 bg-red-50' :
                    action.priority === 'high' ? 'border-orange-300 bg-orange-50' :
                    action.priority === 'medium' ? 'border-yellow-300 bg-yellow-50' :
                    'border-gray-300 bg-gray-50'
                  }`}
                >
                  <div className="flex items-start justify-between mb-3">
                    <h4 className="text-lg font-semibold text-gray-900">{action.title}</h4>
                    <div className="flex gap-2">
                      <span className={`px-3 py-1 text-xs font-semibold rounded-full ${
                        action.priority === 'critical' ? 'bg-red-200 text-red-800' :
                        action.priority === 'high' ? 'bg-orange-200 text-orange-800' :
                        action.priority === 'medium' ? 'bg-yellow-200 text-yellow-800' :
                        'bg-gray-200 text-gray-800'
                      }`}>
                        {action.priority === 'critical' ? '最優先' :
                         action.priority === 'high' ? '高' :
                         action.priority === 'medium' ? '中' : '低'}
                      </span>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-4">
                    <div className="flex items-center text-sm">
                      <BarChart className="w-4 h-4 mr-2 text-blue-600" />
                      <span className="text-gray-600">カテゴリー:</span>
                      <span className="ml-1 font-medium text-gray-900">{action.category}</span>
                    </div>
                    <div className="flex items-center text-sm">
                      <Target className="w-4 h-4 mr-2 text-green-600" />
                      <span className="text-gray-600">影響度:</span>
                      <span className="ml-1 font-medium text-gray-900">{action.expected_impact}/10</span>
                    </div>
                    <div className="flex items-center text-sm">
                      <Clock className="w-4 h-4 mr-2 text-purple-600" />
                      <span className="text-gray-600">期間:</span>
                      <span className="ml-1 font-medium text-gray-900">{action.timeline}</span>
                    </div>
                  </div>

                  {action.steps && action.steps.length > 0 && (
                    <div className="mb-4">
                      <h5 className="text-sm font-semibold text-gray-700 mb-2">実装ステップ:</h5>
                      <ol className="list-decimal list-inside space-y-1">
                        {action.steps.map((step, stepIdx) => (
                          <li key={stepIdx} className="text-sm text-gray-700 ml-2">{step}</li>
                        ))}
                      </ol>
                    </div>
                  )}

                  {action.required_resources && action.required_resources.length > 0 && (
                    <div className="mb-4">
                      <h5 className="text-sm font-semibold text-gray-700 mb-2">必要なリソース:</h5>
                      <ul className="flex flex-wrap gap-2">
                        {action.required_resources.map((resource, resIdx) => (
                          <li key={resIdx} className="text-xs bg-white px-3 py-1 rounded-full border border-gray-300">
                            {resource}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {action.kpis && action.kpis.length > 0 && (
                    <div>
                      <h5 className="text-sm font-semibold text-gray-700 mb-2">KPI:</h5>
                      <ul className="space-y-1">
                        {action.kpis.map((kpi, kpiIdx) => (
                          <li key={kpiIdx} className="text-sm text-gray-600 flex items-center">
                            <span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
                            {kpi}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ))
            ) : (
              <p className="text-gray-600">優先アクションが見つかりませんでした。</p>
            )}
          </div>
        )}

        {/* Timeline Tab */}
        {activeTab === 'timeline' && (
          <div className="space-y-6">
            {/* 30-Day Plan */}
            {actionPlan['30_day_plan'] && (
              <div className="border border-green-200 rounded-lg p-5 bg-green-50">
                <h3 className="text-lg font-bold text-green-900 mb-3 flex items-center">
                  <Calendar className="w-5 h-5 mr-2" />
                  30日プラン
                </h3>
                {actionPlan['30_day_plan'].focus_areas && (
                  <div className="mb-3">
                    <h4 className="text-sm font-semibold text-green-800 mb-2">注力領域:</h4>
                    <ul className="space-y-1">
                      {actionPlan['30_day_plan'].focus_areas.map((area, idx) => (
                        <li key={idx} className="text-sm text-green-900 flex items-center">
                          <span className="w-2 h-2 bg-green-600 rounded-full mr-2"></span>
                          {area}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                {actionPlan['30_day_plan'].expected_score_improvement && (
                  <div className="mb-3">
                    <h4 className="text-sm font-semibold text-green-800 mb-1">期待されるスコア改善:</h4>
                    <p className="text-sm text-green-900">{actionPlan['30_day_plan'].expected_score_improvement}</p>
                  </div>
                )}
                {actionPlan['30_day_plan'].key_deliverables && (
                  <div>
                    <h4 className="text-sm font-semibold text-green-800 mb-2">主要成果物:</h4>
                    <ul className="space-y-1">
                      {actionPlan['30_day_plan'].key_deliverables.map((deliverable, idx) => (
                        <li key={idx} className="text-sm text-green-900 flex items-center">
                          <span className="w-2 h-2 bg-green-600 rounded-full mr-2"></span>
                          {deliverable}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}

            {/* 60-Day Plan */}
            {actionPlan['60_day_plan'] && (
              <div className="border border-blue-200 rounded-lg p-5 bg-blue-50">
                <h3 className="text-lg font-bold text-blue-900 mb-3 flex items-center">
                  <Calendar className="w-5 h-5 mr-2" />
                  60日プラン
                </h3>
                {actionPlan['60_day_plan'].focus_areas && (
                  <div className="mb-3">
                    <h4 className="text-sm font-semibold text-blue-800 mb-2">注力領域:</h4>
                    <ul className="space-y-1">
                      {actionPlan['60_day_plan'].focus_areas.map((area, idx) => (
                        <li key={idx} className="text-sm text-blue-900 flex items-center">
                          <span className="w-2 h-2 bg-blue-600 rounded-full mr-2"></span>
                          {area}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                {actionPlan['60_day_plan'].expected_score_improvement && (
                  <div className="mb-3">
                    <h4 className="text-sm font-semibold text-blue-800 mb-1">期待されるスコア改善:</h4>
                    <p className="text-sm text-blue-900">{actionPlan['60_day_plan'].expected_score_improvement}</p>
                  </div>
                )}
                {actionPlan['60_day_plan'].key_deliverables && (
                  <div>
                    <h4 className="text-sm font-semibold text-blue-800 mb-2">主要成果物:</h4>
                    <ul className="space-y-1">
                      {actionPlan['60_day_plan'].key_deliverables.map((deliverable, idx) => (
                        <li key={idx} className="text-sm text-blue-900 flex items-center">
                          <span className="w-2 h-2 bg-blue-600 rounded-full mr-2"></span>
                          {deliverable}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}

            {/* 90-Day Plan */}
            {actionPlan['90_day_plan'] && (
              <div className="border border-purple-200 rounded-lg p-5 bg-purple-50">
                <h3 className="text-lg font-bold text-purple-900 mb-3 flex items-center">
                  <Calendar className="w-5 h-5 mr-2" />
                  90日プラン
                </h3>
                {actionPlan['90_day_plan'].focus_areas && (
                  <div className="mb-3">
                    <h4 className="text-sm font-semibold text-purple-800 mb-2">注力領域:</h4>
                    <ul className="space-y-1">
                      {actionPlan['90_day_plan'].focus_areas.map((area, idx) => (
                        <li key={idx} className="text-sm text-purple-900 flex items-center">
                          <span className="w-2 h-2 bg-purple-600 rounded-full mr-2"></span>
                          {area}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                {actionPlan['90_day_plan'].expected_score_improvement && (
                  <div className="mb-3">
                    <h4 className="text-sm font-semibold text-purple-800 mb-1">期待されるスコア改善:</h4>
                    <p className="text-sm text-purple-900">{actionPlan['90_day_plan'].expected_score_improvement}</p>
                  </div>
                )}
                {actionPlan['90_day_plan'].key_deliverables && (
                  <div>
                    <h4 className="text-sm font-semibold text-purple-800 mb-2">主要成果物:</h4>
                    <ul className="space-y-1">
                      {actionPlan['90_day_plan'].key_deliverables.map((deliverable, idx) => (
                        <li key={idx} className="text-sm text-purple-900 flex items-center">
                          <span className="w-2 h-2 bg-purple-600 rounded-full mr-2"></span>
                          {deliverable}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}

            {/* Long-term Strategy */}
            {actionPlan.long_term_strategy && (
              <div className="border border-gray-300 rounded-lg p-5 bg-gray-50">
                <h3 className="text-lg font-bold text-gray-900 mb-2">長期戦略</h3>
                <p className="text-sm text-gray-700 leading-relaxed">{actionPlan.long_term_strategy}</p>
              </div>
            )}
          </div>
        )}

        {/* Quick Wins Tab */}
        {activeTab === 'quick-wins' && (
          <div className="space-y-3">
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-4">
              <p className="text-sm text-yellow-800">
                <Zap className="w-4 h-4 inline mr-1" />
                これらのアクションは即座に実装でき、すぐに効果が期待できます。
              </p>
            </div>
            {actionPlan.quick_wins && actionPlan.quick_wins.length > 0 ? (
              actionPlan.quick_wins.map((win, idx) => (
                <div key={idx} className="flex items-start bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                  <Zap className="w-5 h-5 text-yellow-500 mr-3 mt-0.5 flex-shrink-0" />
                  <p className="text-sm text-gray-700">{win}</p>
                </div>
              ))
            ) : (
              <p className="text-gray-600">クイックウィンが見つかりませんでした。</p>
            )}

            {/* Monitoring Recommendations */}
            {actionPlan.monitoring_recommendations && actionPlan.monitoring_recommendations.length > 0 && (
              <div className="mt-6 border-t border-gray-200 pt-6">
                <h4 className="text-md font-semibold text-gray-900 mb-3">継続的モニタリング推奨</h4>
                <ul className="space-y-2">
                  {actionPlan.monitoring_recommendations.map((rec, idx) => (
                    <li key={idx} className="flex items-start bg-blue-50 border border-blue-200 rounded-lg p-3">
                      <BarChart className="w-4 h-4 text-blue-600 mr-2 mt-0.5 flex-shrink-0" />
                      <span className="text-sm text-blue-900">{rec}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ActionPlan;
