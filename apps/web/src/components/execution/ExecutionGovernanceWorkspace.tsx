"use client";

import React, { useState, useEffect } from "react";
import {
  CheckSquare,
  Award,
  Calendar,
  AlertOctagon,
  ShieldCheck,
  FileDiff,
  TrendingUp,
  Search,
  RefreshCw,
  Clock,
  ShieldAlert,
  Zap,
  HelpCircle
} from "lucide-react";

export function ExecutionGovernanceWorkspace() {
  const [activeTab, setActiveTab] = useState<
    "overview" | "benefits" | "milestones" | "variances" | "gates" | "query"
  >("overview");

  const [overview, setOverview] = useState<any>(null);
  const [queryInput, setQueryInput] = useState("Which initiatives are actually delivering benefits?");
  const [queryResult, setQueryResult] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchOverview = async () => {
    setIsLoading(true);
    try {
      const res = await fetch("/api/v1/execution");
      if (res.ok) {
        const data = await res.json();
        setOverview(data);
      }
    } catch (err) {
      console.error("Failed to load execution governance data:", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchOverview();
  }, []);

  const handleQuery = async () => {
    if (!queryInput) return;
    try {
      const res = await fetch("/api/v1/execution/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: queryInput })
      });
      if (res.ok) {
        const data = await res.json();
        setQueryResult(data);
      }
    } catch (err) {
      console.error("NL Execution Query failed:", err);
    }
  };

  return (
    <div className="p-6 space-y-6 max-w-[1600px] mx-auto text-slate-100 font-sans">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/80 p-6 rounded-2xl border border-slate-800 shadow-xl backdrop-blur-md">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-indigo-500/10 border border-indigo-500/20 rounded-xl text-indigo-400">
              <CheckSquare className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-3">
                Execution Governance &amp; Benefits Realization 2.0
                <span className="text-xs px-2.5 py-1 bg-indigo-500/20 text-indigo-300 font-mono font-medium rounded-full border border-indigo-500/30">
                  Evidence-Backed Value Intelligence
                </span>
              </h1>
              <p className="text-xs text-slate-400 font-medium">
                Governed bridge from strategy and portfolio commitments to measured benefits, verified deliverables, and baseline change control
              </p>
            </div>
          </div>
        </div>

        <button
          onClick={fetchOverview}
          className="p-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-xs font-semibold flex items-center gap-2 transition border border-slate-700/50"
        >
          <RefreshCw className={`w-4 h-4 ${isLoading ? "animate-spin" : ""}`} />
          Refresh Governance
        </button>
      </div>

      {/* Top Telemetry Header */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Tracked Benefits</span>
            <Award className="w-4 h-4 text-indigo-400" />
          </div>
          <p className="text-2xl font-bold text-indigo-400">{overview?.benefitsCount || 0}</p>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Realized Rate</span>
            <TrendingUp className="w-4 h-4 text-emerald-400" />
          </div>
          <p className="text-2xl font-bold text-emerald-400">{overview?.achievedRatePct || 0}%</p>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Active Milestones</span>
            <Calendar className="w-4 h-4 text-cyan-400" />
          </div>
          <p className="text-2xl font-bold text-cyan-400">{overview?.milestonesCount || 0}</p>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Variances Tracked</span>
            <AlertOctagon className="w-4 h-4 text-amber-400" />
          </div>
          <p className="text-2xl font-bold text-amber-400">{overview?.variancesCount || 0}</p>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Execution Health</span>
            <ShieldCheck className="w-4 h-4 text-blue-400" />
          </div>
          <p className="text-2xl font-bold text-blue-400">94.0%</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-2 overflow-x-auto">
        {[
          { id: "overview", label: "Execution Overview", icon: CheckSquare },
          { id: "benefits", label: "Benefits & Evidence", icon: Award },
          { id: "milestones", label: "Milestones & Deliverables", icon: Calendar },
          { id: "variances", label: "Variances & Forecasts", icon: AlertOctagon },
          { id: "gates", label: "Governance Gates & Waivers", icon: ShieldCheck },
          { id: "query", label: "Natural Language Query", icon: Search }
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`px-4 py-2 rounded-xl text-xs font-semibold flex items-center gap-2 whitespace-nowrap transition ${
                isActive
                  ? "bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 shadow-sm"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
              }`}
            >
              <Icon className="w-4 h-4" />
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* TAB CONTENT: Overview */}
      {activeTab === "overview" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <CheckSquare className="w-4 h-4 text-indigo-400" />
            Execution Governance Summary
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 font-mono text-xs">
            <div className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
              <span className="font-bold text-indigo-300">Active Change Requests</span>
              <p className="text-slate-300 font-sans">Pending scope &amp; timeline adjustments awaiting approval.</p>
              <p className="text-slate-400">Total Pending: {overview?.changeRequestsCount || 0}</p>
            </div>

            <div className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
              <span className="font-bold text-emerald-300">Evidence Verification Status</span>
              <p className="text-slate-300 font-sans">Verified vs unverified benefit evidence points.</p>
              <p className="text-slate-400">Verified Evidences: {overview?.evidences?.length || 0}</p>
            </div>
          </div>
        </div>
      )}

      {/* TAB CONTENT: Benefits */}
      {activeTab === "benefits" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Award className="w-4 h-4 text-indigo-400" />
            Measured Benefits &amp; Verifiable Evidence
          </h2>

          <div className="space-y-3 font-mono text-xs">
            {overview?.benefits?.map((b: any) => (
              <div key={b.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-indigo-300">{b.name} ({b.benefit_type})</span>
                  <span className="text-[10px] bg-indigo-500/20 text-indigo-300 px-2 py-0.5 rounded font-bold uppercase">{b.status}</span>
                </div>
                <p className="text-slate-300 font-sans">{b.description}</p>
                <div className="flex justify-between text-slate-400 text-[11px] pt-1">
                  <span>Baseline: {b.baseline} {b.unit}</span>
                  <span className="text-emerald-400 font-bold">Current: {b.current_value} {b.unit}</span>
                  <span>Target: {b.target} {b.unit}</span>
                </div>
                <p className="text-slate-500">Method: {b.measurement_method}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Milestones */}
      {activeTab === "milestones" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Calendar className="w-4 h-4 text-cyan-400" />
            Execution Milestones &amp; Deliverables
          </h2>

          <div className="space-y-3 font-mono text-xs">
            {overview?.milestones?.map((m: any) => (
              <div key={m.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-cyan-300">{m.name}</span>
                  <span className="text-[10px] bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded font-bold uppercase">{m.status}</span>
                </div>
                <p className="text-slate-300 font-sans">{m.description}</p>
                <p className="text-slate-400">Due Date: {m.due_date} | Evidence: {m.completion_evidence}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Variances */}
      {activeTab === "variances" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <AlertOctagon className="w-4 h-4 text-amber-400" />
            Execution Variances &amp; Predictive Forecasts
          </h2>

          <div className="space-y-3 font-mono text-xs">
            {overview?.variances?.map((v: any) => (
              <div key={v.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-amber-300">Variance Type: {v.variance_type}</span>
                  <span className="text-[10px] bg-amber-500/20 text-amber-300 px-2 py-0.5 rounded font-bold uppercase">{v.severity}</span>
                </div>
                <p className="text-slate-300 font-sans">{v.delta}</p>
                <p className="text-slate-400">{v.baseline} → {v.forecast}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Gates */}
      {activeTab === "gates" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-blue-400" />
            Quality &amp; Governance Gates
          </h2>

          <div className="space-y-3 font-mono text-xs">
            {overview?.gates?.map((g: any) => (
              <div key={g.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-blue-300">Gate: {g.gate_type}</span>
                  <span className="text-[10px] bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded font-bold uppercase">{g.status}</span>
                </div>
                <p className="text-slate-400">Initiative ID: {g.initiative_id}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Query */}
      {activeTab === "query" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Search className="w-4 h-4 text-indigo-400" />
            Natural Language Execution Query
          </h2>

          <div className="space-y-3 font-mono text-xs">
            <div className="flex gap-2">
              <input
                type="text"
                value={queryInput}
                onChange={(e) => setQueryInput(e.target.value)}
                className="flex-1 bg-slate-800 border border-slate-700 text-slate-200 px-3 py-2 rounded-xl text-xs"
                placeholder="Ask an execution governance question..."
              />
              <button
                onClick={handleQuery}
                className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-xs font-semibold flex items-center gap-2"
              >
                <Search className="w-4 h-4" />
                Execute Query
              </button>
            </div>

            {queryResult && (
              <div className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <span className="font-bold text-indigo-300">Query: {queryResult.query} ({queryResult.confidencePct}% confidence)</span>
                <p className="text-slate-300">Results: {JSON.stringify(queryResult.results)}</p>
                <p className="text-slate-500">Evidence: {JSON.stringify(queryResult.evidenceJson)}</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
