'use client';

import React, { useState, useEffect } from 'react';

export function TransformationResilienceDecisionKnowledgeWorkspace() {
  const [activeTab, setActiveTab] = useState<
    'overview' | 'lessons' | 'patterns' | 'precedents' | 'assumptions' | 'scenario' | 'recovery' | 'investment' | 'conflicts' | 'validation' | 'applicability' | 'reuse' | 'gaps' | 'decay' | 'reviews' | 'timeline' | 'query'
  >('overview');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('What have we learned about this dependency and show relevant precedents?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/transformation-resilience-decision-knowledge');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      } else {
        // Fallback seed data
        setData({
          domainsCount: 1,
          knowledgeObjectsCount: 3,
          validatedObjectsCount: 2,
          supportedObjectsCount: 0,
          contestedObjectsCount: 1,
          invalidatedObjectsCount: 0,
          conflictsCount: 1,
          packsCount: 1,
          gapsCount: 1,
          domains: [
            { id: 'kdom_01', name: 'Global Enterprise Governed Decision Knowledge Intelligence 2.0', owner: 'Principal Enterprise Decision Knowledge Architect', status: 'active', version: 'v2.0' }
          ],
          knowledgeObjects: [
            { id: 'kobj_less_01', type: 'lesson', statement: 'Secondary Cloud Region latency assumptions must include a +15ms vendor SLA buffer.', confidence: 0.95, applicability_level: 'high', limitations: 'Requires multi-region token cache pre-warming and dedicated 10Gbps interconnect.', status: 'validated', version: 1 },
            { id: 'kobj_less_02', type: 'lesson', statement: 'Token cache replication should rely on eventual consistency to save inter-region bandwidth.', confidence: 0.75, applicability_level: 'medium', limitations: 'Not applicable to real-time high-concurrency OAuth gateways.', status: 'contested', version: 1 },
            { id: 'kobj_prec_01', type: 'precedent', statement: '2025 Active-Active Identity Failover Architecture Precedent', confidence: 0.92, applicability_level: 'high', limitations: 'Context mismatch for legacy regional auth stacks.', status: 'validated', version: 1 }
          ],
          validations: [
            { id: 'val_01', supporting_cases_count: 6, contradicting_cases_count: 0, evidence_quality: 0.96, reproducibility: 0.94 }
          ],
          contexts: [
            { id: 'ctx_01', transformation_type: 'Cloud Infrastructure Resilience', dependency_profile: 'OAuth / Multi-Region Identity Cluster', time_horizon: '2026-2028' }
          ],
          applicabilities: [
            { id: 'app_01', target_decision_context_id: 'dec_wave_04_hr', level: 'high', applicability_score: 0.94, explanation: 'Wave 4 HR Cloud shares identical multi-region OAuth token dependency profile.' }
          ],
          conflicts: [
            { id: 'kconf_01', conflicting_claims: 'Lesson A requires strict SLA buffering for cache latency, while Lesson B recommends relaxed eventual consistency.', context_differences: 'Lesson A applies to real-time auth gateways; Lesson B applies to non-critical background SSO sessions.' }
          ],
          invalidations: [
            { id: 'inv_01', trigger: 'new_contradictory_evidence', rationale: 'Single-region cache fallback assumption invalidated by 2026 Q2 fiber outage evidence.' }
          ],
          reviews: [
            { id: 'rev_01', trigger_reason: 'scheduled_quarterly_review', status: 'pending_review' }
          ],
          reuses: [
            { id: 'reuse_01', decision_id: 'dec_wave_03_sso', recommendation_influence: 'high', result: 'successful', outcome_summary: 'Pre-warming reduced Wave 3 p99 latency to 38ms with zero auth dropouts.' }
          ],
          packs: [
            { id: 'kpack_01', pack_version: 'v1.0', decision_id: 'dec_res_01' }
          ],
          qualities: [
            { id: 'kqual_01', completeness: 0.95, provenance: 0.98, freshness: 0.96, validation_level: 0.95 }
          ],
          gaps: [
            { id: 'kgap_01', gap_title: 'Missing Precedent for Secondary Vendor Multi-Cloud Interconnect Failure', priority: 'high', recommended_activity: 'Execute controlled digital twin simulation for multi-cloud vendor fiber severance.' }
          ],
          ignoredLessons: [
            { id: 'attn_ign_01', lesson_id: 'kobj_less_01', target_decision_id: 'dec_unbudgeted_bypass', status: 'ignored', reason: 'Highly applicable validated lesson (Secondary Cloud SLA Buffer) was not considered during decision drafting.' }
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
      const res = await fetch(`/api/v1/transformation-resilience-decision-knowledge/query?query=${encodeURIComponent(queryText)}`, {
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
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-teal-400 via-emerald-400 to-cyan-400">
              Governed Decision Knowledge Intelligence 2.0
            </h1>
            <span className="px-3 py-1 text-xs font-semibold rounded-full bg-teal-500/10 text-teal-400 border border-teal-500/20">
              Governed Resilience Decision Knowledge
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Curates, validates, versions, and retrieves advisory decision knowledge, validated lessons, recurring patterns, and precedents for future resilience decisions.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={fetchData}
            className="px-4 py-2 text-xs font-medium rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition"
          >
            Refresh Knowledge Base
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Knowledge Objects</p>
          <p className="text-xl font-bold text-teal-400 mt-1">{data?.knowledgeObjectsCount ?? 3}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Validated Objects</p>
          <p className="text-xl font-bold text-emerald-400 mt-1">{data?.validatedObjectsCount ?? 2}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Contested Objects</p>
          <p className="text-xl font-bold text-amber-400 mt-1">{data?.contestedObjectsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Knowledge Conflicts</p>
          <p className="text-xl font-bold text-rose-400 mt-1">{data?.conflictsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Knowledge Packs</p>
          <p className="text-xl font-bold text-cyan-400 mt-1">{data?.packsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Knowledge Gaps</p>
          <p className="text-xl font-bold text-purple-400 mt-1">{data?.gapsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Successful Reuses</p>
          <p className="text-xl font-bold text-indigo-400 mt-1">100%</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Ignored Lessons</p>
          <p className="text-xl font-bold text-amber-400 mt-1">{data?.ignoredLessons?.length ?? 1}</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 overflow-x-auto space-x-2 scrollbar-none">
        {[
          { id: 'overview', label: 'Knowledge Overview' },
          { id: 'lessons', label: 'Relevant Lessons' },
          { id: 'patterns', label: 'Patterns' },
          { id: 'precedents', label: 'Precedents' },
          { id: 'assumptions', label: 'Assumptions' },
          { id: 'scenario', label: 'Scenario Insights' },
          { id: 'recovery', label: 'Recovery Insights' },
          { id: 'investment', label: 'Investment Insights' },
          { id: 'conflicts', label: 'Conflicts' },
          { id: 'validation', label: 'Validation' },
          { id: 'applicability', label: 'Applicability' },
          { id: 'reuse', label: 'Reuse View' },
          { id: 'gaps', label: 'Knowledge Gaps' },
          { id: 'decay', label: 'Decay View' },
          { id: 'reviews', label: 'Reviews' },
          { id: 'timeline', label: 'Timeline' },
          { id: 'query', label: 'Decision Knowledge Query' }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-2.5 text-xs font-semibold whitespace-nowrap border-b-2 transition ${
              activeTab === tab.id
                ? 'border-teal-400 text-teal-400 bg-teal-500/5'
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
            Retrieving decision knowledge objects, computing applicability scores, and verifying provenance...
          </div>
        ) : (
          <>
            {activeTab === 'overview' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Governed Decision Knowledge Domain</h3>
                {data?.domains?.map((dom: any) => (
                  <div key={dom.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 flex justify-between items-center">
                    <div>
                      <span className="font-semibold text-teal-400">{dom.name}</span>
                      <p className="text-xs text-slate-400 mt-1">Owner: {dom.owner} | Version: {dom.version}</p>
                    </div>
                    <span className="text-xs px-3 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-semibold">{dom.status}</span>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'lessons' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Validated & Contested Resilience Lessons</h3>
                {data?.knowledgeObjects?.filter((k: any) => k.type === 'lesson').map((less: any) => (
                  <div key={less.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-semibold text-teal-400">Lesson (v{less.version})</span>
                      <span className={`text-xs px-2.5 py-1 rounded font-semibold border ${less.status === 'validated' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' : 'bg-amber-500/10 text-amber-400 border-amber-500/20'}`}>
                        {less.status}
                      </span>
                    </div>
                    <p className="text-xs text-slate-200">{less.statement}</p>
                    <p className="text-xs text-slate-400 font-mono">Limitations: {less.limitations}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'patterns' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Validated Resilience Decision Patterns</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                  <span className="text-sm font-semibold text-indigo-400">Multi-Region Token Cache Pre-Warming Pattern</span>
                  <p className="text-xs text-slate-300">Supporting Cases: 6 | Confidence: 94%</p>
                  <p className="text-xs text-slate-400">Context: High-concurrency OAuth expansion waves.</p>
                </div>
              </div>
            )}

            {activeTab === 'precedents' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Relevant Historical Precedents</h3>
                {data?.knowledgeObjects?.filter((k: any) => k.type === 'precedent').map((prec: any) => (
                  <div key={prec.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <span className="text-sm font-semibold text-cyan-400">{prec.statement}</span>
                    <p className="text-xs text-slate-300">Confidence: {((prec.confidence ?? 0.92) * 100).toFixed(0)}% | Applicability: {prec.applicability_level}</p>
                    <p className="text-xs text-slate-400">Limitations: {prec.limitations}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'conflicts' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Surfaced Knowledge Conflicts</h3>
                {data?.conflicts?.map((kc: any) => (
                  <div key={kc.id} className="p-4 rounded-xl bg-slate-950/60 border border-rose-500/30 space-y-2">
                    <span className="text-xs font-semibold text-rose-400">Contradictory Decision Knowledge</span>
                    <p className="text-xs text-slate-300">{kc.conflicting_claims}</p>
                    <p className="text-xs text-slate-400">Context Differences: {kc.context_differences}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'validation' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Evidence Validation Metrics</h3>
                {data?.validations?.map((v: any) => (
                  <div key={v.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <p className="text-xs text-slate-300">Supporting Cases: {v.supporting_cases_count} | Contradicting: {v.contradicting_cases_count}</p>
                    <p className="text-xs text-slate-400">Evidence Quality: {((v.evidence_quality ?? 0.96) * 100).toFixed(0)}% | Reproducibility: {((v.reproducibility ?? 0.94) * 100).toFixed(0)}%</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'applicability' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Applicability Score & Context Match</h3>
                {data?.applicabilities?.map((app: any) => (
                  <div key={app.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <span className="text-xs font-semibold text-emerald-400">Level: {app.level} (Score: {app.applicability_score})</span>
                    <p className="text-xs text-slate-300">{app.explanation}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'reuse' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Knowledge Reuse History & Outcomes</h3>
                {data?.reuses?.map((r: any) => (
                  <div key={r.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-semibold text-indigo-400">Decision: {r.decision_id}</span>
                      <span className="text-xs px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">{r.result}</span>
                    </div>
                    <p className="text-xs text-slate-300">{r.outcome_summary}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'gaps' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Identified Knowledge Gaps</h3>
                {data?.gaps?.map((g: any) => (
                  <div key={g.id} className="p-4 rounded-xl bg-slate-950/60 border border-purple-500/30 space-y-2">
                    <span className="text-sm font-semibold text-purple-400">{g.gap_title}</span>
                    <p className="text-xs text-slate-300">Priority: {g.priority}</p>
                    <p className="text-xs text-slate-400">Recommended Activity: {g.recommended_activity}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'decay' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Knowledge Decay & Review Status</h3>
                {data?.reviews?.map((rev: any) => (
                  <div key={rev.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <span className="text-xs font-semibold text-amber-400">Trigger: {rev.trigger_reason}</span>
                    <p className="text-xs text-slate-300">Status: {rev.status}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'query' && (
              <div className="space-y-6">
                <h3 className="text-base font-semibold text-slate-200">Natural Language Decision Knowledge Query</h3>
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={queryText}
                    onChange={(e) => setQueryText(e.target.value)}
                    placeholder="Ask a decision knowledge, precedent, or validated lesson question..."
                    className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-teal-500/50"
                  />
                  <button
                    onClick={handleQuery}
                    disabled={queryLoading}
                    className="px-5 py-2.5 bg-teal-500 hover:bg-teal-600 disabled:opacity-50 text-slate-950 text-xs font-semibold rounded-xl transition"
                  >
                    {queryLoading ? 'Processing...' : 'Run Query'}
                  </button>
                </div>

                {queryResult && (
                  <div className="p-5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-semibold text-teal-400">Governed Knowledge Result</span>
                      <span className="text-xs text-slate-400">Confidence: {queryResult.confidencePct}%</span>
                    </div>
                    {queryResult.evidenceJson?.error ? (
                      <div className="text-xs text-rose-400 font-semibold">{queryResult.evidenceJson.error}</div>
                    ) : (
                      <div className="space-y-2 text-xs text-slate-300">
                        {queryResult.results?.map((r: any, idx: number) => (
                          <div key={idx} className="p-3 bg-slate-900 rounded-lg space-y-1">
                            <p><strong className="text-teal-400">Validated Lesson:</strong> {r.validated_lesson}</p>
                            <p><strong className="text-cyan-400">Precedent:</strong> {r.precedent}</p>
                            <p><strong className="text-emerald-400">Retrieval Explanation:</strong> {r.retrieval_explanation}</p>
                            <p><strong className="text-rose-400">Conflicts:</strong> {r.conflicts}</p>
                            <p><strong className="text-amber-400">Applicability Ranking:</strong> {r.applicability_ranking}</p>
                            <p><strong className="text-indigo-400">Reuse History:</strong> {r.reuse_history}</p>
                            <p><strong className="text-purple-400">Knowledge Gaps:</strong> {r.knowledge_gaps}</p>
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
