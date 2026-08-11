'use client';

import React, { useState, useEffect } from 'react';
import {
  DollarSign,
  TrendingUp,
  AlertTriangle,
  Server,
  Cpu,
  Activity,
  ShieldCheck,
  RefreshCw,
  Clock,
  Layers,
  ArrowUpRight,
  Zap,
  BarChart3
} from 'lucide-react';

interface FinOpsOverview {
  today_cost: number;
  last_7d_cost: number;
  last_30d_cost: number;
  mtd_cost: number;
  budget_limit: number;
  budget_used: number;
  budget_remaining: number;
  active_incidents_count: number;
  active_anomalies_count: number;
}

interface ModelHealth {
  provider: string;
  model: string;
  status: string;
  latency_p50_ms: number;
  latency_p95_ms: number;
  success_rate: number;
  total_calls_24h: number;
  estimated_cost_24h: number;
}

export const FinOpsWorkspace: React.FC = () => {
  const [overview, setOverview] = useState<FinOpsOverview | null>(null);
  const [models, setModels] = useState<ModelHealth[]>([]);
  const [anomalies, setAnomalies] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [ovRes, mdRes, anRes] = await Promise.all([
        fetch('/api/v1/finops/overview?workspaceId=ws_default_creator'),
        fetch('/api/v1/infrastructure/models'),
        fetch('/api/v1/anomalies?workspaceId=ws_default_creator')
      ]);

      if (ovRes.ok) setOverview(await ovRes.json());
      if (mdRes.ok) setModels(await mdRes.json());
      if (anRes.ok) setAnomalies(await anRes.json());
    } catch (err) {
      console.error('Failed to fetch FinOps data', err);
    } finally {
      setLoading(false);
    }
  };

  const budgetPct = overview ? Math.min(100, Math.round((overview.budget_used / overview.budget_limit) * 100)) : 0;

  return (
    <div className="flex flex-col h-full bg-slate-950 text-slate-100 p-6 space-y-6 overflow-y-auto">
      {/* Top Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-emerald-500/10 text-emerald-400 rounded-lg border border-emerald-500/20">
            <DollarSign className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-slate-50">FinOps & AI Infrastructure Intelligence</h1>
            <p className="text-xs text-slate-400">Cost attribution, versioned model pricing, pre-flight budget enforcement, and infrastructure health</p>
          </div>
        </div>

        <button
          onClick={fetchData}
          className="flex items-center space-x-1.5 px-3 py-1.5 bg-slate-900 border border-slate-700 text-slate-300 hover:text-slate-100 rounded-lg text-xs font-medium transition"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh Metrics</span>
        </button>
      </div>

      {/* Spend Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>TODAY SPEND (ESTIMATED)</span>
            <DollarSign className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">${overview?.today_cost.toFixed(4) || '0.0000'}</div>
          <span className="text-[10px] text-slate-500 block">7D Cost: ${overview?.last_7d_cost.toFixed(2) || '0.00'}</span>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>MONTH-TO-DATE SPEND</span>
            <TrendingUp className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">${overview?.mtd_cost.toFixed(2) || '0.00'}</div>
          <span className="text-[10px] text-slate-500 block">30D Cost: ${overview?.last_30d_cost.toFixed(2) || '0.00'}</span>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>BUDGET REMAINING</span>
            <ShieldCheck className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-xl font-bold text-emerald-400 font-mono">${overview?.budget_remaining.toFixed(2) || '0.00'}</div>
          <div className="w-full bg-slate-950 rounded-full h-1.5 mt-1 overflow-hidden border border-slate-800">
            <div className={`h-full ${budgetPct > 85 ? 'bg-amber-500' : 'bg-emerald-500'}`} style={{ width: `${budgetPct}%` }} />
          </div>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>ACTIVE COST ANOMALIES</span>
            <AlertTriangle className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">{overview?.active_anomalies_count || 0}</div>
          <span className="text-[10px] text-slate-500 block">Baseline vs Observed Spikes</span>
        </div>
      </div>

      {/* Main Grid: Anomalies & Model Infrastructure Health */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Cost Anomalies Panel */}
        <div className="lg:col-span-1 bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <AlertTriangle className="w-4 h-4 text-amber-400" /> Active Usage & Cost Anomalies
          </h2>

          {anomalies.length === 0 ? (
            <div className="text-center py-8 text-xs text-slate-500 border border-dashed border-slate-800 rounded-lg">
              No active cost or latency anomalies detected.
            </div>
          ) : (
            <div className="space-y-3">
              {anomalies.map((a) => (
                <div key={a.id} className="p-3.5 bg-amber-500/10 border border-amber-500/20 rounded-xl space-y-2 text-xs">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-amber-300 uppercase tracking-wider text-[10px]">{a.type} ({a.severity})</span>
                    <span className="text-[10px] text-amber-400 font-mono">+{Math.round(((a.observed_value - a.baseline_value) / a.baseline_value) * 100)}%</span>
                  </div>
                  <p className="text-[11px] text-slate-300">{a.explanation}</p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Model Infrastructure & Telemetry Table */}
        <div className="lg:col-span-2 bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <Cpu className="w-4 h-4 text-indigo-400" /> LLM Model Infrastructure Telemetry
          </h2>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-800 text-[10px] text-slate-500 uppercase font-mono">
                  <th className="pb-2">Provider / Model</th>
                  <th className="pb-2">Status</th>
                  <th className="pb-2">p50 Latency</th>
                  <th className="pb-2">p95 Latency</th>
                  <th className="pb-2">Success Rate</th>
                  <th className="pb-2">24h Spend (Est.)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {models.map((m, idx) => (
                  <tr key={idx} className="hover:bg-slate-900/80">
                    <td className="py-3 font-semibold text-slate-200">{m.provider} / {m.model}</td>
                    <td className="py-3">
                      <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono">
                        {m.status.toUpperCase()}
                      </span>
                    </td>
                    <td className="py-3 font-mono text-slate-300">{m.latency_p50_ms} ms</td>
                    <td className="py-3 font-mono text-slate-400">{m.latency_p95_ms} ms</td>
                    <td className="py-3 font-mono text-emerald-400">{(m.success_rate * 100).toFixed(1)}%</td>
                    <td className="py-3 font-mono text-indigo-400">${m.estimated_cost_24h.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};
