import React from 'react';
import { X, Play, Pause, AlertOctagon, RotateCcw, ShieldCheck, Activity, Cpu, Clock, HardDrive, CheckCircle2 } from 'lucide-react';

interface AgentDetailDrawerProps {
  agentId: string | null;
  onClose: () => void;
  onPerformAction: (action: string) => void;
}

export const AgentDetailDrawer: React.FC<AgentDetailDrawerProps> = ({ agentId, onClose, onPerformAction }) => {
  if (!agentId) return null;

  return (
    <div className="fixed inset-y-0 right-0 w-full max-w-2xl bg-zinc-950 border-l border-zinc-800 shadow-2xl z-50 p-6 overflow-y-auto space-y-6 text-zinc-100">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-zinc-800 pb-4">
        <div>
          <div className="text-xs font-mono text-zinc-400">AGENT RUN ID: {agentId}</div>
          <h2 className="text-xl font-bold text-white mt-1">Operational Telemetry & Plan DAG</h2>
        </div>
        <button onClick={onClose} className="p-2 hover:bg-zinc-800 rounded-lg transition-colors text-zinc-400 hover:text-white">
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* Policy-Governed Control Actions */}
      <div className="p-4 bg-zinc-900 border border-zinc-800 rounded-xl space-y-3">
        <div className="text-xs font-semibold text-zinc-400 uppercase tracking-wider">Policy-Governed Operator Actions</div>
        <div className="flex items-center gap-3">
          <button
            onClick={() => onPerformAction('pause')}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-amber-500/20 text-amber-300 border border-amber-500/30 hover:bg-amber-500/30 font-medium text-xs rounded-lg transition-all"
          >
            <Pause className="w-3.5 h-3.5" /> Pause Agent
          </button>
          <button
            onClick={() => onPerformAction('resume')}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 hover:bg-emerald-500/30 font-medium text-xs rounded-lg transition-all"
          >
            <Play className="w-3.5 h-3.5 fill-current" /> Resume Execution
          </button>
          <button
            onClick={() => onPerformAction('retry_safe_step')}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-sky-500/20 text-sky-300 border border-sky-500/30 hover:bg-sky-500/30 font-medium text-xs rounded-lg transition-all"
          >
            <RotateCcw className="w-3.5 h-3.5" /> Retry Safe Step
          </button>
          <button
            onClick={() => onPerformAction('cancel')}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-rose-500/20 text-rose-300 border border-rose-500/30 hover:bg-rose-500/30 font-medium text-xs rounded-lg transition-all"
          >
            <AlertOctagon className="w-3.5 h-3.5" /> Cancel Mission
          </button>
        </div>
      </div>

      {/* Plan DAG Graph Representation */}
      <div className="space-y-3">
        <h3 className="text-sm font-semibold text-zinc-200 flex items-center gap-2">
          <Activity className="w-4 h-4 text-indigo-400" /> Plan Node Dependency Graph
        </h3>
        <div className="p-4 bg-zinc-900/80 border border-zinc-800 rounded-xl space-y-2 font-mono text-xs">
          <div className="flex items-center justify-between p-2.5 bg-emerald-500/10 border border-emerald-500/20 rounded-lg">
            <span className="text-emerald-300 font-bold">[1] context_retrieval (search_drive_files)</span>
            <span className="text-emerald-400">COMPLETED</span>
          </div>
          <div className="flex items-center justify-between p-2.5 bg-emerald-500/10 border border-emerald-500/20 rounded-lg">
            <span className="text-emerald-300 font-bold">[2] context_retrieval (search_gmail)</span>
            <span className="text-emerald-400">COMPLETED</span>
          </div>
          <div className="flex items-center justify-between p-2.5 bg-sky-500/10 border border-sky-500/20 rounded-lg">
            <span className="text-sky-300 font-bold">[3] analysis (synthesize_context)</span>
            <span className="text-sky-400">RUNNING</span>
          </div>
          <div className="flex items-center justify-between p-2.5 bg-zinc-800/50 border border-zinc-700/50 rounded-lg text-zinc-400">
            <span>[4] content_generation (create_content)</span>
            <span>PENDING</span>
          </div>
        </div>
      </div>

      {/* Event Timeline */}
      <div className="space-y-3">
        <h3 className="text-sm font-semibold text-zinc-200 flex items-center gap-2">
          <Clock className="w-4 h-4 text-sky-400" /> Live Observable Event Stream
        </h3>
        <div className="space-y-2 border-l-2 border-zinc-800 pl-4 py-1 text-xs">
          <div className="space-y-0.5">
            <div className="font-semibold text-white">Agent Started</div>
            <div className="text-zinc-500">22:04:10 — Initiated by workspace user</div>
          </div>
          <div className="space-y-0.5">
            <div className="font-semibold text-white">Drive Context Retrieved</div>
            <div className="text-zinc-500">22:04:12 — 1 file matched (CloudSpec.pdf)</div>
          </div>
          <div className="space-y-0.5">
            <div className="font-semibold text-white">Checkpoint Saved</div>
            <div className="text-zinc-500">22:04:15 — State version 2 persisted to DB</div>
          </div>
        </div>
      </div>
    </div>
  );
};
