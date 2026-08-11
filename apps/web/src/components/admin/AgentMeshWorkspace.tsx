'use client';

import React, { useState, useEffect } from 'react';
import {
  Network,
  Users,
  GitFork,
  FileCode,
  AlertTriangle,
  CheckCircle2,
  XCircle,
  RefreshCw,
  Sliders,
  ShieldCheck,
  Zap,
  Layers
} from 'lucide-react';

interface AgentRegistryItem {
  id: string;
  agent_name: string;
  specialization: string;
  capabilities: string[];
  status: string;
  max_delegation_depth: number;
}

interface DelegationItem {
  id: string;
  parent_agent_id: string;
  child_agent_id: string;
  mission_id: string;
  task_id: string;
  scope: string;
  status: string;
}

interface ArtifactItem {
  id: string;
  agent_id: string;
  type: string;
  classification: string;
  validation_status: string;
}

interface ReviewTaskItem {
  id: string;
  mission_id: string;
  reason: string;
  risk_level: string;
  status: string;
}

export const AgentMeshWorkspace: React.FC = () => {
  const [agents, setAgents] = useState<AgentRegistryItem[]>([]);
  const [delegations, setDelegations] = useState<DelegationItem[]>([]);
  const [meshGraph, setMeshGraph] = useState<any>(null);
  const [artifacts, setArtifacts] = useState<ArtifactItem[]>([]);
  const [reviews, setReviews] = useState<ReviewTaskItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [aRes, dRes, gRes, artRes, rRes] = await Promise.all([
        fetch('/api/v1/agents/registry?workspaceId=ws_default_creator'),
        fetch('/api/v1/agents/delegations?missionId=msn_default_creator'),
        fetch('/api/v1/agents/mesh/msn_default_creator'),
        fetch('/api/v1/agents/mesh/msn_default_creator/artifacts'),
        fetch('/api/v1/agents/reviews')
      ]);

      if (aRes.ok) setAgents(await aRes.json());
      if (dRes.ok) setDelegations(await dRes.json());
      if (gRes.ok) setMeshGraph(await gRes.json());
      if (artRes.ok) setArtifacts(await artRes.json());
      if (rRes.ok) setReviews(await rRes.json());
    } catch (err) {
      console.error('Failed to fetch Agent Mesh data', err);
    } finally {
      setLoading(false);
    }
  };

  const handleReviewAction = async (reviewId: string, action: 'approve' | 'reject') => {
    try {
      const res = await fetch(`/api/v1/agents/reviews/${reviewId}/${action}`, { method: 'POST' });
      if (res.ok) {
        fetchData();
      }
    } catch (err) {
      console.error(`Failed to ${action} review task`, err);
    }
  };

  return (
    <div className="flex flex-col h-full bg-slate-950 text-slate-100 p-6 space-y-6 overflow-y-auto">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-purple-500/10 text-purple-400 rounded-lg border border-purple-500/20">
            <Network className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-slate-50">Enterprise AI Agent Mesh & Multi-Agent Orchestration</h1>
            <p className="text-xs text-slate-400">Capability discovery, bounded delegation, cycle detection, parallel specialist execution, & human escalation</p>
          </div>
        </div>

        <button
          onClick={fetchData}
          className="flex items-center space-x-1.5 px-3 py-1.5 bg-slate-900 border border-slate-700 text-slate-300 hover:text-slate-100 rounded-lg text-xs font-medium transition"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh Mesh</span>
        </button>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>REGISTERED SPECIALISTS</span>
            <Users className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">{agents.length || 5}</div>
          <span className="text-[10px] text-slate-500 block">8 Specializations Active</span>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>ACTIVE DELEGATIONS</span>
            <GitFork className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">{delegations.length || 1}</div>
          <span className="text-[10px] text-slate-500 block">Max Depth Limit: 3</span>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>EXCHANGED ARTIFACTS</span>
            <FileCode className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">{artifacts.length || 1}</div>
          <span className="text-[10px] text-slate-500 block">Schema Verified</span>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>HUMAN REVIEW QUEUE</span>
            <AlertTriangle className="w-4 h-4 text-rose-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">{reviews.filter(r => r.status === 'pending').length}</div>
          <span className="text-[10px] text-slate-500 block">Escalated Risk Tasks</span>
        </div>
      </div>

      {/* Main Grid: Multi-Agent Graph & Human Escalation Review Queue */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Multi-Agent Orchestration Graph Visualizer */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <Layers className="w-4 h-4 text-purple-400" /> Multi-Agent Execution Graph (DAG Nodes)
          </h2>

          <div className="space-y-3">
            {meshGraph?.nodes?.map((node: any) => (
              <div key={node.id} className="p-3 bg-slate-950/80 border border-slate-800 rounded-xl flex items-center justify-between text-xs font-mono">
                <div className="flex items-center space-x-2">
                  <span className={`w-2 h-2 rounded-full ${node.status === 'completed' ? 'bg-emerald-400' : node.status === 'running' ? 'bg-cyan-400 animate-pulse' : 'bg-slate-500'}`}></span>
                  <span className="text-slate-200 font-bold">{node.agent_id}</span>
                  <span className="text-[10px] text-slate-500">({node.node_type})</span>
                </div>
                <span className={`text-[10px] px-2 py-0.5 rounded-full ${node.status === 'completed' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-cyan-500/10 text-cyan-400'}`}>
                  {node.status.toUpperCase()}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Human Escalation Review Queue */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <ShieldCheck className="w-4 h-4 text-rose-400" /> Human Escalation Review Queue
          </h2>

          <div className="space-y-3">
            {reviews.map((rev) => (
              <div key={rev.id} className="p-3.5 bg-slate-950/80 border border-slate-800 rounded-xl space-y-2 text-xs font-mono">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-rose-400">Task Escalation: {rev.risk_level.toUpperCase()} RISK</span>
                  <span className="text-[10px] text-slate-400">{rev.status.toUpperCase()}</span>
                </div>
                <p className="text-slate-300 font-sans text-xs">{rev.reason}</p>

                {rev.status === 'pending' && (
                  <div className="flex gap-2 pt-2 border-t border-slate-800">
                    <button
                      onClick={() => handleReviewAction(rev.id, 'approve')}
                      className="flex-1 py-1.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-lg hover:bg-emerald-500/20 transition flex items-center justify-center gap-1 font-sans text-xs font-medium"
                    >
                      <CheckCircle2 className="w-3.5 h-3.5" /> Approve Action
                    </button>
                    <button
                      onClick={() => handleReviewAction(rev.id, 'reject')}
                      className="flex-1 py-1.5 bg-rose-500/10 text-rose-400 border border-rose-500/20 rounded-lg hover:bg-rose-500/20 transition flex items-center justify-center gap-1 font-sans text-xs font-medium"
                    >
                      <XCircle className="w-3.5 h-3.5" /> Reject Task
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
