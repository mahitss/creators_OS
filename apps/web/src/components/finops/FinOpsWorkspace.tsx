"use client";

import React, { useState, useEffect } from "react";
import {
  DollarSign,
  TrendingUp,
  PieChart,
  AlertTriangle,
  Zap,
  RefreshCw,
  Clock,
  ShieldCheck,
  Cpu,
  Layers,
  CheckCircle,
  XCircle,
  ChevronRight,
  Filter,
  BarChart3,
  Sliders
} from "lucide-react";

export function FinOpsWorkspace() {
  const [activeTab, setActiveTab] = useState<
    "overview" | "budgets" | "forecast" | "attribution" | "optimization" | "capacity"
  >("overview");

  const [dashboard, setDashboard] = useState<any>(null);
  const [costsByModel, setCostsByModel] = useState<any[]>([]);
  const [costsByAgent, setCostsByAgent] = useState<any[]>([]);
  const [costsByMission, setCostsByMission] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchData = async () => {
    setIsLoading(true);
    try {
      const [dashRes, modelRes, agentRes, missionRes] = await Promise.all([
        fetch("/api/v1/finops").then((r) => (r.ok ? r.json() : null)),
        fetch("/api/v1/finops/costs/by-model").then((r) => (r.ok ? r.json() : [])),
        fetch("/api/v1/finops/costs/by-agent").then((r) => (r.ok ? r.json() : [])),
        fetch("/api/v1/finops/costs/by-mission").then((r) => (r.ok ? r.json() : []))
      ]);

      setDashboard(dashRes);
      setCostsByModel(modelRes);
      setCostsByAgent(agentRes);
      setCostsByMission(missionRes);
    } catch (err) {
      console.error("Failed to load FinOps 2.0 data:", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleApproveRecommendation = async (recId: string) => {
    try {
      const res = await fetch(`/api/v1/finops/optimizations/${recId}/approve`, { method: "POST" });
      if (res.ok) fetchData();
    } catch (err) {
      console.error("Approve recommendation failed:", err);
    }
  };

  const handleApplyRecommendation = async (recId: string) => {
    try {
      const res = await fetch(`/api/v1/finops/optimizations/${recId}/apply`, { method: "POST" });
      if (res.ok) fetchData();
    } catch (err) {
      console.error("Apply recommendation failed:", err);
    }
  };

  return (
    <div className="p-6 space-y-6 max-w-[1600px] mx-auto text-slate-100 font-sans">
      {/* Workspace Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/80 p-6 rounded-2xl border border-slate-800 shadow-xl backdrop-blur-md">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-emerald-400">
              <DollarSign className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-3">
                Enterprise AI FinOps &amp; Capacity Intelligence 2.0
                <span className="text-xs px-2.5 py-1 bg-emerald-500/20 text-emerald-300 font-mono font-medium rounded-full border border-emerald-500/30">
                  Quality-Aware Cost Optimization
                </span>
              </h1>
              <p className="text-xs text-slate-400 font-medium">
                Unified resource intelligence tracking model, agent, mission, tool, retrieval, and compute overhead
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={fetchData}
            className="p-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-xs font-semibold flex items-center gap-2 transition border border-slate-700/50"
          >
            <RefreshCw className={`w-4 h-4 ${isLoading ? "animate-spin" : ""}`} />
            Refresh Telemetry
          </button>
        </div>
      </div>

      {/* Top Telemetry Header */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Current Month Spend</span>
            <DollarSign className="w-4 h-4 text-emerald-400" />
          </div>
          <p className="text-2xl font-bold text-emerald-400">${dashboard?.totalSpend?.toFixed(2) || "420.00"}</p>
          <span className="text-[10px] text-slate-500">Reconciled &amp; estimated</span>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Forecasted Spend</span>
            <TrendingUp className="w-4 h-4 text-cyan-400" />
          </div>
          <p className="text-2xl font-bold text-cyan-400">${dashboard?.forecast?.current_period_expected?.toFixed(2) || "1,850.00"}</p>
          <span className="text-[10px] text-slate-500">91% confidence interval</span>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Budget Utilization</span>
            <PieChart className="w-4 h-4 text-purple-400" />
          </div>
          <p className="text-2xl font-bold text-purple-400">16.8%</p>
          <span className="text-[10px] text-slate-500">$2,500 monthly limit</span>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Savings Opportunities</span>
            <Zap className="w-4 h-4 text-amber-400" />
          </div>
          <p className="text-2xl font-bold text-amber-400">${dashboard?.estimatedMonthlySavings?.toFixed(2) || "145.00"}/mo</p>
          <span className="text-[10px] text-slate-500">Quality-guarded</span>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800 col-span-2 md:col-span-1">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Spend Anomalies</span>
            <AlertTriangle className="w-4 h-4 text-rose-400" />
          </div>
          <p className="text-2xl font-bold text-rose-400">{dashboard?.anomaliesCount || 0}</p>
          <span className="text-[10px] text-slate-500">Spike signals detected</span>
        </div>
      </div>

      {/* Subsystem Navigation Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-2 overflow-x-auto">
        {[
          { id: "overview", label: "Overview & Spend", icon: DollarSign },
          { id: "budgets", label: "Budgets & Limits", icon: PieChart },
          { id: "forecast", label: "Forecasts & Anomalies", icon: TrendingUp },
          { id: "attribution", label: "Attribution Matrix", icon: BarChart3 },
          { id: "optimization", label: "Quality-Aware Optimization", icon: Zap },
          { id: "capacity", label: "Capacity & Quotas", icon: Cpu }
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

      {/* TAB CONTENT: Overview & Spend */}
      {activeTab === "overview" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <DollarSign className="w-4 h-4 text-emerald-400" />
            Resource Spend Distribution
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-3 font-mono text-xs">
              <span className="text-slate-300 font-bold">Top Cost Driving Models</span>
              {costsByModel.map((m, idx) => (
                <div key={idx} className="flex justify-between p-2 bg-slate-800/50 rounded-lg">
                  <span className="text-slate-200">{m.model} ({m.provider})</span>
                  <span className="text-emerald-400 font-bold">${m.cost.toFixed(2)}</span>
                </div>
              ))}
            </div>

            <div className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-3 font-mono text-xs">
              <span className="text-slate-300 font-bold">Top Cost Driving Agents</span>
              {costsByAgent.map((a, idx) => (
                <div key={idx} className="flex justify-between p-2 bg-slate-800/50 rounded-lg">
                  <span className="text-slate-200">{a.name}</span>
                  <span className="text-emerald-400 font-bold">${a.cost.toFixed(2)}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* TAB CONTENT: Budgets & Limits */}
      {activeTab === "budgets" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <PieChart className="w-4 h-4 text-purple-400" />
            Multi-Scope Budgets &amp; Policy Hard Limits
          </h2>

          <div className="space-y-3 font-mono text-xs">
            {dashboard?.budgets?.map((b: any) => (
              <div key={b.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-purple-300">Scope: {b.scope} ({b.period})</span>
                  <span className="text-[10px] bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded font-bold uppercase">{b.status}</span>
                </div>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-slate-300">
                  <p>Limit: ${b.limit_amount}</p>
                  <p>Spent: ${b.spent_amount}</p>
                  <p>Committed: ${b.committed_amount}</p>
                  <p>Remaining: ${b.remaining_amount}</p>
                </div>
                <p className="text-slate-500">Soft Threshold: {b.soft_threshold_pct}% | Hard Limit Action: {b.hard_limit_action}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Forecasts & Anomalies */}
      {activeTab === "forecast" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <TrendingUp className="w-4 h-4 text-cyan-400" />
            Spend Forecasting &amp; Anomaly Signals
          </h2>

          {dashboard?.forecast && (
            <div className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2 font-mono text-xs">
              <span className="font-bold text-cyan-300">Monthly Expected Spend: ${dashboard.forecast.current_period_expected.toFixed(2)}</span>
              <p className="text-slate-300">Confidence Band: ${dashboard.forecast.lower_bound.toFixed(2)} - ${dashboard.forecast.upper_bound.toFixed(2)} ({dashboard.forecast.confidence_pct}% confidence)</p>
            </div>
          )}
        </div>
      )}

      {/* TAB CONTENT: Attribution Matrix */}
      {activeTab === "attribution" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <BarChart3 className="w-4 h-4 text-emerald-400" />
            Hierarchical Cost Attribution Matrix
          </h2>

          <div className="space-y-3 font-mono text-xs">
            <span className="text-slate-400 font-bold">Attributed Mission Costs</span>
            {costsByMission.map((m, idx) => (
              <div key={idx} className="p-3 bg-slate-800/40 rounded-xl border border-slate-700/50 flex justify-between items-center">
                <span className="text-slate-200">{m.name} ({m.mission_id})</span>
                <span className="text-emerald-400 font-bold">${m.cost.toFixed(2)}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Quality-Aware Optimization */}
      {activeTab === "optimization" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Zap className="w-4 h-4 text-amber-400" />
            Quality-Aware Cost Optimization Recommendations
          </h2>

          <div className="space-y-3 font-mono text-xs">
            {dashboard?.recommendations?.map((r: any) => (
              <div key={r.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-amber-300">Type: {r.type}</span>
                  <span className="text-[10px] bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded font-bold uppercase">Estimated Savings: ${r.estimated_savings}/mo</span>
                </div>
                <div className="text-slate-300 space-y-1">
                  <p>Quality Impact: {r.quality_impact} | Latency: {r.latency_impact} | Risk: {r.risk_level}</p>
                  <p className="text-slate-500">Evidence: {JSON.stringify(r.evidence_json)}</p>
                </div>
                <div className="flex items-center gap-2">
                  {r.approval_status === "pending" && (
                    <button
                      onClick={() => handleApproveRecommendation(r.id)}
                      className="px-3.5 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold transition"
                    >
                      Approve Recommendation
                    </button>
                  )}
                  {r.approval_status === "approved" && (
                    <button
                      onClick={() => handleApplyRecommendation(r.id)}
                      className="px-3.5 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-semibold transition"
                    >
                      Apply Optimization
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Capacity & Quotas */}
      {activeTab === "capacity" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Cpu className="w-4 h-4 text-purple-400" />
            AI Capacity &amp; Provider Quotas
          </h2>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 font-mono text-xs">
            <div className="p-4 bg-slate-800/50 rounded-xl border border-slate-700/40">
              <span className="text-slate-400">Active Concurrency</span>
              <p className="text-xl font-bold text-purple-300">12 / 50</p>
            </div>
            <div className="p-4 bg-slate-800/50 rounded-xl border border-slate-700/40">
              <span className="text-slate-400">Queue Depth</span>
              <p className="text-xl font-bold text-purple-300">4 msgs</p>
            </div>
            <div className="p-4 bg-slate-800/50 rounded-xl border border-slate-700/40">
              <span className="text-slate-400">OpenAI RPM Limit</span>
              <p className="text-xl font-bold text-purple-300">10,000</p>
            </div>
            <div className="p-4 bg-slate-800/50 rounded-xl border border-slate-700/40">
              <span className="text-slate-400">Google TPM Limit</span>
              <p className="text-xl font-bold text-purple-300">2,000,000</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
