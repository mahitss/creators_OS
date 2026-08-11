'use client';

import React, { useState, useEffect } from 'react';

export function TransformationControlWorkspace() {
  const [activeTab, setActiveTab] = useState<'overview' | 'live_state' | 'situations' | 'root_causes' | 'wave_readiness' | 'change_requests' | 'incidents' | 'reviews' | 'nl_query'>('overview');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('What changed in the transformation portfolio?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);
  const [approvalMsg, setApprovalMsg] = useState<string | null>(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/transformation-control');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      } else {
        // Fallback seed structure
        setData({
          controlTowersCount: 1,
          liveStatesCount: 1,
          signalsCount: 2,
          situationsCount: 1,
          rootCausesCount: 1,
          earlyWarningsCount: 1,
          waveReadinessesCount: 1,
          proposedChangeRequestsCount: 1,
          activeIncidentsCount: 1,
          activeEscalationsCount: 1,
          weeklyReviewsCount: 1,
          learningsCount: 1,
          controlTowerStatus: 'healthy',
          overallWaveReadinessPct: 92.0,
          towers: [
            {
              id: 'tct_01',
              name: 'Global Enterprise Transformation Control Tower 2.0',
              portfolio_id: 'transport_01',
              status: 'healthy',
              owner: 'usr_chief_transformation_officer'
            }
          ],
          liveStates: [
            {
              id: 'lstate_01',
              planned_state_json: { wave_1_status: 'executing', schedule_variance: '0d', capacity_usage: '60%' },
              actual_state_json: { wave_1_status: 'executing', schedule_variance: '-2d', capacity_usage: '65%' },
              forecast_state_json: { completion_confidence: '94%', expected_completion: 'Q3-2026' },
              last_change: 'Skill Certification Auto-signer pre-validation completed',
              last_evaluation: 'Schedule, capacity, and critical path within nominal thresholds.'
            }
          ],
          signals: [
            {
              id: 'sig_01',
              signal_type: 'capacity',
              severity: 'medium',
              status: 'detected',
              evidence_json: { engineering_headroom: '15% buffer remaining in Q3' }
            },
            {
              id: 'sig_02',
              signal_type: 'dependency',
              severity: 'low',
              status: 'acknowledged',
              evidence_json: { upstream_policy_api: 'minor 2-day integration delay' }
            }
          ],
          situations: [
            {
              id: 'sit_wave_1_capacity_headroom',
              affected_transformations_json: ['cand_01', 'cand_02'],
              affected_waves_json: ['wave_01'],
              evidence_json: { correlated_telemetry: 'Engineering capacity compression coupled with upstream policy API delay' },
              confidence: 'high',
              severity: 'medium'
            }
          ],
          rootCauses: [
            {
              id: 'rc_01',
              situation_id: 'sit_wave_1_capacity_headroom',
              category: 'capacity',
              evidence_label: 'supported',
              description: 'Simultaneous compliance testing and FinOps initial pilot created transient engineering capacity friction.',
              confidence: 'high'
            }
          ],
          earlyWarnings: [
            {
              id: 'ew_01',
              warning_trigger: 'Engineering buffer capacity nearing 15% threshold for Wave 1',
              severity: 'medium',
              status: 'active'
            }
          ],
          waveReadinesses: [
            {
              id: 'wread_01',
              wave_id: 'wave_01',
              capability_readiness: 0.95,
              technology_readiness: 0.98,
              process_readiness: 0.90,
              capacity_readiness: 0.92,
              dependency_readiness: 0.96,
              risk_readiness: 0.94,
              adoption_readiness: 0.88,
              status: 'ready'
            }
          ],
          changeRequests: [
            {
              id: 'cr_sequence_adjust_01',
              request_type: 'sequence',
              proposed_change_desc: 'Advance FinOps parallelization phase post Wave 1 exit criteria clearance',
              impact_analysis_json: { capacity_impact: '+5%', time_saved: '14d', risk_delta: '-0.05' },
              status: 'proposed'
            }
          ],
          incidents: [
            {
              id: 'tc_inc_01',
              title: 'Transient Upstream Policy API Latency Spike',
              severity: 'minor',
              impact_summary: 'Pre-signer latency increased by 120ms during peak batch evaluation',
              response_recommendation: 'Activate ActionGateway read-side cache fallback',
              status: 'active'
            }
          ],
          escalations: [
            {
              id: 'tc_esc_01',
              trigger_reason: 'Capacity headroom reached 15% warning threshold',
              urgency: 'medium',
              decision_owner_unit_id: 'unit_transformation_steering_board',
              status: 'active'
            }
          ],
          weeklyReviews: [
            {
              id: 'wrev_01',
              portfolio_summary: 'Transformation Portfolio executing on schedule across Wave 1.',
              waves_summary: 'Wave 1 (Foundation) at 92% readiness exit criteria.',
              signals_summary: '2 signals ingested, correlated into 1 medium-severity situation.',
              decisions_summary: 'Change Request cr_sequence_adjust_01 pending leadership review.'
            }
          ],
          learnings: [
            {
              id: 'learn_01',
              signal_summary: 'Engineering capacity buffer compression during pre-signer validation.',
              lesson_text: 'Pre-signing zero-trust policies eliminates downstream engineering bottleneck during wave acceleration.'
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

  const handleApproveChangeRequest = async (requestId: string) => {
    try {
      const res = await fetch(`/api/v1/transformation-control/change-requests/${requestId}/approve`, {
        method: 'POST'
      });
      if (res.ok) {
        const json = await res.json();
        setApprovalMsg(json.message);
        fetchData();
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleQuery = async () => {
    if (!queryText.trim()) return;
    setQueryLoading(true);
    try {
      const res = await fetch(`/api/v1/transformation-control/query?query=${encodeURIComponent(queryText)}`, {
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
            <span className="p-2 bg-indigo-600/20 text-indigo-400 rounded-lg text-lg">🗼</span>
            Enterprise Transformation Control Tower + Continuous Change Orchestration 2.0
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Live Strategy → Sequence → Waves → Signals → Drift → Root Cause → Governed Change Requests → Execution Governance.
          </p>
        </div>
        <div className="flex gap-2">
          <span className="px-3 py-1 bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 rounded-full text-xs font-semibold">
            Control Tower Active
          </span>
          <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full text-xs font-semibold">
            Human Governed Gates
          </span>
        </div>
      </div>

      {/* Telemetry Header */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Control Tower Status</div>
          <div className="text-xl font-bold text-emerald-400 mt-1 uppercase">{data?.controlTowerStatus || 'HEALTHY'}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Live Telemetry Signals</div>
          <div className="text-2xl font-bold text-blue-400 mt-1">{data?.signalsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Correlated Situations</div>
          <div className="text-2xl font-bold text-amber-400 mt-1">{data?.situationsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Wave Readiness</div>
          <div className="text-2xl font-bold text-teal-400 mt-1">{data?.overallWaveReadinessPct || 92}%</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Change Requests</div>
          <div className="text-2xl font-bold text-indigo-400 mt-1">{data?.proposedChangeRequestsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Active Incidents</div>
          <div className="text-2xl font-bold text-rose-400 mt-1">{data?.activeIncidentsCount || 0}</div>
        </div>
      </div>

      {/* Approval Banner */}
      {approvalMsg && (
        <div className="p-4 bg-emerald-950/50 border border-emerald-800/60 rounded-xl text-emerald-300 text-sm flex justify-between items-center">
          <span>✅ {approvalMsg}</span>
          <button onClick={() => setApprovalMsg(null)} className="text-xs text-slate-400 hover:text-white">Dismiss</button>
        </div>
      )}

      {/* Subsystem Tabs */}
      <div className="flex border-b border-slate-800 gap-2 text-sm overflow-x-auto pb-1">
        {[
          { id: 'overview', label: 'Control Overview' },
          { id: 'live_state', label: 'Live State & Signals' },
          { id: 'situations', label: 'Situations & Root Cause' },
          { id: 'wave_readiness', label: 'Wave Readiness & Exit Gates' },
          { id: 'change_requests', label: 'Change Requests & Impact' },
          { id: 'incidents', label: 'Incidents & Escalations' },
          { id: 'reviews', label: 'Reviews & Control Learning' },
          { id: 'nl_query', label: 'Natural Language Query' }
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
        <div className="p-8 text-center text-slate-500">Loading Transformation Control Tower telemetry...</div>
      ) : (
        <div className="space-y-6">
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-indigo-400 flex items-center gap-2">
                  <span>🗼</span> Primary Control Tower
                </h2>
                {data?.towers?.[0] && (
                  <div className="space-y-3 text-sm">
                    <div className="font-bold text-slate-100">{data.towers[0].name}</div>
                    <div className="p-3 bg-slate-950 rounded border border-indigo-800/40 text-indigo-300 text-xs">
                      Portfolio ID: {data.towers[0].portfolio_id} | Owner: {data.towers[0].owner}
                    </div>
                    <div className="flex justify-between items-center text-xs text-slate-400">
                      <span>Status: <strong className="text-emerald-400 uppercase">{data.towers[0].status}</strong></span>
                      <span>Evaluated: {new Date(data.towers[0].last_evaluated_at).toLocaleTimeString()}</span>
                    </div>
                  </div>
                )}
              </div>

              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-blue-400 flex items-center gap-2">
                  <span>📈</span> Live Transformation Drift & Forecast
                </h2>
                {data?.liveStates?.[0] && (
                  <div className="space-y-3 text-sm">
                    <div className="p-3 bg-slate-950 rounded border border-blue-800/40 text-blue-300 text-xs space-y-1">
                      <div><strong>Planned vs Actual:</strong> {data.liveStates[0].actual_state_json?.schedule_variance} schedule variance</div>
                      <div><strong>Completion Forecast:</strong> {data.liveStates[0].forecast_state_json?.completion_confidence} confidence ({data.liveStates[0].forecast_state_json?.expected_completion})</div>
                    </div>
                    <div className="text-xs text-slate-400">{data.liveStates[0].last_evaluation}</div>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'live_state' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Live Telemetry Signals</h2>
              {data?.signals?.map((sig: any) => (
                <div key={sig.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-blue-300">Signal Type: {sig.signal_type}</span>
                    <span className="text-xs px-2 py-0.5 bg-amber-500/20 text-amber-300 rounded font-bold">Severity: {sig.severity}</span>
                  </div>
                  <div className="text-xs text-slate-400">Evidence: {JSON.stringify(sig.evidence_json)}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'situations' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Correlated Situations & Evidence-Backed Root Cause</h2>
              {data?.situations?.map((sit: any) => (
                <div key={sit.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-amber-300">Situation ID: {sit.id}</span>
                    <span className="text-xs px-2 py-0.5 bg-rose-500/20 text-rose-300 rounded font-bold">Severity: {sit.severity}</span>
                  </div>
                  <p className="text-xs text-slate-300">{sit.evidence_json?.correlated_telemetry}</p>

                  {data?.rootCauses?.map((rc: any) => (
                    <div key={rc.id} className="p-3 bg-slate-900 rounded border-l-4 border-l-teal-500 text-xs space-y-1">
                      <div className="flex justify-between text-teal-300 font-semibold">
                        <span>Root Cause Category: {rc.category}</span>
                        <span>Evidence Label: {rc.evidence_label}</span>
                      </div>
                      <p className="text-slate-300">{rc.description}</p>
                    </div>
                  ))}
                </div>
              ))}
            </div>
          )}

          {activeTab === 'wave_readiness' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Wave Readiness & Decision Gate Validation</h2>
              {data?.waveReadinesses?.map((wr: any) => (
                <div key={wr.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-teal-300">Wave ID: {wr.wave_id}</span>
                    <span className="text-xs px-2.5 py-0.5 bg-emerald-500/20 text-emerald-300 rounded font-bold">Status: {wr.status}</span>
                  </div>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
                    <div className="p-2 bg-slate-900 rounded text-emerald-300">Capability: {(wr.capability_readiness * 100).toFixed(0)}%</div>
                    <div className="p-2 bg-slate-900 rounded text-blue-300">Technology: {(wr.technology_readiness * 100).toFixed(0)}%</div>
                    <div className="p-2 bg-slate-900 rounded text-indigo-300">Capacity: {(wr.capacity_readiness * 100).toFixed(0)}%</div>
                    <div className="p-2 bg-slate-900 rounded text-purple-300">Adoption: {(wr.adoption_readiness * 100).toFixed(0)}%</div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'change_requests' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Governed Transformation Change Requests</h2>
              {data?.changeRequests?.map((cr: any) => (
                <div key={cr.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-indigo-300">Change Type: {cr.request_type}</span>
                    <span className={`text-xs px-2 py-0.5 rounded font-bold ${
                      cr.status === 'approved' ? 'bg-emerald-500/20 text-emerald-300' : 'bg-indigo-500/20 text-indigo-300'
                    }`}>
                      {cr.status}
                    </span>
                  </div>
                  <p className="text-xs text-slate-300">{cr.proposed_change_desc}</p>
                  <div className="p-2 bg-slate-900 rounded text-xs text-slate-400">
                    Impact Analysis: Time saved {cr.impact_analysis_json?.time_saved}, Risk delta {cr.impact_analysis_json?.risk_delta}
                  </div>

                  {cr.status === 'proposed' && (
                    <button
                      onClick={() => handleApproveChangeRequest(cr.id)}
                      className="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold rounded transition-colors"
                    >
                      Authorize Transformation Change Request
                    </button>
                  )}
                </div>
              ))}
            </div>
          )}

          {activeTab === 'incidents' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Active Transformation Incidents & Escalations</h2>
              {data?.incidents?.map((inc: any) => (
                <div key={inc.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-rose-500">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-rose-300">{inc.title}</span>
                    <span className="text-xs px-2 py-0.5 bg-rose-500/20 text-rose-300 rounded font-bold">Severity: {inc.severity}</span>
                  </div>
                  <p className="text-xs text-slate-300">{inc.impact_summary}</p>
                  <div className="text-xs text-emerald-400">Recommendation: {inc.response_recommendation}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'reviews' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Executive Reviews & Control Learning</h2>
              {data?.weeklyReviews?.map((wrev: any) => (
                <div key={wrev.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="font-bold text-indigo-300">Weekly Review Summary</div>
                  <p className="text-xs text-slate-300">{wrev.portfolio_summary}</p>
                  <div className="text-xs text-slate-400">Waves: {wrev.waves_summary}</div>
                </div>
              ))}

              {data?.learnings?.map((lrn: any) => (
                <div key={lrn.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-emerald-500">
                  <div className="font-bold text-emerald-300">Control Learning Lesson</div>
                  <p className="text-xs text-slate-300">{lrn.lesson_text}</p>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'nl_query' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Natural Language Control Tower Query Interface</h2>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={queryText}
                  onChange={(e) => setQueryText(e.target.value)}
                  placeholder="Ask a transformation control query..."
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
                        <div className="font-semibold text-slate-200">{res.control_tower}</div>
                        <div className="text-blue-300">Live State Drift: {res.live_state_drift}</div>
                        <div className="text-amber-300">Active Situation: {res.active_situation}</div>
                        <div className="text-teal-300">Root Cause Assessment: {res.root_cause_assessment}</div>
                        <div className="text-emerald-400">Wave Readiness: {res.wave_readiness}</div>
                        <div className="text-indigo-300">Pending Decision: {res.pending_decision}</div>
                        <div className="text-purple-300">Recommendation: {res.recommendation}</div>
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
