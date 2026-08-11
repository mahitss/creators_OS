"use client";

import React, { useState, useEffect } from "react";
import {
  Briefcase,
  Layers,
  Rocket,
  AlertTriangle,
  GitPullRequest,
  CheckCircle2,
  TrendingUp,
  Search,
  RefreshCw,
  PieChart,
  ShieldCheck,
  Zap,
  HelpCircle,
  Lightbulb
} from "lucide-react";

export function PortfolioIntelligenceWorkspace() {
  const [activeTab, setActiveTab] = useState<
    "overview" | "programs" | "conflicts" | "overlaps" | "recommendations" | "query"
  >("overview");

  const [overview, setOverview] = useState<any>(null);
  const [queryInput, setQueryInput] = useState("Which initiatives are competing for capacity?");
  const [queryResult, setQueryResult] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchOverview = async () => {
    setIsLoading(true);
    try {
      const res = await fetch("/api/v1/portfolio");
      if (res.ok) {
        const data = await res.json();
        setOverview(data);
      }
    } catch (err) {
      console.error("Failed to load portfolio intelligence data:", err);
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
      const res = await fetch("/api/v1/portfolio/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: queryInput })
      });
      if (res.ok) {
        const data = await res.json();
        setQueryResult(data);
      }
    } catch (err) {
      console.error("NL Portfolio Query failed:", err);
    }
  };

  return (
    <div className="p-6 space-y-6 max-w-[1600px] mx-auto text-slate-100 font-sans">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/80 p-6 rounded-2xl border border-slate-800 shadow-xl backdrop-blur-md">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-cyan-500/10 border border-cyan-500/20 rounded-xl text-cyan-400">
              <Briefcase className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-3">
                Enterprise Portfolio Intelligence 2.0
                <span className="text-xs px-2.5 py-1 bg-cyan-500/20 text-cyan-300 font-mono font-medium rounded-full border border-cyan-500/30">
                  Human-Governed Investment Optimization
                </span>
              </h1>
              <p className="text-xs text-slate-400 font-medium">
                Portfolio intelligence layer linking programs, resource conflicts, overlaps, variances, and evidence-backed investment options
              </p>
            </div>
          </div>
        </div>

        <button
          onClick={fetchOverview}
          className="p-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-xs font-semibold flex items-center gap-2 transition border border-slate-700/50"
        >
          <RefreshCw className={`w-4 h-4 ${isLoading ? "animate-spin" : ""}`} />
          Refresh Portfolio
        </button>
      </div>

      {/* Top Telemetry Header */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Active Programs</span>
            <Layers className="w-4 h-4 text-cyan-400" />
          </div>
          <p className="text-2xl font-bold text-cyan-400">{overview?.programsCount || 0}</p>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Resource Conflicts</span>
            <AlertTriangle className="w-4 h-4 text-rose-400" />
          </div>
          <p className="text-2xl font-bold text-rose-400">{overview?.resourceConflictsCount || 0}</p>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Overlap Signals</span>
            <GitPullRequest className="w-4 h-4 text-amber-400" />
          </div>
          <p className="text-2xl font-bold text-amber-400">{overview?.overlapsCount || 0}</p>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Outcome Variances</span>
            <TrendingUp className="w-4 h-4 text-purple-400" />
          </div>
          <p className="text-2xl font-bold text-purple-400">{overview?.variancesCount || 0}</p>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Portfolio Health</span>
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
          </div>
          <p className="text-2xl font-bold text-emerald-400">92.0%</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-2 overflow-x-auto">
        {[
          { id: "overview", label: "Portfolio Overview", icon: Briefcase },
          { id: "programs", label: "Programs & Initiatives", icon: Layers },
          { id: "conflicts", label: "Resource Conflicts", icon: AlertTriangle },
          { id: "overlaps", label: "Overlaps & Redundancies", icon: GitPullRequest },
          { id: "recommendations", label: "Investment Recommendations", icon: Lightbulb },
          { id: "query", label: "Natural Language Portfolio Query", icon: Search }
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`px-4 py-2 rounded-xl text-xs font-semibold flex items-center gap-2 whitespace-nowrap transition ${
                isActive
                  ? "bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 shadow-sm"
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
            <Briefcase className="w-4 h-4 text-cyan-400" />
            Active Portfolio Overview
          </h2>

          <div className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2 font-mono text-xs">
            <span className="font-bold text-cyan-300">{overview?.portfolio?.name}</span>
            <p className="text-slate-300 font-sans">{overview?.portfolio?.description}</p>
            <p className="text-slate-400">Owner: {overview?.portfolio?.owner} | Status: <strong className="text-emerald-400">{overview?.portfolio?.status}</strong></p>
          </div>
        </div>
      )}

      {/* TAB CONTENT: Programs */}
      {activeTab === "programs" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Layers className="w-4 h-4 text-cyan-400" />
            Programs &amp; Strategic Objectives
          </h2>

          <div className="space-y-3 font-mono text-xs">
            {overview?.programs?.map((pr: any) => (
              <div key={pr.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-cyan-300">{pr.name}</span>
                  <span className="text-[10px] bg-cyan-500/20 text-cyan-300 px-2 py-0.5 rounded font-bold uppercase">{pr.status}</span>
                </div>
                <p className="text-slate-300 font-sans">{pr.description}</p>
                <p className="text-slate-400">Target Outcome: {pr.target_outcome} | Priority: {pr.priority}</p>
                <p className="text-slate-500">Owner: {pr.owner}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Conflicts */}
      {activeTab === "conflicts" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-rose-400" />
            Resource Conflicts &amp; Scarce Capacity Bottlenecks
          </h2>

          <div className="space-y-3 font-mono text-xs">
            {overview?.conflicts?.map((c: any) => (
              <div key={c.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-rose-300">Conflict: {c.resource_type} ({c.time_window})</span>
                  <span className="text-[10px] bg-rose-500/20 text-rose-300 px-2 py-0.5 rounded font-bold uppercase">{c.status}</span>
                </div>
                <p className="text-slate-300 font-sans">{c.capacity_gap_summary}</p>
                <p className="text-slate-400">Competing Initiatives: {JSON.stringify(c.competing_initiatives_json)}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Overlaps */}
      {activeTab === "overlaps" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <GitPullRequest className="w-4 h-4 text-amber-400" />
            Portfolio Overlaps &amp; Redundancies
          </h2>

          <div className="space-y-3 font-mono text-xs">
            {overview?.overlaps?.map((o: any) => (
              <div key={o.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-amber-300">Overlap Type: {o.overlap_type}</span>
                  <span className="text-[10px] bg-amber-500/20 text-amber-300 px-2 py-0.5 rounded font-bold uppercase">{o.status}</span>
                </div>
                <p className="text-slate-300 font-sans">{o.similarity_summary}</p>
                <p className="text-slate-400">Initiatives Involved: {JSON.stringify(o.initiative_ids_json)}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Recommendations */}
      {activeTab === "recommendations" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Lightbulb className="w-4 h-4 text-cyan-400" />
            Evidence-Backed Investment Recommendations &amp; Gated Approvals
          </h2>

          <div className="space-y-4 font-mono text-xs">
            {overview?.recommendations?.map((r: any) => (
              <div key={r.id} className="p-5 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-3">
                <div className="flex justify-between items-center">
                  <span className="font-bold text-cyan-300 text-sm">{r.recommendation} ({r.confidence_pct}% confidence)</span>
                  <span className="text-[10px] px-2 py-0.5 bg-amber-500/20 text-amber-300 rounded font-bold uppercase">Approval {r.approval_status}</span>
                </div>
                <p className="text-slate-400 font-sans">Evidence: {JSON.stringify(r.evidence_json)}</p>

                <h3 className="font-semibold text-slate-200 mt-2">Investment Options:</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {r.alternatives_json?.map((alt: any, idx: number) => (
                    <div key={idx} className="p-3 bg-slate-900/80 rounded-lg border border-slate-700 space-y-1">
                      <span className="font-bold text-emerald-300">{alt.option}</span>
                      <p className="text-slate-300 font-sans text-[11px]">{alt.description}</p>
                      <div className="flex justify-between items-center text-[10px] text-slate-400 pt-1">
                        <span>Cost Impact: {alt.cost_impact}</span>
                        <span className="px-1.5 py-0.5 bg-blue-500/20 text-blue-300 rounded font-mono">{alt.reversibility}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Natural Language Portfolio Query */}
      {activeTab === "query" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Search className="w-4 h-4 text-cyan-400" />
            Natural Language Portfolio Queries
          </h2>

          <div className="space-y-3 font-mono text-xs">
            <div className="flex gap-2">
              <input
                type="text"
                value={queryInput}
                onChange={(e) => setQueryInput(e.target.value)}
                className="flex-1 bg-slate-800 border border-slate-700 text-slate-200 px-3 py-2 rounded-xl text-xs"
                placeholder="Ask a portfolio intelligence question..."
              />
              <button
                onClick={handleQuery}
                className="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-xl text-xs font-semibold flex items-center gap-2"
              >
                <Search className="w-4 h-4" />
                Execute Query
              </button>
            </div>

            {queryResult && (
              <div className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <span className="font-bold text-cyan-300">Query: {queryResult.query} ({queryResult.confidencePct}% confidence)</span>
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
