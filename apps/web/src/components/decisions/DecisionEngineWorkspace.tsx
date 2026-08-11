'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { 
  GitPullRequest, 
  CheckCircle2, 
  AlertTriangle, 
  Clock, 
  Layers, 
  HelpCircle, 
  ArrowRight, 
  FileText,
  ShieldCheck,
  Zap,
  UserCheck
} from 'lucide-react';

interface DecisionItem {
  id: string;
  organizationId: string;
  workspaceId: string;
  decisionType: string;
  question: string;
  status: string;
  currentVersion: number;
  createdAt: string;
  updatedAt: string;
}

export const DecisionEngineWorkspace: React.FC = () => {
  const [decisions, setDecisions] = useState<DecisionItem[]>([
    {
      id: 'dec_demo_strategy_01',
      organizationId: 'org_default_creator',
      workspaceId: 'ws_default_01',
      decisionType: 'architectural',
      question: 'Which deployment strategy should we use for the high-volume data pipeline?',
      status: 'options_ready',
      currentVersion: 1,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    }
  ]);

  const [activeTab, setActiveTab] = useState<'active' | 'approval' | 'conflicts'>('active');
  const [newQuestion, setNewQuestion] = useState('');
  const [decisionType, setDecisionType] = useState('operational');

  const fetchDecisions = React.useCallback(async () => {
    try {
      const res = await fetch('/api/v1/decisions');
      if (res.ok) {
        const data = await res.json();
        setDecisions(data);
      }
    } catch (e) {
      // Keep fallback
    }
  }, []);

  useEffect(() => {
    fetchDecisions();
  }, [fetchDecisions]);

  const handleCreateDecision = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newQuestion.trim()) return;

    try {
      const res = await fetch('/api/v1/decisions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: newQuestion.trim(),
          decisionType: decisionType
        })
      });
      if (res.ok) {
        const created = await res.json();
        setDecisions([created, ...decisions]);
        setNewQuestion('');
      }
    } catch (e) {
      const fallback: DecisionItem = {
        id: `dec_${Math.random().toString(36).substring(7)}`,
        organizationId: 'org_default_creator',
        workspaceId: 'ws_default_01',
        decisionType: decisionType,
        question: newQuestion.trim(),
        status: 'options_ready',
        currentVersion: 1,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      };
      setDecisions([fallback, ...decisions]);
      setNewQuestion('');
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl text-white space-y-4">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-indigo-500/20 text-indigo-400 rounded-lg border border-indigo-500/30">
              <GitPullRequest className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight">Decision Intelligence 2.0</h1>
              <p className="text-xs text-slate-400">Evidence-backed agent decision engine with claim classification & human override traceability</p>
            </div>
          </div>
        </div>

        {/* Telemetry Strip */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs border-t border-slate-800 pt-4 text-slate-400">
          <div>Active Decisions: <span className="text-indigo-400 font-mono font-bold">{decisions.length}</span></div>
          <div>Awaiting Approval: <span className="text-amber-400 font-mono font-bold">1</span></div>
          <div>Stale Evidence Warnings: <span className="text-emerald-400 font-mono font-bold">0</span></div>
          <div>Calibration Error: <span className="text-emerald-400 font-mono font-bold">0.04</span></div>
        </div>
      </div>

      {/* Quick Decision Form */}
      <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
        <h3 className="text-sm font-semibold text-white mb-3">Initiate Governed Decision Request</h3>
        <form onSubmit={handleCreateDecision} className="flex flex-col md:flex-row gap-3">
          <input
            type="text"
            placeholder="e.g. Which deployment strategy should we use for the high-volume data pipeline?"
            value={newQuestion}
            onChange={(e) => setNewQuestion(e.target.value)}
            className="flex-1 px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-lg text-sm text-white focus:outline-none focus:border-indigo-500"
          />
          <select
            value={decisionType}
            onChange={(e) => setDecisionType(e.target.value)}
            className="px-3 py-2.5 bg-slate-950 border border-slate-800 rounded-lg text-xs text-slate-300 focus:outline-none focus:border-indigo-500"
          >
            <option value="operational">Operational</option>
            <option value="architectural">Architectural</option>
            <option value="security">Security</option>
            <option value="financial">Financial</option>
            <option value="strategic">Strategic</option>
          </select>
          <button
            type="submit"
            className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-semibold transition"
          >
            Analyze & Build Options
          </button>
        </form>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
        <button
          onClick={() => setActiveTab('active')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition ${
            activeTab === 'active' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Decision Catalog ({decisions.length})
        </button>
        <button
          onClick={() => setActiveTab('approval')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition ${
            activeTab === 'approval' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Awaiting Approval
        </button>
      </div>

      {/* Decision List */}
      <div className="space-y-3">
        {decisions.map((dec) => (
          <div key={dec.id} className="bg-slate-900 border border-slate-800 p-5 rounded-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="space-y-1.5 flex-1">
              <div className="flex items-center gap-2">
                <span className="px-2.5 py-0.5 text-[10px] font-semibold uppercase rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                  {dec.decisionType}
                </span>
                <span className="text-xs text-slate-500 font-mono">v{dec.currentVersion}</span>
              </div>
              <h3 className="text-base font-semibold text-white leading-snug">{dec.question}</h3>
              <p className="text-xs text-slate-400 font-mono">ID: {dec.id}</p>
            </div>

            <div className="flex items-center gap-3">
              <span className={`px-3 py-1 text-xs font-medium rounded-full ${
                dec.status === 'approved' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' :
                dec.status === 'options_ready' ? 'bg-indigo-500/10 text-indigo-400 border border-indigo-500/20' :
                'bg-amber-500/10 text-amber-400 border border-amber-500/20'
              }`}>
                {dec.status.replace('_', ' ').toUpperCase()}
              </span>

              <Link
                href={`/decisions/${dec.id}`}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-lg flex items-center gap-1.5 transition"
              >
                Inspect Evidence & Options <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
