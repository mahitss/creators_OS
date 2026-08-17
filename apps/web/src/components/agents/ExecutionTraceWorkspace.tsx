'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { 
  Play, 
  Pause, 
  Square, 
  RefreshCw, 
  AlertTriangle, 
  CheckCircle2, 
  Clock, 
  ShieldCheck, 
  Layers, 
  Cpu, 
  FileText, 
  Database,
  ArrowRight,
  UserCheck,
  AlertCircle
} from 'lucide-react';

interface AgentExecutionData {
  id: string;
  organizationId: string;
  workspaceId: string;
  agentId: string;
  missionId?: string;
  status: string;
  version: number;
  currentStep?: string;
  createdAt: string;
  updatedAt: string;
}

interface AgentExecutionStepData {
  id: string;
  executionId: string;
  stepType: string;
  status: string;
  attempt: number;
  inputReference: any;
  outputReference?: any;
  startedAt?: string;
  completedAt?: string;
}

interface ExecutionCheckpointData {
  id: string;
  executionId: string;
  executionVersion: number;
  stepId?: string;
  stateReference: any;
  reason: string;
  createdAt: string;
}

interface UnknownOutcomeData {
  id: string;
  executionId: string;
  stepId: string;
  idempotencyKey: string;
  actionType: string;
  status: string;
  resolutionNotes?: string;
  resolvedBy?: string;
  createdAt: string;
}

export const ExecutionTraceWorkspace: React.FC<{ executionId?: string }> = ({ executionId = 'exec_demo_01' }) => {
  const [execution, setExecution] = useState<AgentExecutionData | null>({
    id: executionId,
    organizationId: 'org_default_creator',
    workspaceId: 'ws_default_01',
    agentId: 'ag_creator_ops_01',
    missionId: 'msn_001',
    status: 'running',
    version: 3,
    currentStep: 'step_003',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  });

  const [steps, setSteps] = useState<AgentExecutionStepData[]>([
    {
      id: 'step_001',
      executionId: executionId,
      stepType: 'knowledge_retrieval',
      status: 'completed',
      attempt: 1,
      inputReference: { query: 'Q3 product roadmap' },
      outputReference: { retrieved_count: 4 },
      startedAt: new Date().toISOString(),
      completedAt: new Date().toISOString()
    },
    {
      id: 'step_002',
      executionId: executionId,
      stepType: 'model_call',
      status: 'completed',
      attempt: 1,
      inputReference: { capability: 'reasoning', prompt: 'Synthesize roadmap report' },
      outputReference: { selected_model: 'gemini-1.5-pro' },
      startedAt: new Date().toISOString(),
      completedAt: new Date().toISOString()
    },
    {
      id: 'step_003',
      executionId: executionId,
      stepType: 'tool_call',
      status: 'running',
      attempt: 1,
      inputReference: { tool: 'gmail.send', recipient: 'exec@vapor.ai' },
      startedAt: new Date().toISOString()
    }
  ]);

  const [checkpoints, setCheckpoints] = useState<ExecutionCheckpointData[]>([
    {
      id: 'chk_001',
      executionId: executionId,
      executionVersion: 2,
      stepId: 'step_002',
      stateReference: { variables_count: 2 },
      reason: 'before_external_action',
      createdAt: new Date().toISOString()
    }
  ]);

  const [unknownOutcomes, setUnknownOutcomes] = useState<UnknownOutcomeData[]>([]);
  const [resolveNotes, setResolveNotes] = useState<string>('Verified external action executed cleanly in provider audit logs.');
  const [activeTab, setActiveTab] = useState<'timeline' | 'checkpoints' | 'state' | 'unknown'>('timeline');
  const [loading, setLoading] = useState<boolean>(false);

  const fetchTrace = useCallback(async () => {
    try {
      const res = await fetch(`/api/v1/agents/executions/${executionId}/trace`);
      if (res.ok) {
        const data = await res.json();
        setExecution(data.execution);
        setSteps(data.steps || []);
        setCheckpoints(data.checkpoints || []);
        setUnknownOutcomes(data.unknown_outcomes || []);
      }
    } catch (e) {
      // Keep fallback state
    }
  }, [executionId]);

  useEffect(() => {
    fetchTrace();
  }, [fetchTrace]);

  const handlePause = async () => {
    try {
      const res = await fetch(`/api/v1/agents/executions/${executionId}/pause`, { method: 'POST' });
      if (res.ok) fetchTrace();
    } catch (e) {
      if (execution) setExecution({ ...execution, status: 'paused' });
    }
  };

  const handleResume = async () => {
    try {
      const res = await fetch(`/api/v1/agents/executions/${executionId}/resume`, { method: 'POST' });
      if (res.ok) fetchTrace();
    } catch (e) {
      if (execution) setExecution({ ...execution, status: 'running' });
    }
  };

  const handleCancel = async () => {
    try {
      const res = await fetch(`/api/v1/agents/executions/${executionId}/cancel`, { method: 'POST' });
      if (res.ok) fetchTrace();
    } catch (e) {
      if (execution) setExecution({ ...execution, status: 'cancelled' });
    }
  };

  const handleResolveUnknown = async (stepId: string) => {
    try {
      const res = await fetch(`/api/v1/agents/executions/${executionId}/unknown-outcomes/${stepId}/resolve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ resolution: 'resolved_success', notes: resolveNotes })
      });
      if (res.ok) fetchTrace();
    } catch (e) {
      setUnknownOutcomes(prev => prev.map(u => u.stepId === stepId ? { ...u, status: 'resolved_success', resolutionNotes: resolveNotes } : u));
    }
  };

  return (
    <div className="space-y-6">
      {/* Execution Top Bar */}
      <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl text-white space-y-4">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <div className="flex items-center gap-3">
              <div className="p-2 bg-indigo-500/20 text-indigo-400 rounded-lg border border-indigo-500/30">
                <Cpu className="w-6 h-6" />
              </div>
              <div>
                <h1 className="text-xl font-bold tracking-tight flex items-center gap-2">
                  Agent Execution: <span className="font-mono text-indigo-400">{execution?.id}</span>
                </h1>
                <p className="text-xs text-slate-400">Durable cognitive execution instance & optimistic concurrency state v{execution?.version}</p>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <span className={`px-3 py-1 text-xs font-semibold rounded-full border ${
              execution?.status === 'running'
                ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                : execution?.status === 'paused'
                ? 'bg-amber-500/10 text-amber-400 border-amber-500/20'
                : 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20'
            }`}>
              {execution?.status.toUpperCase()}
            </span>

            {execution?.status === 'running' && (
              <button
                onClick={handlePause}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-amber-600/20 hover:bg-amber-600/30 text-amber-300 text-xs font-medium rounded-lg transition border border-amber-500/30"
              >
                <Pause className="w-3.5 h-3.5" /> Pause
              </button>
            )}

            {execution?.status === 'paused' && (
              <button
                onClick={handleResume}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-emerald-600/20 hover:bg-emerald-600/30 text-emerald-300 text-xs font-medium rounded-lg transition border border-emerald-500/30"
              >
                <Play className="w-3.5 h-3.5" /> Resume
              </button>
            )}

            <button
              onClick={handleCancel}
              className="flex items-center gap-1.5 px-3 py-1.5 bg-rose-600/20 hover:bg-rose-600/30 text-rose-300 text-xs font-medium rounded-lg transition border border-rose-500/30"
            >
              <Square className="w-3.5 h-3.5" /> Cancel
            </button>
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs border-t border-slate-800 pt-4 text-slate-400">
          <div>Agent ID: <span className="text-slate-200 font-mono">{execution?.agentId}</span></div>
          <div>Mission ID: <span className="text-slate-200 font-mono">{execution?.missionId || 'N/A'}</span></div>
          <div>Total Steps: <span className="text-slate-200 font-mono">{steps.length}</span></div>
          <div>Checkpoints: <span className="text-slate-200 font-mono">{checkpoints.length}</span></div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
        <button
          onClick={() => setActiveTab('timeline')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition ${
            activeTab === 'timeline' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Step Execution Timeline
        </button>
        <button
          onClick={() => setActiveTab('checkpoints')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition ${
            activeTab === 'checkpoints' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Immutable Checkpoints ({checkpoints.length})
        </button>
        <button
          onClick={() => setActiveTab('unknown')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition ${
            activeTab === 'unknown' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Unknown Outcomes ({unknownOutcomes.length})
        </button>
      </div>

      {/* Tab: Step Execution Timeline */}
      {activeTab === 'timeline' && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
          <h2 className="text-base font-semibold text-white">Execution Steps & Model Gateway Calls</h2>
          <div className="space-y-3">
            {steps.map((s, idx) => (
              <div key={s.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono text-slate-500">#{idx + 1}</span>
                    <span className="font-semibold text-white text-sm">{s.stepType}</span>
                    <span className="text-xs text-slate-400 font-mono">({s.id})</span>
                  </div>
                  <span className={`px-2 py-0.5 text-xs font-medium rounded ${
                    s.status === 'completed' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                  }`}>
                    {s.status}
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs font-mono bg-slate-900 p-2.5 rounded text-slate-300">
                  <div>Input: {JSON.stringify(s.inputReference)}</div>
                  <div>Output: {s.outputReference ? JSON.stringify(s.outputReference) : 'In Progress...'}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab: Checkpoints */}
      {activeTab === 'checkpoints' && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-950 text-slate-400 text-xs uppercase border-b border-slate-800">
              <tr>
                <th className="p-4">Checkpoint ID</th>
                <th className="p-4">Version</th>
                <th className="p-4">Reason</th>
                <th className="p-4">Created At</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {checkpoints.map((c) => (
                <tr key={c.id} className="hover:bg-slate-800/50">
                  <td className="p-4 font-mono text-xs text-slate-200">{c.id}</td>
                  <td className="p-4 font-mono text-indigo-400">v{c.executionVersion}</td>
                  <td className="p-4">
                    <span className="px-2 py-0.5 text-xs bg-slate-800 text-slate-300 rounded border border-slate-700">
                      {c.reason}
                    </span>
                  </td>
                  <td className="p-4 text-xs text-slate-400 font-mono">{c.createdAt}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Tab: Unknown Outcomes */}
      {activeTab === 'unknown' && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
          <h2 className="text-base font-semibold text-white flex items-center gap-2">
            <AlertCircle className="w-5 h-5 text-amber-400" /> Side-Effect Crash Resolution (Unknown Outcomes)
          </h2>

          {unknownOutcomes.length === 0 ? (
            <div className="p-6 text-center text-slate-500 text-xs bg-slate-950 rounded-lg border border-slate-800">
              No unresolved side-effect crashes recorded. Agent execution state is fully consistent.
            </div>
          ) : (
            unknownOutcomes.map((u) => (
              <div key={u.id} className="p-4 bg-slate-950 border border-amber-500/30 rounded-lg space-y-3">
                <div className="flex items-center justify-between text-xs text-slate-300">
                  <span className="font-semibold text-amber-400">Step: {u.stepId} ({u.actionType})</span>
                  <span className="font-mono text-slate-500">Key: {u.idempotencyKey}</span>
                </div>

                <div className="text-xs text-slate-400">
                  Resolution Status: <span className="text-white font-semibold">{u.status}</span>
                </div>

                {u.status === 'unresolved' && (
                  <div className="space-y-2">
                    <input
                      type="text"
                      value={resolveNotes}
                      onChange={(e) => setResolveNotes(e.target.value)}
                      className="w-full bg-slate-900 border border-slate-800 rounded px-3 py-1.5 text-xs text-slate-200"
                    />
                    <button
                      onClick={() => handleResolveUnknown(u.stepId)}
                      className="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-medium rounded transition"
                    >
                      Resolve Outcome
                    </button>
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
};
