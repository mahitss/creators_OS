'use client';

import React, { useState, useEffect } from 'react';

export function TransformationResilienceKnowledgeAssuranceCoordinationWorkspace() {
  const [activeTab, setActiveTab] = useState<
    | 'overview'
    | 'active_plans'
    | 'relationships'
    | 'resources'
    | 'demands'
    | 'contentions'
    | 'evidence_contentions'
    | 'review_contentions'
    | 'simulation_contentions'
    | 'deadline_collisions'
    | 'bottlenecks'
    | 'options'
    | 'scenarios'
    | 'recommendations'
    | 'coordination_plans'
    | 'conflicts'
    | 'cascades'
    | 'drift'
    | 'effectiveness'
    | 'query'
  >('overview');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('Which assurance plans compete for experts and simulation capacity?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/transformation-resilience-knowledge-assurance-coordination');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      } else {
        // Fallback seed data
        setData({
          domainsCount: 1,
          activePlansCount: 3,
          relationshipsCount: 1,
          resourcesCount: 1,
          contentionsCount: 1,
          evidenceContentionsCount: 1,
          reviewContentionsCount: 1,
          simulationContentionsCount: 1,
          deadlineCollisionsCount: 1,
          bottlenecksCount: 1,
          coordinationOptionsCount: 1,
          coordinationPlansCount: 1,
          cascadesCount: 1,
          domains: [
            { id: 'cdom_01', name: 'Global Enterprise Knowledge Assurance Coordination & Contention Intelligence 2.0', owner: 'Principal Enterprise Assurance Coordination Architect', status: 'active', version: 'v2.0' }
          ],
          activeSets: [
            { id: 'aset_01', active_plan_ids_json: ['aplan_01', 'aplan_hr_cloud_02', 'aplan_vendor_ops_03'] }
          ],
          relationships: [
            { id: 'prel_01', source_plan_id: 'aplan_01', target_plan_id: 'aplan_hr_cloud_02', relationship_type: 'blocks', description: 'Cloud SLA synthetic telemetry validation blocks HR Cloud Wave 4 deployment.' }
          ],
          resources: [
            { id: 'cres_sim_01', name: 'Governance Twin Simulation Cluster 01', resource_type: 'simulation_capacity', total_capacity: 1.0, unit: 'cluster_units' }
          ],
          contentions: [
            { id: 'rcont_01', resource_id: 'cres_sim_01', competing_plan_ids_json: ['aplan_01', 'aplan_hr_cloud_02'], demand_deficit: 0.20, severity: 'high' }
          ],
          evidenceContentions: [
            { id: 'econt_01', evidence_source_id: 'ev_src_interconnect_01', competing_plan_ids_json: ['aplan_01', 'aplan_vendor_ops_03'], severity: 'material' }
          ],
          reviewContentions: [
            { id: 'rvcont_01', review_domain: 'cloud_security', competing_plan_ids_json: ['aplan_01', 'aplan_hr_cloud_02'], review_capacity_deficit: 0.30, severity: 'high' }
          ],
          simulationContentions: [
            { id: 'scont_01', simulation_cluster: 'governance_twin_cluster_01', competing_plan_ids_json: ['aplan_01', 'aplan_hr_cloud_02'], compute_deficit_pct: 20.0, severity: 'material' }
          ],
          deadlineCollisions: [
            { id: 'dcoll_01', colliding_plan_ids_json: ['aplan_01', 'aplan_hr_cloud_02'], shared_deadline: '2026-08-27T00:00:00Z', impact_description: 'Both plans require final Governance Board approval on the same deadline date.' }
          ],
          bottlenecks: [
            { id: 'bot_01', bottleneck_type: 'simulation_capacity', description: 'Governance Twin Cluster 01 is 20% over-subscribed in Q3.', affected_plan_ids_json: ['aplan_01', 'aplan_hr_cloud_02'], severity: 'critical' }
          ],
          options: [
            { id: 'copt_sequence_01', option_type: 'sequence', title: 'Sequenced Simulation Execution (aplan_01 followed by aplan_hr_cloud_02)', coverage: 0.92, risk_reduction: 0.88, effort: 'medium', time_est: '14 days' }
          ],
          recommendations: [
            { id: 'crec_01', label: 'ANALYTICAL RECOMMENDATION — NOT APPROVAL', recommended_option: 'sequence', reason: 'Sequencing simulation execution eliminates 20% compute deficit while maintaining 92% coverage.' }
          ],
          plans: [
            { id: 'cplan_01', objective: 'Coordinate multi-plan simulation and review workloads for Q3 cloud rollout.', owner: 'Principal Enterprise Assurance Coordination Architect', status: 'approved' }
          ],
          cascades: [
            { id: 'casc_01', source_plan_id: 'aplan_01', affected_plan_id: 'aplan_hr_cloud_02', depth: 2, severity: 'material' }
          ],
          effectivenesses: [
            { id: 'ceff_01', contention_reduction: 0.85, risk_reduction: 0.90, coverage_improvement: 0.92, timeliness: 0.88, capacity_efficiency: 0.94, coordination_stability: 0.95 }
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
      const res = await fetch(`/api/v1/transformation-resilience-knowledge-assurance-coordination/query?query=${encodeURIComponent(queryText)}`, {
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
    <div className="p-6 space-y-6 max-w-[1600px] mx-auto text-slate-100">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-slate-900/80 p-6 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 via-indigo-400 to-blue-400">
              Enterprise Assurance Coordination & Contention Control 2.0
            </h1>
            <span className="px-3 py-1 text-xs font-semibold rounded-full bg-purple-500/10 text-purple-400 border border-purple-500/20">
              Human-Governed Coordination
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Detect resource contention, evidence sharing, review bottlenecks, simulation constraints, deadline collisions, and cross-plan cascades across active assurance plans.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={fetchData}
            className="px-4 py-2 text-xs font-medium rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition"
          >
            Refresh Telemetry
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Domain Status</p>
          <p className="text-xl font-bold text-blue-400 mt-1">Active</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Active Plan Set</p>
          <p className="text-xl font-bold text-emerald-400 mt-1">{data?.activePlansCount ?? 3}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Plan Relationships</p>
          <p className="text-xl font-bold text-purple-400 mt-1">{data?.relationshipsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Resource Contention</p>
          <p className="text-xl font-bold text-amber-400 mt-1">{data?.contentionsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Deadline Collisions</p>
          <p className="text-xl font-bold text-rose-400 mt-1">{data?.deadlineCollisionsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Bottlenecks</p>
          <p className="text-xl font-bold text-red-500 mt-1">{data?.bottlenecksCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Coordinated Plans</p>
          <p className="text-xl font-bold text-teal-400 mt-1">{data?.coordinationPlansCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Contention Reduction</p>
          <p className="text-xl font-bold text-cyan-400 mt-1">85.0%</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 overflow-x-auto space-x-2 scrollbar-none">
        {[
          { id: 'overview', label: 'Coordination Overview' },
          { id: 'active_plans', label: 'Active Plan Set' },
          { id: 'relationships', label: 'Plan Relationships' },
          { id: 'resources', label: 'Resource Definitions' },
          { id: 'demands', label: 'Resource Demands' },
          { id: 'contentions', label: 'Resource Contention' },
          { id: 'evidence_contentions', label: 'Evidence Contention' },
          { id: 'review_contentions', label: 'Review Contention' },
          { id: 'simulation_contentions', label: 'Simulation Contention' },
          { id: 'deadline_collisions', label: 'Deadline Collisions' },
          { id: 'bottlenecks', label: 'Portfolio Bottlenecks' },
          { id: 'options', label: 'Coordination Options' },
          { id: 'scenarios', label: 'Scenario Comparison' },
          { id: 'recommendations', label: 'Analytical Recommendations' },
          { id: 'coordination_plans', label: 'Coordinated Plans' },
          { id: 'conflicts', label: 'Conflict Resolutions' },
          { id: 'cascades', label: 'Cross-Plan Cascades' },
          { id: 'drift', label: 'Coordination Drift' },
          { id: 'effectiveness', label: 'Coordination Effectiveness' },
          { id: 'query', label: 'Coordination Query' }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-2.5 text-xs font-semibold whitespace-nowrap border-b-2 transition ${
              activeTab === tab.id
                ? 'border-purple-400 text-purple-400 bg-purple-500/5'
                : 'border-transparent text-slate-400 hover:text-slate-200 hover:border-slate-700'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 min-h-[400px]">
        {loading ? (
          <div className="flex items-center justify-center h-64 text-slate-400 text-sm">
            Evaluating active plans, discovering dependencies, detecting resource contention, and running scenario comparisons...
          </div>
        ) : (
          <>
            {activeTab === 'overview' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Knowledge Assurance Coordination Control Domain</h3>
                {data?.domains?.map((dom: any) => (
                  <div key={dom.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 flex justify-between items-center">
                    <div>
                      <span className="font-semibold text-purple-400">{dom.name}</span>
                      <p className="text-xs text-slate-400 mt-1">Owner: {dom.owner} | Version: {dom.version}</p>
                    </div>
                    <span className="text-xs px-3 py-1 rounded bg-purple-500/10 text-purple-400 border border-purple-500/20 font-semibold">{dom.status}</span>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'relationships' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Plan Dependencies & Relationships</h3>
                {data?.relationships?.map((r: any) => (
                  <div key={r.id} className="p-4 rounded-xl bg-slate-950/60 border border-purple-500/30 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-semibold text-purple-400">Plan '{r.source_plan_id}' → Plan '{r.target_plan_id}'</span>
                      <span className="text-xs px-2.5 py-1 rounded bg-purple-500/20 text-purple-300 font-semibold uppercase">{r.relationship_type}</span>
                    </div>
                    <p className="text-xs text-slate-300">{r.description}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'contentions' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Resource Contention Telemetry</h3>
                {data?.contentions?.map((c: any) => (
                  <div key={c.id} className="p-4 rounded-xl bg-amber-950/30 border border-amber-500/40 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-semibold text-amber-400">Resource ID: {c.resource_id}</span>
                      <span className="text-xs px-2.5 py-1 rounded bg-amber-500/20 text-amber-300 font-semibold uppercase">{c.severity} Severity</span>
                    </div>
                    <p className="text-xs text-slate-300">Competing Plans: {c.competing_plan_ids_json?.join(', ')}</p>
                    <p className="text-xs text-slate-400">Demand Deficit: {(c.demand_deficit * 100).toFixed(0)}% over capacity</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'bottlenecks' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Portfolio Bottlenecks</h3>
                {data?.bottlenecks?.map((b: any) => (
                  <div key={b.id} className="p-4 rounded-xl bg-rose-950/30 border border-rose-500/40 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-semibold text-rose-400">Bottleneck Type: {b.bottleneck_type}</span>
                      <span className="text-xs px-2.5 py-1 rounded bg-rose-500/20 text-rose-300 font-semibold uppercase">{b.severity}</span>
                    </div>
                    <p className="text-xs text-slate-300">{b.description}</p>
                    <p className="text-xs text-slate-400">Affected Plans: {b.affected_plan_ids_json?.join(', ')}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'recommendations' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Analytical Coordination Recommendations</h3>
                {data?.recommendations?.map((rec: any) => (
                  <div key={rec.id} className="p-4 rounded-xl bg-indigo-950/40 border border-indigo-500/40 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-xs px-3 py-1 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30 font-bold">
                        {rec.label}
                      </span>
                      <span className="text-xs text-indigo-300">Option: {rec.recommended_option}</span>
                    </div>
                    <p className="text-xs text-slate-200 mt-2">{rec.reason}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'query' && (
              <div className="space-y-6">
                <h3 className="text-base font-semibold text-slate-200">Natural Language Assurance Coordination Query</h3>
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={queryText}
                    onChange={(e) => setQueryText(e.target.value)}
                    placeholder="Ask about competing plans, evidence sharing, bottlenecks, or deadline collisions..."
                    className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-purple-500/50"
                  />
                  <button
                    onClick={handleQuery}
                    disabled={queryLoading}
                    className="px-5 py-2.5 bg-purple-500 hover:bg-purple-600 disabled:opacity-50 text-slate-950 text-xs font-semibold rounded-xl transition"
                  >
                    {queryLoading ? 'Processing...' : 'Run Query'}
                  </button>
                </div>

                {queryResult && (
                  <div className="p-5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-semibold text-purple-400">Coordination Intelligence Result</span>
                      <span className="text-xs text-slate-400">Confidence: {queryResult.confidencePct}%</span>
                    </div>
                    {queryResult.evidenceJson?.error ? (
                      <div className="text-xs text-rose-400 font-semibold">{queryResult.evidenceJson.error}</div>
                    ) : (
                      <div className="space-y-2 text-xs text-slate-300">
                        {queryResult.results?.map((r: any, idx: number) => (
                          <div key={idx} className="p-3 bg-slate-900 rounded-lg space-y-1">
                            <p><strong className="text-amber-400">Resource Contention:</strong> {r.competing_plans}</p>
                            <p><strong className="text-indigo-400">Evidence Sharing:</strong> {r.evidence_sharing}</p>
                            <p><strong className="text-rose-400">Portfolio Bottleneck:</strong> {r.bottlenecks}</p>
                            <p><strong className="text-purple-400">Deadline Collisions:</strong> {r.deadline_collisions}</p>
                            <p><strong className="text-teal-400">Baseline Comparison:</strong> {r.baseline_comparison}</p>
                            <p><strong className="text-cyan-400">Cross-Plan Cascades:</strong> {r.cross_plan_cascades}</p>
                            <p><strong className="text-amber-300 font-semibold">Governance Boundary:</strong> {r.recommendation_notice}</p>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
