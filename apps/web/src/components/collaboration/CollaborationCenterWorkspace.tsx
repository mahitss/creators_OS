"use client";

import React, { useState, useEffect } from "react";
import {
  Users,
  Bot,
  Layers,
  Target,
  ArrowRightLeft,
  AlertTriangle,
  Activity,
  ShieldCheck,
  RefreshCw,
  Clock,
  UserCheck
} from "lucide-react";

export function CollaborationCenterWorkspace() {
  const [overview, setOverview] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchOverview = async () => {
    setIsLoading(true);
    try {
      const res = await fetch("/api/v1/collaboration");
      if (res.ok) {
        const data = await res.json();
        setOverview(data);
      }
    } catch (err) {
      console.error("Failed to load collaboration center data:", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchOverview();
  }, []);

  return (
    <div className="p-6 space-y-6 max-w-[1600px] mx-auto text-slate-100 font-sans">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/80 p-6 rounded-2xl border border-slate-800 shadow-xl backdrop-blur-md">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-indigo-500/10 border border-indigo-500/20 rounded-xl text-indigo-400">
              <Users className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-3">
                Collaboration Center &amp; Workforce Intelligence
                <span className="text-xs px-2.5 py-1 bg-indigo-500/20 text-indigo-300 font-mono font-medium rounded-full border border-indigo-500/30">
                  Human-Centered Agent Coordination
                </span>
              </h1>
              <p className="text-xs text-slate-400 font-medium">
                Governed collaboration layer connecting humans, agents, teams, missions, and handoffs
              </p>
            </div>
          </div>
        </div>

        <button
          onClick={fetchOverview}
          className="p-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-xs font-semibold flex items-center gap-2 transition border border-slate-700/50"
        >
          <RefreshCw className={`w-4 h-4 ${isLoading ? "animate-spin" : ""}`} />
          Refresh Operations
        </button>
      </div>

      {/* Telemetry Grid */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Active Work Items</span>
            <Activity className="w-4 h-4 text-indigo-400" />
          </div>
          <p className="text-2xl font-bold text-indigo-400">{overview?.activeWorkItemsCount || 0}</p>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Pending Handoffs</span>
            <ArrowRightLeft className="w-4 h-4 text-cyan-400" />
          </div>
          <p className="text-2xl font-bold text-cyan-400">{overview?.pendingHandoffsCount || 0}</p>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Open Escalations</span>
            <AlertTriangle className="w-4 h-4 text-rose-400" />
          </div>
          <p className="text-2xl font-bold text-rose-400">{overview?.openEscalationsCount || 0}</p>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Workload Fairness</span>
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
          </div>
          <p className="text-2xl font-bold text-emerald-400">94.0%</p>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Automation Ideas</span>
            <Bot className="w-4 h-4 text-amber-400" />
          </div>
          <p className="text-2xl font-bold text-amber-400">{overview?.automationOpportunitiesCount || 0}</p>
        </div>
      </div>

      {/* Subsystems Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Pending Handoffs */}
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <ArrowRightLeft className="w-4 h-4 text-cyan-400" />
            Human &amp; Agent Handoff Stream
          </h2>

          <div className="space-y-3 font-mono text-xs">
            {overview?.handoffs?.map((h: any) => (
              <div key={h.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-cyan-300">{h.from_type} ({h.from_id}) → {h.to_type} ({h.to_id})</span>
                  <span className="text-[10px] bg-cyan-500/20 text-cyan-300 px-2 py-0.5 rounded font-bold uppercase">{h.status}</span>
                </div>
                <p className="text-slate-300 font-sans">{h.reason}</p>
                <p className="text-slate-500">Expected Output: {h.expected_output}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Escalations & Bottlenecks */}
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-rose-400" />
            Collaboration Escalations &amp; Bottlenecks
          </h2>

          <div className="space-y-3 font-mono text-xs">
            {overview?.escalations?.map((e: any) => (
              <div key={e.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-rose-300">Escalation: {e.escalation_type}</span>
                  <span className="text-[10px] bg-rose-500/20 text-rose-300 px-2 py-0.5 rounded font-bold uppercase">{e.status}</span>
                </div>
                <p className="text-slate-300 font-sans">{e.reason}</p>
                <p className="text-slate-500">Target Role: {e.target_role_or_user}</p>
              </div>
            ))}

            {overview?.bottlenecks?.map((b: any, idx: number) => (
              <div key={idx} className="p-3 bg-amber-500/10 border border-amber-500/20 rounded-xl text-amber-300 flex items-center justify-between">
                <span>{b.summary}</span>
                <span className="font-bold">{b.duration_hours}h bottleneck</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
