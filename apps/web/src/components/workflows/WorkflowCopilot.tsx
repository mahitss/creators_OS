'use client';

import React, { useState } from 'react';
import {
  Sparkles,
  Bot,
  HelpCircle,
  AlertTriangle,
  Play,
  CheckCircle2,
  XCircle,
  ShieldCheck,
  Zap,
  Sliders,
  Send,
  Eye,
  Check,
  X,
  FileDiff,
  Activity,
  Layers
} from 'lucide-react';

interface WorkflowCopilotProps {
  workflowId: string;
  selectedNodeId: string | null;
  onApplyProposal?: (proposal: any) => void;
}

export const WorkflowCopilot: React.FC<WorkflowCopilotProps> = ({
  workflowId,
  selectedNodeId,
  onApplyProposal
}) => {
  const [activeTab, setActiveTab] = useState<'ask' | 'explain' | 'debug' | 'optimize' | 'simulate' | 'security'>('ask');
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [proposal, setProposal] = useState<any>(null);
  const [responseMessage, setResponseMessage] = useState<string | null>(null);
  const [debugResult, setDebugResult] = useState<any>(null);
  const [optResult, setOptResult] = useState<any>(null);
  const [simResult, setSimResult] = useState<any>(null);
  const [explainResult, setExplainResult] = useState<any>(null);

  const handleGenerateProposal = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim()) return;
    setLoading(true);
    setResponseMessage(null);
    setProposal(null);

    try {
      const res = await fetch('/api/v1/workflows/ai', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          workspaceId: 'ws_default_creator',
          workflowId: workflowId !== 'wf_default' ? workflowId : undefined,
          request_type: 'create',
          request_text: prompt
        })
      });

      if (res.ok) {
        const data = await res.json();
        setProposal(data);
      } else {
        const err = await res.json();
        setResponseMessage(`Error: ${err.detail || 'Could not generate proposal.'}`);
      }
    } catch (err) {
      setResponseMessage('Network error while generating AI proposal.');
    } finally {
      setLoading(false);
    }
  };

  const handleAcceptProposal = async () => {
    if (!proposal) return;
    try {
      const res = await fetch(`/api/v1/workflows/proposals/${proposal.id}/accept`, { method: 'POST' });
      if (res.ok) {
        const data = await res.json();
        setResponseMessage('Proposal accepted! Draft version created. Review and publish when ready.');
        if (onApplyProposal) onApplyProposal(proposal.proposed_definition);
      }
    } catch (err) {
      setResponseMessage('Failed to accept proposal.');
    }
  };

  const handleRejectProposal = async () => {
    if (!proposal) return;
    try {
      await fetch(`/api/v1/workflows/proposals/${proposal.id}/reject`, { method: 'POST' });
      setProposal(null);
      setResponseMessage('Proposal rejected. No changes made to workflow.');
    } catch (err) {
      setResponseMessage('Failed to reject proposal.');
    }
  };

  const handleExplain = async () => {
    setLoading(true);
    try {
      const res = await fetch(`/api/v1/workflows/${workflowId}/ai/explain`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ selected_node_id: selectedNodeId })
      });
      if (res.ok) {
        const data = await res.json();
        setExplainResult(data);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDebug = async () => {
    setLoading(true);
    try {
      const res = await fetch(`/api/v1/workflows/${workflowId}/ai/debug`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ run_id: 'run_latest' })
      });
      if (res.ok) {
        const data = await res.json();
        setDebugResult(data);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleOptimize = async () => {
    setLoading(true);
    try {
      const res = await fetch(`/api/v1/workflows/${workflowId}/ai/optimize`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ goal: 'balanced' })
      });
      if (res.ok) {
        const data = await res.json();
        setOptResult(data);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSimulate = async () => {
    setLoading(true);
    try {
      const res = await fetch(`/api/v1/workflows/${workflowId}/ai/simulate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scenarios: [] })
      });
      if (res.ok) {
        const data = await res.json();
        setSimResult(data);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-4 flex flex-col h-full space-y-4 text-xs overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-2">
          <div className="p-1.5 bg-indigo-500/10 text-indigo-400 rounded-lg border border-indigo-500/20">
            <Sparkles className="w-4 h-4" />
          </div>
          <span className="font-bold text-slate-100 text-sm">Workflow Copilot</span>
        </div>
        <span className="text-[10px] text-slate-400 bg-slate-950 px-2 py-0.5 rounded border border-slate-800 font-mono">
          Authoring Assistant
        </span>
      </div>

      {/* Tabs */}
      <div className="grid grid-cols-6 gap-1 bg-slate-950 p-1 rounded-lg border border-slate-800 text-[10px] font-medium text-center">
        <button onClick={() => setActiveTab('ask')} className={`py-1 rounded ${activeTab === 'ask' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'}`}>Ask</button>
        <button onClick={() => { setActiveTab('explain'); handleExplain(); }} className={`py-1 rounded ${activeTab === 'explain' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'}`}>Explain</button>
        <button onClick={() => { setActiveTab('debug'); handleDebug(); }} className={`py-1 rounded ${activeTab === 'debug' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'}`}>Debug</button>
        <button onClick={() => { setActiveTab('optimize'); handleOptimize(); }} className={`py-1 rounded ${activeTab === 'optimize' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'}`}>Optimize</button>
        <button onClick={() => { setActiveTab('simulate'); handleSimulate(); }} className={`py-1 rounded ${activeTab === 'simulate' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'}`}>Simulate</button>
        <button onClick={() => setActiveTab('security')} className={`py-1 rounded ${activeTab === 'security' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'}`}>Security</button>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 overflow-y-auto space-y-3 pr-1">
        {/* ASK TAB */}
        {activeTab === 'ask' && (
          <div className="space-y-3">
            <form onSubmit={handleGenerateProposal} className="space-y-2">
              <label className="block text-slate-400 text-[11px]">Describe desired workflow or modifications:</label>
              <div className="relative">
                <textarea
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  placeholder="e.g. Create a workflow that reviews important emails and prepares a response draft with approval"
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-slate-200 text-xs focus:outline-none focus:border-indigo-500 h-24 resize-none"
                />
                <button
                  type="submit"
                  disabled={loading}
                  className="absolute bottom-2 right-2 p-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-md transition"
                >
                  <Send className="w-3.5 h-3.5" />
                </button>
              </div>
            </form>

            {responseMessage && (
              <div className="p-3 rounded-lg bg-slate-950 border border-slate-800 text-[11px] text-slate-300">
                {responseMessage}
              </div>
            )}

            {/* Generated Proposal Visual Diff Viewer */}
            {proposal && (
              <div className="p-4 bg-slate-950 border border-indigo-500/30 rounded-xl space-y-3 shadow-xl">
                <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                  <span className="font-bold text-indigo-400 flex items-center gap-1.5 text-xs">
                    <FileDiff className="w-4 h-4" /> AI Workflow Proposal
                  </span>
                  <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    {proposal.risk_summary?.risk_level || 'Low Risk'}
                  </span>
                </div>

                <div className="space-y-1.5 text-[11px] text-slate-300">
                  <p><strong>Change Summary:</strong> {proposal.change_summary?.summary}</p>
                  <p><strong>Reads:</strong> {proposal.capability_summary?.reads?.join(', ') || 'None'}</p>
                  <p><strong>Writes:</strong> {proposal.capability_summary?.writes?.join(', ') || 'None'}</p>
                </div>

                <div className="flex space-x-2 pt-2 border-t border-slate-800">
                  <button
                    onClick={handleAcceptProposal}
                    className="flex-1 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-slate-950 font-bold rounded-lg transition flex items-center justify-center space-x-1"
                  >
                    <Check className="w-3.5 h-3.5" /> <span>Accept Proposal</span>
                  </button>
                  <button
                    onClick={handleRejectProposal}
                    className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg transition flex items-center justify-center"
                  >
                    <X className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        {/* EXPLAIN TAB */}
        {activeTab === 'explain' && (
          <div className="space-y-3">
            {explainResult ? (
              <div className="space-y-2">
                <div className="p-3 bg-slate-950 rounded-lg border border-slate-800">
                  <span className="font-semibold text-slate-200 block mb-1">Graph Structure:</span>
                  <p className="text-slate-400 text-[11px]">{explainResult.explanation}</p>
                </div>
                <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 space-y-1 text-[11px]">
                  <span className="font-semibold text-slate-200 block">Configured Steps:</span>
                  {explainResult.step_sequence?.map((st: string, idx: number) => (
                    <div key={idx} className="text-slate-400 font-mono">• {st}</div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="text-slate-500 text-center py-6">Loading graph explanation...</div>
            )}
          </div>
        )}

        {/* DEBUG TAB */}
        {activeTab === 'debug' && (
          <div className="space-y-3">
            {debugResult ? (
              <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-rose-400 uppercase text-[10px]">Failure Category: {debugResult.failure_category}</span>
                </div>
                <p className="text-slate-300 text-[11px]">{debugResult.evidence_summary}</p>
                <div className="p-2 bg-slate-900 border border-slate-800 rounded text-cyan-400 font-mono text-[10px]">
                  Remediation: {debugResult.suggested_remediation}
                </div>
              </div>
            ) : (
              <div className="text-slate-500 text-center py-6">Analyzing execution telemetry...</div>
            )}
          </div>
        )}

        {/* OPTIMIZE TAB */}
        {activeTab === 'optimize' && (
          <div className="space-y-3">
            {optResult ? (
              <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 space-y-2">
                <span className="font-bold text-amber-400 block">Optimization Suggestion</span>
                <p className="text-slate-300 text-[11px]">{optResult.reason}</p>
                <div className="grid grid-cols-2 gap-2 text-[10px]">
                  <div className="p-2 bg-slate-900 rounded border border-slate-800">
                    <span className="text-slate-500 block">Cost Reduction</span>
                    <span className="text-emerald-400 font-bold">{optResult.estimated_improvement?.cost_reduction_percent}%</span>
                  </div>
                  <div className="p-2 bg-slate-900 rounded border border-slate-800">
                    <span className="text-slate-500 block">Latency Saved</span>
                    <span className="text-indigo-400 font-bold">{optResult.estimated_improvement?.latency_reduction_ms} ms</span>
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-slate-500 text-center py-6">Evaluating workflow optimizations...</div>
            )}
          </div>
        )}

        {/* SIMULATE TAB */}
        {activeTab === 'simulate' && (
          <div className="space-y-3">
            {simResult ? (
              <div className="space-y-2">
                {simResult.scenarios?.map((sc: any, idx: number) => (
                  <div key={idx} className="p-3 bg-slate-950 rounded-lg border border-slate-800 space-y-1">
                    <div className="flex items-center justify-between">
                      <span className="font-semibold text-slate-200">{sc.scenario_name}</span>
                      <span className="text-emerald-400 font-mono text-[10px]">{sc.simulated_outcome}</span>
                    </div>
                    <span className="text-slate-500 text-[10px] block">Estimated Cost: ${sc.estimated_cost}</span>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-slate-500 text-center py-6">Running synthetic simulations...</div>
            )}
          </div>
        )}

        {/* SECURITY REVIEW TAB */}
        {activeTab === 'security' && (
          <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 space-y-2">
            <span className="font-bold text-slate-200 block text-xs">Deterministic Security Review</span>
            <div className="space-y-1 text-[11px] text-slate-400">
              <div className="flex justify-between"><span>PolicyEngine Status:</span><span className="text-emerald-400 font-semibold">ENFORCED</span></div>
              <div className="flex justify-between"><span>Arbitrary Code Nodes:</span><span className="text-slate-300 font-semibold">FORBIDDEN</span></div>
              <div className="flex justify-between"><span>Secret Protection:</span><span className="text-emerald-400 font-semibold">PROTECTED</span></div>
              <div className="flex justify-between"><span>Kahn Cycle Guard:</span><span className="text-emerald-400 font-semibold">ACTIVE</span></div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
