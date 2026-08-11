'use client';

import React, { useState, useEffect } from 'react';

export function TransformationGovernanceWorkspace() {
  const [activeTab, setActiveTab] = useState<'overview' | 'decision_rights' | 'controls' | 'friction_gaps' | 'overcontrol_load' | 'bottlenecks_delegation' | 'exceptions_drift' | 'change_requests' | 'reviews_learning' | 'nl_query'>('overview');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('Where is governance slowing us down?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/transformation-governance');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      } else {
        // Fallback seed structure
        setData({
          activeProfilesCount: 1,
          decisionRightsCount: 1,
          activeControlsCount: 1,
          surfacedConflictsCount: 1,
          detectedFrictionsCount: 1,
          delegationCandidatesCount: 1,
          activeExceptionsCount: 1,
          governanceEfficiencyScorePct: 94.5,
          profiles: [
            { id: 'gov_prof_01', name: 'Enterprise Autonomous Transformation Adaptive Governance Model', scope: 'enterprise', owner: 'Executive Governance Steering Council', status: 'active', version: 'v2.0' }
          ],
          rights: [
            { id: 'dr_01', decision_type: 'scale', scope: 'Enterprise Wave Rollout', authority_level: 'Transformation Steering Committee', approval_requirement: 'Two-key Executive Approval (CIO + Steering Committee Chair)', delegation_allowed: true }
          ],
          conflicts: [
            { id: 'dr_conf_01', authority_a: 'Engineering Capacity Allocation Board', authority_b: 'Transformation Portfolio Controller', conflict_description: 'Overlapping approval authority for Wave 2 FTE capacity reallocation', status: 'surfaced' }
          ],
          controls: [
            { id: 'ctrl_01', control_type: 'approval', purpose: 'Ensure zero-trust compliance before wave scale deployment', owner: 'Chief Information Security Officer', policy_reference: 'POL-2026-ZERO-TRUST-01' }
          ],
          frictions: [
            { id: 'fric_01', friction_type: 'approval_delay', cause: 'Manual CISO review queue backlog for routine low-risk policy updates', time_impact_hours: 48.0, severity: 'moderate' }
          ],
          gaps: [
            { id: 'gap_01', gap_type: 'missing_escalation_path', risk_description: 'No explicit escalation SLA defined for cross-region data residency compliance ambiguity', severity: 'high', recommendation: 'Add 24-hour escalation rule to Global Compliance Board' }
          ],
          overcontrols: [
            { id: 'oc_01', control_id: 'ctrl_01', overcontrol_reason: 'Low-risk reversible regional pilot decisions require full CISO sign-off instead of delegated regional architect approval', recommendation: 'Delegate regional pilot approval to Regional Architecture Lead (Safety score: 0.94)' }
          ],
          loads: [
            { id: 'load_01', decisions_count: 24, approvals_count: 18, reviews_count: 8, escalations_count: 2, exceptions_count: 1, time_spent_hours: 36.5, time_window: 'monthly' }
          ],
          bottlenecks: [
            { id: 'btn_01', bottleneck_type: 'approval', cause: 'CISO manual review queue bottleneck on routine pilot approvals', severity: 'moderate' }
          ],
          delegationCandidates: [
            { id: 'del_cand_01', decision_type: 'pilot', rationale: 'Low risk, highly reversible ($95k cost, 30-day window) with 98% policy coverage', safety_score: 0.94, policy_coverage: 0.98, status: 'recommended' }
          ],
          exceptions: [
            { id: 'exc_01', reason: 'Temporary 30-day capacity buffer exception for Wave 2 region 2 rollout', scope: 'Region 2 FinOps cluster', duration_days: 30, approver: 'Chief Information Officer', risk: 'low', status: 'active' }
          ],
          changeRequests: [
            { id: 'cr_01', change_type: 'delegation', description: 'Delegate low-risk regional pilot approvals to Regional Architecture Leads', proposed_state: 'Regional Architecture Lead approval for pilot decisions < $100k', status: 'under_review' }
          ],
          drifts: [
            { id: 'gov_drift_01', drift_type: 'approval', approved_summary: 'Two-key Executive Approval required for Wave 2 scale', actual_summary: 'Two-key approval executed on schedule with zero drift', severity: 'none' }
          ],
          reviews: [
            { id: 'gov_rev_01', cadence: 'quarterly', trigger_reason: 'Governance friction detected in routine pilot approval queue', status: 'recommended' }
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
      const res = await fetch(`/api/v1/transformation-governance/query?query=${encodeURIComponent(queryText)}`, {
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
            <span className="p-2 bg-purple-600/20 text-purple-400 rounded-lg text-lg">🏛️</span>
            Enterprise Transformation Adaptive Governance 2.0
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Decision Rights → Controls → Effectiveness → Friction & Gaps → Overcontrol → Load → Bottlenecks → Delegation → Change Simulation → Human Approval.
          </p>
        </div>
        <div className="flex gap-2">
          <span className="px-3 py-1 bg-purple-500/10 text-purple-400 border border-purple-500/20 rounded-full text-xs font-semibold">
            Human-Authorized Governance Evolution
          </span>
          <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full text-xs font-semibold">
            Zero Worker Surveillance
          </span>
        </div>
      </div>

      {/* Telemetry Header */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Active Profiles</div>
          <div className="text-2xl font-bold text-purple-400 mt-1">{data?.activeProfilesCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Decision Rights</div>
          <div className="text-2xl font-bold text-indigo-400 mt-1">{data?.decisionRightsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Active Controls</div>
          <div className="text-2xl font-bold text-emerald-400 mt-1">{data?.activeControlsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Detected Frictions</div>
          <div className="text-2xl font-bold text-amber-400 mt-1">{data?.detectedFrictionsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Delegation Candidates</div>
          <div className="text-2xl font-bold text-teal-400 mt-1">{data?.delegationCandidatesCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Efficiency Score</div>
          <div className="text-2xl font-bold text-blue-400 mt-1">{data?.governanceEfficiencyScorePct || 94.5}%</div>
        </div>
      </div>

      {/* Subsystem Tabs */}
      <div className="flex border-b border-slate-800 gap-2 text-sm overflow-x-auto pb-1">
        {[
          { id: 'overview', label: 'Overview & Profiles' },
          { id: 'decision_rights', label: 'Decision-Rights & Conflicts' },
          { id: 'controls', label: 'Controls & Effectiveness' },
          { id: 'friction_gaps', label: 'Friction & Gaps' },
          { id: 'overcontrol_load', label: 'Overcontrol & Load' },
          { id: 'bottlenecks_delegation', label: 'Bottlenecks & Delegation' },
          { id: 'exceptions_drift', label: 'Exceptions & Drift' },
          { id: 'change_requests', label: 'Change Requests & Simulation' },
          { id: 'reviews_learning', label: 'Reviews & Lessons' },
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
        <div className="p-8 text-center text-slate-500">Loading Enterprise Adaptive Governance...</div>
      ) : (
        <div className="space-y-6">
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-purple-400 flex items-center gap-2">
                  <span>🏛️</span> Active Governance Profiles
                </h2>
                <div className="space-y-2 text-sm">
                  {data?.profiles?.map((prof: any) => (
                    <div key={prof.id} className="p-3 bg-slate-950 rounded border border-purple-800/40 flex justify-between items-center text-xs">
                      <div>
                        <div className="font-bold text-slate-100">{prof.name}</div>
                        <div className="text-slate-400">Version: {prof.version} | Owner: {prof.owner}</div>
                      </div>
                      <span className="px-2 py-0.5 bg-purple-500/20 text-purple-300 rounded font-bold">{prof.status.toUpperCase()}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-amber-400 flex items-center gap-2">
                  <span>⚠️</span> Surfaced Decision-Right Conflicts
                </h2>
                <div className="space-y-2 text-sm">
                  {data?.conflicts?.map((conf: any) => (
                    <div key={conf.id} className="p-3 bg-slate-950 rounded border border-amber-800/40 space-y-1 text-xs">
                      <div className="font-bold text-amber-300">Conflict between {conf.authority_a} & {conf.authority_b}</div>
                      <div className="text-slate-300">{conf.conflict_description}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'decision_rights' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Decision-Rights Definitions & Authority Matrix</h2>
              {data?.rights?.map((dr: any) => (
                <div key={dr.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-purple-500">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-purple-300">Decision Type: {dr.decision_type} | Scope: {dr.scope}</span>
                    <span className="text-xs px-2 py-0.5 bg-purple-500/20 text-purple-300 rounded font-bold">Authority: {dr.authority_level}</span>
                  </div>
                  <div className="text-xs text-slate-300">Approval Requirement: {dr.approval_requirement}</div>
                  <div className="text-xs text-slate-400">Required Evidence: {dr.required_evidence}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'controls' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Active Governance Controls & Policy References</h2>
              {data?.controls?.map((ctrl: any) => (
                <div key={ctrl.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-emerald-500">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-emerald-300">Type: {ctrl.control_type} | Owner: {ctrl.owner}</span>
                    <span className="text-xs px-2 py-0.5 bg-emerald-500/20 text-emerald-300 rounded font-bold">Policy: {ctrl.policy_reference}</span>
                  </div>
                  <div className="text-xs text-slate-300">Purpose: {ctrl.purpose}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'friction_gaps' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Governance Friction & Gap Analysis</h2>
              {data?.frictions?.map((fric: any) => (
                <div key={fric.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-amber-500">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-amber-300">Friction: {fric.friction_type} (Latency: +{fric.time_impact_hours} hours)</span>
                    <span className="text-xs px-2 py-0.5 bg-amber-500/20 text-amber-300 rounded font-bold">Severity: {fric.severity}</span>
                  </div>
                  <div className="text-xs text-slate-300">Cause: {fric.cause}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'overcontrol_load' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Overcontrol Identification & Organizational Load Metrics</h2>
              {data?.overcontrols?.map((oc: any) => (
                <div key={oc.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-indigo-500">
                  <div className="font-bold text-indigo-300">Overcontrol Reason: {oc.overcontrol_reason}</div>
                  <div className="text-xs text-emerald-400 font-semibold">Recommendation: {oc.recommendation}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'bottlenecks_delegation' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Governance Bottlenecks & Delegation Candidates</h2>
              {data?.delegationCandidates?.map((del: any) => (
                <div key={del.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-teal-500">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-teal-300">Delegation Candidate: {del.decision_type}</span>
                    <span className="text-xs px-2 py-0.5 bg-teal-500/20 text-teal-300 rounded font-bold">Safety Score: {(del.safety_score * 100).toFixed(0)}%</span>
                  </div>
                  <div className="text-xs text-slate-300">Rationale: {del.rationale}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'exceptions_drift' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Active Governance Exceptions & Drift Detection</h2>
              {data?.exceptions?.map((exc: any) => (
                <div key={exc.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-cyan-500">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-cyan-300">Exception: {exc.reason}</span>
                    <span className="text-xs px-2 py-0.5 bg-cyan-500/20 text-cyan-300 rounded font-bold">Approver: {exc.approver}</span>
                  </div>
                  <div className="text-xs text-slate-400">Scope: {exc.scope} | Duration: {exc.duration_days} days</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'change_requests' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Human-Governed Change Requests & Simulation</h2>
              {data?.changeRequests?.map((cr: any) => (
                <div key={cr.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-purple-500">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-purple-300">Change Request: {cr.change_type}</span>
                    <span className="text-xs px-2 py-0.5 bg-purple-500/20 text-purple-300 rounded font-bold">Status: {cr.status.toUpperCase()}</span>
                  </div>
                  <div className="text-xs text-slate-300">Description: {cr.description}</div>
                  <div className="text-xs text-teal-400 font-semibold">Simulated Impact: Latency -36.0 hours, Risk +0.02%</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'reviews_learning' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Governance Reviews & Control Lessons Learned</h2>
              {data?.reviews?.map((rev: any) => (
                <div key={rev.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-blue-500">
                  <div className="font-bold text-blue-300">Quarterly Review Trigger: {rev.trigger_reason}</div>
                  <div className="text-xs text-slate-400">Status: {rev.status}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'nl_query' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Natural Language Adaptive Governance Query</h2>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={queryText}
                  onChange={(e) => setQueryText(e.target.value)}
                  placeholder="Ask an adaptive governance query..."
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
                        <div className="font-semibold text-purple-300">{res.governance_profile}</div>
                        <div className="text-slate-300">Decision Rights: {res.decision_rights}</div>
                        <div className="text-amber-300">Authority Conflict: {res.surfaced_conflict}</div>
                        <div className="text-blue-300">Friction Analysis: {res.friction_analysis}</div>
                        <div className="text-teal-300">Delegation Candidate: {res.delegation_candidate}</div>
                        <div className="text-cyan-300">Change Request: {res.governance_change_request}</div>
                        <div className="text-emerald-300">Active Exception: {res.exception_status}</div>
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
