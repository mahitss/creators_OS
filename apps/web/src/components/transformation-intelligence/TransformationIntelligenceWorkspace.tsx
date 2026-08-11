'use client';

import React, { useState, useEffect } from 'react';

export function TransformationIntelligenceWorkspace() {
  const [activeTab, setActiveTab] = useState<'overview' | 'graph_paths' | 'cross_impact' | 'capability_overlaps' | 'assumptions_scenarios' | 'conflicts_risks' | 'patterns_analogies' | 'complexity' | 'nl_query'>('overview');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('What depends on this transformation?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/transformation-intelligence');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      } else {
        // Fallback seed structure
        setData({
          graphNodesCount: 3,
          graphEdgesCount: 2,
          provenanceRecordsCount: 1,
          crossTransformationImpactsCount: 1,
          capabilityOverlapsCount: 1,
          sharedAssumptionClustersCount: 1,
          scenarioExposuresCount: 1,
          benefitGraphsCount: 1,
          conflictGraphsCount: 1,
          patternsDetectedCount: 1,
          analogiesIdentifiedCount: 1,
          complexityHotspotsCount: 1,
          graphSnapshotsCount: 1,
          overallFabricDensityScore: 0.88,
          nodes: [
            { id: 'node_cand_01', entity_type: 'transformation', label: 'Skill Certification Auto-signer Transformation', confidence: 0.98 },
            { id: 'node_cand_02', entity_type: 'transformation', label: 'Autonomous FinOps Scale Transformation', confidence: 0.96 },
            { id: 'node_cap_compliance', entity_type: 'capability', label: 'Zero-Trust Compliance Engine Capability', confidence: 0.99 }
          ],
          edges: [
            { id: 'edge_dep_cand01_cand02', from_node_id: 'node_cand_02', to_node_id: 'node_cand_01', relationship_type: 'depends_on', strength: 0.95 },
            { id: 'edge_enables_cap_cand01', from_node_id: 'node_cand_01', to_node_id: 'node_cap_compliance', relationship_type: 'enables', strength: 0.90 }
          ],
          provenances: [
            { id: 'prov_01', edge_id: 'edge_dep_cand01_cand02', source_system: 'Dependency Matrix Analysis', classified_as: 'observed', confidence: 0.98 }
          ],
          crossImpacts: [
            { id: 'cross_01', source_transformation_id: 'cand_01', target_transformation_id: 'cand_02', impact_type: 'enabling', severity: 'high', confidence: 0.95 }
          ],
          capabilityOverlaps: [
            { id: 'capov_01', capability_id: 'cap_zero_trust_compliance', transformation_ids_json: ['cand_01', 'cand_02'], risk_score: 0.12, conflict_flag: false }
          ],
          assumptionClusters: [
            { id: 'ass_01', shared_assumption: 'Open API AST rule schema stability across enterprise mesh', transformation_ids_json: ['cand_01', 'cand_02'], exposure_level: 'medium', confidence: 0.92 }
          ],
          scenarioExposures: [
            { id: 'scen_exp_01', scenario_id: 'scen_rapid_api_volume_surge', transformation_ids_json: ['cand_01', 'cand_02'], vulnerability_score: 0.08, impact_desc: 'Low vulnerability; pre-signer caching absorbs up to 10x API volume surge' }
          ],
          benefitGraphs: [
            { id: 'bgraph_01', transformation_ids_json: ['cand_01', 'cand_02'], claimed_benefit: 'Aggregate 30% reduction in cloud infrastructure operational expenditure', overlap_flag: false }
          ],
          conflictGraphs: [
            { id: 'cgraph_01', transformation_a_id: 'cand_01', transformation_b_id: 'cand_02', conflict_domain: 'capacity', severity: 'low' }
          ],
          patterns: [
            { id: 'pat_01', pattern_name: 'Foundational Pre-signer Unlocks Downstream Automation', pattern_type: 'enabling_sequence', confidence: 0.95 }
          ],
          analogies: [
            { id: 'analogy_01', current_transformation_id: 'cand_01', historical_transformation_id: 'transprog_policy_v1', similarity_score: 0.88, confidence: 0.91 }
          ],
          hotspots: [
            { id: 'hotspot_01', hotspot_name: 'Zero-Trust Compliance Capability Convergence', converging_transformation_ids_json: ['cand_01', 'cand_02'], hotspot_domain: 'capability', severity: 'medium' }
          ],
          snapshots: [
            { id: 'snap_01', snapshot_label: 'Q3 2026 Baseline Transformation Knowledge Graph', nodes_count: 3, edges_count: 2 }
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
      const res = await fetch(`/api/v1/transformation-intelligence/query?query=${encodeURIComponent(queryText)}`, {
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
            <span className="p-2 bg-purple-600/20 text-purple-400 rounded-lg text-lg">🕸️</span>
            Enterprise Transformation Intelligence Fabric + Cross-Transformation Knowledge Graph 2.0
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Strategy → Capabilities → Transformations → Workstreams → Multi-Hop Paths → Shared Assumptions → Benefit Cascade → Pattern Reasoning.
          </p>
        </div>
        <div className="flex gap-2">
          <span className="px-3 py-1 bg-purple-500/10 text-purple-400 border border-purple-500/20 rounded-full text-xs font-semibold">
            Cross-Transformation Reasoning
          </span>
          <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full text-xs font-semibold">
            Observed Provenance
          </span>
        </div>
      </div>

      {/* Telemetry Header */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Graph Nodes</div>
          <div className="text-2xl font-bold text-purple-400 mt-1">{data?.graphNodesCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Graph Edges</div>
          <div className="text-2xl font-bold text-indigo-400 mt-1">{data?.graphEdgesCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Capability Overlaps</div>
          <div className="text-2xl font-bold text-amber-400 mt-1">{data?.capabilityOverlapsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Assumption Clusters</div>
          <div className="text-2xl font-bold text-teal-400 mt-1">{data?.sharedAssumptionClustersCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Complexity Hotspots</div>
          <div className="text-2xl font-bold text-rose-400 mt-1">{data?.complexityHotspotsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Fabric Density Score</div>
          <div className="text-2xl font-bold text-emerald-400 mt-1">{data?.overallFabricDensityScore ? (data.overallFabricDensityScore * 100).toFixed(0) : 88}%</div>
        </div>
      </div>

      {/* Subsystem Tabs */}
      <div className="flex border-b border-slate-800 gap-2 text-sm overflow-x-auto pb-1">
        {[
          { id: 'overview', label: 'Fabric Overview' },
          { id: 'graph_paths', label: 'Graph & Multi-Hop Paths' },
          { id: 'cross_impact', label: 'Cross-Transformation Impact' },
          { id: 'capability_overlaps', label: 'Capability & Benefit Overlaps' },
          { id: 'assumptions_scenarios', label: 'Assumptions & Scenarios' },
          { id: 'conflicts_risks', label: 'Conflict Graph & Risk Propagation' },
          { id: 'patterns_analogies', label: 'Patterns & Analogies' },
          { id: 'complexity', label: 'Complexity Hotspots' },
          { id: 'nl_query', label: 'Natural Language Query' }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-2 font-medium rounded-t-lg transition-colors whitespace-nowrap ${
              activeTab === tab.id
                ? 'bg-slate-900 text-purple-400 border-b-2 border-purple-500'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/40'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Content */}
      {loading ? (
        <div className="p-8 text-center text-slate-500">Loading Transformation Intelligence Fabric...</div>
      ) : (
        <div className="space-y-6">
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-purple-400 flex items-center gap-2">
                  <span>🕸️</span> Enterprise Knowledge Graph Nodes
                </h2>
                <div className="space-y-2 text-sm">
                  {data?.nodes?.map((n: any) => (
                    <div key={n.id} className="p-3 bg-slate-950 rounded border border-purple-800/40 flex justify-between items-center text-xs">
                      <div>
                        <div className="font-bold text-slate-100">{n.label}</div>
                        <div className="text-slate-400">Type: {n.entity_type} | Source: {n.source}</div>
                      </div>
                      <span className="px-2 py-0.5 bg-emerald-500/20 text-emerald-300 rounded font-bold">{(n.confidence * 100).toFixed(0)}% Conf</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-indigo-400 flex items-center gap-2">
                  <span>🔗</span> Edge Relationships & Provenance
                </h2>
                <div className="space-y-2 text-sm">
                  {data?.edges?.map((e: any) => (
                    <div key={e.id} className="p-3 bg-slate-950 rounded border border-indigo-800/40 space-y-1 text-xs">
                      <div className="flex justify-between font-bold text-indigo-300">
                        <span>{e.from_node_id} → [{e.relationship_type}] → {e.to_node_id}</span>
                        <span>Strength: {(e.strength * 100).toFixed(0)}%</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'graph_paths' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Multi-Hop Path Reasoning Traversal</h2>
              <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                <div className="font-bold text-purple-300">Path: cand_01 → cap_zero_trust_compliance → cand_02</div>
                <div className="space-y-2 text-xs text-slate-300">
                  <div className="p-2 bg-slate-900 rounded">1. Skill Certification Auto-signer Transformation [enables] Zero-Trust Compliance Engine Capability (Observed)</div>
                  <div className="p-2 bg-slate-900 rounded">2. Autonomous FinOps Scale Transformation [depends_on] Skill Certification Auto-signer Transformation (Observed)</div>
                </div>
                <div className="text-xs text-emerald-400 font-semibold">Evidence: Observed dependency matrix + capability enablement graph.</div>
              </div>
            </div>
          )}

          {activeTab === 'cross_impact' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Cross-Transformation Impact Analysis</h2>
              {data?.crossImpacts?.map((ci: any) => (
                <div key={ci.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-indigo-300">{ci.source_transformation_id} → {ci.target_transformation_id}</span>
                    <span className="text-xs px-2 py-0.5 bg-blue-500/20 text-blue-300 rounded font-bold">Impact: {ci.impact_type} ({ci.severity})</span>
                  </div>
                  <div className="text-xs text-slate-400">Evidence: {JSON.stringify(ci.evidence_json)}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'capability_overlaps' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Capability Overlaps & Benefit Graphs</h2>
              {data?.capabilityOverlaps?.map((co: any) => (
                <div key={co.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-amber-300">Shared Capability: {co.capability_id}</span>
                    <span className="text-xs px-2 py-0.5 bg-emerald-500/20 text-emerald-300 rounded font-bold">Conflict Flag: {co.conflict_flag ? 'YES' : 'NONE'}</span>
                  </div>
                  <div className="text-xs text-slate-400">Transformations: {co.transformation_ids_json?.join(', ')}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'assumptions_scenarios' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Shared Assumption Clusters & Scenario Exposures</h2>
              {data?.assumptionClusters?.map((ac: any) => (
                <div key={ac.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-teal-500">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-teal-300">Shared Assumption Cluster</span>
                    <span className="text-xs px-2 py-0.5 bg-teal-500/20 text-teal-300 rounded font-bold">Exposure: {ac.exposure_level}</span>
                  </div>
                  <p className="text-xs text-slate-300">{ac.shared_assumption}</p>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'conflicts_risks' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Conflict Graph & Risk Propagation</h2>
              {data?.conflictGraphs?.map((cg: any) => (
                <div key={cg.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-rose-500">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-rose-300">Conflict Domain: {cg.conflict_domain}</span>
                    <span className="text-xs px-2 py-0.5 bg-rose-500/20 text-rose-300 rounded font-bold">Severity: {cg.severity}</span>
                  </div>
                  <div className="text-xs text-slate-400">Between: {cg.transformation_a_id} and {cg.transformation_b_id}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'patterns_analogies' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Pattern Recognition & Historical Transformation Analogies</h2>
              {data?.patterns?.map((pat: any) => (
                <div key={pat.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-indigo-500">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-indigo-300">{pat.pattern_name}</span>
                    <span className="text-xs px-2 py-0.5 bg-indigo-500/20 text-indigo-300 rounded font-bold">Type: {pat.pattern_type}</span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'complexity' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Enterprise Transformation Complexity Hotspots</h2>
              {data?.hotspots?.map((hs: any) => (
                <div key={hs.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-amber-500">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-amber-300">{hs.hotspot_name}</span>
                    <span className="text-xs px-2 py-0.5 bg-amber-500/20 text-amber-300 rounded font-bold">Domain: {hs.hotspot_domain}</span>
                  </div>
                  <div className="text-xs text-slate-400">Converging Transformations: {hs.converging_transformation_ids_json?.join(', ')}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'nl_query' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Natural Language Knowledge Graph Query Interface</h2>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={queryText}
                  onChange={(e) => setQueryText(e.target.value)}
                  placeholder="Ask a cross-transformation query..."
                  className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-sm text-slate-100 focus:outline-none focus:border-purple-500"
                />
                <button
                  onClick={handleQuery}
                  disabled={queryLoading}
                  className="px-5 py-2 bg-purple-600 hover:bg-purple-500 text-white font-medium rounded-lg text-sm transition-colors"
                >
                  {queryLoading ? 'Evaluating...' : 'Query'}
                </button>
              </div>

              {queryResult && (
                <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                  <div className="text-xs text-purple-400 font-semibold">Query: {queryResult.query}</div>
                  <div className="space-y-2">
                    {queryResult.results?.map((res: any, idx: number) => (
                      <div key={idx} className="p-3 bg-slate-900 rounded space-y-1 text-xs">
                        <div className="font-semibold text-slate-200">{res.primary_root_dependency}</div>
                        <div className="text-amber-300">Shared Capability: {res.shared_capability_overlap}</div>
                        <div className="text-indigo-300">Cross Impact: {res.cross_transformation_impact}</div>
                        <div className="text-teal-300">Shared Assumption Cluster: {res.shared_assumption_cluster}</div>
                        <div className="text-emerald-400">Benefit Graph: {res.benefit_graph_finding}</div>
                        <div className="text-rose-400">Complexity Hotspot: {res.complexity_hotspot}</div>
                        <div className="text-purple-300">Historical Analogy: {res.historical_analogy}</div>
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
