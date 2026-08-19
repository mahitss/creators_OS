import React, { useState, useEffect, useCallback } from 'react';
import { 
  Activity, 
  AlertTriangle, 
  CheckCircle2, 
  XCircle, 
  Pause, 
  Play, 
  RotateCcw, 
  ShieldCheck, 
  Clock, 
  Cpu, 
  DollarSign, 
  Radio, 
  Server, 
  Layers, 
  Search,
  Filter
} from 'lucide-react';
import { AgentDetailDrawer } from './AgentDetailDrawer';
import { ReliabilityWorkspace } from './ReliabilityWorkspace';

interface OverviewMetrics {
  active_agents: number;
  waiting_approvals: number;
  paused_agents: number;
  failed_agents: number;
  recovering_agents: number;
  stuck_agents: number;
  completed_today: number;
  total_tokens: number;
  total_estimated_cost: number;
  eval_suite_status: string;
}

interface AgentRun {
  id: string;
  mission_id: string;
  status: string;
  goal: string;
  current_node: string;
  current_tool: string | null;
  iteration_count: number;
  max_iterations: number;
  lease_worker_id: string | null;
  total_tokens: number;
  estimated_cost: number;
  created_at: string;
  updated_at: string;
}

export const AgentControlCenter: React.FC = () => {
  const [overview, setOverview] = useState<OverviewMetrics | null>(null);
  const [agents, setAgents] = useState<AgentRun[]>([]);
  const [stuckList, setStuckList] = useState<any[]>([]);
  const [selectedAgentId, setSelectedAgentId] = useState<string | null>(null);
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [sseConnected, setSseConnected] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<'agents' | 'reliability'>('agents');

  const fetchData = useCallback(async () => {
    try {
      const ovRes = await fetch('/api/v1/admin/agents/overview', { credentials: 'include' });
      if (ovRes.ok) setOverview(await ovRes.json());

      const url = statusFilter !== 'all' ? `/api/v1/admin/agents?status=${statusFilter}` : '/api/v1/admin/agents';
      const agRes = await fetch(url, { credentials: 'include' });
      if (agRes.ok) setAgents(await agRes.json());

      const stRes = await fetch('/api/v1/admin/agents/stuck', { credentials: 'include' });
      if (stRes.ok) setStuckList(await stRes.json());
    } catch (err) {
      console.error("Control Center fetch failed:", err);
    }
  }, [statusFilter]);

  useEffect(() => {
    fetchData();

    // Setup Server-Sent Events (SSE) stream listener
    const eventSource = new EventSource('/api/v1/admin/agents/events');
    eventSource.onopen = () => setSseConnected(true);
    eventSource.onerror = () => setSseConnected(false);

    eventSource.addEventListener('ping', () => setSseConnected(true));
    eventSource.addEventListener('agent.started', () => fetchData());
    eventSource.addEventListener('agent.step.completed', () => fetchData());
    eventSource.addEventListener('agent.approval.requested', () => fetchData());
    eventSource.addEventListener('agent.failed', () => fetchData());
    eventSource.addEventListener('agent.completed', () => fetchData());

    return () => {
      eventSource.close();
    };
  }, [fetchData]);

  const handleOperatorAction = async (runId: string, action: string) => {
    try {
      const res = await fetch(`/api/v1/admin/agents/${runId}/action`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ action, reason: 'Operator manual override via Control Center' })
      });
      if (res.ok) {
        fetchData();
      }
    } catch (err) {
      console.error("Operator action failed:", err);
    }
  };

  const filteredAgents = agents.filter(a => 
    searchQuery === '' || a.id.toLowerCase().includes(searchQuery.toLowerCase()) || a.goal.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8 text-zinc-100">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-zinc-800 pb-6">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
              <Server className="w-8 h-8 text-indigo-400" />
              Agent Control Center & Live Operations
            </h1>
            <span className={`px-2.5 py-1 text-xs font-semibold rounded-full flex items-center gap-1.5 ${sseConnected ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'}`}>
              <Radio className={`w-3 h-3 ${sseConnected ? 'animate-pulse text-emerald-400' : ''}`} />
              {sseConnected ? 'SSE Live Stream Active' : 'Polling Connection'}
            </span>
          </div>
          <p className="text-zinc-400 mt-1">
            Real-time observability, stuck-agent signals, telemetry metrics, and policy-governed operator controls.
          </p>
        </div>
      </div>

      {/* Control Center Tab Switcher */}
      <div className="flex border-b border-zinc-800 space-x-6 text-sm font-semibold">
        <button
          onClick={() => setActiveTab('agents')}
          className={`pb-3 transition ${activeTab === 'agents' ? 'text-indigo-400 border-b-2 border-indigo-500' : 'text-zinc-400 hover:text-zinc-200'}`}
        >
          Active Agent Runs & Control
        </button>
        <button
          onClick={() => setActiveTab('reliability')}
          className={`pb-3 transition ${activeTab === 'reliability' ? 'text-indigo-400 border-b-2 border-indigo-500' : 'text-zinc-400 hover:text-zinc-200'}`}
        >
          Reliability & Self-Healing Engine
        </button>
      </div>

      {activeTab === 'reliability' ? (
        <ReliabilityWorkspace />
      ) : (
        <>

      {/* Top Overview Metrics */}
      {overview && (
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          <div className="p-5 bg-zinc-900/80 border border-zinc-800 rounded-xl">
            <div className="text-xs text-zinc-400 font-medium">Active Agents</div>
            <div className="text-3xl font-bold mt-1 text-emerald-400">{overview.active_agents}</div>
            <div className="text-xs text-zinc-500 mt-1">Running & Planning</div>
          </div>

          <div className="p-5 bg-zinc-900/80 border border-zinc-800 rounded-xl">
            <div className="text-xs text-zinc-400 font-medium">Waiting Approvals</div>
            <div className="text-3xl font-bold mt-1 text-amber-400">{overview.waiting_approvals}</div>
            <div className="text-xs text-zinc-500 mt-1">Gated WRITE tools</div>
          </div>

          <div className="p-5 bg-zinc-900/80 border border-zinc-800 rounded-xl">
            <div className="text-xs text-zinc-400 font-medium">Stuck Agents</div>
            <div className="text-3xl font-bold mt-1 text-rose-400">{overview.stuck_agents}</div>
            <div className="text-xs text-zinc-500 mt-1">Expired leases & timeouts</div>
          </div>

          <div className="p-5 bg-zinc-900/80 border border-zinc-800 rounded-xl">
            <div className="text-xs text-zinc-400 font-medium">Token Usage</div>
            <div className="text-2xl font-bold mt-1 text-sky-400">{overview.total_tokens.toLocaleString()}</div>
            <div className="text-xs text-zinc-500 mt-1">Context + execution</div>
          </div>

          <div className="p-5 bg-zinc-900/80 border border-zinc-800 rounded-xl">
            <div className="text-xs text-zinc-400 font-medium">Estimated Cost</div>
            <div className="text-2xl font-bold mt-1 text-indigo-400">${overview.total_estimated_cost.toFixed(4)}</div>
            <div className="text-xs text-zinc-500 mt-1">Estimated compute cost</div>
          </div>
        </div>
      )}

      {/* Proactive Automations & Event Operations Bar */}
      <div className="p-5 bg-zinc-900/80 border border-zinc-800 rounded-xl grid grid-cols-2 md:grid-cols-5 gap-4 text-xs">
        <div>
          <div className="text-zinc-400 font-medium">Event Throughput</div>
          <div className="text-xl font-bold text-amber-400 mt-1">100% Bound</div>
          <div className="text-[10px] text-zinc-500">Normalizing & deduplicating</div>
        </div>
        <div>
          <div className="text-zinc-400 font-medium">Active Automations</div>
          <div className="text-xl font-bold text-emerald-400 mt-1">Policy-Engine Gated</div>
          <div className="text-[10px] text-zinc-500">Structured condition triggers</div>
        </div>
        <div>
          <div className="text-zinc-400 font-medium">Dead Letter Queue</div>
          <div className="text-xl font-bold text-zinc-300 mt-1">0 Unhandled</div>
          <div className="text-[10px] text-zinc-500">Operational visibility</div>
        </div>
        <div>
          <div className="text-zinc-400 font-medium">Loop Protection</div>
          <div className="text-xl font-bold text-cyan-400 mt-1">Max Depth ≤ 5</div>
          <div className="text-[10px] text-zinc-500">Ancestry & chain tracking</div>
        </div>
        <div>
          <div className="text-zinc-400 font-medium">Cooldown Controls</div>
          <div className="text-xl font-bold text-indigo-400 mt-1">Active</div>
          <div className="text-[10px] text-zinc-500">Rate-limiting enabled</div>
        </div>
      </div>

      {/* Stuck Agent Signal Alerts */}
      {stuckList.length > 0 && (
        <div className="p-4 bg-rose-500/10 border border-rose-500/30 rounded-xl space-y-2">
          <div className="flex items-center gap-2 text-rose-400 font-semibold text-sm">
            <AlertTriangle className="w-5 h-5" /> Deterministic Stuck Agent Signals ({stuckList.length})
          </div>
          <div className="space-y-1">
            {stuckList.map((st, i) => (
              <div key={i} className="flex items-center justify-between text-xs text-zinc-300 bg-zinc-950/60 p-2.5 rounded-lg border border-zinc-800">
                <div>
                  <span className="font-mono text-rose-300 font-semibold">{st.agent_run_id}</span>
                  <span className="mx-2 text-zinc-500">•</span>
                  <span>{st.signals[0]?.reason}</span>
                </div>
                <button
                  onClick={() => setSelectedAgentId(st.agent_run_id)}
                  className="px-2.5 py-1 bg-rose-600 hover:bg-rose-500 text-white rounded font-medium transition-all"
                >
                  Inspect Signal
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Main Agent Table & Search */}
      <div className="bg-zinc-900/60 border border-zinc-800 rounded-xl overflow-hidden shadow-xl">
        <div className="px-6 py-4 border-b border-zinc-800 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <Layers className="w-5 h-5 text-indigo-400" />
            <h2 className="font-semibold text-zinc-200">Active Operational Agent Runs</h2>
          </div>

          <div className="flex items-center gap-3">
            <div className="relative">
              <Search className="w-4 h-4 text-zinc-500 absolute left-3 top-2.5" />
              <input
                type="text"
                placeholder="Search run ID or goal..."
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                className="pl-9 pr-4 py-1.5 bg-zinc-950 border border-zinc-800 rounded-lg text-xs text-zinc-200 focus:outline-none focus:border-indigo-500 w-64"
              />
            </div>

            <select
              value={statusFilter}
              onChange={e => setStatusFilter(e.target.value)}
              className="px-3 py-1.5 bg-zinc-950 border border-zinc-800 rounded-lg text-xs text-zinc-300 focus:outline-none focus:border-indigo-500"
            >
              <option value="all">All Statuses</option>
              <option value="running">Running</option>
              <option value="waiting_for_approval">Waiting Approval</option>
              <option value="paused">Paused</option>
              <option value="failed">Failed</option>
              <option value="completed">Completed</option>
            </select>
          </div>
        </div>

        <div className="divide-y divide-zinc-800/60">
          {filteredAgents.length === 0 ? (
            <div className="p-8 text-center text-zinc-500 text-sm">No agent runs matching filter criteria.</div>
          ) : (
            filteredAgents.map(ag => (
              <div key={ag.id} className="p-4 hover:bg-zinc-800/30 transition-colors flex items-center justify-between text-sm">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="font-mono font-bold text-white cursor-pointer hover:underline" onClick={() => setSelectedAgentId(ag.id)}>
                      {ag.id}
                    </span>
                    <span className={`px-2 py-0.5 text-xs font-semibold rounded capitalize ${
                      ag.status === 'running' ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' :
                      ag.status === 'waiting_for_approval' ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30' :
                      ag.status === 'paused' ? 'bg-sky-500/20 text-sky-300 border border-sky-500/30' :
                      ag.status === 'failed' ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30' :
                      'bg-zinc-800 text-zinc-300'
                    }`}>
                      {ag.status.replace('_', ' ')}
                    </span>
                  </div>
                  <div className="text-xs text-zinc-400 truncate max-w-lg">{ag.goal}</div>
                </div>

                <div className="flex items-center gap-4 text-xs font-mono text-zinc-400">
                  <div>Iter {ag.iteration_count}/{ag.max_iterations}</div>
                  <div>{ag.total_tokens} tokens</div>
                  <button
                    onClick={() => setSelectedAgentId(ag.id)}
                    className="px-3 py-1.5 bg-zinc-800 hover:bg-zinc-700 text-white rounded font-medium transition-all"
                  >
                    Inspect
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Drawer */}
      <AgentDetailDrawer
        agentId={selectedAgentId}
        onClose={() => setSelectedAgentId(null)}
        onPerformAction={action => {
          if (selectedAgentId) handleOperatorAction(selectedAgentId, action);
        }}
      />
        </>
      )}
    </div>
  );
};
