'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { AppShell } from '@/components/shell/AppShell';
import {
  GitBranch,
  Plus,
  Play,
  CheckCircle2,
  Clock,
  ShieldCheck,
  RefreshCw,
  FileCode
} from 'lucide-react';

interface WorkflowItem {
  id: string;
  name: string;
  description: string | null;
  status: string;
  version: number;
  visibility: string;
  updated_at: string;
}

export default function WorkflowsPage() {
  const router = useRouter();
  const [workflows, setWorkflows] = useState<WorkflowItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [showCreateModal, setShowCreateModal] = useState<boolean>(false);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');

  useEffect(() => {
    fetchWorkflows();
  }, []);

  const fetchWorkflows = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/workflows?workspaceId=ws_default_creator');
      if (res.ok) {
        const data = await res.json();
        setWorkflows(data);
      }
    } catch (err) {
      console.error('Failed to fetch workflows', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateWorkflow = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch('/api/v1/workflows', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          workspace_id: 'ws_default_creator',
          name,
          description,
          visibility: 'workspace'
        })
      });
      if (res.ok) {
        const wf = await res.json();
        router.push(`/workflows/${wf.id}`);
      }
    } catch (err) {
      console.error('Failed to create workflow', err);
    }
  };

  const handleManualRun = async (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    try {
      const res = await fetch(`/api/v1/workflows/${id}/run`, { method: 'POST' });
      if (res.ok) {
        router.push(`/workflows/${id}/runs`);
      }
    } catch (err) {
      console.error('Failed to trigger workflow run', err);
    }
  };

  return (
    <AppShell>
      <div className="flex flex-col h-full bg-slate-950 text-slate-100 p-6 space-y-6 overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-indigo-500/10 text-indigo-400 rounded-lg border border-indigo-500/20">
              <GitBranch className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight text-slate-50">Visual Workflows & Automation Engine</h1>
              <p className="text-xs text-slate-400">Author visual DAG workflows, compile immutable versions, and execute through DAG Scheduler</p>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            <button
              onClick={fetchWorkflows}
              className="flex items-center space-x-1.5 px-3 py-1.5 bg-slate-900 border border-slate-700 text-slate-300 hover:text-slate-100 rounded-lg text-xs font-medium transition"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>Refresh</span>
            </button>

            <button
              onClick={() => setShowCreateModal(true)}
              className="flex items-center space-x-1.5 px-3.5 py-1.5 bg-gradient-to-r from-indigo-500 to-indigo-600 hover:from-indigo-600 hover:to-indigo-700 text-white font-semibold rounded-lg text-xs shadow-lg shadow-indigo-500/10 transition"
            >
              <Plus className="w-4 h-4" />
              <span>New Workflow</span>
            </button>
          </div>
        </div>

        {/* Workflow Cards Library Grid */}
        {loading ? (
          <div className="text-center py-16 text-slate-500 text-xs">Loading workflow library...</div>
        ) : workflows.length === 0 ? (
          <div className="text-center py-16 text-slate-500 text-xs border border-dashed border-slate-800 rounded-xl p-8 space-y-3">
            <p>No workflows created yet.</p>
            <button
              onClick={() => setShowCreateModal(true)}
              className="px-3.5 py-2 bg-indigo-600 text-white rounded-lg text-xs font-semibold"
            >
              Create Your First Workflow
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {workflows.map((wf) => (
              <div
                key={wf.id}
                onClick={() => router.push(`/workflows/${wf.id}`)}
                className="p-5 bg-slate-900/60 border border-slate-800 hover:border-indigo-500/50 rounded-xl cursor-pointer transition flex flex-col justify-between space-y-4 group"
              >
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-bold text-slate-100 group-hover:text-indigo-400 transition">{wf.name}</span>
                    <span className={`text-[10px] px-2 py-0.5 rounded-full border font-medium uppercase ${
                      wf.status === 'active' ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400' : 'bg-slate-800 border-slate-700 text-slate-400'
                    }`}>
                      {wf.status} v{wf.version}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 line-clamp-2">{wf.description || 'No description provided.'}</p>
                </div>

                <div className="flex items-center justify-between border-t border-slate-800/80 pt-3 text-[11px] text-slate-500">
                  <span>Scope: {wf.visibility}</span>
                  <button
                    onClick={(e) => handleManualRun(e, wf.id)}
                    className="flex items-center space-x-1 text-indigo-400 hover:text-indigo-300 font-medium"
                  >
                    <Play className="w-3 h-3" />
                    <span>Run Now</span>
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Modal: New Workflow */}
        {showCreateModal && (
          <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4 z-50">
            <div className="bg-slate-900 border border-slate-800 rounded-xl max-w-md w-full p-6 space-y-4 shadow-2xl">
              <h2 className="text-base font-bold text-slate-100">Create New Visual Workflow</h2>

              <form onSubmit={handleCreateWorkflow} className="space-y-3 text-xs">
                <div>
                  <label className="block text-slate-400 mb-1">Workflow Name</label>
                  <input
                    type="text"
                    required
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="e.g. Executive Morning Briefing Pipeline"
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:border-indigo-500"
                  />
                </div>

                <div>
                  <label className="block text-slate-400 mb-1">Description</label>
                  <textarea
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    placeholder="Workflow authoring purpose and capabilities"
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:border-indigo-500 h-20"
                  />
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
                    className="px-3.5 py-2 bg-indigo-600 text-white rounded-lg font-semibold hover:bg-indigo-500"
                  >
                    Open Canvas
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </AppShell>
  );
}
