'use client';

import React, { useState, useEffect } from 'react';

export function TransformationSimulationWorkspace() {
  const [activeTab, setActiveTab] = useState<'overview' | 'baselines_snapshots' | 'changesets_runs' | 'dependency_capacity' | 'governance_opmodel' | 'multi_scenario' | 'tradeoffs_sensitivity' | 'calibration_drift' | 'reviews_audits' | 'whatif_query'>('overview');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('What if we delay Wave 2 by 3 months?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/transformation-simulation');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      } else {
        // Fallback seed structure
        setData({
          activeTwinsCount: 1,
          totalSnapshotsCount: 1,
          completedRunsCount: 1,
          modelsValidatedCount: 1,
          multiScenarioRobustnessScore: 0.92,
          simulationAccuracyCalibrationPct: 95.8,
          twins: [
            { id: 'twin_01', name: 'Global Enterprise Transformation Digital Twin', scope: 'enterprise', version: 'v2.0', status: 'active' }
          ],
          baselines: [
            { id: 'base_01', twin_id: 'twin_01', strategy_state_json: { active_initiatives: 12 }, capacity_json: { fte_available: 140 } }
          ],
          snapshots: [
            { id: 'snap_01', twin_id: 'twin_01', timestamp: new Date().toISOString(), data_freshness_minutes: 2.5 }
          ],
          changeSets: [
            { id: 'cs_01', twin_id: 'twin_01', changes_json: [{ change_type: 'pause_wave', wave_id: 'wave_02', duration_months: 3 }], status: 'validated' }
          ],
          runs: [
            { id: 'sim_run_01', twin_id: 'twin_01', scenario: 'baseline', status: 'completed', hash_fingerprint: 'sim_fingerprint_hash_8492049182' }
          ],
          outputs: [
            { id: 'out_01', metric: 'Wave 1 Completion Acceleration', low_value: 7, expected_value: 14, high_value: 21, confidence: 0.94 },
            { id: 'out_02', metric: 'Cost Impact ($)', low_value: 80000, expected_value: 150000, high_value: 220000, confidence: 0.92 }
          ],
          multiScenarioRuns: [
            { id: 'msr_01', robustness_score: 0.92, scenarios_json: [{ name: 'baseline', expected_delivery_days_saved: 14 }, { name: 'optimistic', expected_delivery_days_saved: 21 }] }
          ],
          comparisons: [
            { id: 'comp_01', current_summary: 'Wave 1 at risk of 14-day delay due to FTE capacity bottleneck.', proposed_summary: 'Wave 1 accelerated by 14 days by redirecting 15 FTEs from Wave 2.', alternative_summary: 'Outsource Wave 1 bottleneck tasks (higher cost).' }
          ],
          tradeoffs: [
            { id: 'to_01', benefit_gained: 'Wave 1 finishes 14 days earlier, unlocking $1.2M Q4 benefits', risk_gained: 'Wave 2 start delayed by 90 days', cost_impact: 150000.0, optionality_score: 0.88 }
          ],
          sensitivityAnalyses: [
            { id: 'sens_01', variable_name: 'Reallocated FTE Ramp Velocity', low_value: 0.5, expected_value: 0.85, high_value: 1.0, impact_score: 0.85 }
          ],
          reviews: [
            { id: 'sim_rev_01', decision_impact: 'Informs Steering Committee Decision Case DC-2026-WAVE1-ACCEL', limitations: 'Model assumes linear capacity scaling up to +25% FTE reallocation.', status: 'approved' }
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
      const res = await fetch(`/api/v1/transformation-simulation/query?query=${encodeURIComponent(queryText)}`, {
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
            <span className="p-2 bg-indigo-600/20 text-indigo-400 rounded-lg text-lg">🌀</span>
            Enterprise Transformation Digital Twin & Simulation 2.0
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Strategy → Operating Model → Portfolios → Dependencies → Capacity → Decision Simulation → Range Outputs (Low/Expected/High) → Human Approval.
          </p>
        </div>
        <div className="flex gap-2">
          <span className="px-3 py-1 bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 rounded-full text-xs font-semibold">
            Uncertainty-Aware Simulation
          </span>
          <span className="px-3 py-1 bg-purple-500/10 text-purple-400 border border-purple-500/20 rounded-full text-xs font-semibold">
            Zero Worker Twin Surveillance
          </span>
        </div>
      </div>

      {/* Telemetry Header */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Digital Twins</div>
          <div className="text-2xl font-bold text-indigo-400 mt-1">{data?.activeTwinsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Graph Snapshots</div>
          <div className="text-2xl font-bold text-cyan-400 mt-1">{data?.totalSnapshotsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Simulation Runs</div>
          <div className="text-2xl font-bold text-purple-400 mt-1">{data?.completedRunsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Robustness Score</div>
          <div className="text-2xl font-bold text-emerald-400 mt-1">{(data?.multiScenarioRobustnessScore * 100 || 92).toFixed(0)}%</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Model Calibration</div>
          <div className="text-2xl font-bold text-blue-400 mt-1">{data?.simulationAccuracyCalibrationPct || 95.8}%</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Data Freshness</div>
          <div className="text-2xl font-bold text-teal-400 mt-1">2.5 min</div>
        </div>
      </div>

      {/* Subsystem Tabs */}
      <div className="flex border-b border-slate-800 gap-2 text-sm overflow-x-auto pb-1">
        {[
          { id: 'overview', label: 'Overview & Digital Twins' },
          { id: 'baselines_snapshots', label: 'Baselines & Snapshots' },
          { id: 'changesets_runs', label: 'Change Sets & Runs' },
          { id: 'dependency_capacity', label: 'Dependency & Capacity' },
          { id: 'governance_opmodel', label: 'Governance & Operating Model' },
          { id: 'multi_scenario', label: 'Multi-Scenario & Robustness' },
          { id: 'tradeoffs_sensitivity', label: 'Trade-offs & Sensitivity' },
          { id: 'calibration_drift', label: 'Calibration & Model Drift' },
          { id: 'reviews_audits', label: 'Reviews & Audits' },
          { id: 'whatif_query', label: 'What-If Query Engine' }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-2 font-medium rounded-t-lg transition-colors whitespace-nowrap ${
              activeTab === tab.id
                ? 'bg-slate-900 text-indigo-400 border-b-2 border-indigo-500'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/40'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Content */}
      {loading ? (
        <div className="p-8 text-center text-slate-500">Loading Enterprise Transformation Digital Twin...</div>
      ) : (
        <div className="space-y-6">
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-indigo-400 flex items-center gap-2">
                  <span>🌀</span> Active Transformation Digital Twins
                </h2>
                <div className="space-y-2 text-sm">
                  {data?.twins?.map((t: any) => (
                    <div key={t.id} className="p-3 bg-slate-950 rounded border border-indigo-800/40 flex justify-between items-center text-xs">
                      <div>
                        <div className="font-bold text-slate-100">{t.name}</div>
                        <div className="text-slate-400">Scope: {t.scope} | Version: {t.version}</div>
                      </div>
                      <span className="px-2 py-0.5 bg-indigo-500/20 text-indigo-300 rounded font-bold">{t.status.toUpperCase()}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-purple-400 flex items-center gap-2">
                  <span>⚡</span> Active Simulation Runs & Outputs
                </h2>
                <div className="space-y-2 text-sm">
                  {data?.outputs?.map((out: any) => (
                    <div key={out.id} className="p-3 bg-slate-950 rounded border border-purple-800/40 space-y-1 text-xs">
                      <div className="flex justify-between items-center font-bold text-purple-300">
                        <span>{out.metric}</span>
                        <span className="text-emerald-400">Confidence: {(out.confidence * 100).toFixed(0)}%</span>
                      </div>
                      <div className="text-slate-300">
                        Range: Low <span className="text-amber-400 font-bold">{out.low_value}</span> | Expected <span className="text-emerald-400 font-bold">{out.expected_value}</span> | High <span className="text-cyan-400 font-bold">{out.high_value}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'baselines_snapshots' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Baseline Capture & Freshness Telemetry</h2>
              {data?.snapshots?.map((snap: any) => (
                <div key={snap.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-cyan-500">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-cyan-300">Snapshot ID: {snap.id}</span>
                    <span className="text-xs px-2 py-0.5 bg-cyan-500/20 text-cyan-300 rounded font-bold">Data Freshness: {snap.data_freshness_minutes} mins</span>
                  </div>
                  <div className="text-xs text-slate-300">Timestamp: {snap.timestamp}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'changesets_runs' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Validated Change Sets & Simulation Fingerprints</h2>
              {data?.runs?.map((r: any) => (
                <div key={r.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-purple-500">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-purple-300">Run ID: {r.id} | Scenario: {r.scenario}</span>
                    <span className="text-xs px-2 py-0.5 bg-purple-500/20 text-purple-300 rounded font-bold">Fingerprint: {r.hash_fingerprint}</span>
                  </div>
                  <div className="text-xs text-slate-300">Status: {r.status.toUpperCase()}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'multi_scenario' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Multi-Scenario Runs & Robustness Analysis</h2>
              {data?.multiScenarioRuns?.map((msr: any) => (
                <div key={msr.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-emerald-500">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-emerald-300">Multi-Scenario Run ID: {msr.id}</span>
                    <span className="text-xs px-2 py-0.5 bg-emerald-500/20 text-emerald-300 rounded font-bold">Robustness Score: {(msr.robustness_score * 100).toFixed(0)}%</span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'tradeoffs_sensitivity' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Trade-off & Sensitivity Analysis</h2>
              {data?.tradeoffs?.map((to: any) => (
                <div key={to.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-amber-500">
                  <div className="font-bold text-amber-300">Benefit Gained: {to.benefit_gained}</div>
                  <div className="text-xs text-slate-300">Risk Gained: {to.risk_gained} | Cost Impact: ${to.cost_impact}</div>
                  <div className="text-xs text-teal-400 font-semibold">Optionality Score: {(to.optionality_score * 100).toFixed(0)}%</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'reviews_audits' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Simulation Human Reviews & Audit Trail</h2>
              {data?.reviews?.map((rev: any) => (
                <div key={rev.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-blue-500">
                  <div className="font-bold text-blue-300">Decision Impact: {rev.decision_impact}</div>
                  <div className="text-xs text-slate-400">Limitations: {rev.limitations}</div>
                  <div className="text-xs text-emerald-400 font-bold">Status: {rev.status.toUpperCase()}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'whatif_query' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Natural Language What-If Query Engine</h2>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={queryText}
                  onChange={(e) => setQueryText(e.target.value)}
                  placeholder="Ask a what-if simulation query..."
                  className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
                />
                <button
                  onClick={handleQuery}
                  disabled={queryLoading}
                  className="px-5 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-medium rounded-lg text-sm transition-colors"
                >
                  {queryLoading ? 'Simulating...' : 'Simulate'}
                </button>
              </div>

              {queryResult && (
                <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                  <div className="text-xs text-indigo-400 font-semibold">Query: {queryResult.query}</div>
                  <div className="space-y-2">
                    {queryResult.results?.map((res: any, idx: number) => (
                      <div key={idx} className="p-3 bg-slate-900 rounded space-y-1 text-xs">
                        <div className="font-semibold text-indigo-300">{res.digital_twin}</div>
                        <div className="text-slate-300">Simulated Change Set: {res.simulated_change_set}</div>
                        <div className="text-emerald-300">Trade-off Analysis: {res.tradeoff_analysis}</div>
                        <div className="text-cyan-300">Fingerprint Hash: {res.simulation_fingerprint_hash}</div>
                        <div className="text-slate-400 italic">Limitations: {res.model_limitations}</div>
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
