'use client';

import React, { useState, useEffect } from 'react';

export function TransformationResilienceKnowledgeAssurancePlanningWorkspace() {
  const [activeTab, setActiveTab] = useState<
    | 'overview'
    | 'exposure'
    | 'systemic'
    | 'root_causes'
    | 'levers'
    | 'coverage'
    | 'capacity'
    | 'constraints'
    | 'options'
    | 'sequences'
    | 'scenarios'
    | 'plans'
    | 'tradeoffs'
    | 'residuals'
    | 'execution'
    | 'verification'
    | 'failures'
    | 'learning'
    | 'query'
  >('overview');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('Where is knowledge assurance weakest and what assurance plan is recommended?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/transformation-resilience-knowledge-assurance-planning');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      } else {
        // Fallback seed data
        setData({
          domainsCount: 1,
          portfoliosCount: 1,
          systemicRisksCount: 1,
          rootCausesCount: 1,
          leversCount: 1,
          optionsCount: 1,
          plansCount: 1,
          approvedPlansCount: 1,
          pendingPlansCount: 0,
          capacityGap: '15.0% Specialist Capacity Deficit in Q3',
          domains: [
            { id: 'pdom_01', name: 'Global Enterprise Knowledge Assurance Planning & Risk Optimization 2.0', owner: 'Principal Enterprise Knowledge Assurance Planning Architect', status: 'active', version: 'v2.0' }
          ],
          portfolios: [
            { id: 'aport_01', exposure_score: 0.88, current_capacity: 0.75, planned_capacity: 0.95 }
          ],
          systemicRisks: [
            { id: 'sysr_01', title: 'Systemic Secondary Cloud SLA Telemetry Deficit Across Multi-Region Implementations', breadth: 5, dependency_centrality: 0.92, decision_influence: 0.95, recurrence: 4, uncertainty: 0.25, severity: 'critical' }
          ],
          rootCauses: [
            { id: 'rcg_01', root_cause_type: 'stale_source', description: 'Lack of direct synthetic monitoring integration with vendor interconnect telemetry.', frequency: 4 }
          ],
          levers: [
            { id: 'rlev_01', lever_type: 'shared_evidence_source', title: 'Deploy Third-Party Independent Synthetic Telemetry Mesh', risk_coverage: 0.85, confidence: 0.94 }
          ],
          capacities: [
            { id: 'acap_01', available_capacity: 0.80, required_capacity: 0.95, specialist_capacity: 0.75, simulation_capacity: 0.90, review_capacity: 0.70, evidence_capacity: 0.85 }
          ],
          constraints: [
            { id: 'ccons_01', constraint_type: 'limited_experts', description: 'Specialist bandwidth for cloud SLA verification is constrained in Q3.', severity: 'high' }
          ],
          demands: [
            { id: 'adem_01', risk_workload: 0.90, evidence_workload: 0.95, review_workload: 0.85, simulation_workload: 0.80 }
          ],
          options: [
            { id: 'aopt_01', option_type: 'parallel', title: 'Parallel Synthetic Telemetry & Revalidation Packet Execution', coverage: 0.90, effort: 'medium', time_est: '14 days', risk_reduction: 0.85 }
          ],
          sequences: [
            { id: 'aseq_01', sequence_order_json: ['aopt_01'], rationale: 'Deploy synthetic telemetry prior to submitting revalidation packet to Governance Board.' }
          ],
          scenarios: [
            { id: 'ascen_01', scenario_type: 'full_capacity', coverage: 0.95, residual_risk: 0.05, capacity_required: 0.90 }
          ],
          plans: [
            { id: 'aplan_01', objective: 'Execute multi-region cloud SLA assurance plan to remediate high-influence knowledge risks.', owner: 'Principal Enterprise Knowledge Assurance Planning Architect', risk_coverage: 0.92, residual_risk: 0.08, status: 'approved' }
          ],
          residuals: [
            { id: 'aresr_01', plan_id: 'aplan_01', unaddressed_risk: 'Minor SLA jitter on legacy non-critical SSO background sync', reason: 'Intentionally deferred to Q4 migration.', severity: 'low', owner: 'Legacy Systems Lead' }
          ],
          tradeoffs: [
            { id: 'atrade_01', plan_id: 'aplan_01', tradeoff_description: 'Parallel execution increases short-term specialist workload by 15% but reduces time to assurance by 10 days.', coverage_vs_effort: 'High coverage (92%) for moderate effort boost', speed_vs_uncertainty: 'Faster resolution reduces decision uncertainty prior to Wave 4 deployment' }
          ],
          recommendations: [
            { id: 'arec_01', plan_id: 'aplan_01', label: 'ANALYTICAL RECOMMENDATION — NOT APPROVAL', recommendation_text: 'Proceed with Parallel Synthetic Telemetry & Revalidation Option to achieve 92% risk coverage prior to Wave 4 HR rollout.', confidence: 0.94 }
          ],
          verifications: [
            { id: 'apverif_01', plan_id: 'aplan_01', planned_coverage: 0.92, actual_coverage: 0.90, planned_risk_reduction: 0.85, actual_risk_reduction: 0.82 }
          ],
          effectivenesses: [
            { id: 'apeff_01', plan_id: 'aplan_01', risk_reduction: 0.85, coverage_improvement: 0.90, assurance_quality: 0.94, timeliness: 0.88, capacity_efficiency: 0.92 }
          ],
          failures: [
            { id: 'apfail_01', plan_id: 'aplan_failed_02', failure_type: 'capacity_failure', reason: 'Specialist bandwidth unavailable during Q2 freeze period.' }
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
      const res = await fetch(`/api/v1/transformation-resilience-knowledge-assurance-planning/query?query=${encodeURIComponent(queryText)}`, {
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
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 via-indigo-400 to-cyan-400">
              Knowledge Assurance Planning & Portfolio Risk Optimization 2.0
            </h1>
            <span className="px-3 py-1 text-xs font-semibold rounded-full bg-purple-500/10 text-purple-400 border border-purple-500/20">
              Human-Approved Assurance Planning
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Aggregate portfolio exposure, detect systemic risks, analyze remediation levers, model capacity constraints, and formulate human-approved assurance plans.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={fetchData}
            className="px-4 py-2 text-xs font-medium rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition"
          >
            Refresh Planning Telemetry
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Assurance Domain</p>
          <p className="text-xl font-bold text-purple-400 mt-1">{data?.domainsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Portfolio Exposure</p>
          <p className="text-xl font-bold text-rose-400 mt-1">88.0%</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Systemic Risks</p>
          <p className="text-xl font-bold text-amber-400 mt-1">{data?.systemicRisksCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Remediation Levers</p>
          <p className="text-xl font-bold text-indigo-400 mt-1">{data?.leversCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Risk Coverage</p>
          <p className="text-xl font-bold text-emerald-400 mt-1">92.0%</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Capacity Gap</p>
          <p className="text-xl font-bold text-rose-500 mt-1">15.0%</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Assurance Plans</p>
          <p className="text-xl font-bold text-teal-400 mt-1">{data?.plansCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Residual Risk</p>
          <p className="text-xl font-bold text-blue-400 mt-1">8.0%</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 overflow-x-auto space-x-2 scrollbar-none">
        {[
          { id: 'overview', label: 'Planning Overview' },
          { id: 'exposure', label: 'Portfolio Exposure' },
          { id: 'systemic', label: 'Systemic Risks' },
          { id: 'root_causes', label: 'Root Cause Groups' },
          { id: 'levers', label: 'Remediation Levers' },
          { id: 'coverage', label: 'Coverage Analysis' },
          { id: 'capacity', label: 'Assurance Capacity' },
          { id: 'constraints', label: 'Capacity Constraints' },
          { id: 'options', label: 'Remediation Options' },
          { id: 'sequences', label: 'Sequencing' },
          { id: 'scenarios', label: 'Simulation Scenarios' },
          { id: 'plans', label: 'Assurance Plans' },
          { id: 'tradeoffs', label: 'Trade-offs' },
          { id: 'residuals', label: 'Residual Risk' },
          { id: 'execution', label: 'ActionGateway Execution' },
          { id: 'verification', label: 'Plan Verification' },
          { id: 'failures', label: 'Plan Failures' },
          { id: 'learning', label: 'Portfolio Learning' },
          { id: 'query', label: 'Assurance Planning Query' }
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
            Aggregating risk portfolios, analyzing capacity constraints, running simulation scenarios, and loading assurance plans...
          </div>
        ) : (
          <>
            {activeTab === 'overview' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Knowledge Assurance Planning Domain</h3>
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

            {activeTab === 'systemic' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Systemic Risk Factor Breakdown</h3>
                {data?.systemicRisks?.map((sr: any) => (
                  <div key={sr.id} className="p-4 rounded-xl bg-slate-950/60 border border-rose-500/30 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-semibold text-rose-400">{sr.title}</span>
                      <span className="text-xs px-2.5 py-1 rounded bg-rose-500/20 text-rose-300 font-semibold uppercase">{sr.severity}</span>
                    </div>
                    <p className="text-xs text-slate-300">Breadth: {sr.breadth} decisions | Dependency Centrality: {((sr.dependency_centrality ?? 0.92) * 100).toFixed(0)}% | Decision Influence: {((sr.decision_influence ?? 0.95) * 100).toFixed(0)}%</p>
                    <p className="text-xs text-slate-400">Recurrence: {sr.recurrence} occurrences | Uncertainty: {((sr.uncertainty ?? 0.25) * 100).toFixed(0)}%</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'capacity' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Assurance Capacity & Workload Gaps</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {[
                    { label: 'Available Capacity', score: 0.80 },
                    { label: 'Required Capacity', score: 0.95 },
                    { label: 'Specialist Capacity', score: 0.75 },
                    { label: 'Simulation Capacity', score: 0.90 },
                    { label: 'Review Capacity', score: 0.70 },
                    { label: 'Evidence Capacity', score: 0.85 }
                  ].map((c, idx) => (
                    <div key={idx} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 text-center">
                      <span className="text-xs font-medium text-slate-400">{c.label}</span>
                      <p className="text-lg font-bold text-indigo-400 mt-1">{(c.score * 100).toFixed(0)}%</p>
                    </div>
                  ))}
                </div>
                <div className="p-4 rounded-xl bg-rose-950/30 border border-rose-500/30 text-xs text-rose-300">
                  <strong>CAPACITY GAP ALERT:</strong> {data?.capacityGap ?? '15.0% Specialist Capacity Deficit in Q3'}
                </div>
              </div>
            )}

            {activeTab === 'plans' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Human-Approved Assurance Plans</h3>
                {data?.plans?.map((p: any) => (
                  <div key={p.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-semibold text-teal-400">Plan: {p.objective}</span>
                      <span className="text-xs px-2 py-0.5 rounded bg-teal-500/10 text-teal-400 border border-teal-500/20">{p.status}</span>
                    </div>
                    <p className="text-xs text-slate-300">Risk Coverage: {((p.risk_coverage ?? 0.92) * 100).toFixed(0)}% | Residual Risk: {((p.residual_risk ?? 0.08) * 100).toFixed(0)}%</p>
                    <p className="text-xs text-slate-400">Owner: {p.owner} | Deadline: {new Date(p.deadline).toLocaleDateString()}</p>
                    {data?.recommendations?.map((rec: any) => (
                      <div key={rec.id} className="mt-2 p-3 bg-indigo-950/40 border border-indigo-500/30 rounded-lg">
                        <span className="text-[10px] font-bold text-indigo-400 tracking-wider uppercase block">{rec.label}</span>
                        <p className="text-xs text-slate-200 mt-1">{rec.recommendation_text}</p>
                      </div>
                    ))}
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'tradeoffs' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Plan Trade-off Analysis</h3>
                {data?.tradeoffs?.map((t: any) => (
                  <div key={t.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <span className="text-xs font-semibold text-amber-400">Trade-off</span>
                    <p className="text-xs text-slate-200">{t.tradeoff_description}</p>
                    <p className="text-xs text-slate-400">Coverage vs Effort: {t.coverage_vs_effort}</p>
                    <p className="text-xs text-slate-400">Speed vs Uncertainty: {t.speed_vs_uncertainty}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'residuals' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Explicit Residual Risk Tracking</h3>
                {data?.residuals?.map((r: any) => (
                  <div key={r.id} className="p-4 rounded-xl bg-slate-950/60 border border-blue-500/30 space-y-2">
                    <span className="text-xs font-semibold text-blue-400">Unaddressed Risk: {r.unaddressed_risk}</span>
                    <p className="text-xs text-slate-300">Reason: {r.reason}</p>
                    <p className="text-xs text-slate-400">Owner: {r.owner} | Review Date: {new Date(r.review_date).toLocaleDateString()}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'query' && (
              <div className="space-y-6">
                <h3 className="text-base font-semibold text-slate-200">Natural Language Assurance Planning Query</h3>
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={queryText}
                    onChange={(e) => setQueryText(e.target.value)}
                    placeholder="Ask a portfolio weakness, systemic risk, or assurance plan question..."
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
                      <span className="text-xs font-semibold text-purple-400">Planning Assurance Result</span>
                      <span className="text-xs text-slate-400">Confidence: {queryResult.confidencePct}%</span>
                    </div>
                    {queryResult.evidenceJson?.error ? (
                      <div className="text-xs text-rose-400 font-semibold">{queryResult.evidenceJson.error}</div>
                    ) : (
                      <div className="space-y-2 text-xs text-slate-300">
                        {queryResult.results?.map((r: any, idx: number) => (
                          <div key={idx} className="p-3 bg-slate-900 rounded-lg space-y-1">
                            <p><strong className="text-purple-400">Weakest Assurance:</strong> {r.weakest_assurance}</p>
                            <p><strong className="text-rose-400">Systemic Risks:</strong> {r.systemic_risks}</p>
                            <p><strong className="text-amber-400">Root Causes:</strong> {r.root_causes}</p>
                            <p><strong className="text-indigo-400">Remediation Levers:</strong> {r.remediation_levers}</p>
                            <p><strong className="text-cyan-400">Capacity Constraints:</strong> {r.capacity_constraints}</p>
                            <p><strong className="text-teal-400">Assurance Plan:</strong> {r.assurance_plan}</p>
                            <p><strong className="text-indigo-400">Notice:</strong> {r.recommendation_notice}</p>
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
