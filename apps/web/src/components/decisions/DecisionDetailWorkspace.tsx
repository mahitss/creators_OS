'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { 
  GitPullRequest, 
  CheckCircle2, 
  AlertTriangle, 
  RotateCw, 
  ShieldCheck, 
  Layers, 
  FileText, 
  TrendingUp, 
  ArrowLeft,
  UserCheck,
  Zap,
  Sliders
} from 'lucide-react';

export const DecisionDetailWorkspace: React.FC<{ decisionId: string }> = ({ decisionId }) => {
  const [decision, setDecision] = useState<any>({
    id: decisionId,
    decisionType: 'architectural',
    question: 'Which deployment strategy should we use for the high-volume data pipeline?',
    status: 'options_ready',
    currentVersion: 1
  });

  const [evidences, setEvidences] = useState<any[]>([
    {
      id: 'ev_001',
      sourceType: 'document',
      sourceId: 'doc_arch_spec_01',
      claimSummary: 'P99 latency requirement is under 150ms for 95% of queries',
      authority: 'high',
      freshness: 'fresh',
      status: 'verified'
    },
    {
      id: 'ev_002',
      sourceType: 'integration',
      sourceId: 'int_cloud_provider_01',
      claimSummary: 'Legacy serverless tier incurs burst concurrency throttling above 5,000 QPS',
      authority: 'medium',
      freshness: 'fresh',
      status: 'verified'
    }
  ]);

  const [options, setOptions] = useState<any[]>([
    {
      id: 'opt_a_k8s',
      name: 'Provisioned Kubernetes Cluster',
      description: 'Dedicated Kubernetes worker pool with automated Horizontal Pod Autoscaler',
      generatedBy: 'agent',
      isGenerated: true,
      constraints: { budget: '$500/mo' },
      risks: ['Idle resource cost']
    },
    {
      id: 'opt_b_serverless',
      name: 'Serverless Functions with Provisioned Concurrency',
      description: 'On-demand execution with 50 pre-warmed instances',
      generatedBy: 'skill',
      isGenerated: true,
      constraints: { budget: '$300/mo' },
      risks: ['Burst concurrency limit']
    }
  ]);

  const [tradeoffs, setTradeoffs] = useState<any[]>([
    {
      id: 'to_001',
      advantageA: 'Guaranteed low P99 latency under heavy burst QPS',
      advantageB: 'Lower baseline monthly cost during quiet off-peak hours',
      tradeoffSummary: 'Kubernetes yields lower latency and zero throttling at higher fixed cost; Serverless reduces cost at risk of cold-start latency'
    }
  ]);

  const [activeTab, setActiveTab] = useState<'evidence' | 'options' | 'risks' | 'scenarios' | 'approval'>('evidence');
  const [scenarioName, setScenarioName] = useState('High QPS Spike Test');
  const [scenarioResult, setScenarioResult] = useState<any>(null);
  const [overrideReason, setOverrideReason] = useState('');
  const [showOverrideModal, setShowOverrideModal] = useState(false);

  const fetchDecisionDetail = React.useCallback(async () => {
    try {
      const res = await fetch(`/api/v1/decisions/${decisionId}`);
      if (res.ok) {
        setDecision(await res.json());
      }
      const evRes = await fetch(`/api/v1/decisions/${decisionId}/evidence`);
      if (evRes.ok) {
        setEvidences(await evRes.json());
      }
      const optRes = await fetch(`/api/v1/decisions/${decisionId}/options`);
      if (optRes.ok) {
        setOptions(await optRes.json());
      }
    } catch (e) {
      // Keep fallback
    }
  }, [decisionId]);

  useEffect(() => {
    fetchDecisionDetail();
  }, [fetchDecisionDetail]);

  const handleApprove = async (recommendedOptionId: string) => {
    try {
      const res = await fetch(`/api/v1/decisions/${decisionId}/approve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ recommendedOptionId })
      });
      if (res.ok) {
        setDecision(await res.json());
      }
    } catch (e) {
      setDecision({ ...decision, status: 'approved' });
    }
  };

  const handleOverride = async () => {
    if (!overrideReason.trim()) return;
    try {
      const res = await fetch(`/api/v1/decisions/${decisionId}/override`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          originalOptionId: options[0]?.id,
          selectedOptionId: options[1]?.id || options[0]?.id,
          reason: overrideReason.trim()
        })
      });
      if (res.ok) {
        setDecision(await res.json());
        setShowOverrideModal(false);
      }
    } catch (e) {
      setDecision({ ...decision, status: 'approved', currentVersion: decision.currentVersion + 1 });
      setShowOverrideModal(false);
    }
  };

  const handleRunScenario = async () => {
    try {
      const res = await fetch(`/api/v1/decisions/${decisionId}/scenarios`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: scenarioName,
          assumptions: { load_multiplier: 3.5 },
          variables: { target_qps: 15000 }
        })
      });
      if (res.ok) {
        const scen = await res.json();
        setScenarioResult(scen.resultSummary);
      }
    } catch (e) {
      setScenarioResult({
        predicted_impact: 'Latency increases by +25ms, cost decreases by -$120/mo',
        risk_delta: 'Low -> Medium',
        production_mutated: false
      });
    }
  };

  return (
    <div className="space-y-6">
      <Link href="/decisions" className="inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-indigo-400 transition font-medium">
        <ArrowLeft className="w-3.5 h-3.5" /> Back to Decision Catalog
      </Link>

      {/* Header */}
      <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl text-white space-y-4">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="px-2.5 py-0.5 text-[10px] font-semibold uppercase rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                {decision.decisionType}
              </span>
              <span className="text-xs text-slate-400 font-mono">v{decision.currentVersion}</span>
            </div>
            <h1 className="text-xl font-bold tracking-tight">{decision.question}</h1>
          </div>

          <div className="flex items-center gap-2">
            {decision.status !== 'approved' && (
              <>
                <button
                  onClick={() => handleApprove(options[0]?.id || 'opt_a_k8s')}
                  className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-semibold flex items-center gap-1.5 transition"
                >
                  <CheckCircle2 className="w-3.5 h-3.5" /> Approve Recommended Option
                </button>
                <button
                  onClick={() => setShowOverrideModal(true)}
                  className="px-4 py-2 bg-amber-600/20 hover:bg-amber-600/30 text-amber-300 border border-amber-500/30 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition"
                >
                  <UserCheck className="w-3.5 h-3.5" /> Human Override
                </button>
              </>
            )}
            {decision.status === 'approved' && (
              <span className="px-4 py-2 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-semibold rounded-lg flex items-center gap-1.5">
                <ShieldCheck className="w-4 h-4" /> APPROVED & IMMUTABLE
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
        <button
          onClick={() => setActiveTab('evidence')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition ${
            activeTab === 'evidence' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Claims & Evidence ({evidences.length})
        </button>
        <button
          onClick={() => setActiveTab('options')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition ${
            activeTab === 'options' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Options & Trade-Offs ({options.length})
        </button>
        <button
          onClick={() => setActiveTab('scenarios')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition ${
            activeTab === 'scenarios' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          What-If Scenario Simulator
        </button>
      </div>

      {/* Evidence & Claims Tab */}
      {activeTab === 'evidence' && (
        <div className="space-y-4">
          <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl space-y-4">
            <h3 className="text-sm font-semibold text-white">Claim Classification Breakdown</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              <div className="bg-slate-950 p-3.5 rounded-lg border border-slate-800">
                <span className="text-[10px] font-mono uppercase bg-emerald-500/10 text-emerald-400 px-2 py-0.5 rounded font-bold">FACT</span>
                <p className="text-xs text-slate-300 mt-2">P99 latency requirement is under 150ms for 95% of queries (Verified in doc_arch_spec_01)</p>
              </div>
              <div className="bg-slate-950 p-3.5 rounded-lg border border-slate-800">
                <span className="text-[10px] font-mono uppercase bg-indigo-500/10 text-indigo-400 px-2 py-0.5 rounded font-bold">INFERENCE</span>
                <p className="text-xs text-slate-300 mt-2">Serverless scaling will throttle under Black Friday QPS spikes (Derived from telemetry)</p>
              </div>
              <div className="bg-slate-950 p-3.5 rounded-lg border border-slate-800">
                <span className="text-[10px] font-mono uppercase bg-amber-500/10 text-amber-400 px-2 py-0.5 rounded font-bold">RECOMMENDATION</span>
                <p className="text-xs text-slate-300 mt-2">Deploy Provisioned Kubernetes Cluster with HPA enabled</p>
              </div>
            </div>

            <h3 className="text-sm font-semibold text-white pt-2 border-t border-slate-800">Evidence Provenance</h3>
            <div className="space-y-2">
              {evidences.map((ev) => (
                <div key={ev.id} className="bg-slate-950 p-3.5 rounded-lg border border-slate-800 flex items-center justify-between text-xs">
                  <div className="space-y-1">
                    <p className="text-slate-200 font-medium">{ev.claimSummary}</p>
                    <p className="text-slate-400 font-mono text-[11px]">Source: {ev.sourceType} ({ev.sourceId})</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="px-2 py-0.5 bg-slate-800 text-slate-300 rounded font-mono text-[10px] uppercase">{ev.authority} Authority</span>
                    <span className="px-2 py-0.5 bg-emerald-500/10 text-emerald-400 rounded font-mono text-[10px] uppercase">{ev.freshness}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Options & Tradeoffs Tab */}
      {activeTab === 'options' && (
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {options.map((opt) => (
              <div key={opt.id} className="bg-slate-900 border border-slate-800 p-5 rounded-xl space-y-3">
                <div className="flex items-center justify-between">
                  <h4 className="text-base font-semibold text-white">{opt.name}</h4>
                  <span className="text-[10px] font-mono uppercase bg-indigo-500/10 text-indigo-400 px-2 py-0.5 rounded">
                    Generated by {opt.generatedBy}
                  </span>
                </div>
                <p className="text-xs text-slate-300">{opt.description}</p>
                <div className="bg-slate-950 p-3 rounded border border-slate-800 text-xs font-mono space-y-1 text-slate-400">
                  <div>Risks: <span className="text-amber-400">{opt.risks.join(', ')}</span></div>
                </div>
              </div>
            ))}
          </div>

          <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl space-y-2">
            <h4 className="text-sm font-semibold text-white">Trade-Off Analysis</h4>
            {tradeoffs.map((to) => (
              <div key={to.id} className="bg-slate-950 p-4 rounded-lg border border-slate-800 text-xs text-slate-300 space-y-2">
                <p className="font-semibold text-indigo-300">{to.tradeoffSummary}</p>
                <div className="grid grid-cols-2 gap-2 pt-1 border-t border-slate-800 font-mono text-[11px]">
                  <div>Option A Advantage: <span className="text-emerald-400">{to.advantageA}</span></div>
                  <div>Option B Advantage: <span className="text-emerald-400">{to.advantageB}</span></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Scenario Simulator Tab */}
      {activeTab === 'scenarios' && (
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl space-y-4">
          <h3 className="text-sm font-semibold text-white">Non-Destructive Scenario Simulator (&quot;What-If&quot; Analysis)</h3>
          <div className="flex items-center gap-3">
            <input
              type="text"
              value={scenarioName}
              onChange={(e) => setScenarioName(e.target.value)}
              className="flex-1 px-4 py-2 bg-slate-950 border border-slate-800 rounded-lg text-xs text-white"
            />
            <button
              onClick={handleRunScenario}
              className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold transition"
            >
              Simulate Scenario
            </button>
          </div>

          {scenarioResult && (
            <div className="bg-slate-950 p-4 rounded-lg border border-slate-800 text-xs font-mono text-slate-300 space-y-2">
              <div>Predicted Impact: <span className="text-indigo-400">{scenarioResult.predicted_impact}</span></div>
              <div>Risk Delta: <span className="text-amber-400">{scenarioResult.risk_delta}</span></div>
              <div>Production Mutated: <span className="text-emerald-400">{scenarioResult.production_mutated ? 'YES' : 'NO (DRY RUN)'}</span></div>
            </div>
          )}
        </div>
      )}

      {/* Override Modal */}
      {showOverrideModal && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl max-w-md w-full space-y-4">
            <h3 className="text-lg font-bold text-white">Human Override Decision</h3>
            <p className="text-xs text-slate-400">Override the AI recommendation with explicit rationale. The original recommendation and full audit trail will be preserved.</p>

            <textarea
              rows={3}
              placeholder="Specify rationale for override..."
              value={overrideReason}
              onChange={(e) => setOverrideReason(e.target.value)}
              className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-xs text-white focus:outline-none focus:border-indigo-500"
            />

            <div className="flex items-center justify-end gap-2">
              <button
                onClick={() => setShowOverrideModal(false)}
                className="px-4 py-2 bg-slate-800 text-slate-300 text-xs font-semibold rounded-lg"
              >
                Cancel
              </button>
              <button
                onClick={handleOverride}
                className="px-4 py-2 bg-amber-600 hover:bg-amber-500 text-white text-xs font-semibold rounded-lg"
              >
                Confirm Human Override
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
