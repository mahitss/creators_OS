"use client";

import React, { useState, useEffect, useCallback } from "react";
import {
  AlertTriangle,
  Clock,
  Shield,
  ShieldAlert,
  Zap,
  CheckCircle,
  FileText,
  Activity,
  Layers,
  Lock,
  Unlock,
  Check,
  Play,
  RotateCcw,
  Network
} from "lucide-react";

export function IncidentDetailWorkspace({ incidentId }: { incidentId: string }) {
  const [incident, setIncident] = useState<any>(null);
  const [timeline, setTimeline] = useState<any[]>([]);
  const [evidence, setEvidence] = useState<any[]>([]);
  const [impact, setImpact] = useState<any>(null);
  const [responsePlans, setResponsePlans] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchData = useCallback(async () => {
    setIsLoading(true);
    try {
      const [incRes, timeRes, evRes, impRes, respRes] = await Promise.all([
        fetch(`/api/v1/security/incidents/${incidentId}`).then((r) => (r.ok ? r.json() : null)),
        fetch(`/api/v1/security/incidents/${incidentId}/timeline`).then((r) => (r.ok ? r.json() : { timeline: [] })),
        fetch(`/api/v1/security/incidents/${incidentId}/evidence`).then((r) => (r.ok ? r.json() : { evidence_chain: [] })),
        fetch(`/api/v1/security/incidents/${incidentId}/impact`).then((r) => (r.ok ? r.json() : null)),
        fetch(`/api/v1/security/incidents/${incidentId}/response`).then((r) => (r.ok ? r.json() : []))
      ]);

      setIncident(incRes);
      setTimeline(timeRes.timeline || []);
      setEvidence(evRes.evidence_chain || []);
      setImpact(impRes);
      setResponsePlans(respRes);
    } catch (err) {
      console.error("Failed to load Incident Detail:", err);
    } finally {
      setIsLoading(false);
    }
  }, [incidentId]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleApprovePlan = async (planId: string) => {
    try {
      const res = await fetch(`/api/v1/security/incidents/${incidentId}/response/approve?plan_id=${planId}&approver_id=sec_admin_01`, {
        method: "POST"
      });
      if (res.ok) fetchData();
    } catch (err) {
      console.error("Approve plan failed:", err);
    }
  };

  const handleExecutePlan = async (planId: string) => {
    try {
      const res = await fetch(`/api/v1/security/incidents/${incidentId}/response/execute?plan_id=${planId}`, {
        method: "POST"
      });
      if (res.ok) fetchData();
    } catch (err) {
      console.error("Execute plan failed:", err);
    }
  };

  const handleVerifyRecovery = async () => {
    try {
      const res = await fetch(`/api/v1/security/incidents/${incidentId}/verify`, { method: "POST" });
      if (res.ok) fetchData();
    } catch (err) {
      console.error("Verify recovery failed:", err);
    }
  };

  if (isLoading) {
    return <div className="p-8 text-center text-slate-400 font-mono">Loading incident details...</div>;
  }

  return (
    <div className="p-6 space-y-6 max-w-[1600px] mx-auto text-slate-100 font-sans">
      {/* Incident Summary Header */}
      <div className="bg-slate-900/80 p-6 rounded-2xl border border-slate-800 shadow-xl backdrop-blur-md space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-3 mb-1">
              <span className="text-xs font-mono font-bold text-slate-400">{incidentId}</span>
              <span className="text-xs bg-rose-500/20 text-rose-300 px-2.5 py-0.5 rounded font-mono font-bold uppercase border border-rose-500/30">
                {incident?.severity || "high"}
              </span>
              <span className="text-xs bg-amber-500/20 text-amber-300 px-2.5 py-0.5 rounded font-mono font-bold uppercase border border-amber-500/30">
                {incident?.status || "open"}
              </span>
            </div>
            <h1 className="text-xl font-bold text-white tracking-tight">{incident?.summary || "Security Incident"}</h1>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleVerifyRecovery}
              className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-semibold shadow-lg shadow-emerald-600/20 transition flex items-center gap-1.5"
            >
              <CheckCircle className="w-4 h-4" />
              Verify Recovery
            </button>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Section */}
        <div className="lg:col-span-2 space-y-6">
          {/* Section: Timeline & Threat Chain */}
          <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
            <h2 className="text-sm font-semibold text-white flex items-center gap-2">
              <Clock className="w-4 h-4 text-cyan-400" />
              Chronological Incident Timeline
            </h2>

            <div className="space-y-3 font-mono text-xs">
              {timeline.map((item, idx) => (
                <div key={idx} className="p-3 bg-slate-800/40 rounded-xl border border-slate-700/50 flex items-center justify-between">
                  <div className="space-y-0.5">
                    <span className="font-bold text-slate-200">{item.event}</span>
                    <p className="text-[11px] text-slate-400">{item.type || item.status || "logged"}</p>
                  </div>
                  <span className="text-slate-500 text-[10px]">{item.timestamp?.substring(11, 19)}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Section: Response Plans & Approval */}
          <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
            <h2 className="text-sm font-semibold text-white flex items-center gap-2">
              <Zap className="w-4 h-4 text-purple-400" />
              Governed Response Plans &amp; Dual Approval
            </h2>

            <div className="space-y-3 font-mono text-xs">
              {responsePlans.map((p) => (
                <div key={p.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-purple-300">Plan: {p.id} (v{p.version})</span>
                    <span className="bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded text-[10px] font-bold">{p.status}</span>
                  </div>

                  <div className="flex items-center gap-2">
                    {p.status === "draft" && (
                      <button
                        onClick={() => handleApprovePlan(p.id)}
                        className="px-3.5 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold transition"
                      >
                        Approve Plan
                      </button>
                    )}
                    {p.status === "approved" && (
                      <button
                        onClick={() => handleExecutePlan(p.id)}
                        className="px-3.5 py-1.5 bg-rose-600 hover:bg-rose-500 text-white rounded-lg text-xs font-semibold transition"
                      >
                        Execute Controlled Response
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Sidebar: Impact & Evidence Chain */}
        <div className="space-y-6">
          {/* Section: Impact Matrix */}
          <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
            <h2 className="text-sm font-semibold text-white flex items-center gap-2">
              <Activity className="w-4 h-4 text-amber-400" />
              Blast Radius &amp; Impact Matrix
            </h2>

            {impact && (
              <div className="space-y-2 text-xs font-mono">
                <div className="p-2.5 bg-slate-800/50 rounded-lg flex justify-between">
                  <span className="text-slate-400">Affected Users:</span>
                  <span className="text-slate-200 font-bold">{impact.affected_users}</span>
                </div>
                <div className="p-2.5 bg-slate-800/50 rounded-lg flex justify-between">
                  <span className="text-slate-400">Affected Agents:</span>
                  <span className="text-slate-200 font-bold">{impact.affected_agents?.join(", ")}</span>
                </div>
                <div className="p-2.5 bg-slate-800/50 rounded-lg flex justify-between">
                  <span className="text-slate-400">Affected Missions:</span>
                  <span className="text-slate-200 font-bold">{impact.affected_missions?.join(", ")}</span>
                </div>
                <div className="p-2.5 bg-slate-800/50 rounded-lg flex justify-between">
                  <span className="text-slate-400">Data Boundaries:</span>
                  <span className="text-slate-200 font-bold">{impact.affected_data?.join(", ")}</span>
                </div>
              </div>
            )}
          </div>

          {/* Section: Evidence Chain */}
          <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
            <h2 className="text-sm font-semibold text-white flex items-center gap-2">
              <Lock className="w-4 h-4 text-emerald-400" />
              Immutable Evidence Lock
            </h2>

            <div className="space-y-3 font-mono text-xs">
              {evidence.map((ev) => (
                <div key={ev.id} className="p-3 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-1">
                  <span className="text-slate-400 font-bold">{ev.source}</span>
                  <p className="text-[11px] text-slate-300 italic">&quot;{ev.snippet}&quot;</p>
                  <p className="text-[9px] text-slate-500 truncate">Hash: {ev.integrity_hash}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
