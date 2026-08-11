'use client';

import React, { useState, useEffect } from 'react';

export function ThreatIntelligenceWorkspace() {
  const [activeTab, setActiveTab] = useState<'overview' | 'signals' | 'weak_signals' | 'patterns' | 'emerging' | 'warnings' | 'mitigations' | 'accuracy' | 'blind_spots' | 'nl_query'>('overview');
  const [overviewData, setOverviewData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('What risks are emerging right now?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/threats');
      if (res.ok) {
        const data = await res.json();
        setOverviewData(data);
      } else {
        // Fallback seed data
        setOverviewData({
          signalsCount: 1,
          weakSignalsCount: 1,
          correlationsCount: 1,
          patternsCount: 1,
          threatsCount: 1,
          warningsCount: 1,
          mitigationsCount: 1,
          blindSpotsCount: 1,
          precisionScore: 0.94,
          recallScore: 0.91,
          monitoringCoveragePct: 0.96,
          signals: [
            {
              id: "tsig_01",
              source_type: "telemetry_mesh",
              source_id: "src_gpu_cluster_us_east",
              signal_type: "capacity_change",
              confidence: "high",
              quality: "verified"
            }
          ],
          weakSignals: [
            {
              id: "wsig_01",
              signal_id: "tsig_01",
              novelty_score: 0.88,
              persistence_status: "persists",
              signal_velocity: "increasing_frequency",
              confidence: "high"
            }
          ],
          correlations: [
            {
              id: "tcorr_01",
              source_signal_id: "tsig_01",
              target_signal_id: "tsig_02_vendor_latency",
              connection_type: "associated with shared dependency vendor_gpu_cloud"
            }
          ],
          patterns: [
            {
              id: "tpatt_01",
              pattern_type: "cascade",
              entities_json: ["svc_model_router", "cap_core_01"],
              time_window: "24 hours",
              strength: 0.92,
              confidence: "high"
            }
          ],
          threats: [
            {
              id: "ethr_01",
              name: "US-East GPU Cluster Memory Saturation & Thermal Throttling",
              description: "Gradual memory leakage across node pool 4 leading to capacity degradation and potential cascade.",
              probability_range: "40-60%",
              time_horizon: "days",
              severity: "high",
              confidence: "high",
              status: "emerging"
            }
          ],
          warnings: [
            {
              id: "ewarn_01",
              threat_id: "ethr_01",
              trigger_reason: "Weak signal velocity accelerated by 45% over 12 hours.",
              probability: "40-60%",
              time_horizon: "days",
              impact_summary: "Possible 25% throughput degradation across US-East datacenter if unmitigated.",
              priority: "high",
              status: "new"
            }
          ],
          mitigations: [
            {
              id: "tmit_01",
              threat_id: "ethr_01",
              action_name: "Proactive Node Pool Recycling & Traffic Balancing to EU-Central",
              owner: "usr_ops_lead",
              authorization_status: "approved",
              status: "executing",
              expected_risk_reduction_pct: 0.85,
              actual_risk_reduction_pct: 0.88
            }
          ],
          blindSpots: [
            {
              id: "tbspot_01",
              domain: "Secondary Regional Vendor Data Plane",
              missing_signals_json: ["vendor_bgp_route_flaps"],
              impact_summary: "Delayed detection of third-party network route degradation.",
              severity: "medium",
              recommendation: "Deploy external active route health probes."
            }
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
      const res = await fetch(`/api/v1/threats/query?query=${encodeURIComponent(queryText)}`, {
        method: 'POST'
      });
      if (res.ok) {
        const data = await res.json();
        setQueryResult(data);
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
            <span className="p-2 bg-amber-600/20 text-amber-400 rounded-lg text-lg">⚡</span>
            Enterprise Crisis Prediction & Proactive Threat Intelligence 2.0
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Governed early-warning engine: Signal → Normalization → Weak Signals → Associative Correlation → Threat Patterns → Probability → Early Warning → ActionGateway Mitigation.
          </p>
        </div>
        <div className="flex gap-2">
          <span className="px-3 py-1 bg-amber-500/10 text-amber-400 border border-amber-500/20 rounded-full text-xs font-semibold flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></span>
            Proactive Warning Active
          </span>
          <span className="px-3 py-1 bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 rounded-full text-xs font-semibold">
            Anti-Surveillance Governed
          </span>
        </div>
      </div>

      {/* Telemetry Bar */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Ingested Signals</div>
          <div className="text-2xl font-bold text-slate-100 mt-1">{overviewData?.signalsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Weak Signals</div>
          <div className="text-2xl font-bold text-amber-400 mt-1">{overviewData?.weakSignalsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Emerging Threats</div>
          <div className="text-2xl font-bold text-rose-400 mt-1">{overviewData?.threatsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Early Warnings</div>
          <div className="text-2xl font-bold text-orange-400 mt-1">{overviewData?.warningsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Detection Precision</div>
          <div className="text-2xl font-bold text-emerald-400 mt-1">{((overviewData?.precisionScore || 0) * 100).toFixed(0)}%</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Monitoring Coverage</div>
          <div className="text-2xl font-bold text-cyan-400 mt-1">{((overviewData?.monitoringCoveragePct || 0) * 100).toFixed(0)}%</div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 gap-2 text-sm overflow-x-auto pb-1">
        {[
          { id: 'overview', label: 'Threat Overview' },
          { id: 'signals', label: 'Ingested Signals' },
          { id: 'weak_signals', label: 'Weak Signals' },
          { id: 'patterns', label: 'Threat Patterns' },
          { id: 'emerging', label: 'Emerging Threats' },
          { id: 'warnings', label: 'Early Warnings' },
          { id: 'mitigations', label: 'ActionGateway Mitigations' },
          { id: 'accuracy', label: 'Accuracy & Calibration' },
          { id: 'blind_spots', label: 'Blind Spots & Coverage' },
          { id: 'nl_query', label: 'Natural Language Query' }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-2 font-medium rounded-t-lg transition-colors whitespace-nowrap ${
              activeTab === tab.id
                ? 'bg-slate-900 text-amber-400 border-b-2 border-amber-500'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/40'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      {loading ? (
        <div className="p-8 text-center text-slate-500">Loading Threat Intelligence state...</div>
      ) : (
        <div className="space-y-6">
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-amber-400 flex items-center gap-2">
                  <span>⚡</span> Active Emerging Threat
                </h2>
                {overviewData?.threats?.[0] && (
                  <div className="space-y-3 text-sm">
                    <div className="font-bold text-slate-100 text-base">{overviewData.threats[0].name}</div>
                    <p className="text-slate-400">{overviewData.threats[0].description}</p>
                    <div className="grid grid-cols-2 gap-2 text-xs pt-2">
                      <span className="p-2 bg-amber-950/40 border border-amber-800/40 rounded">Probability: <strong className="text-amber-300">{overviewData.threats[0].probability_range}</strong></span>
                      <span className="p-2 bg-slate-800/60 rounded">Time Horizon: <strong className="text-slate-200">{overviewData.threats[0].time_horizon}</strong></span>
                    </div>
                  </div>
                )}
              </div>

              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-emerald-400 flex items-center gap-2">
                  <span>🛡️</span> ActionGateway Preventive Mitigation
                </h2>
                {overviewData?.mitigations?.[0] && (
                  <div className="space-y-3 text-sm">
                    <div className="font-bold text-slate-100">{overviewData.mitigations[0].action_name}</div>
                    <div className="text-xs text-slate-400">Owner: {overviewData.mitigations[0].owner} | Status: <strong className="text-emerald-400">{overviewData.mitigations[0].status}</strong></div>
                    <div className="p-3 bg-slate-950 rounded border border-slate-800 text-xs text-slate-300">
                      Expected Risk Reduction: {(overviewData.mitigations[0].expected_risk_reduction_pct * 100).toFixed(0)}% | Measured Reduction: {(overviewData.mitigations[0].actual_risk_reduction_pct * 100).toFixed(0)}%
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'signals' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Ingested Raw & Normalized Signals</h2>
              {overviewData?.signals?.map((sig: any) => (
                <div key={sig.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-slate-200">Type: {sig.signal_type}</span>
                    <span className="text-xs px-2 py-0.5 bg-emerald-500/10 text-emerald-400 rounded">Quality: {sig.quality}</span>
                  </div>
                  <div className="text-xs text-slate-400">Source: {sig.source_type} ({sig.source_id}) | Confidence: {sig.confidence}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'weak_signals' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Detected Weak Signals</h2>
              {overviewData?.weakSignals?.map((ws: any) => (
                <div key={ws.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-amber-300">Novelty Score: {ws.novelty_score}</span>
                    <span className="text-xs px-2 py-0.5 bg-amber-500/10 text-amber-400 rounded">Velocity: {ws.signal_velocity}</span>
                  </div>
                  <div className="text-xs text-slate-400">Signal Reference: {ws.signal_id} | Persistence: {ws.persistence_status}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'patterns' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Recognized Threat Patterns</h2>
              {overviewData?.patterns?.map((p: any) => (
                <div key={p.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-indigo-400">Pattern Type: {p.pattern_type}</span>
                    <span className="text-xs text-slate-400">Strength: {p.strength}</span>
                  </div>
                  <div className="text-xs text-slate-300">Entities Involved: {JSON.stringify(p.entities_json)}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'emerging' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Emerging Threats & Probability Ranges</h2>
              {overviewData?.threats?.map((th: any) => (
                <div key={th.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-rose-300">{th.name}</span>
                    <span className="text-xs px-2 py-0.5 bg-amber-500/20 text-amber-300 rounded font-bold">Probability: {th.probability_range}</span>
                  </div>
                  <p className="text-xs text-slate-400">{th.description}</p>
                  <div className="text-xs text-slate-500">Severity: {th.severity} | Time Horizon: {th.time_horizon} | Status: {th.status}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'warnings' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Dispatched Early Warnings</h2>
              {overviewData?.warnings?.map((w: any) => (
                <div key={w.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-orange-500">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-orange-300">Trigger: {w.trigger_reason}</span>
                    <span className="text-xs px-2 py-0.5 bg-red-500/10 text-red-400 rounded font-bold">Priority: {w.priority}</span>
                  </div>
                  <p className="text-xs text-slate-300">{w.impact_summary}</p>
                  <div className="text-xs text-slate-500">Probability: {w.probability} | Status: {w.status}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'mitigations' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">ActionGateway Preventive Mitigations</h2>
              {overviewData?.mitigations?.map((m: any) => (
                <div key={m.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-emerald-400">{m.action_name}</span>
                    <span className="text-xs px-2 py-0.5 bg-emerald-500/10 text-emerald-400 rounded">{m.status}</span>
                  </div>
                  <p className="text-xs text-slate-400">Precondition: {m.precondition}</p>
                  <div className="text-xs text-slate-500">Owner: {m.owner} | Risk Reduction: {(m.actual_risk_reduction_pct * 100).toFixed(0)}%</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'accuracy' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Detection Accuracy & Calibration</h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                <div className="p-4 bg-slate-950 border border-slate-800 rounded">
                  <div className="text-xs text-slate-400">Precision</div>
                  <div className="text-2xl font-bold text-emerald-400">{((overviewData?.precisionScore || 0.94) * 100).toFixed(0)}%</div>
                </div>
                <div className="p-4 bg-slate-950 border border-slate-800 rounded">
                  <div className="text-xs text-slate-400">Recall</div>
                  <div className="text-2xl font-bold text-cyan-400">{((overviewData?.recallScore || 0.91) * 100).toFixed(0)}%</div>
                </div>
                <div className="p-4 bg-slate-950 border border-slate-800 rounded">
                  <div className="text-xs text-slate-400">Lead Time</div>
                  <div className="text-2xl font-bold text-amber-400">48.5 hours</div>
                </div>
                <div className="p-4 bg-slate-950 border border-slate-800 rounded">
                  <div className="text-xs text-slate-400">False Positives</div>
                  <div className="text-2xl font-bold text-slate-300">6.0%</div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'blind_spots' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Detection Blind Spots & Coverage Gaps</h2>
              {overviewData?.blindSpots?.map((bs: any) => (
                <div key={bs.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-amber-300">{bs.domain}</span>
                    <span className="text-xs px-2 py-0.5 bg-amber-500/10 text-amber-400 rounded">Severity: {bs.severity}</span>
                  </div>
                  <p className="text-xs text-slate-300">{bs.impact_summary}</p>
                  <div className="text-xs text-cyan-400">Recommendation: {bs.recommendation}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'nl_query' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Natural Language Threat Query Interface</h2>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={queryText}
                  onChange={(e) => setQueryText(e.target.value)}
                  placeholder="Ask a threat query..."
                  className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-sm text-slate-100 focus:outline-none focus:border-amber-500"
                />
                <button
                  onClick={handleQuery}
                  disabled={queryLoading}
                  className="px-5 py-2 bg-amber-600 hover:bg-amber-500 text-white font-medium rounded-lg text-sm transition-colors"
                >
                  {queryLoading ? 'Evaluating...' : 'Query'}
                </button>
              </div>

              {queryResult && (
                <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                  <div className="text-xs text-amber-400 font-semibold">Query: {queryResult.query}</div>
                  <div className="space-y-2">
                    {queryResult.results?.map((res: any, idx: number) => (
                      <div key={idx} className="p-3 bg-slate-900 rounded space-y-1 text-xs">
                        <div className="font-semibold text-slate-200">{res.threat_name}</div>
                        <div className="text-amber-300">Probability: {res.probability_range} | Horizon: {res.time_horizon}</div>
                        <div className="text-slate-400">Weak Signal: {res.associated_weak_signal}</div>
                        <div className="text-emerald-400">Mitigation: {res.active_mitigation}</div>
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
