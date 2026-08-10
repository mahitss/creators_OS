import React, { useState, useEffect } from 'react';
import { Cpu, ShieldCheck, Plus, Play, Clock, AlertTriangle, CheckCircle2, Lock, ArrowRight, Ban, Pause } from 'lucide-react';

interface AgentDefinition {
  id: string;
  name: string;
  description: string;
  created_by: string;
  visibility: string;
  default_purpose: string;
  status: string;
}

interface Delegation {
  id: string;
  agent_id: string;
  mission_id: string | null;
  scope: string;
  allowed_tools: string[];
  autonomy_level: string;
  expires_at: string | null;
  status: string;
}

export const AgentLibrary: React.FC = () => {
  const [agents, setAgents] = useState<AgentDefinition[]>([]);
  const [delegations, setDelegations] = useState<Delegation[]>([]);
  const [selectedAgent, setSelectedAgent] = useState<AgentDefinition | null>(null);
  const [showDelegateModal, setShowDelegateModal] = useState(false);
  const [allowedTools, setAllowedTools] = useState<string[]>(['search_drive_files', 'search_gmail', 'create_content']);
  const [scope, setScope] = useState('mission');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const headers = { 'X-User-Id': 'usr_alex', 'X-Workspace-Id': 'ws_default_01' };
      const aRes = await fetch('/api/v1/agents', { headers });
      if (aRes.ok) setAgents(await aRes.json());
    } catch (err) {
      console.error("Failed to load agent library:", err);
    }
  };

  const handleCreateDelegation = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedAgent) return;
    setError(null);
    try {
      const res = await fetch(`/api/v1/agents/${selectedAgent.id}/delegations`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-User-Id': 'usr_alex',
          'X-Workspace-Id': 'ws_default_01'
        },
        body: JSON.stringify({
          scope,
          allowed_tools: allowedTools,
          autonomy_level: 'FULL_AUTONOMY'
        })
      });
      if (res.ok) {
        setShowDelegateModal(false);
        fetchData();
      } else {
        const data = await res.json();
        setError(data.detail || "Failed to create delegation.");
      }
    } catch (err) {
      setError("Network error creating delegation.");
    }
  };

  const handleRevoke = async (delId: string) => {
    try {
      const res = await fetch(`/api/v1/delegations/${delId}/revoke`, {
        method: 'POST',
        headers: { 'X-User-Id': 'usr_alex', 'X-Workspace-Id': 'ws_default_01' }
      });
      if (res.ok) fetchData();
    } catch (err) {
      console.error("Revocation failed:", err);
    }
  };

  const toggleTool = (tool: string) => {
    if (allowedTools.includes(tool)) {
      setAllowedTools(allowedTools.filter(t => t !== tool));
    } else {
      setAllowedTools([...allowedTools, tool]);
    }
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8 text-zinc-100">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-zinc-800 pb-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
            <Cpu className="w-8 h-8 text-indigo-400" />
            Agent Library & Controlled Delegation
          </h1>
          <p className="text-zinc-400 mt-1">
            Browse shared workspace agent definitions and grant explicit, time-bounded, tool-whitelisted delegations.
          </p>
        </div>
      </div>

      {error && (
        <div className="p-4 bg-rose-500/10 border border-rose-500/30 rounded-xl text-rose-400 text-sm flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 flex-shrink-0" /> {error}
        </div>
      )}

      {/* Shared Agent Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {agents.map(ag => (
          <div key={ag.id} className="p-6 bg-zinc-900/60 border border-zinc-800 rounded-2xl space-y-4 hover:border-zinc-700 transition-all shadow-xl">
            <div className="flex items-start justify-between">
              <div>
                <span className="text-xs font-mono text-indigo-400 uppercase tracking-wider font-semibold">{ag.visibility} AGENT</span>
                <h3 className="text-xl font-bold text-white mt-0.5">{ag.name}</h3>
                <p className="text-xs text-zinc-400 mt-1">{ag.description}</p>
              </div>
              <span className="px-2.5 py-1 text-xs font-semibold rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                {ag.status}
              </span>
            </div>

            <div className="p-3 bg-zinc-950/80 border border-zinc-800/80 rounded-xl text-xs space-y-1">
              <div className="text-zinc-500 font-medium">DEFAULT PURPOSE:</div>
              <div className="text-zinc-300 font-mono">{ag.default_purpose}</div>
            </div>

            <div className="flex items-center justify-between pt-2">
              <span className="text-xs text-zinc-500 font-mono">Created by: {ag.created_by}</span>
              <button
                onClick={() => {
                  setSelectedAgent(ag);
                  setShowDelegateModal(true);
                }}
                className="flex items-center gap-1.5 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs rounded-xl transition-all shadow-lg shadow-indigo-600/20"
              >
                Delegate Authority <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Delegate Modal */}
      {showDelegateModal && selectedAgent && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-zinc-900 border border-zinc-800 rounded-2xl max-w-lg w-full p-6 space-y-5 shadow-2xl">
            <div className="border-b border-zinc-800 pb-3">
              <div className="text-xs text-indigo-400 font-mono">DELEGATE AUTHORITY</div>
              <h2 className="text-xl font-bold text-white">{selectedAgent.name}</h2>
            </div>

            <form onSubmit={handleCreateDelegation} className="space-y-4">
              <div>
                <label className="text-xs text-zinc-400 font-medium">Delegation Scope</label>
                <select
                  value={scope}
                  onChange={e => setScope(e.target.value)}
                  className="w-full mt-1 px-3.5 py-2 bg-zinc-950 border border-zinc-800 rounded-xl text-xs text-zinc-200 focus:outline-none focus:border-indigo-500"
                >
                  <option value="mission">Mission Level (Narrowest Scope)</option>
                  <option value="workspace">Workspace Level</option>
                  <option value="tool">Tool Specific</option>
                </select>
              </div>

              <div>
                <label className="text-xs text-zinc-400 font-medium block mb-2">Allowed Tool Whitelist</label>
                <div className="space-y-2 text-xs font-mono">
                  {['search_drive_files', 'search_gmail', 'create_content', 'create_calendar_event'].map(t => (
                    <label key={t} className="flex items-center gap-2 p-2 bg-zinc-950 border border-zinc-800 rounded-lg cursor-pointer hover:bg-zinc-800/40">
                      <input
                        type="checkbox"
                        checked={allowedTools.includes(t)}
                        onChange={() => toggleTool(t)}
                        className="rounded border-zinc-700 text-indigo-600 focus:ring-indigo-500"
                      />
                      <span className={allowedTools.includes(t) ? 'text-emerald-300 font-bold' : 'text-zinc-500'}>{t}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div className="flex items-center justify-end gap-3 pt-3 border-t border-zinc-800">
                <button
                  type="button"
                  onClick={() => setShowDelegateModal(false)}
                  className="px-4 py-2 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 rounded-xl text-xs font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-xs font-semibold transition-all"
                >
                  Create Explicit Delegation
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
