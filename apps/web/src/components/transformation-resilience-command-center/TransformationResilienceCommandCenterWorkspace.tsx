'use client';

import React, { useState, useEffect } from 'react';

export function TransformationResilienceCommandCenterWorkspace() {
  const [activeTab, setActiveTab] = useState<'overview' | 'executive_state' | 'priorities' | 'situations' | 'exposure_map' | 'evidence' | 'unapplied_lessons' | 'decision_packets' | 'timeline' | 'command_center_query'>('overview');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('What is the current portfolio resilience state and top priority item?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/transformation-resilience-command-center');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      } else {
        // Fallback seed data
        setData({
          commandCentersCount: 1,
          executiveDimensionsCount: 7,
          priorityItemsCount: 1,
          situationsCount: 1,
          snapshotsCount: 1,
          exposureMapsCount: 1,
          unappliedLessonsCount: 1,
          decisionPacketsCount: 1,
          commandCenters: [
            { id: 'cc_res_01', name: 'Global Enterprise Transformation Resilience Command Center 2.0', scope: 'enterprise', owner: 'Principal Enterprise Resilience Systems Architect', status: 'healthy' }
          ],
          executiveStates: [
            { id: 'exec_st_robustness', dimension: 'robustness', state: 'stable', trend: 'improving', confidence: 0.94, evidence_count: 14 },
            { id: 'exec_st_redundancy', dimension: 'redundancy', state: 'attention', trend: 'stable', confidence: 0.91, evidence_count: 10 },
            { id: 'exec_st_recoverability', dimension: 'recoverability', state: 'stable', trend: 'improving', confidence: 0.95, evidence_count: 16 },
            { id: 'exec_st_adaptability', dimension: 'adaptability', state: 'stable', trend: 'improving', confidence: 0.92, evidence_count: 11 },
            { id: 'exec_st_optionality', dimension: 'optionality', state: 'stable', trend: 'improving', confidence: 0.93, evidence_count: 12 },
            { id: 'exec_st_observability', dimension: 'observability', state: 'degraded', trend: 'deteriorating', confidence: 0.96, evidence_count: 18 },
            { id: 'exec_st_governability', dimension: 'governability', state: 'stable', trend: 'improving', confidence: 0.94, evidence_count: 15 }
          ],
          priorities: [
            { id: 'pitem_01', priority: 'critical', title: 'Shared IAM OAuth Gateway Bottleneck & Vendor SLA Drift', impact_score: 0.94, urgency_score: 0.91, scope: 'enterprise_waves_2_to_4', decision_deadline: '2026-Q3' }
          ],
          situations: [
            { id: 'sit_01', summary: 'Primary OAuth Auth Gateway SLA drifted from 99.99% to 99.91% while Senior IAM Engineers experience capacity contention.', recommended_review: 'Initiate Executive Decision Review for pinv_01 Active-Active deployment.' }
          ],
          exposureMaps: [
            { id: 'expmap_01', transformation_id: 'wave_02_finops', dimension: 'observability', severity: 'medium', confidence: 0.95 }
          ],
          evidenceSummary: {
            source_diversity_score: 0.92,
            freshness_score: 0.98,
            quality_score: 0.95,
            has_conflicts: true,
            conflicts_json: [
              { source_a: 'EventMesh.IdentityGateway', source_b: 'KPI.OAuthMonitor', conflict_description: 'EventMesh reports 142.5ms latency; KPI Monitor reports 118.0ms due to sampling windows.' }
            ],
            confidence: 0.94
          },
          unappliedLessons: [
            { id: 'uless_01', lesson_title: 'Multi-Cloud Fallback Route Delay Lesson (Sprint 70 Crisis Post-Mortem)', reason_not_applied: 'Pending Executive Board funding approval for pinv_01.', recommended_review: 'Accelerate pinv_01 funding review to eliminate single vendor lock-in.' }
          ],
          decisionPackets: [
            { id: 'dp_01', title: 'Cross-Portfolio Active-Active IAM Gateway Funding & Deployment Packet', recommendation: 'Approve pinv_01 Active-Active IAM Gateway funding of $350k.', required_approval: 'PolicyEngine + Enterprise Executive Board' }
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
      const res = await fetch(`/api/v1/transformation-resilience-command-center/query?query=${encodeURIComponent(queryText)}`, {
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
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-violet-400 via-purple-400 to-pink-400">
              Transformation Resilience Command Center 2.0
            </h1>
            <span className="px-3 py-1 text-xs font-semibold rounded-full bg-violet-500/10 text-violet-400 border border-violet-500/20">
              Continuous Resilience Decision Intelligence
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Executive operating layer unifying continuous sensing, portfolio exposure, systemic risk, evidence quality, and decision packet generation.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={fetchData}
            className="px-4 py-2 text-xs font-medium rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition"
          >
            Refresh Executive Brief
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Command Center</p>
          <p className="text-xl font-bold text-violet-400 mt-1">{data?.commandCentersCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Resilience Dimensions</p>
          <p className="text-xl font-bold text-pink-400 mt-1">7 / 7</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Priority Queue</p>
          <p className="text-xl font-bold text-rose-400 mt-1">{data?.priorityItemsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Active Situations</p>
          <p className="text-xl font-bold text-amber-400 mt-1">{data?.situationsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Exposure Maps</p>
          <p className="text-xl font-bold text-cyan-400 mt-1">{data?.exposureMapsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Evidence Quality</p>
          <p className="text-xl font-bold text-emerald-400 mt-1">{( (data?.evidenceSummary?.quality_score ?? 0.95) * 100 ).toFixed(0)}%</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Unapplied Lessons</p>
          <p className="text-xl font-bold text-indigo-400 mt-1">{data?.unappliedLessonsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Decision Packets</p>
          <p className="text-xl font-bold text-teal-400 mt-1">{data?.decisionPacketsCount ?? 1}</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 overflow-x-auto space-x-2 scrollbar-none">
        {[
          { id: 'overview', label: 'Executive Command Layer' },
          { id: 'executive_state', label: '7-Dimension Resilience State' },
          { id: 'priorities', label: 'Executive Priority Queue' },
          { id: 'situations', label: 'Situational Intelligence' },
          { id: 'exposure_map', label: 'Portfolio Exposure Heatmap' },
          { id: 'evidence', label: 'Evidence Quality & Conflicts' },
          { id: 'unapplied_lessons', label: 'Unapplied Lessons' },
          { id: 'decision_packets', label: 'Executive Decision Packets' },
          { id: 'timeline', label: 'Unified Resilience Timeline' },
          { id: 'command_center_query', label: 'Command Center Query' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-2.5 text-xs font-semibold whitespace-nowrap border-b-2 transition ${
              activeTab === tab.id
                ? 'border-violet-400 text-violet-400 bg-violet-500/5'
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
            Aggregating executive resilience telemetry and building situation maps...
          </div>
        ) : (
          <>
            {activeTab === 'overview' && (
              <div className="space-y-6">
                <h3 className="text-base font-semibold text-slate-200">Executive Operating Command Center</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {data?.commandCenters?.map((cc: any) => (
                    <div key={cc.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="font-semibold text-violet-400">{cc.name}</span>
                        <span className="text-xs px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">{cc.status}</span>
                      </div>
                      <p className="text-xs text-slate-400">Scope: {cc.scope} | Owner: {cc.owner}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'executive_state' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">7-Dimension Resilience Executive State</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-7 gap-3">
                  {data?.executiveStates?.map((es: any) => (
                    <div key={es.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2 text-center">
                      <span className="text-xs font-semibold text-slate-300 capitalize">{es.dimension}</span>
                      <div className="text-sm font-bold text-violet-400">{es.state}</div>
                      <p className="text-[10px] text-slate-400">Trend: {es.trend} | Confidence: {(es.confidence * 100).toFixed(0)}%</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'priorities' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Executive Priority Queue</h3>
                {data?.priorities?.map((p: any) => (
                  <div key={p.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 flex justify-between items-center">
                    <div>
                      <span className="font-medium text-rose-400">{p.title}</span>
                      <p className="text-xs text-slate-400 mt-1">Impact: {(p.impact_score * 100).toFixed(0)}% | Urgency: {(p.urgency_score * 100).toFixed(0)}% | Deadline: {p.decision_deadline}</p>
                    </div>
                    <span className="text-xs px-3 py-1 rounded bg-rose-500/10 text-rose-400 border border-rose-500/20 font-semibold">{p.priority}</span>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'situations' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Executive Situational Intelligence</h3>
                {data?.situations?.map((s: any) => (
                  <div key={s.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <p className="text-xs text-slate-200 font-medium">{s.summary}</p>
                    <p className="text-xs text-violet-400">Recommended Review: {s.recommended_review}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'exposure_map' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Portfolio Exposure Heatmap</h3>
                {data?.exposureMaps?.map((exp: any) => (
                  <div key={exp.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 flex justify-between items-center">
                    <div>
                      <span className="text-sm font-medium text-slate-200">Transformation: {exp.transformation_id}</span>
                      <p className="text-xs text-slate-400 mt-1">Dimension: {exp.dimension} | Confidence: {(exp.confidence * 100).toFixed(0)}%</p>
                    </div>
                    <span className="text-xs px-2.5 py-1 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20 font-semibold">{exp.severity}</span>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'evidence' && (
              <div className="space-y-6">
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-semibold text-emerald-400">Evidence Quality Assessment</span>
                    <span className="text-xs text-slate-400">Source Diversity: {(data?.evidenceSummary?.source_diversity_score * 100).toFixed(0)}%</span>
                  </div>
                  <p className="text-xs text-slate-400">Freshness: {(data?.evidenceSummary?.freshness_score * 100).toFixed(0)}% | Quality: {(data?.evidenceSummary?.quality_score * 100).toFixed(0)}%</p>
                </div>

                {data?.evidenceSummary?.has_conflicts && (
                  <div className="space-y-3">
                    <h4 className="text-xs font-semibold text-rose-400">Surfaced Signal Conflicts (Contradictory Evidence)</h4>
                    {data?.evidenceSummary?.conflicts_json?.map((c: any, idx: number) => (
                      <div key={idx} className="p-4 rounded-xl bg-slate-950/60 border border-rose-500/30 space-y-1">
                        <span className="text-xs font-medium text-rose-400">Conflict Metric: {c.metric}</span>
                        <p className="text-xs text-slate-300">{c.conflict_description}</p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {activeTab === 'unapplied_lessons' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Unapplied Resilience Lessons</h3>
                {data?.unappliedLessons?.map((ul: any) => (
                  <div key={ul.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <span className="text-sm font-medium text-indigo-400">{ul.lesson_title}</span>
                    <p className="text-xs text-slate-300">Reason Not Applied: {ul.reason_not_applied}</p>
                    <p className="text-xs text-violet-400">Recommended Review: {ul.recommended_review}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'decision_packets' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Generated Executive Decision Packets</h3>
                {data?.decisionPackets?.map((dp: any) => (
                  <div key={dp.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="font-semibold text-teal-400">{dp.title}</span>
                      <span className="text-xs px-2 py-0.5 rounded bg-teal-500/10 text-teal-400 border border-teal-500/20">{dp.required_approval}</span>
                    </div>
                    <p className="text-xs text-slate-300">Recommendation: {dp.recommendation}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'timeline' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Unified Executive Resilience Timeline</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-3">
                  <div className="border-l-2 border-violet-500/40 pl-4 space-y-4 text-xs text-slate-300">
                    <div>
                      <span className="text-violet-400 font-semibold">10:00 AM UTC</span>
                      <p>Signal Ingested: OAuth P99 Latency reached 142.5ms on Identity Gateway.</p>
                    </div>
                    <div>
                      <span className="text-amber-400 font-semibold">10:15 AM UTC</span>
                      <p>Drift Flagged: Persistent drift flagged on Shared Identity Gateway (+8.4% deviation).</p>
                    </div>
                    <div>
                      <span className="text-rose-400 font-semibold">10:30 AM UTC</span>
                      <p>Priority Item Created: Shared IAM OAuth Gateway Bottleneck & Vendor SLA Drift (Critical).</p>
                    </div>
                    <div>
                      <span className="text-teal-400 font-semibold">11:00 AM UTC</span>
                      <p>Decision Packet Generated: dp_01 created for pinv_01 Active-Active IAM Gateway funding review ($350k).</p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'command_center_query' && (
              <div className="space-y-6">
                <h3 className="text-base font-semibold text-slate-200">Natural Language Executive Command Query</h3>
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={queryText}
                    onChange={(e) => setQueryText(e.target.value)}
                    placeholder="Ask an executive resilience command center question..."
                    className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-violet-500/50"
                  />
                  <button
                    onClick={handleQuery}
                    disabled={queryLoading}
                    className="px-5 py-2.5 bg-violet-500 hover:bg-violet-600 disabled:opacity-50 text-slate-950 text-xs font-semibold rounded-xl transition"
                  >
                    {queryLoading ? 'Processing...' : 'Run Query'}
                  </button>
                </div>

                {queryResult && (
                  <div className="p-5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-semibold text-violet-400">Command Center Query Result</span>
                      <span className="text-xs text-slate-400">Confidence: {queryResult.confidencePct}%</span>
                    </div>
                    {queryResult.evidenceJson?.error ? (
                      <div className="text-xs text-rose-400 font-semibold">{queryResult.evidenceJson.error}</div>
                    ) : (
                      <div className="space-y-2 text-xs text-slate-300">
                        {queryResult.results?.map((r: any, idx: number) => (
                          <div key={idx} className="p-3 bg-slate-900 rounded-lg space-y-1">
                            <p><strong className="text-violet-400">Command Center:</strong> {r.command_center}</p>
                            <p><strong className="text-pink-400">Executive Resilience State:</strong> {r.executive_resilience_state}</p>
                            <p><strong className="text-rose-400">Top Priority Item:</strong> {r.top_priority_item}</p>
                            <p><strong className="text-amber-400">Situational Summary:</strong> {r.situation_summary}</p>
                            <p><strong className="text-emerald-400">Evidence Quality & Conflicts:</strong> {r.evidence_summary}</p>
                            <p><strong className="text-indigo-400">Unapplied Lesson:</strong> {r.unapplied_lesson}</p>
                            <p><strong className="text-teal-400">Recommended Decision Packet:</strong> {r.recommended_decision_packet}</p>
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
