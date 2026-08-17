"use client";

import React, { useState, useEffect } from "react";
import {
  Activity,
  ShieldCheck,
  AlertTriangle,
  Zap,
  RefreshCw,
  Clock,
  Flame,
  Cpu,
  Layers,
  FileText,
  Sliders,
  Play,
  RotateCcw,
  CheckCircle,
  XCircle
} from "lucide-react";

export function ResilienceWorkspace() {
  const [activeTab, setActiveTab] = useState<
    "components" | "degradation" | "dr" | "chaos" | "slos" | "capacity"
  >("components");

  const [dashboard, setDashboard] = useState<any>(null);
  const [recoveryPlans, setRecoveryPlans] = useState<any[]>([]);
  const [experiments, setExperiments] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchData = async () => {
    setIsLoading(true);
    try {
      const [dashRes, rpRes, expRes] = await Promise.all([
        fetch("/api/v1/resilience").then((r) => (r.ok ? r.json() : null)),
        fetch("/api/v1/resilience/recovery-plans").then((r) => (r.ok ? r.json() : [])),
        fetch("/api/v1/resilience/experiments").then((r) => (r.ok ? r.json() : []))
      ]);

      setDashboard(dashRes);
      setRecoveryPlans(rpRes);
      setExperiments(expRes);
    } catch (err) {
      console.error("Failed to load Resilience data:", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleStartExperiment = async (expId: string) => {
    try {
      const res = await fetch(`/api/v1/resilience/experiments/${expId}/start`, { method: "POST" });
      if (res.ok) fetchData();
    } catch (err) {
      console.error("Start experiment failed:", err);
    }
  };

  const handleAbortExperiment = async (expId: string) => {
    try {
      const res = await fetch(`/api/v1/resilience/experiments/${expId}/abort`, { method: "POST" });
      if (res.ok) fetchData();
    } catch (err) {
      console.error("Abort experiment failed:", err);
    }
  };

  return (
    <div className="p-6 space-y-6 max-w-[1600px] mx-auto text-slate-100 font-sans">
      {/* Workspace Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/80 p-6 rounded-2xl border border-slate-800 shadow-xl backdrop-blur-md">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-emerald-400">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-3">
                Resilience &amp; Business Continuity Fabric
                <span className="text-xs px-2.5 py-1 bg-emerald-500/20 text-emerald-300 font-mono font-medium rounded-full border border-emerald-500/30">
                  Resilient AI Execution
                </span>
              </h1>
              <p className="text-xs text-slate-400 font-medium">
                Unified resilience layer preserving state, security controls, and tenant isolation during component degradation
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
            <span>Overall Status</span>
            <Activity className="w-4 h-4 text-emerald-400" />
          </div>
          <p className={`text-2xl font-bold uppercase ${dashboard?.overallStatus === "healthy" ? "text-emerald-400" : "text-amber-400"}`}>
            {dashboard?.overallStatus || "healthy"}
          </p>
          <span className="text-[10px] text-slate-500">Component Health Stream</span>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Circuit Breakers</span>
            <Zap className="w-4 h-4 text-purple-400" />
          </div>
          <p className="text-2xl font-bold text-purple-400">{dashboard?.openCircuitBreakersCount || 0}</p>
          <span className="text-[10px] text-slate-500">Open / Half-Open</span>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Degraded Modes</span>
            <AlertTriangle className="w-4 h-4 text-amber-400" />
          </div>
          <p className="text-2xl font-bold text-amber-400">{dashboard?.activeDegradationModesCount || 0}</p>
          <span className="text-[10px] text-slate-500">Policy-Controlled</span>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Chaos Experiments</span>
            <Flame className="w-4 h-4 text-rose-400" />
          </div>
          <p className="text-2xl font-bold text-rose-400">{dashboard?.activeExperimentsCount || 0}</p>
          <span className="text-[10px] text-slate-500">Active Chaos Runs</span>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800 col-span-2 md:col-span-1">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>SLO Compliance</span>
            <Clock className="w-4 h-4 text-cyan-400" />
          </div>
          <p className="text-2xl font-bold text-cyan-400">
            {dashboard?.sloCompliance != null ? `${dashboard.sloCompliance}%` : 'Not Connected'}
          </p>
          <span className="text-[10px] text-slate-500">Live Telemetry Ingestion</span>
        </div>
      </div>

      {/* Subsystem Navigation Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-2 overflow-x-auto">
        {[
          { id: "components", label: "Component Health", icon: Activity },
          { id: "degradation", label: "Failures & Degradation", icon: AlertTriangle },
          { id: "dr", label: "Disaster Recovery Plans", icon: FileText },
          { id: "chaos", label: "Chaos Experiments", icon: Flame },
          { id: "slos", label: "SLOs & Error Budgets", icon: Clock },
          { id: "capacity", label: "Capacity & Load Shedding", icon: Cpu }
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

      {/* TAB CONTENT: Component Health */}
      {activeTab === "components" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Activity className="w-4 h-4 text-emerald-400" />
            Live Component Health Matrix
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {dashboard?.components?.map((c: any) => (
              <div key={c.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-white font-mono">{c.component_id}</span>
                  <span className={`text-[10px] px-2 py-0.5 rounded font-mono uppercase font-bold ${c.status === "healthy" ? "bg-emerald-500/20 text-emerald-300" : "bg-amber-500/20 text-amber-300"}`}>
                    {c.status}
                  </span>
                </div>
                <div className="text-[11px] text-slate-400 space-y-1 font-mono">
                  <p>Type: {c.component_type} | Latency: {c.latency_ms}ms</p>
                  <p>Availability: {c.availability_pct}% | Error Rate: {c.error_rate * 100}%</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Failures & Degradation */}
      {activeTab === "degradation" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-amber-400" />
            Active Degraded Modes &amp; Circuit Breakers
          </h2>

          <div className="space-y-3 font-mono text-xs">
            {dashboard?.degradations?.map((d: any) => (
              <div key={d.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-1">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-amber-300">Mode: {d.mode} ({d.scope})</span>
                  <span className="text-[10px] bg-amber-500/20 text-amber-300 px-2 py-0.5 rounded uppercase">{d.status}</span>
                </div>
                <p className="text-slate-300">{d.reason}</p>
                <p className="text-[10px] text-slate-500">Expires At: {d.expires_at || "N/A"}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Disaster Recovery Plans */}
      {activeTab === "dr" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <FileText className="w-4 h-4 text-cyan-400" />
            Auditable Disaster Recovery (DR) Plans
          </h2>

          <div className="space-y-3 font-mono text-xs">
            {recoveryPlans.map((rp) => (
              <div key={rp.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-cyan-300">{rp.name}</span>
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] bg-cyan-500/20 text-cyan-300 px-2 py-0.5 rounded">RTO: {rp.rtoSeconds}s</span>
                    <span className="text-[10px] bg-cyan-500/20 text-cyan-300 px-2 py-0.5 rounded">RPO: {rp.rpoSeconds}s</span>
                  </div>
                </div>
                <div className="text-slate-300 space-y-1">
                  <p className="text-slate-400 font-bold">Recovery Sequence:</p>
                  {rp.recoveryOrderJson?.map((seq: string, idx: number) => (
                    <p key={idx} className="pl-2 text-slate-300">• {seq}</p>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Chaos Experiments */}
      {activeTab === "chaos" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Flame className="w-4 h-4 text-rose-400" />
            Chaos Engineering Experiments &amp; Abort Triggers
          </h2>

          <div className="space-y-3 font-mono text-xs">
            {experiments.map((e) => (
              <div key={e.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-rose-300">{e.name} ({e.experimentType})</span>
                  <span className={`text-[10px] px-2 py-0.5 rounded uppercase font-bold ${e.status === "running" ? "bg-rose-500/20 text-rose-300 animate-pulse" : "bg-slate-700 text-slate-300"}`}>
                    {e.status}
                  </span>
                </div>
                <p className="text-slate-400">Target Scope: {e.targetScope}</p>
                <div className="flex items-center gap-2">
                  {e.status === "draft" && (
                    <button
                      onClick={() => handleStartExperiment(e.id)}
                      className="px-3.5 py-1.5 bg-rose-600 hover:bg-rose-500 text-white rounded-lg text-xs font-semibold transition"
                    >
                      Start Chaos Run
                    </button>
                  )}
                  {e.status === "running" && (
                    <button
                      onClick={() => handleAbortExperiment(e.id)}
                      className="px-3.5 py-1.5 bg-amber-600 hover:bg-amber-500 text-white rounded-lg text-xs font-semibold transition"
                    >
                      Abort Experiment
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: SLOs & Error Budgets */}
      {activeTab === "slos" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Clock className="w-4 h-4 text-emerald-400" />
            SLO Benchmarks &amp; Reliability Budgets
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 font-mono text-xs">
            <div className="p-4 bg-slate-800/50 rounded-xl border border-slate-700/40 space-y-2">
              <span className="text-slate-400 font-bold">Mission Execution SLO</span>
              <p className="text-2xl font-bold text-emerald-400">
                {dashboard?.missionSlo != null ? `${dashboard.missionSlo}%` : 'Not Connected'}
              </p>
              <p className="text-slate-500">Target: 99.9% | Real Telemetry Ingestion</p>
            </div>
            <div className="p-4 bg-slate-800/50 rounded-xl border border-slate-700/40 space-y-2">
              <span className="text-slate-400 font-bold">Reliability Error Budget</span>
              <p className="text-2xl font-bold text-cyan-400">
                {dashboard?.errorBudget != null ? `${dashboard.errorBudget}% Remaining` : 'Not Connected'}
              </p>
              <p className="text-slate-500">Allowed Error: 0.1% | Active Burn Monitoring</p>
            </div>
          </div>
        </div>
      )}

      {/* TAB CONTENT: Capacity & Load Shedding */}
      {activeTab === "capacity" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Cpu className="w-4 h-4 text-purple-400" />
            Infrastructure Capacity &amp; Load Shedding
          </h2>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 font-mono text-xs">
            <div className="p-4 bg-slate-800/50 rounded-xl border border-slate-700/40">
              <span className="text-slate-400">CPU Usage</span>
              <p className="text-xl font-bold text-purple-300">
                {dashboard?.cpuUsage != null ? `${dashboard.cpuUsage}%` : 'Not Connected'}
              </p>
            </div>
            <div className="p-4 bg-slate-800/50 rounded-xl border border-slate-700/40">
              <span className="text-slate-400">Memory Usage</span>
              <p className="text-xl font-bold text-purple-300">
                {dashboard?.memoryUsage != null ? `${dashboard.memoryUsage}%` : 'Not Connected'}
              </p>
            </div>
            <div className="p-4 bg-slate-800/50 rounded-xl border border-slate-700/40">
              <span className="text-slate-400">Queue Depth</span>
              <p className="text-xl font-bold text-purple-300">
                {dashboard?.queueDepth != null ? `${dashboard.queueDepth} msgs` : '0 msgs'}
              </p>
            </div>
            <div className="p-4 bg-slate-800/50 rounded-xl border border-slate-700/40">
              <span className="text-slate-400">Load Shedding</span>
              <p className="text-xl font-bold text-emerald-400">
                {dashboard?.loadSheddingActive ? 'ACTIVE' : 'INACTIVE'}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
