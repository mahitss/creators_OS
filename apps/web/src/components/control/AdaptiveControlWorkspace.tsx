'use client';

import React, { useState, useEffect } from 'react';

export function AdaptiveControlWorkspace() {
  const [activeTab, setActiveTab] = useState<'overview' | 'loops' | 'signals' | 'reassessments' | 'guardrails' | 'responses' | 'outcomes' | 'nl_query'>('overview');
  const [overviewData, setOverviewData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('Which decisions are no longer valid?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/control');
      if (res.ok) {
        const data = await res.json();
        setOverviewData(data);
      } else {
        // Fallback seed data
        setOverviewData({
          loopsCount: 1,
          activeLoopsCount: 1,
          signalsCount: 1,
          guardrailsCount: 1,
          reassessmentsCount: 1,
          responsesCount: 1,
          observationsCount: 1,
          loopHealthScore: 0.98,
          loops: [
            {
              id: "loop_ctrl_01",
              name: "Enterprise Security SLA & Threat Remediation Control Loop",
              description: "Closed-loop monitoring of threat remediation latency, cluster node health, and model routing SLA.",
              target_entity_type: "infrastructure",
              target_entity_id: "infra_sec_cluster_01",
              mode: "monitor_only",
              status: "active",
              owner: "usr_sec_lead"
            }
          ],
          signals: [
            {
              id: "sig_ctrl_01",
              loop_id: "loop_ctrl_01",
              signal_type: "kpi",
              value: 215.0,
              signal_quality: "verified",
              confidence: "high",
              source: "Prometheus Telemetry Mesh",
              freshness: "fresh"
            }
          ],
          guardrails: [
            {
              id: "grd_01",
              loop_id: "loop_ctrl_01",
              guardrail_type: "max_delay",
              threshold: 300.0,
              severity: "high",
              action: "require_approval",
              approval_required: true,
              policy_reference: "policy_sec_sla_v2"
            }
          ],
          reassessments: [
            {
              id: "dreass_01",
              decision_id: "dec_01",
              trigger_type: "forecast_change",
              evidence: "Forecast predicts +25% latency increase in 14 days due to node capacity bottleneck.",
              affected_decision_id: "dec_01",
              recommended_next_step: "Request Executive Review & Re-optimization via Prescriptive Intelligence.",
              status: "pending"
            }
          ],
          responses: [
            {
              id: "cresp_01",
              loop_id: "loop_ctrl_01",
              response_type: "recommend",
              payload_json: { action: "Scale replica pool from 48 to 64 nodes", required_approval: "usr_sec_lead" },
              status: "proposed",
              confidence: "high"
            }
          ],
          observations: [
            {
              id: "aobs_01",
              action_id: "act_plan_01",
              expected_val: 210.0,
              actual_val: 204.0,
              variance: -6.0,
              outcome_class: "success"
            }
          ],
          regrets: [
            {
              id: "reg_01",
              decision_id: "dec_01",
              selected_option: "Option 1 (A100_SXM)",
              actual_outcome: 952.0,
              regret_score: 0.04,
              counterfactual_label: "simulated"
            }
          ],
          performances: [
            {
              id: "cperf_01",
              loop_id: "loop_ctrl_01",
              false_alerts: 0,
              missed_alerts: 0,
              successful_interventions: 14,
              unnecessary_interventions: 1,
              reassessment_frequency: 0.8,
              health_score: 0.98
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

  const handleQuery = async () => {
    if (!queryText.trim()) return;
    setQueryLoading(true);
    try {
      const res = await fetch(`/api/v1/control/query?query=${encodeURIComponent(queryText)}`, {
        method: 'POST'
      });
      if (res.ok) {
        const data = await res.json();
        setQueryResult(data);
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
            <span className="p-2 bg-emerald-600/20 text-emerald-400 rounded-lg text-lg">🔄</span>
            Enterprise Adaptive Decision Governance & Closed-Loop Control 2.0
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Governed closed-loop operating cycle (Observe → Measure → Forecast → Optimize → Recommend → Decide → Approve → Act → Verify → Learn → Reassess).
          </p>
        </div>
        <div className="flex gap-2">
          <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full text-xs font-semibold flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            Control Loop Active
          </span>
          <span className="px-3 py-1 bg-amber-500/10 text-amber-400 border border-amber-500/20 rounded-full text-xs font-semibold">
            Monitor-Only Mode Default
          </span>
        </div>
      </div>

      {/* Telemetry Bar */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Control Loops</div>
          <div className="text-2xl font-bold text-slate-100 mt-1">{overviewData?.loopsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Active Signals</div>
          <div className="text-2xl font-bold text-indigo-400 mt-1">{overviewData?.signalsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Active Guardrails</div>
          <div className="text-2xl font-bold text-purple-400 mt-1">{overviewData?.guardrailsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Reassessments</div>
          <div className="text-2xl font-bold text-amber-400 mt-1">{overviewData?.reassessmentsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Governed Responses</div>
          <div className="text-2xl font-bold text-emerald-400 mt-1">{overviewData?.responsesCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Control Health</div>
          <div className="text-2xl font-bold text-cyan-400 mt-1">{((overviewData?.loopHealthScore || 0) * 100).toFixed(0)}%</div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 gap-2 text-sm overflow-x-auto pb-1">
        {[
          { id: 'overview', label: 'Control Overview' },
          { id: 'loops', label: 'Control Loops & Modes' },
          { id: 'signals', label: 'Real-Time Signals' },
          { id: 'reassessments', label: 'Decision Reassessments' },
          { id: 'guardrails', label: 'Operational Guardrails' },
          { id: 'responses', label: 'Responses & Actions' },
          { id: 'outcomes', label: 'Post-Action Verification' },
          { id: 'nl_query', label: 'Natural Language Query' }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-2 font-medium rounded-t-lg transition-colors whitespace-nowrap ${
              activeTab === tab.id
                ? 'bg-slate-900 text-emerald-400 border-b-2 border-emerald-500'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/40'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      {loading ? (
        <div className="p-8 text-center text-slate-500">Loading Adaptive Control state...</div>
      ) : (
        <div className="space-y-6">
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-emerald-400 flex items-center gap-2">
                  <span>🔄</span> Active Control Loop
                </h2>
                {overviewData?.loops?.[0] && (
                  <div className="space-y-3 text-sm">
                    <div className="font-medium text-slate-200">{overviewData.loops[0].name}</div>
                    <p className="text-slate-400">{overviewData.loops[0].description}</p>
                    <div className="grid grid-cols-2 gap-2 text-xs pt-2">
                      <span className="p-2 bg-slate-800/60 rounded">Mode: <strong className="text-amber-300">{overviewData.loops[0].mode}</strong></span>
                      <span className="p-2 bg-slate-800/60 rounded">Owner: <strong className="text-slate-300">{overviewData.loops[0].owner}</strong></span>
                    </div>
                  </div>
                )}
              </div>

              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-amber-400 flex items-center gap-2">
                  <span>🚨</span> Pending Decision Reassessment
                </h2>
                {overviewData?.reassessments?.[0] && (
                  <div className="space-y-3 text-sm">
                    <div className="text-slate-300">{overviewData.reassessments[0].evidence}</div>
                    <div className="p-3 bg-amber-950/30 border border-amber-800/40 rounded-lg text-amber-300 text-xs">
                      {overviewData.reassessments[0].recommended_next_step}
                    </div>
                    <div className="text-xs text-slate-400">
                      Trigger: <span className="text-slate-200 font-semibold">{overviewData.reassessments[0].trigger_type}</span> | Status: <span className="text-amber-400 font-semibold">{overviewData.reassessments[0].status}</span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'loops' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Registered Control Loops & Modes</h2>
              <div className="divide-y divide-slate-800">
                {overviewData?.loops?.map((l: any) => (
                  <div key={l.id} className="py-4 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="font-semibold text-emerald-300">{l.name}</span>
                      <span className="px-2 py-1 bg-amber-500/10 text-amber-400 text-xs rounded font-mono">{l.mode}</span>
                    </div>
                    <p className="text-sm text-slate-400">{l.description}</p>
                    <div className="text-xs text-slate-500">Target Entity: {l.target_entity_type} ({l.target_entity_id}) | Status: {l.status}</div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'signals' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Real-Time Ingested Control Signals</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {overviewData?.signals?.map((sig: any) => (
                  <div key={sig.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                    <div className="flex justify-between items-center">
                      <span className="font-semibold text-indigo-300">Signal: {sig.signal_type}</span>
                      <span className="text-xs px-2 py-0.5 bg-emerald-500/10 text-emerald-400 rounded">{sig.signal_quality}</span>
                    </div>
                    <div className="text-2xl font-bold text-slate-100">{sig.value}</div>
                    <div className="text-xs text-slate-400">Source: {sig.source} | Freshness: {sig.freshness}</div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'reassessments' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Decision Validity Assessments & Reassessments</h2>
              {overviewData?.reassessments?.map((reass: any) => (
                <div key={reass.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-amber-300">Reassessment {reass.id}</span>
                    <span className="px-3 py-1 bg-amber-500/20 text-amber-300 rounded text-xs">{reass.status}</span>
                  </div>
                  <p className="text-slate-300">{reass.evidence}</p>
                  <div className="p-3 bg-slate-900 rounded text-xs text-slate-400 space-y-1">
                    <div><strong>Trigger:</strong> {reass.trigger_type}</div>
                    <div><strong>Next Step:</strong> {reass.recommended_next_step}</div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'guardrails' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Operational Control Guardrails</h2>
              {overviewData?.guardrails?.map((g: any) => (
                <div key={g.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-purple-300">Guardrail: {g.guardrail_type}</span>
                    <span className="text-xs px-2 py-0.5 bg-red-500/10 text-red-400 rounded">Threshold: {g.threshold}</span>
                  </div>
                  <div className="grid grid-cols-2 gap-2 text-xs text-slate-400 pt-1">
                    <span>Severity: <strong className="text-slate-200">{g.severity}</strong></span>
                    <span>Action: <strong className="text-slate-200">{g.action}</strong></span>
                    <span>Approval Required: <strong className="text-amber-400">{g.approval_required ? 'YES' : 'NO'}</strong></span>
                    <span>Policy: <strong className="text-slate-200">{g.policy_reference}</strong></span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'responses' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Governed Control Responses</h2>
              {overviewData?.responses?.map((r: any) => (
                <div key={r.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-emerald-400">Response Type: {r.response_type}</span>
                    <span className="text-xs px-2 py-0.5 bg-indigo-500/10 text-indigo-400 rounded">{r.status}</span>
                  </div>
                  <pre className="text-xs bg-slate-900 p-2 rounded text-slate-300">{JSON.stringify(r.payload_json, null, 2)}</pre>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'outcomes' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Post-Action Verification & Regret Analysis</h2>
              {overviewData?.observations?.map((obs: any) => (
                <div key={obs.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-cyan-300">Observation ID: {obs.id}</span>
                    <span className="text-xs px-2 py-0.5 bg-emerald-500/10 text-emerald-400 rounded">{obs.outcome_class}</span>
                  </div>
                  <div className="grid grid-cols-3 gap-2 text-xs text-slate-400 pt-1">
                    <span>Expected: <strong className="text-slate-200">{obs.expected_val}</strong></span>
                    <span>Actual: <strong className="text-emerald-400">{obs.actual_val}</strong></span>
                    <span>Variance: <strong className="text-slate-200">{obs.variance}</strong></span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'nl_query' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Natural Language Control Query Interface</h2>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={queryText}
                  onChange={(e) => setQueryText(e.target.value)}
                  placeholder="Ask a control loop query..."
                  className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-sm text-slate-100 focus:outline-none focus:border-emerald-500"
                />
                <button
                  onClick={handleQuery}
                  disabled={queryLoading}
                  className="px-5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-medium rounded-lg text-sm transition-colors"
                >
                  {queryLoading ? 'Evaluating...' : 'Query'}
                </button>
              </div>

              {queryResult && (
                <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                  <div className="text-xs text-emerald-400 font-semibold">Query: {queryResult.query}</div>
                  <div className="space-y-2">
                    {queryResult.results?.map((res: any, idx: number) => (
                      <div key={idx} className="p-3 bg-slate-900 rounded space-y-1 text-xs">
                        <div className="font-semibold text-slate-200">{res.control_loop}</div>
                        <div className="text-emerald-400">Mode: {res.mode} | Status: {res.status}</div>
                        <div className="text-slate-400">{res.latest_signal}</div>
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
