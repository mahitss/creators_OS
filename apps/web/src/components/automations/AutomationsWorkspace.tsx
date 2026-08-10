'use client';

import React, { useState, useEffect } from 'react';
import {
  Zap,
  Play,
  Pause,
  Clock,
  ShieldCheck,
  AlertTriangle,
  Plus,
  RefreshCw,
  Sliders,
  CheckCircle2,
  XCircle,
  Activity,
  FileText,
  Radio,
  Eye
} from 'lucide-react';

interface TriggerItem {
  id: string;
  workspace_id: string;
  name: string;
  description: string | null;
  event_type: string;
  conditions: Record<string, any>;
  action_type: string;
  enabled: boolean;
  status: string;
  scope: string;
  cooldown_seconds: number;
  last_triggered_at: string | null;
  created_at: string;
}

interface ExecutionItem {
  id: string;
  trigger_id: string;
  event_id: string;
  decision: string;
  action_type: string;
  status: string;
  reason: string;
  chain_depth: number;
  created_at: string;
}

interface DryRunResult {
  matched: boolean;
  trigger_id: string;
  trigger_name: string;
  policy_decision: string;
  reason: string;
  proposed_action: string;
  requires_approval: boolean;
  cooldown_active: boolean;
  chain_depth: number;
}

export const AutomationsWorkspace: React.FC = () => {
  const [triggers, setTriggers] = useState<TriggerItem[]>([]);
  const [selectedTrigger, setSelectedTrigger] = useState<TriggerItem | null>(null);
  const [history, setHistory] = useState<ExecutionItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [showCreateModal, setShowCreateModal] = useState<boolean>(false);
  const [testResult, setTestResult] = useState<DryRunResult | null>(null);
  const [testing, setTesting] = useState<boolean>(false);

  // Form state
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [eventType, setEventType] = useState('calendar.event_updated');
  const [actionType, setActionType] = useState('create_attention');
  const [scope, setScope] = useState('workspace');
  const [cooldownSec, setCooldownSec] = useState(7200);

  useEffect(() => {
    fetchTriggers();
  }, []);

  const fetchTriggers = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/automations?workspaceId=ws_default_creator');
      if (res.ok) {
        const data = await res.json();
        setTriggers(data);
        if (data.length > 0 && !selectedTrigger) {
          setSelectedTrigger(data[0]);
          fetchHistory(data[0].id);
        }
      }
    } catch (err) {
      console.error('Failed to load triggers', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchHistory = async (id: string) => {
    try {
      const res = await fetch(`/api/v1/automations/${id}/history`);
      if (res.ok) {
        const data = await res.json();
        setHistory(data);
      }
    } catch (err) {
      console.error('Failed to load trigger history', err);
    }
  };

  const handleToggleTrigger = async (tr: TriggerItem) => {
    const endpoint = tr.enabled ? `/api/v1/automations/${tr.id}/pause` : `/api/v1/automations/${tr.id}/enable`;
    try {
      const res = await fetch(endpoint, { method: 'POST' });
      if (res.ok) {
        fetchTriggers();
      }
    } catch (err) {
      console.error('Failed to toggle trigger', err);
    }
  };

  const handleCreateTrigger = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch('/api/v1/automations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          workspace_id: 'ws_default_creator',
          name,
          description,
          event_type: eventType,
          conditions: { is_deadline_change: true },
          action_type: actionType,
          scope,
          cooldown_seconds: Number(cooldownSec)
        })
      });
      if (res.ok) {
        setShowCreateModal(false);
        setName('');
        setDescription('');
        fetchTriggers();
      }
    } catch (err) {
      console.error('Failed to create trigger', err);
    }
  };

  const handleDryRunTest = async () => {
    if (!selectedTrigger) return;
    setTesting(true);
    setTestResult(null);
    try {
      const res = await fetch(`/api/v1/automations/${selectedTrigger.id}/test?workspaceId=ws_default_creator`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          event_type: selectedTrigger.event_type,
          resource_type: 'calendar_event',
          resource_id: 'evt_simulated_123',
          metadata_dict: { is_deadline_change: true, priority: 'high' }
        })
      });
      if (res.ok) {
        const data = await res.json();
        setTestResult(data);
      }
    } catch (err) {
      console.error('Failed to run dry-run test', err);
    } finally {
      setTesting(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-slate-950 text-slate-100 p-6 space-y-6 overflow-y-auto">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-amber-500/10 text-amber-400 rounded-lg border border-amber-500/20">
              <Zap className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight text-slate-50">Event-Driven Automations</h1>
              <p className="text-xs text-slate-400">Proactive intelligence triggers, signal filters, and policy-gated rules</p>
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={fetchTriggers}
            className="flex items-center space-x-1.5 px-3 py-1.5 bg-slate-900 border border-slate-700 text-slate-300 hover:text-slate-100 rounded-lg text-xs font-medium transition"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Refresh</span>
          </button>

          <button
            onClick={() => setShowCreateModal(true)}
            className="flex items-center space-x-1.5 px-3.5 py-1.5 bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-600 hover:to-amber-700 text-slate-950 font-semibold rounded-lg text-xs shadow-lg shadow-amber-500/10 transition"
          >
            <Plus className="w-4 h-4" />
            <span>Create Automation</span>
          </button>
        </div>
      </div>

      {/* Main Workspace Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 flex-1">
        {/* Trigger List */}
        <div className="lg:col-span-1 bg-slate-900/50 border border-slate-800 rounded-xl p-4 flex flex-col space-y-4">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Active Triggers</h2>

          {loading ? (
            <div className="flex items-center justify-center py-12 text-slate-500 text-xs">Loading triggers...</div>
          ) : triggers.length === 0 ? (
            <div className="text-center py-12 text-slate-500 text-xs border border-dashed border-slate-800 rounded-lg p-6">
              No recent automation activity.
            </div>
          ) : (
            <div className="space-y-2 overflow-y-auto">
              {triggers.map((tr) => (
                <div
                  key={tr.id}
                  onClick={() => {
                    setSelectedTrigger(tr);
                    fetchHistory(tr.id);
                  }}
                  className={`p-3.5 rounded-lg border text-left cursor-pointer transition ${
                    selectedTrigger?.id === tr.id
                      ? 'bg-amber-500/10 border-amber-500/30 text-slate-100'
                      : 'bg-slate-900/80 border-slate-800 hover:border-slate-700 text-slate-300'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-xs font-semibold text-slate-200">{tr.name}</span>
                    <span
                      className={`text-[10px] px-2 py-0.5 rounded-full border font-medium ${
                        tr.enabled
                          ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400'
                          : 'bg-slate-800 border-slate-700 text-slate-400'
                      }`}
                    >
                      {tr.enabled ? 'ACTIVE' : 'PAUSED'}
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-400 line-clamp-1 mb-2">{tr.description || tr.event_type}</p>
                  <div className="flex items-center justify-between text-[10px] text-slate-500">
                    <span>Event: {tr.event_type}</span>
                    <span>Cooldown: {Math.round(tr.cooldown_seconds / 60)}m</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Selected Trigger Detail & Testing */}
        <div className="lg:col-span-2 space-y-6">
          {selectedTrigger ? (
            <>
              {/* Trigger Details Card */}
              <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4">
                <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
                  <div>
                    <h2 className="text-base font-bold text-slate-100">{selectedTrigger.name}</h2>
                    <p className="text-xs text-slate-400">{selectedTrigger.description || 'No description provided'}</p>
                  </div>
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => handleToggleTrigger(selectedTrigger)}
                      className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium border transition ${
                        selectedTrigger.enabled
                          ? 'bg-amber-500/10 border-amber-500/30 text-amber-300 hover:bg-amber-500/20'
                          : 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300 hover:bg-emerald-500/20'
                      }`}
                    >
                      {selectedTrigger.enabled ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
                      <span>{selectedTrigger.enabled ? 'Pause' : 'Enable'}</span>
                    </button>
                    <button
                      onClick={handleDryRunTest}
                      disabled={testing}
                      className="flex items-center space-x-1.5 px-3 py-1.5 bg-slate-800 border border-slate-700 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-medium transition"
                    >
                      <Eye className="w-3.5 h-3.5 text-cyan-400" />
                      <span>{testing ? 'Testing...' : 'Test Trigger'}</span>
                    </button>
                  </div>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs">
                  <div className="bg-slate-950/60 p-3 rounded-lg border border-slate-800/60">
                    <span className="text-slate-500 block text-[10px]">EVENT TYPE</span>
                    <span className="font-mono text-slate-200">{selectedTrigger.event_type}</span>
                  </div>
                  <div className="bg-slate-950/60 p-3 rounded-lg border border-slate-800/60">
                    <span className="text-slate-500 block text-[10px]">ACTION TYPE</span>
                    <span className="font-mono text-amber-400">{selectedTrigger.action_type}</span>
                  </div>
                  <div className="bg-slate-950/60 p-3 rounded-lg border border-slate-800/60">
                    <span className="text-slate-500 block text-[10px]">SCOPE</span>
                    <span className="font-mono text-cyan-400">{selectedTrigger.scope}</span>
                  </div>
                  <div className="bg-slate-950/60 p-3 rounded-lg border border-slate-800/60">
                    <span className="text-slate-500 block text-[10px]">COOLDOWN</span>
                    <span className="font-mono text-slate-300">{Math.round(selectedTrigger.cooldown_seconds / 60)} min</span>
                  </div>
                </div>

                {/* Dry Run Test Result Alert */}
                {testResult && (
                  <div className={`p-4 rounded-lg border text-xs space-y-1.5 ${
                    testResult.matched && testResult.policy_decision === 'ALLOW'
                      ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300'
                      : 'bg-amber-500/10 border-amber-500/30 text-amber-300'
                  }`}>
                    <div className="flex items-center justify-between font-semibold">
                      <span>SIMULATION TEST RESULT: {testResult.policy_decision}</span>
                      <span>Chain Depth: {testResult.chain_depth}</span>
                    </div>
                    <p className="text-[11px] text-slate-300">{testResult.reason}</p>
                  </div>
                )}
              </div>

              {/* Execution Audit History */}
              <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4">
                <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Trigger Execution Audit Log</h3>

                {history.length === 0 ? (
                  <div className="text-center py-8 text-slate-500 text-xs border border-dashed border-slate-800 rounded-lg">
                    No recent execution history for this trigger.
                  </div>
                ) : (
                  <div className="space-y-2 overflow-y-auto max-h-64">
                    {history.map((h) => (
                      <div key={h.id} className="p-3 bg-slate-950/60 border border-slate-800 rounded-lg text-xs flex items-center justify-between">
                        <div>
                          <div className="flex items-center space-x-2">
                            <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${
                              h.decision === 'allowed' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-red-500/20 text-red-400'
                            }`}>
                              {h.decision.toUpperCase()}
                            </span>
                            <span className="font-medium text-slate-200">{h.action_type}</span>
                          </div>
                          <p className="text-[11px] text-slate-400 mt-1">{h.reason}</p>
                        </div>
                        <div className="text-right text-[10px] text-slate-500">
                          <div>Depth: {h.chain_depth}</div>
                          <div>{new Date(h.created_at).toLocaleTimeString()}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </>
          ) : (
            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-12 text-center text-slate-500 text-xs">
              Select a trigger from the list to view configuration and audit history.
            </div>
          )}
        </div>
      </div>

      {/* Create Trigger Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-800 rounded-xl max-w-md w-full p-6 space-y-4 shadow-2xl">
            <h2 className="text-base font-bold text-slate-100">Create Event-Driven Trigger</h2>

            <form onSubmit={handleCreateTrigger} className="space-y-3 text-xs">
              <div>
                <label className="block text-slate-400 mb-1">Trigger Name</label>
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="e.g. Schedule Change Alert"
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:border-amber-500"
                />
              </div>

              <div>
                <label className="block text-slate-400 mb-1">Description</label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Proactive policy trigger description"
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:border-amber-500 h-20"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-400 mb-1">Event Type</label>
                  <select
                    value={eventType}
                    onChange={(e) => setEventType(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200"
                  >
                    <option value="calendar.event_updated">calendar.event_updated</option>
                    <option value="gmail.thread_updated">gmail.thread_updated</option>
                    <option value="drive.file_updated">drive.file_updated</option>
                    <option value="mission.blocked">mission.blocked</option>
                    <option value="agent.failed">agent.failed</option>
                  </select>
                </div>

                <div>
                  <label className="block text-slate-400 mb-1">Action Type</label>
                  <select
                    value={actionType}
                    onChange={(e) => setActionType(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200"
                  >
                    <option value="create_attention">create_attention</option>
                    <option value="create_insight">create_insight</option>
                    <option value="request_approval">request_approval</option>
                    <option value="create_mission">create_mission</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-400 mb-1">Scope</label>
                  <select
                    value={scope}
                    onChange={(e) => setScope(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200"
                  >
                    <option value="personal">Personal</option>
                    <option value="workspace">Workspace</option>
                    <option value="mission">Mission</option>
                  </select>
                </div>

                <div>
                  <label className="block text-slate-400 mb-1">Cooldown (sec)</label>
                  <input
                    type="number"
                    value={cooldownSec}
                    onChange={(e) => setCooldownSec(Number(e.target.value))}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200"
                  />
                </div>
              </div>

              <div className="flex justify-end space-x-2 pt-3">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="px-3.5 py-2 bg-slate-800 text-slate-300 rounded-lg font-medium hover:bg-slate-700"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-3.5 py-2 bg-amber-500 text-slate-950 rounded-lg font-semibold hover:bg-amber-400"
                >
                  Create Trigger
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
