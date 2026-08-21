'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { AgentRun, AgentObservation, AgentEvent, ToolCallAuditLog, ContextSnapshot } from '@vapor/types';
import {
  fetchAgentRun,
  pauseAgentRun,
  resumeAgentRun,
  cancelAgentRun,
} from '../../lib/api/agents';
import {
  listToolAuditLogs,
  getContextSnapshot
} from '../../lib/api/tools';
import { Card, Typography, Badge, Button, Spinner } from '@vapor/ui';

interface ExecutionTraceWorkspaceProps {
  runId?: string;
  executionId?: string;
}

export const ExecutionTraceWorkspace: React.FC<ExecutionTraceWorkspaceProps> = ({ runId, executionId }) => {
  const activeId = runId || executionId;
  const [run, setRun] = useState<(AgentRun & { observations: AgentObservation[]; events: AgentEvent[] }) | null>(null);
  const [selectedObservation, setSelectedObservation] = useState<AgentObservation | null>(null);
  const [auditLogs, setAuditLogs] = useState<ToolCallAuditLog[]>([]);
  const [contextSnapshot, setContextSnapshot] = useState<ContextSnapshot | null>(null);
  const [activeTab, setActiveTab] = useState<'timeline' | 'observations' | 'tools' | 'snapshot'>('timeline');
  const [isLoading, setIsLoading] = useState(true);
  const [isActionLoading, setIsActionLoading] = useState(false);
  const [autoRefresh, setAutoRefresh] = useState(true);

  const loadRun = useCallback(async () => {
    if (!activeId) return;
    try {
      const data = await fetchAgentRun(activeId);
      setRun(data);
      if (data.observations?.length && !selectedObservation) {
        setSelectedObservation(data.observations[data.observations.length - 1]);
      }

      // Fetch audit logs for this run
      try {
        const auditRes = await listToolAuditLogs({ agentRunId: activeId });
        setAuditLogs(auditRes.logs || []);
      } catch (err) {
        // Audit logs non-critical
      }

      // Fetch context snapshot
      try {
        const snap = await getContextSnapshot(activeId);
        setContextSnapshot(snap);
      } catch (err) {
        // Snapshot non-critical
      }
    } catch (err) {
      console.error('Failed to load AgentRun trace:', err);
    } finally {
      setIsLoading(false);
    }
  }, [activeId, selectedObservation]);

  useEffect(() => {
    loadRun();
    if (!autoRefresh || !activeId) return;
    const interval = setInterval(() => {
      loadRun();
    }, 2000);
    return () => clearInterval(interval);
  }, [loadRun, autoRefresh, activeId]);

  const handlePause = async () => {
    if (!activeId) return;
    setIsActionLoading(true);
    try {
      await pauseAgentRun(activeId);
      await loadRun();
    } catch (err) {
      console.error('Pause failed:', err);
    } finally {
      setIsActionLoading(false);
    }
  };

  const handleResume = async () => {
    if (!activeId) return;
    setIsActionLoading(true);
    try {
      await resumeAgentRun(activeId);
      await loadRun();
    } catch (err) {
      console.error('Resume failed:', err);
    } finally {
      setIsActionLoading(false);
    }
  };

  const handleCancel = async () => {
    if (!activeId) return;
    setIsActionLoading(true);
    try {
      await cancelAgentRun(activeId);
      await loadRun();
    } catch (err) {
      console.error('Cancel failed:', err);
    } finally {
      setIsActionLoading(false);
    }
  };

  if (isLoading && !run) {
    return (
      <div className="py-20 flex flex-col items-center justify-center space-y-3">
        <Spinner size="lg" />
        <span className="text-xs font-mono text-[#777777]">Loading Execution Trace & Citations...</span>
      </div>
    );
  }

  if (!run) {
    return (
      <Card variant="panel" className="p-8 text-center border-dashed font-mono">
        <Typography variant="body" className="text-xs text-[#777777]">
          No execution trace found for run ID: {activeId || 'unspecified'}
        </Typography>
      </Card>
    );
  }

  const isTerminal = ['COMPLETED', 'FAILED', 'CANCELLED', 'TIMED_OUT'].includes(run.status);

  const statusVariantMap: Record<string, 'emerald' | 'amber' | 'crimson' | 'cyan' | 'default'> = {
    QUEUED: 'cyan',
    INITIALIZING: 'cyan',
    EXECUTING: 'emerald',
    WAITING_TOOL: 'amber',
    COMPLETED: 'emerald',
    FAILED: 'crimson',
    CANCELLED: 'default',
    PAUSED: 'amber',
    TIMED_OUT: 'crimson',
  };

  return (
    <div className="space-y-5 font-mono">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-4 bg-[#070707] border border-[rgba(255,255,255,0.08)] rounded-lg">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <Typography variant="caption" className="text-[#62E6B2] text-xs font-semibold uppercase">
              AGENT EXECUTION TRACE
            </Typography>
            <span className="text-[#555555] text-xs">|</span>
            <span className="text-[#858585] text-xs">Run: {run.id.slice(0, 12)}</span>
            <span className="text-[#555555] text-xs">|</span>
            <span className="text-[#858585] text-xs">Agent: {run.agentId}</span>
          </div>
          <div className="text-sm font-bold text-[#F5F5F5]">{run.goal}</div>
        </div>

        <div className="flex items-center gap-2">
          <Badge variant={statusVariantMap[run.status] || 'default'}>
            {run.status}
          </Badge>
          {!isTerminal && (
            <>
              {run.status === 'WAITING_TOOL' ? (
                <Button variant="ghost" size="sm" onClick={handleResume} disabled={isActionLoading} className="text-xs font-mono text-[#62E6B2]">
                  Resume
                </Button>
              ) : (
                <Button variant="ghost" size="sm" onClick={handlePause} disabled={isActionLoading} className="text-xs font-mono">
                  Pause
                </Button>
              )}
              <Button variant="ghost" size="sm" onClick={handleCancel} disabled={isActionLoading} className="text-xs font-mono text-rose-400">
                Cancel
              </Button>
            </>
          )}
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setAutoRefresh(!autoRefresh)}
            className={`text-[10px] font-mono ${autoRefresh ? 'text-[#62E6B2]' : 'text-[#777777]'}`}
          >
            {autoRefresh ? '● LIVE' : '○ PAUSED'}
          </Button>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3 font-mono text-xs">
        <Card variant="panel" className="p-3 bg-[#070707] border-[rgba(255,255,255,0.06)] rounded">
          <div className="text-[#777777] text-[10px] uppercase">Current Step</div>
          <div className="text-sm font-bold text-[#F5F5F5] mt-1">{run.currentStep} / {run.maxSteps || 20}</div>
        </Card>
        <Card variant="panel" className="p-3 bg-[#070707] border-[rgba(255,255,255,0.06)] rounded">
          <div className="text-[#777777] text-[10px] uppercase">Total Tokens</div>
          <div className="text-sm font-bold text-[#62E6B2] mt-1">{(run.totalTokens || 0).toLocaleString()}</div>
        </Card>
        <Card variant="panel" className="p-3 bg-[#070707] border-[rgba(255,255,255,0.06)] rounded">
          <div className="text-[#777777] text-[10px] uppercase">Model Cost</div>
          <div className="text-sm font-bold text-[#F5F5F5] mt-1">${(run.costUsd || 0).toFixed(4)}</div>
        </Card>
        <Card variant="panel" className="p-3 bg-[#070707] border-[rgba(255,255,255,0.06)] rounded">
          <div className="text-[#777777] text-[10px] uppercase">Duration</div>
          <div className="text-sm font-bold text-[#F5F5F5] mt-1">{(run.durationMs / 1000).toFixed(1)}s</div>
        </Card>
        <Card variant="panel" className="p-3 bg-[#070707] border-[rgba(255,255,255,0.06)] rounded">
          <div className="text-[#777777] text-[10px] uppercase">Tool Invocations</div>
          <div className="text-sm font-bold text-[#F5F5F5] mt-1">{auditLogs.length} logged</div>
        </Card>
      </div>

      {/* Tabs Navigation */}
      <div className="flex items-center gap-2 border-b border-[rgba(255,255,255,0.08)] pb-2 text-xs">
        <button
          onClick={() => setActiveTab('timeline')}
          className={`px-3 py-1.5 rounded font-mono transition-all ${
            activeTab === 'timeline'
              ? 'bg-[#11141E] text-[#62E6B2] border border-[#62E6B2]/40 font-bold'
              : 'text-[#858585] hover:text-[#F5F5F5]'
          }`}
        >
          Timeline ({run.events?.length || 0})
        </button>
        <button
          onClick={() => setActiveTab('observations')}
          className={`px-3 py-1.5 rounded font-mono transition-all ${
            activeTab === 'observations'
              ? 'bg-[#11141E] text-[#62E6B2] border border-[#62E6B2]/40 font-bold'
              : 'text-[#858585] hover:text-[#F5F5F5]'
          }`}
        >
          Step Observations ({run.observations?.length || 0})
        </button>
        <button
          onClick={() => setActiveTab('tools')}
          className={`px-3 py-1.5 rounded font-mono transition-all ${
            activeTab === 'tools'
              ? 'bg-[#11141E] text-[#62E6B2] border border-[#62E6B2]/40 font-bold'
              : 'text-[#858585] hover:text-[#F5F5F5]'
          }`}
        >
          Tool Audit Logs ({auditLogs.length})
        </button>
        <button
          onClick={() => setActiveTab('snapshot')}
          className={`px-3 py-1.5 rounded font-mono transition-all ${
            activeTab === 'snapshot'
              ? 'bg-[#11141E] text-[#62E6B2] border border-[#62E6B2]/40 font-bold'
              : 'text-[#858585] hover:text-[#F5F5F5]'
          }`}
        >
          Context Snapshot {contextSnapshot ? '✓' : ''}
        </button>
      </div>

      {/* Main Tab Content Grid */}
      {activeTab === 'timeline' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 font-mono text-xs">
          {/* Left Column: Timeline Events */}
          <div className="space-y-3">
            <Typography variant="caption" className="text-[#A3A3A3] text-xs font-semibold uppercase">
              Chronological Event Stream
            </Typography>

            <div className="space-y-2 max-h-[550px] overflow-y-auto pr-1">
              {(run.events || []).map((evt) => (
                <div
                  key={evt.id}
                  className="p-3 bg-[#070707] border border-[rgba(255,255,255,0.06)] rounded space-y-1 hover:border-[rgba(255,255,255,0.12)] transition-all"
                >
                  <div className="flex items-center justify-between text-[11px]">
                    <span className="text-[#62E6B2] font-semibold">{evt.eventType}</span>
                    <span className="text-[#555555] text-[10px]">{new Date(evt.timestamp).toLocaleTimeString()}</span>
                  </div>
                  {evt.payload && Object.keys(evt.payload).length > 0 && (
                    <div className="text-[#858585] text-[11px] bg-[#050505] p-2 rounded border border-[rgba(255,255,255,0.04)] overflow-x-auto">
                      <pre>{JSON.stringify(evt.payload, null, 2)}</pre>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Right Column: Active Step Details & Output */}
          <div className="space-y-3">
            <Typography variant="caption" className="text-[#A3A3A3] text-xs font-semibold uppercase">
              Active Step State & Final Result
            </Typography>

            <div className="p-4 bg-[#070707] border border-[rgba(255,255,255,0.06)] rounded space-y-3">
              <div className="flex items-center justify-between border-b border-[rgba(255,255,255,0.06)] pb-2">
                <span className="text-[#F5F5F5] font-bold">Execution Status</span>
                <Badge variant={statusVariantMap[run.status] || 'default'}>{run.status}</Badge>
              </div>

              {run.finalResult && (
                <div className="space-y-1">
                  <div className="text-[#62E6B2] font-semibold text-xs">Final Result Output:</div>
                  <div className="p-3 bg-[#050505] border border-[#62E6B2]/20 rounded text-xs text-[#F5F5F5] whitespace-pre-wrap">
                    {run.finalResult}
                  </div>
                </div>
              )}

              {run.errorMessage && (
                <div className="space-y-1">
                  <div className="text-rose-400 font-semibold text-xs">Error Description:</div>
                  <div className="p-3 bg-rose-950/40 border border-rose-800 rounded text-xs text-rose-200">
                    [{run.failureType}] {run.errorMessage}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {activeTab === 'observations' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 font-mono text-xs">
          {/* Observations List */}
          <div className="space-y-3">
            <Typography variant="caption" className="text-[#A3A3A3] text-xs font-semibold uppercase">
              Observations Stream ({run.observations?.length || 0})
            </Typography>

            <div className="space-y-2 max-h-[500px] overflow-y-auto pr-1">
              {(run.observations || []).map((obs) => (
                <div
                  key={obs.id}
                  onClick={() => setSelectedObservation(obs)}
                  className={`p-3 rounded border cursor-pointer transition-all ${
                    selectedObservation?.id === obs.id
                      ? 'bg-[#11141E] border-[#62E6B2]/40'
                      : 'bg-[#070707] border-[rgba(255,255,255,0.06)] hover:border-[rgba(255,255,255,0.12)]'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="text-[#62E6B2] font-bold">Step {obs.stepNumber}</span>
                      <span className="text-[#A3A3A3]">{obs.toolName || obs.observationType}</span>
                    </div>
                    <Badge variant={obs.status === 'success' ? 'emerald' : obs.status === 'denied' ? 'amber' : 'crimson'}>
                      {obs.status}
                    </Badge>
                  </div>
                  <div className="text-[#777777] text-[11px] mt-1 line-clamp-1">{obs.summary}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Observation Payload Inspector */}
          {selectedObservation && (
            <div className="space-y-3">
              <Typography variant="caption" className="text-[#A3A3A3] text-xs font-semibold uppercase">
                Observation Inspector (Step {selectedObservation.stepNumber})
              </Typography>

              <div className="p-4 bg-[#050505] border border-[rgba(255,255,255,0.08)] rounded space-y-3">
                <div className="text-xs text-[#F5F5F5] font-semibold">{selectedObservation.summary}</div>

                <div className="space-y-1">
                  <span className="text-[#777777] text-[10px] uppercase">Raw Output Payload:</span>
                  <div className="text-[#A3A3A3] text-[11px] bg-[#020202] p-2.5 rounded border border-[rgba(255,255,255,0.04)] max-h-[350px] overflow-y-auto">
                    <pre>{JSON.stringify(selectedObservation.rawData || {}, null, 2)}</pre>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {activeTab === 'tools' && (
        <div className="space-y-3">
          <Typography variant="caption" className="text-[#A3A3A3] text-xs font-semibold uppercase">
            Governed Tool Invocations & Policy Audit Trail
          </Typography>

          {auditLogs.length === 0 ? (
            <div className="p-8 text-center bg-[#070707] border border-dashed rounded text-[#777777] text-xs">
              No tool calls executed during this agent run.
            </div>
          ) : (
            <div className="space-y-2">
              {auditLogs.map((l) => (
                <div
                  key={l.id}
                  className="p-3 bg-[#070707] border border-[rgba(255,255,255,0.06)] rounded space-y-2 text-xs"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="text-[#62E6B2] font-bold">{l.tool_name}</span>
                      <span className="text-[#777777] text-[10px]">({l.duration_ms}ms)</span>
                      {l.truncated && (
                        <span className="px-1 py-0.5 rounded text-[9px] bg-amber-950 text-amber-300 border border-amber-800">
                          TRUNCATED
                        </span>
                      )}
                    </div>
                    <Badge variant={l.status === 'SUCCESS' ? 'emerald' : l.status === 'DENIED' ? 'amber' : 'crimson'}>
                      {l.status}
                    </Badge>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-[11px]">
                    <div className="bg-[#050505] p-2 rounded border border-[rgba(255,255,255,0.04)]">
                      <div className="text-[#777777] text-[10px] uppercase mb-1">Sanitized Input (Secrets Redacted):</div>
                      <pre className="text-[#A3A3A3] overflow-x-auto max-h-[100px]">{JSON.stringify(l.input_sanitized || {}, null, 2)}</pre>
                    </div>
                    <div className="bg-[#050505] p-2 rounded border border-[rgba(255,255,255,0.04)]">
                      <div className="text-[#777777] text-[10px] uppercase mb-1">Output / Observations:</div>
                      <pre className="text-[#A3A3A3] overflow-x-auto max-h-[100px]">{JSON.stringify(l.output_summary || {}, null, 2)}</pre>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {activeTab === 'snapshot' && (
        <div className="space-y-3">
          <Typography variant="caption" className="text-[#A3A3A3] text-xs font-semibold uppercase">
            Reproducible Context Snapshot & Governance Provenance
          </Typography>

          {contextSnapshot ? (
            <div className="p-4 bg-[#070707] border border-[rgba(255,255,255,0.08)] rounded-lg space-y-3 text-xs">
              <div className="flex items-center justify-between border-b border-[rgba(255,255,255,0.06)] pb-2">
                <span className="text-[#F5F5F5] font-bold">Snapshot ID: {contextSnapshot.id}</span>
                <span className="text-[#62E6B2]">Policy Version: {contextSnapshot.policy_version}</span>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-[11px]">
                <div className="bg-[#050505] p-2.5 rounded border border-[rgba(255,255,255,0.04)]">
                  <div className="text-[#777777] text-[10px] uppercase">Memory IDs</div>
                  <div className="text-[#F5F5F5] font-bold mt-0.5">{contextSnapshot.memory_ids?.length || 0} loaded</div>
                </div>
                <div className="bg-[#050505] p-2.5 rounded border border-[rgba(255,255,255,0.04)]">
                  <div className="text-[#777777] text-[10px] uppercase">Knowledge IDs</div>
                  <div className="text-[#F5F5F5] font-bold mt-0.5">{contextSnapshot.knowledge_ids?.length || 0} chunks</div>
                </div>
                <div className="bg-[#050505] p-2.5 rounded border border-[rgba(255,255,255,0.04)]">
                  <div className="text-[#777777] text-[10px] uppercase">Document IDs</div>
                  <div className="text-[#F5F5F5] font-bold mt-0.5">{contextSnapshot.document_ids?.length || 0} files</div>
                </div>
                <div className="bg-[#050505] p-2.5 rounded border border-[rgba(255,255,255,0.04)]">
                  <div className="text-[#777777] text-[10px] uppercase">Estimated Tokens</div>
                  <div className="text-[#62E6B2] font-bold mt-0.5">{contextSnapshot.estimated_tokens?.toLocaleString() || 0}</div>
                </div>
              </div>

              {contextSnapshot.sources && contextSnapshot.sources.length > 0 && (
                <div className="space-y-1.5 pt-2">
                  <div className="text-[#A3A3A3] font-semibold text-xs">Referenced Context Sources:</div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                    {contextSnapshot.sources.map((s: any, idx: number) => (
                      <div key={idx} className="p-2 bg-[#050505] rounded border border-[rgba(255,255,255,0.04)] text-[11px] flex justify-between items-center">
                        <span className="text-[#F5F5F5]">{s.title || s.id}</span>
                        <span className="text-[10px] text-[#62E6B2] uppercase">[{s.type}]</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="p-8 text-center bg-[#070707] border border-dashed rounded text-[#777777] text-xs">
              No snapshot recorded for this run.
            </div>
          )}
        </div>
      )}
    </div>
  );
};
