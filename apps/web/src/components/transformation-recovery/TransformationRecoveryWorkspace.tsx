'use client';

import React, { useState, useEffect } from 'react';

export function TransformationRecoveryWorkspace() {
  const [activeTab, setActiveTab] = useState<'overview' | 'disruptions_impact' | 'criticality_priority' | 'paths_options' | 'simulations_comparison' | 'bottlenecks_trajectories' | 'gates_checkpoints' | 'return_to_normal' | 'readiness_gaps' | 'drills' | 'recovery_query'>('overview');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('What recovery options exist for the IAM dependency disruption?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);
  const [drillMessage, setDrillMessage] = useState<string>('');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/transformation-recovery');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      } else {
        // Fallback seed structure
        setData({
          activeRecoveryDomainsCount: 1,
          confirmedDisruptionsCount: 1,
          recommendedRecoveryPathsCount: 1,
          simulatedOptionsCount: 1,
          activeReturnToNormalPlansCount: 1,
          recoveryReadinessScore: 0.92,
          domains: [
            { id: 'rd_01', name: 'Enterprise Core IAM & FinOps Resilience Domain', scope: 'enterprise', owner: 'Head of Enterprise Resilience', status: 'recovery_active', version: 'v2.0' }
          ],
          disruptions: [
            { id: 'dis_01', disruption_type: 'dependency_failure', source: 'Core IAM Gateway API Rate-Limiter Failure', severity: 'high', status: 'confirmed' }
          ],
          impacts: [
            { id: 'imp_01', strategic_impact: 'High. Threatens Q4 enterprise cloud cost reduction targets if unmitigated.' }
          ],
          criticalities: [
            { id: 'crit_01', strategic_importance: 0.92, dependency_centrality: 0.88, recovery_urgency: 0.95 }
          ],
          priorities: [
            { id: 'prio_01', priority_score: 0.94, evidence_summary: 'Core IAM API failure blocks 2 downstream wave deployments; recovery urgency rated 95%.' }
          ],
          protectionTargets: [
            { id: 'targ_01', target_type: 'critical_capability', target_name: 'IAM Federation API Gateway', protection_level: 'maximum' }
          ],
          objectives: [
            { id: 'obj_01', objective_name: 'Restore IAM Gateway Federation & Accelerate Wave 2 Path', target_recovery_time_hours: 72.0, confidence: 0.93 }
          ],
          paths: [
            { id: 'path_01', path_name: 'Path A: Reroute via Secondary OAuth Cluster & Reallocate 15 FTEs', status: 'recommended' }
          ],
          options: [
            { id: 'opt_01', option_type: 'substitute', title: 'Failover to Secondary IAM Cluster & Delegate Approvals', safety_score: 0.91, status: 'simulated' }
          ],
          bottlenecks: [
            { id: 'bot_01', bottleneck_type: 'capacity', entity_name: 'IAM Security Operations Specialist FTEs', impact_description: '15 FTE capacity shortfall in IAM integration team during cluster failover window.' }
          ],
          trajectories: [
            { id: 'traj_01', metric: 'IAM Capability Availability %', confidence: 0.94 }
          ],
          comparisons: [
            { id: 'comp_01', time_score: 0.90, risk_score: 0.08, cost_score: 120000.0, reversibility_score: 0.92 }
          ],
          checkpoints: [
            { id: 'cp_01', checkpoint_name: 'Secondary OAuth Cluster Synchronization Verification', status: 'pending' }
          ],
          gates: [
            { id: 'gate_01', gate_name: 'Stabilization Complete Gate', status: 'open' }
          ],
          returnPlans: [
            { id: 'ret_01', criteria_summary: 'All IAM endpoints verified healthy for 48 consecutive hours; Wave 2 milestones resynced.', status: 'draft' }
          ],
          resilienceGaps: [
            { id: 'gap_01', gap_type: 'single_point_dependency', description: 'Core IAM OAuth Gateway v2 lacks automated cross-region failover route.', severity: 'high' }
          ],
          improvements: [
            { id: 'imp_rec_01', improvement_type: 'redundancy', title: 'Implement Multi-Region Active-Active IAM Gateway Cluster', recommendation_only: true }
          ],
          readinesses: [
            { id: 'read_01', readiness_score: 0.92 }
          ],
          drills: [
            { id: 'drill_01', drill_name: 'Q3 Enterprise IAM Gateway Outage Simulation Exercise', no_production_mutation: true }
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
      const res = await fetch(`/api/v1/transformation-recovery/query?query=${encodeURIComponent(queryText)}`, {
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

  const handleRunDrill = async (drillId: string) => {
    setDrillMessage('Running drill exercise in virtual simulation lab...');
    try {
      const res = await fetch(`/api/v1/transformation-recovery/drills/${drillId}/run`, { method: 'POST' });
      if (res.ok) {
        const json = await res.json();
        setDrillMessage(`Drill exercise completed safely in simulation! Simulated recovery: ${json.simulatedRecoveryHours} hours. Zero production state mutated.`);
      }
    } catch (e) {
      console.error(e);
      setDrillMessage('Drill execution failed.');
    }
  };

  return (
    <div className="p-6 space-y-6 bg-slate-950 text-slate-100 min-h-screen">
      {/* Header */}
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
            <span className="p-2 bg-emerald-600/20 text-emerald-400 rounded-lg text-lg">🛡️</span>
            Enterprise Transformation Recovery Orchestration 2.0
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Disruption → Impact Propagation → Criticality → Recovery Options → Simulation → Human Approval → Verified Execution → Return to Normal.
          </p>
        </div>
        <div className="flex gap-2">
          <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full text-xs font-semibold">
            Human-Authorized Recovery
          </span>
          <span className="px-3 py-1 bg-blue-500/10 text-blue-400 border border-blue-500/20 rounded-full text-xs font-semibold">
            Zero Production Mutation Drills
          </span>
        </div>
      </div>

      {/* Operational Telemetry Header */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Active Recovery Domains</div>
          <div className="text-2xl font-bold text-emerald-400 mt-1">{data?.activeRecoveryDomainsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Confirmed Disruptions</div>
          <div className="text-2xl font-bold text-red-400 mt-1">{data?.confirmedDisruptionsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Recovery Paths</div>
          <div className="text-2xl font-bold text-indigo-400 mt-1">{data?.recommendedRecoveryPathsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Simulated Options</div>
          <div className="text-2xl font-bold text-purple-400 mt-1">{data?.simulatedOptionsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Return Plans</div>
          <div className="text-2xl font-bold text-teal-400 mt-1">{data?.activeReturnToNormalPlansCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Readiness Score</div>
          <div className="text-2xl font-bold text-amber-400 mt-1">92.0%</div>
        </div>
      </div>

      {/* Subsystem Tabs */}
      <div className="flex border-b border-slate-800 gap-2 text-sm overflow-x-auto pb-1">
        {[
          { id: 'overview', label: 'Recovery Overview & Domains' },
          { id: 'disruptions_impact', label: 'Disruptions & Impact' },
          { id: 'criticality_priority', label: 'Criticality & Protection' },
          { id: 'paths_options', label: 'Recovery Paths & Options' },
          { id: 'simulations_comparison', label: 'Path Simulations & Comparisons' },
          { id: 'bottlenecks_trajectories', label: 'Bottlenecks & Trajectories' },
          { id: 'gates_checkpoints', label: 'Gates & Checkpoints' },
          { id: 'return_to_normal', label: 'Return to Normal Plans' },
          { id: 'readiness_gaps', label: 'Resilience Gaps & Readiness' },
          { id: 'drills', label: 'Simulation Drills' },
          { id: 'recovery_query', label: 'Recovery Query Engine' }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-2 font-medium rounded-t-lg transition-colors whitespace-nowrap ${
              activeTab === tab.id
                ? 'bg-slate-900 text-emerald-400 border-b-2 border-emerald-500'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/40'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Content */}
      {loading ? (
        <div className="p-8 text-center text-slate-500">Loading Enterprise Transformation Recovery Orchestration...</div>
      ) : (
        <div className="space-y-6">
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-emerald-400 flex items-center gap-2">
                  <span>🛡️</span> Active Recovery Domains
                </h2>
                <div className="space-y-2 text-sm">
                  {data?.domains?.map((rd: any) => (
                    <div key={rd.id} className="p-3 bg-slate-950 rounded border border-emerald-800/40 flex justify-between items-center text-xs">
                      <div>
                        <div className="font-bold text-slate-100">{rd.name}</div>
                        <div className="text-slate-400">Scope: {rd.scope} | Owner: {rd.owner}</div>
                      </div>
                      <span className="px-2 py-0.5 bg-emerald-500/20 text-emerald-300 rounded font-bold">{rd.status.toUpperCase()}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-red-400 flex items-center gap-2">
                  <span>💥</span> Active Disruption Signal
                </h2>
                <div className="space-y-2 text-sm">
                  {data?.disruptions?.map((dis: any) => (
                    <div key={dis.id} className="p-3 bg-slate-950 rounded border border-red-800/40 space-y-1 text-xs">
                      <div className="font-bold text-red-300">Type: {dis.disruption_type.toUpperCase()} | Source: {dis.source}</div>
                      <div className="text-slate-300">Severity: {dis.severity.toUpperCase()} | Status: {dis.status.toUpperCase()}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'disruptions_impact' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Disruption Signals & Strategic Impact Mapping</h2>
              {data?.impacts?.map((imp: any) => (
                <div key={imp.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-red-500">
                  <div className="font-bold text-red-300">Strategic Impact: {imp.strategic_impact}</div>
                  <div className="text-xs text-slate-300">Affected Transformations: {imp.affected_transformations_json?.join(', ')}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'criticality_priority' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Multi-Dimensional Criticality & Protection Targets</h2>
              {data?.criticalities?.map((crit: any) => (
                <div key={crit.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-amber-500">
                  <div className="flex justify-between items-center font-bold text-amber-300">
                    <span>Strategic Importance: {(crit.strategic_importance * 100).toFixed(0)}%</span>
                    <span className="text-xs px-2 py-0.5 bg-amber-500/20 text-amber-300 rounded font-bold">Recovery Urgency: {(crit.recovery_urgency * 100).toFixed(0)}%</span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'paths_options' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Recovery Paths & Option Selection</h2>
              {data?.paths?.map((path: any) => (
                <div key={path.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-indigo-500">
                  <div className="flex justify-between items-center font-bold text-indigo-300">
                    <span>Path: {path.path_name}</span>
                    <span className="text-xs px-2 py-0.5 bg-indigo-500/20 text-indigo-300 rounded font-bold">Status: {path.status.toUpperCase()}</span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'simulations_comparison' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Recovery Path Simulation & Comparison Framework</h2>
              {data?.comparisons?.map((comp: any) => (
                <div key={comp.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-purple-500">
                  <div className="font-bold text-purple-300">Recovery Time Score: {(comp.time_score * 100).toFixed(0)}% | Secondary Risk Score: {(comp.risk_score * 100).toFixed(0)}%</div>
                  <div className="text-xs text-slate-300">Estimated Cost Impact: ${comp.cost_score?.toLocaleString()} | Reversibility: {(comp.reversibility_score * 100).toFixed(0)}%</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'return_to_normal' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Return to Normal Execution Plans</h2>
              {data?.returnPlans?.map((ret: any) => (
                <div key={ret.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-teal-500">
                  <div className="flex justify-between items-center font-bold text-teal-300">
                    <span>Criteria Summary: {ret.criteria_summary}</span>
                    <span className="text-xs px-2 py-0.5 bg-teal-500/20 text-teal-300 rounded font-bold">Status: {ret.status.toUpperCase()}</span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'drills' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Simulated Disruption Drills (Zero Production State Mutation)</h2>
              {drillMessage && (
                <div className="p-3 bg-emerald-950/40 border border-emerald-800/40 text-emerald-300 text-xs rounded">
                  {drillMessage}
                </div>
              )}
              {data?.drills?.map((drill: any) => (
                <div key={drill.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm border-l-4 border-l-blue-500">
                  <div className="flex justify-between items-center font-bold text-blue-300">
                    <span>Drill Exercise: {drill.drill_name}</span>
                    <span className="text-xs px-2 py-0.5 bg-blue-500/20 text-blue-300 rounded font-bold">Zero Production Mutation</span>
                  </div>
                  <div className="text-xs text-slate-300">{drill.scenario_description}</div>
                  <button
                    onClick={() => handleRunDrill(drill.id)}
                    className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white font-medium rounded-lg text-xs transition-colors"
                  >
                    Run Simulation Drill Exercise
                  </button>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'recovery_query' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Natural Language Recovery Situation Query Engine</h2>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={queryText}
                  onChange={(e) => setQueryText(e.target.value)}
                  placeholder="Ask a recovery situation query..."
                  className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-sm text-slate-100 focus:outline-none focus:border-emerald-500"
                />
                <button
                  onClick={handleQuery}
                  disabled={queryLoading}
                  className="px-5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-medium rounded-lg text-sm transition-colors"
                >
                  {queryLoading ? 'Searching...' : 'Query'}
                </button>
              </div>

              {queryResult && (
                <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                  <div className="text-xs text-emerald-400 font-semibold">Query: {queryResult.query}</div>
                  <div className="space-y-2">
                    {queryResult.results?.map((res: any, idx: number) => (
                      <div key={idx} className="p-3 bg-slate-900 rounded space-y-1 text-xs">
                        <div className="font-semibold text-emerald-300">{res.domain}</div>
                        <div className="text-red-300">Disruption: {res.disruption}</div>
                        <div className="text-slate-300">Strategic Impact: {res.impact}</div>
                        <div className="text-indigo-300">Recommended Path: {res.recommended_path}</div>
                        <div className="text-purple-300">Recovery Objective: {res.recovery_objective}</div>
                        <div className="text-teal-300">Return to Normal Status: {res.return_to_normal_status}</div>
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
