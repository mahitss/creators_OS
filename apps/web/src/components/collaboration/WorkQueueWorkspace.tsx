"use client";

import React, { useState, useEffect } from "react";
import {
  Briefcase,
  Users,
  Bot,
  AlertOctagon,
  FileCheck,
  ShieldAlert,
  Clock,
  ArrowRightLeft,
  CheckCircle2,
  XCircle,
  Plus,
  RefreshCw
} from "lucide-react";

export function WorkQueueWorkspace() {
  const [activeTab, setActiveTab] = useState<"my_work" | "team_work" | "agent_work" | "blocked" | "review" | "approvals">("my_work");
  const [workItems, setWorkItems] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchWorkItems = async () => {
    setIsLoading(true);
    try {
      const res = await fetch("/api/v1/work");
      if (res.ok) {
        const data = await res.json();
        setWorkItems(data);
      }
    } catch (err) {
      console.error("Failed to load work queue items:", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchWorkItems();
  }, []);

  const filteredItems = workItems.filter((item) => {
    if (activeTab === "my_work") return item.assigneeType === "human";
    if (activeTab === "agent_work") return item.assigneeType === "agent";
    if (activeTab === "blocked") return item.status === "blocked";
    if (activeTab === "review") return item.status === "awaiting_review";
    if (activeTab === "approvals") return item.status === "awaiting_approval";
    return true; // team_work
  });

  return (
    <div className="p-6 space-y-6 max-w-[1600px] mx-auto text-slate-100 font-sans">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/80 p-6 rounded-2xl border border-slate-800 shadow-xl backdrop-blur-md">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-blue-500/10 border border-blue-500/20 rounded-xl text-blue-400">
              <Briefcase className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-3">
                Enterprise Work Queue
                <span className="text-xs px-2.5 py-1 bg-blue-500/20 text-blue-300 font-mono font-medium rounded-full border border-blue-500/30">
                  Policy-Governed Work Routing
                </span>
              </h1>
              <p className="text-xs text-slate-400 font-medium">
                Unified task queue connecting humans, teams, agents, missions, handoffs, and approvals
              </p>
            </div>
          </div>
        </div>

        <button
          onClick={fetchWorkItems}
          className="p-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-xs font-semibold flex items-center gap-2 transition border border-slate-700/50"
        >
          <RefreshCw className={`w-4 h-4 ${isLoading ? "animate-spin" : ""}`} />
          Refresh Queue
        </button>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-2 overflow-x-auto">
        {[
          { id: "my_work", label: "My Work", icon: Briefcase },
          { id: "team_work", label: "Team Work", icon: Users },
          { id: "agent_work", label: "Agent Work", icon: Bot },
          { id: "blocked", label: "Blocked", icon: AlertOctagon },
          { id: "review", label: "Pending Review", icon: FileCheck },
          { id: "approvals", label: "Approvals", icon: ShieldAlert }
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`px-4 py-2 rounded-xl text-xs font-semibold flex items-center gap-2 whitespace-nowrap transition ${
                isActive
                  ? "bg-blue-500/10 text-blue-400 border border-blue-500/20 shadow-sm"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
              }`}
            >
              <Icon className="w-4 h-4" />
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Work Item List */}
      <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
        <h2 className="text-sm font-semibold text-white flex items-center gap-2">
          <Briefcase className="w-4 h-4 text-blue-400" />
          Queue Items ({filteredItems.length})
        </h2>

        <div className="space-y-3 font-mono text-xs">
          {filteredItems.map((item) => (
            <div key={item.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-bold text-blue-300">{item.title}</span>
                <span className="text-[10px] bg-slate-800 text-slate-300 border border-slate-700 px-2 py-0.5 rounded font-bold uppercase">{item.status}</span>
              </div>
              <p className="text-slate-400 font-sans">{item.description}</p>
              <div className="flex items-center gap-4 text-slate-500 text-[11px]">
                <span>Classification: <strong className="text-blue-400">{item.workClassification}</strong></span>
                <span>Assignee: <strong className="text-emerald-400">{item.assigneeType} ({item.assigneeId || "unassigned"})</strong></span>
                <span>Priority: <strong className="text-amber-400">{item.priority}</strong></span>
              </div>
            </div>
          ))}
          {filteredItems.length === 0 && (
            <p className="text-slate-500 text-xs py-4 text-center">No work items found in this queue view.</p>
          )}
        </div>
      </div>
    </div>
  );
}
