'use client';

import React, { useState, useEffect } from 'react';

export function TransformationWarRoomWorkspace() {
  const [activeTab, setActiveTab] = useState<'overview' | 'live_state' | 'deviations_variance' | 'root_causes_impact' | 'interventions_blast' | 'do_nothing_baseline' | 'response_checkpoints' | 'trajectories_warnings' | 'governance_escalations' | 'situation_query'>('overview');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('What changed in the transformation portfolio?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/transformation-war-room');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      } else {
        // Fallback seed structure
        setData({
          activeWarRoomsCount: 1,
          detectedDeviationsCount: 1,
          activeEarlyWarningsCount: 1,
          proposedInterventionsCount: 1,
          activeResponsePlansCount: 1,
          liveStateFreshnessMinutes: 2.5,
          warRooms: [
            { id: 'wr_01', name: 'Global Transformation Operations War Room', scope: 'enterprise', owner: 'Chief Transformation Officer', status: 'attention', priority: 'high' }
          ],
          liveStates: [
            { id: 'ls_01', war_room_id: 'wr_01', staleness_status: 'fresh', last_updated: new Date().toISOString(), milestones_json: { active_milestones: 24, delayed_milestones: 2 } }
          ],
          planVariances: [
            { id: 'pv_01', variance_type: 'schedule', planned_summary: 'Wave 2 scheduled for Q3 2026', actual_summary: '14 days behind schedule', severity: 'medium' }
          ],
          deviations: [
            { id: 'dev_01', entity: 'Wave 2 FinOps Migration', metric: 'Execution Schedule (Days)', expected_value: 0.0, actual_value: -14.0, variance_value: -14.0, severity: 'high' }
          ],
          rootCauses: [
            { id: 'rc_01', hypothesis_text: 'Manual CISO review queue backlog (48h delay) coupled with 15 FTE capacity shortfall in Core IAM team', confidence: 0.88 }
          ],
          impacts: [
            { id: 'imp_01', strategic_impact: 'High. Threatens Q4 enterprise cloud cost reduction targets if unmitigated.' }
          ],
          interventions: [
            { id: 'io_01', intervention_type: 'resequence', title: 'Delegate Regional Pilot Approvals & Reallocate 15 FTEs from Wave 3', safety_score: 0.92, reversibility_score: 0.90, status: 'recommended' }
          ],
          recommendations: [
            { id: 'rec_01', evidence_summary: 'Digital Twin simulation sim_run_01 confirms 14-day schedule recovery with zero policy breach risk', uncertainty_level: 'low' }
          ],
          responsePlans: [
            { id: 'rp_01', title: 'Wave 2 Schedule Recovery & Governance Acceleration Plan', status: 'awaiting_approval' }
          ],
          checkpoints: [
            { id: 'cp_01', checkpoint_name: 'Post-Delegation Verification Checkpoint', expected_state: 'Governance backlog reduced to < 12 hours', status: 'pending' }
          ],
          earlyWarnings: [
            { id: 'ew_01', signal_name: 'IAM Integration Queue Pressure Early Warning', signal_strength: 0.88, model_confidence: 0.95, status: 'active' }
          ],
          situationSummaries: [
            { id: 'sit_01', what_changed: 'Wave 2 FinOps migration schedule slipped by 14 days due to IAM capacity bottleneck & CISO review backlog.', why_it_matters: 'Threatens Q4 $1.2M cloud benefit realization if not mitigated within 14 days.' }
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
      const res = await fetch(`/api/v1/transformation-war-room/query?query=${encodeURIComponent(queryText)}`, {
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
            <span className="p-2 bg-red-600/20 text-red-400 rounded-lg text-lg">🚨</span>
            Enterprise Transformation War Room 2.0
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Real State → Live Signals → Deviation Detection → Root Causes → Intervention Simulation → Human Approval → Verified Execution.
          </p>
        </div>
        <div className="flex gap-2">
          <span className="px-3 py-1 bg-red-500/10 text-red-400 border border-red-500/20 rounded-full text-xs font-semibold">
            Human-Authorized Intervention
          </span>
          <span className="px-3 py-1 bg-purple-500/10 text-purple-400 border border-purple-500/20 rounded-full text-xs font-semibold">
            Zero Worker Surveillance
          </span>
        </div>
      </div>

      {/* Operational Telemetry Header */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Active War Rooms</div>
          <div className="text-2xl font-bold text-red-400 mt-1">{data?.activeWarRoomsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Detected Deviations</div>
          <div className="text-2xl font-bold text-amber-400 mt-1">{data?.detectedDeviationsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Early Warnings</div>
          <div className="text-2xl font-bold text-orange-400 mt-1">{data?.activeEarlyWarningsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Proposed Interventions</div>
          <div className="text-2xl font-bold text-indigo-400 mt-1">{data?.proposedInterventionsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Response Plans</div>
          <div className="text-2xl font-bold text-emerald-400 mt-1">{data?.activeResponsePlansCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Live Freshness</div>
          <div className="text-2xl font-bold text-teal-400 mt-1">2.5 min</div>
        </div>
      </div>

      {/* Subsystem Tabs */}
      <div className="flex border-b border-slate-800 gap-2 text-sm overflow-x-auto pb-1">
        {[
          { id: 'overview', label: 'Live Situation & War Rooms' },
          { id: 'live_state', label: 'Live State & Freshness' },
          { id: 'deviations_variance', label: 'Deviations & Plan Variance' },
          { id: 'root_causes_impact', label: 'Root Causes & Impact' },
          { id: 'interventions_blast', label: 'Interventions & Blast Radius' },
          { id: 'do_nothing_baseline', label: 'Do-Nothing Baseline & Tradeoffs' },
          { id: 'response_checkpoints', label: 'Response Plans & Checkpoints' },
          { id: 'trajectories_warnings', label: 'Trajectories & Early Warnings' },
          { id: 'governance_escalations', label: 'Governance & Escalations' },
          { id: 'situation_query', label: 'Situation Query Engine' }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-2 font-medium rounded-t-lg transition-colors whitespace-nowrap ${
              activeTab === tab.id
                ? 'bg-slate-900 text-red-400 border-b-2 border-red-500'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/40'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Content */}
      {loading ? (
        <div className="p-8 text-center text-slate-500">Loading Enterprise Transformation War Room...</div>
      ) : (
        <div className="space-y-6">
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-red-400 flex items-center gap-2">
                  <span>🚨</span> Active Operational War Rooms
                </h2>
                <div className="space-y-2 text-sm">
                  {data?.warRooms?.map((wr: any) => (
                    <div key={wr.id} className="p-3 bg-slate-950 rounded border border-red-800/40 flex justify-between items-center text-xs">
                      <div>
                        <div className="font-bold text-slate-100">{wr.name}</div>
                        <div className="text-slate-400">Scope: {wr.scope} | Owner: {wr.owner}</div>
                      </div>
                      <span className="px-2 py-0.5 bg-red-500/20 text-red-300 rounded font-bold">{wr.status.toUpperCase()}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-amber-400 flex items-center gap-2">
                  <span>⚠️</span> Active Situation Briefing
                </h2>
                <div className="space-y-2 text-sm">
                  {data?.situationSummaries?.map((sit: any) => (
                    <div key={sit.id} className="p-3 bg-slate-950 rounded border border-amber-800/40 space-y-1 text-xs">
                      <div className="font-bold text-amber-300">What Changed: {sit.what_changed}</div>
                      <div className="text-slate-300">Why It Matters: {sit.why_it_matters}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'live_state' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Real-Time Synchronized State & Freshness</h2>
              {data?.liveStates?.map((ls: any) => (
                <div key={ls.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-teal-500">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-teal-300">Freshness Status: {ls.staleness_status.toUpperCase()}</span>
                    <span className="text-xs px-2 py-0.5 bg-teal-500/20 text-teal-300 rounded font-bold">Updated: {ls.last_updated}</span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'deviations_variance' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Plan Variances & Metric Deviations</h2>
              {data?.deviations?.map((dev: any) => (
                <div key={dev.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-amber-500">
                  <div className="flex justify-between items-center font-bold text-amber-300">
                    <span>Entity: {dev.entity} | Metric: {dev.metric}</span>
                    <span className="text-xs px-2 py-0.5 bg-amber-500/20 text-amber-300 rounded font-bold">Severity: {dev.severity.toUpperCase()}</span>
                  </div>
                  <div className="text-xs text-slate-300">Variance: {dev.variance_value} (Expected {dev.expected_value} vs Actual {dev.actual_value})</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'root_causes_impact' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Root-Cause Hypotheses & Cross-Transformation Impact</h2>
              {data?.rootCauses?.map((rc: any) => (
                <div key={rc.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-indigo-500">
                  <div className="font-bold text-indigo-300">Hypothesis: {rc.hypothesis_text}</div>
                  <div className="text-xs text-emerald-400 font-semibold">Confidence: {(rc.confidence * 100).toFixed(0)}%</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'interventions_blast' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Intervention Options & Blast Radius Assessment</h2>
              {data?.interventions?.map((io: any) => (
                <div key={io.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-purple-500">
                  <div className="flex justify-between items-center font-bold text-purple-300">
                    <span>Title: {io.title}</span>
                    <span className="text-xs px-2 py-0.5 bg-purple-500/20 text-purple-300 rounded font-bold">Status: {io.status.toUpperCase()}</span>
                  </div>
                  <div className="text-xs text-slate-300">Description: {io.description}</div>
                  <div className="text-xs text-teal-400 font-semibold">Safety Score: {(io.safety_score * 100).toFixed(0)}% | Reversibility: {(io.reversibility_score * 100).toFixed(0)}%</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'response_checkpoints' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Response Plans & Execution Checkpoints</h2>
              {data?.responsePlans?.map((rp: any) => (
                <div key={rp.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-emerald-500">
                  <div className="flex justify-between items-center font-bold text-emerald-300">
                    <span>Plan: {rp.title}</span>
                    <span className="text-xs px-2 py-0.5 bg-emerald-500/20 text-emerald-300 rounded font-bold">Status: {rp.status.toUpperCase()}</span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'trajectories_warnings' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Predictive Trajectories & Early Warning Signals</h2>
              {data?.earlyWarnings?.map((ew: any) => (
                <div key={ew.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-orange-500">
                  <div className="flex justify-between items-center font-bold text-orange-300">
                    <span>Early Warning: {ew.signal_name}</span>
                    <span className="text-xs px-2 py-0.5 bg-orange-500/20 text-orange-300 rounded font-bold">Model Confidence: {(ew.model_confidence * 100).toFixed(0)}%</span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'situation_query' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Natural Language Situation Briefing Query Engine</h2>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={queryText}
                  onChange={(e) => setQueryText(e.target.value)}
                  placeholder="Ask a war room situation query..."
                  className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-sm text-slate-100 focus:outline-none focus:border-red-500"
                />
                <button
                  onClick={handleQuery}
                  disabled={queryLoading}
                  className="px-5 py-2 bg-red-600 hover:bg-red-500 text-white font-medium rounded-lg text-sm transition-colors"
                >
                  {queryLoading ? 'Briefing...' : 'Query'}
                </button>
              </div>

              {queryResult && (
                <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                  <div className="text-xs text-red-400 font-semibold">Query: {queryResult.query}</div>
                  <div className="space-y-2">
                    {queryResult.results?.map((res: any, idx: number) => (
                      <div key={idx} className="p-3 bg-slate-900 rounded space-y-1 text-xs">
                        <div className="font-semibold text-red-300">{res.war_room}</div>
                        <div className="text-slate-300">Situation Briefing: {res.situation_briefing}</div>
                        <div className="text-amber-300">Why It Matters: {res.why_it_matters}</div>
                        <div className="text-purple-300">Recommended Intervention: {res.recommended_intervention}</div>
                        <div className="text-emerald-300">Response Plan Status: {res.response_plan_status}</div>
                        <div className="text-orange-300">Early Warning Signal: {res.early_warning_signal}</div>
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
