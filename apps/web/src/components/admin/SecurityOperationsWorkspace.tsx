"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import {
  ShieldAlert,
  AlertTriangle,
  FileText,
  Activity,
  CheckCircle,
  Clock,
  Play,
  Check,
  RotateCcw,
  Zap,
  Plus,
  RefreshCw,
  Search,
  Eye,
  Sliders,
  Award,
  Layers,
  ChevronRight
} from "lucide-react";

export function SecurityOperationsWorkspace() {
  const [activeTab, setActiveTab] = useState<
    "incidents" | "response" | "detections" | "runbooks" | "automations" | "sla"
  >("incidents");

  const [dashboard, setDashboard] = useState<any>(null);
  const [detections, setDetections] = useState<any[]>([]);
  const [runbooks, setRunbooks] = useState<any[]>([]);
  const [automations, setAutomations] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchData = async () => {
    setIsLoading(true);
    try {
      const [dashRes, detRes, rbRes, autoRes] = await Promise.all([
        fetch("/api/v1/security/operations").then((r) => (r.ok ? r.json() : null)),
        fetch("/api/v1/security/detections").then((r) => (r.ok ? r.json() : [])),
        fetch("/api/v1/security/runbooks").then((r) => (r.ok ? r.json() : [])),
        fetch("/api/v1/security/automations").then((r) => (r.ok ? r.json() : []))
      ]);

      setDashboard(dashRes);
      setDetections(detRes);
      setRunbooks(rbRes);
      setAutomations(autoRes);
    } catch (err) {
      console.error("Failed to load SecOps data:", err);
    } fontally: {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="p-6 space-y-6 max-w-[1600px] mx-auto text-slate-100 font-sans">
      {/* Workspace Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/80 p-6 rounded-2xl border border-slate-800 shadow-xl backdrop-blur-md">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-rose-500/10 border border-rose-500/20 rounded-xl text-rose-400">
              <ShieldAlert className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-3">
                Security Operations Center (SecOps)
                <span className="text-xs px-2.5 py-1 bg-amber-500/20 text-amber-300 font-mono font-medium rounded-full border border-amber-500/30">
                  Controlled AI Response
                </span>
              </h1>
              <p className="text-xs text-slate-400 font-medium">
                Converts security signals into governed, auditable response workflows with human oversight &amp; PolicyEngine checks
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
            Refresh SecOps
          </button>
        </div>
      </div>

      {/* Top Telemetry Header */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Active Incidents</span>
            <AlertTriangle className="w-4 h-4 text-rose-400" />
          </div>
          <p className="text-2xl font-bold text-rose-400">{dashboard?.activeIncidentsCount || 0}</p>
          <span className="text-[10px] text-slate-500">Require triage &amp; response</span>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Critical Threats</span>
            <ShieldAlert className="w-4 h-4 text-amber-400" />
          </div>
          <p className="text-2xl font-bold text-amber-400">{dashboard?.criticalThreatsCount || 0}</p>
          <span className="text-[10px] text-slate-500">Unresolved threat findings</span>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Response Plans</span>
            <Zap className="w-4 h-4 text-purple-400" />
          </div>
          <p className="text-2xl font-bold text-purple-400">{dashboard?.activeResponsePlansCount || 0}</p>
          <span className="text-[10px] text-slate-500">Executing / Approved</span>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>SLA Breaches</span>
            <Clock className="w-4 h-4 text-cyan-400" />
          </div>
          <p className="text-2xl font-bold text-cyan-400">{dashboard?.breachedSLACount || 0}</p>
          <span className="text-[10px] text-slate-500">TTD / TTC thresholds</span>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800 col-span-2 md:col-span-1">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Detection Rules</span>
            <Activity className="w-4 h-4 text-emerald-400" />
          </div>
          <p className="text-2xl font-bold text-emerald-400">{dashboard?.activeDetectionRulesCount || 0}</p>
          <span className="text-[10px] text-slate-500">Shadow &amp; active rules</span>
        </div>
      </div>

      {/* Subsystem Navigation Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-2 overflow-x-auto">
        {[
          { id: "incidents", label: "Incident Queue", icon: AlertTriangle },
          { id: "response", label: "Response Plans", icon: Zap },
          { id: "detections", label: "Detection Rules & Shadow", icon: Activity },
          { id: "runbooks", label: "Security Runbooks", icon: FileText },
          { id: "automations", label: "Automations & Cooldown", icon: Sliders },
          { id: "sla", label: "SLA Metrics", icon: Clock }
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

      {/* TAB CONTENT: Incident Queue */}
      {activeTab === "incidents" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-amber-400" />
            Active Incident Prioritization Queue
          </h2>

          <div className="space-y-3">
            {dashboard?.incidents?.map((inc: any) => (
              <div key={inc.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-white">{inc.id}</span>
                    <span className="text-[10px] bg-rose-500/20 text-rose-300 px-2 py-0.5 rounded font-mono uppercase">{inc.severity}</span>
                    <span className="text-[10px] bg-amber-500/20 text-amber-300 px-2 py-0.5 rounded font-mono uppercase">{inc.status}</span>
                  </div>
                  <p className="text-xs text-slate-300">{inc.summary}</p>
                </div>

                <Link
                  href={`/security/incidents/${inc.id}`}
                  className="px-3.5 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold transition flex items-center gap-1"
                >
                  Manage Incident &amp; Response <ChevronRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Response Plans */}
      {activeTab === "response" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Zap className="w-4 h-4 text-purple-400" />
            Security Response Plans
          </h2>

          <div className="space-y-3">
            {dashboard?.responsePlans?.map((p: any) => (
              <div key={p.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 font-mono text-xs">
                    <span className="font-bold text-purple-300">Plan: {p.id}</span>
                    <span className="text-slate-400">(Incident: {p.incident_id})</span>
                    <span className="bg-purple-500/20 text-purple-300 px-2 py-0.5 rounded text-[10px] font-bold">v{p.version}</span>
                  </div>
                  <span className="text-[10px] bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded font-mono uppercase">{p.status}</span>
                </div>
                <p className="text-xs text-slate-400 font-mono">Approval Requirements: {p.approval_requirements?.join(", ")}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Detection Rules & Shadow Mode */}
      {activeTab === "detections" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Activity className="w-4 h-4 text-emerald-400" />
            Threat Detection Rules &amp; Shadow Mode Lifecycle
          </h2>

          <div className="space-y-3">
            {detections.map((dr) => (
              <div key={dr.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-white">{dr.name}</span>
                    <span className="text-[10px] bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded font-mono uppercase">{dr.status}</span>
                    <span className="text-[10px] bg-rose-500/20 text-rose-300 px-2 py-0.5 rounded font-mono uppercase">{dr.severity}</span>
                  </div>
                  <p className="text-xs text-slate-300">{dr.description}</p>
                  <p className="text-[11px] text-slate-500 font-mono">Conditions: {JSON.stringify(dr.conditionsJson)}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Security Runbooks */}
      {activeTab === "runbooks" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <FileText className="w-4 h-4 text-cyan-400" />
            Standardized Incident Response Runbooks
          </h2>

          <div className="space-y-3">
            {runbooks.map((rb) => (
              <div key={rb.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-cyan-300">{rb.name}</span>
                  <span className="text-[10px] bg-cyan-500/20 text-cyan-300 px-2 py-0.5 rounded font-mono">Trigger: {rb.triggerCondition}</span>
                </div>
                <div className="text-xs text-slate-300 space-y-1 font-mono">
                  <p className="text-slate-400 font-bold">Investigation Steps:</p>
                  {rb.investigationStepsJson?.map((step: string, idx: number) => (
                    <p key={idx} className="text-slate-300 pl-2">• {step}</p>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Automations */}
      {activeTab === "automations" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Sliders className="w-4 h-4 text-amber-400" />
            Security Response Automation &amp; Cooldown Guardrails
          </h2>

          <div className="space-y-3">
            {automations.map((ar) => (
              <div key={ar.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-1 font-mono text-xs">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-amber-300">{ar.name}</span>
                  <span className="text-[10px] bg-amber-500/20 text-amber-300 px-2 py-0.5 rounded">Action: {ar.responseActionType}</span>
                </div>
                <p className="text-slate-400">Trigger: {ar.triggerEventType} | Scope: {ar.scope}</p>
                <p className="text-slate-500">Max Actions: {ar.maxActions} | Cooldown: {ar.cooldownSeconds}s | Approval Required: {String(ar.approvalRequired)}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: SLA Metrics */}
      {activeTab === "sla" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Clock className="w-4 h-4 text-emerald-400" />
            SecOps SLA Performance Metrics
          </h2>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs font-mono">
            <div className="p-4 bg-slate-800/50 rounded-xl border border-slate-700/40">
              <span className="text-slate-400">Avg Time to Detect (TTD)</span>
              <p className="text-xl font-bold text-emerald-400">30.0s</p>
            </div>
            <div className="p-4 bg-slate-800/50 rounded-xl border border-slate-700/40">
              <span className="text-slate-400">Avg Time to Triage (TTT)</span>
              <p className="text-xl font-bold text-emerald-400">90.0s</p>
            </div>
            <div className="p-4 bg-slate-800/50 rounded-xl border border-slate-700/40">
              <span className="text-slate-400">Avg Time to Contain (TTC)</span>
              <p className="text-xl font-bold text-emerald-400">240.0s</p>
            </div>
            <div className="p-4 bg-slate-800/50 rounded-xl border border-slate-700/40">
              <span className="text-slate-400">Avg Time to Recover (TTR)</span>
              <p className="text-xl font-bold text-emerald-400">1200.0s</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
