'use client';

import React, { useState, useEffect } from 'react';

export function CrisisIntelligenceWorkspace() {
  const [activeTab, setActiveTab] = useState<'overview' | 'crises' | 'signals' | 'impact' | 'command' | 'options' | 'communications' | 'timeline' | 'drills' | 'nl_query'>('overview');
  const [overviewData, setOverviewData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('What is happening right now?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/crisis');
      if (res.ok) {
        const data = await res.json();
        setOverviewData(data);
      } else {
        // Fallback seed data
        setOverviewData({
          crisesCount: 1,
          activeCrisesCount: 1,
          signalsCount: 1,
          impactsCount: 1,
          commandsCount: 1,
          optionsCount: 1,
          commsCount: 1,
          timelineEventsCount: 1,
          drillsCount: 1,
          readinessScore: 0.96,
          crises: [
            {
              id: "crs_sev1_01",
              name: "Global Multi-Tenant Inference Datacenter Outage",
              description: "SEV1 major incident impacting primary US-East GPU inference cluster and real-time model routing.",
              status: "active",
              severity: "SEV1",
              declared_by: "usr_crisis_commander_lead",
              commander_id: "usr_crisis_commander_lead"
            }
          ],
          declarations: [
            {
              id: "cdec_01",
              crisis_id: "crs_sev1_01",
              trigger: "Prometheus metric breach: P99 inference latency > 5000ms & 35% error rate",
              evidence: "Observed 35,000 dropped tokens/sec across primary US-East datacenter.",
              criteria: "SEV1 Declaration Policy: >25% customer degradation",
              authorized_actor: "usr_crisis_commander_lead"
            }
          ],
          signals: [
            {
              id: "csig_01",
              crisis_id: "crs_sev1_01",
              signal_type: "vendor_outage",
              confidence: "high",
              source: "AWS Datacenter Health API"
            }
          ],
          impacts: [
            {
              id: "cimp_01",
              crisis_id: "crs_sev1_01",
              capabilities_impact_json: ["cap_core_01 (Global Multi-Tenant Inference Gateway)"],
              services_impact_json: ["svc_model_router", "svc_policy_evaluator"],
              customers_impact_json: { affected_tenants: 420, tier_1_enterprise: 18 },
              impact_status: "confirmed",
              evidence: "Verified via real-time telemetry mesh and active health probes."
            }
          ],
          commands: [
            {
              id: "cmd_01",
              crisis_id: "crs_sev1_01",
              incident_commander: "usr_crisis_commander_lead",
              operations_lead: "usr_ops_lead",
              technical_lead: "usr_tech_lead",
              security_lead: "usr_sec_lead",
              communications_lead: "usr_comms_lead"
            }
          ],
          options: [
            {
              id: "cropt_01",
              crisis_id: "crs_sev1_01",
              name: "Option 1: Failover Inference Traffic to EU-Central Secondary GPU Cluster",
              expected_impact: "Restores 98% inference throughput within 25 minutes.",
              cost_estimate: 15000.0,
              risk_level: "low",
              recovery_time_min: 25,
              confidence: "high"
            }
          ],
          comms: [
            {
              id: "ccomm_01",
              crisis_id: "crs_sev1_01",
              audience: "executive",
              message: "SEV1 Crisis Declared: Global Multi-Tenant Inference Gateway degraded. Secondary cluster failover initiated.",
              channel: "Slack #crisis-command",
              sender: "usr_comms_lead",
              approval_status: "approved"
            }
          ],
          timeline: [
            {
              id: "ctime_01",
              crisis_id: "crs_sev1_01",
              actor: "usr_crisis_commander_lead",
              event_type: "crisis_declared",
              description: "Crisis SEV1 officially declared. Incident Command activated.",
              evidence: "Declaration criterion verified against SEV1 threshold."
            }
          ],
          drills: [
            {
              id: "hdrill_01",
              name: "Quarterly Regional Cloud Blackout Tabletop & Failover Drill",
              scenario_type: "vendor_outage",
              status: "passed"
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
      const res = await fetch(`/api/v1/crisis/query?query=${encodeURIComponent(queryText)}`, {
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
            <span className="p-2 bg-red-600/20 text-red-400 rounded-lg text-lg">🚨</span>
            Enterprise Crisis Intelligence & Coordinated Response 2.0
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Governed crisis operating layer connecting Signal → Detection → Declaration → Impact Map → Command Structure → Response Options → Approval → Coordinated Action → Communication → Recovery Verification.
          </p>
        </div>
        <div className="flex gap-2">
          <span className="px-3 py-1 bg-red-500/10 text-red-400 border border-red-500/20 rounded-full text-xs font-semibold flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-red-500 animate-ping"></span>
            SEV1 Active Crisis
          </span>
          <span className="px-3 py-1 bg-amber-500/10 text-amber-400 border border-amber-500/20 rounded-full text-xs font-semibold">
            Human Command Authorized
          </span>
        </div>
      </div>

      {/* Telemetry Bar */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Active Crises</div>
          <div className="text-2xl font-bold text-red-400 mt-1">{overviewData?.activeCrisesCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Ingested Signals</div>
          <div className="text-2xl font-bold text-amber-400 mt-1">{overviewData?.signalsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Confirmed Impacts</div>
          <div className="text-2xl font-bold text-rose-400 mt-1">{overviewData?.impactsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Command Roles</div>
          <div className="text-2xl font-bold text-indigo-400 mt-1">7 Active</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Approved Comms</div>
          <div className="text-2xl font-bold text-emerald-400 mt-1">{overviewData?.commsCount || 0}</div>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
          <div className="text-xs text-slate-400 font-medium">Crisis Readiness</div>
          <div className="text-2xl font-bold text-cyan-400 mt-1">{((overviewData?.readinessScore || 0) * 100).toFixed(0)}%</div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 gap-2 text-sm overflow-x-auto pb-1">
        {[
          { id: 'overview', label: 'Crisis Overview' },
          { id: 'crises', label: 'Active Crises & Severity' },
          { id: 'signals', label: 'Crisis Signals' },
          { id: 'impact', label: 'Impact & Cascade Map' },
          { id: 'command', label: 'Command Structure & Roles' },
          { id: 'options', label: 'Response Options' },
          { id: 'communications', label: 'Crisis Communications' },
          { id: 'timeline', label: 'Immutable Timeline' },
          { id: 'drills', label: 'Drills & Readiness' },
          { id: 'nl_query', label: 'Natural Language Query' }
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

      {/* Tab Content */}
      {loading ? (
        <div className="p-8 text-center text-slate-500">Loading Crisis Operations state...</div>
      ) : (
        <div className="space-y-6">
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-red-400 flex items-center gap-2">
                  <span>🚨</span> Declared Major Crisis
                </h2>
                {overviewData?.crises?.[0] && (
                  <div className="space-y-3 text-sm">
                    <div className="font-bold text-slate-100 text-base">{overviewData.crises[0].name}</div>
                    <p className="text-slate-400">{overviewData.crises[0].description}</p>
                    <div className="grid grid-cols-2 gap-2 text-xs pt-2">
                      <span className="p-2 bg-red-950/40 border border-red-800/40 rounded">Severity: <strong className="text-red-400">{overviewData.crises[0].severity}</strong></span>
                      <span className="p-2 bg-slate-800/60 rounded">Commander: <strong className="text-slate-200">{overviewData.crises[0].commander_id}</strong></span>
                    </div>
                  </div>
                )}
              </div>

              <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
                <h2 className="text-lg font-semibold text-indigo-400 flex items-center gap-2">
                  <span>👨‍💼</span> Active Incident Command
                </h2>
                {overviewData?.commands?.[0] && (
                  <div className="space-y-2 text-xs divide-y divide-slate-800">
                    <div className="pt-2 flex justify-between"><span className="text-slate-400">Incident Commander:</span><strong className="text-slate-200">{overviewData.commands[0].incident_commander}</strong></div>
                    <div className="pt-2 flex justify-between"><span className="text-slate-400">Operations Lead:</span><strong className="text-slate-200">{overviewData.commands[0].operations_lead}</strong></div>
                    <div className="pt-2 flex justify-between"><span className="text-slate-400">Technical Lead:</span><strong className="text-slate-200">{overviewData.commands[0].technical_lead}</strong></div>
                    <div className="pt-2 flex justify-between"><span className="text-slate-400">Security Lead:</span><strong className="text-slate-200">{overviewData.commands[0].security_lead}</strong></div>
                    <div className="pt-2 flex justify-between"><span className="text-slate-400">Communications Lead:</span><strong className="text-slate-200">{overviewData.commands[0].communications_lead}</strong></div>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'crises' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Active Crises & Declaration Governance</h2>
              <div className="divide-y divide-slate-800">
                {overviewData?.crises?.map((c: any) => (
                  <div key={c.id} className="py-4 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="font-bold text-red-400">{c.name}</span>
                      <span className="px-3 py-1 bg-red-500/20 text-red-300 font-mono text-xs rounded font-bold">{c.severity}</span>
                    </div>
                    <p className="text-sm text-slate-400">{c.description}</p>
                    <div className="text-xs text-slate-500">Declared By: {c.declared_by} | Commander: {c.commander_id} | Status: {c.status}</div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'signals' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Ingested Crisis Signals</h2>
              {overviewData?.signals?.map((sig: any) => (
                <div key={sig.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-amber-300">Signal: {sig.signal_type}</span>
                    <span className="text-xs px-2 py-0.5 bg-emerald-500/10 text-emerald-400 rounded">Confidence: {sig.confidence}</span>
                  </div>
                  <div className="text-xs text-slate-400">Source: {sig.source} | Version: {sig.source_version}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'impact' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Confirmed Impact & Operating Graph Cascade Map</h2>
              {overviewData?.impacts?.map((imp: any) => (
                <div key={imp.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-rose-300">Impact Status: {imp.impact_status}</span>
                    <span className="text-xs text-slate-400">Evidence verified</span>
                  </div>
                  <p className="text-xs text-slate-300">{imp.evidence}</p>
                  <div className="p-3 bg-slate-900 rounded text-xs text-slate-400 space-y-1">
                    <div><strong>Capabilities Impacted:</strong> {JSON.stringify(imp.capabilities_impact_json)}</div>
                    <div><strong>Services Impacted:</strong> {JSON.stringify(imp.services_impact_json)}</div>
                    <div><strong>Customers Impacted:</strong> {JSON.stringify(imp.customers_impact_json)}</div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'command' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Incident Command Structure & Roles</h2>
              {overviewData?.commands?.map((cmd: any) => (
                <div key={cmd.id} className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                  <div className="p-3 bg-slate-950 border border-slate-800 rounded"><strong>Incident Commander:</strong> {cmd.incident_commander}</div>
                  <div className="p-3 bg-slate-950 border border-slate-800 rounded"><strong>Operations Lead:</strong> {cmd.operations_lead}</div>
                  <div className="p-3 bg-slate-950 border border-slate-800 rounded"><strong>Technical Lead:</strong> {cmd.technical_lead}</div>
                  <div className="p-3 bg-slate-950 border border-slate-800 rounded"><strong>Security Lead:</strong> {cmd.security_lead}</div>
                  <div className="p-3 bg-slate-950 border border-slate-800 rounded"><strong>Communications Lead:</strong> {cmd.communications_lead}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'options' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Evaluated Response Options</h2>
              {overviewData?.options?.map((opt: any) => (
                <div key={opt.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-emerald-400">{opt.name}</span>
                    <span className="text-xs px-2 py-0.5 bg-indigo-500/10 text-indigo-400 rounded">RTO: {opt.recovery_time_min}m</span>
                  </div>
                  <p className="text-xs text-slate-300">{opt.expected_impact}</p>
                  <div className="text-xs text-slate-500">Cost: ${opt.cost_estimate} | Risk: {opt.risk_level} | Confidence: {opt.confidence}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'communications' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Crisis Communications (DLP & Policy Enforced)</h2>
              {overviewData?.comms?.map((co: any) => (
                <div key={co.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-indigo-300">Audience: {co.audience}</span>
                    <span className="text-xs px-2 py-0.5 bg-emerald-500/10 text-emerald-400 rounded">{co.approval_status}</span>
                  </div>
                  <p className="text-xs text-slate-300 font-mono bg-slate-900 p-3 rounded">{co.message}</p>
                  <div className="text-xs text-slate-500">Channel: {co.channel} | Sender: {co.sender}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'timeline' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Immutable Crisis Timeline</h2>
              {overviewData?.timeline?.map((t: any) => (
                <div key={t.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-1 text-sm border-l-4 border-l-red-500">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-slate-200">{t.event_type}</span>
                    <span className="text-xs text-slate-500">{t.timestamp}</span>
                  </div>
                  <p className="text-xs text-slate-300">{t.description}</p>
                  <div className="text-xs text-slate-500">Actor: {t.actor} | Evidence: {t.evidence}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'drills' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Crisis Drills & Command Readiness</h2>
              {overviewData?.drills?.map((dr: any) => (
                <div key={dr.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-cyan-300">{dr.name}</span>
                    <span className="text-xs px-2 py-0.5 bg-emerald-500/10 text-emerald-400 rounded">{dr.status}</span>
                  </div>
                  <div className="text-xs text-slate-400">Scenario: {dr.scenario_type}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'nl_query' && (
            <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
              <h2 className="text-lg font-semibold text-slate-200">Natural Language Crisis Query Interface</h2>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={queryText}
                  onChange={(e) => setQueryText(e.target.value)}
                  placeholder="Ask a crisis query..."
                  className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-sm text-slate-100 focus:outline-none focus:border-red-500"
                />
                <button
                  onClick={handleQuery}
                  disabled={queryLoading}
                  className="px-5 py-2 bg-red-600 hover:bg-red-500 text-white font-medium rounded-lg text-sm transition-colors"
                >
                  {queryLoading ? 'Evaluating...' : 'Query'}
                </button>
              </div>

              {queryResult && (
                <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-sm">
                  <div className="text-xs text-red-400 font-semibold">Query: {queryResult.query}</div>
                  <div className="space-y-2">
                    {queryResult.results?.map((res: any, idx: number) => (
                      <div key={idx} className="p-3 bg-slate-900 rounded space-y-1 text-xs">
                        <div className="font-semibold text-slate-200">{res.crisis_name} ({res.severity})</div>
                        <div className="text-red-400">Commander: {res.incident_commander}</div>
                        <div className="text-amber-300">Affected Capability: {res.affected_capability}</div>
                        <div className="text-emerald-400">Response: {res.active_response_option}</div>
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
