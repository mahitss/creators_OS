'use client';

import React, { useState, useEffect } from 'react';

export function TransformationWorkspace() {
  const [activeTab, setActiveTab] = useState<'overview' | 'programs' | 'future_models' | 'comparisons' | 'scenarios' | 'roadmaps' | 'pilots' | 'proposals' | 'nl_query'>('overview');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('Why does our operating model need to change?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);
  const [approvalMsg, setApprovalMsg] = useState<string | null>(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/transformation');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      } else {
        // Fallback seed structure
        setData({
          programsCount: 1,
          driversCount: 1,
          deltasCount: 1,
          futureModelsCount: 1,
          designOptionsCount: 1,
          scenariosCount: 1,
          roadmapsCount: 1,
          decisionGatesCount: 1,
          pilotsCount: 1,
          proposedChangeProposalsCount: 1,
          overallTransformationReadinessPct: 92.5,
          overallTransformationAdoptionPct: 91.0,
          programs: [
            {
              id: 'transprog_01',
              name: 'Enterprise Autonomous Operating Model Transformation 2026-2029',
              description: 'Multi-phase strategic operating model transformation transitioning from traditional siloed matrix to AI-Augmented Autonomous Mesh.',
              scope: 'Global Enterprise Engineering, Security Operations, and Executive Strategy',
              horizon: '3_year',
              owner: 'usr_chief_transformation_officer',
              status: 'executing'
            }
          ],
          drivers: [
            {
              id: 'transdriver_01',
              driver_type: 'operational_performance',
              source: 'Operating Graph Telemetry Sprint 75',
              evidence_json: { handoff_latency: '14.5h wait time between Engineering & Compliance' },
              confidence: 'high'
            }
          ],
          deltas: [
            {
              id: 'opdelta_01',
              gap_summary: 'Process & Decision Gap: Manual compliance review creates 14.5h latency bottleneck compared to automated sub-1h target.',
              severity: 'critical',
              evidence_json: { cycle_time_delta: '14.5h -> 0.2h', throughput_multiplier: '33x' }
            }
          ],
          futureModels: [
            {
              id: 'futmod_01',
              name: 'Federated Cognitive Agent Mesh Model',
              description: 'Platformized operating model delegating routine compliance checks to PolicyEngine pre-signed attestations.',
              design_principles_json: ['platform_first', 'control_by_design', 'simplify']
            }
          ],
          designOptions: [
            {
              id: 'desopt_01',
              option_type: 'platformize',
              expected_effect: 'Eliminate inter-departmental handoff friction while enforcing Zero-Trust compliance.'
            }
          ],
          comparisons: [
            {
              id: 'optcomp_01',
              option_a_id: 'desopt_01',
              option_b_id: 'desopt_manual_baseline',
              cost_tradeoff: -0.15,
              speed_tradeoff: 0.98,
              control_tradeoff: 0.05,
              resilience_tradeoff: 0.35,
              complexity_tradeoff: -0.10,
              classification: 'high_upside'
            }
          ],
          scenarios: [
            {
              id: 'transcen_01',
              scenario_name: '50x Skill Deployment Demand Surge',
              scenario_type: 'demand_surge',
              simulated_performance: 0.96,
              simulated_risk: 0.08,
              simulated_resilience: 0.98,
              status: 'simulated'
            }
          ],
          roadmaps: [
            {
              id: 'transroad_01',
              name: '3-Phase Operating Model Rollout Roadmap',
              phases_json: ['diagnose', 'design', 'pilot', 'transition', 'scale']
            }
          ],
          gates: [
            {
              id: 'gate_pilot_validation_01',
              gate_name: 'Phase 2 Pilot Validation Checkpoint',
              gate_outcome: 'proceed',
              status: 'approved'
            }
          ],
          pilots: [
            {
              id: 'transpilot_01',
              hypothesis: 'PolicyEngine pre-signed attestations will reduce skill deployment latency from 14.5h to sub-1h without introducing DLP violations.',
              duration_days: 30,
              outcome_status: 'validated'
            }
          ],
          changeProposals: [
            {
              id: 'transprop_01',
              proposal_title: 'Transition Security Compliance Audit to ActionGateway Pre-signed Attestations',
              description: 'Reconfigure inter-departmental decision right rule to allow PolicyEngine auto-signer for routine agent skill certification.',
              expected_effect: 'Reduce cycle time by 98.7% and eliminate engineering bottleneck.',
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

  const handleApproveProposal = async (proposalId: string) => {
    try {
      const res = await fetch(`/api/v1/transformation/change-proposals/${proposalId}/approve`, {
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
      const res = await fetch(`/api/v1/transformation/query?query=${encodeURIComponent(queryText)}`, {
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
            <span className="p-2 bg-indigo-600/20 text-indigo-400 rounded-lg text-lg">⚡</span>
            Enterprise Operating Model Transformation 2.0
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Current State → Observed Friction → Strategic Requirements → Design Options → Future Models → Scenario Simulation → Roadmap → Governed Execution → Adoption → Outcomes.
          </p>
        </div>
        <div className="flex gap-2">
          <span className="px-3 py-1 bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 rounded-full text-xs font-semibold">
            Transformation Intelligence
          </span>
          <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full text-xs font-semibold">
            Human Approval Governed
          </span>
        </div>
      </div>

      {/* Telemetry Header */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Active Programs</div>
          <div className="text-2xl font-bold text-slate-100 mt-1">{data?.programsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Current vs Target Deltas</div>
          <div className="text-2xl font-bold text-rose-400 mt-1">{data?.deltasCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Future Design Options</div>
          <div className="text-2xl font-bold text-indigo-400 mt-1">{data?.designOptionsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Readiness Score</div>
          <div className="text-2xl font-bold text-emerald-400 mt-1">{data?.overallTransformationReadinessPct || 0}%</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Pilot Validations</div>
          <div className="text-2xl font-bold text-amber-400 mt-1">{data?.pilotsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Change Proposals</div>
          <div className="text-2xl font-bold text-purple-400 mt-1">{data?.proposedChangeProposalsCount || 0}</div>
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
          { id: 'overview', label: 'Transformation Overview' },
          { id: 'programs', label: 'Programs & Drivers' },
          { id: 'future_models', label: 'Future Models & Options' },
          { id: 'comparisons', label: 'Trade-off Comparison' },
          { id: 'scenarios', label: 'Stress-Test Scenarios' },
          { id: 'roadmaps', label: 'Roadmaps & Decision Gates' },
          { id: 'pilots', label: 'Pilots & Validation' },
          { id: 'proposals', label: 'Change Proposals' },
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
        <div className="p-8 text-center text-slate-500">Loading Transformation state...</div>
      ) : (
        <div className="space-y-6">
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-indigo-400 flex items-center gap-2">
                  <span>🚀</span> Active Transformation Program
                </h2>
                {data?.programs?.[0] && (
                  <div className="space-y-3 text-sm">
                    <div className="font-bold text-slate-100">{data.programs[0].name}</div>
                    <div className="p-3 bg-slate-950 rounded border border-indigo-800/40 text-indigo-300 text-xs">
                      {data.programs[0].description}
                    </div>
                    <div className="text-xs text-slate-400">Scope: {data.programs[0].scope}</div>
                    <div className="flex justify-between items-center text-xs text-slate-400">
                      <span>Owner: {data.programs[0].owner}</span>
                      <span className="px-2 py-0.5 bg-emerald-500/20 text-emerald-400 rounded font-bold">{data.programs[0].status}</span>
                    </div>
                  </div>
                )}
              </div>

              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-rose-400 flex items-center gap-2">
                  <span>🎯</span> Current vs Target State Delta
                </h2>
                {data?.deltas?.[0] && (
                  <div className="space-y-3 text-sm border-l-4 border-l-rose-500 pl-3">
                    <div className="font-bold text-slate-100">{data.deltas[0].gap_summary}</div>
                    <div className="p-3 bg-slate-950 rounded border border-rose-800/40 text-rose-300 text-xs">
                      <strong>Cycle Time Delta:</strong> {data.deltas[0].evidence_json?.cycle_time_delta}<br/>
                      <strong>Throughput Multiplier:</strong> {data.deltas[0].evidence_json?.throughput_multiplier}
                    </div>
                    <span className="inline-block px-2 py-0.5 bg-rose-500/20 text-rose-300 rounded text-xs font-bold">
                      Severity: {data.deltas[0].severity}
                    </span>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'programs' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Transformation Programs & Strategic Drivers</h2>
              {data?.programs?.map((pr: any) => (
                <div key={pr.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-indigo-300">{pr.name}</span>
                    <span className="text-xs px-2 py-0.5 bg-emerald-500/20 text-emerald-400 rounded font-bold">{pr.status}</span>
                  </div>
                  <p className="text-xs text-slate-300">{pr.description}</p>
                  <div className="text-xs text-slate-400">Horizon: {pr.horizon} | Owner: {pr.owner}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'future_models' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Future Operating Models & Design Options</h2>
              {data?.futureModels?.map((fm: any) => (
                <div key={fm.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-teal-300">{fm.name}</span>
                    <span className="text-xs px-2 py-0.5 bg-teal-500/20 text-teal-300 rounded font-bold">Principles: {fm.design_principles_json?.join(', ')}</span>
                  </div>
                  <p className="text-xs text-slate-300">{fm.description}</p>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'comparisons' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Operating Model Design Comparisons & Trade-off Frontier</h2>
              {data?.comparisons?.map((cmp: any) => (
                <div key={cmp.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-indigo-300">Comparison ID: {cmp.id}</span>
                    <span className="text-xs px-2.5 py-0.5 bg-emerald-500/20 text-emerald-300 rounded font-bold uppercase">Classification: {cmp.classification}</span>
                  </div>
                  <div className="grid grid-cols-2 md:grid-cols-5 gap-2 text-xs">
                    <div className="p-2 bg-slate-900 rounded">Speed: +{(cmp.speed_tradeoff * 100).toFixed(0)}%</div>
                    <div className="p-2 bg-slate-900 rounded">Resilience: +{(cmp.resilience_tradeoff * 100).toFixed(0)}%</div>
                    <div className="p-2 bg-slate-900 rounded">Control: +{(cmp.control_tradeoff * 100).toFixed(0)}%</div>
                    <div className="p-2 bg-slate-900 rounded">Cost Delta: {(cmp.cost_tradeoff * 100).toFixed(0)}%</div>
                    <div className="p-2 bg-slate-900 rounded">Complexity: {(cmp.complexity_tradeoff * 100).toFixed(0)}%</div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'scenarios' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Stress-Test Transformation Scenarios</h2>
              {data?.scenarios?.map((sc: any) => (
                <div key={sc.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-amber-300">{sc.scenario_name} ({sc.scenario_type})</span>
                    <span className="text-xs px-2 py-0.5 bg-amber-500/20 text-amber-300 rounded font-bold">Simulated Resilience: {(sc.simulated_resilience * 100).toFixed(0)}%</span>
                  </div>
                  <div className="flex gap-4 text-xs text-slate-400">
                    <span>Performance: {(sc.simulated_performance * 100).toFixed(0)}%</span>
                    <span>Risk: {(sc.simulated_risk * 100).toFixed(0)}%</span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'roadmaps' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Transformation Roadmaps & Decision Gates</h2>
              {data?.roadmaps?.map((rm: any) => (
                <div key={rm.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="font-bold text-indigo-300">{rm.name}</div>
                  <div className="text-xs text-slate-400">Phases: {rm.phases_json?.join(' → ')}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'pilots' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Pilot Validations & Design Hypotheses</h2>
              {data?.pilots?.map((pl: any) => (
                <div key={pl.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-emerald-500">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-emerald-300">Pilot Outcome: {pl.outcome_status}</span>
                    <span className="text-xs px-2 py-0.5 bg-emerald-500/20 text-emerald-400 rounded font-bold">Duration: {pl.duration_days} days</span>
                  </div>
                  <p className="text-xs text-slate-300">Hypothesis: {pl.hypothesis}</p>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'proposals' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Transformation Change Proposals (Human Approval Governed)</h2>
              {data?.changeProposals?.map((cp: any) => (
                <div key={cp.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-purple-300">{cp.proposal_title}</span>
                    <span className={`text-xs px-2 py-0.5 rounded font-bold ${
                      cp.status === 'approved' ? 'bg-emerald-500/20 text-emerald-300' : 'bg-purple-500/20 text-purple-300'
                    }`}>
                      {cp.status}
                    </span>
                  </div>
                  <p className="text-xs text-slate-300">{cp.description}</p>
                  <div className="text-xs text-emerald-400">Expected Effect: {cp.expected_effect}</div>

                  {cp.status === 'proposed' && (
                    <button
                      onClick={() => handleApproveProposal(cp.id)}
                      className="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold rounded transition-colors"
                    >
                      Authorize Transformation Change Proposal
                    </button>
                  )}
                </div>
              ))}
            </div>
          )}

          {activeTab === 'nl_query' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Natural Language Transformation Query Interface</h2>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={queryText}
                  onChange={(e) => setQueryText(e.target.value)}
                  placeholder="Ask a transformation query..."
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
                        <div className="font-semibold text-slate-200">{res.program_name}</div>
                        <div className="text-amber-400">Driver: {res.driver}</div>
                        <div className="text-rose-400">Gap: {res.current_vs_target_gap}</div>
                        <div className="text-indigo-300">Design Option: {res.future_model_option}</div>
                        <div className="text-emerald-400">Stress Test: {res.stress_test_scenario}</div>
                        <div className="text-teal-300">Pilot Validation: {res.pilot_validation}</div>
                        <div className="text-purple-300">Change Proposal: {res.change_proposal}</div>
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
