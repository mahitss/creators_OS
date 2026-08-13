'use client';

import React, { useState, useEffect } from 'react';

export function TransformationResilienceKnowledgeAssuranceConflictsWorkspace() {
  const [activeTab, setActiveTab] = useState<
    | 'overview'
    | 'queue'
    | 'critical'
    | 'root_causes'
    | 'impacts'
    | 'options'
    | 'tradeoffs'
    | 'scenarios'
    | 'recommendations'
    | 'decision_packets'
    | 'resolution_plans'
    | 'residual_conflicts'
    | 'cascades'
    | 'clusters'
    | 'systemic'
    | 'drift'
    | 'escalations'
    | 'effectiveness'
    | 'patterns'
    | 'query'
  >('overview');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('Show critical assurance conflicts and root causes.');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/transformation-resilience-knowledge-assurance-conflicts');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      } else {
        // Fallback seed data
        setData({
          domainsCount: 1,
          conflictCasesCount: 1,
          criticalConflictsCount: 1,
          rootCausesCount: 1,
          optionsCount: 2,
          decisionPacketsCount: 1,
          resolutionPlansCount: 1,
          residualConflictsCount: 1,
          cascadesCount: 1,
          clustersCount: 1,
          systemicConflictsCount: 1,
          patternsCount: 1,
          domains: [
            { id: 'cfdom_01', name: 'Global Enterprise Knowledge Assurance Conflict Intelligence & Trade-Off Resolution 2.0', owner: 'Principal Enterprise Assurance Conflict Architect', status: 'active', version: 'v2.0' }
          ],
          cases: [
            { id: 'ccase_01', conflict_type: 'resource', severity: 'high', status: 'options_ready', owner: 'Principal Enterprise Assurance Conflict Architect', affected_plan_ids_json: ['aplan_01', 'aplan_hr_cloud_02'] }
          ],
          impacts: [
            { id: 'cimp_01', conflict_case_id: 'ccase_01', risk_exposure: 0.25, coverage_loss: 0.15, deadline_exposure_days: 7, severity: 'high' }
          ],
          rootCauses: [
            { id: 'rcause_01', conflict_case_id: 'ccase_01', root_cause_category: 'shared_resource', description: 'Simulation Cluster 01 is over-subscribed by 20% due to overlapping Q3 assurance validation timelines.', frequency: 3 }
          ],
          options: [
            { id: 'ropt_baseline_01', option_type: 'continue_without_change', title: 'Baseline Option: Continue Without Change', risk_score: 0.25, coverage_score: 0.84, deadline_shift_days: 0 },
            { id: 'ropt_sequence_01', option_type: 'sequence', title: 'Sequenced Execution Option (aplan_01 week 1, aplan_hr_cloud_02 week 2)', risk_score: 0.08, coverage_score: 0.92, deadline_shift_days: 3 }
          ],
          tradeoffs: [
            { id: 'trade_01', dimension_a: 'coverage', dimension_b: 'speed', tradeoff_description: 'Sequencing increases assurance coverage from 84% to 92% but delays HR Cloud validation by 3 days.' }
          ],
          scenarios: [
            { id: 'scen_base_01', scenario_type: 'continue_without_change', risk: 0.25, coverage: 0.84, residual_risk: 0.16 },
            { id: 'scen_seq_01', scenario_type: 'sequence', risk: 0.08, coverage: 0.92, residual_risk: 0.08 }
          ],
          recommendations: [
            { id: 'crec_01', label: 'ANALYTICAL RECOMMENDATION — NOT DECISION', recommended_option: 'sequence', reason: 'Sequencing simulation execution resolves 20% compute deficit while elevating coverage to 92%.' }
          ],
          decisionPackets: [
            { id: 'dpkt_01', summary: 'Multi-plan simulation compute conflict decision packet for Q3 cloud rollout.', required_authority: 'governance_authority', residual_risk: 0.08 }
          ],
          resolutionPlans: [
            { id: 'rplan_01', selected_option: 'sequence', owner: 'Principal Enterprise Assurance Conflict Architect', status: 'planned' }
          ],
          residualConflicts: [
            { id: 'resconf_01', remaining_conflict: 'Minor review window overlap on legacy SSO background sync.', owner: 'Cloud SLA Architect', impact: 'Low risk jitter on secondary SSO telemetry feed.' }
          ],
          cascades: [
            { id: 'casc_01', source_conflict_id: 'ccase_01', affected_conflict_id: 'ccase_secondary_02', depth: 2, severity: 'material' }
          ],
          clusters: [
            { id: 'clust_01', name: 'Cloud Infrastructure Interconnect Dependency Cluster', cluster_type: 'shared_dependency' }
          ],
          systemic: [
            { id: 'sysconf_01', pattern_description: 'Repeated simulation cluster compute bottlenecks across Q3 transformation waves.', severity: 'critical' }
          ],
          patterns: [
            { id: 'rpatt_01', name: 'Sequenced Simulation Workload Resolution Pattern', reusability_score: 0.92, confidence: 0.95 }
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
      const res = await fetch(`/api/v1/transformation-resilience-knowledge-assurance-conflicts/query?query=${encodeURIComponent(queryText)}`, {
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
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-rose-400 via-amber-400 to-teal-400">
              Assurance Conflict Intelligence & Governed Portfolio Balancing 2.0
            </h1>
            <span className="px-3 py-1 text-xs font-semibold rounded-full bg-rose-500/10 text-rose-400 border border-rose-500/20">
              Human-Authorized Conflict Resolution
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Transform cross-plan conflicts into explicit, explainable, governed resolution options with evidence-backed decision packets, baseline comparisons, trade-off analysis, and systemic pattern learning.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={fetchData}
            className="px-4 py-2 text-xs font-medium rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition"
          >
            Refresh Conflict Engine
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
          <p className="text-xs text-slate-400 font-medium">Conflict Cases</p>
          <p className="text-xl font-bold text-rose-400 mt-1">{data?.conflictCasesCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Critical Conflicts</p>
          <p className="text-xl font-bold text-red-500 mt-1">{data?.criticalConflictsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Resolution Options</p>
          <p className="text-xl font-bold text-amber-400 mt-1">{data?.optionsCount ?? 2}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Decision Packets</p>
          <p className="text-xl font-bold text-indigo-400 mt-1">{data?.decisionPacketsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Residual Conflicts</p>
          <p className="text-xl font-bold text-cyan-400 mt-1">{data?.residualConflictsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Systemic Clusters</p>
          <p className="text-xl font-bold text-purple-400 mt-1">{data?.systemicConflictsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Resolution Patterns</p>
          <p className="text-xl font-bold text-teal-400 mt-1">{data?.patternsCount ?? 1}</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 overflow-x-auto space-x-2 scrollbar-none">
        {[
          { id: 'overview', label: 'Conflict Overview' },
          { id: 'queue', label: 'Conflict Queue' },
          { id: 'critical', label: 'Critical Conflicts' },
          { id: 'root_causes', label: 'Root Cause Groupings' },
          { id: 'impacts', label: 'Conflict Impact Analysis' },
          { id: 'options', label: 'Resolution Options' },
          { id: 'tradeoffs', label: 'Trade-Off Comparison' },
          { id: 'scenarios', label: 'Scenario Simulations' },
          { id: 'recommendations', label: 'Analytical Recommendations' },
          { id: 'decision_packets', label: 'Decision Packets' },
          { id: 'resolution_plans', label: 'Resolution Plans' },
          { id: 'residual_conflicts', label: 'Residual Conflicts' },
          { id: 'cascades', label: 'Conflict Cascades' },
          { id: 'clusters', label: 'Conflict Clusters' },
          { id: 'systemic', label: 'Systemic Conflicts' },
          { id: 'drift', label: 'Conflict Drift' },
          { id: 'escalations', label: 'Escalations & SLA' },
          { id: 'effectiveness', label: 'Resolution Effectiveness' },
          { id: 'patterns', label: 'Resolution Patterns' },
          { id: 'query', label: 'Conflict Intelligence Query' }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-2.5 text-xs font-semibold whitespace-nowrap border-b-2 transition ${
              activeTab === tab.id
                ? 'border-rose-400 text-rose-400 bg-rose-500/5'
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
            Classifying conflict cases, analyzing root causes, calculating trade-offs, and preparing decision packets...
          </div>
        ) : (
          <>
            {activeTab === 'overview' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Conflict Intelligence Domain</h3>
                {data?.domains?.map((dom: any) => (
                  <div key={dom.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 flex justify-between items-center">
                    <div>
                      <span className="font-semibold text-rose-400">{dom.name}</span>
                      <p className="text-xs text-slate-400 mt-1">Owner: {dom.owner} | Version: {dom.version}</p>
                    </div>
                    <span className="text-xs px-3 py-1 rounded bg-rose-500/10 text-rose-400 border border-rose-500/20 font-semibold">{dom.status}</span>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'queue' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Conflict Cases Queue</h3>
                {data?.cases?.map((c: any) => (
                  <div key={c.id} className="p-4 rounded-xl bg-slate-950/60 border border-rose-500/30 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-semibold text-rose-400">Case ID: {c.id} ({c.conflict_type})</span>
                      <span className="text-xs px-2.5 py-1 rounded bg-rose-500/20 text-rose-300 font-semibold uppercase">{c.status}</span>
                    </div>
                    <p className="text-xs text-slate-300">Affected Plans: {c.affected_plan_ids_json?.join(', ')}</p>
                    <p className="text-xs text-slate-400">Owner: {c.owner}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'root_causes' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Root Cause Analysis & Groupings</h3>
                {data?.rootCauses?.map((rc: any) => (
                  <div key={rc.id} className="p-4 rounded-xl bg-slate-950/60 border border-amber-500/30 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-semibold text-amber-400">Category: {rc.root_cause_category}</span>
                      <span className="text-xs px-2.5 py-1 rounded bg-amber-500/20 text-amber-300 font-semibold">Freq: {rc.frequency}x</span>
                    </div>
                    <p className="text-xs text-slate-300">{rc.description}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'options' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Resolution Options (Baseline 'Continue Without Change' Included)</h3>
                {data?.options?.map((opt: any) => (
                  <div key={opt.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-semibold text-teal-400">{opt.title}</span>
                      <span className="text-xs px-2.5 py-1 rounded bg-teal-500/10 text-teal-300 font-semibold uppercase">{opt.option_type}</span>
                    </div>
                    <div className="grid grid-cols-3 gap-2 text-xs text-slate-400 mt-2">
                      <p>Risk Score: <strong className="text-slate-200">{(opt.risk_score * 100).toFixed(0)}%</strong></p>
                      <p>Coverage: <strong className="text-slate-200">{(opt.coverage_score * 100).toFixed(0)}%</strong></p>
                      <p>Deadline Shift: <strong className="text-slate-200">{opt.deadline_shift_days} days</strong></p>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'decision_packets' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Evidence-Backed Decision Packets</h3>
                {data?.decisionPackets?.map((dp: any) => (
                  <div key={dp.id} className="p-5 rounded-xl bg-indigo-950/40 border border-indigo-500/40 space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-semibold text-indigo-300">Decision Packet {dp.id}</span>
                      <span className="text-xs px-3 py-1 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30 font-semibold">
                        Authority Required: {dp.required_authority}
                      </span>
                    </div>
                    <p className="text-xs text-slate-200">{dp.summary}</p>
                    <p className="text-xs text-slate-400">Recommendation: {dp.recommendation} | Residual Risk: {(dp.residual_risk * 100).toFixed(0)}%</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'systemic' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Systemic Conflicts & Pattern Detection</h3>
                {data?.systemic?.map((sys: any) => (
                  <div key={sys.id} className="p-4 rounded-xl bg-rose-950/30 border border-rose-500/40 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-semibold text-rose-400">Systemic Pattern ({sys.severity})</span>
                    </div>
                    <p className="text-xs text-slate-300">{sys.pattern_description}</p>
                    <p className="text-xs text-slate-400">Affected Transformations: {sys.affected_transformations_json?.join(', ')}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'query' && (
              <div className="space-y-6">
                <h3 className="text-base font-semibold text-slate-200">Natural Language Assurance Conflict Query</h3>
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={queryText}
                    onChange={(e) => setQueryText(e.target.value)}
                    placeholder="Ask about critical conflicts, root causes, baseline options, or decision packets..."
                    className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-rose-500/50"
                  />
                  <button
                    onClick={handleQuery}
                    disabled={queryLoading}
                    className="px-5 py-2.5 bg-rose-500 hover:bg-rose-600 disabled:opacity-50 text-slate-950 text-xs font-semibold rounded-xl transition"
                  >
                    {queryLoading ? 'Processing...' : 'Run Query'}
                  </button>
                </div>

                {queryResult && (
                  <div className="p-5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-semibold text-rose-400">Conflict Intelligence Result</span>
                      <span className="text-xs text-slate-400">Confidence: {queryResult.confidencePct}%</span>
                    </div>
                    {queryResult.evidenceJson?.error ? (
                      <div className="text-xs text-rose-400 font-semibold">{queryResult.evidenceJson.error}</div>
                    ) : (
                      <div className="space-y-2 text-xs text-slate-300">
                        {queryResult.results?.map((r: any, idx: number) => (
                          <div key={idx} className="p-3 bg-slate-900 rounded-lg space-y-1">
                            <p><strong className="text-rose-400">Critical Conflicts:</strong> {r.critical_conflicts}</p>
                            <p><strong className="text-amber-400">Root Cause:</strong> {r.root_cause}</p>
                            <p><strong className="text-teal-400">Baseline Comparison:</strong> {r.baseline_option}</p>
                            <p><strong className="text-indigo-400">Trade-Off Analysis:</strong> {r.tradeoffs}</p>
                            <p><strong className="text-amber-300 font-semibold">Governance Notice:</strong> {r.recommendation_notice}</p>
                            <p><strong className="text-cyan-400">Residual Conflicts:</strong> {r.residual_conflicts}</p>
                            <p><strong className="text-purple-400">Systemic Conflicts:</strong> {r.systemic_conflicts}</p>
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
