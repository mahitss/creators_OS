'use client';

import React, { useState, useEffect } from 'react';

export function TransformationResiliencePortfolioWorkspace() {
  const [activeTab, setActiveTab] = useState<'overview' | 'exposures' | 'shared_deps' | 'capacity' | 'multi_failure' | 'investments' | 'overlaps_gaps' | 'tradeoffs_sequences' | 'verification' | 'portfolio_query'>('overview');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('Which transformations share critical dependencies across Wave 2 and Wave 3?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/transformation-resilience-portfolio');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      } else {
        // Fallback seed data
        setData({
          activePortfoliosCount: 1,
          systemicExposuresCount: 1,
          sharedDependenciesCount: 1,
          capacityConflictsCount: 1,
          systemicRisksCount: 1,
          investmentCandidatesCount: 1,
          investmentOverlapsCount: 1,
          investmentGapsCount: 1,
          portfolioRobustnessScore: 0.94,
          portfolios: [
            { id: 'port_res_01', name: 'Global Enterprise Transformation Resilience Portfolio 2.0', scope: 'enterprise', owner: 'Chief Resilience Portfolio Architect', status: 'baseline', version: 'v2.0' }
          ],
          exposures: [
            { id: 'exp_01', transformation_id: 'wave_02_finops', exposure_type: 'dependency', severity: 'high', confidence: 0.94 }
          ],
          sharedDependencies: [
            { id: 'sdep_01', dependency_name: 'Central IAM OAuth Federation Gateway v2', criticality: 0.96, affected_transformations_json: ['wave_02_finops', 'wave_03_sso', 'wave_04_hr_cloud'] }
          ],
          capacityExposures: [
            { id: 'cap_01', capacity_type: 'engineering_fte', required_capacity: 45.0, available_capacity: 30.0, contention_score: 0.88 }
          ],
          capacityConflicts: [
            { id: 'conf_01', capacity_resource: 'Senior IAM Security Engineers', severity: 'high' }
          ],
          failurePatterns: [
            { id: 'fpat_01', pattern_name: 'Shared Identity Dependency Bottleneck Pattern', recurring_failure_type: 'single_dependency', affected_transformations_count: 4, confidence: 0.95 }
          ],
          systemicRisks: [
            { id: 'srisk_01', source_dependency: 'Central OAuth Gateway API', severity: 'critical', confidence: 0.97 }
          ],
          multiFailures: [
            { id: 'mfail_01', scenario_title: 'Simultaneous IAM Gateway Failure & Regional Cloud Quota Exhaustion' }
          ],
          investments: [
            { id: 'pinv_01', investment_title: 'Cross-Portfolio Active-Active IAM Gateway & 15 FTE Resilience Reserve', cost: 350000.0, risk_reduction_pct: 65.0, priority: 'high' }
          ],
          overlaps: [
            { id: 'over_01', duplicated_coverage_description: 'Wave 2 local failover investment is redundant given portfolio-wide active-active deployment.', potential_savings: 120000.0 }
          ],
          gaps: [
            { id: 'gap_01', unprotected_systemic_exposure: 'Wave 4 HR Cloud Migration lacks fallback vendor SLA coverage.', severity: 'high' }
          ],
          tradeoffs: [
            { id: 'trade_01', option_a_json: { title: 'Active-Active IAM Gateway', cost: 350000.0 }, option_b_json: { title: 'Distributed Rate Limiter', cost: 150000.0 } }
          ],
          sequences: [
            { id: 'seq_01', sequence_order: 1, investment_id: 'pinv_01' }
          ],
          optionValues: [
            { id: 'optv_01', option_name: 'Multi-Cloud IAM Federation Option', flexibility_score: 0.93, preserved_future_paths_count: 4 }
          ],
          diversifications: [
            { id: 'div_01', concentration_target: 'Single Primary Cloud Auth Provider', proposed_diversification: 'Deploy secondary cloud provider fallback route.' }
          ],
          roadmaps: [
            { id: 'proad_01', roadmap_title: 'Enterprise Portfolio Resilience Protection Roadmap 2.0', total_budget: 750000.0, status: 'draft' }
          ],
          reviews: [
            { id: 'prev_01', review_trigger: 'Shared Dependency Concentration Exceeded 90%', status: 'open' }
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
      const res = await fetch(`/api/v1/transformation-resilience-portfolio/query?query=${encodeURIComponent(queryText)}`, {
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
              Transformation Resilience Portfolio 2.0
            </h1>
            <span className="px-3 py-1 text-xs font-semibold rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              Cross-Portfolio Protection Engine
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Optimizing structural resilience, capacity allocation, shared dependencies, and investment coverage across the enterprise transformation portfolio.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={fetchData}
            className="px-4 py-2 text-xs font-medium rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition"
          >
            Refresh Telemetry
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Portfolio Robustness</p>
          <p className="text-xl font-bold text-emerald-400 mt-1">{data?.portfolioRobustnessScore ?? 0.94}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Shared Dependencies</p>
          <p className="text-xl font-bold text-teal-400 mt-1">{data?.sharedDependenciesCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Capacity Conflicts</p>
          <p className="text-xl font-bold text-amber-400 mt-1">{data?.capacityConflictsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Systemic Risks</p>
          <p className="text-xl font-bold text-rose-400 mt-1">{data?.systemicRisksCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Investments</p>
          <p className="text-xl font-bold text-cyan-400 mt-1">{data?.investmentCandidatesCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Overlaps Detected</p>
          <p className="text-xl font-bold text-violet-400 mt-1">{data?.investmentOverlapsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Investment Gaps</p>
          <p className="text-xl font-bold text-rose-400 mt-1">{data?.investmentGapsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Systemic Exposures</p>
          <p className="text-xl font-bold text-sky-400 mt-1">{data?.systemicExposuresCount ?? 1}</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 overflow-x-auto space-x-2 scrollbar-none">
        {[
          { id: 'overview', label: 'Portfolio Overview' },
          { id: 'exposures', label: 'Resilience Exposures' },
          { id: 'shared_deps', label: 'Shared Dependencies' },
          { id: 'capacity', label: 'Shared Capacity & Conflicts' },
          { id: 'multi_failure', label: 'Multi-Failure Scenarios' },
          { id: 'investments', label: 'Resilience Investments' },
          { id: 'overlaps_gaps', label: 'Overlaps & Gaps' },
          { id: 'tradeoffs_sequences', label: 'Trade-Offs & Sequences' },
          { id: 'verification', label: 'Roadmap & Verification' },
          { id: 'portfolio_query', label: 'Natural Language Query' },
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
            Loading Transformation Resilience Portfolio telemetry...
          </div>
        ) : (
          <>
            {activeTab === 'overview' && (
              <div className="space-y-6">
                <h3 className="text-base font-semibold text-slate-200">Portfolio Baseline Summary</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {data?.portfolios?.map((p: any) => (
                    <div key={p.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="font-semibold text-emerald-400">{p.name}</span>
                        <span className="text-xs px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">{p.status}</span>
                      </div>
                      <p className="text-xs text-slate-400">Scope: {p.scope} | Owner: {p.owner} | Version: {p.version}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'exposures' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Resilience Exposures Across Portfolio</h3>
                <div className="space-y-3">
                  {data?.exposures?.map((exp: any) => (
                    <div key={exp.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 flex justify-between items-center">
                      <div>
                        <span className="text-sm font-medium text-slate-200">Transformation: {exp.transformation_id}</span>
                        <p className="text-xs text-slate-400 mt-1">Exposure Type: {exp.exposure_type} | Confidence: {exp.confidence}</p>
                      </div>
                      <span className="text-xs px-2.5 py-1 rounded bg-rose-500/10 text-rose-400 border border-rose-500/20 font-semibold">{exp.severity}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'shared_deps' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Shared Dependency Concentration</h3>
                <div className="space-y-3">
                  {data?.sharedDependencies?.map((dep: any) => (
                    <div key={dep.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="font-medium text-teal-400">{dep.dependency_name}</span>
                        <span className="text-xs px-2 py-0.5 rounded bg-teal-500/10 text-teal-400 border border-teal-500/20">Criticality: {dep.criticality * 100}%</span>
                      </div>
                      <p className="text-xs text-slate-400">Affected Waves: {dep.affected_transformations_json?.join(', ')}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'capacity' && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-base font-semibold text-slate-200 mb-3">Shared Capacity Exposures</h3>
                  {data?.capacityExposures?.map((cap: any) => (
                    <div key={cap.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 mb-2">
                      <span className="font-medium text-amber-400">Type: {cap.capacity_type}</span>
                      <p className="text-xs text-slate-400 mt-1">Required: {cap.required_capacity} FTE | Available: {cap.available_capacity} FTE | Contention Score: {cap.contention_score}</p>
                    </div>
                  ))}
                </div>
                <div>
                  <h3 className="text-base font-semibold text-slate-200 mb-3">Capacity Conflicts</h3>
                  {data?.capacityConflicts?.map((conf: any) => (
                    <div key={conf.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 flex justify-between items-center">
                      <span className="text-sm font-medium text-slate-200">Resource: {conf.capacity_resource}</span>
                      <span className="text-xs px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20">{conf.severity}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'multi_failure' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Multi-Failure Scenario Simulation</h3>
                {data?.multiFailures?.map((mf: any) => (
                  <div key={mf.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                    <span className="font-medium text-rose-400">{mf.scenario_title}</span>
                    <p className="text-xs text-slate-400">Simultaneous Failures: {mf.simultaneous_failures_json?.join(' + ')}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'investments' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Cross-Portfolio Resilience Investments</h3>
                {data?.investments?.map((inv: any) => (
                  <div key={inv.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 flex justify-between items-center">
                    <div>
                      <span className="font-medium text-cyan-400">{inv.investment_title}</span>
                      <p className="text-xs text-slate-400 mt-1">Cost: ${inv.cost?.toLocaleString()} | Protection Scope: {inv.protected_transformations_json?.join(', ')}</p>
                    </div>
                    <span className="text-xs px-3 py-1 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 font-semibold">{inv.risk_reduction_pct}% Risk Reduction</span>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'overlaps_gaps' && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h3 className="text-base font-semibold text-slate-200 mb-3">Duplicated Coverage & Overlaps</h3>
                  {data?.overlaps?.map((over: any) => (
                    <div key={over.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 mb-3">
                      <p className="text-xs text-slate-300">{over.duplicated_coverage_description}</p>
                      <span className="text-xs text-emerald-400 font-semibold mt-2 inline-block">Potential Savings: ${over.potential_savings?.toLocaleString()}</span>
                    </div>
                  ))}
                </div>
                <div>
                  <h3 className="text-base font-semibold text-slate-200 mb-3">Unprotected Investment Gaps</h3>
                  {data?.gaps?.map((gap: any) => (
                    <div key={gap.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 mb-3">
                      <p className="text-xs text-slate-300">{gap.unprotected_systemic_exposure}</p>
                      <span className="text-xs text-rose-400 font-semibold mt-2 inline-block">Severity: {gap.severity}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'tradeoffs_sequences' && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-base font-semibold text-slate-200 mb-3">Investment Trade-Off Analyses</h3>
                  {data?.tradeoffs?.map((tr: any) => (
                    <div key={tr.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                      <p className="text-xs text-slate-300">Option A: {tr.option_a_json?.title} (${tr.option_a_json?.cost})</p>
                      <p className="text-xs text-slate-300">Option B: {tr.option_b_json?.title} (${tr.option_b_json?.cost})</p>
                    </div>
                  ))}
                </div>
                <div>
                  <h3 className="text-base font-semibold text-slate-200 mb-3">Capacity-Aware Sequencing</h3>
                  {data?.sequences?.map((seq: any) => (
                    <div key={seq.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                      <span className="text-xs font-semibold text-emerald-400">Sequence Order #{seq.sequence_order}</span>
                      <p className="text-xs text-slate-400 mt-1">Investment ID: {seq.investment_id}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'verification' && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-base font-semibold text-slate-200 mb-3">Portfolio Resilience Protection Roadmap 2.0</h3>
                  {data?.roadmaps?.map((road: any) => (
                    <div key={road.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                      <span className="font-semibold text-emerald-400">{road.roadmap_title}</span>
                      <p className="text-xs text-slate-400">Total Budget: ${road.total_budget?.toLocaleString()} | Milestones: {road.milestones_json?.join(' → ')}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'portfolio_query' && (
              <div className="space-y-6">
                <h3 className="text-base font-semibold text-slate-200">Natural Language Portfolio Query Engine</h3>
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={queryText}
                    onChange={(e) => setQueryText(e.target.value)}
                    placeholder="Ask a portfolio resilience question..."
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
                      <span className="text-xs font-semibold text-emerald-400">Query Result</span>
                      <span className="text-xs text-slate-400">Confidence: {queryResult.confidencePct}%</span>
                    </div>
                    {queryResult.evidenceJson?.error ? (
                      <div className="text-xs text-rose-400 font-semibold">{queryResult.evidenceJson.error}</div>
                    ) : (
                      <div className="space-y-2 text-xs text-slate-300">
                        {queryResult.results?.map((r: any, idx: number) => (
                          <div key={idx} className="p-3 bg-slate-900 rounded-lg space-y-1">
                            <p><strong className="text-emerald-400">Portfolio:</strong> {r.portfolio}</p>
                            <p><strong className="text-teal-400">Shared Dependency:</strong> {r.shared_dependency}</p>
                            <p><strong className="text-amber-400">Capacity Conflict:</strong> {r.capacity_conflict}</p>
                            <p><strong className="text-cyan-400">Recommended Investment:</strong> {r.recommended_investment}</p>
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
