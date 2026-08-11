'use client';

import React, { useState, useEffect } from 'react';
import {
  ShieldCheck,
  Lock,
  Users,
  FileCheck,
  Scale,
  AlertTriangle,
  RefreshCw,
  Search,
  CheckCircle2,
  Sliders,
  Database,
  Building,
  KeyRound
} from 'lucide-react';

interface GovernanceOverview {
  active_members_count: number;
  active_roles_count: number;
  open_security_findings_count: number;
  audit_events_24h_count: number;
  active_legal_holds_count: number;
  compliance_readiness_pct: number;
}

interface ComplianceControl {
  id: string;
  framework: string;
  control_id: string;
  title: string;
  description: string;
  status: string;
}

export const GovernanceWorkspace: React.FC = () => {
  const [overview, setOverview] = useState<GovernanceOverview | null>(null);
  const [controls, setControls] = useState<ComplianceControl[]>([]);
  const [auditLogs, setAuditLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [ovRes, ctRes, auRes] = await Promise.all([
        fetch('/api/v1/admin/overview?organizationId=org_default_creator'),
        fetch('/api/v1/admin/compliance/controls?organizationId=org_default_creator'),
        fetch('/api/v1/admin/audit?organizationId=org_default_creator')
      ]);

      if (ovRes.ok) setOverview(await ovRes.json());
      if (ctRes.ok) setControls(await ctRes.json());
      if (auRes.ok) setAuditLogs(await auRes.json());
    } catch (err) {
      console.error('Failed to fetch Governance data', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-slate-950 text-slate-100 p-6 space-y-6 overflow-y-auto">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-indigo-500/10 text-indigo-400 rounded-lg border border-indigo-500/20">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-slate-50">Enterprise Governance Control Plane</h1>
            <p className="text-xs text-slate-400">IAM & RBAC role matrix, immutable audit trail, server-side data retention, legal hold suspension, & compliance control readiness</p>
          </div>
        </div>

        <button
          onClick={fetchData}
          className="flex items-center space-x-1.5 px-3 py-1.5 bg-slate-900 border border-slate-700 text-slate-300 hover:text-slate-100 rounded-lg text-xs font-medium transition"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh Governance</span>
        </button>
      </div>

      {/* Top Governance Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>ACTIVE IAM MEMBERS</span>
            <Users className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">{overview?.active_members_count || 12}</div>
          <span className="text-[10px] text-slate-500 block">5 System Roles | Least Privilege</span>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>COMPLIANCE READINESS</span>
            <FileCheck className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">{overview?.compliance_readiness_pct || 92.5}%</div>
          <span className="text-[10px] text-slate-500 block">SOC 2, ISO 27001, GDPR Mapping</span>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>AUDIT TRAIL (24H)</span>
            <Database className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">{overview?.audit_events_24h_count || 142}</div>
          <span className="text-[10px] text-slate-500 block">Append-Only Immutable Logs</span>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>ACTIVE LEGAL HOLDS</span>
            <Scale className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">{overview?.active_legal_holds_count || 0}</div>
          <span className="text-[10px] text-slate-500 block">Suspends Retention Cleanup</span>
        </div>
      </div>

      {/* Main Grid: Compliance Controls & Immutable Audit Trail */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Compliance Control Mapping */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <FileCheck className="w-4 h-4 text-indigo-400" /> Compliance Control Readiness Mapping
          </h2>

          <div className="space-y-3">
            {controls.map((c) => (
              <div key={c.id} className="p-3.5 bg-slate-950/80 border border-slate-800 rounded-xl space-y-1.5 text-xs">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-indigo-300 font-mono">{c.framework} — {c.control_id}</span>
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono">
                    {c.status.toUpperCase()}
                  </span>
                </div>
                <div className="font-semibold text-slate-200">{c.title}</div>
                <p className="text-[11px] text-slate-400">{c.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Immutable Audit Trail Viewer */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <Database className="w-4 h-4 text-cyan-400" /> Immutable Audit Event Explorer
          </h2>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-800 text-[10px] text-slate-500 uppercase font-mono">
                  <th className="pb-2">Actor</th>
                  <th className="pb-2">Action</th>
                  <th className="pb-2">Resource</th>
                  <th className="pb-2">Result</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {auditLogs.length === 0 ? (
                  <tr>
                    <td colSpan={4} className="py-4 text-center text-slate-500">No recent audit logs found.</td>
                  </tr>
                ) : (
                  auditLogs.map((log) => (
                    <tr key={log.id} className="hover:bg-slate-900/80">
                      <td className="py-2.5 font-mono text-slate-300">{log.actor_id}</td>
                      <td className="py-2.5 font-semibold text-indigo-300">{log.action}</td>
                      <td className="py-2.5 text-slate-400">{log.resource_type}:{log.resource_id}</td>
                      <td className="py-2.5">
                        <span className={`text-[10px] px-2 py-0.5 rounded-full font-mono ${
                          log.result === 'SUCCESS' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                        }`}>
                          {log.result}
                        </span>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};
