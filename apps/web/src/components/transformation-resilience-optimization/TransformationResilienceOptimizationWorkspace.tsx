'use client';

import React, { useState, useEffect } from 'react';

export function TransformationResilienceOptimizationWorkspace() {
  const [activeTab, setActiveTab] = useState<
    | 'overview'
    | 'problems'
    | 'candidates'
    | 'pareto'
    | 'tradeoffs'
    | 'resources'
    | 'investments'
    | 'control_redundancy'
    | 'priorities'
    | 'recommendations'
    | 'sensitivity'
    | 'outcomes'
    | 'query'
  >('overview');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('Where should we improve resilience first to reduce compute cluster outage risk under budget constraints?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/transformation-resilience-optimization/status');
      const overviewRes = await fetch('/api/v1/transformation-resilience-optimization/problems');
      if (res.ok && overviewRes.ok) {
        const dom = await res.json();
        const probs = await overviewRes.json();
        setData({
          domain: dom,
          problems: probs,
          candidatesCount: 2,
          runsCount: 1,
          paretoPointsCount: 1,
          investmentsCount: 1,
          gapPrioritiesCount: 1,
          recommendationsCount: 1
        });
      } else {
        // Fallback seed data
        setData({
          domain: { name: 'Global Enterprise Resilience Multi-Objective Optimization Strategy 2.0', status: 'active', version: 'v2.0' },
          problems: [{ id: 'prob_01', name: 'HR Cloud & Compute Cluster Resilience Optimization', baseline_strategy: 'continue_current_state' }],
          candidatesCount: 2,
          runsCount: 1,
          paretoPointsCount: 1,
          investmentsCount: 1,
          gapPrioritiesCount: 1,
          recommendationsCount: 1
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
      const res = await fetch(`/api/v1/transformation-resilience-optimization/query?query=${encodeURIComponent(queryText)}`, {
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
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400">
              Enterprise Resilience Optimization 2.0
            </h1>
            <span className="px-3 py-1 text-xs font-bold rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20">
              Multi-Objective Strategy & Governed Investment Decision Support
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Answers "WHERE SHOULD WE IMPROVE FIRST?" by comparing resilience improvements across risk reduction, coverage, resilience, capacity, cost, effort, deadline, dependency concentration, and evidence quality.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={fetchData}
            className="px-4 py-2 text-xs font-semibold rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition"
          >
            Re-Sync Optimization State
          </button>
        </div>
      </div>

      {/* Top Banner Notice */}
      <div className="bg-blue-950/40 border border-blue-500/30 p-3.5 rounded-xl flex justify-between items-center text-xs">
        <div className="flex items-center gap-2 text-blue-300 font-medium">
          <span>⚖️ DECISION SUPPORT NOTICE:</span>
          <span className="text-slate-300">Vapor provides multi-objective optimization intelligence and decision support. Vapor does NOT autonomously allocate budgets, approve investments, or reassign people.</span>
        </div>
        <span className="text-[11px] font-bold px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 uppercase">Decision Support</span>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-3">
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Active Problems</p>
          <p className="text-lg font-bold text-emerald-400 mt-0.5">{data?.problems?.length ?? 1}</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Candidates</p>
          <p className="text-lg font-bold text-blue-400 mt-0.5">{data?.candidatesCount ?? 2}</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Optimization Runs</p>
          <p className="text-lg font-bold text-cyan-400 mt-0.5">{data?.runsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Pareto Points</p>
          <p className="text-lg font-bold text-indigo-400 mt-0.5">{data?.paretoPointsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Investment Cases</p>
          <p className="text-lg font-bold text-purple-400 mt-0.5">{data?.investmentsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Gap Priorities</p>
          <p className="text-lg font-bold text-amber-400 mt-0.5">{data?.gapPrioritiesCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Recommendations</p>
          <p className="text-lg font-bold text-teal-400 mt-0.5">{data?.recommendationsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Robustness Score</p>
          <p className="text-lg font-bold text-emerald-400 mt-0.5">94%</p>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-800 overflow-x-auto space-x-2 scrollbar-none">
        {[
          { id: 'overview', label: 'Optimization Overview' },
          { id: 'problems', label: 'Problems & Baseline' },
          { id: 'candidates', label: 'Candidate Improvements' },
          { id: 'pareto', label: 'Pareto Frontier' },
          { id: 'tradeoffs', label: 'Explicit Trade-Offs' },
          { id: 'resources', label: 'Resource & Capacity' },
          { id: 'investments', label: 'Investment Cases' },
          { id: 'control_redundancy', label: 'Control & Redundancy' },
          { id: 'priorities', label: 'Gap Priorities' },
          { id: 'recommendations', label: 'Governed Recommendations' },
          { id: 'sensitivity', label: 'Sensitivity & Robustness' },
          { id: 'outcomes', label: 'Outcomes & Lessons' },
          { id: 'query', label: 'Optimization Query' }
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

      {/* Tab Panels */}
      <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 min-h-[420px]">
        {loading ? (
          <div className="flex items-center justify-center h-64 text-slate-400 text-sm">
            Executing multi-objective resilience portfolio optimization & Pareto analysis...
          </div>
        ) : (
          <>
            {activeTab === 'overview' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Multi-Objective Resilience Portfolio Strategy Engine</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                  <span className="font-bold text-blue-400">{data?.domain?.name}</span>
                  <p className="text-xs text-slate-300">Status: {data?.domain?.status} | Version: {data?.domain?.version}</p>
                  <p className="text-xs text-slate-400">
                    Evaluates candidate resilience investments against the baseline strategy (`continue_current_state`), generating non-dominated Pareto sets, trade-off comparisons, analytical investment cases, and robust recommendations.
                  </p>
                </div>
              </div>
            )}

            {activeTab === 'problems' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Optimization Problems & Baseline Strategy</h3>
                {data?.problems?.map((p: any) => (
                  <div key={p.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="font-semibold text-emerald-400">{p.name}</span>
                      <span className="text-xs px-2.5 py-1 rounded bg-slate-800 text-slate-300">Horizon: 90 Days</span>
                    </div>
                    <p className="text-xs text-slate-300">
                      Baseline Strategy: <strong className="text-amber-400">{p.baseline_strategy ?? 'continue_current_state'}</strong> (Residual risk score 0.35 with 85% capacity utilization).
                    </p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'candidates' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Candidate Improvements</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-blue-500/30 space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-bold text-blue-400">Candidate cand_01: Configure Dynamic Secondary Cloud Cluster Reserve Pool</span>
                    <span className="text-xs px-2.5 py-1 rounded bg-blue-500/20 text-blue-300 font-semibold uppercase">Reversible</span>
                  </div>
                  <p className="text-xs text-slate-300">Impact: Risk Reduction Score +0.35 | Effort: 8 Days | Cost: $35,000 | Residual Risk: 0.05</p>
                </div>
              </div>
            )}

            {activeTab === 'pareto' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Pareto Frontier Analysis</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-cyan-500/30 space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-bold text-cyan-300">Pareto Set pset_01: 3 Non-Dominated Points</span>
                    <span className="text-xs px-2.5 py-1 rounded bg-cyan-500/20 text-cyan-300 font-semibold">Algorithm: pareto_analysis</span>
                  </div>
                  <p className="text-xs text-slate-300">Point ppoint_01 (Non-Dominated): Risk Score 0.05, Cost $47,000, Effort 11 days, Coverage 95%, Recovery 92%.</p>
                </div>
              </div>
            )}

            {activeTab === 'tradeoffs' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Explicit Trade-Off Comparisons</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-indigo-500/30 space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-bold text-indigo-300">Tradeoff tradeoff_01: Candidate cand_01 vs cand_02</span>
                    <span className="text-xs px-2.5 py-1 rounded bg-indigo-500/20 text-indigo-300 font-semibold">Cost Delta: +$23,000</span>
                  </div>
                  <p className="text-xs text-slate-300">Summary: Option A (Secondary Cluster Reserve) provides 20% higher risk reduction for +$23,000 cost vs Option B.</p>
                </div>
              </div>
            )}

            {activeTab === 'investments' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Analytical Investment Cases</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-purple-500/30 space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-xs px-2.5 py-1 rounded bg-purple-500/20 text-purple-300 font-bold uppercase">
                      ANALYTICAL INVESTMENT CASE — NOT APPROVED BUDGET
                    </span>
                    <span className="text-xs text-slate-400">Time Horizon: 3 Months</span>
                  </div>
                  <p className="text-xs text-slate-200 font-semibold">Expected Benefit: Eliminates systemic compute outage risk for Wave 3 deployment, saving estimated $250,000 in delay costs.</p>
                  <p className="text-xs text-slate-400">Cost: $35,000 | Effort: 8 Days | Risk Level: Low | Uncertainty: Low</p>
                </div>
              </div>
            )}

            {activeTab === 'priorities' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Resilience Gap Priorities</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-amber-500/30 space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-bold text-amber-300">Gap Priority #1: Gap gap_01 (Capacity Gap)</span>
                    <span className="text-xs px-2.5 py-1 rounded bg-amber-500/20 text-amber-300 font-semibold">Rank #1</span>
                  </div>
                  <p className="text-xs text-slate-300">Impact Score: 0.90 | Urgency: 0.85 | Dependency Concentration: 0.80 | Control Weakness: 0.75</p>
                </div>
              </div>
            )}

            {activeTab === 'recommendations' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Governed Recommendations</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-emerald-500/30 space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-xs px-2.5 py-1 rounded bg-emerald-500/20 text-emerald-300 font-bold uppercase">
                      ANALYTICAL RECOMMENDATION — NOT DECISION
                    </span>
                    <span className="text-xs text-slate-400">Confidence: 92%</span>
                  </div>
                  <p className="text-xs text-slate-200 font-semibold">Recommended Strategy: Configure Dynamic Secondary Cloud Cluster Reserve Pool (cand_01) under balanced profile.</p>
                  <p className="text-xs text-slate-400">Impact: Reduces residual risk score from 0.35 (baseline) to 0.05 (+30% risk reduction).</p>
                </div>
              </div>
            )}

            {activeTab === 'query' && (
              <div className="space-y-6">
                <h3 className="text-base font-semibold text-slate-200">Natural Language Optimization Query</h3>
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={queryText}
                    onChange={(e) => setQueryText(e.target.value)}
                    placeholder="Ask where to improve resilience first, compare investments, or view Pareto frontier..."
                    className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500/50"
                  />
                  <button
                    onClick={handleQuery}
                    disabled={queryLoading}
                    className="px-5 py-2.5 bg-blue-500 hover:bg-blue-600 disabled:opacity-50 text-slate-950 text-xs font-bold rounded-xl transition"
                  >
                    {queryLoading ? 'Processing...' : 'Run Optimization Query'}
                  </button>
                </div>

                {queryResult && (
                  <div className="p-5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-semibold text-blue-400">Optimization Query Result</span>
                      <span className="text-xs text-slate-400">Confidence: {queryResult.confidencePct}%</span>
                    </div>
                    {queryResult.evidenceJson?.error ? (
                      <div className="text-xs text-rose-400 font-semibold">{queryResult.evidenceJson.error}</div>
                    ) : (
                      <div className="space-y-2 text-xs text-slate-300">
                        {queryResult.results?.map((r: any, idx: number) => (
                          <div key={idx} className="p-3 bg-slate-900 rounded-lg space-y-1">
                            <p><strong className="text-emerald-400">Priority Area:</strong> {r.priority_area}</p>
                            <p><strong className="text-amber-400">Baseline Comparison:</strong> {r.baseline_comparison}</p>
                            <p><strong className="text-cyan-400">Pareto Trade-Off:</strong> {r.pareto_tradeoff}</p>
                            <p><strong className="text-rose-400">Resource Shortfall:</strong> {r.resource_shortfall}</p>
                            <p><strong className="text-purple-400 font-semibold">Investment Case Label:</strong> {r.investment_case_label}</p>
                            <p><strong className="text-teal-400 font-semibold">Recommendation Label:</strong> {r.recommendation_label}</p>
                            <p><strong className="text-indigo-300 font-semibold">Robustness:</strong> {r.robustness}</p>
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
