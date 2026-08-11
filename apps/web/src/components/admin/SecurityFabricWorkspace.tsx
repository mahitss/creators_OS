"use client";

import React, { useState, useEffect } from "react";
import {
  Shield,
  ShieldAlert,
  AlertTriangle,
  Lock,
  Unlock,
  Activity,
  Search,
  Eye,
  FileText,
  Terminal,
  Cpu,
  Zap,
  RefreshCw,
  CheckCircle,
  XCircle,
  Plus,
  Network,
  Database
} from "lucide-react";

export function SecurityFabricWorkspace() {
  const [activeTab, setActiveTab] = useState<
    "overview" | "threats" | "incidents" | "investigations" | "quarantine" | "behavior" | "intelligence" | "supply_chain" | "audit"
  >("overview");

  const [events, setEvents] = useState<any[]>([]);
  const [threats, setThreats] = useState<any[]>([]);
  const [incidents, setIncidents] = useState<any[]>([]);
  const [quarantines, setQuarantines] = useState<any[]>([]);
  const [intelSignals, setIntelSignals] = useState<any[]>([]);
  const [baseline, setBaseline] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Quarantine Modal State
  const [showQuarantineModal, setShowQuarantineModal] = useState(false);
  const [qTargetType, setQTargetType] = useState("agent");
  const [qTargetId, setQTargetId] = useState("");
  const [qReason, setQReason] = useState("");

  const fetchData = async () => {
    setIsLoading(true);
    try {
      const [evtsRes, thrRes, incRes, quarRes, intelRes, baseRes] = await Promise.all([
        fetch("/api/v1/security/events").then((r) => (r.ok ? r.json() : [])),
        fetch("/api/v1/security/threats").then((r) => (r.ok ? r.json() : [])),
        fetch("/api/v1/security/incidents").then((r) => (r.ok ? r.json() : [])),
        fetch("/api/v1/security/quarantine?status=all").then((r) => (r.ok ? r.json() : [])),
        fetch("/api/v1/security/intelligence").then((r) => (r.ok ? r.json() : [])),
        fetch("/api/v1/security/agents/agent_analyst_01/baseline").then((r) => (r.ok ? r.json() : null))
      ]);

      setEvents(evtsRes);
      setThreats(thrRes);
      setIncidents(incRes);
      setQuarantines(quarRes);
      setIntelSignals(intelRes);
      setBaseline(baseRes);
    } catch (err) {
      console.error("Failed to load Security Fabric data:", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleQuarantineSubmit = async () => {
    if (!qTargetId || !qReason) return;
    try {
      const res = await fetch("/api/v1/security/quarantine", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          targetType: qTargetType,
          targetId: qTargetId,
          reason: qReason,
          scope: "full_isolation",
          createdBy: "sec_admin_ui"
        })
      });
      if (res.ok) {
        setShowQuarantineModal(false);
        setQTargetId("");
        setQReason("");
        fetchData();
      }
    } catch (err) {
      console.error("Quarantine failed:", err);
    }
  };

  const handleReleaseQuarantine = async (id: string) => {
    try {
      const res = await fetch(`/api/v1/security/quarantine/${id}/release?release_by=sec_admin_ui`, {
        method: "POST"
      });
      if (res.ok) {
        fetchData();
      }
    } catch (err) {
      console.error("Release quarantine failed:", err);
    }
  };

  const handleContainIncident = async (id: string) => {
    try {
      const res = await fetch(`/api/v1/security/incidents/${id}/contain`, { method: "POST" });
      if (res.ok) fetchData();
    } catch (err) {
      console.error("Contain incident failed:", err);
    }
  };

  return (
    <div className="p-6 space-y-6 max-w-[1600px] mx-auto text-slate-100 font-sans">
      {/* Workspace Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/80 p-6 rounded-2xl border border-slate-800 shadow-xl backdrop-blur-md">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-rose-500/10 border border-rose-500/20 rounded-xl text-rose-400">
              <Shield className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-3">
                Security &amp; Threat Intelligence Fabric
                <span className="text-xs px-2.5 py-1 bg-rose-500/20 text-rose-300 font-mono font-medium rounded-full border border-rose-500/30">
                  Zero-Trust Defense
                </span>
              </h1>
              <p className="text-xs text-slate-400 font-medium">
                Defense-in-depth agent security, continuous threat detection, DLP boundary control &amp; quarantine engine
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
          <button
            onClick={() => setShowQuarantineModal(true)}
            className="px-4 py-2.5 bg-rose-600 hover:bg-rose-500 text-white rounded-xl text-xs font-semibold shadow-lg shadow-rose-600/20 flex items-center gap-2 transition"
          >
            <Lock className="w-4 h-4" />
            Quarantine Resource
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
          <p className="text-2xl font-bold text-rose-400">{incidents.filter((i) => i.status !== "closed").length}</p>
          <span className="text-[10px] text-slate-500">Correlated attack chains</span>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Critical Threats</span>
            <ShieldAlert className="w-4 h-4 text-amber-400" />
          </div>
          <p className="text-2xl font-bold text-amber-400">{threats.filter((t) => t.severity === "high" || t.severity === "critical").length}</p>
          <span className="text-[10px] text-slate-500">Injection &amp; tool abuse</span>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Quarantined Resources</span>
            <Lock className="w-4 h-4 text-purple-400" />
          </div>
          <p className="text-2xl font-bold text-purple-400">{quarantines.filter((q) => q.status === "active").length}</p>
          <span className="text-[10px] text-slate-500">Full isolation active</span>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Behavior Anomalies</span>
            <Activity className="w-4 h-4 text-cyan-400" />
          </div>
          <p className="text-2xl font-bold text-cyan-400">1</p>
          <span className="text-[10px] text-slate-500">Baseline deviations</span>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800 col-span-2 md:col-span-1">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Threat Intel Indicators</span>
            <Network className="w-4 h-4 text-emerald-400" />
          </div>
          <p className="text-2xl font-bold text-emerald-400">{intelSignals.length}</p>
          <span className="text-[10px] text-slate-500">Active feed signatures</span>
        </div>
      </div>

      {/* Subsystem Navigation Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-2 overflow-x-auto">
        {[
          { id: "overview", label: "Overview", icon: Shield },
          { id: "threats", label: "Threat Findings", icon: ShieldAlert },
          { id: "incidents", label: "Incidents", icon: AlertTriangle },
          { id: "investigations", label: "Attack Chains", icon: Network },
          { id: "quarantine", label: "Quarantine Control", icon: Lock },
          { id: "behavior", label: "Agent Baselines", icon: Activity },
          { id: "intelligence", label: "Threat Intelligence", icon: Database },
          { id: "supply_chain", label: "Supply Chain", icon: Cpu },
          { id: "audit", label: "Security Audit", icon: FileText }
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`px-4 py-2 rounded-xl text-xs font-semibold flex items-center gap-2 whitespace-nowrap transition ${
                isActive
                  ? "bg-rose-500/10 text-rose-400 border border-rose-500/20 shadow-sm"
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
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-4">
            <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
              <h2 className="text-sm font-semibold text-white flex items-center gap-2">
                <Activity className="w-4 h-4 text-rose-400" />
                Live Security Telemetry Stream
              </h2>

              <div className="space-y-2">
                {events.map((evt) => (
                  <div key={evt.id} className="p-3.5 bg-slate-800/40 rounded-xl border border-slate-700/50 flex items-center justify-between">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span className={`text-[10px] font-mono px-2 py-0.5 rounded font-bold uppercase ${
                          evt.severity === "high" || evt.severity === "critical" ? "bg-rose-500/20 text-rose-300 border border-rose-500/30" : "bg-amber-500/20 text-amber-300 border border-amber-500/30"
                        }`}>
                          {evt.severity}
                        </span>
                        <span className="text-xs font-semibold text-slate-200">{evt.eventType}</span>
                        <span className="text-xs text-slate-500">from {evt.source}</span>
                      </div>
                      <p className="text-xs text-slate-400 font-mono">Actor: {evt.actor} | Target: {evt.resource}</p>
                    </div>
                    <span className="text-[10px] text-slate-500 font-mono">{evt.timestamp.substring(11, 19)}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
              <h2 className="text-sm font-semibold text-white flex items-center gap-2">
                <Shield className="w-4 h-4 text-emerald-400" />
                Zero-Trust Defense Status
              </h2>

              <div className="space-y-3">
                <div className="p-3 bg-slate-800/50 rounded-xl border border-slate-700/40 flex items-center justify-between text-xs">
                  <span className="text-slate-300 font-medium">Prompt Injection Scanner</span>
                  <span className="text-emerald-400 font-mono flex items-center gap-1"><CheckCircle className="w-3.5 h-3.5" /> Enforcing</span>
                </div>
                <div className="p-3 bg-slate-800/50 rounded-xl border border-slate-700/40 flex items-center justify-between text-xs">
                  <span className="text-slate-300 font-medium">Secret &amp; Credential Redactor</span>
                  <span className="text-emerald-400 font-mono flex items-center gap-1"><CheckCircle className="w-3.5 h-3.5" /> Enforcing</span>
                </div>
                <div className="p-3 bg-slate-800/50 rounded-xl border border-slate-700/40 flex items-center justify-between text-xs">
                  <span className="text-slate-300 font-medium">DLP Exfiltration Boundary</span>
                  <span className="text-emerald-400 font-mono flex items-center gap-1"><CheckCircle className="w-3.5 h-3.5" /> Enforcing</span>
                </div>
                <div className="p-3 bg-slate-800/50 rounded-xl border border-slate-700/40 flex items-center justify-between text-xs">
                  <span className="text-slate-300 font-medium">Cross-Tenant Isolation Shield</span>
                  <span className="text-emerald-400 font-mono flex items-center gap-1"><CheckCircle className="w-3.5 h-3.5" /> Authoritative</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB CONTENT: Threats */}
      {activeTab === "threats" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <ShieldAlert className="w-4 h-4 text-amber-400" />
            Detected Threat Findings
          </h2>

          <div className="space-y-3">
            {threats.map((tf) => (
              <div key={tf.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-rose-400">{tf.threatType}</span>
                    <span className="text-[10px] bg-rose-500/20 text-rose-300 px-2 py-0.5 rounded font-mono uppercase">{tf.severity}</span>
                    <span className="text-[10px] bg-slate-700 text-slate-300 px-2 py-0.5 rounded font-mono">{tf.status}</span>
                  </div>
                  <p className="text-xs text-slate-300 font-mono">Matched Pattern: {tf.evidence?.matched_pattern || "n/a"}</p>
                  <p className="text-[11px] text-slate-400 italic">&quot;{tf.evidence?.snippet || "No snippet available"}&quot;</p>
                </div>

                <div className="flex items-center gap-3">
                  <span className="text-xs text-indigo-300 font-mono">Action: {tf.recommendedAction}</span>
                  <button
                    onClick={() => {
                      setQTargetType("agent");
                      setQTargetId("agent_analyst_01");
                      setQReason(`Threat finding ${tf.id}: ${tf.threatType}`);
                      setShowQuarantineModal(true);
                    }}
                    className="px-3 py-1.5 bg-rose-600 hover:bg-rose-500 text-white rounded-lg text-xs font-semibold transition"
                  >
                    Quarantine Agent
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Incidents */}
      {activeTab === "incidents" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-rose-400" />
            Security Incidents
          </h2>

          <div className="space-y-3">
            {incidents.map((inc) => (
              <div key={inc.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-white">{inc.id}</span>
                    <span className="text-[10px] bg-rose-500/20 text-rose-300 px-2 py-0.5 rounded font-mono uppercase">{inc.severity}</span>
                    <span className="text-[10px] bg-amber-500/20 text-amber-300 px-2 py-0.5 rounded font-mono uppercase">{inc.status}</span>
                  </div>
                  <span className="text-[10px] text-slate-500 font-mono">{inc.createdAt.substring(0, 10)}</span>
                </div>
                <p className="text-xs text-slate-300">{inc.summary}</p>
                <div className="flex items-center gap-2 pt-2 border-t border-slate-700/50">
                  {inc.status !== "contained" && (
                    <button onClick={() => handleContainIncident(inc.id)} className="px-3 py-1.5 bg-amber-600 hover:bg-amber-500 text-white rounded-lg text-xs font-semibold transition">
                      Contain Incident
                    </button>
                  )}
                  <span className="text-[11px] text-slate-400 font-mono">Linked Events: {inc.event_ids?.length || 1}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Quarantine Control */}
      {activeTab === "quarantine" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-semibold text-white flex items-center gap-2">
              <Lock className="w-4 h-4 text-purple-400" />
              Active Quarantine Isolation List
            </h2>
            <button
              onClick={() => setShowQuarantineModal(true)}
              className="px-3.5 py-1.5 bg-rose-600 hover:bg-rose-500 text-white rounded-lg text-xs font-semibold transition flex items-center gap-1.5"
            >
              <Plus className="w-3.5 h-3.5" />
              Quarantine Target
            </button>
          </div>

          <div className="space-y-3">
            {quarantines.map((q) => (
              <div key={q.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-purple-300">{q.targetId} ({q.targetType})</span>
                    <span className={`text-[10px] px-2 py-0.5 rounded font-mono uppercase ${q.status === "active" ? "bg-rose-500/20 text-rose-300" : "bg-emerald-500/20 text-emerald-300"}`}>
                      {q.status}
                    </span>
                  </div>
                  <p className="text-xs text-slate-300 font-mono">Reason: {q.reason}</p>
                  <p className="text-[11px] text-slate-500">Scope: {q.scope} | Created by: {q.createdBy}</p>
                </div>

                {q.status === "active" && (
                  <button
                    onClick={() => handleReleaseQuarantine(q.id)}
                    className="px-3.5 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-semibold transition flex items-center gap-1.5"
                  >
                    <Unlock className="w-3.5 h-3.5" />
                    Release Isolation
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Agent Baselines */}
      {activeTab === "behavior" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Activity className="w-4 h-4 text-cyan-400" />
            Agent Behavior Baseline Metrics
          </h2>

          {baseline && (
            <div className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-cyan-300">{baseline.agentId}</span>
                <span className="text-[10px] text-slate-500 font-mono">Updated: {baseline.updatedAt?.substring(0, 10)}</span>
              </div>
              <div className="grid grid-cols-3 gap-4 text-xs font-mono">
                <div>
                  <span className="text-slate-400">Average Latency:</span>
                  <p className="text-slate-200 font-bold">{baseline.avgLatencyMs} ms</p>
                </div>
                <div>
                  <span className="text-slate-400">Average Data Volume:</span>
                  <p className="text-slate-200 font-bold">{baseline.avgDataVolumeBytes} bytes</p>
                </div>
                <div>
                  <span className="text-slate-400">Tool Frequencies:</span>
                  <p className="text-slate-200 font-bold">{JSON.stringify(baseline.toolFrequencyJson)}</p>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* TAB CONTENT: Threat Intelligence */}
      {activeTab === "intelligence" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Database className="w-4 h-4 text-emerald-400" />
            Pluggable Threat Intelligence Feed Signals
          </h2>

          <div className="space-y-3">
            {intelSignals.map((sig) => (
              <div key={sig.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-1">
                <div className="flex items-center justify-between text-xs font-mono">
                  <span className="font-bold text-emerald-400">{sig.indicatorValue} ({sig.indicatorType})</span>
                  <span className="text-slate-400">Confidence: {(sig.confidence * 100).toFixed(0)}%</span>
                </div>
                <p className="text-xs text-slate-300 font-mono">Source: {sig.source}</p>
                <p className="text-[11px] text-slate-400">{JSON.stringify(sig.context)}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Quarantine Modal */}
      {showQuarantineModal && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 max-w-md w-full space-y-4">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <Lock className="w-5 h-5 text-rose-400" />
              Quarantine Resource Target
            </h3>

            <div className="space-y-3">
              <div>
                <label className="text-xs text-slate-400 block mb-1">Target Type</label>
                <select
                  value={qTargetType}
                  onChange={(e) => setQTargetType(e.target.value)}
                  className="w-full bg-slate-800 border border-slate-700 rounded-xl p-2 text-xs text-white"
                >
                  <option value="agent">Agent</option>
                  <option value="skill">Skill</option>
                  <option value="capability">Capability</option>
                  <option value="workflow">Workflow</option>
                  <option value="integration">Integration</option>
                </select>
              </div>

              <div>
                <label className="text-xs text-slate-400 block mb-1">Target Identifier (ID)</label>
                <input
                  type="text"
                  placeholder="e.g. agent_analyst_01"
                  value={qTargetId}
                  onChange={(e) => setQTargetId(e.target.value)}
                  className="w-full bg-slate-800 border border-slate-700 rounded-xl p-2 text-xs text-white font-mono"
                />
              </div>

              <div>
                <label className="text-xs text-slate-400 block mb-1">Reason for Quarantine</label>
                <textarea
                  placeholder="Describe security isolation reason..."
                  value={qReason}
                  onChange={(e) => setQReason(e.target.value)}
                  className="w-full bg-slate-800 border border-slate-700 rounded-xl p-2 text-xs text-white h-20"
                />
              </div>
            </div>

            <div className="flex items-center justify-end gap-2 pt-2">
              <button
                onClick={() => setShowQuarantineModal(false)}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-xs font-semibold transition"
              >
                Cancel
              </button>
              <button
                onClick={handleQuarantineSubmit}
                className="px-4 py-2 bg-rose-600 hover:bg-rose-500 text-white rounded-xl text-xs font-semibold transition"
              >
                Enforce Quarantine
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
