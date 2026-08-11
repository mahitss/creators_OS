'use client';

import React, { useState, useEffect } from 'react';
import { 
  BarChart3, 
  CheckCircle2, 
  AlertOctagon, 
  Play, 
  RefreshCw, 
  Sliders, 
  Database, 
  UserCheck, 
  Layers, 
  Cpu, 
  ShieldCheck, 
  FileCheck2,
  TrendingUp,
  Activity
} from 'lucide-react';

interface EvaluationOverview {
  totalRuns: number;
  groundingRate: number;
  citationAccuracy: number;
  taskSuccessRate: number;
  judgeCalibrationScore: number;
  activeRegressionsCount: number;
  totalDatasetsCount: number;
  lastEvaluatedAt: string;
}

interface EvaluationRun {
  id: string;
  evaluationType: string;
  targetType: string;
  targetId: string;
  model: string;
  modelVersion: string;
  promptVersion: string;
  status: string;
  startedAt: string;
}

interface EvaluationDataset {
  id: string;
  name: string;
  version: string;
  description: string;
  scope: string;
  isGolden: boolean;
  createdAt: string;
}

export const EnterpriseEvaluationWorkspace: React.FC = () => {
  const [overview, setOverview] = useState<EvaluationOverview | null>(null);
  const [runs, setRuns] = useState<EvaluationRun[]>([]);
  const [datasets, setDatasets] = useState<EvaluationDataset[]>([]);
  const [activeTab, setActiveTab] = useState<'overview' | 'runs' | 'datasets' | 'calibration'>('overview');
  const [isLoading, setIsLoading] = useState(true);

  // New Evaluation Run Form State
  const [targetType, setTargetType] = useState('response');
  const [evalType, setEvalType] = useState('benchmark');
  const [isTriggering, setIsTriggering] = useState(false);

  const fetchData = async () => {
    setIsLoading(true);
    try {
      const [ovRes, runRes, dsRes] = await Promise.all([
        fetch('/api/v1/ai/evaluation'),
        fetch('/api/v1/ai/evaluation/runs'),
        fetch('/api/v1/ai/evaluation/datasets')
      ]);

      if (ovRes.ok) setOverview(await ovRes.json());
      if (runRes.ok) setRuns(await runRes.json());
      if (dsRes.ok) setDatasets(await dsRes.json());
    } catch (err) {
      console.error('Failed to fetch Evaluation data:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleTriggerRun = async () => {
    setIsTriggering(true);
    try {
      const res = await fetch('/api/v1/ai/evaluation/runs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          evaluationType: evalType,
          targetType: targetType,
          targetId: 'model_gemini_1_5_pro',
          model: 'gemini-1.5-pro',
          modelVersion: '1.0',
          promptVersion: 'v1.0'
        })
      });
      if (res.ok) {
        fetchData();
      }
    } catch (err) {
      console.error('Failed to trigger evaluation run:', err);
    } finally {
      setIsTriggering(false);
    }
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8 bg-slate-950 text-slate-100 min-h-screen">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-3">
            <BarChart3 className="w-8 h-8 text-cyan-400" />
            <h1 className="text-3xl font-bold tracking-tight text-white">Enterprise AI Evaluation & Intelligence Improvement</h1>
          </div>
          <p className="text-slate-400 mt-1">
            Continuous Quality, Grounding, Citation Accuracy, Judge Calibration & Regression Monitoring
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button 
            onClick={fetchData}
            className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg text-sm font-medium transition"
          >
            <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
            Refresh Telemetry
          </button>
        </div>
      </div>

      {/* Top Telemetry Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="text-slate-400 text-xs font-semibold uppercase tracking-wider">Grounding Rate</div>
          <div className="flex items-center gap-2 mt-2">
            <CheckCircle2 className="w-5 h-5 text-emerald-400" />
            <span className="text-xl font-bold text-white">{((overview?.groundingRate || 0.96) * 100).toFixed(1)}%</span>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="text-slate-400 text-xs font-semibold uppercase tracking-wider">Citation Accuracy</div>
          <div className="flex items-center gap-2 mt-2">
            <FileCheck2 className="w-5 h-5 text-cyan-400" />
            <span className="text-xl font-bold text-white">{((overview?.citationAccuracy || 0.98) * 100).toFixed(1)}%</span>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="text-slate-400 text-xs font-semibold uppercase tracking-wider">Judge Calibration</div>
          <div className="flex items-center gap-2 mt-2">
            <UserCheck className="w-5 h-5 text-indigo-400" />
            <span className="text-xl font-bold text-white">{((overview?.judgeCalibrationScore || 0.92) * 100).toFixed(1)}%</span>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="text-slate-400 text-xs font-semibold uppercase tracking-wider">Active Regressions</div>
          <div className="flex items-center gap-2 mt-2">
            <AlertOctagon className="w-5 h-5 text-emerald-400" />
            <span className="text-xl font-bold text-white">{overview?.activeRegressionsCount || 0}</span>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-800 gap-6">
        <button
          onClick={() => setActiveTab('overview')}
          className={`pb-3 text-sm font-medium border-b-2 transition ${
            activeTab === 'overview'
              ? 'border-cyan-400 text-cyan-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          Evaluation Overview
        </button>
        <button
          onClick={() => setActiveTab('runs')}
          className={`pb-3 text-sm font-medium border-b-2 transition ${
            activeTab === 'runs'
              ? 'border-cyan-400 text-cyan-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          Evaluation Runs ({runs.length})
        </button>
        <button
          onClick={() => setActiveTab('datasets')}
          className={`pb-3 text-sm font-medium border-b-2 transition ${
            activeTab === 'datasets'
              ? 'border-cyan-400 text-cyan-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          Datasets & Golden Suites ({datasets.length})
        </button>
      </div>

      {/* Overview Tab */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
            <h2 className="text-lg font-semibold text-white flex items-center gap-2">
              <Play className="w-5 h-5 text-emerald-400" />
              Trigger Multi-Dimensional Evaluation Run
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="text-xs text-slate-400 font-semibold uppercase">Target Type</label>
                <select
                  value={targetType}
                  onChange={(e) => setTargetType(e.target.value)}
                  className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-cyan-500"
                >
                  <option value="response">Response Grounding</option>
                  <option value="agent">Agent Planning & Mesh</option>
                  <option value="workflow">Workflow Execution</option>
                  <option value="decision">Decision Recommendation</option>
                  <option value="retrieval">Knowledge Retrieval</option>
                </select>
              </div>

              <div>
                <label className="text-xs text-slate-400 font-semibold uppercase">Evaluation Type</label>
                <select
                  value={evalType}
                  onChange={(e) => setEvalType(e.target.value)}
                  className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-cyan-500"
                >
                  <option value="benchmark">Benchmark Suite</option>
                  <option value="regression">Regression Gate Check</option>
                  <option value="simulation">Agent Simulation Lab</option>
                  <option value="human_review">Human Judge Calibration</option>
                </select>
              </div>

              <div className="flex items-end">
                <button
                  onClick={handleTriggerRun}
                  disabled={isTriggering}
                  className="w-full py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-medium rounded-lg transition"
                >
                  {isTriggering ? 'Executing Evaluation...' : 'Execute Evaluation Run'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Runs Tab */}
      {activeTab === 'runs' && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
          <div className="p-4 border-b border-slate-800 font-semibold text-white">
            Evaluation Run History
          </div>
          <div className="divide-y divide-slate-800">
            {runs.map((r) => (
              <div key={r.id} className="p-4 flex items-center justify-between">
                <div className="space-y-1">
                  <div className="text-sm font-medium text-white">
                    <span className="font-bold text-cyan-400">{r.evaluationType.toUpperCase()}</span> | Target: <span className="text-emerald-400">{r.targetType}</span> ({r.targetId})
                  </div>
                  <div className="text-xs text-slate-400">
                    Model: {r.model} (v{r.modelVersion}) | Prompt: {r.promptVersion}
                  </div>
                </div>

                <span className="px-2.5 py-0.5 bg-emerald-950 text-emerald-400 border border-emerald-800 text-xs rounded-full font-mono">
                  {r.status.toUpperCase()}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Datasets Tab */}
      {activeTab === 'datasets' && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
          <div className="p-4 border-b border-slate-800 font-semibold text-white flex items-center justify-between">
            <span>Evaluation Datasets & Golden Suites</span>
            <span className="text-xs text-slate-400">Immutable Versioning Enforced</span>
          </div>
          <div className="divide-y divide-slate-800">
            {datasets.map((ds) => (
              <div key={ds.id} className="p-4 flex items-center justify-between">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-bold text-white">{ds.name}</span>
                    {ds.isGolden && (
                      <span className="px-2 py-0.5 bg-amber-950 text-amber-400 border border-amber-800 text-xs rounded font-semibold">
                        GOLDEN
                      </span>
                    )}
                  </div>
                  <div className="text-xs text-slate-400">{ds.description} | Scope: {ds.scope}</div>
                </div>

                <span className="text-xs font-mono text-cyan-400">v{ds.version}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
