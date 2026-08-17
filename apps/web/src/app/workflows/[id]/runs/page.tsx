'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { useParams } from 'next/navigation';
import { AppShell } from '@/components/shell/AppShell';
import { WorkflowRunDetail } from '@/components/workflows/WorkflowRunDetail';
import { Activity, Play, RotateCcw, Server } from 'lucide-react';

export default function WorkflowRunsPage() {
  const params = useParams();
  const workflowId = (params?.id as string) || 'wf_default';
  const [runs, setRuns] = useState<any[]>([]);
  const [selectedRunId, setSelectedRunId] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const fetchRuns = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch(`/api/v1/workflows/${workflowId}/runs`);
      if (res.ok) {
        const data = await res.json();
        setRuns(data);
        if (data.length > 0 && !selectedRunId) {
          setSelectedRunId(data[0].id);
        }
      }
    } catch (err) {
      console.error('Failed to fetch workflow runs', err);
    } finally {
      setLoading(false);
    }
  }, [workflowId, selectedRunId]);

  useEffect(() => {
    fetchRuns();
  }, [fetchRuns]);

  return (
    <AppShell>
      <div className="flex flex-col h-full bg-slate-950 text-slate-100 p-6 space-y-6 overflow-y-auto">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-indigo-500/10 text-indigo-400 rounded-lg border border-indigo-500/20">
              <Activity className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight text-slate-50">Workflow Execution History</h1>
              <p className="text-xs text-slate-400">Telemetry logs for workflow executions running via DAG Scheduler</p>
            </div>
          </div>

          <button
            onClick={fetchRuns}
            className="flex items-center space-x-1.5 px-3 py-1.5 bg-slate-900 border border-slate-700 text-slate-300 hover:text-slate-100 rounded-lg text-xs font-medium transition"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Refresh</span>
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 flex-1">
          <div className="lg:col-span-1 bg-slate-900/50 border border-slate-800 rounded-xl p-4 flex flex-col space-y-3">
            <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Run History</h2>

            {loading ? (
              <div className="text-center py-8 text-xs text-slate-500">Loading runs...</div>
            ) : runs.length === 0 ? (
              <div className="text-center py-8 text-xs text-slate-500 border border-dashed border-slate-800 rounded-lg">
                No runs recorded for this workflow.
              </div>
            ) : (
              <div className="space-y-2 overflow-y-auto">
                {runs.map((r) => (
                  <div
                    key={r.id}
                    onClick={() => setSelectedRunId(r.id)}
                    className={`p-3 rounded-lg border cursor-pointer transition text-xs ${
                      selectedRunId === r.id
                        ? 'bg-indigo-500/10 border-indigo-500/30 text-slate-100'
                        : 'bg-slate-900/80 border-slate-800 hover:border-slate-700 text-slate-300'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-mono text-[11px] font-semibold text-slate-200">{r.id.slice(0, 12)}...</span>
                      <span className={`text-[10px] px-1.5 py-0.5 rounded font-medium uppercase ${
                        r.status === 'completed' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-slate-800 text-slate-400'
                      }`}>
                        {r.status}
                      </span>
                    </div>
                    <div className="text-[10px] text-slate-500">{new Date(r.created_at).toLocaleString()}</div>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="lg:col-span-2">
            {selectedRunId ? (
              <WorkflowRunDetail runId={selectedRunId} />
            ) : (
              <div className="p-8 text-center text-xs text-slate-500 bg-slate-900/50 border border-slate-800 rounded-xl">
                Select a workflow run to view execution telemetry.
              </div>
            )}
          </div>
        </div>
      </div>
    </AppShell>
  );
}
