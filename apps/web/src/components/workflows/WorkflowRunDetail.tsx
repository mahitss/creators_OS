'use client';

import React, { useState, useEffect, useCallback } from 'react';
import {
  Activity,
  CheckCircle2,
  XCircle,
  Clock,
  RotateCcw,
  ShieldCheck,
  Server,
  Play
} from 'lucide-react';

interface WorkflowRunDetailProps {
  runId: string;
}

export const WorkflowRunDetail: React.FC<WorkflowRunDetailProps> = ({ runId }) => {
  const [run, setRun] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const fetchRunDetail = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch(`/api/v1/workflows/runs/${runId}`);
      if (res.ok) {
        const data = await res.json();
        setRun(data);
      }
    } catch (err) {
      console.error('Failed to fetch workflow run detail', err);
    } finally {
      setLoading(false);
    }
  }, [runId]);

  useEffect(() => {
    fetchRunDetail();
  }, [fetchRunDetail]);

  if (loading) {
    return <div className="p-8 text-center text-xs text-slate-500">Loading workflow execution telemetry...</div>;
  }

  if (!run) {
    return <div className="p-8 text-center text-xs text-slate-500">Workflow run not found.</div>;
  }

  return (
    <div className="bg-slate-950 border border-slate-800 rounded-xl p-6 space-y-6 text-slate-100">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <div className="flex items-center space-x-3">
            <h2 className="text-lg font-bold text-slate-100">Execution Telemetry: {run.id}</h2>
            <span className={`text-[10px] px-2 py-0.5 rounded-full border font-medium uppercase ${
              run.status === 'completed' ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400' :
              run.status === 'running' ? 'bg-amber-500/10 border-amber-500/20 text-amber-400' :
              'bg-slate-800 border-slate-700 text-slate-400'
            }`}>
              {run.status}
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">Workspace: {run.workspace_id} | Version: {run.workflow_version_id}</p>
        </div>

        <button
          onClick={fetchRunDetail}
          className="flex items-center space-x-1.5 px-3 py-1.5 bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-300 rounded-lg text-xs font-medium transition"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          <span>Refresh Run</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs">
        <div className="bg-slate-900/60 p-3.5 rounded-lg border border-slate-800">
          <span className="text-slate-500 block text-[10px]">STARTED AT</span>
          <span className="font-mono text-slate-200">{run.started_at ? new Date(run.started_at).toLocaleString() : 'Pending'}</span>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-lg border border-slate-800">
          <span className="text-slate-500 block text-[10px]">COMPLETED AT</span>
          <span className="font-mono text-slate-200">{run.completed_at ? new Date(run.completed_at).toLocaleString() : 'In Progress'}</span>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-lg border border-slate-800">
          <span className="text-slate-500 block text-[10px]">TRIGGER EVENT</span>
          <span className="font-mono text-cyan-400">{run.trigger_event_id || 'Manual User Trigger'}</span>
        </div>
        <div className="bg-slate-900/60 p-3.5 rounded-lg border border-slate-800">
          <span className="text-slate-500 block text-[10px]">DAG SCHEDULER GATE</span>
          <span className="font-mono text-emerald-400">Authoritative Runtime</span>
        </div>
      </div>
    </div>
  );
};
