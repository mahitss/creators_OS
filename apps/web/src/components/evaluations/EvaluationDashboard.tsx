import React, { useState, useEffect } from 'react';
import { 
  ShieldCheck, 
  AlertTriangle, 
  CheckCircle2, 
  XCircle, 
  Play, 
  RefreshCw, 
  Cpu, 
  DollarSign, 
  Clock, 
  Layers 
} from 'lucide-react';

interface EvalSuite {
  id: string;
  name: string;
  description: string;
  version: number;
  status: string;
}

interface EvalRun {
  id: string;
  suite_id: string;
  status: string;
  started_at: string | null;
  completed_at: string | null;
  total_cases: number;
  passed_cases: number;
  failed_cases: number;
  score: number;
  release_blocked: boolean;
  regression_detected: boolean;
}

interface EvalResult {
  id: string;
  case_id: string;
  case_name: string;
  category: string;
  status: string;
  score: number;
  hard_security_failure: boolean;
  failure_category: string | null;
  duration_ms: number;
  estimated_cost: number;
}

export const EvaluationDashboard: React.FC = () => {
  const [suites, setSuites] = useState<EvalSuite[]>([]);
  const [activeRun, setActiveRun] = useState<EvalRun | null>(null);
  const [results, setResults] = useState<EvalResult[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [running, setRunning] = useState<boolean>(false);

  useEffect(() => {
    fetchSuites();
  }, []);

  const fetchSuites = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/evaluations/suites', {
        headers: { 'X-User-Id': 'usr_admin_01' }
      });
      if (res.ok) {
        const data = await res.json();
        setSuites(data);
      }
    } catch (err) {
      console.error("Failed to fetch evaluation suites:", err);
    } finally {
      setLoading(false);
    }
  };

  const triggerRun = async (suiteId: string) => {
    setRunning(true);
    try {
      const res = await fetch(`/api/v1/evaluations/suites/${suiteId}/run`, {
        method: 'POST',
        headers: { 'X-User-Id': 'usr_admin_01' }
      });
      if (res.ok) {
        const runData: EvalRun = await res.json();
        setActiveRun(runData);

        // Poll for completion
        const interval = setInterval(async () => {
          const runRes = await fetch(`/api/v1/evaluations/runs/${runData.id}`, {
            headers: { 'X-User-Id': 'usr_admin_01' }
          });
          if (runRes.ok) {
            const updatedRun: EvalRun = await runRes.json();
            setActiveRun(updatedRun);
            if (updatedRun.status === 'completed' || updatedRun.status === 'failed') {
              clearInterval(interval);
              setRunning(false);
              fetchResults(updatedRun.id);
            }
          }
        }, 1000);
      }
    } catch (err) {
      console.error("Failed to trigger evaluation run:", err);
      setRunning(false);
    }
  };

  const fetchResults = async (runId: string) => {
    try {
      const res = await fetch(`/api/v1/evaluations/runs/${runId}/results`, {
        headers: { 'X-User-Id': 'usr_admin_01' }
      });
      if (res.ok) {
        const data = await res.json();
        setResults(data);
      }
    } catch (err) {
      console.error("Failed to fetch run results:", err);
    }
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8 text-zinc-100">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-zinc-800 pb-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
            <ShieldCheck className="w-8 h-8 text-emerald-400" />
            Vapor OS Evaluation & Simulation Lab
          </h1>
          <p className="text-zinc-400 mt-1">
            Deterministic regression suite, safety gates, and multi-model benchmarking sandbox.
          </p>
        </div>
        {suites.length > 0 && (
          <button
            onClick={() => triggerRun(suites[0].id)}
            disabled={running}
            className="flex items-center gap-2 px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white font-medium rounded-lg shadow-lg transition-all"
          >
            {running ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4 fill-current" />}
            {running ? 'Executing 30 Golden Cases...' : 'Run Golden Suite (30 Cases)'}
          </button>
        )}
      </div>

      {/* Metrics Banner */}
      {activeRun && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="p-5 bg-zinc-900/80 border border-zinc-800 rounded-xl backdrop-blur-sm">
            <div className="flex items-center gap-2 text-zinc-400 text-sm">
              <Cpu className="w-4 h-4" /> Overall Pass Score
            </div>
            <div className="text-3xl font-bold mt-2 text-white">
              {(activeRun.score * 100).toFixed(0)}%
            </div>
            <div className="text-xs text-zinc-500 mt-1">
              {activeRun.passed_cases} / {activeRun.total_cases} cases passed
            </div>
          </div>

          <div className="p-5 bg-zinc-900/80 border border-zinc-800 rounded-xl backdrop-blur-sm">
            <div className="flex items-center gap-2 text-zinc-400 text-sm">
              <AlertTriangle className="w-4 h-4 text-amber-400" /> Release Gate Status
            </div>
            <div className={`text-xl font-bold mt-2 ${activeRun.release_blocked ? 'text-rose-400' : 'text-emerald-400'}`}>
              {activeRun.release_blocked ? 'RELEASE BLOCKED' : 'CLEARED FOR DEPLOY'}
            </div>
            <div className="text-xs text-zinc-500 mt-1">
              {activeRun.release_blocked ? 'Hard security failure or score regression' : 'Zero hard security failures'}
            </div>
          </div>

          <div className="p-5 bg-zinc-900/80 border border-zinc-800 rounded-xl backdrop-blur-sm">
            <div className="flex items-center gap-2 text-zinc-400 text-sm">
              <Clock className="w-4 h-4 text-sky-400" /> Total Duration
            </div>
            <div className="text-2xl font-bold mt-2 text-white">
              {results.reduce((acc, r) => acc + r.duration_ms, 0)} ms
            </div>
            <div className="text-xs text-zinc-500 mt-1">Bounded parallel workers (max 5)</div>
          </div>

          <div className="p-5 bg-zinc-900/80 border border-zinc-800 rounded-xl backdrop-blur-sm">
            <div className="flex items-center gap-2 text-zinc-400 text-sm">
              <DollarSign className="w-4 h-4 text-emerald-400" /> Estimated Suite Cost
            </div>
            <div className="text-2xl font-bold mt-2 text-white">
              ${results.reduce((acc, r) => acc + r.estimated_cost, 0).toFixed(5)}
            </div>
            <div className="text-xs text-zinc-500 mt-1">Deterministic fake AI provider</div>
          </div>
        </div>
      )}

      {/* Case Results Table */}
      {results.length > 0 && (
        <div className="bg-zinc-900/60 border border-zinc-800 rounded-xl overflow-hidden shadow-xl">
          <div className="px-6 py-4 border-b border-zinc-800 font-semibold text-zinc-200 flex items-center justify-between">
            <span className="flex items-center gap-2">
              <Layers className="w-5 h-5 text-indigo-400" /> Case Execution Results ({results.length})
            </span>
            <span className="text-xs text-zinc-400">Isolated Synthetic Workspaces</span>
          </div>
          <div className="divide-y divide-zinc-800/60 max-h-[500px] overflow-y-auto">
            {results.map((res) => (
              <div key={res.id} className="p-4 hover:bg-zinc-800/30 transition-colors flex items-center justify-between text-sm">
                <div className="flex items-center gap-3">
                  {res.status === 'passed' ? (
                    <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
                  ) : (
                    <XCircle className="w-5 h-5 text-rose-400 shrink-0" />
                  )}
                  <div>
                    <div className="font-medium text-white">{res.case_name}</div>
                    <div className="text-xs text-zinc-400 capitalize">{res.category.replace('_', ' ')}</div>
                  </div>
                </div>

                <div className="flex items-center gap-6">
                  {res.hard_security_failure && (
                    <span className="px-2.5 py-1 text-xs font-semibold bg-rose-500/20 text-rose-300 border border-rose-500/30 rounded-md">
                      HARD SECURITY FAILURE
                    </span>
                  )}
                  <span className="text-xs text-zinc-400 font-mono">{res.duration_ms} ms</span>
                  <span className="font-bold text-white w-12 text-right">{(res.score * 100).toFixed(0)}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
