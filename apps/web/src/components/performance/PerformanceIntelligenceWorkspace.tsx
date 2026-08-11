"use client";

import React, { useState, useEffect } from "react";
import {
  BarChart3,
  Target,
  Clock,
  AlertTriangle,
  Layers,
  ShieldCheck,
  TrendingUp,
  Search,
  RefreshCw,
  Zap,
  Activity,
  Lightbulb
} from "lucide-react";

export function PerformanceIntelligenceWorkspace() {
  const [activeTab, setActiveTab] = useState<
    "overview" | "kpis" | "targets" | "alerts" | "forecasts" | "query"
  >("overview");

  const [overview, setOverview] = useState<any>(null);
  const [queryInput, setQueryInput] = useState("Which KPIs are deteriorating?");
  const [queryResult, setQueryResult] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchOverview = async () => {
    setIsLoading(true);
    try {
      const res = await fetch("/api/v1/performance");
      if (res.ok) {
        const data = await res.json();
        setOverview(data);
      }
    } catch (err) {
      console.error("Failed to load performance intelligence data:", err);
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
      const res = await fetch("/api/v1/performance/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: queryInput })
      });
      if (res.ok) {
        const data = await res.json();
        setQueryResult(data);
      }
    } catch (err) {
      console.error("NL Performance Query failed:", err);
    }
  };

  return (
    <div className="p-6 space-y-6 max-w-[1600px] mx-auto text-slate-100 font-sans">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/80 p-6 rounded-2xl border border-slate-800 shadow-xl backdrop-blur-md">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-emerald-400">
              <BarChart3 className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-3">
                Enterprise Performance Intelligence &amp; KPI OS 2.0
                <span className="text-xs px-2.5 py-1 bg-emerald-500/20 text-emerald-300 font-mono font-medium rounded-full border border-emerald-500/30">
                  Evidence-Backed KPI Engine
                </span>
              </h1>
              <p className="text-xs text-slate-400 font-medium">
                Governed measurement layer connecting strategy, outcomes, benefits, and operational metrics with full provenance
              </p>
            </div>
          </div>
        </div>

        <button
          onClick={fetchOverview}
          className="p-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-xs font-semibold flex items-center gap-2 transition border border-slate-700/50"
        >
          <RefreshCw className={`w-4 h-4 ${isLoading ? "animate-spin" : ""}`} />
          Refresh Performance
        </button>
      </div>

      {/* Top Telemetry Header */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Active KPIs</span>
            <Activity className="w-4 h-4 text-emerald-400" />
          </div>
          <p className="text-2xl font-bold text-emerald-400">{overview?.kpisCount || 0}</p>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>On-Track Rate</span>
            <TrendingUp className="w-4 h-4 text-cyan-400" />
          </div>
          <p className="text-2xl font-bold text-cyan-400">{overview?.onTrackRatePct || 0}%</p>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Stale Metrics</span>
            <Clock className="w-4 h-4 text-amber-400" />
          </div>
          <p className="text-2xl font-bold text-amber-400">{overview?.staleCount || 0}</p>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Active Alerts</span>
            <AlertTriangle className="w-4 h-4 text-rose-400" />
          </div>
          <p className="text-2xl font-bold text-rose-400">{overview?.alertsCount || 0}</p>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Performance Health</span>
            <ShieldCheck className="w-4 h-4 text-blue-400" />
          </div>
          <p className="text-2xl font-bold text-blue-400">95.0%</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-2 overflow-x-auto">
        {[
          { id: "overview", label: "Performance Overview", icon: BarChart3 },
          { id: "kpis", label: "KPI Registry & Definitions", icon: Activity },
          { id: "targets", label: "Targets & Versioning", icon: Target },
          { id: "alerts", label: "Alerts & Anomalies", icon: AlertTriangle },
          { id: "forecasts", label: "Forecasts & Drivers", icon: Lightbulb },
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
                  ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 shadow-sm"
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
            <BarChart3 className="w-4 h-4 text-emerald-400" />
            Performance Intelligence Overview
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 font-mono text-xs">
            <div className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
              <span className="font-bold text-emerald-300">Active Scorecards</span>
              <p className="text-slate-300 font-sans">Enterprise Scorecards grouped by Strategy, Portfolio, and Program.</p>
              <p className="text-slate-400">Total Scorecards: {overview?.scorecardsCount || 0}</p>
            </div>

            <div className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
              <span className="font-bold text-cyan-300">Correlated KPI Drivers</span>
              <p className="text-slate-300 font-sans">Measurable drivers associated with metric changes without unevidenced causality.</p>
              <p className="text-slate-400">Active Drivers: {overview?.drivers?.length || 0}</p>
            </div>
          </div>
        </div>
      )}

      {/* TAB CONTENT: KPIs */}
      {activeTab === "kpis" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Activity className="w-4 h-4 text-emerald-400" />
            KPI Registry &amp; Formula Definitions
          </h2>

          <div className="space-y-3 font-mono text-xs">
            {overview?.kpis?.map((k: any) => (
              <div key={k.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-emerald-300">{k.name} ({k.category})</span>
                  <span className="text-[10px] bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded font-bold uppercase">{k.status}</span>
                </div>
                <p className="text-slate-300 font-sans">{k.description}</p>
                <p className="text-slate-400 font-mono text-[11px] bg-slate-900/80 p-2 rounded border border-slate-800">Formula: {k.definition}</p>
                <p className="text-slate-500">Unit: {k.unit} | Direction: {k.direction} | Owner: {k.owner}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Targets */}
      {activeTab === "targets" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Target className="w-4 h-4 text-cyan-400" />
            Versioned KPI Targets &amp; Effective Dates
          </h2>

          <div className="space-y-3 font-mono text-xs">
            {overview?.targets?.map((t: any) => (
              <div key={t.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-cyan-300">Target Value: {t.target_value} (v{t.version})</span>
                  <span className="text-[10px] bg-cyan-500/20 text-cyan-300 px-2 py-0.5 rounded font-bold uppercase">Active</span>
                </div>
                <p className="text-slate-400">Effective: {t.effective_from} to {t.effective_to} | Owner: {t.owner}</p>
                <p className="text-slate-500">Approval Ref: {t.approval_reference}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Alerts */}
      {activeTab === "alerts" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-rose-400" />
            KPI Alerts &amp; Anomaly Signals
          </h2>

          <div className="space-y-3 font-mono text-xs">
            {overview?.alerts?.length === 0 ? (
              <p className="text-slate-400">No active anomaly or threshold alerts detected.</p>
            ) : (
              overview?.alerts?.map((a: any) => (
                <div key={a.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-rose-300">{a.title} ({a.alert_type})</span>
                    <span className="text-[10px] bg-rose-500/20 text-rose-300 px-2 py-0.5 rounded font-bold uppercase">{a.status}</span>
                  </div>
                  <p className="text-slate-300 font-sans">{a.description}</p>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Forecasts */}
      {activeTab === "forecasts" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Lightbulb className="w-4 h-4 text-emerald-400" />
            Predictive Forecasts &amp; Correlated Drivers
          </h2>

          <div className="space-y-4 font-mono text-xs">
            {overview?.forecasts?.map((f: any) => (
              <div key={f.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-emerald-300">Forecast Value: {f.forecast_value} ({f.confidence_pct}% confidence)</span>
                  <span className="text-[10px] bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded font-bold uppercase">Predictive</span>
                </div>
                <p className="text-slate-400">Bounds: Lower ({f.lower_bound}) — Upper ({f.upper_bound})</p>
              </div>
            ))}

            <h3 className="font-semibold text-slate-200 mt-2">Correlated Drivers:</h3>
            {overview?.drivers?.map((d: any) => (
              <div key={d.id} className="p-3 bg-slate-900/80 rounded-lg border border-slate-700 space-y-1">
                <span className="font-bold text-cyan-300">{d.driver_name} ({d.association_type})</span>
                <p className="text-slate-300 font-sans text-[11px]">{d.evidence_summary}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Query */}
      {activeTab === "query" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Search className="w-4 h-4 text-emerald-400" />
            Natural Language Performance Query
          </h2>

          <div className="space-y-3 font-mono text-xs">
            <div className="flex gap-2">
              <input
                type="text"
                value={queryInput}
                onChange={(e) => setQueryInput(e.target.value)}
                className="flex-1 bg-slate-800 border border-slate-700 text-slate-200 px-3 py-2 rounded-xl text-xs"
                placeholder="Ask a performance intelligence question..."
              />
              <button
                onClick={handleQuery}
                className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-semibold flex items-center gap-2"
              >
                <Search className="w-4 h-4" />
                Execute Query
              </button>
            </div>

            {queryResult && (
              <div className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <span className="font-bold text-emerald-300">Query: {queryResult.query} ({queryResult.confidencePct}% confidence)</span>
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
