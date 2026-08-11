'use client';

import React, { useState, useEffect } from 'react';

export function TransformationForesightWorkspace() {
  const [activeTab, setActiveTab] = useState<'overview' | 'drivers_signals' | 'scenarios_states' | 'second_order' | 'vulnerability_robustness' | 'opportunities_actions' | 'triggers_calibration' | 'reviews_query'>('overview');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('What future risks should we watch?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/transformation-foresight');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      } else {
        // Fallback seed structure
        setData({
          activeDomainsCount: 1,
          futureDriversCount: 2,
          weakSignalsCount: 1,
          emergingPatternsCount: 1,
          futureStatesCount: 2,
          scenarioImpactsCount: 1,
          secondOrderEffectsCount: 1,
          vulnerabilitiesCount: 1,
          opportunitiesCount: 1,
          noRegretActionsCount: 1,
          triggersCount: 1,
          forecastVersionsCount: 1,
          calibrationAccuracyPct: 96.0,
          drivers: [
            { id: 'drv_zero_trust_ast', driver_type: 'technology', name: 'Autonomous AST Pre-signer Rule Adoption', confidence: 0.94 },
            { id: 'drv_cloud_finops_surge', driver_type: 'economic', name: 'Global Infrastructure Spend Optimization Pressure', confidence: 0.96 }
          ],
          trends: [
            { id: 'tr_01', driver_id: 'drv_zero_trust_ast', direction: 'increasing', velocity: 0.82, acceleration: 0.18, uncertainty_score: 0.14 }
          ],
          signals: [
            { id: 'wsig_01', signal_text: 'Early cross-unit adoption of zero-trust API AST schema validators in pre-production pipelines', possible_meaning: 'Potential shift toward zero-overhead policy authorization across microservices', confidence: 0.68 }
          ],
          patterns: [
            { id: 'epat_01', pattern_name: 'Decentralized Pre-signer Adoption Accelerating Downstream FinOps Wave', frequency: 4, confidence: 0.89 }
          ],
          futureStates: [
            { id: 'fstate_baseline', state_type: 'baseline', description: 'Steady rollout with sub-100ms policy authorization & 28% FinOps cost optimization' },
            { id: 'fstate_disruptive', state_type: 'disruptive', description: 'Accelerated mesh adoption unlocking autonomous real-time policy enforcement' }
          ],
          scenarioImpacts: [
            { id: 'scen_imp_01', scenario_id: 'scen_rapid_api_volume_surge', transformation_ids_json: ['cand_01', 'cand_02'], impact_range_json: { low: '12%', expected: '30%', high: '45%' }, confidence: 0.92 }
          ],
          secondOrderEffects: [
            { id: 'so_01', propagation_path_json: ['Technology AST Driver', 'Zero-Trust Pre-signer Capability', 'FinOps Scaling Wave', '30% OpEx Benefit'], description: 'AST pre-signer deployment eliminates synchronous authorization bottlenecks, directly driving sub-minute FinOps policy enforcement', confidence: 0.88 }
          ],
          vulnerabilities: [
            { id: 'vuln_01', transformation_id: 'cand_01', overall_score: 0.15 }
          ],
          opportunities: [
            { id: 'opp_01', transformation_id: 'cand_01', opportunity_type: 'new_strategic_option', potential_benefit: 'Unlocks multi-region real-time zero-trust compliance automation for future enterprise acquisitions', confidence: 0.93 }
          ],
          noRegretActions: [
            { id: 'nra_01', action_desc: 'Standardize AST pre-signer schema validators across all deployment pipelines', multiscenario_utility: 0.95, reversibility: 'high', downside_risk: 'low' }
          ],
          triggers: [
            { id: 'trig_01', threshold_id: 'thresh_01', status: 'watching', evidence_json: { current_adoption_rate: 0.68, trend: 'approaching threshold' } }
          ],
          forecastVersions: [
            { id: 'fv_01', version_tag: 'v2026.3.1', confidence: 0.93, model_version: 'vpr_foresight_v2.0' }
          ],
          forecastErrors: [
            { id: 'fe_01', error_magnitude: 0.04, direction: 'underestimate' }
          ],
          reviews: [
            { id: 'rev_01', review_cadence: 'monthly', summary_json: { drivers_count: 2, weak_signals_count: 1, top_opportunity: 'Multi-region Zero-Trust compliance automation' } }
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
      const res = await fetch(`/api/v1/transformation-foresight/query?query=${encodeURIComponent(queryText)}`, {
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
            <span className="p-2 bg-indigo-600/20 text-indigo-400 rounded-lg text-lg">🔮</span>
            Enterprise Transformation Foresight + Predictive Scenario Intelligence 2.0
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Observed Signals → Drivers → Future States → Scenarios → Multi-Order Propagation → Vulnerability & Robustness → No-Regret Actions → Triggers & Reviews.
          </p>
        </div>
        <div className="flex gap-2">
          <span className="px-3 py-1 bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 rounded-full text-xs font-semibold">
            Predictive Scenario Intelligence
          </span>
          <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full text-xs font-semibold">
            Forecast Calibration: {data?.calibrationAccuracyPct || 96}%
          </span>
        </div>
      </div>

      {/* Telemetry Header */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Future Drivers</div>
          <div className="text-2xl font-bold text-indigo-400 mt-1">{data?.futureDriversCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Weak Signals</div>
          <div className="text-2xl font-bold text-amber-400 mt-1">{data?.weakSignalsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Scenario Impacts</div>
          <div className="text-2xl font-bold text-purple-400 mt-1">{data?.scenarioImpactsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">No-Regret Actions</div>
          <div className="text-2xl font-bold text-teal-400 mt-1">{data?.noRegretActionsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Active Triggers</div>
          <div className="text-2xl font-bold text-blue-400 mt-1">{data?.triggersCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Forecast Version</div>
          <div className="text-2xl font-bold text-emerald-400 mt-1">v2026.3.1</div>
        </div>
      </div>

      {/* Subsystem Tabs */}
      <div className="flex border-b border-slate-800 gap-2 text-sm overflow-x-auto pb-1">
        {[
          { id: 'overview', label: 'Foresight Overview' },
          { id: 'drivers_signals', label: 'Drivers & Weak Signals' },
          { id: 'scenarios_states', label: 'Scenarios & Future States' },
          { id: 'second_order', label: 'Multi-Order Propagation' },
          { id: 'vulnerability_robustness', label: 'Vulnerability & Robustness' },
          { id: 'opportunities_actions', label: 'Opportunities & No-Regret Actions' },
          { id: 'triggers_calibration', label: 'Triggers & Calibration' },
          { id: 'reviews_query', label: 'Reviews & Natural Language Query' }
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
        <div className="p-8 text-center text-slate-500">Loading Transformation Foresight...</div>
      ) : (
        <div className="space-y-6">
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-indigo-400 flex items-center gap-2">
                  <span>⚡</span> Strategic Future Drivers
                </h2>
                <div className="space-y-2 text-sm">
                  {data?.drivers?.map((d: any) => (
                    <div key={d.id} className="p-3 bg-slate-950 rounded border border-indigo-800/40 flex justify-between items-center text-xs">
                      <div>
                        <div className="font-bold text-slate-100">{d.name}</div>
                        <div className="text-slate-400">Type: {d.driver_type}</div>
                      </div>
                      <span className="px-2 py-0.5 bg-emerald-500/20 text-emerald-300 rounded font-bold">{(d.confidence * 100).toFixed(0)}% Conf</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-amber-400 flex items-center gap-2">
                  <span>📡</span> Early Weak Signals
                </h2>
                <div className="space-y-2 text-sm">
                  {data?.signals?.map((s: any) => (
                    <div key={s.id} className="p-3 bg-slate-950 rounded border border-amber-800/40 space-y-1 text-xs">
                      <div className="font-bold text-amber-300">{s.signal_text}</div>
                      <div className="text-slate-400">Meaning: {s.possible_meaning}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'drivers_signals' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Future Drivers, Trends & Weak Signal Trajectories</h2>
              {data?.drivers?.map((d: any) => (
                <div key={d.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-indigo-300">{d.name} ({d.driver_type})</span>
                    <span className="text-xs px-2 py-0.5 bg-indigo-500/20 text-indigo-300 rounded font-bold">Velocity: 0.82 | Acceleration: 0.18</span>
                  </div>
                  <div className="text-xs text-slate-400">Confidence: {(d.confidence * 100).toFixed(0)}%</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'scenarios_states' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Plausible Future States & Scenario Probability Ranges</h2>
              {data?.futureStates?.map((fs: any) => (
                <div key={fs.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-purple-500">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-purple-300">State Type: {fs.state_type}</span>
                  </div>
                  <p className="text-xs text-slate-300">{fs.description}</p>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'second_order' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Second & Third-Order Effect Propagation Paths</h2>
              {data?.secondOrderEffects?.map((so: any) => (
                <div key={so.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                  <div className="font-bold text-teal-300">Path: {so.propagation_path_json?.join(' → ')}</div>
                  <div className="text-xs text-slate-300">{so.description}</div>
                  <div className="text-xs text-emerald-400 font-semibold">Confidence: {(so.confidence * 100).toFixed(0)}%</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'vulnerability_robustness' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Transformation Vulnerability Profiles & Scenario Robustness</h2>
              {data?.vulnerabilities?.map((v: any) => (
                <div key={v.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-emerald-500">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-slate-200">Transformation: {v.transformation_id}</span>
                    <span className="text-xs px-2 py-0.5 bg-emerald-500/20 text-emerald-300 rounded font-bold">Vulnerability Score: {v.overall_score} (LOW)</span>
                  </div>
                  <div className="text-xs text-slate-400">Robustness: High stability across baseline & disruptive scenarios</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'opportunities_actions' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Strategic Opportunities & No-Regret Preparation Actions</h2>
              {data?.noRegretActions?.map((nra: any) => (
                <div key={nra.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-teal-500">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-teal-300">No-Regret Action</span>
                    <span className="text-xs px-2 py-0.5 bg-teal-500/20 text-teal-300 rounded font-bold">Utility: {(nra.multiscenario_utility * 100).toFixed(0)}%</span>
                  </div>
                  <p className="text-xs text-slate-300">{nra.action_desc}</p>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'triggers_calibration' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Foresight Triggers & Forecast Calibration Tracking</h2>
              {data?.triggers?.map((tr: any) => (
                <div key={tr.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-blue-500">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-blue-300">Trigger Threshold ID: {tr.threshold_id}</span>
                    <span className="text-xs px-2 py-0.5 bg-blue-500/20 text-blue-300 rounded font-bold">Status: {tr.status}</span>
                  </div>
                  <div className="text-xs text-slate-400">Evidence: {JSON.stringify(tr.evidence_json)}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'reviews_query' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Executive Foresight Reviews & Natural Language Query</h2>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={queryText}
                  onChange={(e) => setQueryText(e.target.value)}
                  placeholder="Ask a transformation foresight query..."
                  className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
                />
                <button
                  onClick={handleQuery}
                  disabled={queryLoading}
                  className="px-5 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-medium rounded-lg text-sm transition-colors"
                >
                  {queryLoading ? 'Evaluating...' : 'Query'}
                </button>
              </div>

              {queryResult && (
                <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                  <div className="text-xs text-indigo-400 font-semibold">Query: {queryResult.query}</div>
                  <div className="space-y-2">
                    {queryResult.results?.map((res: any, idx: number) => (
                      <div key={idx} className="p-3 bg-slate-900 rounded space-y-1 text-xs">
                        <div className="font-semibold text-indigo-300">{res.primary_future_driver}</div>
                        <div className="text-slate-300">Trend: {res.driver_trend}</div>
                        <div className="text-amber-300">Weak Signal: {res.weak_signal}</div>
                        <div className="text-purple-300">Impact Range: {res.scenario_impact_range}</div>
                        <div className="text-teal-300">Second-Order Effect: {res.second_order_effect}</div>
                        <div className="text-emerald-400">No-Regret Action: {res.no_regret_action}</div>
                        <div className="text-slate-400">Calibration Error: {res.forecast_calibration}</div>
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
