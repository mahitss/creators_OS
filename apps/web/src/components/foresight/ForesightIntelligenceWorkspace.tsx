'use client';

import React, { useState, useEffect } from 'react';

export function ForesightIntelligenceWorkspace() {
  const [activeTab, setActiveTab] = useState<'overview' | 'drivers' | 'trends' | 'assumptions' | 'scenarios' | 'indicators' | 'options' | 'bets' | 'red_teams' | 'nl_query'>('overview');
  const [overviewData, setOverviewData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('What could change our business in five years?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/foresight');
      if (res.ok) {
        const data = await res.json();
        setOverviewData(data);
      } else {
        // Fallback seed data
        setOverviewData({
          programsCount: 1,
          driversCount: 1,
          trendsCount: 1,
          fragileAssumptionsCount: 1,
          scenariosCount: 1,
          indicatorsCount: 1,
          optionsCount: 1,
          betsCount: 1,
          exposuresCount: 1,
          redTeamScenariosCount: 1,
          robustnessScore: 0.94,
          programs: [
            {
              id: "fprog_5yr_01",
              name: "Global 2026-2031 Enterprise AI & Compute Transformation Foresight",
              horizon: "5_year",
              scope: "global_enterprise",
              owner: "usr_chief_strategy_officer",
              status: "active"
            }
          ],
          drivers: [
            {
              id: "fdriv_01",
              type: "technology",
              driver_name: "Autonomous Agent Mesh & Real-Time Cognitive Workflow Orchestration",
              strength: "accelerating"
            }
          ],
          trends: [
            {
              id: "strnd_01",
              trend_name: "Shift from Static SaaS Subscriptions to Value-Based Autonomous Work Output Pricing",
              direction: "increasing",
              velocity: "high"
            }
          ],
          assumptions: [
            {
              id: "sassm_01",
              statement: "Primary US-East Cloud Provider inference unit costs will decay by 25% annually through 2029.",
              status: "fragile",
              confidence: "medium"
            }
          ],
          scenarios: [
            {
              id: "fscen_01",
              name: "Scenario A: Multi-Region Autonomous Agent Mesh Ubiquity (Disruption Future)",
              description: "Enterprise workflows transition 80% of routine execution to autonomous agent DAGs under centralized policy control.",
              horizon: "5_year",
              scenario_type: "disruption",
              plausibility: "high",
              status: "active"
            }
          ],
          indicators: [
            {
              id: "sind_01",
              indicator_name: "Autonomous Agent API Execution Share (% of total Enterprise Workflows)",
              baseline_val: 15.0,
              threshold_val: 45.0,
              current_val: 52.4,
              direction: "increasing"
            }
          ],
          options: [
            {
              id: "sopt_01",
              option_name: "Option 1: Deploy Multi-Cloud Fallback Router for Agent Model Inference",
              option_type: "experiment",
              reversibility: "highly_reversible",
              robustness_score: 0.94,
              status: "active"
            }
          ],
          bets: [
            {
              id: "sbet_01",
              thesis: "Invest $500k in building proprietary Enterprise Skill Fabric & Capability Registry.",
              investment_amount: 500000.0,
              status: "active"
            }
          ],
          redTeams: [
            {
              id: "ared_01",
              name: "Red-Team Stress Test: Global Transatlantic Fiber Cut & Single Cloud Blackout",
              adversarial_thesis: "Hypothetical catastrophic disruption testing multi-region failover speed and offline memory caching.",
              is_hypothetical: true,
              status: "active"
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
      const res = await fetch(`/api/v1/foresight/query?query=${encodeURIComponent(queryText)}`, {
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
            <span className="p-2 bg-indigo-600/20 text-indigo-400 rounded-lg text-lg">🔮</span>
            Enterprise Strategic Foresight & Long-Horizon Scenario Intelligence 2.0
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Long-horizon intelligence layer connecting Weak Signals → Trends → Drivers → Uncertainties → Assumptions → Plausible Scenarios → Strategic Options → Monitoring Triggers.
          </p>
        </div>
        <div className="flex gap-2">
          <span className="px-3 py-1 bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 rounded-full text-xs font-semibold">
            5-Year Strategic Horizon
          </span>
          <span className="px-3 py-1 bg-purple-500/10 text-purple-400 border border-purple-500/20 rounded-full text-xs font-semibold">
            Plausible Futures Mode
          </span>
        </div>
      </div>

      {/* Telemetry Bar */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Active Programs</div>
          <div className="text-2xl font-bold text-slate-100 mt-1">{overviewData?.programsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Future Drivers</div>
          <div className="text-2xl font-bold text-indigo-400 mt-1">{overviewData?.driversCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Fragile Assumptions</div>
          <div className="text-2xl font-bold text-rose-400 mt-1">{overviewData?.fragileAssumptionsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Plausible Scenarios</div>
          <div className="text-2xl font-bold text-purple-400 mt-1">{overviewData?.scenariosCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Reversible Options</div>
          <div className="text-2xl font-bold text-emerald-400 mt-1">{overviewData?.optionsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Strategy Robustness</div>
          <div className="text-2xl font-bold text-cyan-400 mt-1">{((overviewData?.robustnessScore || 0) * 100).toFixed(0)}%</div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 gap-2 text-sm overflow-x-auto pb-1">
        {[
          { id: 'overview', label: 'Foresight Overview' },
          { id: 'drivers', label: 'Future Drivers & Trends' },
          { id: 'assumptions', label: 'Assumptions & Fragility' },
          { id: 'scenarios', label: 'Future Scenarios' },
          { id: 'indicators', label: 'Indicators & Triggers' },
          { id: 'options', label: 'Options & Reversibility' },
          { id: 'bets', label: 'Strategic Bets & Exposure' },
          { id: 'red_teams', label: 'Red-Team Scenarios' },
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

      {/* Tab Content */}
      {loading ? (
        <div className="p-8 text-center text-slate-500">Loading Strategic Foresight state...</div>
      ) : (
        <div className="space-y-6">
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-indigo-400 flex items-center gap-2">
                  <span>🔮</span> Active Foresight Program
                </h2>
                {overviewData?.programs?.[0] && (
                  <div className="space-y-3 text-sm">
                    <div className="font-bold text-slate-100 text-base">{overviewData.programs[0].name}</div>
                    <p className="text-slate-400">{overviewData.programs[0].description}</p>
                    <div className="grid grid-cols-2 gap-2 text-xs pt-2">
                      <span className="p-2 bg-indigo-950/40 border border-indigo-800/40 rounded">Horizon: <strong className="text-indigo-300">{overviewData.programs[0].horizon}</strong></span>
                      <span className="p-2 bg-slate-800/60 rounded">Owner: <strong className="text-slate-200">{overviewData.programs[0].owner}</strong></span>
                    </div>
                  </div>
                )}
              </div>

              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-rose-400 flex items-center gap-2">
                  <span>⚠️</span> Fragile Strategic Assumption
                </h2>
                {overviewData?.assumptions?.[0] && (
                  <div className="space-y-3 text-sm">
                    <div className="font-bold text-slate-100">{overviewData.assumptions[0].statement}</div>
                    <div className="text-xs text-slate-400">Source: {overviewData.assumptions[0].source}</div>
                    <div className="p-3 bg-slate-950 rounded border border-rose-800/40 text-xs text-rose-300 flex justify-between">
                      <span>Status: <strong>{overviewData.assumptions[0].status}</strong></span>
                      <span>Confidence: {overviewData.assumptions[0].confidence}</span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'drivers' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Future Drivers & Macro Trends</h2>
              {overviewData?.drivers?.map((dr: any) => (
                <div key={dr.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-indigo-300">Driver: {dr.driver_name}</span>
                    <span className="text-xs px-2 py-0.5 bg-emerald-500/10 text-emerald-400 rounded">Strength: {dr.strength}</span>
                  </div>
                  <div className="text-xs text-slate-400">Type: {dr.type}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'assumptions' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Strategic Assumptions & Fragility Analysis</h2>
              {overviewData?.assumptions?.map((a: any) => (
                <div key={a.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-rose-500">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-slate-100">{a.statement}</span>
                    <span className="text-xs px-2 py-0.5 bg-rose-500/20 text-rose-300 rounded font-bold">{a.status}</span>
                  </div>
                  <div className="text-xs text-slate-400">Source: {a.source} | Confidence: {a.confidence}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'scenarios' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Plausible Future Scenarios</h2>
              {overviewData?.scenarios?.map((sc: any) => (
                <div key={sc.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-purple-300">{sc.name}</span>
                    <span className="text-xs px-2 py-0.5 bg-purple-500/20 text-purple-300 rounded font-bold">Plausibility: {sc.plausibility}</span>
                  </div>
                  <p className="text-xs text-slate-400">{sc.description}</p>
                  <div className="text-xs text-slate-500">Horizon: {sc.horizon} | Type: {sc.scenario_type}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'indicators' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Leading Indicators & Review Triggers</h2>
              {overviewData?.indicators?.map((ind: any) => (
                <div key={ind.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-cyan-300">{ind.indicator_name}</span>
                    <span className="text-xs px-2 py-0.5 bg-amber-500/20 text-amber-300 rounded font-bold">Threshold Breached: {ind.current_val} &gt; {ind.threshold_val}</span>
                  </div>
                  <div className="text-xs text-slate-400">Baseline: {ind.baseline_val} | Direction: {ind.direction}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'options' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Strategic Options & Reversibility Classification</h2>
              {overviewData?.options?.map((opt: any) => (
                <div key={opt.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-emerald-400">{opt.option_name}</span>
                    <span className="text-xs px-2 py-0.5 bg-emerald-500/10 text-emerald-400 rounded">Reversibility: {opt.reversibility}</span>
                  </div>
                  <div className="text-xs text-slate-400">Type: {opt.option_type} | Robustness Score: {(opt.robustness_score * 100).toFixed(0)}%</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'bets' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Strategic Bets & Portfolio Exposures</h2>
              {overviewData?.bets?.map((b: any) => (
                <div key={b.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-indigo-300">Thesis: {b.thesis}</span>
                    <span className="text-xs px-2 py-0.5 bg-indigo-500/20 text-indigo-300 rounded font-bold">${(b.investment_amount).toLocaleString()}</span>
                  </div>
                  <div className="text-xs text-slate-400">Status: {b.status}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'red_teams' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Red-Team Adversarial Scenarios (Hypothetical)</h2>
              {overviewData?.redTeams?.map((rt: any) => (
                <div key={rt.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm border-l-4 border-l-red-500">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-red-400">{rt.name}</span>
                    <span className="text-xs px-2 py-0.5 bg-red-500/20 text-red-300 rounded font-mono">HYPOTHETICAL</span>
                  </div>
                  <p className="text-xs text-slate-300">{rt.adversarial_thesis}</p>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'nl_query' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Natural Language Strategic Foresight Query Interface</h2>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={queryText}
                  onChange={(e) => setQueryText(e.target.value)}
                  placeholder="Ask a foresight query..."
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
                        <div className="font-semibold text-slate-200">{res.program_name} ({res.horizon})</div>
                        <div className="text-purple-300">Plausible Scenario: {res.plausible_scenario}</div>
                        <div className="text-rose-400">Fragile Assumption: {res.fragile_assumption}</div>
                        <div className="text-amber-300">Indicator: {res.leading_indicator}</div>
                        <div className="text-emerald-400">Robust Option: {res.robust_option}</div>
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
