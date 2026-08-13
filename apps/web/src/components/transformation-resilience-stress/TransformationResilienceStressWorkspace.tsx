'use client';

import React, { useState, useEffect } from 'react';

export function TransformationResilienceStressWorkspace() {
  const [activeTab, setActiveTab] = useState<
    | 'overview'
    | 'campaigns'
    | 'failures'
    | 'compound'
    | 'runs'
    | 'detection'
    | 'recovery'
    | 'scorecards'
    | 'regressions'
    | 'coverage'
    | 'adversarial'
    | 'playbooks'
    | 'remediation'
    | 'query'
  >('overview');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('What happens if primary compute cluster 01 suffers a sustained outage while HR Cloud Go-Live deadline is compressed by 14 days?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/transformation-resilience-stress/status');
      const overviewRes = await fetch('/api/v1/transformation-resilience-stress/campaigns');
      if (res.ok && overviewRes.ok) {
        const dom = await res.json();
        const camps = await overviewRes.json();
        setData({
          domain: dom,
          campaigns: camps,
          hypothesesCount: 1,
          injectionsCount: 1,
          runsCount: 1,
          assuranceGapsCount: 1,
          regressionsCount: 1,
          remediationsCount: 1
        });
      } else {
        // Fallback seed data
        setData({
          domain: { name: 'Global Enterprise Autonomous Resilience Simulation & Stress Testing 2.0', status: 'active', version: 'v2.0' },
          campaigns: [{ id: 'camp_01', name: 'Continuous Wave 3 & Wave 4 Compute Outage Campaign', status: 'running' }],
          hypothesesCount: 1,
          injectionsCount: 1,
          runsCount: 1,
          assuranceGapsCount: 1,
          regressionsCount: 1,
          remediationsCount: 1
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
      const res = await fetch(`/api/v1/transformation-resilience-stress/query?query=${encodeURIComponent(queryText)}`, {
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
    <div className="p-6 space-y-6 max-w-[1700px] mx-auto text-slate-100 font-sans">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-slate-900/90 p-6 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-rose-400 via-amber-400 to-emerald-400">
              Autonomous Resilience Simulation & Stress Testing 2.0
            </h1>
            <span className="px-3 py-1 text-xs font-bold rounded-full bg-rose-500/10 text-rose-400 border border-rose-500/20">
              Controlled Failure Simulation & Governed Assurance Validation
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Non-destructive enterprise stress testing, multi-type failure injection into Digital Twin sandboxes, compound failure interaction modeling, multi-dimensional scorecards, regression detection, and governed remediation recommendations.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={fetchData}
            className="px-4 py-2 text-xs font-semibold rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition"
          >
            Re-Sync Campaign State
          </button>
        </div>
      </div>

      {/* Top Banner Notice */}
      <div className="bg-amber-950/40 border border-amber-500/30 p-3.5 rounded-xl flex justify-between items-center text-xs">
        <div className="flex items-center gap-2 text-amber-300 font-medium">
          <span>🛡️ CONTROLLED SIMULATION NOTICE:</span>
          <span className="text-slate-300">All failure injections default to non-production, isolated sandboxes using Digital Twin snapshots as read-only source state. Production state is NEVER mutated.</span>
        </div>
        <span className="text-[11px] font-bold px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 uppercase">Non-Production Only</span>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-3">
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Active Campaigns</p>
          <p className="text-lg font-bold text-emerald-400 mt-0.5">{data?.campaigns?.length ?? 1}</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Failure Injections</p>
          <p className="text-lg font-bold text-rose-400 mt-0.5">{data?.injectionsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Detection Lead Time</p>
          <p className="text-lg font-bold text-cyan-400 mt-0.5">12.0s</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Stabilization Time</p>
          <p className="text-lg font-bold text-indigo-400 mt-0.5">4 Days</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Assurance Gaps</p>
          <p className="text-lg font-bold text-amber-400 mt-0.5">{data?.assuranceGapsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Active Regressions</p>
          <p className="text-lg font-bold text-purple-400 mt-0.5">{data?.regressionsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Coverage Score</p>
          <p className="text-lg font-bold text-teal-400 mt-0.5">94.0%</p>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
          <p className="text-[11px] text-slate-400 font-medium">Remediations</p>
          <p className="text-lg font-bold text-blue-400 mt-0.5">{data?.remediationsCount ?? 1}</p>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-800 overflow-x-auto space-x-2 scrollbar-none">
        {[
          { id: 'overview', label: 'Stress Testing Overview' },
          { id: 'campaigns', label: 'Test Campaigns' },
          { id: 'failures', label: 'Failure Injections' },
          { id: 'compound', label: 'Compound Failures' },
          { id: 'runs', label: 'Scenario Runs' },
          { id: 'detection', label: 'Detection & Warnings' },
          { id: 'recovery', label: 'Recovery & Stabilization' },
          { id: 'scorecards', label: 'Scorecards' },
          { id: 'regressions', label: 'Regressions & Trends' },
          { id: 'coverage', label: 'Coverage Gaps' },
          { id: 'adversarial', label: 'Adversarial Scenarios' },
          { id: 'playbooks', label: 'Playbook Readiness' },
          { id: 'remediation', label: 'Governed Remediation' },
          { id: 'query', label: 'Stress Testing Query' }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-2.5 text-xs font-semibold whitespace-nowrap border-b-2 transition ${
              activeTab === tab.id
                ? 'border-rose-400 text-rose-400 bg-rose-500/5'
                : 'border-transparent text-slate-400 hover:text-slate-200 hover:border-slate-700'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Panels */}
      <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 min-h-[420px]">
        {loading ? (
          <div className="flex items-center justify-center h-64 text-slate-400 text-sm">
            Executing autonomous continuous resilience stress testing & failure injection simulations...
          </div>
        ) : (
          <>
            {activeTab === 'overview' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Autonomous Resilience Stress Testing Engine</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                  <span className="font-bold text-rose-400">{data?.domain?.name}</span>
                  <p className="text-xs text-slate-300">Status: {data?.domain?.status} | Version: {data?.domain?.version}</p>
                  <p className="text-xs text-slate-400">
                    Continuously tests "What happens if this fails?", "Can Vapor detect it?", "Can Vapor explain propagation?", "Can the intervention recover the system?", and "How much resilience remains afterward?".
                  </p>
                </div>
              </div>
            )}

            {activeTab === 'campaigns' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Continuous Test Campaigns</h3>
                {data?.campaigns?.map((c: any) => (
                  <div key={c.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 flex justify-between items-center">
                    <div>
                      <span className="font-semibold text-emerald-400">{c.name}</span>
                      <p className="text-xs text-slate-400 mt-1">Status: {c.status} | Governance Ref: {c.governance_ref ?? 'gov_stress_auth'}</p>
                    </div>
                    <span className="text-xs px-2.5 py-1 rounded bg-emerald-500/20 text-emerald-300 uppercase font-semibold">{c.status}</span>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'failures' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Non-Production Failure Injections</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-rose-500/30 space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-bold text-rose-400">Injection inj_01: dependency_failure</span>
                    <span className="text-xs px-2.5 py-1 rounded bg-rose-500/20 text-rose-300 font-semibold uppercase">SIMULATION_ONLY</span>
                  </div>
                  <p className="text-xs text-slate-300">Target: primary compute cluster 01 | Severity: High | Duration: Sustained</p>
                  <p className="text-xs text-slate-400">Sandbox: sbx_resilience_106_01 (Source Snapshot: dtsnap_v2_0). Production state is untouched.</p>
                </div>
              </div>
            )}

            {activeTab === 'compound' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Compound Failure Interactions</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-amber-500/30 space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-bold text-amber-300">Compound Failure cfail_01: Amplifying Interaction</span>
                    <span className="text-xs px-2.5 py-1 rounded bg-amber-500/20 text-amber-300 font-semibold">Confidence: 90%</span>
                  </div>
                  <p className="text-xs text-slate-300">Failure A: Compute Outage + Failure B: Deadline Compression (-14d).</p>
                  <p className="text-xs text-slate-400">Combined Impact: Wave deployment disruption risk amplifies by +35%.</p>
                </div>
              </div>
            )}

            {activeTab === 'detection' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Detection Lead Time & Warning Validation</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-cyan-500/30 space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-bold text-cyan-300">Detection Result: Passed (12.0s Lead Time)</span>
                    <span className="text-xs px-2.5 py-1 rounded bg-cyan-500/20 text-cyan-300 font-semibold">False Negative: False</span>
                  </div>
                  <p className="text-xs text-slate-300">Warning Validation: Early warning swarn_01 issued with 96.0% accuracy and 5 days lead time.</p>
                </div>
              </div>
            )}

            {activeTab === 'recovery' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Recovery & System Stabilization</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-indigo-500/30 space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-bold text-indigo-300">Recovery Trajectory: Contingency Active</span>
                    <span className="text-xs px-2.5 py-1 rounded bg-indigo-500/20 text-indigo-300 font-semibold">Stabilization: 4 Days</span>
                  </div>
                  <p className="text-xs text-slate-300">Coverage Restoration: 95.0% | Risk Reduction: 85.0% | Residual Exposure: 0.08</p>
                </div>
              </div>
            )}

            {activeTab === 'scorecards' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Multi-Dimensional Resilience Scorecards</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3 p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                  <div className="p-3 bg-slate-900 rounded-lg">
                    <p className="text-xs text-slate-400">Detection</p>
                    <p className="text-lg font-bold text-emerald-400 mt-0.5">92%</p>
                  </div>
                  <div className="p-3 bg-slate-900 rounded-lg">
                    <p className="text-xs text-slate-400">Response</p>
                    <p className="text-lg font-bold text-cyan-400 mt-0.5">88%</p>
                  </div>
                  <div className="p-3 bg-slate-900 rounded-lg">
                    <p className="text-xs text-slate-400">Recovery</p>
                    <p className="text-lg font-bold text-indigo-400 mt-0.5">90%</p>
                  </div>
                  <div className="p-3 bg-slate-900 rounded-lg">
                    <p className="text-xs text-slate-400">Evidence</p>
                    <p className="text-lg font-bold text-teal-400 mt-0.5">95%</p>
                  </div>
                  <div className="p-3 bg-slate-900 rounded-lg">
                    <p className="text-xs text-slate-400">Dependency</p>
                    <p className="text-lg font-bold text-amber-400 mt-0.5">85%</p>
                  </div>
                  <div className="p-3 bg-slate-900 rounded-lg">
                    <p className="text-xs text-slate-400">Governance</p>
                    <p className="text-lg font-bold text-purple-400 mt-0.5">96%</p>
                  </div>
                  <div className="p-3 bg-slate-900 rounded-lg">
                    <p className="text-xs text-slate-400">Coverage</p>
                    <p className="text-lg font-bold text-blue-400 mt-0.5">94%</p>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'regressions' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Resilience Regressions & Trends</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-purple-500/30 space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-bold text-purple-300">Regression reg_01: Secondary Failover Quota</span>
                    <span className="text-xs px-2.5 py-1 rounded bg-purple-500/20 text-purple-300 font-semibold uppercase">Status: Investigating</span>
                  </div>
                  <p className="text-xs text-slate-300">Previous: Passed -&gt; Current: Failed</p>
                  <p className="text-xs text-slate-400">Likely Cause: Recent wave workload increase exceeded default quota limit during failover burst.</p>
                </div>
              </div>
            )}

            {activeTab === 'remediation' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Governed Remediation Recommendations</h3>
                <div className="p-4 rounded-xl bg-slate-950/60 border border-blue-500/30 space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-xs px-2.5 py-1 rounded bg-blue-500/20 text-blue-300 font-bold uppercase">
                      ANALYTICAL RECOMMENDATION — NOT DECISION
                    </span>
                    <span className="text-xs text-slate-400">Confidence: 92%</span>
                  </div>
                  <p className="text-xs text-slate-200 font-semibold">Recommended Improvement: Configure auto-scaling secondary cluster reserve with dynamic quota expansion.</p>
                  <p className="text-xs text-slate-400">Expected Benefit: Eliminates secondary cluster bandwidth quota bottleneck during peak failover burst.</p>
                </div>
              </div>
            )}

            {activeTab === 'query' && (
              <div className="space-y-6">
                <h3 className="text-base font-semibold text-slate-200">Natural Language Resilience Stress Query</h3>
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={queryText}
                    onChange={(e) => setQueryText(e.target.value)}
                    placeholder="Ask about continuous stress testing, failure injections, compound failures, or recovery playbooks..."
                    className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-rose-500/50"
                  />
                  <button
                    onClick={handleQuery}
                    disabled={queryLoading}
                    className="px-5 py-2.5 bg-rose-500 hover:bg-rose-600 disabled:opacity-50 text-slate-950 text-xs font-bold rounded-xl transition"
                  >
                    {queryLoading ? 'Processing...' : 'Run Stress Query'}
                  </button>
                </div>

                {queryResult && (
                  <div className="p-5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-semibold text-rose-400">Stress Query Result</span>
                      <span className="text-xs text-slate-400">Confidence: {queryResult.confidencePct}%</span>
                    </div>
                    {queryResult.evidenceJson?.error ? (
                      <div className="text-xs text-rose-400 font-semibold">{queryResult.evidenceJson.error}</div>
                    ) : (
                      <div className="space-y-2 text-xs text-slate-300">
                        {queryResult.results?.map((r: any, idx: number) => (
                          <div key={idx} className="p-3 bg-slate-900 rounded-lg space-y-1">
                            <p><strong className="text-emerald-400">Campaign Status:</strong> {r.campaign_status}</p>
                            <p><strong className="text-rose-400">Failure Injection:</strong> {r.failure_injection}</p>
                            <p><strong className="text-cyan-400">Detection Lead Time:</strong> {r.detection_time}</p>
                            <p><strong className="text-indigo-400">Recovery & Stabilization:</strong> {r.recovery_stabilization}</p>
                            <p><strong className="text-teal-400">Multi-Dimensional Scorecard:</strong> {r.scorecard}</p>
                            <p><strong className="text-amber-400">Assurance Gaps:</strong> {r.assurance_gaps}</p>
                            <p><strong className="text-blue-400 font-semibold">Remediation Label:</strong> {r.remediation_label}</p>
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
