'use client';

import React, { useState, useEffect } from 'react';

export function PrescriptiveIntelligenceWorkspace() {
  const [activeTab, setActiveTab] = useState<'overview' | 'problems' | 'options' | 'recommendations' | 'robustness' | 'actions' | 'performance' | 'nl_query'>('overview');
  const [overviewData, setOverviewData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('How should we allocate this capacity?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/optimization');
      if (res.ok) {
        const data = await res.json();
        setOverviewData(data);
      } else {
        // Fallback seed data
        setOverviewData({
          problemsCount: 1,
          optionsCount: 2,
          recommendationsCount: 1,
          actionPlansCount: 1,
          paretoOptionsCount: 1,
          optimizationHealthScore: 0.96,
          problems: [
            {
              id: "prob_opt_01",
              name: "Q3 Enterprise AI Compute & Agent Allocation Optimization",
              description: "Optimize agent node placement and GPU compute allocation to maximize throughput while respecting strict budget and SLA constraints.",
              objective_type: "maximize_capacity_efficiency",
              status: "ready_for_review",
              owner: "usr_head_of_arch"
            }
          ],
          options: [
            {
              id: "opt_01",
              problem_id: "prob_opt_01",
              variables_json: { replica_pool_size: 48, gpu_tier: "A100_SXM" },
              constraints_satisfied: true,
              expected_outcome: 940.0,
              expected_cost: 42500.0,
              expected_risk: "low",
              confidence: 93.0
            },
            {
              id: "opt_02",
              problem_id: "prob_opt_01",
              variables_json: { replica_pool_size: 64, gpu_tier: "H100_SXM" },
              constraints_satisfied: true,
              expected_outcome: 1150.0,
              expected_cost: 49000.0,
              expected_risk: "medium",
              confidence: 89.0
            }
          ],
          recommendations: [
            {
              id: "rec_presc_01",
              problem_id: "prob_opt_01",
              recommended_option_id: "opt_01",
              objective_summary: "Maximize agent throughput while keeping compute cost under $50k/mo.",
              constraints_summary: "Hard budget cap $50k satisfied; Hard security DLP policy satisfied.",
              evidence: "Option 1 achieves 940 missions/hr at $42.5k/mo with highest robustness score (0.94).",
              expected_impact: "+28% throughput increase with $7.5k budget buffer.",
              risk_level: "low",
              confidence_pct: 93.0,
              robustness_score: 0.94,
              status: "ready_for_review"
            }
          ],
          actionPlans: [
            {
              id: "act_plan_01",
              recommendation_id: "rec_presc_01",
              actions_json: [
                { step: 1, action: "Provision 48 Agent Replicas", system: "Universal Action Gateway" },
                { step: 2, action: "Update Model Gateway Routing Weights", system: "Model Gateway" }
              ],
              owner: "usr_head_of_arch",
              rollback_plan: "Restore Previous Replica Weights (v1.8) via Universal Action Gateway within 60s.",
              execution_mode: "approval_gated"
            }
          ],
          robustness: [
            {
              id: "rob_01",
              option_id: "opt_01",
              demand_change: "+20% demand increase maintains SLA (<300ms)",
              cost_change: "+10% pricing surge absorbed within budget",
              capacity_change: "-15% node outage maintains 92% throughput",
              dependency_failure_impact: "Graceful fallback to secondary cluster",
              robustness_score: 0.94
            }
          ],
          performances: [
            {
              id: "opt_perf_01",
              recommendation_id: "rec_presc_01",
              expected_outcome: 940.0,
              actual_outcome: 952.0,
              expected_cost: 42500.0,
              actual_cost: 41800.0,
              benefit_accuracy: 98.7,
              cost_accuracy: 98.4,
              forecast_error: 1.4
            }
          ]
        });
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleQuery = async () => {
    if (!queryText.trim()) return;
    setQueryLoading(true);
    try {
      const res = await fetch(`/api/v1/optimization/query?query=${encodeURIComponent(queryText)}`, {
        method: 'POST'
      });
      if (res.ok) {
        const data = await res.json();
        setQueryResult(data);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setQueryLoading(false);
    }
  };

  return (
    <div className="p-6 space-y-6 bg-slate-950 text-slate-100 min-h-screen">
      {/* Header */}
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
            <span className="p-2 bg-indigo-600/20 text-indigo-400 rounded-lg text-lg">⚖️</span>
            Enterprise Prescriptive Intelligence & Decision Optimization 2.0
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Constraint-aware optimization engine, Pareto trade-off analysis, robustness simulation & human-governed action plans.
          </p>
        </div>
        <div className="flex gap-2">
          <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full text-xs font-semibold flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            Prescriptive Engine Active
          </span>
          <span className="px-3 py-1 bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 rounded-full text-xs font-semibold">
            Human Authority Gated
          </span>
        </div>
      </div>

      {/* Telemetry Bar */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Optimization Problems</div>
          <div className="text-2xl font-bold text-slate-100 mt-1">{overviewData?.problemsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Feasible Options</div>
          <div className="text-2xl font-bold text-indigo-400 mt-1">{overviewData?.optionsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Pareto Alternatives</div>
          <div className="text-2xl font-bold text-purple-400 mt-1">{overviewData?.paretoOptionsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Recommendations</div>
          <div className="text-2xl font-bold text-amber-400 mt-1">{overviewData?.recommendationsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Action Plans</div>
          <div className="text-2xl font-bold text-emerald-400 mt-1">{overviewData?.actionPlansCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Optimization Score</div>
          <div className="text-2xl font-bold text-cyan-400 mt-1">{((overviewData?.optimizationHealthScore || 0) * 100).toFixed(0)}%</div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 gap-2 text-sm overflow-x-auto pb-1">
        {[
          { id: 'overview', label: 'Prescriptive Overview' },
          { id: 'problems', label: 'Problems & Constraints' },
          { id: 'options', label: 'Feasible Options & Pareto' },
          { id: 'recommendations', label: 'Prescriptive Recommendations' },
          { id: 'robustness', label: 'Robustness & Sensitivity' },
          { id: 'actions', label: 'Action Plans & Rollback' },
          { id: 'performance', label: 'Optimization Performance' },
          { id: 'nl_query', label: 'Natural Language Query' }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-2 font-medium rounded-t-lg transition-colors whitespace-nowrap ${
              activeTab === tab.id
                ? 'bg-slate-900 text-indigo-400 border-b-2 border-indigo-500'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/40'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      {loading ? (
        <div className="p-8 text-center text-slate-500">Loading Prescriptive Intelligence state...</div>
      ) : (
        <div className="space-y-6">
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-indigo-400 flex items-center gap-2">
                  <span>🎯</span> Active Optimization Problem
                </h2>
                {overviewData?.problems?.[0] && (
                  <div className="space-y-3 text-sm">
                    <div className="font-medium text-slate-200">{overviewData.problems[0].name}</div>
                    <p className="text-slate-400">{overviewData.problems[0].description}</p>
                    <div className="grid grid-cols-2 gap-2 text-xs pt-2">
                      <span className="p-2 bg-slate-800/60 rounded">Objective: <strong className="text-indigo-300">{overviewData.problems[0].objective_type}</strong></span>
                      <span className="p-2 bg-slate-800/60 rounded">Owner: <strong className="text-slate-300">{overviewData.problems[0].owner}</strong></span>
                    </div>
                  </div>
                )}
              </div>

              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-emerald-400 flex items-center gap-2">
                  <span>✨</span> Top Advisory Recommendation
                </h2>
                {overviewData?.recommendations?.[0] && (
                  <div className="space-y-3 text-sm">
                    <div className="text-slate-300">{overviewData.recommendations[0].objective_summary}</div>
                    <div className="p-3 bg-emerald-950/30 border border-emerald-800/40 rounded-lg text-emerald-300 text-xs">
                      {overviewData.recommendations[0].expected_impact}
                    </div>
                    <div className="text-xs text-slate-400">
                      Confidence: <span className="text-slate-200 font-semibold">{overviewData.recommendations[0].confidence_pct}%</span> | Robustness: <span className="text-slate-200 font-semibold">{overviewData.recommendations[0].robustness_score}</span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'problems' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Configured Optimization Problems & Constraints</h2>
              <div className="divide-y divide-slate-800">
                {overviewData?.problems?.map((p: any) => (
                  <div key={p.id} className="py-4 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="font-semibold text-indigo-300">{p.name}</span>
                      <span className="px-2 py-1 bg-indigo-500/10 text-indigo-400 text-xs rounded">{p.status}</span>
                    </div>
                    <p className="text-sm text-slate-400">{p.description}</p>
                    <div className="text-xs text-slate-500">ID: {p.id} | Owner: {p.owner}</div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'options' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Feasible Options & Pareto Non-Dominated Alternatives</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {overviewData?.options?.map((op: any) => (
                  <div key={op.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2">
                    <div className="flex justify-between items-center text-sm">
                      <span className="font-semibold text-purple-300">Option {op.id}</span>
                      <span className="text-xs px-2 py-0.5 bg-emerald-500/10 text-emerald-400 rounded">Feasible</span>
                    </div>
                    <pre className="text-xs bg-slate-900 p-2 rounded text-slate-300">{JSON.stringify(op.variables_json, null, 2)}</pre>
                    <div className="grid grid-cols-2 gap-2 text-xs text-slate-400 pt-1">
                      <span>Outcome: <strong className="text-emerald-400">{op.expected_outcome} missions/hr</strong></span>
                      <span>Cost: <strong className="text-amber-400">${op.expected_cost.toLocaleString()}/mo</strong></span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'recommendations' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Prescriptive Advisory Recommendations</h2>
              {overviewData?.recommendations?.map((rec: any) => (
                <div key={rec.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-amber-300">Recommendation {rec.id}</span>
                    <span className="px-3 py-1 bg-indigo-500/20 text-indigo-300 rounded text-xs">{rec.status}</span>
                  </div>
                  <p className="text-sm text-slate-300">{rec.evidence}</p>
                  <div className="p-3 bg-slate-900 rounded text-xs text-slate-400 space-y-1">
                    <div><strong>Constraints Summary:</strong> {rec.constraints_summary}</div>
                    <div><strong>Expected Impact:</strong> {rec.expected_impact}</div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'robustness' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Robustness & Sensitivity Analysis</h2>
              {overviewData?.robustness?.map((rob: any) => (
                <div key={rob.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-cyan-300">Robustness Evaluation</span>
                    <span className="text-xs px-2 py-0.5 bg-cyan-500/10 text-cyan-400 rounded">Score: {rob.robustness_score}</span>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs text-slate-400 pt-1">
                    <span>Demand Shift: <strong className="text-slate-200">{rob.demand_change}</strong></span>
                    <span>Cost Shift: <strong className="text-slate-200">{rob.cost_change}</strong></span>
                    <span>Capacity Shift: <strong className="text-slate-200">{rob.capacity_change}</strong></span>
                    <span>Dependency Impact: <strong className="text-slate-200">{rob.dependency_failure_impact}</strong></span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'actions' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Approved Action Plans & Rollback Safety Controls</h2>
              {overviewData?.actionPlans?.map((ap: any) => (
                <div key={ap.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-emerald-400">Action Plan {ap.id}</span>
                    <span className="text-xs px-2 py-0.5 bg-amber-500/10 text-amber-400 rounded">{ap.execution_mode}</span>
                  </div>
                  <div className="space-y-1">
                    {ap.actions_json?.map((act: any, idx: number) => (
                      <div key={idx} className="text-xs text-slate-300 flex justify-between bg-slate-900 p-2 rounded">
                        <span>Step {act.step}: {act.action}</span>
                        <span className="text-indigo-400 font-mono">{act.system}</span>
                      </div>
                    ))}
                  </div>
                  <div className="p-3 bg-red-950/20 border border-red-900/30 rounded text-xs text-red-300">
                    <strong>Rollback Plan:</strong> {ap.rollback_plan}
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'performance' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Optimization Recommendation Performance & Learning</h2>
              {overviewData?.performances?.map((perf: any) => (
                <div key={perf.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-indigo-300">Performance Metric ID: {perf.id}</span>
                    <span className="text-xs text-emerald-400 font-bold">Benefit Accuracy: {perf.benefit_accuracy}%</span>
                  </div>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs text-slate-400 pt-1">
                    <span>Expected Outcome: <strong className="text-slate-200">{perf.expected_outcome}</strong></span>
                    <span>Actual Outcome: <strong className="text-emerald-400">{perf.actual_outcome}</strong></span>
                    <span>Expected Cost: <strong className="text-slate-200">${perf.expected_cost}</strong></span>
                    <span>Actual Cost: <strong className="text-emerald-400">${perf.actual_cost}</strong></span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'nl_query' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Natural Language Prescriptive Query Interface</h2>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={queryText}
                  onChange={(e) => setQueryText(e.target.value)}
                  placeholder="Ask a prescriptive optimization question..."
                  className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
                />
                <button
                  onClick={handleQuery}
                  disabled={queryLoading}
                  className="px-5 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-medium rounded-lg text-sm transition-colors"
                >
                  {queryLoading ? 'Optimizing...' : 'Evaluate'}
                </button>
              </div>

              {queryResult && (
                <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                  <div className="text-xs text-indigo-400 font-semibold">Query: {queryResult.query}</div>
                  <div className="space-y-2">
                    {queryResult.results?.map((res: any, idx: number) => (
                      <div key={idx} className="p-3 bg-slate-900 rounded space-y-1 text-xs">
                        <div className="font-semibold text-slate-200">{res.recommendation}</div>
                        <div className="text-emerald-400">Throughput: {res.expected_throughput} | Cost: {res.expected_cost}</div>
                        <div className="text-slate-400">Robustness: {res.robustness_score} | Reversibility: {res.reversibility}</div>
                      </div>
                    ))}
                  </div>
                  {queryResult.evidenceJson?.error && (
                    <div className="p-3 bg-red-950/40 border border-red-800/40 text-red-300 text-xs rounded">
                      {queryResult.evidenceJson.error}
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
