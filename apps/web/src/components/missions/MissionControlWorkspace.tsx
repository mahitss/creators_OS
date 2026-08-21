'use client';

import React, { useState, useEffect } from 'react';
import { 
  GitBranch, 
  RotateCw, 
  FileCheck,
} from 'lucide-react';
import { getMission, fetchMissionSteps, Mission, MissionStep } from '../../lib/api/missions';

export const MissionControlWorkspace: React.FC<{ missionId: string }> = ({ missionId }) => {
  const [mission, setMission] = useState<Mission | null>(null);
  const [steps, setSteps] = useState<MissionStep[]>([]);
  const [activeTab, setActiveTab] = useState<'plan' | 'deliverables' | 'telemetry'>('plan');
  const [isLoading, setIsLoading] = useState(true);

  const fetchMissionData = React.useCallback(async () => {
    setIsLoading(true);
    try {
      const [m, s] = await Promise.all([
        getMission(missionId),
        fetchMissionSteps(missionId),
      ]);
      setMission(m);
      setSteps(s.steps || []);
    } catch (e) {
      console.error('Failed to load mission control data:', e);
    } finally {
      setIsLoading(false);
    }
  }, [missionId]);

  useEffect(() => {
    fetchMissionData();
  }, [fetchMissionData]);

  const plan = mission?.latest_plan || (mission?.plan as any);
  const planSteps = plan?.steps || steps;
  const cost = mission?.cost_usd || mission?.cost || 0.0;
  const tokens = mission?.token_usage?.total_tokens || mission?.tokenUsage?.totalTokens || 0;
  const deliverables = plan?.deliverables || (mission?.result as any)?.deliverables || [];

  return (
    <div className="space-y-6">
      {/* Top Header & Telemetry Bar */}
      <div className="bg-neutral-950 border border-neutral-800 p-5 rounded text-neutral-100 space-y-4">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-neutral-900 text-neutral-300 rounded border border-neutral-800">
              <GitBranch className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-base font-semibold tracking-tight font-mono">{mission?.name || mission?.title || 'Autonomous Mission Orchestrator'}</h1>
              <p className="text-xs text-neutral-400 font-mono">Agent: {mission?.agent_id || mission?.agentId || 'ag_executive_core'} | Model: {mission?.model || 'openrouter/free'}</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={fetchMissionData}
              disabled={isLoading}
              className="flex items-center gap-1.5 px-3 py-1.5 bg-neutral-900 hover:bg-neutral-800 text-neutral-300 border border-neutral-800 rounded text-xs font-mono transition"
            >
              <RotateCw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin' : ''}`} /> Refresh Telemetry
            </button>
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs border-t border-neutral-900 pt-4 text-neutral-400 font-mono">
          <div>STATUS: <span className="text-emerald-400 font-semibold uppercase">{mission?.status || 'DRAFT'}</span></div>
          <div>PROGRESS: <span className="text-neutral-200 font-mono">{Math.round(mission?.progress || 0)}%</span></div>
          <div>TOTAL TOKENS: <span className="text-neutral-200 font-mono">{tokens.toLocaleString()}</span></div>
          <div>ACCUMULATED COST: <span className="text-emerald-400 font-mono">${cost.toFixed(4)}</span></div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-2 border-b border-neutral-800 pb-2">
        <button
          onClick={() => setActiveTab('plan')}
          className={`px-3 py-1.5 text-xs font-mono rounded transition ${
            activeTab === 'plan' ? 'bg-neutral-800 text-neutral-100' : 'text-neutral-400 hover:text-neutral-200'
          }`}
        >
          Execution Plan ({planSteps?.length || 0})
        </button>
        <button
          onClick={() => setActiveTab('deliverables')}
          className={`px-3 py-1.5 text-xs font-mono rounded transition ${
            activeTab === 'deliverables' ? 'bg-neutral-800 text-neutral-100' : 'text-neutral-400 hover:text-neutral-200'
          }`}
        >
          Deliverables & Artifacts ({deliverables.length})
        </button>
        <button
          onClick={() => setActiveTab('telemetry')}
          className={`px-3 py-1.5 text-xs font-mono rounded transition ${
            activeTab === 'telemetry' ? 'bg-neutral-800 text-neutral-100' : 'text-neutral-400 hover:text-neutral-200'
          }`}
        >
          Cost & Resource Accounting
        </button>
      </div>

      {/* Tab: Execution Plan */}
      {activeTab === 'plan' && (
        <div className="space-y-4">
          <div className="bg-neutral-950 border border-neutral-800 p-4 rounded">
            <h3 className="text-xs font-semibold text-neutral-400 uppercase font-mono mb-3">Structured Step Sequence</h3>
            {planSteps && planSteps.length > 0 ? (
              <div className="space-y-2">
                {planSteps.map((step: any, idx: number) => (
                  <div key={step.id || idx} className="bg-neutral-900/60 border border-neutral-800/80 p-3 rounded flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="w-5 h-5 rounded bg-neutral-800 flex items-center justify-center text-xs font-mono text-neutral-300 font-bold">
                        {step.order || idx + 1}
                      </div>
                      <div>
                        <h4 className="text-xs font-semibold text-neutral-200 font-mono">{step.title || step.name}</h4>
                        {step.description && (
                          <p className="text-[11px] text-neutral-400 font-mono mt-0.5">{step.description}</p>
                        )}
                      </div>
                    </div>

                    <span className="px-2 py-0.5 text-[10px] font-mono rounded bg-neutral-800 text-neutral-300 border border-neutral-700">
                      {String(step.status || 'PENDING').toUpperCase()}
                    </span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-xs text-neutral-500 font-mono italic">Plan will be structured upon mission launch.</p>
            )}
          </div>
        </div>
      )}

      {/* Tab: Deliverables */}
      {activeTab === 'deliverables' && (
        <div className="bg-neutral-950 border border-neutral-800 p-5 rounded space-y-3 font-mono">
          <div className="flex items-center gap-2 text-emerald-400 text-xs font-semibold uppercase">
            <FileCheck className="w-4 h-4" /> Verified Deliverables
          </div>
          {deliverables.length > 0 ? (
            <div className="space-y-2">
              {deliverables.map((item: string, i: number) => (
                <div key={i} className="p-3 bg-neutral-900/80 border border-neutral-800 rounded text-xs text-neutral-300 flex items-center gap-2">
                  <span className="text-emerald-400">✓</span> {item}
                </div>
              ))}
            </div>
          ) : (
            <p className="text-xs text-neutral-500 italic">No deliverables produced yet. Launch mission to execute.</p>
          )}
        </div>
      )}

      {/* Tab: Cost & Resource Telemetry */}
      {activeTab === 'telemetry' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 font-mono">
          <div className="bg-neutral-950 border border-neutral-800 p-4 rounded space-y-3">
            <h3 className="text-xs font-semibold text-neutral-300 uppercase">Token Accounting</h3>
            <div className="space-y-2 text-xs text-neutral-400 bg-neutral-900/60 p-3 rounded border border-neutral-800">
              <div className="flex justify-between">
                <span>Input Tokens:</span>
                <span className="text-neutral-200">{(mission?.token_usage?.input_tokens || 0).toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span>Output Tokens:</span>
                <span className="text-neutral-200">{(mission?.token_usage?.output_tokens || 0).toLocaleString()}</span>
              </div>
              <div className="flex justify-between border-t border-neutral-800 pt-2 font-semibold">
                <span>Total Tokens:</span>
                <span className="text-emerald-400">{tokens.toLocaleString()}</span>
              </div>
            </div>
          </div>

          <div className="bg-neutral-950 border border-neutral-800 p-4 rounded space-y-3">
            <h3 className="text-xs font-semibold text-neutral-300 uppercase">Cost Attribution (USD)</h3>
            <div className="space-y-2 text-xs text-neutral-400 bg-neutral-900/60 p-3 rounded border border-neutral-800">
              <div className="flex justify-between">
                <span>Execution Provider:</span>
                <span className="text-neutral-200">OpenRouter</span>
              </div>
              <div className="flex justify-between">
                <span>Selected Model:</span>
                <span className="text-neutral-200">{mission?.model || 'openrouter/free'}</span>
              </div>
              <div className="flex justify-between border-t border-neutral-800 pt-2 font-semibold">
                <span>Total Mission Cost:</span>
                <span className="text-emerald-400">${cost.toFixed(6)}</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
