'use client';

import React, { useState, useEffect } from 'react';

export function ContinuityIntelligenceWorkspace() {
  const [activeTab, setActiveTab] = useState<'overview' | 'capabilities' | 'dependencies' | 'scenarios' | 'gaps' | 'plans' | 'tests' | 'ai_vendor' | 'nl_query'>('overview');
  const [overviewData, setOverviewData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('What happens if our primary vendor fails?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/resilience');
      if (res.ok) {
        const data = await res.json();
        setOverviewData(data);
      } else {
        // Fallback seed data
        setOverviewData({
          capabilitiesCount: 1,
          dependenciesCount: 1,
          spofCount: 1,
          gapsCount: 1,
          scenariosCount: 1,
          plansCount: 1,
          stalePlansCount: 0,
          testsCount: 1,
          vendorsCount: 1,
          dataAssetsCount: 1,
          aiModelsCount: 1,
          overallReadinessScore: 0.94,
          capabilities: [
            {
              id: "cap_core_01",
              name: "Global Multi-Tenant Inference Gateway & Decision Pipeline",
              description: "Critical core service providing real-time AI model routing, policy enforcement, and execution governance.",
              owner: "usr_resilience_lead",
              criticality: "critical",
              status: "active"
            }
          ],
          dependencies: [
            {
              id: "dep_spof_01",
              capability_id: "cap_core_01",
              dependency_id: "vendor_primary_gpu_cloud",
              dependency_type: "vendor",
              criticality: "required",
              is_single_point_of_failure: true,
              has_fallback: true,
              primary_fallback: "vendor_secondary_gpu_cloud"
            }
          ],
          gaps: [
            {
              id: "gap_01",
              capability_id: "cap_core_01",
              gap_type: "redundancy",
              severity: "high",
              evidence: "Primary GPU cloud vendor lacks active-active secondary regional failover cluster.",
              owner: "usr_infra_lead",
              status: "open"
            }
          ],
          scenarios: [
            {
              id: "scen_01",
              name: "Regional Cloud Vendor Outage & Infrastructure Blackout",
              description: "Simulates complete loss of US-East GPU cluster datacenter node capacity.",
              scenario_type: "vendor_outage",
              trigger: "Fiber cut & power grid failure",
              probability_range: "[0.02, 0.08]",
              impact_summary: "High operational impact; inference requests degrade unless failover triggers.",
              cascade_depth: "multi-hop",
              status: "active"
            }
          ],
          plans: [
            {
              id: "cplan_01",
              name: "Multi-Region GPU Cloud Failover & Disaster Recovery Plan",
              description: "Automated and governed failover plan switching inference routing to EU-Central secondary cloud.",
              status: "active",
              version: 2
            }
          ],
          tests: [
            {
              id: "rtest_01",
              plan_id: "cplan_01",
              test_type: "failover",
              frequency: "quarterly",
              result: "passed"
            }
          ],
          vendors: [
            {
              id: "vprof_01",
              vendor_id: "vendor_primary_gpu_cloud",
              vendor_name: "Hyperscale Cloud GPU Provider Inc.",
              criticality: "critical",
              concentration_risk_flag: true,
              fallback_available: true
            }
          ],
          dataAssets: [
            {
              id: "dprof_01",
              data_asset_id: "db_master_postgres",
              backup_status: "healthy",
              replication_status: "active",
              rpo_minutes: 15,
              rto_minutes: 60
            }
          ],
          aiModels: [
            {
              id: "aiprof_01",
              model_id: "gemini-1.5-pro",
              provider_name: "Google Vertex AI",
              fallback_model_id: "claude-3-5-sonnet",
              human_escalation_enabled: true,
              quality_score: 0.98
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
      const res = await fetch(`/api/v1/resilience/query?query=${encodeURIComponent(queryText)}`, {
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
            <span className="p-2 bg-rose-600/20 text-rose-400 rounded-lg text-lg">🛡️</span>
            Enterprise Resilience & Continuity Intelligence 2.0
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Governed resilience layer connecting Critical Capabilities → Dependencies → Threats → Failure Scenarios → Impact → Continuity Plans → Recovery Verification.
          </p>
        </div>
        <div className="flex gap-2">
          <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full text-xs font-semibold flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            Resilience Active
          </span>
          <span className="px-3 py-1 bg-rose-500/10 text-rose-400 border border-rose-500/20 rounded-full text-xs font-semibold">
            Evidence-Backed Recovery
          </span>
        </div>
      </div>

      {/* Telemetry Bar */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Critical Capabilities</div>
          <div className="text-2xl font-bold text-slate-100 mt-1">{overviewData?.capabilitiesCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Active SPOFs</div>
          <div className="text-2xl font-bold text-red-400 mt-1">{overviewData?.spofCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Resilience Gaps</div>
          <div className="text-2xl font-bold text-amber-400 mt-1">{overviewData?.gapsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Continuity Plans</div>
          <div className="text-2xl font-bold text-indigo-400 mt-1">{overviewData?.plansCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Verified Tests</div>
          <div className="text-2xl font-bold text-emerald-400 mt-1">{overviewData?.testsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Readiness Score</div>
          <div className="text-2xl font-bold text-cyan-400 mt-1">{((overviewData?.overallReadinessScore || 0) * 100).toFixed(0)}%</div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 gap-2 text-sm overflow-x-auto pb-1">
        {[
          { id: 'overview', label: 'Resilience Overview' },
          { id: 'capabilities', label: 'Critical Capabilities' },
          { id: 'dependencies', label: 'Dependencies & SPOFs' },
          { id: 'scenarios', label: 'Failure Scenarios' },
          { id: 'gaps', label: 'Resilience Gaps' },
          { id: 'plans', label: 'Continuity Plans' },
          { id: 'tests', label: 'Recovery Tests' },
          { id: 'ai_vendor', label: 'Vendor, Data & AI Resilience' },
          { id: 'nl_query', label: 'Natural Language Query' }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-2 font-medium rounded-t-lg transition-colors whitespace-nowrap ${
              activeTab === tab.id
                ? 'bg-slate-900 text-rose-400 border-b-2 border-rose-500'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/40'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      {loading ? (
        <div className="p-8 text-center text-slate-500">Loading Enterprise Resilience state...</div>
      ) : (
        <div className="space-y-6">
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-rose-400 flex items-center gap-2">
                  <span>🛡️</span> Critical Capability & Impact
                </h2>
                {overviewData?.capabilities?.[0] && (
                  <div className="space-y-3 text-sm">
                    <div className="font-medium text-slate-200">{overviewData.capabilities[0].name}</div>
                    <p className="text-slate-400">{overviewData.capabilities[0].description}</p>
                    <div className="grid grid-cols-2 gap-2 text-xs pt-2">
                      <span className="p-2 bg-slate-800/60 rounded">Criticality: <strong className="text-red-400">{overviewData.capabilities[0].criticality}</strong></span>
                      <span className="p-2 bg-slate-800/60 rounded">Owner: <strong className="text-slate-300">{overviewData.capabilities[0].owner}</strong></span>
                    </div>
                  </div>
                )}
              </div>

              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-amber-400 flex items-center gap-2">
                  <span>⚠️</span> Single Point of Failure (SPOF) Alert
                </h2>
                {overviewData?.dependencies?.[0] && (
                  <div className="space-y-3 text-sm">
                    <div className="text-slate-300 font-semibold">SPOF Dependency: {overviewData.dependencies[0].dependency_id}</div>
                    <div className="p-3 bg-red-950/30 border border-red-800/40 rounded-lg text-red-300 text-xs">
                      Dependency lacks active redundancy. Primary fallback: {overviewData.dependencies[0].primary_fallback}.
                    </div>
                    <div className="text-xs text-slate-400">
                      Criticality: <span className="text-slate-200 font-semibold">{overviewData.dependencies[0].criticality}</span> | Has Fallback: <span className="text-emerald-400 font-semibold">YES</span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'capabilities' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Registered Critical Capabilities</h2>
              <div className="divide-y divide-slate-800">
                {overviewData?.capabilities?.map((c: any) => (
                  <div key={c.id} className="py-4 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="font-semibold text-rose-300">{c.name}</span>
                      <span className="px-2 py-1 bg-red-500/10 text-red-400 text-xs rounded font-mono">{c.criticality}</span>
                    </div>
                    <p className="text-sm text-slate-400">{c.description}</p>
                    <div className="text-xs text-slate-500">Owner: {c.owner} | Status: {c.status}</div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'dependencies' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Capability Dependencies & Single Points of Failure</h2>
              {overviewData?.dependencies?.map((d: any) => (
                <div key={d.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-indigo-300">Dependency ID: {d.dependency_id}</span>
                    <span className={`text-xs px-2 py-0.5 rounded ${d.is_single_point_of_failure ? 'bg-red-500/20 text-red-400 font-bold' : 'bg-emerald-500/10 text-emerald-400'}`}>
                      {d.is_single_point_of_failure ? 'SPOF DETECTED' : 'REDUNDANT'}
                    </span>
                  </div>
                  <div className="grid grid-cols-3 gap-2 text-xs text-slate-400 pt-1">
                    <span>Type: <strong className="text-slate-200">{d.dependency_type}</strong></span>
                    <span>Criticality: <strong className="text-slate-200">{d.criticality}</strong></span>
                    <span>Fallback: <strong className="text-emerald-400">{d.primary_fallback}</strong></span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'scenarios' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Failure Scenarios & Cascading Impact Analysis</h2>
              {overviewData?.scenarios?.map((s: any) => (
                <div key={s.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-amber-300">{s.name}</span>
                    <span className="text-xs px-2 py-0.5 bg-slate-800 text-slate-300 rounded font-mono">{s.scenario_type}</span>
                  </div>
                  <p className="text-slate-400 text-xs">{s.description}</p>
                  <div className="p-3 bg-slate-900 rounded text-xs text-slate-300 space-y-1">
                    <div><strong>Trigger:</strong> {s.trigger}</div>
                    <div><strong>Cascade Depth:</strong> {s.cascade_depth}</div>
                    <div><strong>Impact Summary:</strong> {s.impact_summary}</div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'gaps' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Identified Resilience Gaps</h2>
              {overviewData?.gaps?.map((g: any) => (
                <div key={g.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-amber-400">Gap Type: {g.gap_type}</span>
                    <span className="text-xs px-2 py-0.5 bg-red-500/10 text-red-400 rounded">Severity: {g.severity}</span>
                  </div>
                  <p className="text-slate-300">{g.evidence}</p>
                  <div className="text-xs text-slate-500">Owner: {g.owner} | Status: {g.status}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'plans' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Business Continuity Plans</h2>
              {overviewData?.plans?.map((p: any) => (
                <div key={p.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-emerald-400">{p.name} (v{p.version})</span>
                    <span className="text-xs px-2 py-0.5 bg-indigo-500/10 text-indigo-400 rounded">{p.status}</span>
                  </div>
                  <p className="text-slate-400 text-xs">{p.description}</p>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'tests' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Recovery Verification & Resilience Tests</h2>
              {overviewData?.tests?.map((t: any) => (
                <div key={t.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-cyan-300">Test ID: {t.id}</span>
                    <span className="text-xs px-2 py-0.5 bg-emerald-500/10 text-emerald-400 rounded">{t.result}</span>
                  </div>
                  <div className="text-xs text-slate-400">Test Type: {t.test_type} | Frequency: {t.frequency}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'ai_vendor' && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-3">
                <h3 className="text-md font-semibold text-purple-400">Vendor Resilience</h3>
                {overviewData?.vendors?.map((v: any) => (
                  <div key={v.id} className="p-3 bg-slate-950 rounded text-xs space-y-1">
                    <div className="font-semibold text-slate-200">{v.vendor_name}</div>
                    <div className="text-amber-400">Concentration Risk: {v.concentration_risk_flag ? 'YES' : 'NO'}</div>
                  </div>
                ))}
              </div>

              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-3">
                <h3 className="text-md font-semibold text-cyan-400">Data Resilience</h3>
                {overviewData?.dataAssets?.map((d: any) => (
                  <div key={d.id} className="p-3 bg-slate-950 rounded text-xs space-y-1">
                    <div className="font-semibold text-slate-200">{d.data_asset_id}</div>
                    <div className="text-emerald-400">RPO: {d.rpo_minutes}m | RTO: {d.rto_minutes}m</div>
                  </div>
                ))}
              </div>

              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-3">
                <h3 className="text-md font-semibold text-emerald-400">AI Model Resilience</h3>
                {overviewData?.aiModels?.map((m: any) => (
                  <div key={m.id} className="p-3 bg-slate-950 rounded text-xs space-y-1">
                    <div className="font-semibold text-slate-200">{m.model_id} ({m.provider_name})</div>
                    <div className="text-slate-400">Fallback Model: {m.fallback_model_id}</div>
                    <div className="text-emerald-400">Human Escalation: {m.human_escalation_enabled ? 'ENABLED' : 'DISABLED'}</div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'nl_query' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Natural Language Resilience Query Interface</h2>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={queryText}
                  onChange={(e) => setQueryText(e.target.value)}
                  placeholder="Ask a resilience query..."
                  className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-sm text-slate-100 focus:outline-none focus:border-rose-500"
                />
                <button
                  onClick={handleQuery}
                  disabled={queryLoading}
                  className="px-5 py-2 bg-rose-600 hover:bg-rose-500 text-white font-medium rounded-lg text-sm transition-colors"
                >
                  {queryLoading ? 'Evaluating...' : 'Query'}
                </button>
              </div>

              {queryResult && (
                <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                  <div className="text-xs text-rose-400 font-semibold">Query: {queryResult.query}</div>
                  <div className="space-y-2">
                    {queryResult.results?.map((res: any, idx: number) => (
                      <div key={idx} className="p-3 bg-slate-900 rounded space-y-1 text-xs">
                        <div className="font-semibold text-slate-200">{res.capability}</div>
                        <div className="text-red-400">SPOF: {res.single_point_of_failure}</div>
                        <div className="text-amber-300">Resilience Gap: {res.resilience_gap}</div>
                        <div className="text-emerald-400">AI Fallback: {res.ai_fallback}</div>
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
