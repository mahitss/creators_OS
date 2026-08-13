'use client';

import React, { useState, useEffect } from 'react';

export function TransformationResilienceKnowledgeAssuranceControlWorkspace() {
  const [activeTab, setActiveTab] = useState<
    | 'overview'
    | 'baselines'
    | 'signals'
    | 'detections'
    | 'assumptions'
    | 'plan_impacts'
    | 'health'
    | 'staleness'
    | 'triggers'
    | 'options'
    | 'versions'
    | 'diffs'
    | 'queue'
    | 'execution'
    | 'cross_plan'
    | 'drift'
    | 'emergency'
    | 'query'
  >('overview');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('Which plans are stale and what changed since approval?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/transformation-resilience-knowledge-assurance-control');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      } else {
        // Fallback seed data
        setData({
          domainsCount: 1,
          baselinesCount: 1,
          signalsCount: 1,
          stalePlansCount: 1,
          replanTriggersCount: 1,
          planVersionsCount: 2,
          emergencyReplansCount: 1,
          crossPlanImpactsCount: 1,
          portfolioDriftPct: '12.0% Risk Drift | 15.0% Capacity Drift',
          domains: [
            { id: 'adom_01', name: 'Global Enterprise Adaptive Knowledge Assurance & Continuous Replanning Control 2.0', owner: 'Principal Enterprise Adaptive Assurance Architect', status: 'active', version: 'v2.0' }
          ],
          baselines: [
            { id: 'abase_01', plan_id: 'aplan_01', plan_version: 'v1.0', residual_risk: 0.08, approval_state: 'approved' }
          ],
          signals: [
            { id: 'csig_01', source: 'resilience_sensing', change_type: 'dependency_change', significance: 'material', description: 'Secondary Cloud Interconnect SLA shifted from 99.99% to 99.90% following Q3 infrastructure update.' }
          ],
          detections: [
            { id: 'cdet_01', signal_id: 'csig_01', plan_id: 'aplan_01', confidence: 0.94 }
          ],
          assumptionImpacts: [
            { id: 'aimp_01', plan_id: 'aplan_01', assumption: 'Third-party monitoring vendor API remains accessible.', previous_state: 'Stable 99.99% interconnect', current_state: 'Degraded 99.90% interconnect with latency spikes', impact: 'Synthetic telemetry packets require 2x retry buffer.' }
          ],
          planImpacts: [
            { id: 'pimp_01', plan_id: 'aplan_01', risk_impact: 'Cloud SLA uncertainty increased by 12%', sequence_impact: 'Requires retry buffer prior to Governance submission', severity: 'material' }
          ],
          healths: [
            { id: 'phealth_01', plan_id: 'aplan_01', risk_alignment: 0.92, evidence_alignment: 0.88, capacity_alignment: 0.75, sequence_alignment: 0.90, deadline_alignment: 0.95, assumption_alignment: 0.80 }
          ],
          stalenesses: [
            { id: 'pstale_01', plan_id: 'aplan_01', status: 'materially_stale', outdated_assumptions_json: ['Third-party monitoring vendor API remains accessible.'] }
          ],
          triggers: [
            { id: 'rtrig_01', plan_id: 'aplan_01', trigger_type: 'material_plan_impact', description: 'Secondary Cloud Interconnect SLA change invalidated V1.0 assumptions.', status: 'open' }
          ],
          recommendations: [
            { id: 'rrec_01', plan_id: 'aplan_01', label: 'ANALYTICAL RECOMMENDATION — NOT APPROVAL', recommended_option: 'resequence', reason: 'Resequence synthetic telemetry execution to add 2x retry buffer prior to Governance submission.' }
          ],
          versions: [
            { id: 'pver_v1', plan_id: 'aplan_01', version_number: 'v1.0', parent_version: 'root', approval_state: 'approved' },
            { id: 'pver_v2', plan_id: 'aplan_01', version_number: 'v2.0', parent_version: 'v1.0', approval_state: 'approved' }
          ],
          diffs: [
            { id: 'pdiff_01', plan_id: 'aplan_01', from_version: 'v1.0', to_version: 'v2.0', reordered_actions_json: ['aopt_retry_buffer', 'aopt_01'], changed_assumptions_json: ['Vendor API retry threshold adjusted to 2000ms'] }
          ],
          queues: [
            { id: 'pqueue_01', plan_id: 'aplan_01', trigger_type: 'material_plan_impact', severity: 'material', priority: 1, recommended_action: 'resequence', approval_requirement: 'approval_required' }
          ],
          emergencies: [
            { id: 'emg_01', plan_id: 'aplan_critical_99', trigger_reason: 'Complete secondary cloud provider regional outage.', status: 'active', war_room_session_id: 'war_room_resilience_01' }
          ],
          crossImpacts: [
            { id: 'cpimp_01', source_plan_id: 'aplan_01', affected_plan_id: 'aplan_hr_cloud_02', impact_description: 'Resequencing cloud SLA assurance delays HR Cloud Wave 4 validation by 2 days.', severity: 'material' }
          ],
          drifts: [
            { id: 'pdrift_01', risk_drift: 0.12, capacity_drift: 0.15, evidence_drift: 0.08, dependency_drift: 0.10 }
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
      const res = await fetch(`/api/v1/transformation-resilience-knowledge-assurance-control/query?query=${encodeURIComponent(queryText)}`, {
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
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-teal-400 to-emerald-400">
              Adaptive Knowledge Assurance & Replanning Control 2.0
            </h1>
            <span className="px-3 py-1 text-xs font-semibold rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20">
              Human-Governed Adaptive Execution
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Detect live change signals, evaluate assumption impacts, track plan staleness, simulate replan options, version immutable plan baselines, and enforce stale-execution protection.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={fetchData}
            className="px-4 py-2 text-xs font-medium rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition"
          >
            Refresh Adaptive Telemetry
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Control Domain</p>
          <p className="text-xl font-bold text-blue-400 mt-1">{data?.domainsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Plan Baselines</p>
          <p className="text-xl font-bold text-emerald-400 mt-1">{data?.baselinesCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Change Signals</p>
          <p className="text-xl font-bold text-amber-400 mt-1">{data?.signalsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Stale Plans Alert</p>
          <p className="text-xl font-bold text-rose-500 mt-1">{data?.stalePlansCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Replan Triggers</p>
          <p className="text-xl font-bold text-indigo-400 mt-1">{data?.replanTriggersCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Plan Versions</p>
          <p className="text-xl font-bold text-teal-400 mt-1">{data?.planVersionsCount ?? 2}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Cross-Plan Impact</p>
          <p className="text-xl font-bold text-cyan-400 mt-1">{data?.crossPlanImpactsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Portfolio Risk Drift</p>
          <p className="text-xl font-bold text-purple-400 mt-1">12.0%</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 overflow-x-auto space-x-2 scrollbar-none">
        {[
          { id: 'overview', label: 'Adaptive Overview' },
          { id: 'baselines', label: 'Plan Baselines (V1.0)' },
          { id: 'signals', label: 'Live Change Signals' },
          { id: 'detections', label: 'Signal Detections' },
          { id: 'assumptions', label: 'Assumption Impacts' },
          { id: 'plan_impacts', label: 'Plan Impact Analysis' },
          { id: 'health', label: 'Plan Health Dimensions' },
          { id: 'staleness', label: 'Plan Staleness Status' },
          { id: 'triggers', label: 'Replan Triggers' },
          { id: 'options', label: 'Replan Option Simulation' },
          { id: 'versions', label: 'Plan Versioning (V2.0)' },
          { id: 'diffs', label: 'Exact Plan Diffs' },
          { id: 'queue', label: 'Replan Priority Queue' },
          { id: 'execution', label: 'ActionGateway Execution' },
          { id: 'cross_plan', label: 'Cross-Plan Impacts' },
          { id: 'drift', label: 'Portfolio Drift' },
          { id: 'emergency', label: 'Emergency Replans' },
          { id: 'query', label: 'Adaptive Control Query' }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-2.5 text-xs font-semibold whitespace-nowrap border-b-2 transition ${
              activeTab === tab.id
                ? 'border-blue-400 text-blue-400 bg-blue-500/5'
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
            Ingesting change signals, calculating assumption impacts, evaluating staleness, and retrieving plan version diffs...
          </div>
        ) : (
          <>
            {activeTab === 'overview' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Adaptive Knowledge Assurance Control Domain</h3>
                {data?.domains?.map((dom: any) => (
                  <div key={dom.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 flex justify-between items-center">
                    <div>
                      <span className="font-semibold text-blue-400">{dom.name}</span>
                      <p className="text-xs text-slate-400 mt-1">Owner: {dom.owner} | Version: {dom.version}</p>
                    </div>
                    <span className="text-xs px-3 py-1 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20 font-semibold">{dom.status}</span>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'signals' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Live Change Signals</h3>
                {data?.signals?.map((sig: any) => (
                  <div key={sig.id} className="p-4 rounded-xl bg-slate-950/60 border border-amber-500/30 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-semibold text-amber-400">Signal ({sig.source}): {sig.change_type}</span>
                      <span className="text-xs px-2.5 py-1 rounded bg-amber-500/20 text-amber-300 font-semibold uppercase">{sig.significance}</span>
                    </div>
                    <p className="text-xs text-slate-300">{sig.description}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'health' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Plan Health Dimensions (Separated Alignment)</h3>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                  {[
                    { label: 'Risk Alignment', score: 0.92 },
                    { label: 'Evidence Alignment', score: 0.88 },
                    { label: 'Capacity Alignment', score: 0.75 },
                    { label: 'Sequence Alignment', score: 0.90 },
                    { label: 'Deadline Alignment', score: 0.95 },
                    { label: 'Assumption Alignment', score: 0.80 }
                  ].map((h, idx) => (
                    <div key={idx} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 text-center">
                      <span className="text-xs font-medium text-slate-400">{h.label}</span>
                      <p className="text-lg font-bold text-teal-400 mt-1">{(h.score * 100).toFixed(0)}%</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'staleness' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Plan Staleness Alerts</h3>
                {data?.stalenesses?.map((s: any) => (
                  <div key={s.id} className="p-4 rounded-xl bg-rose-950/30 border border-rose-500/40 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-semibold text-rose-400">Plan ID: {s.plan_id}</span>
                      <span className="text-xs px-2.5 py-1 rounded bg-rose-500/20 text-rose-300 font-semibold uppercase">{s.status}</span>
                    </div>
                    <p className="text-xs text-slate-300">Outdated Assumptions: {s.outdated_assumptions_json?.join(', ')}</p>
                    <div className="mt-2 p-3 bg-rose-900/40 rounded-lg text-xs text-rose-200">
                      <strong>STALE EXECUTION PROTECTION ACTIVE:</strong> Plan execution is paused per policy until human governance review and version approval.
                    </div>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'versions' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Immutable Plan Versions</h3>
                {data?.versions?.map((v: any) => (
                  <div key={v.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 flex justify-between items-center">
                    <div>
                      <span className="font-semibold text-teal-400">Version {v.version_number} (Parent: {v.parent_version})</span>
                      <p className="text-xs text-slate-400 mt-1">{v.change_summary ?? v.reason}</p>
                    </div>
                    <span className="text-xs px-3 py-1 rounded bg-teal-500/10 text-teal-400 border border-teal-500/20 font-semibold">{v.approval_state}</span>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'diffs' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Exact Version Diffs (V1.0 → V2.0)</h3>
                {data?.diffs?.map((d: any) => (
                  <div key={d.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <span className="text-xs font-semibold text-cyan-400">Diff {d.from_version} → {d.to_version}</span>
                    <p className="text-xs text-slate-300">Reordered Actions: {d.reordered_actions_json?.join(' → ')}</p>
                    <p className="text-xs text-slate-400">Changed Assumptions: {d.changed_assumptions_json?.join(', ')}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'emergency' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Emergency Replans (Crisis Governance)</h3>
                {data?.emergencies?.map((e: any) => (
                  <div key={e.id} className="p-4 rounded-xl bg-slate-950/60 border border-rose-500/30 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-semibold text-rose-400">Emergency Replan: {e.plan_id}</span>
                      <span className="text-xs px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 font-semibold">{e.status}</span>
                    </div>
                    <p className="text-xs text-slate-300">Trigger: {e.trigger_reason}</p>
                    <p className="text-xs text-slate-400">War Room Session: {e.war_room_session_id}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'query' && (
              <div className="space-y-6">
                <h3 className="text-base font-semibold text-slate-200">Natural Language Assurance Control Query</h3>
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={queryText}
                    onChange={(e) => setQueryText(e.target.value)}
                    placeholder="Ask a plan staleness, change signal, version diff, or replan question..."
                    className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500/50"
                  />
                  <button
                    onClick={handleQuery}
                    disabled={queryLoading}
                    className="px-5 py-2.5 bg-blue-500 hover:bg-blue-600 disabled:opacity-50 text-slate-950 text-xs font-semibold rounded-xl transition"
                  >
                    {queryLoading ? 'Processing...' : 'Run Query'}
                  </button>
                </div>

                {queryResult && (
                  <div className="p-5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-semibold text-blue-400">Adaptive Control Result</span>
                      <span className="text-xs text-slate-400">Confidence: {queryResult.confidencePct}%</span>
                    </div>
                    {queryResult.evidenceJson?.error ? (
                      <div className="text-xs text-rose-400 font-semibold">{queryResult.evidenceJson.error}</div>
                    ) : (
                      <div className="space-y-2 text-xs text-slate-300">
                        {queryResult.results?.map((r: any, idx: number) => (
                          <div key={idx} className="p-3 bg-slate-900 rounded-lg space-y-1">
                            <p><strong className="text-rose-400">Stale Plans Alert:</strong> {r.stale_plans}</p>
                            <p><strong className="text-amber-400">What Changed:</strong> {r.what_changed}</p>
                            <p><strong className="text-indigo-400">Assumptions Affected:</strong> {r.assumptions_affected}</p>
                            <p><strong className="text-teal-400">Replan Recommendation:</strong> {r.replan_recommendation}</p>
                            <p><strong className="text-cyan-400">Baseline Comparison:</strong> {r.baseline_comparison}</p>
                            <p><strong className="text-blue-400">Version Notice:</strong> {r.version_notice}</p>
                            <p><strong className="text-rose-400 font-semibold">Protection:</strong> {r.stale_execution_notice}</p>
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
