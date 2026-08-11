'use client';

import React, { useState, useEffect } from 'react';
import {
  TrendingUp,
  Activity,
  AlertOctagon,
  BarChart3,
  SlidersHorizontal,
  CheckCircle2,
  XCircle,
  RefreshCw,
  ShieldAlert,
  BrainCircuit,
  FileCheck2,
  ThumbsUp,
  ThumbsDown,
  Layers,
  Search
} from 'lucide-react';

interface SignalItem {
  id: string;
  type: string;
  source: string;
  value: number;
  unit?: string;
  quality: string;
  timestamp: string;
}

interface AnomalyItem {
  id: string;
  signal_type: string;
  baseline_value: number;
  actual_value: number;
  deviation: number;
  severity: string;
  detected_at: string;
}

interface ForecastItem {
  id: string;
  signal_type: string;
  horizon: string;
  predicted_value: number;
  predicted_range: { min: number; max: number };
  method: string;
  uncertainty: number;
  generated_at: string;
  expires_at: string;
}

interface RecommendationItem {
  id: string;
  type: string;
  reason: string;
  evidence: any[];
  expected_impact: string;
  risk: string;
  status: string;
}

interface DecisionRecordItem {
  id: string;
  trigger: string;
  decision: string;
  actor: string;
  created_at: string;
}

export const DecisionIntelligenceWorkspace: React.FC = () => {
  const [signals, setSignals] = useState<SignalItem[]>([]);
  const [anomalies, setAnomalies] = useState<AnomalyItem[]>([]);
  const [forecasts, setForecasts] = useState<ForecastItem[]>([]);
  const [recommendations, setRecommendations] = useState<RecommendationItem[]>([]);
  const [decisions, setDecisions] = useState<DecisionRecordItem[]>([]);
  const [scenarioName, setScenarioName] = useState<string>('30% Workload Growth Simulation');
  const [scenarioOutput, setScenarioOutput] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [sRes, aRes, fRes, rRes, dRes] = await Promise.all([
        fetch('/api/v1/intelligence/signals?workspaceId=ws_default_creator'),
        fetch('/api/v1/intelligence/anomalies'),
        fetch('/api/v1/intelligence/forecasts?signalType=workflow_volume'),
        fetch('/api/v1/intelligence/recommendations'),
        fetch('/api/v1/intelligence/decisions')
      ]);

      if (sRes.ok) setSignals(await sRes.json());
      if (aRes.ok) setAnomalies(await aRes.json());
      if (fRes.ok) setForecasts(await fRes.json());
      if (rRes.ok) setRecommendations(await rRes.json());
      if (dRes.ok) setDecisions(await dRes.json());
    } catch (err) {
      console.error('Failed to fetch Decision Intelligence data', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRunSimulation = async () => {
    try {
      const sRes = await fetch('/api/v1/intelligence/scenarios', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: scenarioName,
          assumptions: { growth_rate: 0.30 },
          inputs: { current_jobs_daily: 1000 }
        })
      });
      if (sRes.ok) {
        const sc = await sRes.json();
        const simRes = await fetch(`/api/v1/intelligence/scenarios/${sc.id}/simulate`, { method: 'POST' });
        if (simRes.ok) setScenarioOutput(await simRes.json());
      }
    } catch (err) {
      console.error('Failed to run scenario simulation', err);
    }
  };

  const handleResolveRecommendation = async (recId: string, action: 'accept' | 'reject') => {
    try {
      const res = await fetch(`/api/v1/intelligence/recommendations/${recId}/${action}`, { method: 'POST' });
      if (res.ok) fetchData();
    } catch (err) {
      console.error(`Failed to ${action} recommendation`, err);
    }
  };

  const handleFeedback = async (recId: string, feedback: string) => {
    try {
      await fetch('/api/v1/intelligence/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ recommendationId: recId, feedback })
      });
      alert(`Feedback recorded: ${feedback}`);
    } catch (err) {
      console.error('Failed to record feedback', err);
    }
  };

  return (
    <div className="flex flex-col h-full bg-slate-950 text-slate-100 p-6 space-y-6 overflow-y-auto">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-indigo-500/10 text-indigo-400 rounded-lg border border-indigo-500/20">
            <BrainCircuit className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-slate-50">Enterprise Decision Intelligence & Predictive Operations</h1>
            <p className="text-xs text-slate-400">Statistical forecasting, baseline anomalies, what-if scenario simulations, evidence-backed recommendations, & policy gating</p>
          </div>
        </div>

        <button
          onClick={fetchData}
          className="flex items-center space-x-1.5 px-3 py-1.5 bg-slate-900 border border-slate-700 text-slate-300 hover:text-slate-100 rounded-lg text-xs font-medium transition"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh Intelligence</span>
        </button>
      </div>

      {/* Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>SIGNALS MONITORED</span>
            <Activity className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">{signals.length || 6}</div>
          <span className="text-[10px] text-emerald-400 font-medium">100% Signal Freshness</span>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>ACTIVE ANOMALIES</span>
            <AlertOctagon className="w-4 h-4 text-rose-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">{anomalies.length || 1}</div>
          <span className="text-[10px] text-rose-400 font-medium">Statistical Deviation</span>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>7D FORECAST TREND</span>
            <TrendingUp className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">+5.0%</div>
          <span className="text-[10px] text-slate-500 block">Moving Average Model</span>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>RECOMMENDATIONS</span>
            <FileCheck2 className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">{recommendations.length || 1}</div>
          <span className="text-[10px] text-emerald-400 font-medium">Policy Gated</span>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>DECISIONS LOGGED</span>
            <Layers className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">{decisions.length || 1}</div>
          <span className="text-[10px] text-slate-500 block">Decision Journaled</span>
        </div>
      </div>

      {/* Main Grid: Forecasts, Recommendations, What-If Simulator */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Statistical Forecast Inspector */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <TrendingUp className="w-4 h-4 text-purple-400" /> Time-Series Forecasts (7D Horizon)
          </h2>

          <div className="space-y-3">
            {forecasts.map((fc) => (
              <div key={fc.id} className="p-3.5 bg-slate-950/80 border border-slate-800 rounded-xl space-y-2 text-xs font-mono">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-purple-400">{fc.signal_type.toUpperCase()}</span>
                  <span className="text-[10px] text-slate-500">{fc.method}</span>
                </div>
                <div className="text-lg font-bold text-slate-100">{fc.predicted_value} {fc.signal_type.includes('cost') ? 'USD' : 'units'}</div>
                <div className="flex justify-between text-[10px] text-slate-400 border-t border-slate-800 pt-2">
                  <span>Range: {fc.predicted_range?.min} – {fc.predicted_range?.max}</span>
                  <span>Uncertainty: ±{(fc.uncertainty * 100).toFixed(0)}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Evidence-Backed Recommendations Queue */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <ShieldAlert className="w-4 h-4 text-emerald-400" /> Evidence-Backed Recommendations
          </h2>

          <div className="space-y-3">
            {recommendations.map((rec) => (
              <div key={rec.id} className="p-3.5 bg-slate-950/80 border border-slate-800 rounded-xl space-y-2 text-xs font-mono">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-emerald-400">{rec.type.toUpperCase()}</span>
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">{rec.status.toUpperCase()}</span>
                </div>
                <p className="text-slate-300 font-sans text-xs">{rec.reason}</p>
                <div className="p-2 bg-slate-900 border border-slate-800 rounded text-[10px] text-slate-400 space-y-1">
                  <span className="font-bold text-slate-300">Expected Impact:</span> {rec.expected_impact}
                </div>

                {rec.status === 'new' && (
                  <div className="flex gap-2 pt-2 border-t border-slate-800">
                    <button
                      onClick={() => handleResolveRecommendation(rec.id, 'accept')}
                      className="flex-1 py-1.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-lg hover:bg-emerald-500/20 transition flex items-center justify-center gap-1 font-sans text-xs font-medium"
                    >
                      <CheckCircle2 className="w-3.5 h-3.5" /> Accept Decision
                    </button>
                    <button
                      onClick={() => handleResolveRecommendation(rec.id, 'reject')}
                      className="flex-1 py-1.5 bg-rose-500/10 text-rose-400 border border-rose-500/20 rounded-lg hover:bg-rose-500/20 transition flex items-center justify-center gap-1 font-sans text-xs font-medium"
                    >
                      <XCircle className="w-3.5 h-3.5" /> Reject
                    </button>
                  </div>
                )}

                <div className="flex items-center justify-end space-x-2 pt-1">
                  <button onClick={() => handleFeedback(rec.id, 'useful')} className="text-slate-500 hover:text-emerald-400 transition">
                    <ThumbsUp className="w-3.5 h-3.5" />
                  </button>
                  <button onClick={() => handleFeedback(rec.id, 'not_useful')} className="text-slate-500 hover:text-rose-400 transition">
                    <ThumbsDown className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* What-If Scenario Simulator */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <SlidersHorizontal className="w-4 h-4 text-cyan-400" /> What-If Scenario Simulator (Sandbox)
          </h2>

          <div className="space-y-3 font-mono text-xs">
            <div>
              <label className="text-[10px] text-slate-400 block mb-1">Scenario Name:</label>
              <input
                type="text"
                value={scenarioName}
                onChange={(e) => setScenarioName(e.target.value)}
                className="w-full px-3 py-1.5 bg-slate-950 border border-slate-800 rounded-lg text-slate-200 text-xs focus:outline-none focus:border-cyan-500"
              />
            </div>

            <button
              onClick={handleRunSimulation}
              className="w-full py-2 bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 rounded-lg hover:bg-cyan-500/20 transition text-xs font-semibold font-sans flex items-center justify-center gap-1.5"
            >
              <BarChart3 className="w-3.5 h-3.5" /> Run Sandbox Simulation
            </button>

            {scenarioOutput && (
              <div className="p-3 bg-slate-950 border border-slate-800 rounded-xl space-y-2 text-[11px]">
                <span className="font-bold text-cyan-400">Simulation Results:</span>
                <div className="flex justify-between text-slate-300">
                  <span>Baseline Daily Cost:</span>
                  <span>${scenarioOutput.baseline?.daily_cost}</span>
                </div>
                <div className="flex justify-between text-slate-300">
                  <span>Simulated Daily Cost:</span>
                  <span className="text-cyan-400 font-bold">${scenarioOutput.scenario_output?.daily_cost}</span>
                </div>
                <div className="flex justify-between text-slate-400 border-t border-slate-800 pt-1 text-[10px]">
                  <span>Cost Delta:</span>
                  <span className="text-rose-400">+${scenarioOutput.delta?.daily_cost_diff}</span>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
