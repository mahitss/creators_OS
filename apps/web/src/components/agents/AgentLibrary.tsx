'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { Agent, AgentVersion, AgentRun, ToolDefinition, ContextPreview } from '@vapor/types';
import {
  fetchAgents,
  pauseAgent,
  resumeAgent,
  disableAgent,
  createAgentRun,
  fetchAgentVersions,
} from '../../lib/api/agents';
import {
  discoverAgentTools,
  previewContext,
} from '../../lib/api/tools';
import { Card, Typography, Badge, Button, Spinner } from '@vapor/ui';

export const AgentLibrary: React.FC = () => {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);
  const [versions, setVersions] = useState<AgentVersion[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isActionLoading, setIsActionLoading] = useState(false);

  // Modals
  const [showRunModal, setShowRunModal] = useState(false);
  const [showVersionsModal, setShowVersionsModal] = useState(false);
  const [showToolsModal, setShowToolsModal] = useState(false);
  const [showContextModal, setShowContextModal] = useState(false);

  // Tools modal state
  const [agentTools, setAgentTools] = useState<{ authorized: ToolDefinition[]; denied: any[] }>({
    authorized: [],
    denied: []
  });
  const [toolsLoading, setToolsLoading] = useState(false);

  // Context preview modal state
  const [contextPreviewData, setContextPreviewData] = useState<ContextPreview | null>(null);
  const [contextGoal, setContextGoal] = useState('Analyze workspace missions and formulate strategic proposal.');
  const [contextLoading, setContextLoading] = useState(false);

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

  const handleOpenTools = async (agent: Agent) => {
    setSelectedAgent(agent);
    setShowToolsModal(true);
    setToolsLoading(true);
    try {
      const res = await discoverAgentTools(agent.id);
      setAgentTools({
        authorized: res.authorized_tools || [],
        denied: res.denied_tools || []
      });
    } catch (err) {
      console.error('Failed to discover agent tools:', err);
    } finally {
      setToolsLoading(false);
    }
  };

  const handleOpenContextPreview = async (agent: Agent) => {
    setSelectedAgent(agent);
    setShowContextModal(true);
    setContextLoading(true);
    try {
      const res = await previewContext({
        agent_id: agent.id,
        goal: contextGoal
      });
      setContextPreviewData(res);
    } catch (err) {
      console.error('Failed to preview context:', err);
    } finally {
      setContextLoading(false);
    }
  };

  const handleRefreshContext = async () => {
    if (!selectedAgent) return;
    setContextLoading(true);
    try {
      const res = await previewContext({
        agent_id: selectedAgent.id,
        goal: contextGoal
      });
      setContextPreviewData(res);
    } catch (err) {
      console.error('Failed to refresh context:', err);
    } finally {
      setContextLoading(false);
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
    } catch (err: any) {
      setFeedbackMsg(err.message || 'Run execution failed.');
    } finally {
      setIsActionLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-[rgba(255,255,255,0.08)] pb-4">
        <div>
          <Typography variant="h1" className="text-xl font-bold font-mono text-[#F5F5F5]">
            AGENT RUNTIME & TOOL FABRIC
          </Typography>
          <Typography variant="body" className="text-[#858585] text-xs font-mono mt-1">
            Governed autonomous agents, capability-aware tool discovery, and isolated context assembly.
          </Typography>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            size="sm"
            onClick={loadAgents}
            disabled={isLoading}
            className="font-mono text-xs text-[#A3A3A3]"
          >
            ↻ Refresh Registry
          </Button>
        </div>
      </div>

      {feedbackMsg && (
        <div className="p-3 bg-[#0B1510] border border-[#62E6B2]/30 rounded text-xs font-mono text-[#62E6B2] flex items-center justify-between">
          <span>{feedbackMsg}</span>
          <button onClick={() => setFeedbackMsg(null)} className="text-[#62E6B2]/60 hover:text-[#62E6B2]">✕</button>
        </div>
      )}

      {/* Agents Grid */}
      {isLoading ? (
        <div className="py-20 flex flex-col items-center justify-center space-y-3">
          <Spinner size="lg" />
          <span className="text-xs font-mono text-[#777777]">Loading Governed Agents...</span>
        </div>
      ) : agents.length === 0 ? (
        <Card variant="panel" className="py-16 text-center border-dashed">
          <Typography variant="body" className="text-[#777777] text-xs font-mono">
            No agents registered in this workspace catalog.
          </Typography>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {agents.map((ag) => {
            const isExecutable = ag.status === 'ACTIVE';

            return (
              <Card
                key={ag.id}
                variant="panel"
                className="flex flex-col justify-between p-5 bg-[#070707] border-[rgba(255,255,255,0.08)] hover:border-[rgba(255,255,255,0.16)] transition-all rounded-lg"
              >
                <div className="space-y-3">
                  {/* Top Bar */}
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <Typography variant="h3" className="text-sm font-bold font-mono text-[#F5F5F5] line-clamp-1">
                        {ag.name}
                      </Typography>
                      <div className="flex items-center gap-2 mt-1">
                        <Badge variant="cyan">
                          v{ag.currentVersion || 1}
                        </Badge>
                        <span className="text-[#666666] text-[10px] font-mono">
                          ID: {ag.id.slice(0, 8)}
                        </span>
                      </div>
                    </div>
                    <Badge
                      variant={
                        ag.status === 'ACTIVE'
                          ? 'emerald'
                          : ag.status === 'PAUSED'
                          ? 'amber'
                          : 'crimson'
                      }
                    >
                      {ag.status}
                    </Badge>
                  </div>

                  {/* Description */}
                  <Typography variant="body" className="text-xs text-[#858585] font-mono line-clamp-2 min-h-[32px]">
                    {ag.description || 'No system description configured.'}
                  </Typography>

                  {/* Metadata Stats */}
                  <div className="p-2.5 bg-[#050505] rounded border border-[rgba(255,255,255,0.04)] font-mono text-[11px] space-y-1 text-[#858585]">
                    <div className="flex justify-between">
                      <span>Max Steps:</span>
                      <span className="text-[#F5F5F5]">{ag.maxSteps || 20}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Allowed Tools:</span>
                      <span className="text-[#62E6B2]">{(ag.allowedTools || []).length} registered</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Total Runs:</span>
                      <span className="text-[#F5F5F5]">{ag.totalRuns ?? ag.total_runs ?? 0}</span>
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
                <div className="pt-4 mt-3 border-t border-[rgba(255,255,255,0.08)] space-y-2">
                  <div className="flex items-center justify-between gap-1.5">
                    <div className="flex items-center gap-1">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleOpenTools(ag)}
                        className="text-[11px] font-mono text-[#62E6B2] px-2 py-1 h-auto"
                      >
                        ⚡ Tools
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleOpenContextPreview(ag)}
                        className="text-[11px] font-mono text-[#A3A3A3] px-2 py-1 h-auto"
                      >
                        🔍 Context
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleOpenVersions(ag)}
                        className="text-[11px] font-mono text-[#777777] px-2 py-1 h-auto"
                      >
                        History
                      </Button>
                    </div>

                    <div className="flex items-center gap-1">
                      {ag.status === 'ACTIVE' && (
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleToggleStatus(ag)}
                          disabled={isActionLoading}
                          className="text-[11px] font-mono px-2 py-1 h-auto"
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
                          className="text-[11px] font-mono text-[#62E6B2] px-2 py-1 h-auto"
                        >
                          Resume
                        </Button>
                      )}
                    </div>
                  </div>

                  <Button
                    variant="primary"
                    size="sm"
                    disabled={!isExecutable || isActionLoading}
                    onClick={() => {
                      setSelectedAgent(ag);
                      setShowRunModal(true);
                    }}
                    className="w-full font-mono text-xs py-1.5"
                  >
                    Execute Agent Run →
                  </Button>
                </div>
              </Card>
            );
          })}
        </div>
      )}

      {/* Governed Tools & Capability Discovery Modal */}
      {showToolsModal && selectedAgent && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#0A0A0A] border border-[rgba(255,255,255,0.12)] rounded-lg max-w-2xl w-full p-6 space-y-4 shadow-2xl max-h-[85vh] flex flex-col">
            <div className="border-b border-[rgba(255,255,255,0.08)] pb-3 flex items-center justify-between shrink-0">
              <div>
                <Typography variant="caption" className="text-[#62E6B2] font-mono text-xs">
                  GOVERNED TOOL CATALOG & PERMISSIONS
                </Typography>
                <Typography variant="h2" className="text-lg font-bold font-mono text-[#F5F5F5]">
                  {selectedAgent.name} (v{selectedAgent.currentVersion || 1})
                </Typography>
              </div>
              <button onClick={() => setShowToolsModal(false)} className="text-[#777777] hover:text-[#F5F5F5]">✕</button>
            </div>

            {toolsLoading ? (
              <div className="py-12 flex flex-col items-center justify-center space-y-2">
                <Spinner size="md" />
                <span className="text-xs font-mono text-[#777777]">Evaluating Policy Engine & Tool Permissions...</span>
              </div>
            ) : (
              <div className="overflow-y-auto space-y-4 flex-1 pr-1 font-mono text-xs">
                {/* Authorized Tools */}
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-[#62E6B2] font-bold text-xs">
                    <span>Authorized Tools ({agentTools.authorized.length})</span>
                    <span className="text-[10px] text-[#777777]">Evaluated via PolicyEngine</span>
                  </div>
                  {agentTools.authorized.length === 0 ? (
                    <div className="p-3 bg-[#070707] rounded border border-[rgba(255,255,255,0.04)] text-[#777777]">
                      No tools permitted for this agent policy.
                    </div>
                  ) : (
                    <div className="grid grid-cols-1 gap-2">
                      {agentTools.authorized.map((t) => {
                        const riskColor =
                          t.risk_level === 'CRITICAL'
                            ? 'bg-red-950/60 border-red-800 text-red-300'
                            : t.risk_level === 'HIGH'
                            ? 'bg-amber-950/60 border-amber-800 text-amber-300'
                            : t.risk_level === 'MEDIUM'
                            ? 'bg-blue-950/60 border-blue-800 text-blue-300'
                            : 'bg-emerald-950/60 border-emerald-800 text-emerald-300';

                        return (
                          <div
                            key={t.id}
                            className="p-3 bg-[#070707] border border-[rgba(255,255,255,0.06)] rounded space-y-1.5"
                          >
                            <div className="flex items-center justify-between">
                              <div className="flex items-center gap-2">
                                <span className="text-[#F5F5F5] font-bold">{t.name}</span>
                                <span className="text-[10px] text-[#777777] uppercase">[{t.category}]</span>
                              </div>
                              <span className={`px-1.5 py-0.5 rounded text-[9px] border font-semibold ${riskColor}`}>
                                {t.risk_level} RISK
                              </span>
                            </div>
                            <div className="text-[#858585] text-[11px]">{t.description}</div>
                            <div className="flex items-center gap-3 text-[10px] text-[#555555] pt-1 border-t border-[rgba(255,255,255,0.04)]">
                              <span>Timeout: {t.timeout_seconds || 30}s</span>
                              <span>Permissions: {(t.required_permissions || []).join(', ') || 'read'}</span>
                              {t.risk_level === 'HIGH' || t.risk_level === 'CRITICAL' ? (
                                <span className="text-amber-400">⚠️ Requires Execution Approval</span>
                              ) : (
                                <span className="text-emerald-400">✓ Autonomous Execution</span>
                              )}
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  )}
                </div>

                {/* Denied / Restricted Tools */}
                {agentTools.denied.length > 0 && (
                  <div className="space-y-2 pt-2 border-t border-[rgba(255,255,255,0.06)]">
                    <div className="text-rose-400 font-bold text-xs">
                      Restricted Tools ({agentTools.denied.length})
                    </div>
                    <div className="grid grid-cols-1 gap-1.5">
                      {agentTools.denied.map((d: any) => (
                        <div
                          key={d.tool_id || d.name}
                          className="p-2.5 bg-[#0A0404] border border-rose-950/40 rounded flex items-center justify-between text-[11px]"
                        >
                          <div>
                            <span className="text-[#F5F5F5] font-semibold">{d.name}</span>
                            <span className="text-rose-400 text-[10px] ml-2">({d.reason})</span>
                          </div>
                          <span className="text-[9px] px-1.5 py-0.5 bg-rose-950/60 text-rose-300 rounded border border-rose-800">
                            BLOCKED
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            <div className="flex justify-end pt-3 border-t border-[rgba(255,255,255,0.08)] shrink-0">
              <Button variant="ghost" size="sm" onClick={() => setShowToolsModal(false)}>
                Close
              </Button>
            </div>
          </div>
        </div>
      )}

      {/* Context Assembler & Boundary Isolation Preview Modal */}
      {showContextModal && selectedAgent && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#0A0A0A] border border-[rgba(255,255,255,0.12)] rounded-lg max-w-3xl w-full p-6 space-y-4 shadow-2xl max-h-[90vh] flex flex-col">
            <div className="border-b border-[rgba(255,255,255,0.08)] pb-3 flex items-center justify-between shrink-0">
              <div>
                <Typography variant="caption" className="text-[#62E6B2] font-mono text-xs">
                  CONTEXT FABRIC & PROMPT BOUNDARY PREVIEW
                </Typography>
                <Typography variant="h2" className="text-lg font-bold font-mono text-[#F5F5F5]">
                  {selectedAgent.name} Context Preview
                </Typography>
              </div>
              <button onClick={() => setShowContextModal(false)} className="text-[#777777] hover:text-[#F5F5F5]">✕</button>
            </div>

            {/* Live Goal Input */}
            <div className="flex items-center gap-2 shrink-0">
              <input
                type="text"
                value={contextGoal}
                onChange={(e) => setContextGoal(e.target.value)}
                placeholder="Enter sample goal to preview assembled context..."
                className="flex-1 p-2 bg-[#050505] border border-[rgba(255,255,255,0.10)] rounded text-xs text-[#F5F5F5] font-mono focus:outline-none"
              />
              <Button variant="primary" size="sm" onClick={handleRefreshContext} disabled={contextLoading} className="font-mono text-xs">
                Assemble Context
              </Button>
            </div>

            {contextLoading ? (
              <div className="py-16 flex flex-col items-center justify-center space-y-2">
                <Spinner size="md" />
                <span className="text-xs font-mono text-[#777777]">Retrieving Authorized Memory & Assembling Prompt Boundaries...</span>
              </div>
            ) : contextPreviewData ? (
              <div className="overflow-y-auto space-y-4 flex-1 pr-1 font-mono text-xs">
                {/* Token Budget Summary */}
                {(() => {
                  const totalTokens = contextPreviewData.total_estimated_tokens ?? contextPreviewData.totalEstimatedTokens ?? 0;
                  const ceiling = contextPreviewData.token_ceiling ?? contextPreviewData.tokenCeiling ?? 16384;
                  const isExceeded = contextPreviewData.is_budget_exceeded ?? contextPreviewData.isBudgetExceeded ?? false;

                  return (
                    <div className="p-3 bg-[#070707] border border-[rgba(255,255,255,0.06)] rounded space-y-2">
                      <div className="flex items-center justify-between text-[11px]">
                        <span className="text-[#A3A3A3]">Token Consumption</span>
                        <span className="text-[#62E6B2] font-bold">
                          {totalTokens.toLocaleString()} / {ceiling.toLocaleString()} tokens
                        </span>
                      </div>
                      <div className="w-full bg-[#111111] h-1.5 rounded overflow-hidden">
                        <div
                          className={`h-full ${isExceeded ? 'bg-rose-500' : 'bg-[#62E6B2]'}`}
                          style={{
                            width: `${Math.min(100, (totalTokens / Math.max(1, ceiling)) * 100)}%`
                          }}
                        />
                      </div>
                    </div>
                  );
                })()}

                {/* Structured Sections */}
                <div className="space-y-3">
                  <div className="text-[#A3A3A3] font-bold text-xs">Assembled Context Sections</div>
                  {(contextPreviewData.sections || []).map((sec, idx) => {
                    const isUntrusted = sec.is_untrusted ?? sec.isUntrusted ?? false;
                    const estTokens = sec.estimated_tokens ?? sec.estimatedTokens ?? 0;

                    return (
                      <div
                        key={idx}
                        className="p-3 bg-[#050505] border border-[rgba(255,255,255,0.06)] rounded space-y-1.5"
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            <span className="text-[#F5F5F5] font-bold">{sec.name}</span>
                            {isUntrusted ? (
                              <span className="px-1.5 py-0.5 rounded text-[9px] bg-amber-950/60 border border-amber-800 text-amber-300 font-semibold">
                                QUARANTINED UNTRUSTED DATA
                              </span>
                            ) : (
                              <span className="px-1.5 py-0.5 rounded text-[9px] bg-emerald-950/60 border border-emerald-800 text-emerald-300 font-semibold">
                                SYSTEM GOVERNED
                              </span>
                            )}
                          </div>
                          <span className="text-[#777777] text-[10px]">~{estTokens} tokens</span>
                        </div>
                        <pre className="text-[#858585] text-[11px] bg-[#020202] p-2.5 rounded border border-[rgba(255,255,255,0.04)] overflow-x-auto whitespace-pre-wrap max-h-[140px]">
                          {sec.content}
                        </pre>
                      </div>
                    );
                  })}
                </div>

                {/* Structured Citations */}
                {(contextPreviewData.citations || []).length > 0 && (
                  <div className="space-y-2 pt-2 border-t border-[rgba(255,255,255,0.06)]">
                    <div className="text-[#62E6B2] font-bold text-xs">
                      Governed Citations ({contextPreviewData.citations.length})
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                      {contextPreviewData.citations.map((c, i) => {
                        const sType = c.source_type || c.sourceType || 'document';
                        const sId = c.source_id || c.sourceId || '';

                        return (
                          <div
                            key={i}
                            className="p-2.5 bg-[#070707] border border-[rgba(255,255,255,0.06)] rounded space-y-1 text-[11px]"
                          >
                            <div className="flex items-center justify-between">
                              <span className="text-[#F5F5F5] font-semibold">{c.title}</span>
                              <span className="text-[9px] text-[#62E6B2] uppercase">[{sType}]</span>
                            </div>
                            {c.snippet && <div className="text-[#777777] text-[10px] line-clamp-2">{c.snippet}</div>}
                            <div className="text-[#555555] text-[9px]">ID: {sId.slice(0, 12)}</div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}
              </div>
            ) : null}

            <div className="flex justify-end pt-3 border-t border-[rgba(255,255,255,0.08)] shrink-0">
              <Button variant="ghost" size="sm" onClick={() => setShowContextModal(false)}>
                Close
              </Button>
            </div>
          </div>
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
