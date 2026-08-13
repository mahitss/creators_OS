'use client';

import React, { useState, useEffect } from 'react';

export function TransformationResilienceCrossDomainWorkspace() {
  const [activeTab, setActiveTab] = useState<
    | 'overview'
    | 'graph'
    | 'exposures'
    | 'propagation'
    | 'compound'
    | 'fragility'
    | 'gaps'
    | 'breakpoints'
    | 'second_order'
    | 'collisions'
    | 'warnings'
    | 'query'
  >('overview');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('Which risks compound across Cloud Transformation Wave 3 and HR Cloud Wave 4?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/transformation-resilience-cross-domain');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      } else {
        // Fallback seed data
        setData({
          domainsCount: 1,
          nodesCount: 5,
          edgesCount: 3,
          propagationsCount: 1,
          systemicExposuresCount: 1,
          compoundRisksCount: 1,
          cascadeProjectionsCount: 1,
          cascadeBreakpointsCount: 1,
          secondOrderEffectsCount: 1,
          interventionCollisionsCount: 1,
          systemicWarningsCount: 1,
          domains: [
            { id: 'xdom_01', name: 'Global Enterprise Cross-Domain Resilience Intelligence Fabric 2.0', owner: 'Principal Enterprise Cross-Domain Resilience Architect', status: 'active', version: 'v2.0' }
          ],
          resilienceGraphs: [
            { id: 'rgraph_01', total_nodes_count: 12, total_edges_count: 18, status: 'active' }
          ],
          nodes: [
            { id: 'gnode_dep_01', node_type: 'dependency', node_id: 'dep_compute_cluster_01', domain: 'Infrastructure & Compute', severity: 'critical', confidence: 0.98 },
            { id: 'gnode_plan_01', node_type: 'plan', node_id: 'aplan_01', domain: 'Cloud Transformation Wave 3', severity: 'high', confidence: 0.95 },
            { id: 'gnode_plan_02', node_type: 'plan', node_id: 'aplan_hr_cloud_02', domain: 'HR Cloud Wave 4', severity: 'high', confidence: 0.95 },
            { id: 'gnode_risk_01', node_type: 'risk', node_id: 'emrisk_01', domain: 'Assurance Foresight', severity: 'high', confidence: 0.95 },
            { id: 'gnode_interv_01', node_type: 'intervention', node_id: 'icase_01', domain: 'Intervention Orchestration', severity: 'high', confidence: 0.95 }
          ],
          edges: [
            { id: 'gedge_01', source_node_id: 'gnode_plan_01', target_node_id: 'gnode_dep_01', relationship: 'depends_on', confidence: 0.98, evidence_count: 3 },
            { id: 'gedge_02', source_node_id: 'gnode_plan_02', target_node_id: 'gnode_dep_01', relationship: 'depends_on', confidence: 0.98, evidence_count: 3 },
            { id: 'gedge_03', source_node_id: 'gnode_risk_01', target_node_id: 'gnode_dep_01', relationship: 'affects', confidence: 0.95, evidence_count: 2 }
          ],
          propagationPaths: [
            { id: 'ppath_01', source: 'dep_compute_cluster_01', target: 'aplan_hr_cloud_02', depth: 3, severity: 'high', confidence: 0.95 }
          ],
          propagations: [
            { id: 'prop_01', source_condition: 'Gradual 15% compute cluster queue depth compression', propagation_type: 'dependency', estimated_impact: 'Causes 7-day schedule shift across HR Cloud wave deployment.', confidence: 0.95 }
          ],
          systemicExposures: [
            { id: 'sysexp_01', title: 'Systemic Compute Capacity & Wave Deployment Exposure', severity: 'critical', exposure_state: 'elevated', confidence: 0.95 }
          ],
          singlePointExposures: [
            { id: 'spexp_01', component_type: 'shared dependency', component_id: 'dep_compute_cluster_01', severity: 'high', affected_systems_json: ['Cloud Transformation Wave 3', 'HR Cloud Wave 4', 'ERP Wave 5'] }
          ],
          fragilities: [
            { id: 'frag_01', object_id: 'dep_compute_cluster_01', alternative_paths_count: 1, confidence: 0.90 }
          ],
          redundancies: [
            { id: 'red_01', object_id: 'dep_compute_cluster_01' }
          ],
          resilienceGaps: [
            { id: 'rgap_01', gap_type: 'single_dependency', description: 'Lack of automated secondary cloud cluster failover for Wave 4 simulation runs.', severity: 'high', recommended_mitigation: 'Configure auto-scaling secondary cluster reserve.' }
          ],
          compoundRisks: [
            { id: 'crisk_01', title: 'Compound Compute Deficit & Governance Deadline Pressure Risk', severity: 'critical', confidence: 0.92, contributing_conditions_json: ['Moderate evidence staleness on queue depth (5%)', 'Moderate deadline compression on Governance Board sign-off (5 days remaining)', 'Shared compute cluster dependency concentration (85%)'] }
          ],
          cascadeProjections: [
            { id: 'casc_01', source_id: 'dep_compute_cluster_01', depth: 3, severity: 'critical', confidence: 0.90 }
          ],
          cascadeBreakpoints: [
            { id: 'cbreak_01', cascade_id: 'casc_01', location_node_id: 'gnode_plan_01', option_type: 'resequence', expected_effect: 'Staggers simulation runs by 7 days, eliminating 90% of downstream compute queue compression.', confidence: 0.90 }
          ],
          secondOrderEffects: [
            { id: 'soeff_01', intervention_id: 'icase_01', affected_object_id: 'aplan_hr_cloud_02', effect_description: 'Preemptive resequencing reduces compute bottleneck risk but shifts simulation batch into HR Cloud testing window.', direction: 'capacity_pressure_increased', confidence: 0.90 }
          ],
          interventionCollisions: [
            { id: 'icoll_01', intervention_a_id: 'icase_01', intervention_b_id: 'icase_hr_02', collision_type: 'compete', resolution: 'Stagger testing windows by 48 hours to eliminate capacity overlap.' }
          ],
          systemicWarnings: [
            { id: 'swarn_01', trigger_reason: 'Systemic risk exposure detected: shared compute cluster dependency compression affecting Wave 3 and Wave 4.', status: 'open', severity: 'critical', evidence_count: 4 }
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
      const res = await fetch(`/api/v1/transformation-resilience-cross-domain/query?query=${encodeURIComponent(queryText)}`, {
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
    <div className="p-6 space-y-6 max-w-[1700px] mx-auto text-slate-100 font-sans">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-slate-900/90 p-6 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 via-teal-400 to-indigo-400">
              Cross-Domain Assurance Intelligence Fabric 2.0
            </h1>
            <span className="px-3 py-1 text-xs font-bold rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
              Unified Resilience Graph & Systemic Risk Propagation
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Detect when individually manageable conditions combine into systemic enterprise resilience problems: explained multi-node relationships, propagation paths, compound risks, cascade breakpoints, and second-order effect intelligence.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={fetchData}
            className="px-4 py-2 text-xs font-semibold rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition"
          >
            Refresh Resilience Graph
          </button>
        </div>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-3">
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Domain Status</p>
          <p className="text-lg font-bold text-cyan-400 mt-0.5">Active</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Graph Nodes</p>
          <p className="text-lg font-bold text-teal-400 mt-0.5">{data?.nodesCount ?? 12}</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Graph Edges</p>
          <p className="text-lg font-bold text-indigo-400 mt-0.5">{data?.edgesCount ?? 18}</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Systemic Exposures</p>
          <p className="text-lg font-bold text-rose-400 mt-0.5">{data?.systemicExposuresCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Compound Risks</p>
          <p className="text-lg font-bold text-amber-400 mt-0.5">{data?.compoundRisksCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Single Points</p>
          <p className="text-lg font-bold text-yellow-400 mt-0.5">{data?.singlePointExposures?.length ?? 1}</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Cascade Breakpoints</p>
          <p className="text-lg font-bold text-emerald-400 mt-0.5">{data?.cascadeBreakpointsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Collisions</p>
          <p className="text-lg font-bold text-purple-400 mt-0.5">{data?.interventionCollisionsCount ?? 1}</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 overflow-x-auto space-x-2 scrollbar-none">
        {[
          { id: 'overview', label: 'Cross-Domain Overview' },
          { id: 'graph', label: 'Unified Resilience Graph' },
          { id: 'exposures', label: 'Systemic Exposures' },
          { id: 'propagation', label: 'Propagation Paths' },
          { id: 'compound', label: 'Compound Risks (Visible Factors)' },
          { id: 'fragility', label: 'Component Fragility & Redundancy' },
          { id: 'gaps', label: 'Resilience Gaps' },
          { id: 'breakpoints', label: 'Cascade Breakpoints' },
          { id: 'second_order', label: 'Second-Order Effects' },
          { id: 'collisions', label: 'Intervention Collisions' },
          { id: 'warnings', label: 'Systemic Warnings' },
          { id: 'query', label: 'Cross-Domain Query' }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-2.5 text-xs font-semibold whitespace-nowrap border-b-2 transition ${
              activeTab === tab.id
                ? 'border-cyan-400 text-cyan-400 bg-cyan-500/5'
                : 'border-transparent text-slate-400 hover:text-slate-200 hover:border-slate-700'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 min-h-[420px]">
        {loading ? (
          <div className="flex items-center justify-center h-64 text-slate-400 text-sm">
            Traversing cross-domain resilience graph, calculating propagation paths, and identifying compound risk conditions...
          </div>
        ) : (
          <>
            {activeTab === 'overview' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Cross-Domain Intelligence Domain</h3>
                {data?.domains?.map((dom: any) => (
                  <div key={dom.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 flex justify-between items-center">
                    <div>
                      <span className="font-semibold text-cyan-400">{dom.name}</span>
                      <p className="text-xs text-slate-400 mt-1">Owner: {dom.owner} | Version: {dom.version}</p>
                    </div>
                    <span className="text-xs px-3 py-1 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 font-semibold">{dom.status}</span>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'graph' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Unified Resilience Graph Nodes & Edges</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <h4 className="text-xs font-bold text-cyan-400 uppercase">Graph Nodes</h4>
                    {data?.nodes?.map((n: any) => (
                      <div key={n.id} className="p-3 rounded-xl bg-slate-950/70 border border-slate-800 space-y-1">
                        <div className="flex justify-between items-center">
                          <span className="text-xs font-bold text-teal-300">{n.node_id}</span>
                          <span className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-300 uppercase">{n.node_type}</span>
                        </div>
                        <p className="text-[11px] text-slate-400">Domain: {n.domain} | Severity: {n.severity} | Confidence: {n.confidence}</p>
                      </div>
                    ))}
                  </div>

                  <div className="space-y-2">
                    <h4 className="text-xs font-bold text-indigo-400 uppercase">Graph Edges (Explained Relationships)</h4>
                    {data?.edges?.map((e: any) => (
                      <div key={e.id} className="p-3 rounded-xl bg-slate-950/70 border border-indigo-500/30 space-y-1">
                        <div className="flex justify-between items-center">
                          <span className="text-xs font-bold text-indigo-300">{e.source_node_id} → {e.target_node_id}</span>
                          <span className="text-[10px] px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 font-semibold uppercase">{e.relationship}</span>
                        </div>
                        <p className="text-[11px] text-slate-400">Confidence: {e.confidence} | Evidence Count: {e.evidence_count}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'exposures' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Systemic Exposures & Single-Point Dependencies</h3>
                {data?.systemicExposures?.map((exp: any) => (
                  <div key={exp.id} className="p-4 rounded-xl bg-slate-950/60 border border-rose-500/30 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-bold text-rose-400">{exp.title}</span>
                      <span className="text-xs px-2.5 py-1 rounded bg-rose-500/20 text-rose-300 font-semibold uppercase">Severity: {exp.severity}</span>
                    </div>
                    <p className="text-xs text-slate-300">Exposure State: <strong>{exp.exposure_state}</strong> | Confidence: {(exp.confidence * 100).toFixed(0)}%</p>
                  </div>
                ))}

                {data?.singlePointExposures?.map((sp: any) => (
                  <div key={sp.id} className="p-3.5 rounded-xl bg-slate-950/60 border border-amber-500/30 space-y-1">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-bold text-amber-300">Single Point: {sp.component_id}</span>
                      <span className="text-[10px] px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 font-semibold">{sp.component_type}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'compound' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Compound Risks (Visible Contributing Factors)</h3>
                {data?.compoundRisks?.map((cr: any) => (
                  <div key={cr.id} className="p-4 rounded-xl bg-slate-950/70 border border-amber-500/40 space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-bold text-amber-300">{cr.title}</span>
                      <span className="text-xs px-2.5 py-1 rounded bg-amber-500/20 text-amber-300 font-semibold uppercase">{cr.severity}</span>
                    </div>
                    <div className="space-y-1">
                      <p className="text-xs text-slate-400 font-semibold">Contributing Factors (Fully Transparent):</p>
                      {cr.contributing_conditions_json?.map((cond: string, idx: number) => (
                        <p key={idx} className="text-xs text-slate-300 bg-slate-900 px-3 py-1.5 rounded border border-slate-800">
                          • {cond}
                        </p>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'breakpoints' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Cascade Breakpoints & Intervention Points</h3>
                {data?.cascadeBreakpoints?.map((cb: any) => (
                  <div key={cb.id} className="p-4 rounded-xl bg-slate-950/60 border border-emerald-500/30 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-bold text-emerald-400">Breakpoint Node: {cb.location_node_id}</span>
                      <span className="text-xs px-2.5 py-1 rounded bg-emerald-500/20 text-emerald-300 font-semibold uppercase">Option: {cb.option_type}</span>
                    </div>
                    <p className="text-xs text-slate-300">{cb.expected_effect}</p>
                    <p className="text-[11px] text-slate-400">Cost: {cb.cost} | Reversibility: {cb.reversibility}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'collisions' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Intervention Collisions & Conflicts</h3>
                {data?.interventionCollisions?.map((ic: any) => (
                  <div key={ic.id} className="p-4 rounded-xl bg-slate-950/60 border border-purple-500/30 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-bold text-purple-300">{ic.intervention_a_id} ⚡ {ic.intervention_b_id}</span>
                      <span className="text-xs px-2.5 py-1 rounded bg-purple-500/20 text-purple-300 font-semibold uppercase">{ic.collision_type}</span>
                    </div>
                    <p className="text-xs text-slate-300">Resolution: {ic.resolution}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'query' && (
              <div className="space-y-6">
                <h3 className="text-base font-semibold text-slate-200">Cross-Domain Intelligence Natural Language Query</h3>
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={queryText}
                    onChange={(e) => setQueryText(e.target.value)}
                    placeholder="Ask about connected risks, single point exposures, compound conditions, or cascade breakpoints..."
                    className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-500/50"
                  />
                  <button
                    onClick={handleQuery}
                    disabled={queryLoading}
                    className="px-5 py-2.5 bg-cyan-500 hover:bg-cyan-600 disabled:opacity-50 text-slate-950 text-xs font-bold rounded-xl transition"
                  >
                    {queryLoading ? 'Processing...' : 'Run Query'}
                  </button>
                </div>

                {queryResult && (
                  <div className="p-5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-semibold text-cyan-400">Cross-Domain Intelligence Result</span>
                      <span className="text-xs text-slate-400">Confidence: {queryResult.confidencePct}%</span>
                    </div>
                    {queryResult.evidenceJson?.error ? (
                      <div className="text-xs text-rose-400 font-semibold">{queryResult.evidenceJson.error}</div>
                    ) : (
                      <div className="space-y-2 text-xs text-slate-300">
                        {queryResult.results?.map((r: any, idx: number) => (
                          <div key={idx} className="p-3 bg-slate-900 rounded-lg space-y-1">
                            <p><strong className="text-cyan-400">Connected Systems:</strong> {r.connected_systems}</p>
                            <p><strong className="text-rose-400">Single Point Exposures:</strong> {r.single_point_exposures}</p>
                            <p><strong className="text-indigo-400">Propagation Path:</strong> {r.propagation_path}</p>
                            <p><strong className="text-amber-400">Compound Risks:</strong> {r.compound_risks}</p>
                            <p><strong className="text-emerald-400">Cascade Breakpoints:</strong> {r.cascade_breakpoints}</p>
                            <p><strong className="text-teal-400">Second-Order Effects:</strong> {r.second_order_effects}</p>
                            <p><strong className="text-purple-400">Intervention Collisions:</strong> {r.intervention_collisions}</p>
                            <p><strong className="text-cyan-300 font-semibold">Governance Notice:</strong> {r.recommendation_notice}</p>
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
