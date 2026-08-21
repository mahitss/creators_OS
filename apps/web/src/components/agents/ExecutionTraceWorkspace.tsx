'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { AgentRun, AgentObservation, AgentEvent } from '@vapor/types';
import {
  fetchAgentRun,
  pauseAgentRun,
  resumeAgentRun,
  cancelAgentRun,
} from '../../lib/api/agents';
import { Card, Typography, Badge, Button, Spinner } from '@vapor/ui';

interface ExecutionTraceWorkspaceProps {
  runId?: string;
  executionId?: string;
}

export const ExecutionTraceWorkspace: React.FC<ExecutionTraceWorkspaceProps> = ({ runId, executionId }) => {
  const activeId = runId || executionId;
  const [run, setRun] = useState<(AgentRun & { observations: AgentObservation[]; events: AgentEvent[] }) | null>(null);
  const [selectedObservation, setSelectedObservation] = useState<AgentObservation | null>(null);
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

  const statusVariantMap: Record<string, 'default' | 'emerald' | 'amber' | 'crimson' | 'cyan'> = {
    INITIALIZING: 'cyan',
    PLANNING: 'cyan',
    EXECUTING: 'cyan',
    WAITING_TOOL: 'amber',
    OBSERVING: 'cyan',
    COMPLETED: 'emerald',
    FAILED: 'crimson',
    CANCELLED: 'default',
    TIMED_OUT: 'crimson',
    QUEUED: 'default',
  };

  if (!runId) {
    return (
      <div className="p-8 text-center border border-[rgba(255,255,255,0.08)] rounded-lg bg-[#070707] text-[#A3A3A3] font-mono text-xs">
        No active AgentRun specified for execution trace analysis.
      </div>
    );
  }

  if (isLoading && !run) {
    return (
      <div className="flex flex-col items-center justify-center p-16 gap-3">
        <Spinner size="md" />
        <Typography variant="caption" className="text-[#777777] font-mono text-xs">
          Loading live agent runtime telemetry...
        </Typography>
      </div>
    );
  }

  if (!run) {
    return (
      <div className="p-8 text-center border border-rose-500/20 bg-rose-500/5 rounded-lg text-rose-400 font-mono text-xs">
        AgentRun '{runId}' not found.
      </div>
    );
  }

  const isTerminal = ['COMPLETED', 'FAILED', 'CANCELLED', 'TIMED_OUT'].includes(run.status);

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-5 text-[#F5F5F5]">
      {/* Top Telemetry Strip */}
      <div className="flex flex-col md:flex-row md:items-center justify-between border-b border-[rgba(255,255,255,0.08)] pb-4 gap-4">
        <div>
          <div className="flex items-center gap-2">
            <Typography variant="caption" className="text-[#62E6B2] font-mono text-xs">
              AGENT RUNTIME EXECUTION TRACE
            </Typography>
            <Badge variant="cyan">
              v{run.agentVersionId?.slice(-2) || '1'}
            </Badge>
          </div>
          <Typography variant="h2" className="text-base font-bold font-mono text-[#F5F5F5] mt-0.5">
            Run: {run.id}
          </Typography>
        </div>

        {/* Action Controls & Status */}
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
          <div className="text-sm font-bold text-[#F5F5F5] mt-1">{run.currentStep}</div>
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
          <div className="text-[#777777] text-[10px] uppercase">Observations</div>
          <div className="text-sm font-bold text-[#F5F5F5] mt-1">{run.observations?.length || 0}</div>
        </Card>
      </div>

      {/* Main Trace & Inspector Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 font-mono text-xs">
        {/* Left Column: Timeline Events */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <Typography variant="caption" className="text-[#A3A3A3] text-xs font-semibold uppercase">
              Execution Timeline ({run.events?.length || 0} events)
            </Typography>
          </div>

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
                    {JSON.stringify(evt.payload)}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Right Column: Step Observations & Payload Inspector */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <Typography variant="caption" className="text-[#A3A3A3] text-xs font-semibold uppercase">
              Step Observations ({run.observations?.length || 0})
            </Typography>
          </div>

          <div className="space-y-2 max-h-[250px] overflow-y-auto pr-1">
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

          {/* Selected Observation Raw Payload Inspector */}
          {selectedObservation && (
            <div className="p-4 bg-[#050505] border border-[rgba(255,255,255,0.08)] rounded space-y-2">
              <div className="flex items-center justify-between border-b border-[rgba(255,255,255,0.06)] pb-2">
                <span className="text-[#62E6B2] font-bold">
                  Observation Inspector (Step {selectedObservation.stepNumber})
                </span>
                <span className="text-[#555555] text-[10px]">ID: {selectedObservation.id.slice(0, 8)}</span>
              </div>
              <div className="text-xs text-[#F5F5F5]">{selectedObservation.summary}</div>
              <div className="text-[#A3A3A3] text-[11px] bg-[#020202] p-2.5 rounded border border-[rgba(255,255,255,0.04)] max-h-[200px] overflow-y-auto">
                <pre>{JSON.stringify(selectedObservation.rawData || {}, null, 2)}</pre>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
