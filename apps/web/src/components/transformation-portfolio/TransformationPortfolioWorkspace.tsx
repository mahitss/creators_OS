'use client';

import React, { useState, useEffect } from 'react';

export function TransformationPortfolioWorkspace() {
  const [activeTab, setActiveTab] = useState<'overview' | 'candidates' | 'dependencies' | 'sequences' | 'capacity' | 'optionality' | 'waves' | 'rebalances' | 'nl_query'>('overview');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('Which transformation should happen first?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);
  const [approvalMsg, setApprovalMsg] = useState<string | null>(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/transformation-portfolio');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      } else {
        // Fallback seed structure
        setData({
          portfoliosCount: 1,
          candidatesCount: 2,
          criticalPathCandidatesCount: 2,
          sequencesCount: 1,
          sequenceComparisonsCount: 1,
          activeCapacityPlansCount: 1,
          lockInRisksCount: 1,
          wavesCount: 1,
          minimumSetsCount: 1,
          proposedRebalancesCount: 1,
          overallPortfolioRobustnessScore: 0.94,
          portfolios: [
            {
              id: 'transport_01',
              name: 'Global Cognitive Enterprise Transformation Portfolio 2026-2029',
              description: 'Strategic portfolio governing AI-Augmented Mesh, ActionGateway Pre-signer, and Autonomous FinOps transformations.',
              strategy_id: 'strat_enterprise_growth_01',
              horizon: '3_year',
              status: 'approved',
              owner: 'usr_chief_investment_officer'
            }
          ],
          candidates: [
            {
              id: 'cand_01',
              transformation_program_id: 'transprog_01',
              strategic_value_json: { growth: 'high', cost_reduction: '30%', resilience: '98%' },
              urgency: 'critical',
              risk_score: 0.12,
              cost_estimate: 250000.0,
              optional_value: 0.92
            },
            {
              id: 'cand_02',
              transformation_program_id: 'transprog_finops_02',
              strategic_value_json: { growth: 'medium', cost_reduction: '45%', resilience: '94%' },
              urgency: 'medium',
              risk_score: 0.18,
              cost_estimate: 180000.0,
              optional_value: 0.88
            }
          ],
          graphs: [
            {
              id: 'depgraph_01',
              critical_path_json: ['cand_01', 'cand_02'],
              cycles_detected: false
            }
          ],
          sequences: [
            {
              id: 'seq_risk_first_01',
              name: 'Risk-First Foundational Sequence',
              sequence_type: 'risk_first',
              phases_json: ['Phase 1: Compliance Auto-signer', 'Phase 2: FinOps Autonomous Scale'],
              order_json: ['cand_01', 'cand_02'],
              status: 'active'
            }
          ],
          comparisons: [
            {
              id: 'seqcomp_01',
              sequence_a_id: 'seq_risk_first_01',
              time_diff: -0.35,
              cost_diff: -0.10,
              risk_diff: -0.40,
              robustness_score: 0.94
            }
          ],
          capacityPlans: [
            {
              id: 'cplan_01',
              time_window: 'Q3-2026',
              required_capacity: 60.0,
              available_capacity: 100.0,
              committed_capacity: 45.0,
              buffer_capacity: 40.0
            }
          ],
          lockInRisks: [
            {
              id: 'lockin_01',
              risk_type: 'architecture',
              description: 'Zero-Trust PolicyEngine rule structure preserves open AST schemas to avoid vendor lock-in.',
              severity: 'low',
              reversibility: 'high'
            }
          ],
          waves: [
            {
              id: 'wave_01',
              wave_number: 1,
              wave_type: 'foundation',
              candidate_ids_json: ['cand_01'],
              status: 'executing'
            }
          ],
          minimumSets: [
            {
              id: 'minset_01',
              target_objective: 'Sub-1h Skill Certification & 30% Cost Reduction',
              required_candidate_ids_json: ['cand_01'],
              total_cost: 250000.0,
              total_time: '3_months'
            }
          ],
          rebalances: [
            {
              id: 'rebal_01',
              rebalance_reason: 'scenario_shift',
              proposed_sequence_id: 'seq_risk_first_01',
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

  const handleApproveRebalance = async (rebalanceId: string) => {
    try {
      const res = await fetch(`/api/v1/transformation-portfolio/rebalances/${rebalanceId}/approve`, {
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
      const res = await fetch(`/api/v1/transformation-portfolio/query?query=${encodeURIComponent(queryText)}`, {
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
            <span className="p-2 bg-blue-600/20 text-blue-400 rounded-lg text-lg">📊</span>
            Enterprise Transformation Portfolio Intelligence + Change Sequencing 2.0
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Transformation Candidates → Dependencies → Capacity → Risk → Optionality → Change Sequencing → Wave Rollout → Governed Rebalancing.
          </p>
        </div>
        <div className="flex gap-2">
          <span className="px-3 py-1 bg-blue-500/10 text-blue-400 border border-blue-500/20 rounded-full text-xs font-semibold">
            Change Sequencing Engine
          </span>
          <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full text-xs font-semibold">
            Human Approval Governed
          </span>
        </div>
      </div>

      {/* Telemetry Header */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Active Portfolios</div>
          <div className="text-2xl font-bold text-slate-100 mt-1">{data?.portfoliosCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Candidates</div>
          <div className="text-2xl font-bold text-blue-400 mt-1">{data?.candidatesCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Critical Path Length</div>
          <div className="text-2xl font-bold text-rose-400 mt-1">{data?.criticalPathCandidatesCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Robustness Score</div>
          <div className="text-2xl font-bold text-emerald-400 mt-1">{data?.overallPortfolioRobustnessScore ? (data.overallPortfolioRobustnessScore * 100).toFixed(0) : 0}%</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Execution Waves</div>
          <div className="text-2xl font-bold text-amber-400 mt-1">{data?.wavesCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Rebalance Proposals</div>
          <div className="text-2xl font-bold text-purple-400 mt-1">{data?.proposedRebalancesCount || 0}</div>
        </div>
      </div>

      {/* Approval Banner */}
      {approvalMsg && (
        <div className="p-4 bg-emerald-950/50 border border-emerald-800/60 rounded-xl text-emerald-300 text-sm flex justify-between items-center">
          <span>✅ {approvalMsg}</span>
          <button onClick={() => setApprovalMsg(null)} className="text-xs text-slate-400 hover:text-white">Dismiss</button>
        </div>
      )}

      {/* Subsystem Tabs */}
      <div className="flex border-b border-slate-800 gap-2 text-sm overflow-x-auto pb-1">
        {[
          { id: 'overview', label: 'Portfolio Overview' },
          { id: 'candidates', label: 'Candidates & Value' },
          { id: 'dependencies', label: 'Dependency Graph & Critical Path' },
          { id: 'sequences', label: 'Sequences & Comparisons' },
          { id: 'capacity', label: 'Capacity Planning' },
          { id: 'optionality', label: 'Optionality & Lock-In' },
          { id: 'waves', label: 'Waves & Exit Criteria' },
          { id: 'rebalances', label: 'Rebalances & Governance' },
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

      {/* Content */}
      {loading ? (
        <div className="p-8 text-center text-slate-500">Loading Transformation Portfolio state...</div>
      ) : (
        <div className="space-y-6">
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-blue-400 flex items-center gap-2">
                  <span>💼</span> Active Transformation Portfolio
                </h2>
                {data?.portfolios?.[0] && (
                  <div className="space-y-3 text-sm">
                    <div className="font-bold text-slate-100">{data.portfolios[0].name}</div>
                    <div className="p-3 bg-slate-950 rounded border border-blue-800/40 text-blue-300 text-xs">
                      {data.portfolios[0].description}
                    </div>
                    <div className="flex justify-between items-center text-xs text-slate-400">
                      <span>Owner: {data.portfolios[0].owner}</span>
                      <span className="px-2 py-0.5 bg-emerald-500/20 text-emerald-400 rounded font-bold">{data.portfolios[0].status}</span>
                    </div>
                  </div>
                )}
              </div>

              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-indigo-400 flex items-center gap-2">
                  <span>⚡</span> Active Change Sequence
                </h2>
                {data?.sequences?.[0] && (
                  <div className="space-y-3 text-sm">
                    <div className="font-bold text-slate-100">{data.sequences[0].name} ({data.sequences[0].sequence_type})</div>
                    <div className="p-3 bg-slate-950 rounded border border-indigo-800/40 text-indigo-300 text-xs">
                      <strong>Order:</strong> {data.sequences[0].order_json?.join(' → ')}
                    </div>
                    <div className="text-xs text-slate-400">Phases: {data.sequences[0].phases_json?.join(' | ')}</div>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'candidates' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Transformation Candidates & Strategic Value Dimensions</h2>
              {data?.candidates?.map((cand: any) => (
                <div key={cand.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-blue-300">Candidate Program: {cand.transformation_program_id}</span>
                    <span className="text-xs px-2 py-0.5 bg-rose-500/20 text-rose-300 rounded font-bold">Urgency: {cand.urgency}</span>
                  </div>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
                    <div className="p-2 bg-slate-900 rounded text-emerald-300">Resilience: {cand.strategic_value_json?.resilience}</div>
                    <div className="p-2 bg-slate-900 rounded text-teal-300">Cost Reduction: {cand.strategic_value_json?.cost_reduction}</div>
                    <div className="p-2 bg-slate-900 rounded text-slate-300">Cost Estimate: ${cand.cost_estimate?.toLocaleString()}</div>
                    <div className="p-2 bg-slate-900 rounded text-amber-300">Optional Value: {cand.optional_value}</div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'dependencies' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Transformation Dependency Graph & Critical Path Analysis</h2>
              {data?.graphs?.map((g: any) => (
                <div key={g.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-rose-300">Critical Path: {g.critical_path_json?.join(' → ')}</span>
                    <span className="text-xs px-2 py-0.5 bg-emerald-500/20 text-emerald-300 rounded font-bold">Cycles Detected: {g.cycles_detected ? 'YES' : 'NONE (Safe Graph)'}</span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'sequences' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Sequence Alternatives & Trade-off Robustness Comparisons</h2>
              {data?.comparisons?.map((cmp: any) => (
                <div key={cmp.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-indigo-300">Sequence Comparison ID: {cmp.id}</span>
                    <span className="text-xs px-2.5 py-0.5 bg-emerald-500/20 text-emerald-300 rounded font-bold">Robustness Score: {(cmp.robustness_score * 100).toFixed(0)}%</span>
                  </div>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
                    <div className="p-2 bg-slate-900 rounded text-emerald-300">Risk Reduction: {(cmp.risk_diff * -100).toFixed(0)}%</div>
                    <div className="p-2 bg-slate-900 rounded text-teal-300">Time Delta: {(cmp.time_diff * 100).toFixed(0)}%</div>
                    <div className="p-2 bg-slate-900 rounded text-indigo-300">Benefit Gain: +{(cmp.benefit_diff * 100).toFixed(0)}%</div>
                    <div className="p-2 bg-slate-900 rounded text-amber-300">Optionality Gain: +{(cmp.optionality_diff * 100).toFixed(0)}%</div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'capacity' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Capacity Headroom & Capital Constraints</h2>
              {data?.capacityPlans?.map((cp: any) => (
                <div key={cp.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-teal-300">Window: {cp.time_window}</span>
                    <span className="text-xs px-2 py-0.5 bg-emerald-500/20 text-emerald-300 rounded font-bold">Buffer Capacity: {cp.buffer_capacity}%</span>
                  </div>
                  <div className="flex gap-4 text-xs text-slate-400">
                    <span>Required: {cp.required_capacity}%</span>
                    <span>Committed: {cp.committed_capacity}%</span>
                    <span>Available: {cp.available_capacity}%</span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'optionality' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Strategic Optionality & Lock-In Risks</h2>
              {data?.lockInRisks?.map((lk: any) => (
                <div key={lk.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-amber-500">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-amber-300">Risk Type: {lk.risk_type}</span>
                    <span className="text-xs px-2 py-0.5 bg-emerald-500/20 text-emerald-300 rounded font-bold">Reversibility: {lk.reversibility}</span>
                  </div>
                  <p className="text-xs text-slate-300">{lk.description}</p>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'waves' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Transformation Waves & Exit Criteria</h2>
              {data?.waves?.map((wv: any) => (
                <div key={wv.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-blue-500">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-blue-300">Wave #{wv.wave_number} ({wv.wave_type})</span>
                    <span className="text-xs px-2 py-0.5 bg-blue-500/20 text-blue-300 rounded font-bold">{wv.status}</span>
                  </div>
                  <div className="text-xs text-slate-400">Candidates: {wv.candidate_ids_json?.join(', ')}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'rebalances' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Portfolio Rebalance Proposals (Human Approval Governed)</h2>
              {data?.rebalances?.map((rb: any) => (
                <div key={rb.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-purple-300">Rebalance Reason: {rb.rebalance_reason}</span>
                    <span className={`text-xs px-2 py-0.5 rounded font-bold ${
                      rb.status === 'approved' ? 'bg-emerald-500/20 text-emerald-300' : 'bg-purple-500/20 text-purple-300'
                    }`}>
                      {rb.status}
                    </span>
                  </div>
                  <div className="text-xs text-slate-400">Proposed Sequence: {rb.proposed_sequence_id}</div>

                  {rb.status === 'proposed' && (
                    <button
                      onClick={() => handleApproveRebalance(rb.id)}
                      className="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold rounded transition-colors"
                    >
                      Authorize Transformation Portfolio Rebalance
                    </button>
                  )}
                </div>
              ))}
            </div>
          )}

          {activeTab === 'nl_query' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Natural Language Portfolio & Sequencing Query Interface</h2>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={queryText}
                  onChange={(e) => setQueryText(e.target.value)}
                  placeholder="Ask a portfolio sequencing query..."
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
                        <div className="font-semibold text-slate-200">{res.portfolio_name}</div>
                        <div className="text-blue-300">Top Candidates: {res.top_candidates}</div>
                        <div className="text-rose-400">Critical Path: {res.critical_path}</div>
                        <div className="text-indigo-300">Recommended Sequence: {res.recommended_sequence}</div>
                        <div className="text-emerald-400">Capacity Headroom: {res.capacity_headroom}</div>
                        <div className="text-teal-300">Minimum Set: {res.minimum_viable_set}</div>
                        <div className="text-purple-300">Rebalance Proposal: {res.rebalance_proposal}</div>
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
