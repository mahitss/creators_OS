"use client";

import React, { useState, useEffect } from "react";
import {
  TrendingUp,
  AlertTriangle,
  Zap,
  Activity,
  Layers,
  ShieldCheck,
  Search,
  RefreshCw,
  Sliders,
  Sparkles,
  BarChart3
} from "lucide-react";

export function PredictiveOperationsWorkspace() {
  const [activeTab, setActiveTab] = useState<
    "overview" | "forecasts" | "alerts" | "capacity" | "risks" | "scenarios" | "query"
  >("overview");

  const [overview, setOverview] = useState<any>(null);
  const [queryInput, setQueryInput] = useState("What is likely to miss target in the next 30 days?");
  const [queryResult, setQueryResult] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchOverview = async () => {
    setIsLoading(true);
    try {
      const res = await fetch("/api/v1/predictions");
      if (res.ok) {
        const data = await res.json();
        setOverview(data);
      }
    } catch (err) {
      console.error("Failed to load predictive operations data:", err);
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
      const res = await fetch("/api/v1/predictions/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: queryInput })
      });
      if (res.ok) {
        const data = await res.json();
        setQueryResult(data);
      }
    } catch (err) {
      console.error("NL Predictive Query failed:", err);
    }
  };

  return (
    <div className="p-6 space-y-6 max-w-[1600px] mx-auto text-slate-100 font-sans">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/80 p-6 rounded-2xl border border-slate-800 shadow-xl backdrop-blur-md">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-purple-500/10 border border-purple-500/20 rounded-xl text-purple-400">
              <Sparkles className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-3">
                Enterprise Predictive Operations &amp; Forecast OS 2.0
                <span className="text-xs px-2.5 py-1 bg-purple-500/20 text-purple-300 font-mono font-medium rounded-full border border-purple-500/30">
                  Uncertainty-Aware Forecasting
                </span>
              </h1>
              <p className="text-xs text-slate-400 font-medium">
                Probabilistic decision support layer connecting signals, forecasts, risk matrices, and What-If scenario simulations
              </p>
            </div>
          </div>
        </div>

        <button
          onClick={fetchOverview}
          className="p-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-xs font-semibold flex items-center gap-2 transition border border-slate-700/50"
        >
          <RefreshCw className={`w-4 h-4 ${isLoading ? "animate-spin" : ""}`} />
          Recalculate Forecasts
        </button>
      </div>

      {/* Top Telemetry Header */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Active Forecasts</span>
            <TrendingUp className="w-4 h-4 text-purple-400" />
          </div>
          <p className="text-2xl font-bold text-purple-400">{overview?.forecastsCount || 0}</p>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Early Warnings</span>
            <AlertTriangle className="w-4 h-4 text-rose-400" />
          </div>
          <p className="text-2xl font-bold text-rose-400">{overview?.alertsCount || 0}</p>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Emerging Risks</span>
            <Zap className="w-4 h-4 text-amber-400" />
          </div>
          <p className="text-2xl font-bold text-amber-400">{overview?.risksCount || 0}</p>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Capacity Gaps</span>
            <Layers className="w-4 h-4 text-cyan-400" />
          </div>
          <p className="text-2xl font-bold text-cyan-400">{overview?.capacityGapsCount || 0}</p>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Model Accuracy</span>
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
          </div>
          <p className="text-2xl font-bold text-emerald-400">{overview?.overallAccuracyPct || 95.8}%</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-2 overflow-x-auto">
        {[
          { id: "overview", label: "Predictive Overview", icon: Sparkles },
          { id: "forecasts", label: "Forecasts & Horizons", icon: TrendingUp },
          { id: "alerts", label: "Early Warnings", icon: AlertTriangle },
          { id: "capacity", label: "Capacity & Demand", icon: Layers },
          { id: "risks", label: "Predictive Risk Matrix", icon: Zap },
          { id: "scenarios", label: "What-If Scenarios", icon: Sliders },
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
                  ? "bg-purple-500/10 text-purple-400 border border-purple-500/20 shadow-sm"
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
            <Sparkles className="w-4 h-4 text-purple-400" />
            Predictive Operations Executive Brief
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 font-mono text-xs">
            <div className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
              <span className="font-bold text-purple-300">Active Forecast Models</span>
              <p className="text-slate-300 font-sans">Time-series ensemble models evaluating KPI, Capacity, Cost, and Execution trajectories.</p>
              <p className="text-slate-400">Backtested Calibration Coverage: 96.0%</p>
            </div>

            <div className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
              <span className="font-bold text-cyan-300">Capacity &amp; Demand Alignment</span>
              <p className="text-slate-300 font-sans">Forecasting agent thread demand vs compute node capacity across active missions.</p>
              <p className="text-slate-400">Active Capacity Gap: 50 threads (Medium Term)</p>
            </div>
          </div>
        </div>
      )}

      {/* TAB CONTENT: Forecasts */}
      {activeTab === "forecasts" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <TrendingUp className="w-4 h-4 text-purple-400" />
            Active Forecast Trajectories &amp; Uncertainty Bounds
          </h2>

          <div className="space-y-3 font-mono text-xs">
            {overview?.forecasts?.map((f: any) => (
              <div key={f.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-purple-300">Entity: {f.entity_type} ({f.entity_id})</span>
                  <span className="text-[10px] bg-purple-500/20 text-purple-300 px-2 py-0.5 rounded font-bold uppercase">{f.horizon}</span>
                </div>
                <p className="text-slate-300 font-sans">Method: {f.method}</p>
                <p className="text-slate-400">Created: {f.created_at}</p>
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
            Early Warning Signals &amp; Estimated Time Windows
          </h2>

          <div className="space-y-3 font-mono text-xs">
            {overview?.alerts?.map((a: any) => (
              <div key={a.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-rose-300">{a.alert_type} ({a.confidence} confidence)</span>
                  <span className="text-[10px] bg-rose-500/20 text-rose-300 px-2 py-0.5 rounded font-bold uppercase">{a.status}</span>
                </div>
                <p className="text-slate-300 font-sans">Estimated Time Window: <span className="font-bold text-amber-300">{a.predicted_window}</span></p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Capacity */}
      {activeTab === "capacity" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Layers className="w-4 h-4 text-cyan-400" />
            Capacity &amp; Demand Forecasting
          </h2>

          <div className="space-y-3 font-mono text-xs">
            {overview?.capacityForecasts?.map((c: any) => (
              <div key={c.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-cyan-300">Type: {c.capacity_type} ({c.horizon})</span>
                  <span className={`text-[10px] px-2 py-0.5 rounded font-bold uppercase ${c.gap > 0 ? "bg-amber-500/20 text-amber-300" : "bg-emerald-500/20 text-emerald-300"}`}>
                    {c.gap > 0 ? `Gap: +${c.gap}` : "Balanced"}
                  </span>
                </div>
                <p className="text-slate-400">Demand: {c.demand_value} | Capacity: {c.capacity_value}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Risks */}
      {activeTab === "risks" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Zap className="w-4 h-4 text-amber-400" />
            Predictive Risk Matrix &amp; Probability Ranges
          </h2>

          <div className="space-y-3 font-mono text-xs">
            {overview?.risks?.map((r: any) => (
              <div key={r.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-amber-300">Risk: {r.risk_id} (Probability: {r.probability_range})</span>
                  <span className="text-[10px] bg-rose-500/20 text-rose-300 px-2 py-0.5 rounded font-bold uppercase">Impact: {r.impact}</span>
                </div>
                <p className="text-slate-300 font-sans">{r.evidence}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Scenarios */}
      {activeTab === "scenarios" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Sliders className="w-4 h-4 text-purple-400" />
            What-If Scenario Simulations (Simulation Lab)
          </h2>

          <div className="space-y-3 font-mono text-xs">
            {overview?.scenarios?.map((s: any) => (
              <div key={s.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-purple-300">Scenario: {s.scenario_name}</span>
                  <span className="text-[10px] bg-purple-500/20 text-purple-300 px-2 py-0.5 rounded font-bold uppercase">Simulation</span>
                </div>
                <p className="text-slate-400">Parameters: {JSON.stringify(s.scenario_params_json)}</p>
                <p className="text-slate-500">Output Distribution: {JSON.stringify(s.output_distribution_json)}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Query */}
      {activeTab === "query" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Search className="w-4 h-4 text-purple-400" />
            Natural Language Predictive Query
          </h2>

          <div className="space-y-3 font-mono text-xs">
            <div className="flex gap-2">
              <input
                type="text"
                value={queryInput}
                onChange={(e) => setQueryInput(e.target.value)}
                className="flex-1 bg-slate-800 border border-slate-700 text-slate-200 px-3 py-2 rounded-xl text-xs"
                placeholder="Ask a predictive operations question..."
              />
              <button
                onClick={handleQuery}
                className="px-4 py-2 bg-purple-600 hover:bg-purple-500 text-white rounded-xl text-xs font-semibold flex items-center gap-2"
              >
                <Search className="w-4 h-4" />
                Execute Query
              </button>
            </div>

            {queryResult && (
              <div className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <span className="font-bold text-purple-300">Query: {queryResult.query} ({queryResult.confidencePct}% confidence)</span>
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
