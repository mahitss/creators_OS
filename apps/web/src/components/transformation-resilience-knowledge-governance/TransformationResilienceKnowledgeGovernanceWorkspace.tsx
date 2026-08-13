'use client';

import React, { useState, useEffect } from 'react';

export function TransformationResilienceKnowledgeGovernanceWorkspace() {
  const [activeTab, setActiveTab] = useState<
    'overview' | 'health' | 'evidence' | 'claims' | 'conflicts' | 'drift' | 'reuse' | 'influence' | 'risks' | 'reviews' | 'revalidation' | 'gaps' | 'state' | 'lineage' | 'query'
  >('overview');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('Which resilience knowledge is trustworthy and why is this knowledge under review?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/transformation-resilience-knowledge-governance');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      } else {
        // Fallback seed data
        setData({
          domainsCount: 1,
          healthsCount: 1,
          trustedCount: 1,
          reviewRequiredCount: 0,
          contestedCount: 0,
          claimsCount: 1,
          conflictsCount: 1,
          contextDriftsCount: 1,
          reviewsCount: 1,
          revalidationsCount: 1,
          gapsCount: 1,
          domains: [
            { id: 'adom_01', name: 'Global Enterprise Continuous Knowledge Assurance & Evidence Quality 2.0', owner: 'Principal Enterprise Knowledge Governance Architect', status: 'active', version: 'v2.0' }
          ],
          healths: [
            { id: 'kh_01', knowledge_object_id: 'kobj_less_01', freshness_score: 0.96, provenance_score: 0.98, validation_strength: 0.95, applicability_score: 0.94, reuse_score: 0.92, consistency_score: 0.90, context_stability: 0.96, evidence_coverage: 0.95, overall_status: 'trusted' }
          ],
          evidence: [
            { id: 'eass_01', source: 'Multi-Region Token Cache Telemetry Mesh', freshness: 0.96, quality: 0.95, reliability: 0.98, independence_type: 'independent', coverage: 0.94 }
          ],
          claims: [
            { id: 'claim_01', statement: 'Secondary Cloud SLA buffer must be +15ms to absorb vendor maintenance jitter.', claim_type: 'validated', confidence: 0.95, status: 'active' }
          ],
          conflicts: [
            { id: 'cconf_01', claim_a_id: 'claim_01', claim_b_id: 'claim_eventual_consistency', context_description: 'Claim A applies to real-time auth; Claim B applies to background sync.', severity: 'medium' }
          ],
          drifts: [
            { id: 'cdrift_01', dimension: 'vendor_infrastructure_topology', drift_description: 'Secondary cloud region network provider announced fiber route upgrade in Q3.', status: 'changing' }
          ],
          reuses: [
            { id: 'rass_01', reuse_count: 5, successful_reuse_count: 5, failed_reuse_count: 0, context_similarity_score: 0.95 }
          ],
          influences: [
            { id: 'inf_01', target_type: 'decision', target_id: 'dec_res_01', influence_level: 'high' }
          ],
          risks: [
            { id: 'krisk_01', risk_type: 'high_influence_low_quality', severity: 'low', confidence: 0.92 }
          ],
          reviews: [
            { id: 'arev_01', trigger: 'context_drift_detected', priority: 'high', recommended_action: 'revalidate', status: 'pending' }
          ],
          revalidations: [
            { id: 'reval_01', review_question: 'Does the +15ms SLA buffer apply to new 10Gbps interconnects?', result: 'narrowed', reviewer: 'Principal Knowledge Governance Architect' }
          ],
          lineages: [
            { id: 'lin_01', knowledge_object_id: 'kobj_less_01', source_decision_id: 'dec_res_01', outcome_id: 'obs_out_01', lesson_id: 'less_01' }
          ],
          gaps: [
            { id: 'egap_01', gap_title: 'Lack of Independent Corroboration for Secondary Cloud Provider SLA Jitter', priority: 'high', recommended_activity: 'Collect telemetry from independent third-party monitoring vendor.' }
          ],
          states: [
            { id: 'govstate_01', state: 'trusted', authorized_by: 'Enterprise Knowledge Governance Board', rationale: 'High evidence coverage and 100% successful reuse rate across 5 decisions.' }
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
      const res = await fetch(`/api/v1/transformation-resilience-knowledge-governance/query?query=${encodeURIComponent(queryText)}`, {
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
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-emerald-400 via-teal-400 to-cyan-400">
              Continuous Knowledge Assurance & Evidence Quality 2.0
            </h1>
            <span className="px-3 py-1 text-xs font-semibold rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              Human-Governed Knowledge Revalidation
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Continuous evidence assurance, source independence verification, claim conflict detection, context drift tracking, and revalidation review packets.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={fetchData}
            className="px-4 py-2 text-xs font-medium rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition"
          >
            Refresh Assurance Telemetry
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Assurance Domain</p>
          <p className="text-xl font-bold text-emerald-400 mt-1">{data?.domainsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Trusted Objects</p>
          <p className="text-xl font-bold text-teal-400 mt-1">{data?.trustedCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Evidence Quality</p>
          <p className="text-xl font-bold text-cyan-400 mt-1">95.0%</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Independence</p>
          <p className="text-xl font-bold text-indigo-400 mt-1">Independent</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Context Drift</p>
          <p className="text-xl font-bold text-amber-400 mt-1">{data?.contextDriftsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Pending Reviews</p>
          <p className="text-xl font-bold text-rose-400 mt-1">{data?.reviewsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Revalidations</p>
          <p className="text-xl font-bold text-purple-400 mt-1">{data?.revalidationsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Evidence Gaps</p>
          <p className="text-xl font-bold text-blue-400 mt-1">{data?.gapsCount ?? 1}</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 overflow-x-auto space-x-2 scrollbar-none">
        {[
          { id: 'overview', label: 'Assurance Overview' },
          { id: 'health', label: 'Knowledge Health' },
          { id: 'evidence', label: 'Evidence Assurance' },
          { id: 'claims', label: 'Claims & Support' },
          { id: 'conflicts', label: 'Claim Conflicts' },
          { id: 'drift', label: 'Context Drift' },
          { id: 'reuse', label: 'Reuse Assurance' },
          { id: 'influence', label: 'Knowledge Influence' },
          { id: 'risks', label: 'Knowledge Risk' },
          { id: 'reviews', label: 'Review Queue & Packets' },
          { id: 'revalidation', label: 'Revalidation & Narrowing' },
          { id: 'gaps', label: 'Evidence Gaps' },
          { id: 'state', label: 'Governance State' },
          { id: 'lineage', label: 'Knowledge Lineage' },
          { id: 'query', label: 'Knowledge Governance Query' }
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

      {/* Tab Content */}
      <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 min-h-[400px]">
        {loading ? (
          <div className="flex items-center justify-center h-64 text-slate-400 text-sm">
            Evaluating continuous knowledge health, checking source independence, and building lineage graphs...
          </div>
        ) : (
          <>
            {activeTab === 'overview' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Knowledge Governance Assurance Domain</h3>
                {data?.domains?.map((dom: any) => (
                  <div key={dom.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 flex justify-between items-center">
                    <div>
                      <span className="font-semibold text-emerald-400">{dom.name}</span>
                      <p className="text-xs text-slate-400 mt-1">Owner: {dom.owner} | Version: {dom.version}</p>
                    </div>
                    <span className="text-xs px-3 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-semibold">{dom.status}</span>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'health' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Multidimensional Knowledge Health</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {[
                    { label: 'Freshness Score', score: 0.96 },
                    { label: 'Provenance Score', score: 0.98 },
                    { label: 'Validation Strength', score: 0.95 },
                    { label: 'Applicability Score', score: 0.94 },
                    { label: 'Reuse Score', score: 0.92 },
                    { label: 'Consistency Score', score: 0.90 },
                    { label: 'Context Stability', score: 0.96 },
                    { label: 'Evidence Coverage', score: 0.95 }
                  ].map((h, idx) => (
                    <div key={idx} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 text-center">
                      <span className="text-xs font-medium text-slate-400">{h.label}</span>
                      <p className="text-lg font-bold text-teal-400 mt-1">{(h.score * 100).toFixed(0)}%</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'evidence' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Source Independence & Evidence Assurance</h3>
                {data?.evidence?.map((e: any) => (
                  <div key={e.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-semibold text-cyan-400">{e.source}</span>
                      <span className="text-xs px-2.5 py-1 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-semibold">{e.independence_type}</span>
                    </div>
                    <p className="text-xs text-slate-300">Freshness: {((e.freshness ?? 0.96) * 100).toFixed(0)}% | Quality: {((e.quality ?? 0.95) * 100).toFixed(0)}% | Reliability: {((e.reliability ?? 0.98) * 100).toFixed(0)}%</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'claims' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Knowledge Claims & Corroborating Support</h3>
                {data?.claims?.map((c: any) => (
                  <div key={c.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <span className="text-xs font-semibold text-blue-400 uppercase">{c.claim_type} Claim</span>
                    <p className="text-xs text-slate-200">{c.statement}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'conflicts' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Claim Conflicts & Severity Ranking</h3>
                {data?.conflicts?.map((cc: any) => (
                  <div key={cc.id} className="p-4 rounded-xl bg-slate-950/60 border border-amber-500/30 space-y-2">
                    <span className="text-xs font-semibold text-amber-400">Severity: {cc.severity}</span>
                    <p className="text-xs text-slate-300">{cc.context_description}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'drift' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Context Drift Tracking</h3>
                {data?.drifts?.map((cd: any) => (
                  <div key={cd.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <span className="text-xs font-semibold text-indigo-400">Dimension: {cd.dimension}</span>
                    <p className="text-xs text-slate-300">{cd.drift_description}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'influence' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Knowledge Influence Mapping</h3>
                {data?.influences?.map((inf: any) => (
                  <div key={inf.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <span className="text-xs font-semibold text-emerald-400">Influence: {inf.influence_level}</span>
                    <p className="text-xs text-slate-300">Influences {inf.target_type} ID: {inf.target_id}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'reviews' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Assurance Review Queue & Review Packets</h3>
                {data?.reviews?.map((rev: any) => (
                  <div key={rev.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-semibold text-rose-400">Trigger: {rev.trigger}</span>
                      <span className="text-xs px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20">{rev.priority}</span>
                    </div>
                    <p className="text-xs text-slate-300">Recommended Action: {rev.recommended_action}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'revalidation' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Revalidation & Applicability Narrowing</h3>
                {data?.revalidations?.map((reval: any) => (
                  <div key={reval.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <span className="text-xs font-semibold text-purple-400">Result: {reval.result}</span>
                    <p className="text-xs text-slate-300">Review Question: {reval.review_question}</p>
                    <p className="text-xs text-slate-400">New Context: {reval.new_context}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'gaps' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Prioritized Evidence Gaps</h3>
                {data?.gaps?.map((g: any) => (
                  <div key={g.id} className="p-4 rounded-xl bg-slate-950/60 border border-purple-500/30 space-y-2">
                    <span className="text-sm font-semibold text-purple-400">{g.gap_title}</span>
                    <p className="text-xs text-slate-300">Priority: {g.priority}</p>
                    <p className="text-xs text-slate-400">Recommended Activity: {g.recommended_activity}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'state' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Governance State & Authorization</h3>
                {data?.states?.map((st: any) => (
                  <div key={st.id} className="p-4 rounded-xl bg-slate-950/60 border border-emerald-500/30 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-bold text-emerald-400 uppercase">State: {st.state}</span>
                      <span className="text-xs text-slate-400">Authorized By: {st.authorized_by}</span>
                    </div>
                    <p className="text-xs text-slate-300">{st.rationale}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'lineage' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Full Knowledge Lineage Graph</h3>
                {data?.lineages?.map((lin: any) => (
                  <div key={lin.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2 font-mono text-xs">
                    <p><strong className="text-emerald-400">Source Decision:</strong> {lin.source_decision_id}</p>
                    <p><strong className="text-teal-400">Observed Outcome:</strong> {lin.outcome_id}</p>
                    <p><strong className="text-cyan-400">Lesson:</strong> {lin.lesson_id}</p>
                    <p><strong className="text-indigo-400">Pattern:</strong> {lin.pattern_id}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'query' && (
              <div className="space-y-6">
                <h3 className="text-base font-semibold text-slate-200">Natural Language Knowledge Governance Query</h3>
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={queryText}
                    onChange={(e) => setQueryText(e.target.value)}
                    placeholder="Ask a knowledge trustworthiness, context drift, or revalidation question..."
                    className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-emerald-500/50"
                  />
                  <button
                    onClick={handleQuery}
                    disabled={queryLoading}
                    className="px-5 py-2.5 bg-emerald-500 hover:bg-emerald-600 disabled:opacity-50 text-slate-950 text-xs font-semibold rounded-xl transition"
                  >
                    {queryLoading ? 'Processing...' : 'Run Query'}
                  </button>
                </div>

                {queryResult && (
                  <div className="p-5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-semibold text-emerald-400">Governance Assurance Result</span>
                      <span className="text-xs text-slate-400">Confidence: {queryResult.confidencePct}%</span>
                    </div>
                    {queryResult.evidenceJson?.error ? (
                      <div className="text-xs text-rose-400 font-semibold">{queryResult.evidenceJson.error}</div>
                    ) : (
                      <div className="space-y-2 text-xs text-slate-300">
                        {queryResult.results?.map((r: any, idx: number) => (
                          <div key={idx} className="p-3 bg-slate-900 rounded-lg space-y-1">
                            <p><strong className="text-emerald-400">Trustworthiness:</strong> {r.trustworthiness}</p>
                            <p><strong className="text-cyan-400">Evidence Assurance:</strong> {r.evidence_assurance}</p>
                            <p><strong className="text-teal-400">Claims Support:</strong> {r.claims_support}</p>
                            <p><strong className="text-indigo-400">Context Drift:</strong> {r.context_drift}</p>
                            <p><strong className="text-rose-400">Contested Warning:</strong> {r.contested_warning}</p>
                            <p><strong className="text-amber-400">Knowledge Influence:</strong> {r.knowledge_influence}</p>
                            <p><strong className="text-purple-400">Evidence Gaps:</strong> {r.evidence_gaps}</p>
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
