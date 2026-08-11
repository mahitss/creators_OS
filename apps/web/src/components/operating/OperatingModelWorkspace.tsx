'use client';

import React, { useState, useEffect } from 'react';

export function OperatingModelWorkspace() {
  const [activeTab, setActiveTab] = useState<'overview' | 'units' | 'decision_rights' | 'processes' | 'handoffs' | 'gaps' | 'drift' | 'proposals' | 'nl_query'>('overview');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('Where are our biggest operating bottlenecks?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);
  const [approvalMsg, setApprovalMsg] = useState<string | null>(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/operating-model');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      } else {
        // Fallback seed structure
        setData({
          modelsCount: 1,
          unitsCount: 2,
          decisionRightsCount: 1,
          processesCount: 1,
          activeHandoffFrictionsCount: 1,
          operatingGapsCount: 1,
          formalVsObservedDriftsCount: 1,
          proposedChangeProposalsCount: 1,
          overallOperatingEfficiencyIndex: 0.89,
          models: [
            {
              id: 'opmod_01',
              name: 'Enterprise Autonomous Cognitive Operating Model 2.0',
              description: 'Cross-functional matrix operating model integrating AI Agent DAGs and Human Executive Decision Rights.',
              version: 'v2.0',
              status: 'active',
              owner: 'usr_chief_operating_officer'
            }
          ],
          units: [
            {
              id: 'unit_eng_01',
              name: 'Autonomous Systems & Engineering Division',
              type: 'division',
              purpose: 'Design, build, and optimize enterprise autonomous AI agent DAGs.',
              scope: 'Global engineering, cloud architecture, and model gateway infrastructure',
              status: 'active'
            },
            {
              id: 'unit_sec_01',
              name: 'Enterprise Security & Compliance Governance',
              type: 'shared_service',
              purpose: 'Enforce Zero-Trust access, DLP boundaries, and compliance monitoring.',
              scope: 'Enterprise security operations and privacy enforcement',
              status: 'active'
            }
          ],
          decisionRights: [
            {
              id: 'dright_01',
              decision_type: 'portfolio_reconfiguration',
              scope: 'Capital reallocations over $100k and strategic initiative re-sequencing',
              authority_level: 'executive_leadership',
              escalation_path: 'Chief Operating Officer -> Board Executive Committee'
            }
          ],
          matrices: [
            {
              id: 'matrix_01',
              decision_right_id: 'dright_01',
              unit_id: 'unit_eng_01',
              role_type: 'recommends'
            }
          ],
          processes: [
            {
              id: 'proc_agent_deployment_01',
              name: 'Agent Skill Fabric Certification & Deployment',
              purpose: 'Validate sub-agent capabilities, test against DLP sandbox, and deploy to production mesh.',
              owner_unit_id: 'unit_eng_01',
              status: 'active'
            }
          ],
          handoffs: [
            {
              id: 'handoff_01',
              process_id: 'proc_agent_deployment_01',
              from_unit_id: 'unit_eng_01',
              to_unit_id: 'unit_sec_01',
              artifact_name: 'Security Compliance Audit Package',
              wait_time_hours: 14.5,
              failure_rate: 0.04,
              friction_flag: true
            }
          ],
          gaps: [
            {
              id: 'opgap_01',
              gap_type: 'decision',
              description: 'Decision latency bottleneck: Security audit handoffs between Engineering and Compliance require 14.5h average wait time.',
              severity: 'medium'
            }
          ],
          drifts: [
            {
              id: 'opdrift_01',
              documented_behavior: 'Formal documentation states Security Audit approval occurs in PolicyEngine within 1 hour.',
              observed_behavior: 'Observed Operating Graph telemetry indicates manual cross-department reviews delay approvals by 14.5h.',
              difference_summary: 'Formal process assumes automated approval; actual behavior relies on manual review bottleneck.',
              confidence: 'high',
              severity: 'medium'
            }
          ],
          changeProposals: [
            {
              id: 'opprop_01',
              problem_summary: 'Automate routine Security Compliance Audit verification via ActionGateway pre-signed attestations.',
              evidence_json: { observed_wait_time: '14.5h -> estimated 0.2h' },
              expected_effect: 'Reduce agent skill deployment cycle time from 16h to sub-1h while maintaining 100% compliance.',
              status: 'proposed'
            }
          ]
        });
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleApproveProposal = async (proposalId: string) => {
    try {
      const res = await fetch(`/api/v1/operating-model/change-proposals/${proposalId}/approve`, {
        method: 'POST'
      });
      if (res.ok) {
        const json = await res.json();
        setApprovalMsg(json.message);
        fetchData();
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleQuery = async () => {
    if (!queryText.trim()) return;
    setQueryLoading(true);
    try {
      const res = await fetch(`/api/v1/operating-model/query?query=${encodeURIComponent(queryText)}`, {
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
            <span className="p-2 bg-teal-600/20 text-teal-400 rounded-lg text-lg">⚙️</span>
            Enterprise Organizational Operating Intelligence 2.0
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Strategy → Operating Model → Capabilities → Org Units → Decision Rights → Processes → Handoffs → Execution → Outcomes.
          </p>
        </div>
        <div className="flex gap-2">
          <span className="px-3 py-1 bg-teal-500/10 text-teal-400 border border-teal-500/20 rounded-full text-xs font-semibold">
            Operating Systems Analysis
          </span>
          <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full text-xs font-semibold">
            Human Approval Governed
          </span>
        </div>
      </div>

      {/* Telemetry Header */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Operating Model</div>
          <div className="text-2xl font-bold text-slate-100 mt-1">{data?.modelsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Org Units</div>
          <div className="text-2xl font-bold text-teal-400 mt-1">{data?.unitsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Efficiency Index</div>
          <div className="text-2xl font-bold text-emerald-400 mt-1">{data?.overallOperatingEfficiencyIndex || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Handoff Frictions</div>
          <div className="text-2xl font-bold text-rose-400 mt-1">{data?.activeHandoffFrictionsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Formal vs Observed Drift</div>
          <div className="text-2xl font-bold text-amber-400 mt-1">{data?.formalVsObservedDriftsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Change Proposals</div>
          <div className="text-2xl font-bold text-purple-400 mt-1">{data?.proposedChangeProposalsCount || 0}</div>
        </div>
      </div>

      {/* Approval Notification Banner */}
      {approvalMsg && (
        <div className="p-4 bg-emerald-950/50 border border-emerald-800/60 rounded-xl text-emerald-300 text-sm flex justify-between items-center">
          <span>✅ {approvalMsg}</span>
          <button onClick={() => setApprovalMsg(null)} className="text-xs text-slate-400 hover:text-white">Dismiss</button>
        </div>
      )}

      {/* Subsystem Tabs */}
      <div className="flex border-b border-slate-800 gap-2 text-sm overflow-x-auto pb-1">
        {[
          { id: 'overview', label: 'Operating Overview' },
          { id: 'units', label: 'Org Units & Hierarchy' },
          { id: 'decision_rights', label: 'Decision Rights Matrix' },
          { id: 'processes', label: 'Processes & Steps' },
          { id: 'handoffs', label: 'Handoff Frictions' },
          { id: 'gaps', label: 'Operating Gaps' },
          { id: 'drift', label: 'Formal vs Observed Drift' },
          { id: 'proposals', label: 'Change Proposals' },
          { id: 'nl_query', label: 'Natural Language Query' }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-2 font-medium rounded-t-lg transition-colors whitespace-nowrap ${
              activeTab === tab.id
                ? 'bg-slate-900 text-teal-400 border-b-2 border-teal-500'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/40'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Content */}
      {loading ? (
        <div className="p-8 text-center text-slate-500">Loading Operating Model state...</div>
      ) : (
        <div className="space-y-6">
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-teal-400 flex items-center gap-2">
                  <span>🏢</span> Active Operating Model
                </h2>
                {data?.models?.[0] && (
                  <div className="space-y-3 text-sm">
                    <div className="font-bold text-slate-100">{data.models[0].name} ({data.models[0].version})</div>
                    <div className="p-3 bg-slate-950 rounded border border-teal-800/40 text-teal-300 text-xs">
                      {data.models[0].description}
                    </div>
                    <div className="flex justify-between items-center text-xs text-slate-400">
                      <span>Owner: {data.models[0].owner}</span>
                      <span className="px-2 py-0.5 bg-emerald-500/20 text-emerald-400 rounded font-bold">{data.models[0].status}</span>
                    </div>
                  </div>
                )}
              </div>

              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-amber-400 flex items-center gap-2">
                  <span>📡</span> Formal vs Observed Operating Drift
                </h2>
                {data?.drifts?.[0] && (
                  <div className="space-y-3 text-sm">
                    <div className="font-bold text-slate-100">{data.drifts[0].difference_summary}</div>
                    <div className="p-3 bg-slate-950 rounded border border-amber-800/40 text-amber-300 text-xs">
                      <strong>Documented:</strong> {data.drifts[0].documented_behavior}<br/>
                      <strong>Observed:</strong> {data.drifts[0].observed_behavior}
                    </div>
                    <span className="inline-block px-2 py-0.5 bg-amber-500/20 text-amber-300 rounded text-xs font-bold">
                      Confidence: {data.drifts[0].confidence}
                    </span>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'units' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Organizational Units & Structural Scope</h2>
              {data?.units?.map((u: any) => (
                <div key={u.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-teal-300">{u.name}</span>
                    <span className="text-xs px-2 py-0.5 bg-teal-500/20 text-teal-300 rounded font-bold">Type: {u.type}</span>
                  </div>
                  <p className="text-xs text-slate-300">Purpose: {u.purpose}</p>
                  <div className="text-xs text-slate-400">Scope: {u.scope}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'decision_rights' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Decision Rights Matrix (RACI Governance)</h2>
              {data?.decisionRights?.map((dr: any) => (
                <div key={dr.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-teal-300">Decision: {dr.decision_type}</span>
                    <span className="text-xs px-2 py-0.5 bg-purple-500/20 text-purple-300 rounded font-bold">Authority: {dr.authority_level}</span>
                  </div>
                  <p className="text-xs text-slate-300">Scope: {dr.scope}</p>
                  <div className="text-xs text-indigo-400">Escalation Path: {dr.escalation_path}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'processes' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Operating Processes & Systems Integration</h2>
              {data?.processes?.map((pr: any) => (
                <div key={pr.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-teal-300">{pr.name}</span>
                    <span className="text-xs px-2 py-0.5 bg-emerald-500/20 text-emerald-400 rounded font-bold">{pr.status}</span>
                  </div>
                  <p className="text-xs text-slate-300">{pr.purpose}</p>
                  <div className="text-xs text-slate-400">Owner Unit: {pr.owner_unit_id}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'handoffs' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Inter-Unit Process Handoffs & Friction Flags</h2>
              {data?.handoffs?.map((ho: any) => (
                <div key={ho.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm border-l-4 border-l-rose-500">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-rose-300">Artifact: {ho.artifact_name}</span>
                    <span className="text-xs px-2 py-0.5 bg-rose-500/20 text-rose-300 rounded font-bold">Wait Time: {ho.wait_time_hours}h</span>
                  </div>
                  <div className="text-xs text-slate-400">Handoff: {ho.from_unit_id} → {ho.to_unit_id}</div>
                  <div className="text-xs text-amber-400">Failure Rate: {(ho.failure_rate * 100).toFixed(1)}%</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'gaps' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Operating Model Structural Gaps</h2>
              {data?.gaps?.map((gp: any) => (
                <div key={gp.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-amber-500">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-amber-300">Gap Type: {gp.gap_type}</span>
                    <span className="text-xs px-2 py-0.5 bg-amber-500/20 text-amber-300 rounded font-bold">Severity: {gp.severity}</span>
                  </div>
                  <p className="text-xs text-slate-300">{gp.description}</p>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'drift' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Formal vs Observed Operating Behavior Signals</h2>
              {data?.drifts?.map((dr: any) => (
                <div key={dr.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                  <div className="font-bold text-slate-100">{dr.difference_summary}</div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
                    <div className="p-2 bg-slate-900 rounded text-slate-300">Documented: {dr.documented_behavior}</div>
                    <div className="p-2 bg-slate-900 rounded text-amber-300">Observed: {dr.observed_behavior}</div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'proposals' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Operating Model Change Proposals (Human Authorization Governed)</h2>
              {data?.changeProposals?.map((cp: any) => (
                <div key={cp.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-purple-300">Proposal ID: {cp.id}</span>
                    <span className={`text-xs px-2 py-0.5 rounded font-bold ${
                      cp.status === 'approved' ? 'bg-emerald-500/20 text-emerald-300' : 'bg-purple-500/20 text-purple-300'
                    }`}>
                      {cp.status}
                    </span>
                  </div>
                  <p className="text-xs text-slate-300">Problem: {cp.problem_summary}</p>
                  <div className="text-xs text-emerald-400">Expected Effect: {cp.expected_effect}</div>

                  {cp.status === 'proposed' && (
                    <button
                      onClick={() => handleApproveProposal(cp.id)}
                      className="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold rounded transition-colors"
                    >
                      Authorize Operating Model Change Proposal
                    </button>
                  )}
                </div>
              ))}
            </div>
          )}

          {activeTab === 'nl_query' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Natural Language Operating Query Interface</h2>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={queryText}
                  onChange={(e) => setQueryText(e.target.value)}
                  placeholder="Ask an operating model query..."
                  className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-sm text-slate-100 focus:outline-none focus:border-teal-500"
                />
                <button
                  onClick={handleQuery}
                  disabled={queryLoading}
                  className="px-5 py-2 bg-teal-600 hover:bg-teal-500 text-white font-medium rounded-lg text-sm transition-colors"
                >
                  {queryLoading ? 'Evaluating...' : 'Query'}
                </button>
              </div>

              {queryResult && (
                <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                  <div className="text-xs text-teal-400 font-semibold">Query: {queryResult.query}</div>
                  <div className="space-y-2">
                    {queryResult.results?.map((res: any, idx: number) => (
                      <div key={idx} className="p-3 bg-slate-900 rounded space-y-1 text-xs">
                        <div className="font-semibold text-slate-200">{res.model_name}</div>
                        <div className="text-teal-300">Org Units: {res.org_units}</div>
                        <div className="text-indigo-300">Decision Rights: {res.decision_rights}</div>
                        <div className="text-rose-400">Handoff Friction: {res.handoff_friction}</div>
                        <div className="text-amber-400">Formal vs Observed Drift: {res.formal_vs_observed_drift}</div>
                        <div className="text-purple-300">Change Proposal: {res.change_proposal}</div>
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
