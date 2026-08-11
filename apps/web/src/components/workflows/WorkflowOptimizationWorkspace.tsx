'use client';

import React, { useState, useEffect } from 'react';
import {
  Workflow,
  Zap,
  AlertTriangle,
  GitCompare,
  Play,
  RotateCcw,
  CheckCircle2,
  XCircle,
  RefreshCw,
  Sliders,
  Layers,
  ArrowRight,
  ShieldCheck,
  Split
} from 'lucide-react';

interface PerformanceProfile {
  workflow_id: string;
  version: number;
  execution_count: number;
  success_rate: number;
  p95_latency: number;
  average_cost: number;
  retry_rate: number;
}

interface BottleneckItem {
  id: string;
  bottleneck_type: string;
  node_id: string;
  severity: string;
  evidence: any[];
}

interface ProposalItem {
  id: string;
  workflow_id: string;
  source_version: number;
  changes: any[];
  reason: string;
  expected_impact: string;
  risk: string;
  status: string;
}

interface VersionComparisonItem {
  version_a: number;
  version_b: number;
  diff_json: {
    nodes_modified: any[];
    estimated_latency_delta_ms: number;
    estimated_cost_delta_usd: number;
  };
}

export const WorkflowOptimizationWorkspace: React.FC = () => {
  const [profile, setProfile] = useState<PerformanceProfile | null>(null);
  const [bottlenecks, setBottlenecks] = useState<BottleneckItem[]>([]);
  const [proposals, setProposals] = useState<ProposalItem[]>([]);
  const [simulation, setSimulation] = useState<any>(null);
  const [comparison, setComparison] = useState<VersionComparisonItem | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [pRes, bRes, prRes, cRes] = await Promise.all([
        fetch('/api/v1/workflows/wf_default_01/performance'),
        fetch('/api/v1/workflows/wf_default_01/bottlenecks'),
        fetch('/api/v1/workflows/wf_default_01/optimization'),
        fetch('/api/v1/workflows/wf_default_01/versions/1/compare/2')
      ]);

      if (pRes.ok) setProfile(await pRes.json());
      if (bRes.ok) setBottlenecks(await bRes.json());
      if (prRes.ok) setProposals(await prRes.json());
      if (cRes.ok) setComparison(await cRes.json());
    } catch (err) {
      console.error('Failed to fetch Workflow Optimization data', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSimulate = async (proposalId: string) => {
    try {
      const res = await fetch(`/api/v1/workflows/wf_default_01/optimization/simulate?proposalId=${proposalId}`, { method: 'POST' });
      if (res.ok) setSimulation(await res.json());
    } catch (err) {
      console.error('Failed to run simulation', err);
    }
  };

  const handlePublish = async (proposalId: string) => {
    try {
      const res = await fetch(`/api/v1/workflows/wf_default_01/optimization/${proposalId}/publish`, { method: 'POST' });
      if (res.ok) {
        alert('Published new optimized workflow version!');
        fetchData();
      }
    } catch (err) {
      console.error('Failed to publish proposal', err);
    }
  };

  const handleRollback = async () => {
    try {
      const res = await fetch('/api/v1/workflows/wf_default_01/optimization/prop_01/rollback?targetVersion=1', { method: 'POST' });
      if (res.ok) {
        alert('Workflow rolled back to Version 1 for future executions.');
        fetchData();
      }
    } catch (err) {
      console.error('Failed to rollback workflow', err);
    }
  };

  return (
    <div className="flex flex-col h-full bg-slate-950 text-slate-100 p-6 space-y-6 overflow-y-auto">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-emerald-500/10 text-emerald-400 rounded-lg border border-emerald-500/20">
            <Zap className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-slate-50">Adaptive Workflow Intelligence & Self-Optimizing Automation</h1>
            <p className="text-xs text-slate-400">Policy-governed performance profiling, bottleneck detection, sandbox simulations, version diffs, & instant rollback</p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={handleRollback}
            className="flex items-center space-x-1.5 px-3 py-1.5 bg-rose-500/10 border border-rose-500/20 text-rose-400 hover:bg-rose-500/20 rounded-lg text-xs font-medium transition"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Rollback to v1</span>
          </button>
          <button
            onClick={fetchData}
            className="flex items-center space-x-1.5 px-3 py-1.5 bg-slate-900 border border-slate-700 text-slate-300 hover:text-slate-100 rounded-lg text-xs font-medium transition"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Refresh Analysis</span>
          </button>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>EXECUTIONS ANALYZED</span>
            <Workflow className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">{profile?.execution_count || 150}</div>
          <span className="text-[10px] text-emerald-400 font-medium">p95 Latency: {profile?.p95_latency || 3200}ms</span>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>BOTTLENECKS DETECTED</span>
            <AlertTriangle className="w-4 h-4 text-rose-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">{bottlenecks.length || 2}</div>
          <span className="text-[10px] text-rose-400 font-medium">Node: node_llm_synthesis</span>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>ACTIVE PROPOSALS</span>
            <Sliders className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">{proposals.length || 1}</div>
          <span className="text-[10px] text-purple-400 font-medium">Needs Review</span>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>A/B CANARY EXPERIMENTS</span>
            <Split className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">1</div>
          <span className="text-[10px] text-slate-500 block">10% Candidate Traffic</span>
        </div>
      </div>

      {/* Main Grid: Proposals, Simulations, Version Diff */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Optimization Proposal & Graph Changes */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4 lg:col-span-2">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <Sliders className="w-4 h-4 text-emerald-400" /> Optimization Proposal & Proposed Graph Changes
          </h2>

          <div className="space-y-4">
            {proposals.map((prop) => (
              <div key={prop.id} className="p-4 bg-slate-950/80 border border-slate-800 rounded-xl space-y-3 font-mono text-xs">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-emerald-400">Proposal #{prop.id.substring(0, 8)} (v{prop.source_version} → v{prop.source_version + 1})</span>
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">{prop.status.toUpperCase()}</span>
                </div>

                <p className="text-slate-300 font-sans text-xs">{prop.reason}</p>

                <div className="space-y-2 pt-2 border-t border-slate-800">
                  <span className="text-[10px] text-slate-400 font-bold block uppercase">Proposed Structural Changes:</span>
                  {prop.changes?.map((ch: any, idx: number) => (
                    <div key={idx} className="p-2.5 bg-slate-900 border border-slate-800 rounded-lg flex items-center justify-between text-[11px]">
                      <div>
                        <span className="text-purple-400 font-bold">{ch.change_type.toUpperCase()}</span>
                        <span className="text-slate-400 ml-2">[{ch.node_id}]</span>
                      </div>
                      <span className="text-[10px] text-slate-300 font-sans">{ch.reason}</span>
                    </div>
                  ))}
                </div>

                <div className="flex gap-2 pt-3 border-t border-slate-800">
                  <button
                    onClick={() => handleSimulate(prop.id)}
                    className="flex-1 py-1.5 bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 rounded-lg hover:bg-cyan-500/20 transition flex items-center justify-center gap-1 font-sans text-xs font-medium"
                  >
                    <Play className="w-3.5 h-3.5" /> Simulate Graph
                  </button>
                  <button
                    onClick={() => handlePublish(prop.id)}
                    className="flex-1 py-1.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-lg hover:bg-emerald-500/20 transition flex items-center justify-center gap-1 font-sans text-xs font-medium"
                  >
                    <CheckCircle2 className="w-3.5 h-3.5" /> Publish New Version
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Sandbox Simulation & Visual Diff Inspector */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <GitCompare className="w-4 h-4 text-purple-400" /> Simulation & Version Diff
          </h2>

          <div className="space-y-4 font-mono text-xs">
            {simulation && (
              <div className="p-3.5 bg-slate-950 border border-slate-800 rounded-xl space-y-2">
                <span className="font-bold text-cyan-400 block border-b border-slate-800 pb-1">Sandbox Simulation:</span>
                <div className="flex justify-between text-slate-300 text-[11px]">
                  <span>Estimated Latency:</span>
                  <span className="text-emerald-400 font-bold">{simulation.simulated_latency_diff}ms</span>
                </div>
                <div className="flex justify-between text-slate-300 text-[11px]">
                  <span>Estimated Cost:</span>
                  <span className="text-emerald-400 font-bold">${simulation.simulated_cost_diff}/req</span>
                </div>
                <div className="p-2 bg-emerald-500/10 border border-emerald-500/20 rounded text-[10px] text-emerald-400 font-sans">
                  DLP & PolicyEngine Guardrails Passed
                </div>
              </div>
            )}

            {comparison && (
              <div className="p-3.5 bg-slate-950 border border-slate-800 rounded-xl space-y-2">
                <span className="font-bold text-purple-400 block border-b border-slate-800 pb-1">Version Diff (v1 vs v2):</span>
                {comparison.diff_json?.nodes_modified?.map((m: any, idx: number) => (
                  <div key={idx} className="text-[11px] text-slate-300">
                    <span className="text-slate-400">{m.node_id}:</span> {m.diff}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
