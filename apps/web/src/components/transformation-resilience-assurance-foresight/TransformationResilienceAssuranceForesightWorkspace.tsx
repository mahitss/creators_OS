'use client';

import React, { useState, useEffect } from 'react';

export function TransformationResilienceAssuranceForesightWorkspace() {
  const [activeTab, setActiveTab] = useState<
    | 'overview'
    | 'signals'
    | 'indicators'
    | 'pressures'
    | 'emerging_risks'
    | 'forecasts'
    | 'scenarios'
    | 'early_warnings'
    | 'windows'
    | 'preventive_options'
    | 'recommendations'
    | 'calibrations'
    | 'false_positives'
    | 'false_negatives'
    | 'context_shifts'
    | 'regime_changes'
    | 'clusters'
    | 'systemic_warnings'
    | 'cascades'
    | 'escalations'
    | 'lessons'
    | 'query'
  >('overview');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('What risks are emerging and what preventive options are available?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/transformation-resilience-assurance-foresight');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      } else {
        // Fallback seed data
        setData({
          domainsCount: 1,
          signalsCount: 1,
          indicatorsCount: 1,
          pressuresCount: 1,
          emergingRisksCount: 1,
          forecastsCount: 1,
          scenariosCount: 2,
          warningsCount: 1,
          windowsCount: 1,
          optionsCount: 2,
          systemicWarningsCount: 1,
          lessonsCount: 1,
          domains: [
            { id: 'fdom_01', name: 'Global Enterprise Assurance Foresight & Emerging Conflict Intelligence 2.0', owner: 'Principal Enterprise Assurance Foresight Architect', status: 'active', version: 'v2.0' }
          ],
          signals: [
            { id: 'fsig_01', source: 'resilience_sensing', type: 'capacity_pressure', description: 'Gradual 15% increase in Simulation Cluster 01 queue depth over past 14 days.', confidence: 0.94 }
          ],
          indicators: [
            { id: 'lind_01', name: 'Simulation Compute Capacity Utilization Indicator', direction: 'increasing', threshold: 0.85, state: 'warning' }
          ],
          pressures: [
            { id: 'press_01', capacity_pressure: 0.85, deadline_pressure: 0.75, conflict_pressure: 0.40, risk_pressure: 0.20 }
          ],
          emergingRisks: [
            { id: 'emrisk_01', risk_name: 'Q3 Wave 4 Simulation Compute Deficit Risk', horizon: 'near_term', confidence: 0.92, status: 'developing', affected_plans_json: ['aplan_01', 'aplan_hr_cloud_02'] }
          ],
          forecasts: [
            { id: 'fcst_01', target: 'Simulation Cluster 01 Capacity Deficit in Week 3', horizon: 'near_term', baseline_value: 0.84, expected_state_value: 0.92, lower_bound: 0.88, central_estimate: 0.92, upper_bound: 0.95, confidence: 0.95, uncertainty: 0.05 }
          ],
          scenarios: [
            { id: 'fscen_01', scenario_type: 'continue_current_state', risk_score: 0.25, coverage_score: 0.84, capacity_score: 0.70 },
            { id: 'fscen_02', scenario_type: 'resequence', risk_score: 0.08, coverage_score: 0.92, capacity_score: 0.85 }
          ],
          warnings: [
            { id: 'ewarn_01', severity: 'high', horizon: 'near_term', recommended_attention: 'Preemptively resequence Q3 simulation execution windows prior to week 3 peak load.', status: 'open', confidence: 0.95 }
          ],
          interventionWindows: [
            { id: 'iwin_01', estimated_duration_days: 10, confidence: 0.92, constraints: 'Resequencing must be confirmed by Governance Board prior to week 2 close.' }
          ],
          preventiveOptions: [
            { id: 'popt_baseline_01', option_type: 'do_nothing', title: 'Baseline Option: Do Nothing / Continue Current State', risk_reduction: 0.0, coverage: 0.84, effort: 'none', reversibility: 'high' },
            { id: 'popt_resequence_01', option_type: 'resequence', title: 'Preemptive Resequencing Option (Stagger simulation runs by 7 days)', risk_reduction: 0.90, coverage: 0.92, effort: 'medium', reversibility: 'high' }
          ],
          recommendations: [
            { id: 'frec_01', label: 'ANALYTICAL RECOMMENDATION — NOT DECISION', recommended_option: 'resequence', reason: 'Preemptive resequencing eliminates predicted compute bottleneck while preserving 92% coverage.', confidence: 0.95 }
          ],
          regimeChanges: [
            { id: 'regchange_01', description: 'Suspected regime change: transition from hybrid-cloud to multi-cloud infrastructure alters historical latency baselines.', status: 'suspected' }
          ],
          systemicWarnings: [
            { id: 'syswarn_01', pattern_description: 'Systemic capacity pressure building across multiple Q3 transformation waves.', severity: 'critical', affected_transformations_json: ['Cloud Transformation Wave 3', 'HR Cloud Wave 4'] }
          ],
          lessons: [
            { id: 'fless_01', lesson_type: 'leading_indicator', title: 'Simulation Capacity Leading Indicator Lesson', description: 'Tracking queue depth trend 14 days in advance provides a 10-day intervention window to preempt compute bottlenecks.' }
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
      const res = await fetch(`/api/v1/transformation-resilience-assurance-foresight/query?query=${encodeURIComponent(queryText)}`, {
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
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 via-pink-400 to-amber-400">
              Assurance Foresight & Early-Warning Intelligence 2.0
            </h1>
            <span className="px-3 py-1 text-xs font-semibold rounded-full bg-purple-500/10 text-purple-400 border border-purple-500/20">
              Human-Governed Preventive Planning
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Detect emerging conditions before they become material assurance failures: live signals, leading indicators, range forecasts, early warnings, intervention windows, and preventive options.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={fetchData}
            className="px-4 py-2 text-xs font-medium rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition"
          >
            Refresh Foresight Engine
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Foresight Status</p>
          <p className="text-xl font-bold text-purple-400 mt-1">Active</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Live Signals</p>
          <p className="text-xl font-bold text-pink-400 mt-1">{data?.signalsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Indicator State</p>
          <p className="text-xl font-bold text-amber-400 mt-1">Warning</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Emerging Risks</p>
          <p className="text-xl font-bold text-rose-500 mt-1">{data?.emergingRisksCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Forecast Confidence</p>
          <p className="text-xl font-bold text-teal-400 mt-1">95.0%</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Intervention Window</p>
          <p className="text-xl font-bold text-cyan-400 mt-1">10 Days</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Preventive Options</p>
          <p className="text-xl font-bold text-indigo-400 mt-1">{data?.optionsCount ?? 2}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Systemic Warnings</p>
          <p className="text-xl font-bold text-red-400 mt-1">{data?.systemicWarningsCount ?? 1}</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 overflow-x-auto space-x-2 scrollbar-none">
        {[
          { id: 'overview', label: 'Foresight Overview' },
          { id: 'signals', label: 'Live Signals' },
          { id: 'indicators', label: 'Leading Indicators' },
          { id: 'pressures', label: 'Assurance Pressure' },
          { id: 'emerging_risks', label: 'Emerging Risks' },
          { id: 'forecasts', label: 'Range Forecasts' },
          { id: 'scenarios', label: 'Forecast Scenarios' },
          { id: 'early_warnings', label: 'Early Warnings' },
          { id: 'windows', label: 'Intervention Windows' },
          { id: 'preventive_options', label: 'Preventive Options' },
          { id: 'recommendations', label: 'Analytical Recommendations' },
          { id: 'calibrations', label: 'Forecast Calibration' },
          { id: 'false_positives', label: 'False Positives' },
          { id: 'false_negatives', label: 'False Negatives' },
          { id: 'context_shifts', label: 'Context Shifts' },
          { id: 'regime_changes', label: 'Regime Changes' },
          { id: 'clusters', label: 'Signal Clusters' },
          { id: 'systemic_warnings', label: 'Systemic Early Warnings' },
          { id: 'cascades', label: 'Foresight Cascades' },
          { id: 'escalations', label: 'Foresight Escalations' },
          { id: 'lessons', label: 'Foresight Lessons' },
          { id: 'query', label: 'Assurance Foresight Query' }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-2.5 text-xs font-semibold whitespace-nowrap border-b-2 transition ${
              activeTab === tab.id
                ? 'border-purple-400 text-purple-400 bg-purple-500/5'
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
            Processing live signals, updating leading indicators, generating range forecasts, and analyzing intervention windows...
          </div>
        ) : (
          <>
            {activeTab === 'overview' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Assurance Foresight Domain</h3>
                {data?.domains?.map((dom: any) => (
                  <div key={dom.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 flex justify-between items-center">
                    <div>
                      <span className="font-semibold text-purple-400">{dom.name}</span>
                      <p className="text-xs text-slate-400 mt-1">Owner: {dom.owner} | Version: {dom.version}</p>
                    </div>
                    <span className="text-xs px-3 py-1 rounded bg-purple-500/10 text-purple-400 border border-purple-500/20 font-semibold">{dom.status}</span>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'signals' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Live Foresight Telemetry Signals</h3>
                {data?.signals?.map((sig: any) => (
                  <div key={sig.id} className="p-4 rounded-xl bg-slate-950/60 border border-purple-500/30 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-semibold text-purple-400">Signal ID: {sig.id} ({sig.type})</span>
                      <span className="text-xs px-2.5 py-1 rounded bg-purple-500/20 text-purple-300 font-semibold">Quality: {(sig.source_quality * 100).toFixed(0)}%</span>
                    </div>
                    <p className="text-xs text-slate-300">{sig.description}</p>
                    <p className="text-xs text-slate-400">Source: {sig.source} | Confidence: {(sig.confidence * 100).toFixed(0)}%</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'indicators' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Leading Indicators</h3>
                {data?.indicators?.map((ind: any) => (
                  <div key={ind.id} className="p-4 rounded-xl bg-slate-950/60 border border-amber-500/30 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-semibold text-amber-400">{ind.name}</span>
                      <span className="text-xs px-2.5 py-1 rounded bg-amber-500/20 text-amber-300 font-semibold uppercase">State: {ind.state}</span>
                    </div>
                    <p className="text-xs text-slate-300">Direction: {ind.direction} | Warning Threshold: {(ind.warning_level * 100).toFixed(0)}% | Critical: {(ind.critical_level * 100).toFixed(0)}%</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'forecasts' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Range Forecasts (Exposing Uncertainty & Bounds)</h3>
                {data?.forecasts?.map((fcst: any) => (
                  <div key={fcst.id} className="p-4 rounded-xl bg-slate-950/60 border border-teal-500/30 space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-semibold text-teal-400">{fcst.target}</span>
                      <span className="text-xs px-2.5 py-1 rounded bg-teal-500/20 text-teal-300 font-semibold">Confidence: {(fcst.confidence * 100).toFixed(0)}%</span>
                    </div>
                    <div className="grid grid-cols-4 gap-3 text-xs text-slate-300 bg-slate-900 p-3 rounded-lg">
                      <div><p className="text-slate-400">Baseline</p><p className="font-bold text-slate-200">{(fcst.baseline_value * 100).toFixed(0)}%</p></div>
                      <div><p className="text-slate-400">Lower Bound</p><p className="font-bold text-slate-200">{(fcst.lower_bound * 100).toFixed(0)}%</p></div>
                      <div><p className="text-slate-400">Central Estimate</p><p className="font-bold text-teal-300">{(fcst.central_estimate * 100).toFixed(0)}%</p></div>
                      <div><p className="text-slate-400">Upper Bound</p><p className="font-bold text-slate-200">{(fcst.upper_bound * 100).toFixed(0)}%</p></div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'early_warnings' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Early Warnings & Intervention Windows</h3>
                {data?.warnings?.map((warn: any) => (
                  <div key={warn.id} className="p-4 rounded-xl bg-rose-950/30 border border-rose-500/40 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-semibold text-rose-400">Early Warning {warn.id} ({warn.severity})</span>
                      <span className="text-xs px-2.5 py-1 rounded bg-rose-500/20 text-rose-300 font-semibold uppercase">{warn.status}</span>
                    </div>
                    <p className="text-xs text-slate-200">{warn.recommended_attention}</p>
                    {data?.interventionWindows?.map((win: any) => (
                      <p key={win.id} className="text-xs text-cyan-300 bg-slate-900 p-2 rounded">
                        Intervention Window Duration: {win.estimated_duration_days} days | Constraint: {win.constraints}
                      </p>
                    ))}
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'preventive_options' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Preventive Options (Baseline 'Do Nothing' Included)</h3>
                {data?.preventiveOptions?.map((popt: any) => (
                  <div key={popt.id} className="p-4 rounded-xl bg-slate-950/60 border border-indigo-500/30 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-semibold text-indigo-300">{popt.title}</span>
                      <span className="text-xs px-2.5 py-1 rounded bg-indigo-500/20 text-indigo-300 font-semibold uppercase">{popt.option_type}</span>
                    </div>
                    <div className="grid grid-cols-3 gap-2 text-xs text-slate-300">
                      <p>Risk Reduction: <strong>{(popt.risk_reduction * 100).toFixed(0)}%</strong></p>
                      <p>Coverage: <strong>{(popt.coverage * 100).toFixed(0)}%</strong></p>
                      <p>Reversibility: <strong>{popt.reversibility}</strong></p>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'query' && (
              <div className="space-y-6">
                <h3 className="text-base font-semibold text-slate-200">Natural Language Assurance Foresight Query</h3>
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={queryText}
                    onChange={(e) => setQueryText(e.target.value)}
                    placeholder="Ask about emerging risks, range forecasts, early warnings, or preventive options..."
                    className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-purple-500/50"
                  />
                  <button
                    onClick={handleQuery}
                    disabled={queryLoading}
                    className="px-5 py-2.5 bg-purple-500 hover:bg-purple-600 disabled:opacity-50 text-slate-950 text-xs font-semibold rounded-xl transition"
                  >
                    {queryLoading ? 'Processing...' : 'Run Query'}
                  </button>
                </div>

                {queryResult && (
                  <div className="p-5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-semibold text-purple-400">Assurance Foresight Result</span>
                      <span className="text-xs text-slate-400">Confidence: {queryResult.confidencePct}%</span>
                    </div>
                    {queryResult.evidenceJson?.error ? (
                      <div className="text-xs text-rose-400 font-semibold">{queryResult.evidenceJson.error}</div>
                    ) : (
                      <div className="space-y-2 text-xs text-slate-300">
                        {queryResult.results?.map((r: any, idx: number) => (
                          <div key={idx} className="p-3 bg-slate-900 rounded-lg space-y-1">
                            <p><strong className="text-purple-400">Emerging Risks:</strong> {r.emerging_risks}</p>
                            <p><strong className="text-teal-400">Range Forecast:</strong> {r.forecast_range}</p>
                            <p><strong className="text-rose-400">Early Warnings & Intervention Windows:</strong> {r.early_warnings_and_windows}</p>
                            <p><strong className="text-indigo-400">Preventive Options:</strong> {r.preventive_options}</p>
                            <p><strong className="text-amber-300 font-semibold">Governance Notice:</strong> {r.recommendation_notice}</p>
                            <p><strong className="text-cyan-400">Invalidation Conditions:</strong> {r.invalidation_conditions}</p>
                            <p><strong className="text-pink-400">Regime Changes:</strong> {r.regime_changes}</p>
                            <p><strong className="text-red-400">Systemic Warnings:</strong> {r.systemic_early_warnings}</p>
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
