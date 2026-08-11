"use client";

import React, { useState, useEffect } from "react";
import {
  Compass,
  Target,
  Rocket,
  HelpCircle,
  Play,
  Lightbulb,
  Activity,
  AlertTriangle,
  Search,
  RefreshCw,
  TrendingUp,
  ShieldCheck,
  DollarSign,
  ArrowRight
} from "lucide-react";

export function StrategicPlanningWorkspace() {
  const [activeTab, setActiveTab] = useState<
    "overview" | "objectives" | "initiatives" | "assumptions" | "scenarios" | "recommendations" | "reviews" | "query"
  >("overview");

  const [overview, setOverview] = useState<any>(null);
  const [queryInput, setQueryInput] = useState("Which objectives are most at risk?");
  const [queryResult, setQueryResult] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchOverview = async () => {
    setIsLoading(true);
    try {
      const res = await fetch("/api/v1/strategy");
      if (res.ok) {
        const data = await res.json();
        setOverview(data);
      }
    } catch (err) {
      console.error("Failed to load strategic planning data:", err);
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
      const res = await fetch("/api/v1/strategy/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: queryInput })
      });
      if (res.ok) {
        const data = await res.json();
        setQueryResult(data);
      }
    } catch (err) {
      console.error("NL Strategy Query failed:", err);
    }
  };

  return (
    <div className="p-6 space-y-6 max-w-[1600px] mx-auto text-slate-100 font-sans">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/80 p-6 rounded-2xl border border-slate-800 shadow-xl backdrop-blur-md">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-amber-500/10 border border-amber-500/20 rounded-xl text-amber-400">
              <Compass className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-3">
                Strategic Planning &amp; Scenario Intelligence 2.0
                <span className="text-xs px-2.5 py-1 bg-amber-500/20 text-amber-300 font-mono font-medium rounded-full border border-amber-500/30">
                  Human-Governed Strategic Execution
                </span>
              </h1>
              <p className="text-xs text-slate-400 font-medium">
                AI-assisted scenario analysis, evidence-backed recommendations, trade-off matrices, and reversibility ratings
              </p>
            </div>
          </div>
        </div>

        <button
          onClick={fetchOverview}
          className="p-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-xs font-semibold flex items-center gap-2 transition border border-slate-700/50"
        >
          <RefreshCw className={`w-4 h-4 ${isLoading ? "animate-spin" : ""}`} />
          Refresh Strategy
        </button>
      </div>

      {/* Top Telemetry Header */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Strategic Objectives</span>
            <Target className="w-4 h-4 text-emerald-400" />
          </div>
          <p className="text-2xl font-bold text-emerald-400">{overview?.objectivesCount || 0}</p>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Active Initiatives</span>
            <Rocket className="w-4 h-4 text-cyan-400" />
          </div>
          <p className="text-2xl font-bold text-cyan-400">{overview?.initiativesCount || 0}</p>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Assumptions Monitored</span>
            <HelpCircle className="w-4 h-4 text-amber-400" />
          </div>
          <p className="text-2xl font-bold text-amber-400">{overview?.assumptionsCount || 0}</p>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Strategy Drift Signals</span>
            <Activity className="w-4 h-4 text-purple-400" />
          </div>
          <p className="text-2xl font-bold text-purple-400">{overview?.strategyDriftCount || 0}</p>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Strategy Health Score</span>
            <ShieldCheck className="w-4 h-4 text-indigo-400" />
          </div>
          <p className="text-2xl font-bold text-indigo-400">94.0%</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-2 overflow-x-auto">
        {[
          { id: "overview", label: "Strategy Overview", icon: Compass },
          { id: "objectives", label: "Objectives", icon: Target },
          { id: "initiatives", label: "Initiatives", icon: Rocket },
          { id: "assumptions", label: "Assumptions", icon: HelpCircle },
          { id: "recommendations", label: "Multi-Option Recommendations", icon: Lightbulb },
          { id: "reviews", label: "Reviews & Drift", icon: Activity },
          { id: "query", label: "Natural Language Strategy Query", icon: Search }
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`px-4 py-2 rounded-xl text-xs font-semibold flex items-center gap-2 whitespace-nowrap transition ${
                isActive
                  ? "bg-amber-500/10 text-amber-400 border border-amber-500/20 shadow-sm"
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
            <Compass className="w-4 h-4 text-amber-400" />
            Active Strategic Plan Summary
          </h2>

          <div className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
            <span className="font-bold text-amber-300">{overview?.plan?.name} (v{overview?.plan?.version})</span>
            <p className="text-slate-300 font-sans">{overview?.plan?.description}</p>
            <div className="flex gap-4 text-slate-400 font-mono text-xs">
              <span>Owner: {overview?.plan?.owner}</span>
              <span>Timeline: {overview?.plan?.start_date} to {overview?.plan?.end_date}</span>
              <span>Status: <strong className="text-emerald-400">{overview?.plan?.status}</strong></span>
            </div>
          </div>
        </div>
      )}

      {/* TAB CONTENT: Objectives */}
      {activeTab === "objectives" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Target className="w-4 h-4 text-emerald-400" />
            Strategic Objectives &amp; Progress
          </h2>

          <div className="space-y-3 font-mono text-xs">
            {overview?.objectives?.map((o: any) => (
              <div key={o.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-emerald-300">{o.name}</span>
                  <span className="text-[10px] bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded font-bold uppercase">{o.status}</span>
                </div>
                <p className="text-slate-300 font-sans">{o.description}</p>
                <p className="text-slate-400">Target: {o.target} | Current: {o.current_state}</p>
                <p className="text-slate-500">Deadline: {o.deadline} | Priority: {o.priority}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Initiatives */}
      {activeTab === "initiatives" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Rocket className="w-4 h-4 text-cyan-400" />
            Strategic Initiatives &amp; Resource Commitments
          </h2>

          <div className="space-y-3 font-mono text-xs">
            {overview?.initiatives?.map((i: any) => (
              <div key={i.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-cyan-300">{i.name}</span>
                  <span className="text-[10px] bg-cyan-500/20 text-cyan-300 px-2 py-0.5 rounded font-bold uppercase">{i.status}</span>
                </div>
                <p className="text-slate-300 font-sans">{i.description}</p>
                <p className="text-slate-400">Estimated Cost: ${i.estimated_cost?.toLocaleString()} | Duration: {i.estimated_duration}</p>
                <p className="text-slate-500">Owner: {i.owner} | Expected Outcome: {i.expected_outcome}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Assumptions */}
      {activeTab === "assumptions" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <HelpCircle className="w-4 h-4 text-amber-400" />
            Strategic Assumptions &amp; Evidence Tracking
          </h2>

          <div className="space-y-3 font-mono text-xs">
            {overview?.assumptions?.map((a: any) => (
              <div key={a.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-amber-300">Type: {a.assumption_type}</span>
                  <span className="text-[10px] bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded font-bold uppercase">{a.validity}</span>
                </div>
                <p className="text-slate-200 font-sans">{a.statement}</p>
                <p className="text-slate-400">Source: {a.source} | Confidence: {a.confidence}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Multi-Option Recommendations */}
      {activeTab === "recommendations" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Lightbulb className="w-4 h-4 text-amber-400" />
            Multi-Option Strategic Recommendations &amp; Reversibility Ratings
          </h2>

          <div className="space-y-4 font-mono text-xs">
            {overview?.recommendations?.map((r: any) => (
              <div key={r.id} className="p-5 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-3">
                <span className="font-bold text-amber-300 text-sm">{r.recommendation} ({r.confidence_pct}% confidence)</span>
                <p className="text-slate-400 font-sans">Evidence: {JSON.stringify(r.evidence_json)}</p>

                <h3 className="font-semibold text-slate-200 mt-2">Available Alternatives:</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                  {r.alternatives_json?.map((alt: any, idx: number) => (
                    <div key={idx} className="p-3 bg-slate-900/80 rounded-lg border border-slate-700 space-y-1">
                      <span className="font-bold text-cyan-300">{alt.option}</span>
                      <p className="text-slate-300 font-sans text-[11px]">{alt.description}</p>
                      <div className="flex justify-between items-center text-[10px] text-slate-400 pt-1">
                        <span>Cost: {alt.cost_estimate}</span>
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

      {/* TAB CONTENT: Reviews & Drift */}
      {activeTab === "reviews" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Activity className="w-4 h-4 text-purple-400" />
            Strategy Drift Signals &amp; Periodic Reviews
          </h2>

          <div className="space-y-3 font-mono text-xs">
            {overview?.drifts?.map((d: any) => (
              <div key={d.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-purple-300">Drift Type: {d.drift_type}</span>
                  <span className="text-[10px] bg-purple-500/20 text-purple-300 px-2 py-0.5 rounded font-bold uppercase">{d.status}</span>
                </div>
                <p className="text-slate-200 font-sans">{d.signal_summary}</p>
                <p className="text-slate-500">Evidence: {JSON.stringify(d.evidence_json)}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Natural Language Strategy Query */}
      {activeTab === "query" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Search className="w-4 h-4 text-amber-400" />
            Natural Language Strategy Queries
          </h2>

          <div className="space-y-3 font-mono text-xs">
            <div className="flex gap-2">
              <input
                type="text"
                value={queryInput}
                onChange={(e) => setQueryInput(e.target.value)}
                className="flex-1 bg-slate-800 border border-slate-700 text-slate-200 px-3 py-2 rounded-xl text-xs"
                placeholder="Ask a strategic question..."
              />
              <button
                onClick={handleQuery}
                className="px-4 py-2 bg-amber-600 hover:bg-amber-500 text-white rounded-xl text-xs font-semibold flex items-center gap-2"
              >
                <Search className="w-4 h-4" />
                Execute Query
              </button>
            </div>

            {queryResult && (
              <div className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <span className="font-bold text-amber-300">Query: {queryResult.query} ({queryResult.confidencePct}% confidence)</span>
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
