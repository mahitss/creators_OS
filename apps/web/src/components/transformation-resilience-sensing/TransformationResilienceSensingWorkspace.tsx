'use client';

import React, { useState, useEffect } from 'react';

export function TransformationResilienceSensingWorkspace() {
  const [activeTab, setActiveTab] = useState<'overview' | 'observations' | 'quality' | 'drift' | 'warnings' | 'correlations' | 'trends_forecasts' | 'assumptions' | 'investment_reviews' | 'sensing_query'>('overview');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('Has resilience improved or deteriorated over the last 30 days?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/transformation-resilience-sensing');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      } else {
        // Fallback seed data
        setData({
          domainsCount: 1,
          observationsCount: 1,
          activeDriftsCount: 1,
          structuralChangesCount: 1,
          activeWarningsCount: 1,
          signalCorrelationsCount: 1,
          assumptionDriftsCount: 1,
          investmentReviewTriggersCount: 1,
          portfolioState: {
            robustness: 0.94,
            redundancy: 0.91,
            recoverability: 0.95,
            adaptability: 0.92,
            optionality: 0.93,
            observability: 0.96,
            governability: 0.94
          },
          domains: [
            { id: 'sens_dom_01', name: 'Global Enterprise Transformation Resilience Sensing 2.0 Domain', scope: 'enterprise', owner: 'Principal Resilience Sensing Architect', status: 'active', version: 'v2.0' }
          ],
          observations: [
            { id: 'obs_01', source: 'EventMesh.IdentityGateway', metric: 'OAuth Token Resolution Latency (P99)', value: 142.5, confidence: 0.96, freshness: 1.0 }
          ],
          qualities: [
            { id: 'obs_qual_01', completeness: 0.98, freshness: 1.0, consistency: 0.95, reliability: 0.96 }
          ],
          drifts: [
            { id: 'drift_01', drift_type: 'persistent', metric_name: 'Shared Identity Gateway Latency', deviation_pct: 8.4, severity: 'medium' }
          ],
          structuralChanges: [
            { id: 'schange_01', change_type: 'vendor_concentration_increased', affected_scope_json: ['Wave 2 FinOps', 'Wave 3 SSO', 'Wave 4 HR Cloud'], materiality: 'material' }
          ],
          warnings: [
            { id: 'swarn_01', condition: 'IAM OAuth Gateway Latency Degradation & Senior Security Engineer Capacity Contention', severity: 'high', confidence: 0.95, recommended_review: 'Initiate Portfolio Resilience Investment Review for pinv_01 Active-Active deploy.' }
          ],
          correlations: [
            { id: 'scorr_01', signal_a: 'OAuth Gateway Latency P99', signal_b: 'Senior IAM Engineer Backlog', relationship_type: 'observed_correlation', confidence: 0.93 }
          ],
          trends: [
            { id: 'tr_01', dimension: 'recoverability', trend_direction: 'deteriorating', window: '30d' }
          ],
          forecasts: [
            { id: 'fc_01', target_metric: 'Shared Dependency Recovery Margin', forecast_value: 0.84 }
          ],
          assumptions: [
            { id: 'ass_01', assumption_title: 'Primary OAuth Auth Gateway SLA >= 99.99%', source_context: 'Wave 2 FinOps Design', status: 'degraded' }
          ],
          assumptionDrifts: [
            { id: 'assdrift_01', drift_description: 'Actual primary OAuth Gateway availability dropped to 99.91% over 30d window.', severity: 'high' }
          ],
          investmentTriggers: [
            { id: 'invtrig_01', affected_investment_id: 'pinv_01', reason: "Key assumption 'Primary Auth Gateway SLA >= 99.99%' drifted to degraded status.", severity: 'high', review_deadline: '2026-Q3' }
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
      const res = await fetch(`/api/v1/transformation-resilience-sensing/query?query=${encodeURIComponent(queryText)}`, {
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
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 via-sky-400 to-indigo-400">
              Transformation Resilience Sensing 2.0
            </h1>
            <span className="px-3 py-1 text-xs font-semibold rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
              Continuous Portfolio Resilience Intelligence
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Detecting structural drift, vendor concentration, capacity erosion, and assumption degradation across the transformation portfolio.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={fetchData}
            className="px-4 py-2 text-xs font-medium rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition"
          >
            Refresh Sensing Stream
          </button>
        </div>
      </div>

      {/* KPI Overview Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Sensing Domains</p>
          <p className="text-xl font-bold text-cyan-400 mt-1">{data?.domainsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Live Observations</p>
          <p className="text-xl font-bold text-sky-400 mt-1">{data?.observationsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Active Drifts</p>
          <p className="text-xl font-bold text-amber-400 mt-1">{data?.activeDriftsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Structural Changes</p>
          <p className="text-xl font-bold text-rose-400 mt-1">{data?.structuralChangesCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Early Warnings</p>
          <p className="text-xl font-bold text-rose-400 mt-1">{data?.activeWarningsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Correlations</p>
          <p className="text-xl font-bold text-teal-400 mt-1">{data?.signalCorrelationsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Assumption Drifts</p>
          <p className="text-xl font-bold text-indigo-400 mt-1">{data?.assumptionDriftsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Review Triggers</p>
          <p className="text-xl font-bold text-violet-400 mt-1">{data?.investmentReviewTriggersCount ?? 1}</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 overflow-x-auto space-x-2 scrollbar-none">
        {[
          { id: 'overview', label: 'Live Portfolio Dimensions' },
          { id: 'observations', label: 'Telemetry Observations' },
          { id: 'quality', label: 'Signal Quality' },
          { id: 'drift', label: 'Resilience Drift & Changes' },
          { id: 'warnings', label: 'Early Warnings' },
          { id: 'correlations', label: 'Signal Correlations' },
          { id: 'trends_forecasts', label: 'Trends & Forecasts' },
          { id: 'assumptions', label: 'Assumption Monitoring' },
          { id: 'investment_reviews', label: 'Review Triggers' },
          { id: 'sensing_query', label: 'Sensing Query Engine' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-2.5 text-xs font-semibold whitespace-nowrap border-b-2 transition ${
              activeTab === tab.id
                ? 'border-cyan-400 text-cyan-400 bg-cyan-500/5'
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
            Ingesting live resilience observations and computing drift models...
          </div>
        ) : (
          <>
            {activeTab === 'overview' && (
              <div className="space-y-6">
                <h3 className="text-base font-semibold text-slate-200">Current Portfolio Resilience State (7 Dimensions)</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-3">
                  {Object.entries(data?.portfolioState ?? {}).map(([dim, val]: any) => (
                    <div key={dim} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 text-center space-y-1">
                      <span className="text-xs text-slate-400 capitalize">{dim}</span>
                      <p className="text-lg font-bold text-cyan-400">{(val * 100).toFixed(0)}%</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'observations' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Live Resilience Observations</h3>
                {data?.observations?.map((obs: any) => (
                  <div key={obs.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 flex justify-between items-center">
                    <div>
                      <span className="text-sm font-medium text-cyan-400">{obs.metric}</span>
                      <p className="text-xs text-slate-400 mt-1">Source: {obs.source} | Scope: {obs.scope} | Value: {obs.value}</p>
                    </div>
                    <span className="text-xs px-2.5 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-semibold">Confidence: {(obs.confidence * 100).toFixed(0)}%</span>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'quality' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Signal Quality Evaluation</h3>
                {data?.qualities?.map((q: any) => (
                  <div key={q.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-medium text-slate-200">Observation ID: {q.observation_id}</span>
                      <span className="text-xs px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">Reliability: {(q.reliability * 100).toFixed(0)}%</span>
                    </div>
                    <p className="text-xs text-slate-400">Completeness: {(q.completeness * 100).toFixed(0)}% | Freshness: {(q.freshness * 100).toFixed(0)}% | Consistency: {(q.consistency * 100).toFixed(0)}%</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'drift' && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-base font-semibold text-slate-200 mb-3">Resilience Metric Drift</h3>
                  {data?.drifts?.map((dr: any) => (
                    <div key={dr.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 flex justify-between items-center mb-3">
                      <div>
                        <span className="text-sm font-medium text-amber-400">{dr.metric_name}</span>
                        <p className="text-xs text-slate-400 mt-1">Drift Type: {dr.drift_type} | Deviation: +{dr.deviation_pct}%</p>
                      </div>
                      <span className="text-xs px-2.5 py-1 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20 font-semibold">{dr.severity}</span>
                    </div>
                  ))}
                </div>
                <div>
                  <h3 className="text-base font-semibold text-slate-200 mb-3">Structural Changes</h3>
                  {data?.structuralChanges?.map((sc: any) => (
                    <div key={sc.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2 mb-3">
                      <div className="flex justify-between items-center">
                        <span className="text-sm font-medium text-rose-400">Type: {sc.change_type}</span>
                        <span className="text-xs px-2 py-0.5 rounded bg-rose-500/10 text-rose-400 border border-rose-500/20">{sc.materiality}</span>
                      </div>
                      <p className="text-xs text-slate-400">Affected Scope: {sc.affected_scope_json?.join(', ')}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'warnings' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">High-Confidence Early Warnings</h3>
                {data?.warnings?.map((w: any) => (
                  <div key={w.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-medium text-rose-400">{w.condition}</span>
                      <span className="text-xs px-2.5 py-1 rounded bg-rose-500/10 text-rose-400 border border-rose-500/20 font-semibold">{w.severity}</span>
                    </div>
                    <p className="text-xs text-slate-300">Recommended Review: {w.recommended_review}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'correlations' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Cross-Signal Correlations</h3>
                {data?.correlations?.map((c: any) => (
                  <div key={c.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 flex justify-between items-center">
                    <div>
                      <span className="text-sm font-medium text-teal-400">{c.signal_a} ↔ {c.signal_b}</span>
                      <p className="text-xs text-slate-400 mt-1">Relationship: {c.relationship_type} (Does NOT imply confirmed causation)</p>
                    </div>
                    <span className="text-xs px-2.5 py-1 rounded bg-teal-500/10 text-teal-400 border border-teal-500/20 font-semibold">Confidence: {(c.confidence * 100).toFixed(0)}%</span>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'trends_forecasts' && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h3 className="text-base font-semibold text-slate-200 mb-3">Historical Trajectory & Trends</h3>
                  {data?.trends?.map((t: any) => (
                    <div key={t.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 mb-3">
                      <span className="text-xs font-semibold text-cyan-400">Dimension: {t.dimension}</span>
                      <p className="text-xs text-slate-400 mt-1">Direction: {t.trend_direction} ({t.window} window)</p>
                    </div>
                  ))}
                </div>
                <div>
                  <h3 className="text-base font-semibold text-slate-200 mb-3">Resilience Margin Forecasts</h3>
                  {data?.forecasts?.map((fc: any) => (
                    <div key={fc.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 mb-3">
                      <span className="text-xs font-semibold text-indigo-400">Target: {fc.target_metric}</span>
                      <p className="text-xs text-slate-400 mt-1">Forecast Value: {(fc.forecast_value * 100).toFixed(0)}%</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'assumptions' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Resilience Assumption Monitoring & Drift</h3>
                {data?.assumptions?.map((ass: any) => (
                  <div key={ass.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-medium text-slate-200">{ass.assumption_title}</span>
                      <span className="text-xs px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20">{ass.status}</span>
                    </div>
                    <p className="text-xs text-slate-400">Source: {ass.source_context}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'investment_reviews' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Governance Review Triggers</h3>
                {data?.investmentTriggers?.map((trig: any) => (
                  <div key={trig.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-medium text-violet-400">Affected Investment: {trig.affected_investment_id}</span>
                      <span className="text-xs px-2 py-0.5 rounded bg-violet-500/10 text-violet-400 border border-violet-500/20">Deadline: {trig.review_deadline}</span>
                    </div>
                    <p className="text-xs text-slate-300">Reason: {trig.reason}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'sensing_query' && (
              <div className="space-y-6">
                <h3 className="text-base font-semibold text-slate-200">Natural Language Sensing Query Engine</h3>
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={queryText}
                    onChange={(e) => setQueryText(e.target.value)}
                    placeholder="Ask a resilience sensing question..."
                    className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-500/50"
                  />
                  <button
                    onClick={handleQuery}
                    disabled={queryLoading}
                    className="px-5 py-2.5 bg-cyan-500 hover:bg-cyan-600 disabled:opacity-50 text-slate-950 text-xs font-semibold rounded-xl transition"
                  >
                    {queryLoading ? 'Processing...' : 'Run Query'}
                  </button>
                </div>

                {queryResult && (
                  <div className="p-5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-semibold text-cyan-400">Sensing Query Result</span>
                      <span className="text-xs text-slate-400">Confidence: {queryResult.confidencePct}%</span>
                    </div>
                    {queryResult.evidenceJson?.error ? (
                      <div className="text-xs text-rose-400 font-semibold">{queryResult.evidenceJson.error}</div>
                    ) : (
                      <div className="space-y-2 text-xs text-slate-300">
                        {queryResult.results?.map((r: any, idx: number) => (
                          <div key={idx} className="p-3 bg-slate-900 rounded-lg space-y-1">
                            <p><strong className="text-cyan-400">Domain:</strong> {r.sensing_domain}</p>
                            <p><strong className="text-sky-400">Live Observation:</strong> {r.live_observation}</p>
                            <p><strong className="text-amber-400">Resilience Drift:</strong> {r.detected_drift}</p>
                            <p><strong className="text-rose-400">Structural Change:</strong> {r.structural_change}</p>
                            <p><strong className="text-teal-400">Signal Correlation:</strong> {r.signal_correlation}</p>
                            <p><strong className="text-indigo-400">Assumption Drift:</strong> {r.assumption_drift}</p>
                            <p><strong className="text-violet-400">Review Trigger:</strong> {r.investment_review_trigger}</p>
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
