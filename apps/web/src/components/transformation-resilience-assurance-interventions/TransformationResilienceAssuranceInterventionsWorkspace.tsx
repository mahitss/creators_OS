'use client';

import React, { useState, useEffect } from 'react';

export function TransformationResilienceAssuranceInterventionsWorkspace() {
  const [activeTab, setActiveTab] = useState<
    | 'overview'
    | 'cases'
    | 'triggers'
    | 'options'
    | 'scenarios'
    | 'recommendations'
    | 'decision_packets'
    | 'plans'
    | 'actions'
    | 'readiness'
    | 'rollbacks'
    | 'contingencies'
    | 'conflicts'
    | 'cascades'
    | 'expirations'
    | 'effectiveness'
    | 'failures'
    | 'lessons'
    | 'query'
  >('overview');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('Which warnings require intervention and what are the reversible options?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/transformation-resilience-assurance-interventions');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      } else {
        // Fallback seed data
        setData({
          domainsCount: 1,
          casesCount: 1,
          triggersCount: 1,
          optionsCount: 3,
          rollbacksCount: 1,
          contingenciesCount: 1,
          plansCount: 1,
          actionsCount: 1,
          conflictsCount: 1,
          lessonsCount: 1,
          domains: [
            { id: 'idom_01', name: 'Global Enterprise Assurance Intervention Orchestration 2.0', owner: 'Principal Enterprise Assurance Intervention Architect', status: 'active', version: 'v2.0' }
          ],
          cases: [
            { id: 'icase_01', warning_id: 'ewarn_01', forecast_id: 'fcst_01', risk_id: 'emrisk_01', severity: 'high', horizon: 'near_term', intervention_window: '10 days remaining', status: 'options_ready', owner: 'Transformation Resilience Preventive Operations Engineer' }
          ],
          triggers: [
            { id: 'itrig_01', type: 'early_warning', signal_id: 'fsig_01', evidence_description: 'Gradual 15% increase in Simulation Cluster 01 queue depth over past 14 days.', confidence: 0.95, validation_status: 'validated' }
          ],
          options: [
            { id: 'iopt_baseline_01', option_type: 'continue_current_state', title: 'Baseline Option: Continue Current State / Do Nothing', reversibility: 'reversible', risk_reduction: 0.0, coverage: 0.84, effort: 'none' },
            { id: 'iopt_resequence_01', option_type: 'resequence', title: 'Preemptive Resequencing Option (Stagger simulation runs by 7 days)', reversibility: 'reversible', risk_reduction: 0.90, coverage: 0.92, effort: 'medium' },
            { id: 'iopt_reserve_01', option_type: 'reserve_capacity', title: 'Capacity Expansion Option (Reserve 4 cloud compute nodes)', reversibility: 'partially_reversible', risk_reduction: 0.95, coverage: 0.95, effort: 'high' }
          ],
          rollbackPlans: [
            { id: 'rplan_01', option_id: 'iopt_resequence_01', rollback_trigger: 'Simulated capacity bottleneck is cleared earlier than week 3.', authorization_required: 'Governance Board Authorization', expected_recovery_time_hours: 2 }
          ],
          contingencyPlans: [
            { id: 'cplan_01', activation_criteria: 'If queue depth exceeds 90% in week 2.', capacity_reserved: '2 backup compute nodes', status: 'ready' }
          ],
          readinesses: [
            { id: 'cread_01', evidence_readiness: 'ready', resource_readiness: 'ready', dependency_readiness: 'partially_ready', execution_readiness: 'ready', governance_readiness: 'ready', overall_status: 'partially_ready' }
          ],
          recommendations: [
            { id: 'irec_01', label: 'ANALYTICAL RECOMMENDATION — NOT DECISION', recommended_option_id: 'iopt_resequence_01', reason: 'Preemptive resequencing eliminates predicted compute bottleneck with zero budget increase and high reversibility.', confidence: 0.95 }
          ],
          decisionPackets: [
            { id: 'dpack_01', governance_requirement: 'Requires Governance Board sign-off prior to week 2 close.', packet_summary: 'Intervention Decision Packet for Q3 Wave 4 Compute Deficit Risk.' }
          ],
          plans: [
            { id: 'iplan_01', objective: 'Eliminate Q3 Wave 4 simulation compute bottleneck', selected_option_id: 'iopt_resequence_01', status: 'approved' }
          ],
          actions: [
            { id: 'iact_01', plan_id: 'iplan_01', action_type: 'change_sequence', description: 'Shift HR Cloud Wave 4 simulation batch by 7 days.', status: 'ready' }
          ],
          conflicts: [
            { id: 'iconf_01', case_id: 'icase_01', conflicting_plan_id: 'aplan_hr_cloud_02', severity: 'high', conflict_summary: 'Resequencing shifts simulation batch into HR Cloud testing window.' }
          ],
          lessons: [
            { id: 'iless_01', lesson_type: 'timing', title: 'Intervention Timing Lesson', description: 'Submitting intervention decision packets 10 days in advance allows full governance approval without delaying wave deployment.' }
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
      const res = await fetch(`/api/v1/transformation-resilience-assurance-interventions/query?query=${encodeURIComponent(queryText)}`, {
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
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-teal-400 via-cyan-400 to-indigo-400">
              Assurance Intervention Orchestration 2.0
            </h1>
            <span className="px-3 py-1 text-xs font-semibold rounded-full bg-teal-500/10 text-teal-400 border border-teal-500/20">
              Governed Preventive Prevention & Action Control
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Turn credible early warnings into evidence-backed, governed intervention plans: option reversibility, rollback plans, contingency readiness, ActionGateway protection, and human decision authority.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={fetchData}
            className="px-4 py-2 text-xs font-medium rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition"
          >
            Refresh Intervention Engine
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Intervention Domain</p>
          <p className="text-xl font-bold text-teal-400 mt-1">Active</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Active Cases</p>
          <p className="text-xl font-bold text-cyan-400 mt-1">{data?.casesCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Triggers</p>
          <p className="text-xl font-bold text-amber-400 mt-1">Validated</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Preventive Options</p>
          <p className="text-xl font-bold text-indigo-400 mt-1">{data?.optionsCount ?? 3}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Contingency Readiness</p>
          <p className="text-xl font-bold text-emerald-400 mt-1">Partially Ready</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Action Protection</p>
          <p className="text-xl font-bold text-blue-400 mt-1">ActionGateway</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Rollback Target</p>
          <p className="text-xl font-bold text-rose-400 mt-1">2 Hours</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Intervention Conflicts</p>
          <p className="text-xl font-bold text-yellow-400 mt-1">{data?.conflictsCount ?? 1}</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 overflow-x-auto space-x-2 scrollbar-none">
        {[
          { id: 'overview', label: 'Intervention Overview' },
          { id: 'cases', label: 'Active Cases' },
          { id: 'triggers', label: 'Validated Triggers' },
          { id: 'options', label: 'Preventive Options' },
          { id: 'scenarios', label: 'Simulation Scenarios' },
          { id: 'recommendations', label: 'Analytical Recommendations' },
          { id: 'decision_packets', label: 'Decision Packets' },
          { id: 'plans', label: 'Approved Plans' },
          { id: 'actions', label: 'ActionGateway Actions' },
          { id: 'readiness', label: 'Contingency Readiness' },
          { id: 'rollbacks', label: 'Rollback Plans' },
          { id: 'contingencies', label: 'Contingency Plans' },
          { id: 'conflicts', label: 'Intervention Conflicts' },
          { id: 'cascades', label: 'Intervention Cascades' },
          { id: 'expirations', label: 'Expirations & Stale Protection' },
          { id: 'effectiveness', label: 'Intervention Effectiveness' },
          { id: 'failures', label: 'Failure Analysis' },
          { id: 'lessons', label: 'Intervention Lessons' },
          { id: 'query', label: 'Assurance Intervention Query' }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-2.5 text-xs font-semibold whitespace-nowrap border-b-2 transition ${
              activeTab === tab.id
                ? 'border-teal-400 text-teal-400 bg-teal-500/5'
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
            Evaluating active intervention cases, revalidating triggers, scoring option reversibility, and checking ActionGateway protection...
          </div>
        ) : (
          <>
            {activeTab === 'overview' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Assurance Intervention Domain</h3>
                {data?.domains?.map((dom: any) => (
                  <div key={dom.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 flex justify-between items-center">
                    <div>
                      <span className="font-semibold text-teal-400">{dom.name}</span>
                      <p className="text-xs text-slate-400 mt-1">Owner: {dom.owner} | Version: {dom.version}</p>
                    </div>
                    <span className="text-xs px-3 py-1 rounded bg-teal-500/10 text-teal-400 border border-teal-500/20 font-semibold">{dom.status}</span>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'cases' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Active Intervention Cases</h3>
                {data?.cases?.map((c: any) => (
                  <div key={c.id} className="p-4 rounded-xl bg-slate-950/60 border border-cyan-500/30 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-semibold text-cyan-400">Case ID: {c.id} (Severity: {c.severity})</span>
                      <span className="text-xs px-2.5 py-1 rounded bg-cyan-500/20 text-cyan-300 font-semibold uppercase">Status: {c.status}</span>
                    </div>
                    <p className="text-xs text-slate-300">Intervention Window: {c.intervention_window} | Horizon: {c.horizon}</p>
                    <p className="text-xs text-slate-400">Owner: {c.owner}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'options' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Intervention Options (Baseline 'Continue Current State' Included)</h3>
                {data?.options?.map((opt: any) => (
                  <div key={opt.id} className="p-4 rounded-xl bg-slate-950/60 border border-indigo-500/30 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-semibold text-indigo-300">{opt.title}</span>
                      <span className={`text-xs px-2.5 py-1 rounded font-semibold uppercase ${
                        opt.reversibility === 'reversible' ? 'bg-emerald-500/20 text-emerald-300' : 'bg-amber-500/20 text-amber-300'
                      }`}>
                        Reversibility: {opt.reversibility}
                      </span>
                    </div>
                    <div className="grid grid-cols-4 gap-2 text-xs text-slate-300 bg-slate-900 p-3 rounded-lg">
                      <p>Risk Reduction: <strong className="text-emerald-400">{(opt.risk_reduction * 100).toFixed(0)}%</strong></p>
                      <p>Coverage: <strong>{(opt.coverage * 100).toFixed(0)}%</strong></p>
                      <p>Effort: <strong>{opt.effort}</strong></p>
                      <p>Capacity: <strong>{opt.capacity_required}</strong></p>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'rollbacks' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Rollback Plans & Authorization</h3>
                {data?.rollbackPlans?.map((r: any) => (
                  <div key={r.id} className="p-4 rounded-xl bg-slate-950/60 border border-rose-500/30 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-semibold text-rose-400">Rollback Plan ID: {r.id}</span>
                      <span className="text-xs px-2.5 py-1 rounded bg-rose-500/20 text-rose-300 font-semibold">Target Recovery: {r.expected_recovery_time_hours} hrs</span>
                    </div>
                    <p className="text-xs text-slate-300">Trigger: {r.rollback_trigger}</p>
                    <p className="text-xs text-slate-400 font-semibold">Authorization Required: {r.authorization_required}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'readiness' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Contingency Readiness Dimensions</h3>
                {data?.readinesses?.map((rd: any) => (
                  <div key={rd.id} className="p-4 rounded-xl bg-slate-950/60 border border-emerald-500/30 space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-semibold text-emerald-400">Contingency ID: {rd.contingency_id}</span>
                      <span className="text-xs px-2.5 py-1 rounded bg-emerald-500/20 text-emerald-300 font-semibold uppercase">Overall: {rd.overall_status}</span>
                    </div>
                    <div className="grid grid-cols-5 gap-2 text-xs text-slate-300 bg-slate-900 p-3 rounded-lg">
                      <div><p className="text-slate-400">Evidence</p><p className="font-bold text-emerald-400">{rd.evidence_readiness}</p></div>
                      <div><p className="text-slate-400">Resource</p><p className="font-bold text-emerald-400">{rd.resource_readiness}</p></div>
                      <div><p className="text-slate-400">Dependency</p><p className="font-bold text-amber-400">{rd.dependency_readiness}</p></div>
                      <div><p className="text-slate-400">Execution</p><p className="font-bold text-emerald-400">{rd.execution_readiness}</p></div>
                      <div><p className="text-slate-400">Governance</p><p className="font-bold text-emerald-400">{rd.governance_readiness}</p></div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'query' && (
              <div className="space-y-6">
                <h3 className="text-base font-semibold text-slate-200">Natural Language Assurance Intervention Query</h3>
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={queryText}
                    onChange={(e) => setQueryText(e.target.value)}
                    placeholder="Ask about active intervention cases, reversible options, rollback plans, or contingency readiness..."
                    className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-teal-500/50"
                  />
                  <button
                    onClick={handleQuery}
                    disabled={queryLoading}
                    className="px-5 py-2.5 bg-teal-500 hover:bg-teal-600 disabled:opacity-50 text-slate-950 text-xs font-semibold rounded-xl transition"
                  >
                    {queryLoading ? 'Processing...' : 'Run Query'}
                  </button>
                </div>

                {queryResult && (
                  <div className="p-5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-semibold text-teal-400">Assurance Intervention Result</span>
                      <span className="text-xs text-slate-400">Confidence: {queryResult.confidencePct}%</span>
                    </div>
                    {queryResult.evidenceJson?.error ? (
                      <div className="text-xs text-rose-400 font-semibold">{queryResult.evidenceJson.error}</div>
                    ) : (
                      <div className="space-y-2 text-xs text-slate-300">
                        {queryResult.results?.map((r: any, idx: number) => (
                          <div key={idx} className="p-3 bg-slate-900 rounded-lg space-y-1">
                            <p><strong className="text-cyan-400">Intervention Cases:</strong> {r.intervention_cases}</p>
                            <p><strong className="text-amber-400">Validated Triggers:</strong> {r.triggers}</p>
                            <p><strong className="text-indigo-400">Intervention Options:</strong> {r.intervention_options}</p>
                            <p><strong className="text-rose-400">Rollback Plans:</strong> {r.rollback_plans}</p>
                            <p><strong className="text-emerald-400">Contingencies & Readiness:</strong> {r.contingencies_and_readiness}</p>
                            <p><strong className="text-purple-300 font-semibold">Governance Notice:</strong> {r.recommendation_notice}</p>
                            <p><strong className="text-blue-400">Governance & ActionGateway:</strong> {r.governance_and_execution}</p>
                            <p><strong className="text-teal-400">Effectiveness & Learning:</strong> {r.effectiveness_and_learning}</p>
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
