'use client';

import React, { useState, useEffect } from 'react';

export function ExecutionIntelligenceWorkspace() {
  const [activeTab, setActiveTab] = useState<'overview' | 'objectives' | 'coverage' | 'drift' | 'blockers' | 'decision_gaps' | 'outcomes' | 'recommendations' | 'nl_query'>('overview');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('Are we executing our strategy?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);
  const [approvalMsg, setApprovalMsg] = useState<string | null>(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/execution-intelligence');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      } else {
        // Fallback seed structure
        setData({
          objectivesCount: 1,
          alignmentsCount: 1,
          coveragesCount: 1,
          pathsCount: 1,
          driftsCount: 1,
          activeBlockersCount: 1,
          staleDecisionGapsCount: 1,
          outcomeGapsCount: 1,
          proposedRecommendationsCount: 1,
          executionVelocityIndex: 0.91,
          overallExecutionCoveragePct: 0.88,
          objectives: [
            {
              id: 'eobj_01',
              name: 'Objective 1: Deploy Autonomous Multi-Region Agent Mesh across 40 Workspaces',
              description: 'Establish continuous agent DAG execution under central PolicyEngine governance.',
              target_outcome: '60% workflow automation with sub-500ms execution latency',
              priority: 'p1',
              owner: 'usr_chief_technology_officer',
              status: 'active'
            }
          ],
          alignments: [
            {
              id: 'align_01',
              objective_id: 'eobj_01',
              portfolio_id: 'port_core_01',
              initiative_id: 'init_agent_mesh_v2',
              mission_id: 'msn_dag_orchestration_01',
              alignment_status: 'aligned',
              evidence_json: { kpi_contribution: 0.88, strategic_intent_match: 'high' }
            }
          ],
          coverages: [
            {
              id: 'ecov_01',
              objective_id: 'eobj_01',
              portfolio_coverage_pct: 0.95,
              initiative_coverage_pct: 0.90,
              mission_coverage_pct: 0.88,
              execution_coverage_pct: 0.85,
              benefit_coverage_pct: 0.82,
              has_gap: false
            }
          ],
          paths: [
            {
              id: 'epath_01',
              strategy_id: 'astrat_01',
              objective_id: 'eobj_01',
              initiative_id: 'init_agent_mesh_v2',
              mission_id: 'msn_dag_orchestration_01',
              action_id: 'act_mesh_policy_enforcement',
              deliverable_id: 'deliv_agent_mesh_kernel',
              outcome_id: 'out_60pct_automation',
              benefit_id: 'ben_4x_productivity_boost',
              path_integrity_status: 'intact'
            }
          ],
          drifts: [
            {
              id: 'edrift_01',
              drift_type: 'schedule',
              severity: 'medium',
              evidence_json: { milestone_delay: 'Phase 2 Edge Node deployment delayed by 8 days' }
            }
          ],
          blockers: [
            {
              id: 'eblock_01',
              blocked_initiative_id: 'init_agent_mesh_v2',
              dependency_id: 'dep_transatlantic_network_peering',
              owner: 'usr_infrastructure_lead',
              duration_days: 6,
              impact_summary: 'Delaying regional edge synchronization across European workspaces',
              severity: 'high',
              status: 'active'
            }
          ],
          decisionGaps: [
            {
              id: 'dgap_01',
              decision_id: 'dec_multi_cloud_router_01',
              approval_id: 'appr_multi_cloud_router_01',
              delay_days: 14,
              is_stale: true
            }
          ],
          outcomeGaps: [
            {
              id: 'ogap_01',
              execution_id: 'exec_agent_mesh_v1',
              expected_outcome: '10x reduction in manual workflow creation latency',
              actual_outcome: '2x reduction observed due to unoptimized prompt templates',
              gap_summary: 'Task completed technically, but realized benefits fall short of strategic target.',
              completion_without_success_flag: true
            }
          ],
          recommendations: [
            {
              id: 'erec_01',
              objective_id: 'eobj_01',
              initiative_id: 'init_agent_mesh_v2',
              recommendation_type: 'resequence',
              reason: 'Resequence Edge Node deployment to prioritize high-volume domestic workspaces while resolving European peering blocker.',
              evidence_json: { velocity_impact: '+22% overall execution throughput' },
              status: 'proposed'
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

  const handleApproveRecommendation = async (recId: string) => {
    try {
      const res = await fetch(`/api/v1/execution-intelligence/recommendations/${recId}/approve`, {
        method: 'POST'
      });
      if (res.ok) {
        const json = await res.json();
        setApprovalMsg(json.message);
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
      const res = await fetch(`/api/v1/execution-intelligence/query?query=${encodeURIComponent(queryText)}`, {
        method: 'POST'
      });
      if (res.ok) {
        const json = await res.json();
        setQueryResult(json);
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
            <span className="p-2 bg-indigo-600/20 text-indigo-400 rounded-lg text-lg">🚀</span>
            Enterprise Strategic Execution Intelligence 2.0
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Strategy → Strategic Objectives → Portfolio → Programs → Initiatives → Missions → Execution → Deliverables → Outcomes → Benefits → Strategic Impact.
          </p>
        </div>
        <div className="flex gap-2">
          <span className="px-3 py-1 bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 rounded-full text-xs font-semibold">
            Strategy-to-Outcome Visibility
          </span>
          <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full text-xs font-semibold">
            Human Approval Governed
          </span>
        </div>
      </div>

      {/* Telemetry Header */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Strategic Objectives</div>
          <div className="text-2xl font-bold text-slate-100 mt-1">{data?.objectivesCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Overall Coverage</div>
          <div className="text-2xl font-bold text-indigo-400 mt-1">{((data?.overallExecutionCoveragePct || 0) * 100).toFixed(0)}%</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Velocity Index</div>
          <div className="text-2xl font-bold text-emerald-400 mt-1">{data?.executionVelocityIndex || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Active Blockers</div>
          <div className="text-2xl font-bold text-rose-400 mt-1">{data?.activeBlockersCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Stale Decision Gaps</div>
          <div className="text-2xl font-bold text-amber-400 mt-1">{data?.staleDecisionGapsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Outcome Gaps</div>
          <div className="text-2xl font-bold text-purple-400 mt-1">{data?.outcomeGapsCount || 0}</div>
        </div>
      </div>

      {/* Approval Notification Banner */}
      {approvalMsg && (
        <div className="p-4 bg-emerald-950/50 border border-emerald-800/60 rounded-xl text-emerald-300 text-sm flex justify-between items-center">
          <span>✅ {approvalMsg}</span>
          <button onClick={() => setApprovalMsg(null)} className="text-xs text-slate-400 hover:text-white">Dismiss</button>
        </div>
      )}

      {/* Subsystem Tabs */}
      <div className="flex border-b border-slate-800 gap-2 text-sm overflow-x-auto pb-1">
        {[
          { id: 'overview', label: 'Execution Overview' },
          { id: 'objectives', label: 'Strategic Objectives & Alignment' },
          { id: 'coverage', label: 'Coverage & Path Integrity' },
          { id: 'drift', label: 'Drift & Velocity' },
          { id: 'blockers', label: 'Dependency Blockers & Capacity' },
          { id: 'decision_gaps', label: 'Decision Gaps' },
          { id: 'outcomes', label: 'Outcome Gaps & Waste' },
          { id: 'recommendations', label: 'Recommendations & Approvals' },
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

      {/* Content */}
      {loading ? (
        <div className="p-8 text-center text-slate-500">Loading Execution Intelligence state...</div>
      ) : (
        <div className="space-y-6">
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-indigo-400 flex items-center gap-2">
                  <span>🎯</span> Strategic Objectives & Alignment
                </h2>
                {data?.objectives?.[0] && (
                  <div className="space-y-3 text-sm">
                    <div className="font-bold text-slate-100">{data.objectives[0].name}</div>
                    <div className="p-3 bg-slate-950 rounded border border-indigo-800/40 text-indigo-300 text-xs">
                      {data.objectives[0].description}
                    </div>
                    <div className="grid grid-cols-2 gap-2 text-xs text-slate-400">
                      <span>Target: {data.objectives[0].target_outcome}</span>
                      <span>Owner: {data.objectives[0].owner}</span>
                    </div>
                  </div>
                )}
              </div>

              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-rose-400 flex items-center gap-2">
                  <span>⚠️</span> Active Dependency Blocker
                </h2>
                {data?.blockers?.[0] && (
                  <div className="space-y-3 text-sm">
                    <div className="font-bold text-slate-100">Dependency: {data.blockers[0].dependency_id}</div>
                    <div className="p-3 bg-slate-950 rounded border border-rose-800/40 text-rose-300 text-xs">
                      {data.blockers[0].impact_summary}
                    </div>
                    <div className="flex justify-between items-center text-xs text-slate-400">
                      <span>Owner: {data.blockers[0].owner}</span>
                      <span className="px-2 py-0.5 bg-rose-500/20 text-rose-300 rounded font-bold">
                        Blocked for {data.blockers[0].duration_days} days
                      </span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'objectives' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Strategic Objectives & Execution Alignment</h2>
              {data?.objectives?.map((obj: any) => (
                <div key={obj.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-indigo-300">{obj.name}</span>
                    <span className="text-xs px-2 py-0.5 bg-emerald-500/20 text-emerald-400 rounded font-bold">{obj.status}</span>
                  </div>
                  <p className="text-xs text-slate-300">{obj.description}</p>
                  <div className="text-xs text-indigo-400">Target Outcome: {obj.target_outcome}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'coverage' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Multi-Layer Execution Coverage & Path Integrity</h2>
              {data?.coverages?.map((cov: any) => (
                <div key={cov.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                  <div className="grid grid-cols-2 md:grid-cols-5 gap-3 text-center">
                    <div className="p-2 bg-slate-900 rounded">
                      <div className="text-xs text-slate-400">Portfolio</div>
                      <div className="text-base font-bold text-indigo-400">{(cov.portfolio_coverage_pct * 100).toFixed(0)}%</div>
                    </div>
                    <div className="p-2 bg-slate-900 rounded">
                      <div className="text-xs text-slate-400">Initiative</div>
                      <div className="text-base font-bold text-blue-400">{(cov.initiative_coverage_pct * 100).toFixed(0)}%</div>
                    </div>
                    <div className="p-2 bg-slate-900 rounded">
                      <div className="text-xs text-slate-400">Mission</div>
                      <div className="text-base font-bold text-emerald-400">{(cov.mission_coverage_pct * 100).toFixed(0)}%</div>
                    </div>
                    <div className="p-2 bg-slate-900 rounded">
                      <div className="text-xs text-slate-400">Execution</div>
                      <div className="text-base font-bold text-purple-400">{(cov.execution_coverage_pct * 100).toFixed(0)}%</div>
                    </div>
                    <div className="p-2 bg-slate-900 rounded">
                      <div className="text-xs text-slate-400">Benefit</div>
                      <div className="text-base font-bold text-amber-400">{(cov.benefit_coverage_pct * 100).toFixed(0)}%</div>
                    </div>
                  </div>
                  {data?.paths?.[0] && (
                    <div className="p-3 bg-slate-900 border border-emerald-800/40 rounded text-xs text-emerald-300 flex justify-between items-center">
                      <span>Execution Path: Strategy → Objective → Initiative → Mission → Action → Deliverable → Outcome → Benefit</span>
                      <span className="px-2 py-0.5 bg-emerald-500/20 rounded font-bold">Status: {data.paths[0].path_integrity_status}</span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}

          {activeTab === 'drift' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Execution Drift Signals & Velocity Warning</h2>
              {data?.drifts?.map((df: any) => (
                <div key={df.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-amber-500">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-amber-300">Drift Type: {df.drift_type}</span>
                    <span className="text-xs px-2 py-0.5 bg-amber-500/20 text-amber-300 rounded font-bold">Severity: {df.severity}</span>
                  </div>
                  <div className="text-xs text-slate-300">Evidence: {JSON.stringify(df.evidence_json)}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'blockers' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Dependency Blockers & Operating Graph Propagation</h2>
              {data?.blockers?.map((bl: any) => (
                <div key={bl.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm border-l-4 border-l-rose-500">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-rose-300">Blocked Initiative: {bl.blocked_initiative_id}</span>
                    <span className="text-xs px-2 py-0.5 bg-rose-500/20 text-rose-300 rounded font-bold">{bl.status}</span>
                  </div>
                  <p className="text-xs text-slate-300">Impact: {bl.impact_summary}</p>
                  <div className="text-xs text-slate-400">Owner: {bl.owner} (Blocked for {bl.duration_days} days)</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'decision_gaps' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Decision-to-Action Gaps & Stale Decision Alerts</h2>
              {data?.decisionGaps?.map((dg: any) => (
                <div key={dg.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-amber-500">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-amber-300">Decision: {dg.decision_id}</span>
                    <span className="text-xs px-2 py-0.5 bg-amber-500/20 text-amber-300 rounded font-bold">Stale Unexecuted ({dg.delay_days} days)</span>
                  </div>
                  <div className="text-xs text-slate-400">Approval ID: {dg.approval_id}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'outcomes' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Execution Outcome Gaps (Completion ≠ Success)</h2>
              {data?.outcomeGaps?.map((og: any) => (
                <div key={og.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm border-l-4 border-l-purple-500">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-purple-300">Execution: {og.execution_id}</span>
                    <span className="text-xs px-2 py-0.5 bg-purple-500/20 text-purple-300 rounded font-bold">Completion Without Success</span>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
                    <div className="p-2 bg-slate-900 rounded text-slate-300">Expected: {og.expected_outcome}</div>
                    <div className="p-2 bg-slate-900 rounded text-amber-300">Actual: {og.actual_outcome}</div>
                  </div>
                  <p className="text-xs text-slate-400">{og.gap_summary}</p>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'recommendations' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Execution Recommendations (Human Authorization Governed)</h2>
              {data?.recommendations?.map((rc: any) => (
                <div key={rc.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-indigo-300">Type: {rc.recommendation_type}</span>
                    <span className={`text-xs px-2 py-0.5 rounded font-bold ${
                      rc.status === 'approved' ? 'bg-emerald-500/20 text-emerald-300' : 'bg-indigo-500/20 text-indigo-300'
                    }`}>
                      {rc.status}
                    </span>
                  </div>
                  <p className="text-xs text-slate-300">Reason: {rc.reason}</p>

                  {rc.status === 'proposed' && (
                    <button
                      onClick={() => handleApproveRecommendation(rc.id)}
                      className="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold rounded transition-colors"
                    >
                      Authorize Execution Recommendation
                    </button>
                  )}
                </div>
              ))}
            </div>
          )}

          {activeTab === 'nl_query' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Natural Language Execution Query Interface</h2>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={queryText}
                  onChange={(e) => setQueryText(e.target.value)}
                  placeholder="Ask a strategic execution query..."
                  className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
                />
                <button
                  onClick={handleQuery}
                  disabled={queryLoading}
                  className="px-5 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-medium rounded-lg text-sm transition-colors"
                >
                  {queryLoading ? 'Evaluating...' : 'Query'}
                </button>
              </div>

              {queryResult && (
                <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                  <div className="text-xs text-indigo-400 font-semibold">Query: {queryResult.query}</div>
                  <div className="space-y-2">
                    {queryResult.results?.map((res: any, idx: number) => (
                      <div key={idx} className="p-3 bg-slate-900 rounded space-y-1 text-xs">
                        <div className="font-semibold text-slate-200">{res.objective_name}</div>
                        <div className="text-indigo-300">Alignment: {res.alignment_status}</div>
                        <div className="text-emerald-400">Coverage: {res.execution_coverage}</div>
                        <div className="text-amber-400">Drift: {res.drift_signal}</div>
                        <div className="text-rose-400">Blocker: {res.active_blocker}</div>
                        <div className="text-purple-300">Outcome Gap: {res.outcome_gap}</div>
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
