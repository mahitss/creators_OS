'use client';

import React, { useState, useEffect } from 'react';

export function TransformationResilienceEngineeringWorkspace() {
  const [activeTab, setActiveTab] = useState<'overview' | 'failure_modes' | 'weaknesses_spofs' | 'redundancy_substitution' | 'buffers_optionality' | 'investments' | 'cascades' | 'interventions_roadmaps' | 'verification' | 'drills_lessons' | 'resilience_query'>('overview');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('Where are our biggest resilience weaknesses across Wave 2 and Wave 3?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/transformation-resilience-engineering');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      } else {
        // Fallback seed structure
        setData({
          activeResilienceDomainsCount: 1,
          detectedFailureModesCount: 1,
          systemicWeaknessesCount: 1,
          singlePointsOfFailureCount: 1,
          investmentCandidatesCount: 1,
          resilienceRobustnessScore: 0.91,
          domains: [
            { id: 'red_01', name: 'Global Transformation Resilience Engineering Domain', scope: 'enterprise', owner: 'Chief Resilience Engineer', status: 'baseline', version: 'v2.0' }
          ],
          baselines: [
            { id: 'base_01', robustness_score: 0.91, redundancy_score: 0.86, recoverability_score: 0.94, adaptability_score: 0.89 }
          ],
          failureModes: [
            { id: 'fm_01', failure_type: 'single_dependency', frequency: 4, severity: 'high', recovery_time_hours: 48.0 }
          ],
          weaknesses: [
            { id: 'weak_01', description: 'Systemic concentration of identity federation requests through single regional gateway.', severity: 'high' }
          ],
          spofs: [
            { id: 'spof_01', entity_type: 'dependency', entity_name: 'Core IAM OAuth Gateway v2', criticality_score: 0.95 }
          ],
          redundancies: [
            { id: 'red_option_01', title: 'Deploy Active-Active Multi-Region IAM Gateway Redundancy', cost_estimate: 150000.0, risk_reduction_score: 0.88 }
          ],
          substitutions: [
            { id: 'sub_01', primary_entity: 'Legacy OAuth Rate-Limiter', substitute_entity: 'Distributed Mesh Rate-Limiter Cluster', feasibility_score: 0.90 }
          ],
          buffers: [
            { id: 'buf_01', required_buffer_fte: 15.0, cost_estimate: 180000.0 }
          ],
          optionalities: [
            { id: 'opt_01', path_count: 3 }
          ],
          investments: [
            { id: 'inv_01', improvement_title: 'Multi-Region Active-Active IAM Gateway & 15 FTE Capacity Buffer', investment_amount: 250000.0, risk_reduction_pct: 45.0, priority: 'high' }
          ],
          cascades: [
            { id: 'casc_01', initial_trigger: 'IAM Rate-Limiter Failure', uncertainty_label: 'estimated' }
          ],
          interventions: [
            { id: 'inter_01', title: 'Proactive Active-Active Gateway Redundancy Implementation', priority_score: 0.92, recommendation_only: true }
          ],
          roadmaps: [
            { id: 'road_01', investment_total: 430000.0, status: 'draft' }
          ],
          comparisons: [
            { id: 'comp_01', baseline_scores_json: { robustness: 0.91 }, improved_scores_json: { robustness: 0.98 } }
          ],
          lessons: [
            { id: 'les_01', lesson_text: 'Automated active-active failover is mandatory for central identity federation dependencies.', confidence: 0.94 }
          ],
          patterns: [
            { id: 'pat_01', pattern_name: 'Shared Identity Dependency Concentration Pattern', confidence: 0.95 }
          ],
          warnings: [
            { id: 'warn_01', warning_signal: 'IAM Gateway Concentration Risk Warning', severity: 'high' }
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
      const res = await fetch(`/api/v1/transformation-resilience-engineering/query?query=${encodeURIComponent(queryText)}`, {
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
            <span className="p-2 bg-blue-600/20 text-blue-400 rounded-lg text-lg">🏗️</span>
            Enterprise Transformation Resilience Engineering 2.0
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Historical Disruptions → Failure Modes → Systemic Weaknesses → Resilience Engineering → Simulations → Governed Approvals → Verification.
          </p>
        </div>
        <div className="flex gap-2">
          <span className="px-3 py-1 bg-blue-500/10 text-blue-400 border border-blue-500/20 rounded-full text-xs font-semibold">
            Evidence-Backed Engineering
          </span>
          <span className="px-3 py-1 bg-purple-500/10 text-purple-400 border border-purple-500/20 rounded-full text-xs font-semibold">
            Zero Worker Surveillance
          </span>
        </div>
      </div>

      {/* Operational Telemetry Header */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Resilience Domains</div>
          <div className="text-2xl font-bold text-blue-400 mt-1">{data?.activeResilienceDomainsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Failure Modes</div>
          <div className="text-2xl font-bold text-red-400 mt-1">{data?.detectedFailureModesCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Systemic Weaknesses</div>
          <div className="text-2xl font-bold text-amber-400 mt-1">{data?.systemicWeaknessesCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Single Points of Failure</div>
          <div className="text-2xl font-bold text-orange-400 mt-1">{data?.singlePointsOfFailureCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Investment Proposals</div>
          <div className="text-2xl font-bold text-emerald-400 mt-1">{data?.investmentCandidatesCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Robustness Score</div>
          <div className="text-2xl font-bold text-teal-400 mt-1">91.0%</div>
        </div>
      </div>

      {/* Subsystem Tabs */}
      <div className="flex border-b border-slate-800 gap-2 text-sm overflow-x-auto pb-1">
        {[
          { id: 'overview', label: 'Resilience Overview & Domains' },
          { id: 'failure_modes', label: 'Failure Modes & Evidence' },
          { id: 'weaknesses_spofs', label: 'Systemic Weaknesses & SPOFs' },
          { id: 'redundancy_substitution', label: 'Redundancy & Substitutions' },
          { id: 'buffers_optionality', label: 'Capacity Buffers & Optionality' },
          { id: 'investments', label: 'Resilience Investment Candidates' },
          { id: 'cascades', label: 'Cascading Failure Simulations' },
          { id: 'interventions_roadmaps', label: 'Interventions & Roadmaps' },
          { id: 'verification', label: 'Verification & Comparisons' },
          { id: 'drills_lessons', label: 'Drills, Lessons & Patterns' },
          { id: 'resilience_query', label: 'Resilience Query Engine' }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-2 font-medium rounded-t-lg transition-colors whitespace-nowrap ${
              activeTab === tab.id
                ? 'bg-slate-900 text-blue-400 border-b-2 border-blue-500'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/40'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Content */}
      {loading ? (
        <div className="p-8 text-center text-slate-500">Loading Enterprise Transformation Resilience Engineering...</div>
      ) : (
        <div className="space-y-6">
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-blue-400 flex items-center gap-2">
                  <span>🏗️</span> Active Resilience Engineering Domains
                </h2>
                <div className="space-y-2 text-sm">
                  {data?.domains?.map((red: any) => (
                    <div key={red.id} className="p-3 bg-slate-950 rounded border border-blue-800/40 flex justify-between items-center text-xs">
                      <div>
                        <div className="font-bold text-slate-100">{red.name}</div>
                        <div className="text-slate-400">Scope: {red.scope} | Owner: {red.owner}</div>
                      </div>
                      <span className="px-2 py-0.5 bg-blue-500/20 text-blue-300 rounded font-bold">{red.status.toUpperCase()}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-amber-400 flex items-center gap-2">
                  <span>⚡</span> Dimension-Level Resilience Scorecard
                </h2>
                {data?.baselines?.map((b: any) => (
                  <div key={b.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-xs">
                    <div className="flex justify-between"><span>Robustness:</span> <span className="text-blue-300 font-bold">{(b.robustness_score * 100).toFixed(0)}%</span></div>
                    <div className="flex justify-between"><span>Redundancy:</span> <span className="text-indigo-300 font-bold">{(b.redundancy_score * 100).toFixed(0)}%</span></div>
                    <div className="flex justify-between"><span>Recoverability:</span> <span className="text-emerald-300 font-bold">{(b.recoverability_score * 100).toFixed(0)}%</span></div>
                    <div className="flex justify-between"><span>Adaptability:</span> <span className="text-teal-300 font-bold">{(b.adaptability_score * 100).toFixed(0)}%</span></div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'failure_modes' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Recurring Failure Modes & Evidence Analysis</h2>
              {data?.failureModes?.map((fm: any) => (
                <div key={fm.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-red-500">
                  <div className="flex justify-between items-center font-bold text-red-300">
                    <span>Failure Type: {fm.failure_type.toUpperCase()}</span>
                    <span className="text-xs px-2 py-0.5 bg-red-500/20 text-red-300 rounded font-bold">Recurrence: {fm.frequency}x</span>
                  </div>
                  <div className="text-xs text-slate-300">Historical Recovery Delay: {fm.recovery_time_hours} hours | Confidence: {(fm.confidence * 100).toFixed(0)}%</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'weaknesses_spofs' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Systemic Weaknesses & Single Points of Failure (SPOFs)</h2>
              {data?.spofs?.map((spof: any) => (
                <div key={spof.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-orange-500">
                  <div className="flex justify-between items-center font-bold text-orange-300">
                    <span>SPOF Entity: {spof.entity_name} ({spof.entity_type})</span>
                    <span className="text-xs px-2 py-0.5 bg-orange-500/20 text-orange-300 rounded font-bold">Criticality: {(spof.criticality_score * 100).toFixed(0)}%</span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'redundancy_substitution' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Redundancy & Technology Substitution Options</h2>
              {data?.redundancies?.map((red: any) => (
                <div key={red.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-indigo-500">
                  <div className="flex justify-between items-center font-bold text-indigo-300">
                    <span>Title: {red.title}</span>
                    <span className="text-xs px-2 py-0.5 bg-indigo-500/20 text-indigo-300 rounded font-bold">Risk Reduction: {(red.risk_reduction_score * 100).toFixed(0)}%</span>
                  </div>
                  <div className="text-xs text-slate-300">Estimated Investment: ${red.cost_estimate?.toLocaleString()}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'investments' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Resilience Investment Proposals</h2>
              {data?.investments?.map((inv: any) => (
                <div key={inv.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-emerald-500">
                  <div className="flex justify-between items-center font-bold text-emerald-300">
                    <span>Proposal: {inv.improvement_title}</span>
                    <span className="text-xs px-2 py-0.5 bg-emerald-500/20 text-emerald-300 rounded font-bold">Risk Reduction: {inv.risk_reduction_pct}%</span>
                  </div>
                  <div className="text-xs text-slate-300">Problem: {inv.problem_statement}</div>
                  <div className="text-xs text-teal-400 font-semibold">Investment Required: ${inv.investment_amount?.toLocaleString()} | Priority: {inv.priority.toUpperCase()}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'verification' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Before vs After Resilience Performance Comparisons</h2>
              {data?.comparisons?.map((comp: any) => (
                <div key={comp.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-purple-500">
                  <div className="font-bold text-purple-300">Baseline Robustness: {(comp.baseline_scores_json?.robustness * 100).toFixed(0)}% → Improved Robustness: {(comp.improved_scores_json?.robustness * 100).toFixed(0)}%</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'resilience_query' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Natural Language Resilience Engineering Query Engine</h2>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={queryText}
                  onChange={(e) => setQueryText(e.target.value)}
                  placeholder="Ask a resilience engineering query..."
                  className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-sm text-slate-100 focus:outline-none focus:border-blue-500"
                />
                <button
                  onClick={handleQuery}
                  disabled={queryLoading}
                  className="px-5 py-2 bg-blue-600 hover:bg-blue-500 text-white font-medium rounded-lg text-sm transition-colors"
                >
                  {queryLoading ? 'Analyzing...' : 'Query'}
                </button>
              </div>

              {queryResult && (
                <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                  <div className="text-xs text-blue-400 font-semibold">Query: {queryResult.query}</div>
                  <div className="space-y-2">
                    {queryResult.results?.map((res: any, idx: number) => (
                      <div key={idx} className="p-3 bg-slate-900 rounded space-y-1 text-xs">
                        <div className="font-semibold text-blue-300">{res.domain}</div>
                        <div className="text-amber-300">Systemic Weakness: {res.systemic_weakness}</div>
                        <div className="text-orange-300">Single Point of Failure: {res.single_point_of_failure}</div>
                        <div className="text-indigo-300">Redundancy Proposal: {res.redundancy_proposal}</div>
                        <div className="text-emerald-300">Investment Candidate: {res.investment_candidate}</div>
                        <div className="text-teal-300">Resilience Roadmap: {res.resilience_roadmap}</div>
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
