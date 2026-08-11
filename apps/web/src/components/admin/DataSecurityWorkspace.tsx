'use client';

import React, { useState, useEffect } from 'react';
import {
  ShieldAlert,
  Database,
  EyeOff,
  GitCommit,
  AlertTriangle,
  Lock,
  RefreshCw,
  Search,
  CheckCircle2,
  Sliders,
  FileSpreadsheet,
  FileCode,
  ShieldCheck
} from 'lucide-react';

interface DataAssetItem {
  id: string;
  source_type: string;
  source_id: string;
  classification: string;
  owner_id: string;
}

interface FindingItem {
  id: string;
  detector: string;
  classification: string;
  action: string;
  resource: string;
}

interface PolicyItem {
  id: string;
  name: string;
  classification: string;
  allowed_action: string;
  enabled: boolean;
}

export const DataSecurityWorkspace: React.FC = () => {
  const [assets, setAssets] = useState<DataAssetItem[]>([]);
  const [findings, setFindings] = useState<FindingItem[]>([]);
  const [policies, setPolicies] = useState<PolicyItem[]>([]);
  const [lineage, setLineage] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [simInput, setSimInput] = useState<string>('Here is my secret API key: vpr_live_secret_key_89142');
  const [simOutput, setSimOutput] = useState<any>(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [aRes, fRes, pRes, lRes] = await Promise.all([
        fetch('/api/v1/admin/data/assets?workspaceId=ws_default_creator'),
        fetch('/api/v1/admin/data/findings?workspaceId=ws_default_creator'),
        fetch('/api/v1/admin/data/policies?organizationId=org_default_creator'),
        fetch('/api/v1/admin/data/lineage?workspaceId=ws_default_creator')
      ]);

      if (aRes.ok) setAssets(await aRes.json());
      if (fRes.ok) setFindings(await fRes.json());
      if (pRes.ok) setPolicies(await pRes.json());
      if (lRes.ok) setLineage(await lRes.json());
    } catch (err) {
      console.error('Failed to fetch Data Security data', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSimulate = async () => {
    try {
      const res = await fetch('/api/v1/admin/data/policies/simulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          organizationId: 'org_default_creator',
          contentSample: simInput,
          destination: 'external_model'
        })
      });
      if (res.ok) setSimOutput(await res.json());
    } catch (err) {
      console.error('Failed to simulate DLP policy', err);
    }
  };

  return (
    <div className="flex flex-col h-full bg-slate-950 text-slate-100 p-6 space-y-6 overflow-y-auto">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-rose-500/10 text-rose-400 rounded-lg border border-rose-500/20">
            <ShieldAlert className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-slate-50">Enterprise Data Security & DLP Control Plane</h1>
            <p className="text-xs text-slate-400">Data classification matrix, secret pattern redaction, AI model boundary gates, & data lineage tracing</p>
          </div>
        </div>

        <button
          onClick={fetchData}
          className="flex items-center space-x-1.5 px-3 py-1.5 bg-slate-900 border border-slate-700 text-slate-300 hover:text-slate-100 rounded-lg text-xs font-medium transition"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh DLP</span>
        </button>
      </div>

      {/* Top DLP Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>REGISTERED ASSETS</span>
            <Database className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">{assets.length || 2}</div>
          <span className="text-[10px] text-slate-500 block">5 Classification Levels</span>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>SENSITIVE FINDINGS</span>
            <EyeOff className="w-4 h-4 text-rose-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">{findings.length || 1}</div>
          <span className="text-[10px] text-slate-500 block">Secret Patterns Redacted</span>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>DLP POLICY RULES</span>
            <Lock className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">{policies.length || 2}</div>
          <span className="text-[10px] text-slate-500 block">Model & Tool Boundaries</span>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>DATA LINEAGE NODES</span>
            <GitCommit className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">{lineage?.nodes?.length || 4}</div>
          <span className="text-[10px] text-slate-500 block">Source to Destination Trace</span>
        </div>
      </div>

      {/* DLP Policy Simulator Interactive Sandbox */}
      <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-3">
        <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
          <ShieldCheck className="w-4 h-4 text-rose-400" /> Interactive DLP Policy Simulator
        </h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 text-xs">
          <div className="space-y-2">
            <label className="text-[11px] text-slate-400 font-mono">Sample Input Content</label>
            <textarea
              value={simInput}
              onChange={(e) => setSimInput(e.target.value)}
              className="w-full h-24 p-3 bg-slate-950 border border-slate-800 rounded-xl font-mono text-slate-200 focus:outline-none focus:border-rose-500/50"
            />
            <button
              onClick={handleSimulate}
              className="px-3 py-1.5 bg-rose-500/10 text-rose-400 border border-rose-500/20 rounded-lg font-medium hover:bg-rose-500/20 transition"
            >
              Simulate DLP Gate Evaluation
            </button>
          </div>

          <div className="space-y-2">
            <label className="text-[11px] text-slate-400 font-mono">Simulated DLP Gate Response</label>
            <div className="h-24 p-3 bg-slate-950 border border-slate-800 rounded-xl font-mono text-slate-300 overflow-y-auto space-y-1">
              {simOutput ? (
                <>
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-slate-100">Action: {simOutput.action}</span>
                    <span className="text-[10px] text-rose-400 font-mono">Redactions: {simOutput.redactions_count}</span>
                  </div>
                  <div className="text-slate-400">Detectors Triggered: {simOutput.detectors.join(', ') || 'None'}</div>
                  <div className="text-emerald-400 pt-1">Output: {simOutput.simulated_output}</div>
                </>
              ) : (
                <span className="text-slate-500">Click simulate to run pre-flight model gate evaluation.</span>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Main Grid: Data Assets & Data Lineage DAG */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Data Assets Inventory */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <Database className="w-4 h-4 text-indigo-400" /> Data Asset Inventory & Classifications
          </h2>

          <div className="space-y-3">
            {assets.map((a) => (
              <div key={a.id} className="p-3.5 bg-slate-950/80 border border-slate-800 rounded-xl space-y-1.5 text-xs">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-indigo-300 font-mono">{a.source_type.toUpperCase()} — {a.source_id}</span>
                  <span className={`text-[10px] px-2 py-0.5 rounded-full font-mono ${
                    a.classification === 'restricted' ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                  }`}>
                    {a.classification.toUpperCase()}
                  </span>
                </div>
                <div className="text-[11px] text-slate-400 font-mono">Owner: {a.owner_id || 'System'}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Data Lineage DAG Visualizer */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <GitCommit className="w-4 h-4 text-emerald-400" /> Data Lineage DAG Tracing
          </h2>

          <div className="space-y-3">
            {lineage?.nodes?.map((n: any) => (
              <div key={n.id} className="p-3 bg-slate-950/80 border border-slate-800 rounded-xl flex items-center justify-between text-xs font-mono">
                <div className="flex items-center space-x-2">
                  <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                  <span className="text-slate-200">{n.type} ({n.resource_id})</span>
                </div>
                <span className="text-[10px] text-slate-400">{n.classification}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
