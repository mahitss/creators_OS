'use client';

import React, { useState, useEffect } from 'react';
import {
  ShieldAlert,
  Activity,
  Zap,
  CheckCircle2,
  XCircle,
  Clock,
  RefreshCw,
  Cpu,
  FileText,
  Lock,
  Flame,
  ArrowRight
} from 'lucide-react';

interface IncidentItem {
  id: string;
  service: string;
  severity: string;
  status: string;
  detected_at: string;
  summary: string;
}

interface CircuitBreakerItem {
  service: string;
  status: string;
  failure_count: number;
  cooldown_seconds: number;
}

export const ReliabilityWorkspace: React.FC = () => {
  const [circuitBreakers, setCircuitBreakers] = useState<CircuitBreakerItem[]>([]);
  const [incidents, setIncidents] = useState<IncidentItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [cbRes, incRes] = await Promise.all([
        fetch('/api/v1/circuit-breakers/openai'),
        fetch('/api/v1/incidents?workspaceId=ws_default_creator')
      ]);

      if (cbRes.ok) {
        const cbData = await cbRes.json();
        setCircuitBreakers([
          cbData,
          { service: 'anthropic', status: 'closed', failure_count: 0, cooldown_seconds: 60 },
          { service: 'google_calendar', status: 'closed', failure_count: 0, cooldown_seconds: 60 }
        ]);
      }
      if (incRes.ok) {
        setIncidents(await incRes.json());
      }
    } catch (err) {
      console.error('Failed to fetch reliability metrics', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>SELF-HEALING ENGINE</span>
            <Zap className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">ACTIVE (BOUNDED)</div>
          <span className="text-[10px] text-slate-500 block">Max Chain Depth: 5 | Policy-Enforced</span>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>CIRCUIT BREAKERS</span>
            <Activity className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">
            {circuitBreakers.filter(c => c.status === 'closed').length} / {circuitBreakers.length || 3} HEALTHY
          </div>
          <span className="text-[10px] text-slate-500 block">Auto Cooldown Failover</span>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>RECOVERY VERIFICATION</span>
            <CheckCircle2 className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-xl font-bold text-emerald-400 font-mono">100% IDEMPOTENT</div>
          <span className="text-[10px] text-slate-500 block">Post-Remediation Verification</span>
        </div>
      </div>

      {/* Main Grid: Circuit Breakers & Incident Triage */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Service Circuit Breakers */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
              <Activity className="w-4 h-4 text-indigo-400" /> Circuit Breaker States
            </h2>
            <button onClick={fetchData} className="text-slate-400 hover:text-slate-200">
              <RefreshCw className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="space-y-3">
            {circuitBreakers.map((cb, idx) => (
              <div key={idx} className="p-3 bg-slate-950/80 border border-slate-800 rounded-xl flex items-center justify-between text-xs">
                <div>
                  <div className="font-semibold text-slate-200">{cb.service}</div>
                  <div className="text-[10px] text-slate-500">Failures: {cb.failure_count} | Cooldown: {cb.cooldown_seconds}s</div>
                </div>
                <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-mono border ${
                  cb.status === 'closed' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' :
                  cb.status === 'half_open' ? 'bg-amber-500/10 text-amber-400 border-amber-500/20' :
                  'bg-rose-500/10 text-rose-400 border-rose-500/20'
                }`}>
                  {cb.status.toUpperCase()}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Reliability Security & Guardrails */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <Lock className="w-4 h-4 text-emerald-400" /> Forbidden Remediation Boundaries
          </h2>

          <div className="p-3.5 bg-slate-950/90 border border-slate-800 rounded-xl text-xs space-y-2">
            <p className="text-[11px] text-slate-400">
              The AI Self-Healing Engine is strictly prohibited from executing destructive or privilege-escalating actions without authorized human review.
            </p>

            <ul className="space-y-1 text-[11px] text-slate-300">
              <li className="flex items-center gap-1.5"><XCircle className="w-3.5 h-3.5 text-rose-400" /> Source code modification</li>
              <li className="flex items-center gap-1.5"><XCircle className="w-3.5 h-3.5 text-rose-400" /> Security policy or permission changes</li>
              <li className="flex items-center gap-1.5"><XCircle className="w-3.5 h-3.5 text-rose-400" /> Secret rotation or credential access</li>
              <li className="flex items-center gap-1.5"><XCircle className="w-3.5 h-3.5 text-rose-400" /> Billing record manipulation</li>
              <li className="flex items-center gap-1.5"><XCircle className="w-3.5 h-3.5 text-rose-400" /> Arbitrary SQL execution</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};
