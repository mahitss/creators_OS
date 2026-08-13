'use client';

import React, { useState, useEffect } from 'react';

export function TransformationResilienceKnowledgeOperationsWorkspace() {
  const [activeTab, setActiveTab] = useState<
    | 'overview'
    | 'queue'
    | 'critical'
    | 'overdue'
    | 'assignments'
    | 'plans'
    | 'evidence'
    | 'reviews'
    | 'escalations'
    | 'accepted'
    | 'deferred'
    | 'verification'
    | 'effectiveness'
    | 'recurring'
    | 'concentration'
    | 'quality'
    | 'patterns'
    | 'query'
  >('overview');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('Which knowledge risks need attention and what remediation is underway?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/transformation-resilience-knowledge-operations');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      } else {
        // Fallback seed data
        setData({
          domainsCount: 1,
          casesCount: 4,
          criticalCount: 1,
          overdueCount: 1,
          acceptedCount: 1,
          deferredCount: 1,
          plansCount: 1,
          evidenceTasksCount: 1,
          reviewTasksCount: 1,
          escalationsCount: 1,
          recurringPatternsCount: 1,
          domains: [
            { id: 'opdom_01', name: 'Global Enterprise Knowledge Operations & Remediation Operating System 2.0', owner: 'Principal Enterprise Knowledge Operations Architect', status: 'active', version: 'v2.0' }
          ],
          cases: [
            { id: 'rcase_01', knowledge_object_id: 'kobj_less_01', risk_type: 'high_influence_low_quality', severity: 'high', impact: 'high_decision_impact', owner: 'Principal Decision Assurance Engineer', status: 'in_remediation', due_at: '2026-08-20T12:00:00Z' },
            { id: 'rcase_overdue_01', knowledge_object_id: 'kobj_stale_02', risk_type: 'stale_unsupported_precedent', severity: 'critical', impact: 'critical_decision_impact', owner: 'Enterprise Architecture Board', status: 'triaged', due_at: '2026-08-10T12:00:00Z' },
            { id: 'rcase_accepted_01', knowledge_object_id: 'kobj_legacy_03', risk_type: 'context_mismatch', severity: 'medium', impact: 'medium_decision_impact', owner: 'Legacy System Remediation Lead', status: 'accepted_risk', due_at: '2026-08-20T12:00:00Z', reason: 'Datacenter migration scheduled in Q4.' },
            { id: 'rcase_deferred_01', knowledge_object_id: 'kobj_vendor_04', risk_type: 'unsupported_claim', severity: 'low', impact: 'low_decision_impact', owner: 'Vendor Assurance Lead', status: 'deferred', due_at: '2026-08-20T12:00:00Z', defer_until: '2026-09-15T12:00:00Z' }
          ],
          queues: [
            { id: 'rq_01', risk_case_id: 'rcase_01', severity: 'high', impact: 'high_decision_impact', owner: 'Principal Decision Assurance Engineer', deadline: '2026-08-20T12:00:00Z', status: 'in_remediation' }
          ],
          assignments: [
            { id: 'rasgn_01', risk_case_id: 'rcase_01', owner: 'Principal Decision Assurance Engineer', assigned_by: 'Principal Knowledge Operations Architect', reason: 'High decision influence on Multi-Region Token Cache deployment.' }
          ],
          plans: [
            { id: 'rplan_01', risk_case_id: 'rcase_01', objective: 'Collect independent telemetry to validate +15ms SLA buffer under 10Gbps interconnect load.', owner: 'Principal Decision Assurance Engineer', status: 'in_progress' }
          ],
          actions: [
            { id: 'act_01', plan_id: 'rplan_01', action_type: 'collect_evidence', title: 'Obtain independent telemetry from third-party vendor', owner: 'Observability Lead', status: 'in_progress' }
          ],
          evidenceTasks: [
            { id: 'etask_01', gap_id: 'egap_01', requested_evidence: 'Third-party synthetic latency trace for secondary cloud provider route', source: 'Independent Monitoring Network', owner: 'Observability Lead', status: 'assigned', quality: 0.95 }
          ],
          reviewTasks: [
            { id: 'rtask_01', risk_case_id: 'rcase_01', review_question: 'Does the +15ms buffer remain required after fiber route upgrade?', reviewer: 'Principal Knowledge Governance Architect', status: 'assigned', result: 'inconclusive' }
          ],
          verifications: [
            { id: 'rverif_01', risk_case_id: 'rcase_01', risk_before: { severity: 'high' }, risk_after: { severity: 'low' }, knowledge_health_before: { freshness_score: 0.70 }, knowledge_health_after: { freshness_score: 0.96 } }
          ],
          effectivenesses: [
            { id: 'reff_01', risk_case_id: 'rcase_01', risk_reduction: 0.85, evidence_improvement: 0.90, confidence_improvement: 0.88, applicability_improvement: 0.92, reuse_improvement: 0.95 }
          ],
          escalations: [
            { id: 'resc_01', risk_case_id: 'rcase_overdue_01', trigger: 'sla_breached_critical_severity', severity: 'critical', owner: 'Enterprise Architecture Board', status: 'escalated' }
          ],
          recurring: [
            { id: 'rrec_01', pattern_title: 'Repeated Evidence Gap in Secondary Cloud Provider SLA Jitter', frequency: 4, confidence: 0.94 }
          ],
          qualities: [
            { id: 'rqual_01', risk_case_id: 'rcase_01', completeness: 0.95, evidence_quality: 0.94, verification_quality: 0.96, timeliness: 0.92, repeatability: 0.90 }
          ],
          operatingPatterns: [
            { id: 'opat_01', title: 'Independent Evidence Corroboration Pattern', description: 'Cross-verifying secondary vendor benchmarks via third-party synthetic monitoring resolves high-influence knowledge risks.', confidence: 0.95 }
          ],
          riskConcentration: [
            { domain: 'Secondary Cloud Resilience', transformation: 'Global Enterprise Multi-Region Cloud Wave 4', weakestAssurance: 'Lack of Independent Telemetry Corroboration', riskCount: 3, severity: 'high' }
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
      const res = await fetch(`/api/v1/transformation-resilience-knowledge-operations/query?query=${encodeURIComponent(queryText)}`, {
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
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-amber-400 via-rose-400 to-purple-400">
              Knowledge Risk Remediation & Governed Assurance Operating System 2.0
            </h1>
            <span className="px-3 py-1 text-xs font-semibold rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20">
              Operational Assurance Workflow
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Turn knowledge-assurance findings into an accountable operational workflow: Risk Detection → Prioritization → Owner Assignment → Remediation → Verification.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={fetchData}
            className="px-4 py-2 text-xs font-medium rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition"
          >
            Refresh Operations Telemetry
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Risk Cases</p>
          <p className="text-xl font-bold text-amber-400 mt-1">{data?.casesCount ?? 4}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Critical Severity</p>
          <p className="text-xl font-bold text-rose-400 mt-1">{data?.criticalCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Overdue Risks</p>
          <p className="text-xl font-bold text-rose-500 mt-1">{data?.overdueCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Active Plans</p>
          <p className="text-xl font-bold text-purple-400 mt-1">{data?.plansCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Evidence Tasks</p>
          <p className="text-xl font-bold text-cyan-400 mt-1">{data?.evidenceTasksCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Escalations</p>
          <p className="text-xl font-bold text-indigo-400 mt-1">{data?.escalationsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Accepted Risks</p>
          <p className="text-xl font-bold text-blue-400 mt-1">{data?.acceptedCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Recurring Patterns</p>
          <p className="text-xl font-bold text-teal-400 mt-1">{data?.recurringPatternsCount ?? 1}</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 overflow-x-auto space-x-2 scrollbar-none">
        {[
          { id: 'overview', label: 'Operations Overview' },
          { id: 'queue', label: 'Risk Queue' },
          { id: 'critical', label: 'Critical Risks' },
          { id: 'overdue', label: 'Overdue Risks' },
          { id: 'assignments', label: 'Owner Assignments' },
          { id: 'plans', label: 'Remediation Plans' },
          { id: 'evidence', label: 'Evidence Tasks' },
          { id: 'reviews', label: 'Review Tasks' },
          { id: 'escalations', label: 'Escalations' },
          { id: 'accepted', label: 'Accepted Risks' },
          { id: 'deferred', label: 'Deferred Risks' },
          { id: 'verification', label: 'Verification' },
          { id: 'effectiveness', label: 'Effectiveness' },
          { id: 'recurring', label: 'Recurring Risks' },
          { id: 'concentration', label: 'Risk Concentration' },
          { id: 'quality', label: 'Remediation Quality' },
          { id: 'patterns', label: 'Operating Patterns' },
          { id: 'query', label: 'Operations Query' }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-2.5 text-xs font-semibold whitespace-nowrap border-b-2 transition ${
              activeTab === tab.id
                ? 'border-amber-400 text-amber-400 bg-amber-500/5'
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
            Retrieving risk queue, owner assignments, remediation plans, and verification data...
          </div>
        ) : (
          <>
            {activeTab === 'overview' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Knowledge Operations Domain</h3>
                {data?.domains?.map((dom: any) => (
                  <div key={dom.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 flex justify-between items-center">
                    <div>
                      <span className="font-semibold text-amber-400">{dom.name}</span>
                      <p className="text-xs text-slate-400 mt-1">Owner: {dom.owner} | Version: {dom.version}</p>
                    </div>
                    <span className="text-xs px-3 py-1 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20 font-semibold">{dom.status}</span>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'queue' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Accountable Risk Queue</h3>
                {data?.cases?.map((c: any) => (
                  <div key={c.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-semibold text-amber-400">{c.risk_type}</span>
                      <span className={`text-xs px-2.5 py-1 rounded font-semibold border ${
                        c.severity === 'critical' ? 'bg-rose-500/10 text-rose-400 border-rose-500/20' : 'bg-amber-500/10 text-amber-400 border-amber-500/20'
                      }`}>{c.severity}</span>
                    </div>
                    <p className="text-xs text-slate-300">Owner: {c.owner} | Status: {c.status}</p>
                    <p className="text-xs text-slate-400">Impact: {c.impact} | Due: {new Date(c.due_at).toLocaleDateString()}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'overdue' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">SLA Breached & Overdue Risks</h3>
                {data?.cases?.filter((c: any) => c.id === 'rcase_overdue_01').map((c: any) => (
                  <div key={c.id} className="p-4 rounded-xl bg-slate-950/60 border border-rose-500/40 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-bold text-rose-400">SLA BREACHED: {c.risk_type}</span>
                      <span className="text-xs px-2.5 py-1 rounded bg-rose-500/20 text-rose-300 font-semibold border border-rose-500/30">OVERDUE</span>
                    </div>
                    <p className="text-xs text-slate-300">Owner: {c.owner} | Severity: {c.severity}</p>
                    <p className="text-xs text-slate-400">Past Due Since: {new Date(c.due_at).toLocaleDateString()}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'assignments' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Risk Owner Assignments</h3>
                {data?.assignments?.map((asgn: any) => (
                  <div key={asgn.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <span className="text-xs font-semibold text-purple-400">Assigned To: {asgn.owner}</span>
                    <p className="text-xs text-slate-300">Assigned By: {asgn.assigned_by}</p>
                    <p className="text-xs text-slate-400">Reason: {asgn.reason}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'plans' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Active Remediation Plans & Actions</h3>
                {data?.plans?.map((p: any) => (
                  <div key={p.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-semibold text-emerald-400">Plan: {p.objective}</span>
                      <span className="text-xs px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">{p.status}</span>
                    </div>
                    <p className="text-xs text-slate-300">Owner: {p.owner}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'evidence' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Evidence Tasks & Collection</h3>
                {data?.evidenceTasks?.map((et: any) => (
                  <div key={et.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <span className="text-sm font-semibold text-cyan-400">{et.requested_evidence}</span>
                    <p className="text-xs text-slate-300">Source: {et.source} | Owner: {et.owner}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'accepted' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Intentionally Accepted Risks</h3>
                {data?.cases?.filter((c: any) => c.status === 'accepted_risk').map((c: any) => (
                  <div key={c.id} className="p-4 rounded-xl bg-slate-950/60 border border-blue-500/30 space-y-2">
                    <span className="text-xs font-semibold text-blue-400">Accepted Risk: {c.risk_type}</span>
                    <p className="text-xs text-slate-300">Reason: {c.reason}</p>
                    <p className="text-xs text-slate-400">Review Date: {new Date(c.review_date).toLocaleDateString()}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'recurring' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Recurring Risk Patterns</h3>
                {data?.recurring?.map((r: any) => (
                  <div key={r.id} className="p-4 rounded-xl bg-slate-950/60 border border-purple-500/30 space-y-2">
                    <span className="text-sm font-semibold text-purple-400">{r.pattern_title}</span>
                    <p className="text-xs text-slate-300">Frequency: {r.frequency} occurrences | Confidence: {((r.confidence ?? 0.94) * 100).toFixed(0)}%</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'concentration' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Risk Concentration Heatmap</h3>
                {data?.riskConcentration?.map((rc: any, idx: number) => (
                  <div key={idx} className="p-4 rounded-xl bg-slate-950/60 border border-amber-500/30 space-y-2">
                    <span className="text-sm font-semibold text-amber-400">Concentration Domain: {rc.domain}</span>
                    <p className="text-xs text-slate-300">Transformation: {rc.transformation}</p>
                    <p className="text-xs text-slate-400">Weakest Assurance Area: {rc.weakestAssurance}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'query' && (
              <div className="space-y-6">
                <h3 className="text-base font-semibold text-slate-200">Natural Language Operations Query</h3>
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={queryText}
                    onChange={(e) => setQueryText(e.target.value)}
                    placeholder="Ask a risk remediation, owner assignment, or overdue risk question..."
                    className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-amber-500/50"
                  />
                  <button
                    onClick={handleQuery}
                    disabled={queryLoading}
                    className="px-5 py-2.5 bg-amber-500 hover:bg-amber-600 disabled:opacity-50 text-slate-950 text-xs font-semibold rounded-xl transition"
                  >
                    {queryLoading ? 'Processing...' : 'Run Query'}
                  </button>
                </div>

                {queryResult && (
                  <div className="p-5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-semibold text-amber-400">Operations Assurance Result</span>
                      <span className="text-xs text-slate-400">Confidence: {queryResult.confidencePct}%</span>
                    </div>
                    {queryResult.evidenceJson?.error ? (
                      <div className="text-xs text-rose-400 font-semibold">{queryResult.evidenceJson.error}</div>
                    ) : (
                      <div className="space-y-2 text-xs text-slate-300">
                        {queryResult.results?.map((r: any, idx: number) => (
                          <div key={idx} className="p-3 bg-slate-900 rounded-lg space-y-1">
                            <p><strong className="text-amber-400">Risk Attention:</strong> {r.risk_attention}</p>
                            <p><strong className="text-rose-400">Overdue Risks:</strong> {r.overdue_risks}</p>
                            <p><strong className="text-purple-400">Risk Ownership:</strong> {r.risk_ownership}</p>
                            <p><strong className="text-cyan-400">Missing Evidence:</strong> {r.missing_evidence}</p>
                            <p><strong className="text-teal-400">Recurring Risks:</strong> {r.recurring_risks}</p>
                            <p><strong className="text-indigo-400">Risk Concentration:</strong> {r.risk_concentration}</p>
                            <p><strong className="text-emerald-400">Remediation Effectiveness:</strong> {r.remediation_effectiveness}</p>
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
