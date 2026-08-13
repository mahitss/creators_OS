'use client';

import React, { useState, useEffect } from 'react';

export function TransformationResilienceDecisionLifecycleWorkspace() {
  const [activeTab, setActiveTab] = useState<'queue' | 'questions' | 'evidence' | 'options' | 'scenarios' | 'tradeoffs' | 'recommendations' | 'approvals' | 'decisions' | 'execution' | 'verification' | 'learning' | 'query'>('queue');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('What resilience decisions need attention and what evidence supports option A?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/transformation-resilience-decisions');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      } else {
        // Fallback seed data
        setData({
          domainsCount: 1,
          questionsCount: 1,
          decisionsCount: 1,
          optionsCount: 3,
          evidencePacksCount: 1,
          precedentsCount: 1,
          domains: [
            { id: 'dec_dom_01', name: 'Global Enterprise Governed Resilience Decision OS 2.0', owner: 'Principal Enterprise Decision Governance Architect', status: 'active', version: 'v2.0' }
          ],
          questions: [
            { id: 'dec_q_01', question: 'Should Enterprise Board approve $350,000 funding for pinv_01 Active-Active IAM Gateway deployment?', trigger: 'warning', deadline: '2026-Q3', decision_owner: 'Chief Resilience Officer' }
          ],
          evidencePacks: [
            { id: 'dec_ev_01', source: 'EventMesh.IdentityGateway + ResilienceSensingEngine', quality: 0.95, confidence: 0.94 }
          ],
          assumptions: [
            { id: 'dec_assm_01', assumption: 'Secondary Multi-Cloud region latency remains under 35ms overhead.', sensitivity: 'critical', status: 'valid' }
          ],
          options: [
            { id: 'opt_01', title: 'Option A: Full Active-Active Multi-Region IAM Deployment (Recommended)', cost: 350000.0, optionality_score: 0.96 },
            { id: 'opt_02', title: 'Option B: Rate Limiting Cluster Only', cost: 150000.0, optionality_score: 0.72 },
            { id: 'opt_03', title: 'Option C: Do Nothing (Maintain Baseline)', cost: 0.0, optionality_score: 0.40 }
          ],
          tradeoffs: [
            { id: 'dec_to_01', tradeoff_matrix_json: { comparison: [{ option: 'Option A', cost: 350000, risk_reduction: '65%' }] } }
          ],
          recommendations: [
            { id: 'dec_rec_01', label: 'RECOMMENDATION - NOT DECISION', recommended_option_id: 'opt_01', required_approval: 'PolicyEngine + Enterprise Board' }
          ],
          decisions: [
            { id: 'dec_res_01', decision_title: 'Active-Active Multi-Region Identity Gateway Architecture & Funding Decision', owner: 'Chief Resilience Officer', status: 'pending_decision', deadline: '2026-Q3' }
          ],
          executionPlans: [
            { id: 'dec_exec_01', owner: 'Lead Cloud Infrastructure Engineer', rollback_strategy: 'Automated traffic drain back to Region A within 30 seconds.' }
          ],
          verifications: [
            { id: 'dec_verif_01', variance_pct: 2.1, confidence: 0.96 }
          ],
          precedents: [
            { id: 'dec_prec_01', prior_decision_id: 'dec_hist_2025_04', context_description: '2025 SSO Cluster Multi-Region Expansion', applicability: 0.92 }
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
      const res = await fetch(`/api/v1/transformation-resilience-decisions/query?query=${encodeURIComponent(queryText)}`, {
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
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400">
              Governed Resilience Decision Operating System 2.0
            </h1>
            <span className="px-3 py-1 text-xs font-semibold rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20">
              Human Decision Authority Absolute
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Structured, evidence-backed decision lifecycle converting sensing intelligence into human-governed execution.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={fetchData}
            className="px-4 py-2 text-xs font-medium rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition"
          >
            Refresh Decision Queue
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Decision Domain</p>
          <p className="text-xl font-bold text-blue-400 mt-1">{data?.domainsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Active Questions</p>
          <p className="text-xl font-bold text-indigo-400 mt-1">{data?.questionsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Pending Decisions</p>
          <p className="text-xl font-bold text-amber-400 mt-1">{data?.decisionsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Evaluated Options</p>
          <p className="text-xl font-bold text-cyan-400 mt-1">{data?.optionsCount ?? 3}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Evidence Quality</p>
          <p className="text-xl font-bold text-emerald-400 mt-1">95%</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Sensitivity</p>
          <p className="text-xl font-bold text-rose-400 mt-1">Critical</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Verification Variance</p>
          <p className="text-xl font-bold text-teal-400 mt-1">2.1%</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Precedents</p>
          <p className="text-xl font-bold text-purple-400 mt-1">{data?.precedentsCount ?? 1}</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 overflow-x-auto space-x-2 scrollbar-none">
        {[
          { id: 'queue', label: 'Executive Decision Queue' },
          { id: 'questions', label: 'Decision Questions & Context' },
          { id: 'evidence', label: 'Evidence Packs & Assumptions' },
          { id: 'options', label: 'Option Analysis' },
          { id: 'scenarios', label: 'Scenario Set Comparison' },
          { id: 'tradeoffs', label: 'Trade-Off Matrix' },
          { id: 'recommendations', label: 'Analytical Recommendations' },
          { id: 'approvals', label: 'Approval Routing' },
          { id: 'decisions', label: 'Decisions & Consequences' },
          { id: 'execution', label: 'ActionGateway Execution' },
          { id: 'verification', label: 'Verification & Effectiveness' },
          { id: 'learning', label: 'Historical Precedents & Learning' },
          { id: 'query', label: 'Natural Language Decision Query' }
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
            Framing decision questions, loading context snapshots, and gathering evidence...
          </div>
        ) : (
          <>
            {activeTab === 'queue' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Executive Decision Queue</h3>
                {data?.decisions?.map((d: any) => (
                  <div key={d.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 flex justify-between items-center">
                    <div>
                      <span className="font-semibold text-blue-400">{d.decision_title}</span>
                      <p className="text-xs text-slate-400 mt-1">Owner: {d.owner} | Deadline: {d.deadline}</p>
                    </div>
                    <span className="text-xs px-3 py-1 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20 font-semibold">{d.status}</span>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'questions' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Decision Questions & Trigger Context</h3>
                {data?.questions?.map((q: any) => (
                  <div key={q.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <span className="text-sm font-semibold text-slate-200">{q.question}</span>
                    <p className="text-xs text-slate-400">Trigger: {q.trigger} | Owner: {q.decision_owner} | Deadline: {q.deadline}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'evidence' && (
              <div className="space-y-6">
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                  <span className="text-sm font-semibold text-emerald-400">Versioned Evidence Pack</span>
                  <p className="text-xs text-slate-400">Source: {data?.evidencePacks?.[0]?.source}</p>
                  <p className="text-xs text-slate-400">Quality: {( (data?.evidencePacks?.[0]?.quality ?? 0.95) * 100 ).toFixed(0)}% | Confidence: {( (data?.evidencePacks?.[0]?.confidence ?? 0.94) * 100 ).toFixed(0)}%</p>
                </div>

                <div className="space-y-3">
                  <h4 className="text-xs font-semibold text-slate-200">Key Assumptions & Sensitivity</h4>
                  {data?.assumptions?.map((a: any) => (
                    <div key={a.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 flex justify-between items-center">
                      <div>
                        <span className="text-xs text-slate-300 font-medium">{a.assumption}</span>
                        <p className="text-[10px] text-slate-400 mt-0.5">Status: {a.status}</p>
                      </div>
                      <span className="text-xs px-2.5 py-1 rounded bg-rose-500/10 text-rose-400 border border-rose-500/20 font-semibold">{a.sensitivity}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'options' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Options Analysis</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {data?.options?.map((opt: any) => (
                    <div key={opt.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                      <span className="text-sm font-semibold text-cyan-400">{opt.title}</span>
                      <p className="text-xs text-slate-300">Cost: ${opt.cost?.toLocaleString()}</p>
                      <p className="text-xs text-slate-400">Optionality Score: {(opt.optionality_score * 100).toFixed(0)}%</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'scenarios' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Scenario Set Evaluation</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                  <p className="text-xs text-slate-300 font-medium">Evaluated Scenarios: baseline, stress, severe, multi-failure, capacity-constrained</p>
                  <p className="text-xs text-slate-400">Option A Robustness under Severe Stress: 96.0%</p>
                  <p className="text-xs text-slate-400">Option B Robustness under Severe Stress: 81.0%</p>
                  <p className="text-xs text-slate-400">Option C Robustness under Severe Stress: 54.0%</p>
                </div>
              </div>
            )}

            {activeTab === 'tradeoffs' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Trade-Off Matrix</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                  <table className="w-full text-left text-xs text-slate-300">
                    <thead>
                      <tr className="border-b border-slate-800 text-slate-400">
                        <th className="pb-2">Option</th>
                        <th className="pb-2">Cost</th>
                        <th className="pb-2">Risk Reduction</th>
                        <th className="pb-2">Optionality</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr className="border-b border-slate-900">
                        <td className="py-2 font-medium text-cyan-400">Option A: Full Active-Active</td>
                        <td className="py-2">$350,000</td>
                        <td className="py-2 text-emerald-400">65%</td>
                        <td className="py-2">0.96</td>
                      </tr>
                      <tr className="border-b border-slate-900">
                        <td className="py-2 font-medium text-slate-300">Option B: Rate Limiter</td>
                        <td className="py-2">$150,000</td>
                        <td className="py-2 text-amber-400">25%</td>
                        <td className="py-2">0.72</td>
                      </tr>
                      <tr>
                        <td className="py-2 font-medium text-rose-400">Option C: Do Nothing</td>
                        <td className="py-2">$0</td>
                        <td className="py-2 text-rose-400">0%</td>
                        <td className="py-2">0.40</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {activeTab === 'recommendations' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Analytical Recommendation Engine</h3>
                {data?.recommendations?.map((rec: any) => (
                  <div key={rec.id} className="p-4 rounded-xl bg-slate-950/60 border border-indigo-500/30 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="px-3 py-1 text-xs font-bold rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">{rec.label}</span>
                      <span className="text-xs text-slate-400">Approval Required: {rec.required_approval}</span>
                    </div>
                    <p className="text-xs text-slate-300">Recommended Option: Option A (Full Active-Active Deployment)</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'approvals' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Integrated Approval Routing</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                  <p className="text-xs text-slate-300">Approver: PolicyEngine | Status: Approved</p>
                  <p className="text-xs text-slate-300">Approver: Enterprise Executive Board | Status: Pending Review (Condition: Budget Validation)</p>
                </div>
              </div>
            )}

            {activeTab === 'decisions' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Authorized Decision & Consequences</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                  <span className="text-sm font-semibold text-blue-400">Selected Option: Option A ($350,000 Active-Active Deployment)</span>
                  <p className="text-xs text-slate-300">Decision Owner: Chief Resilience Officer</p>
                  <p className="text-xs text-amber-400">Delay Consequence: $12,500/day risk burn with 3.5 weeks cascading delay across Wave 2 & Wave 4.</p>
                </div>
              </div>
            )}

            {activeTab === 'execution' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">ActionGateway Governed Execution</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                  <p className="text-xs text-slate-300 font-medium">Execution Target: ActionGateway Universal Dispatcher</p>
                  <p className="text-xs text-slate-400">Rollback Strategy: Automated traffic drain back to Region A within 30 seconds.</p>
                </div>
              </div>
            )}

            {activeTab === 'verification' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Verification & Effectiveness Ratings</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                  <p className="text-xs text-emerald-400 font-semibold">Observed Latency P99: 42.0ms (Expected: 45.0ms)</p>
                  <p className="text-xs text-slate-300">Variance: 2.1% | Confidence: 96.0%</p>
                  <p className="text-xs text-slate-400">Risk Reduction Achieved: 65.0%</p>
                </div>
              </div>
            )}

            {activeTab === 'learning' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Historical Precedents & Learning</h3>
                {data?.precedents?.map((prec: any) => (
                  <div key={prec.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <span className="text-sm font-semibold text-purple-400">{prec.context_description}</span>
                    <p className="text-xs text-slate-300">Applicability Rating: {(prec.applicability * 100).toFixed(0)}%</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'query' && (
              <div className="space-y-6">
                <h3 className="text-base font-semibold text-slate-200">Natural Language Decision Lifecycle Query</h3>
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={queryText}
                    onChange={(e) => setQueryText(e.target.value)}
                    placeholder="Ask a decision question, evidence request, or option comparison..."
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
                      <span className="text-xs font-semibold text-blue-400">Decision Query Result</span>
                      <span className="text-xs text-slate-400">Confidence: {queryResult.confidencePct}%</span>
                    </div>
                    {queryResult.evidenceJson?.error ? (
                      <div className="text-xs text-rose-400 font-semibold">{queryResult.evidenceJson.error}</div>
                    ) : (
                      <div className="space-y-2 text-xs text-slate-300">
                        {queryResult.results?.map((r: any, idx: number) => (
                          <div key={idx} className="p-3 bg-slate-900 rounded-lg space-y-1">
                            <p><strong className="text-blue-400">Decision Question:</strong> {r.decision_question}</p>
                            <p><strong className="text-indigo-400">Trigger:</strong> {r.trigger}</p>
                            <p><strong className="text-emerald-400">Evidence Summary:</strong> {r.evidence_summary}</p>
                            <p><strong className="text-rose-400">Sensitive Assumption:</strong> {r.sensitive_assumption}</p>
                            <p><strong className="text-cyan-400">Options Evaluated:</strong> {r.options_evaluated}</p>
                            <p><strong className="text-teal-400">Recommendation:</strong> {r.recommendation}</p>
                            <p><strong className="text-amber-400">Delay Consequence:</strong> {r.delay_consequence}</p>
                            <p><strong className="text-purple-400">Precedent Lookup:</strong> {r.precedent_lookup}</p>
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
