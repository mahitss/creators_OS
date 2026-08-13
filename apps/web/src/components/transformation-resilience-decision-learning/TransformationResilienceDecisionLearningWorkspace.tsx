'use client';

import React, { useState, useEffect } from 'react';

export function TransformationResilienceDecisionLearningWorkspace() {
  const [activeTab, setActiveTab] = useState<'overview' | 'outcomes' | 'attribution' | 'patterns' | 'lessons' | 'conflicts' | 'quality' | 'calibration' | 'delays' | 'counterfactuals' | 'query'>('overview');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('Which resilience decisions worked best and what lessons have been validated?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/transformation-resilience-decision-learning');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      } else {
        // Fallback seed data
        setData({
          domainsCount: 1,
          expectedOutcomesCount: 1,
          observedOutcomesCount: 1,
          comparisonsCount: 1,
          lessonsCount: 2,
          validatedLessonsCount: 1,
          conflictsCount: 1,
          successPatternsCount: 1,
          failurePatternsCount: 1,
          domains: [
            { id: 'learn_dom_01', name: 'Global Enterprise Continuous Resilience Decision Quality & Outcome Intelligence 2.0', owner: 'Principal Enterprise Decision Learning Architect', status: 'active', version: 'v2.0' }
          ],
          expectedOutcomes: [
            { id: 'exp_out_01', objective: 'Restore Primary OAuth Gateway Latency and SLA Stability', metric: 'OAuth Gateway P99 Latency ms', target_value: 45.0 }
          ],
          observedOutcomes: [
            { id: 'obs_out_01', metric: 'OAuth Gateway P99 Latency ms', observed_value: 42.0, source: 'EventMesh.IdentityGateway' }
          ],
          comparisons: [
            { id: 'comp_01', expected_value: 45.0, observed_value: 42.0, variance_pct: -6.67, variance_type: 'better_than_expected', materiality: 'high' }
          ],
          attributions: [
            { id: 'attr_01', attribution_level: 'likely_related', rationale: 'Multi-region token cache pre-warming reduced cold-start latency spikes by 18ms.', confidence: 0.88 }
          ],
          externalFactors: [
            { id: 'ext_01', factor_type: 'vendor_disruption', description: 'Secondary Cloud Region network provider performed unscheduled fiber maintenance.' }
          ],
          successPatterns: [
            { id: 'succ_pat_01', pattern_title: 'Multi-Region Token Cache Pre-Warming Pattern', supporting_cases_count: 6, confidence: 0.94 }
          ],
          failurePatterns: [
            { id: 'fail_pat_01', pattern_title: 'Single-Region Auth Bottleneck Pattern', frequency: 4 }
          ],
          lessons: [
            { id: 'less_01', lesson: 'Secondary Cloud Region latency assumptions must include a +15ms vendor SLA buffer.', confidence: 'validated' },
            { id: 'less_02', lesson: 'Token cache replication should rely on eventual consistency to save inter-region bandwidth.', confidence: 'medium' }
          ],
          lessonConflicts: [
            { id: 'lconf_01', conflict_description: 'Lesson 1 recommends strict SLA buffering for cache latency while Lesson 2 recommends relaxed eventual consistency.' }
          ],
          qualityAssessments: [
            { id: 'qual_01', evidence_completeness: 0.95, scenario_coverage: 0.96, tradeoff_completeness: 0.94, decision_timeliness: 0.88 }
          ],
          calibrations: [
            { id: 'cal_01', prediction_value: 45.0, actual_value: 42.0, error_pct: 6.67, bias_direction: 'conservative' }
          ],
          modelPerformances: [
            { id: 'mperf_01', model_version: 'DigitalTwin_v2.0', outcome_accuracy_pct: 94.5, evaluated_cases_count: 42 }
          ],
          delayAnalyses: [
            { id: 'delay_01', delay_days: 2.5, consequence_summary: '$12,500/day risk burn during 2.5-day executive alignment delay.' }
          ],
          counterfactuals: [
            { id: 'count_01', simulated_alternative: 'Option C: Do Nothing', simulated_outcome: 'Cascading OAuth outage affecting 3 transformation waves.', label: 'SIMULATED - COUNTERFACTUAL' }
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
      const res = await fetch(`/api/v1/transformation-resilience-decision-learning/query?query=${encodeURIComponent(queryText)}`, {
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
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-emerald-400 via-teal-400 to-cyan-400">
              Continuous Decision Quality & Outcome Intelligence 2.0
            </h1>
            <span className="px-3 py-1 text-xs font-semibold rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              Closed-Loop Decision Learning
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Evaluates actual decision outcomes against expected predictions, analyzes root cause failures, validates recurring patterns, and resolves lesson conflicts.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={fetchData}
            className="px-4 py-2 text-xs font-medium rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition"
          >
            Refresh Outcome Brief
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Learning Domain</p>
          <p className="text-xl font-bold text-emerald-400 mt-1">{data?.domainsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Outcome Variance</p>
          <p className="text-xl font-bold text-teal-400 mt-1">-6.67%</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Attribution</p>
          <p className="text-xl font-bold text-cyan-400 mt-1">Likely Related</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Success Patterns</p>
          <p className="text-xl font-bold text-indigo-400 mt-1">{data?.successPatternsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Validated Lessons</p>
          <p className="text-xl font-bold text-blue-400 mt-1">{data?.validatedLessonsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Lesson Conflicts</p>
          <p className="text-xl font-bold text-amber-400 mt-1">{data?.conflictsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Model Accuracy</p>
          <p className="text-xl font-bold text-purple-400 mt-1">94.5%</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Decision Delay</p>
          <p className="text-xl font-bold text-rose-400 mt-1">2.5 Days</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 overflow-x-auto space-x-2 scrollbar-none">
        {[
          { id: 'overview', label: 'Learning Overview' },
          { id: 'outcomes', label: 'Expected vs Observed Outcomes' },
          { id: 'attribution', label: 'Attribution & External Factors' },
          { id: 'patterns', label: 'Success & Failure Patterns' },
          { id: 'lessons', label: 'Validated Lessons' },
          { id: 'conflicts', label: 'Lesson Conflicts & Discrepancies' },
          { id: 'quality', label: '8-Dimension Decision Quality' },
          { id: 'calibration', label: 'Calibration & Bias Tracking' },
          { id: 'delays', label: 'Decision Delay Analysis' },
          { id: 'counterfactuals', label: 'Counterfactual Simulations' },
          { id: 'query', label: 'Decision Learning Query' }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-2.5 text-xs font-semibold whitespace-nowrap border-b-2 transition ${
              activeTab === tab.id
                ? 'border-emerald-400 text-emerald-400 bg-emerald-500/5'
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
            Ingesting decision outcomes, computing variance metrics, and validating lessons...
          </div>
        ) : (
          <>
            {activeTab === 'overview' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Executive Decision Learning Fabric</h3>
                {data?.domains?.map((dom: any) => (
                  <div key={dom.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 flex justify-between items-center">
                    <div>
                      <span className="font-semibold text-emerald-400">{dom.name}</span>
                      <p className="text-xs text-slate-400 mt-1">Owner: {dom.owner} | Version: {dom.version}</p>
                    </div>
                    <span className="text-xs px-3 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-semibold">{dom.status}</span>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'outcomes' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Expected vs Observed Outcomes</h3>
                {data?.comparisons?.map((c: any) => (
                  <div key={c.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-semibold text-teal-400">OAuth Gateway P99 Latency Comparison</span>
                      <span className="text-xs px-2.5 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-semibold">{c.variance_type}</span>
                    </div>
                    <p className="text-xs text-slate-300">Expected: {c.expected_value}ms | Observed: {c.observed_value}ms (Variance: {c.variance_pct}%)</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'attribution' && (
              <div className="space-y-6">
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                  <span className="text-sm font-semibold text-cyan-400">Outcome Attribution</span>
                  <p className="text-xs text-slate-300">Level: {data?.attributions?.[0]?.attribution_level} (Confidence: {( (data?.attributions?.[0]?.confidence ?? 0.88) * 100 ).toFixed(0)}%)</p>
                  <p className="text-xs text-slate-400">{data?.attributions?.[0]?.rationale}</p>
                </div>

                <div className="space-y-3">
                  <h4 className="text-xs font-semibold text-amber-400">External Influencing Factors</h4>
                  {data?.externalFactors?.map((ext: any) => (
                    <div key={ext.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-1">
                      <span className="text-xs font-semibold text-amber-400">{ext.factor_type}</span>
                      <p className="text-xs text-slate-300">{ext.description}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'patterns' && (
              <div className="space-y-6">
                <div className="space-y-3">
                  <h4 className="text-xs font-semibold text-emerald-400">Recurring Success Patterns</h4>
                  {data?.successPatterns?.map((sp: any) => (
                    <div key={sp.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-1">
                      <span className="text-sm font-semibold text-emerald-400">{sp.pattern_title}</span>
                      <p className="text-xs text-slate-300">Supporting Cases: {sp.supporting_cases_count} | Confidence: {(sp.confidence * 100).toFixed(0)}%</p>
                    </div>
                  ))}
                </div>

                <div className="space-y-3">
                  <h4 className="text-xs font-semibold text-rose-400">Recurring Failure Patterns</h4>
                  {data?.failurePatterns?.map((fp: any) => (
                    <div key={fp.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-1">
                      <span className="text-sm font-semibold text-rose-400">{fp.pattern_title}</span>
                      <p className="text-xs text-slate-300">Frequency: {fp.frequency} times across affected waves</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'lessons' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Validated Decision Lessons</h3>
                {data?.lessons?.map((less: any) => (
                  <div key={less.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 flex justify-between items-center">
                    <div>
                      <span className="text-xs font-semibold text-blue-400 capitalize">{less.lesson_type} Lesson:</span>
                      <p className="text-xs text-slate-200 mt-1">{less.lesson}</p>
                    </div>
                    <span className="text-xs px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">{less.confidence}</span>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'conflicts' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Surfaced Lesson Conflicts</h3>
                {data?.lessonConflicts?.map((lc: any) => (
                  <div key={lc.id} className="p-4 rounded-xl bg-slate-950/60 border border-amber-500/30 space-y-2">
                    <span className="text-xs font-semibold text-amber-400">Conflicting Resilience Lessons</span>
                    <p className="text-xs text-slate-300">{lc.conflict_description}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'quality' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">8-Dimension Decision Quality Assessment</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {[
                    { label: 'Evidence Completeness', score: 0.95 },
                    { label: 'Assumption Quality', score: 0.92 },
                    { label: 'Scenario Coverage', score: 0.96 },
                    { label: 'Option Diversity', score: 0.90 },
                    { label: 'Trade-Off Completeness', score: 0.94 },
                    { label: 'Decision Timeliness', score: 0.88 },
                    { label: 'Execution Quality', score: 0.95 },
                    { label: 'Verification Quality', score: 0.96 },
                  ].map((q, idx) => (
                    <div key={idx} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 text-center">
                      <span className="text-xs font-medium text-slate-400">{q.label}</span>
                      <p className="text-lg font-bold text-emerald-400 mt-1">{(q.score * 100).toFixed(0)}%</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'calibration' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Forecast & Simulation Model Calibration</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                  <p className="text-xs text-slate-300">Model Version: {data?.modelPerformances?.[0]?.model_version} (Accuracy: {data?.modelPerformances?.[0]?.outcome_accuracy_pct}%)</p>
                  <p className="text-xs text-slate-400">Calibration Error: {data?.calibrations?.[0]?.error_pct}% | Bias: {data?.calibrations?.[0]?.bias_direction}</p>
                </div>
              </div>
            )}

            {activeTab === 'delays' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Decision Delay Analysis</h3>
                {data?.delayAnalyses?.map((d: any) => (
                  <div key={d.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <span className="text-xs font-semibold text-rose-400">Decision Delay: {d.delay_days} Days</span>
                    <p className="text-xs text-slate-300">{d.consequence_summary}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'counterfactuals' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Counterfactual Simulation Lab</h3>
                {data?.counterfactuals?.map((c: any) => (
                  <div key={c.id} className="p-4 rounded-xl bg-slate-950/60 border border-purple-500/30 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-bold text-purple-400">{c.label}</span>
                      <span className="text-xs text-slate-400">Simulated Alternative: {c.simulated_alternative}</span>
                    </div>
                    <p className="text-xs text-slate-300">Outcome: {c.simulated_outcome}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'query' && (
              <div className="space-y-6">
                <h3 className="text-base font-semibold text-slate-200">Natural Language Decision Learning Query</h3>
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={queryText}
                    onChange={(e) => setQueryText(e.target.value)}
                    placeholder="Ask a decision outcome, quality, or lesson validation question..."
                    className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-emerald-500/50"
                  />
                  <button
                    onClick={handleQuery}
                    disabled={queryLoading}
                    className="px-5 py-2.5 bg-emerald-500 hover:bg-emerald-600 disabled:opacity-50 text-slate-950 text-xs font-semibold rounded-xl transition"
                  >
                    {queryLoading ? 'Processing...' : 'Run Query'}
                  </button>
                </div>

                {queryResult && (
                  <div className="p-5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-semibold text-emerald-400">Decision Learning Query Result</span>
                      <span className="text-xs text-slate-400">Confidence: {queryResult.confidencePct}%</span>
                    </div>
                    {queryResult.evidenceJson?.error ? (
                      <div className="text-xs text-rose-400 font-semibold">{queryResult.evidenceJson.error}</div>
                    ) : (
                      <div className="space-y-2 text-xs text-slate-300">
                        {queryResult.results?.map((r: any, idx: number) => (
                          <div key={idx} className="p-3 bg-slate-900 rounded-lg space-y-1">
                            <p><strong className="text-emerald-400">Outcome Comparison:</strong> {r.outcome_comparison}</p>
                            <p><strong className="text-cyan-400">Attribution:</strong> {r.attribution}</p>
                            <p><strong className="text-rose-400">Failure Analysis:</strong> {r.failure_analysis}</p>
                            <p><strong className="text-teal-400">Success Pattern:</strong> {r.success_pattern}</p>
                            <p><strong className="text-blue-400">Validated Lesson:</strong> {r.validated_lesson}</p>
                            <p><strong className="text-amber-400">Lesson Conflict:</strong> {r.lesson_conflict}</p>
                            <p><strong className="text-indigo-400">Decision Quality:</strong> {r.decision_quality}</p>
                            <p><strong className="text-purple-400">Calibration Error:</strong> {r.calibration_error}</p>
                            <p><strong className="text-pink-400">Counterfactual Analysis:</strong> {r.counterfactual_analysis}</p>
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
