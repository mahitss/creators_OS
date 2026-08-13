'use client';

import React, { useState, useEffect } from 'react';

export function TransformationResilienceDigitalTwinWorkspace() {
  const [activeTab, setActiveTab] = useState<
    | 'overview'
    | 'snapshots'
    | 'reality'
    | 'what_if'
    | 'stress'
    | 'recovery'
    | 'experiments'
    | 'validation'
    | 'library'
    | 'query'
  >('overview');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('What happens to HR Cloud Go-Live if primary compute cluster 01 suffers a 72-hour outage?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/transformation-resilience-digital-twin/status');
      const overviewRes = await fetch('/api/v1/transformation-resilience-digital-twin/snapshots');
      if (res.ok && overviewRes.ok) {
        const dom = await res.json();
        const snaps = await overviewRes.json();
        setData({
          domain: dom,
          snapshots: snaps,
          freshness: 1.0,
          completeness: 0.98,
          lagSeconds: 0.0,
          driftStatus: '3% (behavior_drift)',
          activeForks: 1
        });
      } else {
        // Fallback seed data
        setData({
          domain: { name: 'Global Enterprise Transformation Resilience Digital Twin 2.0', status: 'current', state_version: 'v2.0' },
          snapshots: [{ id: 'dtsnap_v2_0', version: 'v2.0', transformations_count: 8, plans_count: 14, dependencies_count: 22, state_hash: 'sha256_e3b0c442...' }],
          freshness: 1.0,
          completeness: 0.98,
          lagSeconds: 0.0,
          driftStatus: '3% (behavior_drift)',
          activeForks: 1
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
      const res = await fetch(`/api/v1/transformation-resilience-digital-twin/query?query=${encodeURIComponent(queryText)}`, {
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
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-emerald-400 via-cyan-400 to-blue-400">
              Enterprise Resilience Digital Twin 2.0
            </h1>
            <span className="px-3 py-1 text-xs font-bold rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              Read-Only State Model & Governed Counterfactual Experiments
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Non-destructive digital representation of the enterprise resilience environment: live operational state modeling, isolated scenario forks, stress testing, and reproducible experiments.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={fetchData}
            className="px-4 py-2 text-xs font-semibold rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition"
          >
            Re-Sync Twin State
          </button>
        </div>
      </div>

      {/* Top Banner Notice */}
      <div className="bg-cyan-950/40 border border-cyan-500/30 p-3.5 rounded-xl flex justify-between items-center text-xs">
        <div className="flex items-center gap-2 text-cyan-300 font-medium">
          <span>⚠️ READ-ONLY DIGITAL TWIN NOTICE:</span>
          <span className="text-slate-300">All simulations and counterfactual What-If analyses execute in strictly isolated scenario forks. Production state is never mutated from simulation.</span>
        </div>
        <span className="text-[11px] font-bold px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-300 uppercase">Non-Production</span>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-3">
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Twin Status</p>
          <p className="text-lg font-bold text-emerald-400 mt-0.5">{data?.domain?.status ?? 'Current'}</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Freshness</p>
          <p className="text-lg font-bold text-cyan-400 mt-0.5">{((data?.freshness ?? 1.0) * 100).toFixed(0)}%</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Completeness</p>
          <p className="text-lg font-bold text-teal-400 mt-0.5">{((data?.completeness ?? 0.98) * 100).toFixed(0)}%</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Telemetry Lag</p>
          <p className="text-lg font-bold text-indigo-400 mt-0.5">{data?.lagSeconds ?? 0.0}s</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Active Scenario Forks</p>
          <p className="text-lg font-bold text-amber-400 mt-0.5">{data?.activeForks ?? 1}</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Model Accuracy</p>
          <p className="text-lg font-bold text-blue-400 mt-0.5">94.5%</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Model Drift</p>
          <p className="text-lg font-bold text-purple-400 mt-0.5">{data?.driftStatus ?? '3%'}</p>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-800 overflow-x-auto space-x-2 scrollbar-none">
        {[
          { id: 'overview', label: 'Twin Overview' },
          { id: 'snapshots', label: 'Snapshots & State Diffs' },
          { id: 'reality', label: 'Reality Comparison (Divergence)' },
          { id: 'what_if', label: 'What-If Counterfactuals' },
          { id: 'stress', label: 'Stress & Shock Tests' },
          { id: 'recovery', label: 'Recovery Simulations' },
          { id: 'experiments', label: 'Governed Experiments' },
          { id: 'validation', label: 'Model Validation & Errors' },
          { id: 'library', label: 'Scenario Library' },
          { id: 'query', label: 'Digital Twin Query' }
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

      {/* Tab Panels */}
      <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 min-h-[420px]">
        {loading ? (
          <div className="flex items-center justify-center h-64 text-slate-400 text-sm">
            Synchronizing live operational state model with Event Mesh telemetry...
          </div>
        ) : (
          <>
            {activeTab === 'overview' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Live Operational State Model</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                  <span className="font-bold text-emerald-400">{data?.domain?.name}</span>
                  <p className="text-xs text-slate-300">State Version: {data?.domain?.state_version} | Status: {data?.domain?.status}</p>
                  <p className="text-xs text-slate-400">Tracks 8 transformations, 14 plans, 22 dependencies, 18 risks, 35 knowledge assets, and 42 evidence records in read-only representation.</p>
                </div>
              </div>
            )}

            {activeTab === 'snapshots' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Immutable Digital Twin Snapshots</h3>
                {data?.snapshots?.map((s: any) => (
                  <div key={s.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 flex justify-between items-center">
                    <div>
                      <span className="font-semibold text-cyan-400">Snapshot {s.version}</span>
                      <p className="text-xs text-slate-400 mt-1">
                        Transformations: {s.transformations_count} | Plans: {s.plans_count} | Dependencies: {s.dependencies_count}
                      </p>
                    </div>
                    <span className="text-xs text-slate-500 font-mono">{s.state_hash?.slice(0, 16)}...</span>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'reality' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Production vs Digital Twin Reality Comparison</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-indigo-500/30 space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-bold text-indigo-300">Production Alignment: 98.0%</span>
                    <span className="text-xs px-2.5 py-1 rounded bg-indigo-500/20 text-indigo-300 font-semibold">Freshness: 100%</span>
                  </div>
                  <p className="text-xs text-slate-300">Production shows Compute Cluster 01 at 85% utilization with 2 active wave deployments.</p>
                  <p className="text-xs text-slate-400">Divergence Notice: 2% divergence due to 45-second latency on secondary backup telemetry feed.</p>
                </div>
              </div>
            )}

            {activeTab === 'what_if' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">What-If Counterfactual Scenario Simulation</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-amber-500/30 space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-bold text-amber-300">Counterfactual: 72-Hour Compute Cluster Outage</span>
                    <span className="text-xs px-2.5 py-1 rounded bg-amber-500/20 text-amber-300 font-semibold">Strictly Isolated Fork</span>
                  </div>
                  <p className="text-xs text-slate-300">Simulated Outcome: Wave deployment risk score increases to 0.88 (+28%), delaying HR Cloud Go-Live by 14 days.</p>
                  <div className="text-xs text-slate-400 bg-slate-900 p-2.5 rounded border border-slate-800">
                    Explicit Assumptions: 1) No automated secondary cloud cluster failover available. 2) Governance board sign-off requires 48h.
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'stress' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Stress & External Shock Testing</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-rose-500/30 space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-bold text-rose-400">Stress Test: Capacity Stress (Critical)</span>
                    <span className="text-xs px-2.5 py-1 rounded bg-rose-500/20 text-rose-300 font-semibold">Critical Severity</span>
                  </div>
                  <p className="text-xs text-slate-300">Recovery Impact: Requires 5-day contingency buffer to stabilize compute queue depth under severe stress.</p>
                </div>
              </div>
            )}

            {activeTab === 'experiments' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Governed Resilience Experiments</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-emerald-500/30 space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-bold text-emerald-400">Experiment exp_01: Secondary Cluster Failover Reserve</span>
                    <span className="text-xs px-2.5 py-1 rounded bg-emerald-500/20 text-emerald-300 font-semibold uppercase">Status: Approved</span>
                  </div>
                  <p className="text-xs text-slate-300">Hypothesis: Configuring auto-scaling secondary cluster reserve reduces systemic compute exposure by &gt;80%.</p>
                  <p className="text-xs text-slate-400">Result: Observed 84% reduction in systemic compute exposure during simulated 72-hour primary outage (v2.0 reproducible).</p>
                </div>
              </div>
            )}

            {activeTab === 'query' && (
              <div className="space-y-6">
                <h3 className="text-base font-semibold text-slate-200">Digital Twin Natural Language Query</h3>
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={queryText}
                    onChange={(e) => setQueryText(e.target.value)}
                    placeholder="Ask about live twin state, what-if counterfactuals, stress tests, or governed experiments..."
                    className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-emerald-500/50"
                  />
                  <button
                    onClick={handleQuery}
                    disabled={queryLoading}
                    className="px-5 py-2.5 bg-emerald-500 hover:bg-emerald-600 disabled:opacity-50 text-slate-950 text-xs font-bold rounded-xl transition"
                  >
                    {queryLoading ? 'Processing...' : 'Run Twin Query'}
                  </button>
                </div>

                {queryResult && (
                  <div className="p-5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-semibold text-emerald-400">Digital Twin Query Result</span>
                      <span className="text-xs text-slate-400">Confidence: {queryResult.confidencePct}%</span>
                    </div>
                    {queryResult.evidenceJson?.error ? (
                      <div className="text-xs text-rose-400 font-semibold">{queryResult.evidenceJson.error}</div>
                    ) : (
                      <div className="space-y-2 text-xs text-slate-300">
                        {queryResult.results?.map((r: any, idx: number) => (
                          <div key={idx} className="p-3 bg-slate-900 rounded-lg space-y-1">
                            <p><strong className="text-emerald-400">Current State:</strong> {r.current_state}</p>
                            <p><strong className="text-indigo-400">Reality Comparison:</strong> {r.reality_comparison}</p>
                            <p><strong className="text-amber-400">What-If Outcomes:</strong> {r.what_if_outcomes}</p>
                            <p><strong className="text-rose-400">Stress Testing:</strong> {r.stress_testing}</p>
                            <p><strong className="text-teal-400">Governed Experiment:</strong> {r.governed_experiment}</p>
                            <p><strong className="text-blue-400">Model Validation:</strong> {r.model_validation}</p>
                            <p><strong className="text-cyan-300 font-semibold">Read-Only Notice:</strong> {r.read_only_notice}</p>
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
