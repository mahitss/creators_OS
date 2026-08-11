'use client';

import React, { useState, useEffect } from 'react';
import { 
  ShieldCheck, 
  AlertTriangle, 
  CheckCircle, 
  FileText, 
  RefreshCw, 
  Zap, 
  Check, 
  XCircle, 
  Activity, 
  HelpCircle, 
  Clock, 
  Layers, 
  UserCheck, 
  Search,
  MessageSquare
} from 'lucide-react';

interface GovernanceOverview {
  totalObjects: number;
  authoritativeSourcesCount: number;
  freshRatio: number;
  staleCount: number;
  activeConflictsCount: number;
  unverifiedClaimsCount: number;
  groundingAccuracy: number;
  lastUpdated: string;
}

interface KnowledgeConflict {
  id: string;
  subject: string;
  claimA: any;
  claimB: any;
  sources: any[];
  status: string;
  createdAt: string;
}

interface KnowledgeClaim {
  id: string;
  subject: string;
  predicate: string;
  objectVal: string;
  sourceReferences: any[];
  status: string;
  confidence: string;
  observedAt: string;
}

export const KnowledgeGovernanceWorkspace: React.FC = () => {
  const [overview, setOverview] = useState<GovernanceOverview | null>(null);
  const [conflicts, setConflicts] = useState<KnowledgeConflict[]>([]);
  const [claims, setClaims] = useState<KnowledgeClaim[]>([]);
  const [activeTab, setActiveTab] = useState<'governance' | 'conflicts' | 'claims' | 'trusted_context'>('governance');
  const [isLoading, setIsLoading] = useState(true);

  // Trusted Context Builder Test state
  const [contextQuery, setContextQuery] = useState('Project Alpha release deadline');
  const [contextResult, setContextResult] = useState<any>(null);
  const [isContextLoading, setIsContextLoading] = useState(false);

  const fetchData = async () => {
    setIsLoading(true);
    try {
      const [ovRes, confRes, clmRes] = await Promise.all([
        fetch('/api/v1/knowledge/governance'),
        fetch('/api/v1/knowledge/conflicts'),
        fetch('/api/v1/knowledge/claims')
      ]);

      if (ovRes.ok) setOverview(await ovRes.json());
      if (confRes.ok) setConflicts(await confRes.json());
      if (clmRes.ok) setClaims(await clmRes.json());
    } catch (err) {
      console.error('Failed to fetch Governance data:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleTestTrustedContext = async () => {
    setIsContextLoading(true);
    try {
      const res = await fetch('/api/v1/knowledge/trusted-context', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: contextQuery,
          userPermissions: ['read_restricted']
        })
      });
      if (res.ok) {
        setContextResult(await res.json());
      }
    } catch (err) {
      console.error('Trusted context generation failed:', err);
    } finally {
      setIsContextLoading(false);
    }
  };

  const handleResolveConflict = async (conflictId: string, decision: string) => {
    try {
      const res = await fetch(`/api/v1/knowledge/conflicts/${conflictId}/resolve?decision=${decision}&notes=Resolved+by+operator`, {
        method: 'POST'
      });
      if (res.ok) {
        fetchData();
      }
    } catch (err) {
      console.error('Failed to resolve conflict:', err);
    }
  };

  const handleVerifyClaim = async (claimId: string, decision: string) => {
    try {
      const res = await fetch(`/api/v1/knowledge/${claimId}/verify`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ decision, reason: 'Human operator verification' })
      });
      if (res.ok) {
        fetchData();
      }
    } catch (err) {
      console.error('Failed to verify claim:', err);
    }
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8 bg-slate-950 text-slate-100 min-h-screen">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-3">
            <ShieldCheck className="w-8 h-8 text-emerald-400" />
            <h1 className="text-3xl font-bold tracking-tight text-white">Intelligence Governance & Trusted Knowledge</h1>
          </div>
          <p className="text-slate-400 mt-1">
            Provenance, Freshness, Conflict Resolution, Citation Validation & Grounding Enforcement
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

      {/* Top Health Indicators */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="text-slate-400 text-xs font-semibold uppercase tracking-wider">Freshness Rate</div>
          <div className="flex items-center gap-2 mt-2">
            <Clock className="w-5 h-5 text-emerald-400" />
            <span className="text-xl font-bold text-white">{((overview?.freshRatio || 0.92) * 100).toFixed(1)}%</span>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="text-slate-400 text-xs font-semibold uppercase tracking-wider">Active Conflicts</div>
          <div className="flex items-center gap-2 mt-2">
            <AlertTriangle className="w-5 h-5 text-amber-400" />
            <span className="text-xl font-bold text-white">{overview?.activeConflictsCount || 1}</span>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="text-slate-400 text-xs font-semibold uppercase tracking-wider">Grounding Accuracy</div>
          <div className="flex items-center gap-2 mt-2">
            <CheckCircle className="w-5 h-5 text-cyan-400" />
            <span className="text-xl font-bold text-white">{((overview?.groundingAccuracy || 0.96) * 100).toFixed(1)}%</span>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="text-slate-400 text-xs font-semibold uppercase tracking-wider">Stale Knowledge Objects</div>
          <div className="flex items-center gap-2 mt-2">
            <Layers className="w-5 h-5 text-indigo-400" />
            <span className="text-xl font-bold text-white">{overview?.staleCount || 1}</span>
          </div>
        </div>
      </div>

      {/* Main Tabs */}
      <div className="flex border-b border-slate-800 gap-6">
        <button
          onClick={() => setActiveTab('governance')}
          className={`pb-3 text-sm font-medium border-b-2 transition ${
            activeTab === 'governance'
              ? 'border-emerald-400 text-emerald-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          Governance Dashboard
        </button>
        <button
          onClick={() => setActiveTab('conflicts')}
          className={`pb-3 text-sm font-medium border-b-2 transition ${
            activeTab === 'conflicts'
              ? 'border-emerald-400 text-emerald-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          Conflict Resolution Queue ({conflicts.length})
        </button>
        <button
          onClick={() => setActiveTab('claims')}
          className={`pb-3 text-sm font-medium border-b-2 transition ${
            activeTab === 'claims'
              ? 'border-emerald-400 text-emerald-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          Claims Verification ({claims.length})
        </button>
        <button
          onClick={() => setActiveTab('trusted_context')}
          className={`pb-3 text-sm font-medium border-b-2 transition ${
            activeTab === 'trusted_context'
              ? 'border-emerald-400 text-emerald-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          TrustedContextBuilder Simulator
        </button>
      </div>

      {/* Governance Dashboard Tab */}
      {activeTab === 'governance' && (
        <div className="space-y-6">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
            <h2 className="text-lg font-semibold text-white">Trust & Quality Indicators</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-1">
                <span className="text-xs text-slate-400 font-semibold uppercase">Authoritative Sources</span>
                <div className="text-2xl font-bold text-emerald-400">{overview?.authoritativeSourcesCount || 2}</div>
              </div>
              <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-1">
                <span className="text-xs text-slate-400 font-semibold uppercase">Unverified Claims</span>
                <div className="text-2xl font-bold text-amber-400">{overview?.unverifiedClaimsCount || 1}</div>
              </div>
              <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-1">
                <span className="text-xs text-slate-400 font-semibold uppercase">Total Tracked Objects</span>
                <div className="text-2xl font-bold text-cyan-400">{overview?.totalObjects || 12}</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Conflict Resolution Queue Tab */}
      {activeTab === 'conflicts' && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden space-y-4">
          <div className="p-4 border-b border-slate-800 font-semibold text-white flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-amber-400" />
            Active Evidence Conflicts Requiring Operator Resolution
          </div>

          <div className="divide-y divide-slate-800">
            {conflicts.map((conf) => (
              <div key={conf.id} className="p-6 space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-md font-bold text-white">Subject: {conf.subject}</span>
                  <span className={`text-xs px-2.5 py-0.5 rounded-full ${
                    conf.status === 'open' ? 'bg-amber-950 text-amber-400 border border-amber-800' : 'bg-emerald-950 text-emerald-400 border border-emerald-800'
                  }`}>
                    {conf.status.toUpperCase()}
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2">
                    <span className="text-xs text-emerald-400 font-semibold uppercase">Claim A (Source 1)</span>
                    <div className="text-sm font-medium text-white">{conf.claimA?.subject} {conf.claimA?.predicate} {conf.claimA?.object_val}</div>
                    <div className="text-xs text-slate-400">Confidence: {conf.claimA?.confidence}</div>
                  </div>

                  <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2">
                    <span className="text-xs text-amber-400 font-semibold uppercase">Claim B (Source 2)</span>
                    <div className="text-sm font-medium text-white">{conf.claimB?.subject} {conf.claimB?.predicate} {conf.claimB?.object_val}</div>
                    <div className="text-xs text-slate-400">Confidence: {conf.claimB?.confidence}</div>
                  </div>
                </div>

                {conf.status === 'open' && (
                  <div className="flex items-center gap-3 pt-2">
                    <button
                      onClick={() => handleResolveConflict(conf.id, 'accepted_a')}
                      className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-medium rounded transition"
                    >
                      Accept Claim A
                    </button>
                    <button
                      onClick={() => handleResolveConflict(conf.id, 'accepted_b')}
                      className="px-4 py-2 bg-amber-600 hover:bg-amber-500 text-white text-xs font-medium rounded transition"
                    >
                      Accept Claim B
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Claims Verification Tab */}
      {activeTab === 'claims' && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
          <div className="p-4 border-b border-slate-800 font-semibold text-white">
            Structured Claims Verification Queue
          </div>
          <div className="divide-y divide-slate-800">
            {claims.map((clm) => (
              <div key={clm.id} className="p-4 flex items-center justify-between">
                <div className="space-y-1">
                  <div className="text-sm font-medium text-white">
                    <span className="font-bold text-cyan-400">{clm.subject}</span> {clm.predicate} <span className="font-bold text-white">{clm.objectVal}</span>
                  </div>
                  <div className="text-xs text-slate-400">Confidence: {clm.confidence} | Status: {clm.status}</div>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={() => handleVerifyClaim(clm.id, 'verified')}
                    className="px-3 py-1 bg-emerald-600 hover:bg-emerald-500 text-white text-xs rounded transition flex items-center gap-1 font-medium"
                  >
                    <Check className="w-3.5 h-3.5" /> Verify
                  </button>
                  <button
                    onClick={() => handleVerifyClaim(clm.id, 'rejected')}
                    className="px-3 py-1 bg-rose-600 hover:bg-rose-500 text-white text-xs rounded transition flex items-center gap-1 font-medium"
                  >
                    <XCircle className="w-3.5 h-3.5" /> Reject
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TrustedContextBuilder Simulator Tab */}
      {activeTab === 'trusted_context' && (
        <div className="space-y-6">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
            <h2 className="text-lg font-semibold text-white flex items-center gap-2">
              <Zap className="w-5 h-5 text-emerald-400" />
              TrustedContextBuilder Pre-Generation Simulator
            </h2>
            <p className="text-slate-400 text-sm">
              Simulate pre-generation authorization, DLP gating, freshness evaluation, conflict detection, and evidence assembly.
            </p>

            <div className="flex gap-3">
              <input
                type="text"
                value={contextQuery}
                onChange={(e) => setContextQuery(e.target.value)}
                className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2.5 text-sm text-white focus:outline-none focus:border-emerald-500"
              />
              <button
                onClick={handleTestTrustedContext}
                disabled={isContextLoading}
                className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-medium rounded-lg transition"
              >
                {isContextLoading ? 'Processing...' : 'Run Pipeline'}
              </button>
            </div>
          </div>

          {contextResult && (
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
              <h3 className="text-md font-semibold text-white border-b border-slate-800 pb-2">
                Pipeline Output & Evidence Assembly
              </h3>

              {contextResult.warnings.length > 0 && (
                <div className="p-4 bg-amber-950/40 border border-amber-800/60 rounded-lg space-y-1">
                  <span className="text-xs font-semibold text-amber-400 uppercase">Pipeline Warnings & Guardrails</span>
                  {contextResult.warnings.map((w: string, idx: number) => (
                    <div key={idx} className="text-xs text-amber-200">{w}</div>
                  ))}
                </div>
              )}

              <div>
                <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Assembled Context Items ({contextResult.contextItems.length})</h4>
                <div className="space-y-2">
                  {contextResult.contextItems.map((item: any) => (
                    <div key={item.id} className="p-3 bg-slate-950 border border-slate-800 rounded-lg space-y-1">
                      <div className="flex items-center justify-between text-xs">
                        <span className="font-mono text-cyan-400">ID: {item.id}</span>
                        <span className="px-2 py-0.5 bg-slate-800 text-slate-300 rounded font-mono">{item.authority}</span>
                      </div>
                      <div className="text-sm text-white font-medium">{item.content}</div>
                      <div className="text-xs text-slate-500">Source: {item.source} | Freshness: {item.freshness}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
