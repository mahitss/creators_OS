'use client';

import React, { useState, useEffect } from 'react';

export function TransformationResilienceLearningWorkspace() {
  const [activeTab, setActiveTab] = useState<
    | 'overview'
    | 'expectations'
    | 'prediction_errors'
    | 'warning_quality'
    | 'intervention_outcomes'
    | 'recovery_learning'
    | 'simulation_twin'
    | 'assumptions'
    | 'lessons_patterns'
    | 'calibration'
    | 'model_health'
    | 'experiments'
    | 'query'
  >('overview');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('What did Vapor get wrong recently and what should be recalibrated under governed approval?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/transformation-resilience-learning/status');
      const warningRes = await fetch('/api/v1/transformation-resilience-learning/warnings/quality');
      if (res.ok && warningRes.ok) {
        const dom = await res.json();
        const wqual = await warningRes.json();
        setData({
          domain: dom,
          warningQuality: wqual,
          observationsCount: 1,
          expectationsCount: 1,
          outcomesCount: 1,
          comparisonsCount: 1,
          predictionErrorsCount: 1,
          lessonsCount: 1,
          patternsCount: 1,
          proposalsCount: 1,
          modelPerformancesCount: 1
        });
      } else {
        // Fallback seed data
        setData({
          domain: { name: 'Global Enterprise Resilience Learning Fabric & Outcome Calibration 2.0', status: 'active', version: 'v2.0' },
          warningQuality: { precision_pct: 95.0, recall_pct: 92.0, avg_lead_time_hours: 48.0, false_positive_rate: 0.05, false_negative_rate: 0.08, confidence_calibration_score: 0.94 },
          observationsCount: 1,
          expectationsCount: 1,
          outcomesCount: 1,
          comparisonsCount: 1,
          predictionErrorsCount: 1,
          lessonsCount: 1,
          patternsCount: 1,
          proposalsCount: 1,
          modelPerformancesCount: 1
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
      const res = await fetch(`/api/v1/transformation-resilience-learning/query?query=${encodeURIComponent(queryText)}`, {
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
    <div className="p-6 space-y-6 max-w-[1700px] mx-auto text-slate-100 font-sans">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-slate-900/90 p-6 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-teal-400 via-emerald-400 to-cyan-400">
              Enterprise Resilience Learning Fabric 2.0
            </h1>
            <span className="px-3 py-1 text-xs font-bold rounded-full bg-teal-500/10 text-teal-400 border border-teal-500/20">
              Assurance Memory, Outcome Learning & Governed Model Calibration
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Closes the continuous loop by comparing WHAT VAPOR EXPECTED vs WHAT ACTUALLY HAPPENED across predictions, warnings, interventions, recovery, simulations, and optimization recommendations.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={fetchData}
            className="px-4 py-2 text-xs font-semibold rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition"
          >
            Re-Sync Learning State
          </button>
        </div>
      </div>

      {/* Top Banner Notice */}
      <div className="bg-teal-950/40 border border-teal-500/30 p-3.5 rounded-xl flex justify-between items-center text-xs">
        <div className="flex items-center gap-2 text-teal-300 font-medium">
          <span>🧠 GOVERNED CALIBRATION PRINCIPLE:</span>
          <span className="text-slate-300">Vapor does NOT learn by silently rewriting models. Every material learning event is observable, versioned, evidence-backed, reviewable, reversible, and auditable.</span>
        </div>
        <span className="text-[11px] font-bold px-2 py-0.5 rounded bg-teal-500/20 text-teal-300 uppercase">Versioned Intelligence</span>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-3">
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Warning Precision</p>
          <p className="text-lg font-bold text-emerald-400 mt-0.5">{data?.warningQuality?.precision_pct ?? 95.0}%</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Warning Recall</p>
          <p className="text-lg font-bold text-teal-400 mt-0.5">{data?.warningQuality?.recall_pct ?? 92.0}%</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Outcome Variance</p>
          <p className="text-lg font-bold text-amber-400 mt-0.5">0.15 (Low)</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Intervention Efficacy</p>
          <p className="text-lg font-bold text-cyan-400 mt-0.5">85%</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Recovery Accuracy</p>
          <p className="text-lg font-bold text-indigo-400 mt-0.5">100%</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Active Lessons</p>
          <p className="text-lg font-bold text-purple-400 mt-0.5">{data?.lessonsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Confirmed Patterns</p>
          <p className="text-lg font-bold text-rose-400 mt-0.5">{data?.patternsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Proposals in Review</p>
          <p className="text-lg font-bold text-emerald-400 mt-0.5">{data?.proposalsCount ?? 1}</p>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-800 overflow-x-auto space-x-2 scrollbar-none">
        {[
          { id: 'overview', label: 'Learning Overview' },
          { id: 'expectations', label: 'Expectations vs Actuals' },
          { id: 'prediction_errors', label: 'Prediction Errors' },
          { id: 'warning_quality', label: 'Warning Quality & Calibration' },
          { id: 'intervention_outcomes', label: 'Intervention Outcomes' },
          { id: 'recovery_learning', label: 'Recovery Learning' },
          { id: 'simulation_twin', label: 'Simulation & Twin Validation' },
          { id: 'assumptions', label: 'Assumptions & Failures' },
          { id: 'lessons_patterns', label: 'Lessons & Patterns' },
          { id: 'calibration', label: 'Calibration Proposals & Rollbacks' },
          { id: 'model_health', label: 'Model Health & Drift' },
          { id: 'experiments', label: 'Sandboxed Experiments' },
          { id: 'query', label: 'Learning Query' }
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

      {/* Tab Panels */}
      <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 min-h-[420px]">
        {loading ? (
          <div className="flex items-center justify-center h-64 text-slate-400 text-sm">
            Closing loop across prediction errors, warning accuracy, intervention effectiveness, and governed calibration...
          </div>
        ) : (
          <>
            {activeTab === 'overview' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Continuous Enterprise Resilience Learning Engine</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                  <span className="font-bold text-teal-400">{data?.domain?.name}</span>
                  <p className="text-xs text-slate-300">Status: {data?.domain?.status} | Version: {data?.domain?.version}</p>
                  <p className="text-xs text-slate-400">
                    Continuously records observations, expectations, actual outcomes, and prediction errors to refine warning thresholds, intervention recovery models, and digital twin state representations under governed review.
                  </p>
                </div>
              </div>
            )}

            {activeTab === 'expectations' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Expectations vs Actual Outcomes</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-teal-500/30 space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-bold text-teal-300">Foresight Early Warning exp_01 vs Actual act_01</span>
                    <span className="text-xs px-2.5 py-1 rounded bg-teal-500/20 text-teal-300 font-semibold">Direction: Worse than Expected</span>
                  </div>
                  <p className="text-xs text-slate-300">Expected Severity: 0.85 (36 hrs) vs Observed Severity: 0.70 (42 hrs). Variance Score: 0.15.</p>
                </div>
              </div>
            )}

            {activeTab === 'prediction_errors' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Prediction Error Categorization</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-amber-500/30 space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-bold text-amber-300">Prediction Error perr_01: severity_error</span>
                    <span className="text-xs px-2.5 py-1 rounded bg-amber-500/20 text-amber-300 font-semibold">Severity Delta: 0.15</span>
                  </div>
                  <p className="text-xs text-slate-300">Foresight model overestimated outage severity by 0.15 score delta due to unmodeled automated queue throttling.</p>
                </div>
              </div>
            )}

            {activeTab === 'warning_quality' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Warning Quality & Multi-Metric Calibration</h3>
                <div className="grid grid-cols-3 gap-4">
                  <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                    <p className="text-xs text-slate-400">Warning Precision</p>
                    <p className="text-xl font-bold text-emerald-400 mt-1">95.0%</p>
                  </div>
                  <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                    <p className="text-xs text-slate-400">Warning Recall</p>
                    <p className="text-xl font-bold text-teal-400 mt-1">92.0%</p>
                  </div>
                  <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                    <p className="text-xs text-slate-400">Average Lead Time</p>
                    <p className="text-xl font-bold text-cyan-400 mt-1">48.0 Hours</p>
                  </div>
                </div>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 text-xs text-slate-300">
                  False Positive Rate: 5.0% | False Negative Rate: 8.0% | Confidence Calibration Score: 0.94
                </div>
              </div>
            )}

            {activeTab === 'intervention_outcomes' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Intervention Outcomes & Side Effects</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-cyan-500/30 space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-bold text-cyan-300">Intervention int_reserve_cluster_01</span>
                    <span className="text-xs px-2.5 py-1 rounded bg-cyan-500/20 text-cyan-300 font-semibold">Effectiveness: 85%</span>
                  </div>
                  <p className="text-xs text-slate-300">Actual Effect: Eliminated compute cluster outage risk by 85% with 0 unexpected side effects.</p>
                </div>
              </div>
            )}

            {activeTab === 'recovery_learning' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Recovery Learning & Variance</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-indigo-500/30 space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-bold text-indigo-300">Recovery Outcome recout_01</span>
                    <span className="text-xs px-2.5 py-1 rounded bg-indigo-500/20 text-indigo-300 font-semibold">Coverage: 98.0%</span>
                  </div>
                  <p className="text-xs text-slate-300">Expected Recovery: 24.0 Hours vs Actual Recovery: 24.0 Hours (0.0% variance).</p>
                </div>
              </div>
            )}

            {activeTab === 'assumptions' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Assumptions & Downstream Failure Impact</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-rose-500/30 space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-bold text-rose-300">Assumption Failure assumpfail_01</span>
                    <span className="text-xs px-2.5 py-1 rounded bg-rose-500/20 text-rose-300 font-semibold">Status: Failed</span>
                  </div>
                  <p className="text-xs text-slate-300">Expected: Bandwidth quota pre-allocated vs Actual: Bandwidth quota delayed by 15 minutes.</p>
                </div>
              </div>
            )}

            {activeTab === 'lessons_patterns' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Validated Lessons & Confirmed Patterns</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-purple-500/30 space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-bold text-purple-300">Lesson less_01: Foresight Early Warning Lead-Time Accuracy</span>
                    <span className="text-xs px-2.5 py-1 rounded bg-purple-500/20 text-purple-300 font-semibold">Confidence: 94%</span>
                  </div>
                  <p className="text-xs text-slate-300">Summary: Foresight early warning lead-time estimates are accurate within +/- 6 hours for compute cluster load spikes.</p>
                </div>
              </div>
            )}

            {activeTab === 'calibration' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Governed Calibration Proposals & Version Rollback</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-emerald-500/30 space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-bold text-emerald-300">Proposal calprop_01: Recalibrate Queue Depth Sensor Threshold</span>
                    <span className="text-xs px-2.5 py-1 rounded bg-emerald-500/20 text-emerald-300 font-bold uppercase">Policy Approval Required</span>
                  </div>
                  <p className="text-xs text-slate-300">Proposed Change: queue_depth_threshold from 80% to 75% (+18 min lead time).</p>
                </div>
              </div>
            )}

            {activeTab === 'query' && (
              <div className="space-y-6">
                <h3 className="text-base font-semibold text-slate-200">Natural Language Learning Query</h3>
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={queryText}
                    onChange={(e) => setQueryText(e.target.value)}
                    placeholder="Ask what Vapor got wrong recently, check model drift, or view calibration proposals..."
                    className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-teal-500/50"
                  />
                  <button
                    onClick={handleQuery}
                    disabled={queryLoading}
                    className="px-5 py-2.5 bg-teal-500 hover:bg-teal-600 disabled:opacity-50 text-slate-950 text-xs font-bold rounded-xl transition"
                  >
                    {queryLoading ? 'Processing...' : 'Run Learning Query'}
                  </button>
                </div>

                {queryResult && (
                  <div className="p-5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-semibold text-teal-400">Learning Query Result</span>
                      <span className="text-xs text-slate-400">Confidence: {queryResult.confidencePct}%</span>
                    </div>
                    {queryResult.evidenceJson?.error ? (
                      <div className="text-xs text-rose-400 font-semibold">{queryResult.evidenceJson.error}</div>
                    ) : (
                      <div className="space-y-2 text-xs text-slate-300">
                        {queryResult.results?.map((r: any, idx: number) => (
                          <div key={idx} className="p-3 bg-slate-900 rounded-lg space-y-1">
                            <p><strong className="text-amber-400">Wrong Recently:</strong> {r.wrong_recently}</p>
                            <p><strong className="text-emerald-400">Warning Quality:</strong> {r.warning_quality}</p>
                            <p><strong className="text-cyan-400">Intervention Outcomes:</strong> {r.intervention_outcomes}</p>
                            <p><strong className="text-indigo-300">Recovery Accuracy:</strong> {r.recovery_accuracy}</p>
                            <p><strong className="text-rose-400">Assumption Failures:</strong> {r.assumption_failures}</p>
                            <p><strong className="text-purple-400">Recurring Patterns:</strong> {r.recurring_patterns}</p>
                            <p><strong className="text-teal-400 font-semibold">Model Health:</strong> {r.model_health}</p>
                            <p><strong className="text-emerald-300 font-semibold">Calibration Proposal:</strong> {r.calibration_proposal}</p>
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
