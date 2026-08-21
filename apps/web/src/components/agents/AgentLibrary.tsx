'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { Agent, AgentVersion, AgentRun } from '@vapor/types';
import {
  fetchAgents,
  pauseAgent,
  resumeAgent,
  disableAgent,
  createAgentRun,
  fetchAgentVersions,
} from '../../lib/api/agents';
import { Card, Typography, Badge, Button, Spinner } from '@vapor/ui';

export const AgentLibrary: React.FC = () => {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);
  const [versions, setVersions] = useState<AgentVersion[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isActionLoading, setIsActionLoading] = useState(false);
  const [showRunModal, setShowRunModal] = useState(false);
  const [showVersionsModal, setShowVersionsModal] = useState(false);
  const [runGoal, setRunGoal] = useState('');
  const [feedbackMsg, setFeedbackMsg] = useState<string | null>(null);

  const loadAgents = useCallback(async () => {
    setIsLoading(true);
    try {
      const data = await fetchAgents();
      setAgents(data);
    } catch (err) {
      console.error('Failed to load agents:', err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadAgents();
  }, [loadAgents]);

  const handleToggleStatus = async (agent: Agent) => {
    setIsActionLoading(true);
    setFeedbackMsg(null);
    try {
      if (agent.status === 'ACTIVE') {
        await pauseAgent(agent.id);
        setFeedbackMsg(`Agent '${agent.name}' paused.`);
      } else if (agent.status === 'PAUSED') {
        await resumeAgent(agent.id);
        setFeedbackMsg(`Agent '${agent.name}' resumed.`);
      } else if (agent.status === 'DISABLED') {
        await resumeAgent(agent.id);
        setFeedbackMsg(`Agent '${agent.name}' enabled.`);
      }
      await loadAgents();
    } catch (err: any) {
      setFeedbackMsg(err.message || 'Status transition failed.');
    } finally {
      setIsActionLoading(false);
    }
  };

  const handleDisable = async (agent: Agent) => {
    setIsActionLoading(true);
    try {
      await disableAgent(agent.id);
      setFeedbackMsg(`Agent '${agent.name}' disabled.`);
      await loadAgents();
    } catch (err: any) {
      setFeedbackMsg(err.message || 'Disable action failed.');
    } finally {
      setIsActionLoading(false);
    }
  };

  const handleOpenVersions = async (agent: Agent) => {
    setSelectedAgent(agent);
    setShowVersionsModal(true);
    try {
      const v = await fetchAgentVersions(agent.id);
      setVersions(v);
    } catch (err) {
      console.error('Failed to load versions:', err);
    }
  };

  const handleLaunchRun = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedAgent || !runGoal.trim()) return;
    setIsActionLoading(true);
    setFeedbackMsg(null);
    try {
      const run = await createAgentRun({
        agent_id: selectedAgent.id,
        goal: runGoal.trim(),
      });
      setFeedbackMsg(`AgentRun '${run.id}' started successfully.`);
      setShowRunModal(false);
      setRunGoal('');
      await loadAgents();
    } catch (err: any) {
      setFeedbackMsg(err.message || 'Run execution failed.');
    } finally {
      setIsActionLoading(false);
    }
  };

  const statusVariantMap: Record<string, 'default' | 'emerald' | 'amber' | 'crimson' | 'cyan'> = {
    ACTIVE: 'emerald',
    PAUSED: 'amber',
    DISABLED: 'crimson',
    ARCHIVED: 'default',
    DRAFT: 'default',
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6 text-[#F5F5F5]">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-[rgba(255,255,255,0.08)] pb-5">
        <div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-[#62E6B2]" />
            <Typography variant="h1" className="text-xl font-bold font-mono tracking-tight text-[#F5F5F5]">
              Autonomous Agent Registry
            </Typography>
          </div>
          <Typography variant="caption" className="text-[#A3A3A3] font-mono text-xs mt-1">
            Governed AI agent execution runtimes, immutable versions, and permission boundaries.
          </Typography>
        </div>
      </div>

      {feedbackMsg && (
        <div className="p-3 bg-[#12141C] border border-[rgba(255,255,255,0.12)] rounded-md text-xs font-mono text-[#62E6B2] flex items-center justify-between">
          <span>{feedbackMsg}</span>
          <button onClick={() => setFeedbackMsg(null)} className="text-[#A3A3A3] hover:text-[#F5F5F5]">✕</button>
        </div>
      )}

      {/* Agents Grid */}
      {isLoading ? (
        <div className="flex flex-col items-center justify-center p-16 gap-3">
          <Spinner size="md" />
          <Typography variant="caption" className="text-[#777777] font-mono text-xs">
            Loading governed agent definitions...
          </Typography>
        </div>
      ) : agents.length === 0 ? (
        <div className="p-12 text-center border border-[rgba(255,255,255,0.08)] rounded-lg bg-[#070707]">
          <Typography variant="body" className="text-[#A3A3A3] font-mono text-sm">
            No agents registered in this workspace.
          </Typography>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {agents.map((ag) => {
            const isExecutable = ag.status === 'ACTIVE' || ag.status === 'PAUSED';
            return (
              <Card
                key={ag.id}
                variant="panel"
                className="p-5 flex flex-col justify-between border-[rgba(255,255,255,0.08)] bg-[#070707] hover:border-[rgba(255,255,255,0.18)] transition-all rounded-lg"
              >
                <div className="space-y-3">
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <div className="flex items-center gap-2">
                        <Typography variant="h3" className="text-sm font-bold font-mono text-[#F5F5F5]">
                          {ag.name}
                        </Typography>
                        <Badge variant="cyan">
                          v{ag.currentVersion || 1}
                        </Badge>
                      </div>
                      <Typography variant="caption" className="text-[#858585] text-xs line-clamp-2 mt-1">
                        {ag.description}
                      </Typography>
                    </div>
                    <Badge variant={statusVariantMap[ag.status] || 'default'}>
                      {ag.status}
                    </Badge>
                  </div>

                  {/* Capabilities & Tools */}
                  <div className="space-y-1.5 pt-2 border-t border-[rgba(255,255,255,0.06)] text-xs font-mono">
                    <div className="flex items-center justify-between text-[#858585]">
                      <span>Authorized Tools:</span>
                      <span className="text-[#F5F5F5] font-semibold">{ag.allowedTools?.length || 0} tools</span>
                    </div>
                    <div className="flex items-center justify-between text-[#858585]">
                      <span>Max Steps:</span>
                      <span className="text-[#F5F5F5]">{ag.maxSteps || 20}</span>
                    </div>
                    <div className="flex items-center justify-between text-[#858585]">
                      <span>Token Ceiling:</span>
                      <span className="text-[#F5F5F5]">{(ag.maxTokenBudget || 100000).toLocaleString()}</span>
                    </div>
                    <div className="flex items-center justify-between text-[#858585]">
                      <span>Total Executions:</span>
                      <span className="text-[#62E6B2]">{ag.totalRuns ?? ag.total_runs ?? 0} runs</span>
                    </div>
                  </div>

                  {/* Capabilities Badges */}
                  <div className="flex flex-wrap gap-1 pt-1">
                    {(ag.capabilities || []).map((cap) => (
                      <span
                        key={cap}
                        className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-[#111111] text-[#A3A3A3] border border-[rgba(255,255,255,0.06)]"
                      >
                        {cap}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Actions Bar */}
                <div className="flex items-center justify-between pt-4 mt-3 border-t border-[rgba(255,255,255,0.08)] gap-2">
                  <div className="flex items-center gap-1.5">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleOpenVersions(ag)}
                      className="text-xs font-mono"
                    >
                      History
                    </Button>
                    {ag.status === 'ACTIVE' && (
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleToggleStatus(ag)}
                        disabled={isActionLoading}
                        className="text-xs font-mono"
                      >
                        Pause
                      </Button>
                    )}
                    {ag.status === 'PAUSED' && (
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleToggleStatus(ag)}
                        disabled={isActionLoading}
                        className="text-xs font-mono text-[#62E6B2]"
                      >
                        Resume
                      </Button>
                    )}
                    {ag.status !== 'DISABLED' && ag.status !== 'ARCHIVED' && (
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleDisable(ag)}
                        disabled={isActionLoading}
                        className="text-xs font-mono text-rose-400"
                      >
                        Disable
                      </Button>
                    )}
                  </div>

                  <Button
                    variant="primary"
                    size="sm"
                    disabled={!isExecutable || isActionLoading}
                    onClick={() => {
                      setSelectedAgent(ag);
                      setShowRunModal(true);
                    }}
                    className="font-mono text-xs"
                  >
                    Execute Run →
                  </Button>
                </div>
              </Card>
            );
          })}
        </div>
      )}

      {/* Launch Agent Run Modal */}
      {showRunModal && selectedAgent && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#0A0A0A] border border-[rgba(255,255,255,0.12)] rounded-lg max-w-lg w-full p-6 space-y-4 shadow-2xl">
            <div className="border-b border-[rgba(255,255,255,0.08)] pb-3 flex items-center justify-between">
              <div>
                <Typography variant="caption" className="text-[#62E6B2] font-mono text-xs">
                  EXECUTE AUTONOMOUS AGENT RUN
                </Typography>
                <Typography variant="h2" className="text-lg font-bold font-mono text-[#F5F5F5]">
                  {selectedAgent.name} (v{selectedAgent.currentVersion || 1})
                </Typography>
              </div>
              <button onClick={() => setShowRunModal(false)} className="text-[#777777] hover:text-[#F5F5F5]">✕</button>
            </div>

            <form onSubmit={handleLaunchRun} className="space-y-4">
              <div className="space-y-1.5">
                <label className="text-xs text-[#A3A3A3] font-mono">Run Objective & Task Goal</label>
                <textarea
                  required
                  rows={4}
                  value={runGoal}
                  onChange={(e) => setRunGoal(e.target.value)}
                  placeholder="Specify the clear objective for this autonomous execution run..."
                  className="w-full p-2.5 bg-[#050505] border border-[rgba(255,255,255,0.10)] rounded text-xs text-[#F5F5F5] font-mono focus:outline-none focus:border-[rgba(255,255,255,0.25)]"
                />
              </div>

              <div className="p-3 bg-[#070707] border border-[rgba(255,255,255,0.06)] rounded text-xs font-mono space-y-1 text-[#858585]">
                <div className="text-[#A3A3A3] font-semibold">Execution Constraints:</div>
                <div>• Max Steps: {selectedAgent.maxSteps || 20}</div>
                <div>• Max Runtime: {selectedAgent.maxRuntimeSeconds || 300}s</div>
                <div>• Token Ceiling: {(selectedAgent.maxTokenBudget || 100000).toLocaleString()} tokens</div>
              </div>

              <div className="flex items-center justify-end gap-2 pt-3 border-t border-[rgba(255,255,255,0.08)]">
                <Button variant="ghost" size="sm" onClick={() => setShowRunModal(false)}>
                  Cancel
                </Button>
                <Button variant="primary" size="sm" type="submit" isLoading={isActionLoading}>
                  Start Agent Run
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Version History Modal */}
      {showVersionsModal && selectedAgent && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#0A0A0A] border border-[rgba(255,255,255,0.12)] rounded-lg max-w-2xl w-full p-6 space-y-4 shadow-2xl max-h-[85vh] flex flex-col">
            <div className="border-b border-[rgba(255,255,255,0.08)] pb-3 flex items-center justify-between shrink-0">
              <div>
                <Typography variant="caption" className="text-[#62E6B2] font-mono text-xs">
                  IMMUTABLE VERSION HISTORY
                </Typography>
                <Typography variant="h2" className="text-lg font-bold font-mono text-[#F5F5F5]">
                  {selectedAgent.name}
                </Typography>
              </div>
              <button onClick={() => setShowVersionsModal(false)} className="text-[#777777] hover:text-[#F5F5F5]">✕</button>
            </div>

            <div className="overflow-y-auto space-y-3 flex-1 pr-1 font-mono text-xs">
              {versions.map((ver) => (
                <div
                  key={ver.id}
                  className="p-3.5 bg-[#070707] border border-[rgba(255,255,255,0.08)] rounded-md space-y-2"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Badge variant="cyan">
                        Version v{ver.version}
                      </Badge>
                      <span className="text-[#777777] text-[11px]">{new Date(ver.createdAt).toLocaleString()}</span>
                    </div>
                    <span className="text-[#555555] text-[10px]">ID: {ver.id.slice(0, 8)}</span>
                  </div>
                  <div className="text-[#A3A3A3] text-xs bg-[#050505] p-2 rounded border border-[rgba(255,255,255,0.04)] whitespace-pre-wrap">
                    {ver.instructions}
                  </div>
                </div>
              ))}
            </div>

            <div className="flex justify-end pt-3 border-t border-[rgba(255,255,255,0.08)] shrink-0">
              <Button variant="ghost" size="sm" onClick={() => setShowVersionsModal(false)}>
                Close
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
