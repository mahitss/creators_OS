'use client';

import React, { useState, useEffect } from 'react';

export function AdaptiveStrategyWorkspace() {
  const [activeTab, setActiveTab] = useState<'overview' | 'theses' | 'health' | 'reconfigurations' | 'bottlenecks' | 'experiments' | 'nl_query'>('overview');
  const [overviewData, setOverviewData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('Is our current strategy still working?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);
  const [approvalMessage, setApprovalMessage] = useState<string | null>(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/strategy/adaptive');
      if (res.ok) {
        const data = await res.json();
        setOverviewData(data);
      } else {
        // Fallback seed data
        setOverviewData({
          strategiesCount: 1,
          thesesCount: 1,
          indicatorsCount: 1,
          driftsCount: 1,
          proposedReconfigurationsCount: 1,
          bottlenecksCount: 1,
          runningExperimentsCount: 1,
          healthDimensions: {
            intentAlignment: 0.94,
            assumptionValidity: 0.82,
            performance: 0.91,
            scenarioRobustness: 0.89,
            riskControl: 0.95,
            executionProgress: 0.88,
            capabilityReadiness: 0.90
          },
          strategies: [
            {
              id: "astrat_01",
              name: "Enterprise Autonomous Agent Mesh & Cognitive Work Scaling Strategy",
              description: "3-Year adaptive enterprise strategy scaling agent-driven workflow execution.",
              strategic_intent: "Transition 60% of routine cross-department workflows to autonomous AI agent DAGs.",
              horizon: "3_year",
              status: "active",
              owner: "usr_chief_strategy_officer"
            }
          ],
          theses: [
            {
              id: "sthes_01",
              belief: "Autonomous agent mesh adoption will yield 4.5x productivity acceleration.",
              expected_outcome: "60% workflow automation by 2028",
              confidence: "high",
              status: "supported"
            }
          ],
          indicators: [
            {
              id: "sind_adp_01",
              metric: "Agent DAG Workflow Execution Share (%)",
              baseline: 15.0,
              target: 60.0,
              current: 42.8,
              direction: "increasing"
            }
          ],
          drifts: [
            {
              id: "sdrift_01",
              drift_type: "assumption_fragility_drift",
              severity: "medium",
              affected_strategy: "Inference budget allocation for 2027"
            }
          ],
          reconfigurations: [
            {
              id: "prconf_01",
              reconfiguration_type: "investment_shift",
              reason: "Mitigate GPU unit cost inflation by shifting 35% load to hybrid edge clusters.",
              expected_effect: "18% reduction in annual inference operational expenditure",
              status: "proposed"
            }
          ],
          bottlenecks: [
            {
              id: "sbot_01",
              bottleneck_type: "capacity",
              description: "GPU inference throughput saturation during peak morning executive brief generation",
              severity: "high",
              recommended_mitigation: "Deploy ActionGateway async batch queuing & regional model fallback routing"
            }
          ],
          experiments: [
            {
              id: "sexp_01",
              hypothesis: "Sub-8B local model quantization retains 98% task completion accuracy while reducing GPU memory 4x.",
              cost: 8500.0,
              status: "running"
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

  const handleApproveReconfiguration = async (reconfigId: string) => {
    try {
      const res = await fetch(`/api/v1/strategy/adaptive/reconfigurations/${reconfigId}/approve`, {
        method: 'POST'
      });
      if (res.ok) {
        const data = await res.json();
        setApprovalMessage(data.message);
        fetchData();
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleQuery = async () => {
    if (!queryText.trim()) return;
    setQueryLoading(true);
    try {
      const res = await fetch(`/api/v1/strategy/adaptive/query?query=${encodeURIComponent(queryText)}`, {
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
            <span className="p-2 bg-blue-600/20 text-blue-400 rounded-lg text-lg">⚡</span>
            Enterprise Adaptive Strategy & Dynamic Portfolio Reconfiguration 2.0
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Human-governed strategy adaptation connecting Intent → Theses → Assumptions → Live Indicators → Drift Signals → Portfolio Reconfiguration Proposals → Leadership Approval.
          </p>
        </div>
        <div className="flex gap-2">
          <span className="px-3 py-1 bg-blue-500/10 text-blue-400 border border-blue-500/20 rounded-full text-xs font-semibold">
            Dynamic Strategy Mode
          </span>
          <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full text-xs font-semibold">
            Human Approval Required
          </span>
        </div>
      </div>

      {/* Telemetry Bar */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Active Strategies</div>
          <div className="text-2xl font-bold text-slate-100 mt-1">{overviewData?.strategiesCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Strategic Theses</div>
          <div className="text-2xl font-bold text-blue-400 mt-1">{overviewData?.thesesCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Drift Signals</div>
          <div className="text-2xl font-bold text-amber-400 mt-1">{overviewData?.driftsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Pending Proposals</div>
          <div className="text-2xl font-bold text-purple-400 mt-1">{overviewData?.proposedReconfigurationsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Active Bottlenecks</div>
          <div className="text-2xl font-bold text-rose-400 mt-1">{overviewData?.bottlenecksCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Running Experiments</div>
          <div className="text-2xl font-bold text-emerald-400 mt-1">{overviewData?.runningExperimentsCount || 0}</div>
        </div>
      </div>

      {/* Approval Notification Banner */}
      {approvalMessage && (
        <div className="p-4 bg-emerald-950/50 border border-emerald-800/60 rounded-xl text-emerald-300 text-sm flex justify-between items-center">
          <span>✅ {approvalMessage}</span>
          <button onClick={() => setApprovalMessage(null)} className="text-xs text-slate-400 hover:text-white">Dismiss</button>
        </div>
      )}

      {/* Tabs */}
      <div className="flex border-b border-slate-800 gap-2 text-sm overflow-x-auto pb-1">
        {[
          { id: 'overview', label: 'Adaptive Overview' },
          { id: 'theses', label: 'Strategic Theses & Intent' },
          { id: 'health', label: 'Multi-Dimensional Health' },
          { id: 'reconfigurations', label: 'Portfolio Reconfigurations' },
          { id: 'bottlenecks', label: 'Bottlenecks & Capability Gaps' },
          { id: 'experiments', label: 'Strategic Experiments' },
          { id: 'nl_query', label: 'Natural Language Query' }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-2 font-medium rounded-t-lg transition-colors whitespace-nowrap ${
              activeTab === tab.id
                ? 'bg-slate-900 text-blue-400 border-b-2 border-blue-500'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/40'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      {loading ? (
        <div className="p-8 text-center text-slate-500">Loading Adaptive Strategy state...</div>
      ) : (
        <div className="space-y-6">
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-blue-400 flex items-center gap-2">
                  <span>🎯</span> Strategic Intent & Active Plan
                </h2>
                {overviewData?.strategies?.[0] && (
                  <div className="space-y-3 text-sm">
                    <div className="font-bold text-slate-100 text-base">{overviewData.strategies[0].name}</div>
                    <div className="p-3 bg-slate-950 rounded border border-blue-800/40 text-blue-300">
                      <strong>Intent:</strong> {overviewData.strategies[0].strategic_intent}
                    </div>
                    <div className="grid grid-cols-2 gap-2 text-xs text-slate-400">
                      <span>Horizon: {overviewData.strategies[0].horizon}</span>
                      <span>Owner: {overviewData.strategies[0].owner}</span>
                    </div>
                  </div>
                )}
              </div>

              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-amber-400 flex items-center gap-2">
                  <span>📡</span> Strategy Drift Signal
                </h2>
                {overviewData?.drifts?.[0] && (
                  <div className="space-y-3 text-sm">
                    <div className="font-bold text-slate-100">{overviewData.drifts[0].drift_type}</div>
                    <div className="p-3 bg-slate-950 rounded border border-amber-800/40 text-amber-300 text-xs">
                      {overviewData.drifts[0].affected_strategy}
                    </div>
                    <span className="inline-block px-2 py-0.5 bg-amber-500/20 text-amber-300 rounded text-xs font-bold">
                      Severity: {overviewData.drifts[0].severity}
                    </span>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'theses' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Strategic Theses & Belief Statements</h2>
              {overviewData?.theses?.map((th: any) => (
                <div key={th.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-blue-300">Belief: {th.belief}</span>
                    <span className="text-xs px-2 py-0.5 bg-emerald-500/20 text-emerald-400 rounded font-bold">Status: {th.status}</span>
                  </div>
                  <div className="text-xs text-slate-400">Expected Outcome: {th.expected_outcome}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'health' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Multi-Dimensional Strategy Health Breakdown</h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg">
                  <div className="text-xs text-slate-400">Intent Alignment</div>
                  <div className="text-xl font-bold text-blue-400 mt-1">{((overviewData?.healthDimensions?.intentAlignment || 0) * 100).toFixed(0)}%</div>
                </div>
                <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg">
                  <div className="text-xs text-slate-400">Assumption Validity</div>
                  <div className="text-xl font-bold text-amber-400 mt-1">{((overviewData?.healthDimensions?.assumptionValidity || 0) * 100).toFixed(0)}%</div>
                </div>
                <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg">
                  <div className="text-xs text-slate-400">Performance Index</div>
                  <div className="text-xl font-bold text-emerald-400 mt-1">{((overviewData?.healthDimensions?.performance || 0) * 100).toFixed(0)}%</div>
                </div>
                <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg">
                  <div className="text-xs text-slate-400">Scenario Robustness</div>
                  <div className="text-xl font-bold text-purple-400 mt-1">{((overviewData?.healthDimensions?.scenarioRobustness || 0) * 100).toFixed(0)}%</div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'reconfigurations' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Portfolio Reconfiguration Proposals (Human Authorization Required)</h2>
              {overviewData?.reconfigurations?.map((rc: any) => (
                <div key={rc.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-purple-300">Type: {rc.reconfiguration_type}</span>
                    <span className={`text-xs px-2 py-0.5 rounded font-bold ${
                      rc.status === 'approved' ? 'bg-emerald-500/20 text-emerald-300' : 'bg-purple-500/20 text-purple-300'
                    }`}>
                      {rc.status}
                    </span>
                  </div>
                  <p className="text-xs text-slate-300">Reason: {rc.reason}</p>
                  <div className="text-xs text-emerald-400">Expected Effect: {rc.expected_effect}</div>

                  {rc.status === 'proposed' && (
                    <button
                      onClick={() => handleApproveReconfiguration(rc.id)}
                      className="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold rounded transition-colors"
                    >
                      Authorize & Approve Reconfiguration
                    </button>
                  )}
                </div>
              ))}
            </div>
          )}

          {activeTab === 'bottlenecks' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Strategic Bottlenecks & Capacity Constraints</h2>
              {overviewData?.bottlenecks?.map((bt: any) => (
                <div key={bt.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-rose-500">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-rose-300">Bottleneck: {bt.description}</span>
                    <span className="text-xs px-2 py-0.5 bg-rose-500/20 text-rose-300 rounded font-bold">Severity: {bt.severity}</span>
                  </div>
                  <div className="text-xs text-slate-400">Mitigation: {bt.recommended_mitigation}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'experiments' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Strategic Experiments & Hypothesis Learning</h2>
              {overviewData?.experiments?.map((ex: any) => (
                <div key={ex.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-emerald-300">Hypothesis: {ex.hypothesis}</span>
                    <span className="text-xs px-2 py-0.5 bg-emerald-500/20 text-emerald-300 rounded font-bold">Cost: ${ex.cost.toLocaleString()}</span>
                  </div>
                  <div className="text-xs text-slate-400">Status: {ex.status}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'nl_query' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Natural Language Adaptive Strategy Query Interface</h2>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={queryText}
                  onChange={(e) => setQueryText(e.target.value)}
                  placeholder="Ask an adaptive strategy query..."
                  className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-sm text-slate-100 focus:outline-none focus:border-blue-500"
                />
                <button
                  onClick={handleQuery}
                  disabled={queryLoading}
                  className="px-5 py-2 bg-blue-600 hover:bg-blue-500 text-white font-medium rounded-lg text-sm transition-colors"
                >
                  {queryLoading ? 'Evaluating...' : 'Query'}
                </button>
              </div>

              {queryResult && (
                <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                  <div className="text-xs text-blue-400 font-semibold">Query: {queryResult.query}</div>
                  <div className="space-y-2">
                    {queryResult.results?.map((res: any, idx: number) => (
                      <div key={idx} className="p-3 bg-slate-900 rounded space-y-1 text-xs">
                        <div className="font-semibold text-slate-200">{res.strategy_name} ({res.status})</div>
                        <div className="text-amber-400">Drift Signal: {res.drift_signal}</div>
                        <div className="text-purple-300">Proposed Reconfiguration: {res.proposed_reconfiguration}</div>
                        <div className="text-emerald-400">Approval: {res.approval_status}</div>
                        <div className="text-cyan-300">Experiment: {res.running_experiment}</div>
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
