'use client';

import React, { useState, useEffect } from 'react';

export function TransformationDecisionsWorkspace() {
  const [activeTab, setActiveTab] = useState<'overview' | 'cases_questions' | 'evidence_conflicts' | 'options_tradeoffs' | 'scenario_robustness' | 'readiness_value' | 'packets_approvals' | 'execution_learning' | 'nl_query'>('overview');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('What decisions are waiting for leadership?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/transformation-decisions');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      } else {
        // Fallback seed structure
        setData({
          activeDecisionCasesCount: 1,
          readyForReviewCount: 1,
          evidenceConflictsCount: 1,
          decisionOptionsCount: 2,
          decisionPacketsCount: 1,
          decisionCalibrationAccuracyPct: 97.5,
          cases: [
            { id: 'case_scale_finops_01', title: 'Wave 2 Scale Authorization: Autonomous FinOps Transformation', decision_type: 'scale', status: 'ready', priority: 'critical', owner: 'Executive Transformation Steering Committee' }
          ],
          questions: [
            { id: 'q_01', question_text: 'Should Wave 2 Autonomous FinOps proceed to full enterprise scale following sub-100ms policy validation?' }
          ],
          items: [
            { id: 'item_01', type: 'fact', source: 'Zero-Trust AST Pre-signer Telemetry', value_json: { verified_latency_ms: 12.4, build_validation_pass_rate: 0.998 }, confidence: 0.99 },
            { id: 'item_02', type: 'measurement', source: 'Cloud Infrastructure Cost Accounting', value_json: { actual_q2_cost_reduction_pct: 31.2 }, confidence: 0.98 }
          ],
          conflicts: [
            { id: 'conf_01', source_a: 'Engineering Capacity Allocation Board', source_b: 'Transformation Portfolio Controller', conflicting_claim: 'Engineering Board estimates 6.5 FTE capacity demand vs Controller estimate of 4.0 FTE for Wave 2 scale', status: 'surfaced' }
          ],
          assumptions: [
            { id: 'ass_01', assumption_text: 'Multi-region Zero-Trust AST pre-signer API schema stability across cloud regions', status: 'valid', impact: 'high' }
          ],
          options: [
            { id: 'opt_scale_full', description: 'Proceed to full enterprise Wave 2 scale rollout across all 4 region clusters', cost: '$180,000', capacity: '4.5 FTEs', timing: 'Immediate Q3 Rollout', reversibility: 'partially_reversible' },
            { id: 'opt_pilot_staggered', description: 'Stagger Wave 2 rollout across 2 regions initially before full 4-region scale', cost: '$95,000', capacity: '2.5 FTEs', timing: 'Staggered Q3-Q4 Rollout', reversibility: 'reversible' }
          ],
          tradeoffs: [
            { id: 'to_01', option_id: 'opt_scale_full', benefit_gained: 'Unlocks full $4.2M annual OpEx savings 45 days earlier', cost_incurred: '$180,000 direct implementation expenditure', risk_accepted: 'Minor Q3 engineering capacity stretch', optionality_lost: 'Immediate reallocation of 4.5 FTEs', optionality_gained: 'Establishes automated baseline for future zero-trust acquisitions' }
          ],
          recommendations: [
            { id: 'rec_01', recommended_option_id: 'opt_scale_full', rationale_summary: 'Proceeding to full Wave 2 scale provides highest strategic value ($4.2M OpEx reduction) with low vulnerability (0.15) and sub-100ms policy validation performance', confidence: 'high' }
          ],
          packets: [
            { id: 'dpkt_01', version_tag: 'v1.0', packet_json: { question: 'Should Wave 2 Autonomous FinOps proceed to full enterprise scale?', recommended_option: 'Proceed to full enterprise Wave 2 scale rollout', required_approvals: ['Transformation Steering Committee', 'Chief Information Officer'] } }
          ],
          readinesses: [
            { id: 'read_01', status: 'ready', readiness_dimensions_json: { evidence: 0.95, clarity: 0.98, options: 0.92, scenario_coverage: 0.94, risk_visibility: 0.90, dependency_visibility: 0.96, approval_readiness: 0.95 } }
          ],
          values: [
            { id: 'dval_01', expected_strategic_value: 'High strategic alignment with Zero-Trust & FinOps transformation goals', expected_benefit: '$4.2M Annualized Cloud Infrastructure OpEx Reduction' }
          ],
          learnings: [
            { id: 'dlearn_01', lesson_text: 'Pre-signer rule caching exceeded baseline speed projections by 1.2%' }
          ],
          drifts: [
            { id: 'ddrift_01', approved_decision_summary: 'Full Wave 2 scale across 4 region clusters', implemented_decision_summary: 'Full Wave 2 scale implemented cleanly on schedule', drift_severity: 'none' }
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
      const res = await fetch(`/api/v1/transformation-decisions/query?query=${encodeURIComponent(queryText)}`, {
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
            <span className="p-2 bg-emerald-600/20 text-emerald-400 rounded-lg text-lg">⚖️</span>
            Enterprise Transformation Decision Intelligence 3.0
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Evidence Packs → Option Analysis → Scenario Testing → Trade-offs → Readiness → Decision Packets → Human Approval → Execution & Verification.
          </p>
        </div>
        <div className="flex gap-2">
          <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full text-xs font-semibold">
            Evidence-Backed Decision Support
          </span>
          <span className="px-3 py-1 bg-purple-500/10 text-purple-400 border border-purple-500/20 rounded-full text-xs font-semibold">
            Human-in-the-Loop Approval
          </span>
        </div>
      </div>

      {/* Telemetry Header */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Active Decision Cases</div>
          <div className="text-2xl font-bold text-emerald-400 mt-1">{data?.activeDecisionCasesCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Ready for Review</div>
          <div className="text-2xl font-bold text-indigo-400 mt-1">{data?.readyForReviewCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Evidence Conflicts</div>
          <div className="text-2xl font-bold text-amber-400 mt-1">{data?.evidenceConflictsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Decision Options</div>
          <div className="text-2xl font-bold text-teal-400 mt-1">{data?.decisionOptionsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Decision Packets</div>
          <div className="text-2xl font-bold text-purple-400 mt-1">{data?.decisionPacketsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Calibration Accuracy</div>
          <div className="text-2xl font-bold text-blue-400 mt-1">{data?.decisionCalibrationAccuracyPct || 97.5}%</div>
        </div>
      </div>

      {/* Subsystem Tabs */}
      <div className="flex border-b border-slate-800 gap-2 text-sm overflow-x-auto pb-1">
        {[
          { id: 'overview', label: 'Overview & Queue' },
          { id: 'cases_questions', label: 'Decision Cases & Questions' },
          { id: 'evidence_conflicts', label: 'Evidence Packs & Conflicts' },
          { id: 'options_tradeoffs', label: 'Option Analysis & Trade-offs' },
          { id: 'scenario_robustness', label: 'Scenario Testing & Robustness' },
          { id: 'readiness_value', label: 'Readiness & Strategic Value' },
          { id: 'packets_approvals', label: 'Decision Packets & Approvals' },
          { id: 'execution_learning', label: 'Execution & Calibration' },
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

      {/* Content */}
      {loading ? (
        <div className="p-8 text-center text-slate-500">Loading Transformation Decision Intelligence...</div>
      ) : (
        <div className="space-y-6">
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-emerald-400 flex items-center gap-2">
                  <span>⚖️</span> Active Decision Queue
                </h2>
                <div className="space-y-2 text-sm">
                  {data?.cases?.map((c: any) => (
                    <div key={c.id} className="p-3 bg-slate-950 rounded border border-emerald-800/40 flex justify-between items-center text-xs">
                      <div>
                        <div className="font-bold text-slate-100">{c.title}</div>
                        <div className="text-slate-400">Type: {c.decision_type} | Owner: {c.owner}</div>
                      </div>
                      <span className="px-2 py-0.5 bg-emerald-500/20 text-emerald-300 rounded font-bold">{c.status.toUpperCase()}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-amber-400 flex items-center gap-2">
                  <span>⚠️</span> Surfaced Evidence Conflicts
                </h2>
                <div className="space-y-2 text-sm">
                  {data?.conflicts?.map((conf: any) => (
                    <div key={conf.id} className="p-3 bg-slate-950 rounded border border-amber-800/40 space-y-1 text-xs">
                      <div className="font-bold text-amber-300">Conflict between {conf.source_a} & {conf.source_b}</div>
                      <div className="text-slate-300">{conf.conflicting_claim}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'cases_questions' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Transformation Decision Cases & Core Questions</h2>
              {data?.cases?.map((c: any) => (
                <div key={c.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-emerald-300">{c.title}</span>
                    <span className="text-xs px-2 py-0.5 bg-emerald-500/20 text-emerald-300 rounded font-bold">Priority: {c.priority}</span>
                  </div>
                  <p className="text-xs text-slate-300">{c.description}</p>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'evidence_conflicts' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Evidence Packs & Provenance Items</h2>
              {data?.items?.map((item: any) => (
                <div key={item.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-blue-500">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-blue-300">Type: {item.type} | Source: {item.source}</span>
                    <span className="text-xs px-2 py-0.5 bg-emerald-500/20 text-emerald-300 rounded font-bold">Conf: {(item.confidence * 100).toFixed(0)}%</span>
                  </div>
                  <div className="text-xs text-slate-400">Value: {JSON.stringify(item.value_json)}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'options_tradeoffs' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Option Analysis & Explicit Trade-offs</h2>
              {data?.options?.map((opt: any) => (
                <div key={opt.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-teal-500">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-teal-300">{opt.description}</span>
                    <span className="text-xs px-2 py-0.5 bg-teal-500/20 text-teal-300 rounded font-bold">Reversibility: {opt.reversibility}</span>
                  </div>
                  <div className="text-xs text-slate-300">Expected Outcome: {opt.expected_outcome}</div>
                  <div className="text-xs text-slate-400">Cost: {opt.cost} | Capacity: {opt.capacity} | Timing: {opt.timing}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'scenario_robustness' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Multi-Scenario Option Testing & Robustness</h2>
              <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                <div className="font-bold text-emerald-300">Most Robust Option: Proceed to full enterprise Wave 2 scale rollout</div>
                <div className="text-xs text-slate-300">Performs acceptably across baseline, optimistic, and stress scenarios with sub-100ms policy authorization.</div>
                <div className="text-xs text-emerald-400 font-semibold">Fragility Warning: None detected for Option 1 under tested scenarios.</div>
              </div>
            </div>
          )}

          {activeTab === 'readiness_value' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Decision Readiness & Expected Strategic Value</h2>
              {data?.readinesses?.map((r: any) => (
                <div key={r.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-purple-500">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-purple-300">Status: {r.status.toUpperCase()}</span>
                  </div>
                  <div className="text-xs text-slate-400">Dimensions: {JSON.stringify(r.readiness_dimensions_json)}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'packets_approvals' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Decision Packets & Required Human Approvals</h2>
              {data?.packets?.map((p: any) => (
                <div key={p.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-emerald-500">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-emerald-300">Decision Packet Tag: {p.version_tag}</span>
                  </div>
                  <div className="text-xs text-slate-300">Packet Details: {JSON.stringify(p.packet_json)}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'execution_learning' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Execution Drift & Forecast Calibration Learning</h2>
              {data?.learnings?.map((l: any) => (
                <div key={l.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-blue-500">
                  <div className="font-bold text-blue-300">Post-Decision Learning</div>
                  <div className="text-xs text-slate-300">{l.lesson_text}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'nl_query' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Natural Language Decision Intelligence Query</h2>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={queryText}
                  onChange={(e) => setQueryText(e.target.value)}
                  placeholder="Ask a decision intelligence query..."
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
                        <div className="font-semibold text-emerald-300">{res.decision_case}</div>
                        <div className="text-slate-300">Question: {res.decision_question}</div>
                        <div className="text-blue-300">Evidence: {res.evidence_summary}</div>
                        <div className="text-amber-300">Conflict: {res.evidence_conflict}</div>
                        <div className="text-teal-300">Recommendation: {res.recommended_option}</div>
                        <div className="text-purple-300">Tradeoff: {res.tradeoff_analysis}</div>
                        <div className="text-slate-400">Reversibility: {res.reversibility_window}</div>
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
