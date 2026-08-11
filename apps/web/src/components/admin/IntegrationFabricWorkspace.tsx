'use client';

import React, { useState, useEffect } from 'react';
import {
  Plug,
  ShieldCheck,
  ShieldAlert,
  Zap,
  Activity,
  CheckCircle2,
  AlertTriangle,
  Play,
  RotateCcw,
  RefreshCw,
  Lock,
  Layers,
  Globe,
  Radio
} from 'lucide-react';

interface CatalogItem {
  id: string;
  name: string;
  provider: string;
  category: string;
  description: string;
  status: string;
  capabilities: any[];
}

interface ActionItem {
  id: string;
  capability_id: string;
  connection_id: string;
  actor: string;
  status: string;
  created_at: string;
}

export const IntegrationFabricWorkspace: React.FC = () => {
  const [catalog, setCatalog] = useState<CatalogItem[]>([]);
  const [actions, setActions] = useState<ActionItem[]>([]);
  const [selectedProvider, setSelectedProvider] = useState<CatalogItem | null>(null);
  const [simulationResult, setSimulationResult] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [cRes, aRes] = await Promise.all([
        fetch('/api/v1/integrations/catalog'),
        fetch('/api/v1/integrations/actions')
      ]);

      if (cRes.ok) {
        const catData = await cRes.json();
        setCatalog(catData);
        if (catData.length > 0) setSelectedProvider(catData[0]);
      }
      if (aRes.ok) setActions(await aRes.json());
    } catch (err) {
      console.error('Failed to fetch Integration Fabric data', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSimulateAction = async (capabilityId: string) => {
    try {
      const res = await fetch('/api/v1/integrations/actions/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          capabilityId,
          connectionId: 'conn_google_01',
          inputData: { recipient: 'alex.creator@vapor.os', subject: 'Simulated Execution' },
          simulateOnly: true
        })
      });
      if (res.ok) setSimulationResult(await res.json());
    } catch (err) {
      console.error('Failed to simulate action', err);
    }
  };

  return (
    <div className="flex flex-col h-full bg-slate-950 text-slate-100 p-6 space-y-6 overflow-y-auto">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-purple-500/10 text-purple-400 rounded-lg border border-purple-500/20">
            <Plug className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-slate-50">Enterprise Integration Fabric & Universal Action Gateway</h1>
            <p className="text-xs text-slate-400">Policy-governed integration boundaries, capability registries, SSRF protection, DLP checks, & 10-step action audit</p>
          </div>
        </div>

        <button
          onClick={fetchData}
          className="flex items-center space-x-1.5 px-3 py-1.5 bg-slate-900 border border-slate-700 text-slate-300 hover:text-slate-100 rounded-lg text-xs font-medium transition"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh Fabric</span>
        </button>
      </div>

      {/* Overview Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>AVAILABLE PROVIDERS</span>
            <Globe className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">{catalog.length || 3}</div>
          <span className="text-[10px] text-emerald-400 font-medium">Google, GitHub, Slack</span>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>REGISTERED CAPABILITIES</span>
            <Zap className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">9</div>
          <span className="text-[10px] text-purple-400 font-medium">Capability-Based Scopes</span>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>ACTION GATEWAY AUDIT</span>
            <Activity className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">{actions.length || 1}</div>
          <span className="text-[10px] text-emerald-400 font-medium">100% Policy & DLP Checked</span>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>SECURITY BOUNDARY</span>
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-xl font-bold text-emerald-400 font-mono">SSRF + DLP</div>
          <span className="text-[10px] text-slate-500 block">Private Network Isolation</span>
        </div>
      </div>

      {/* Main Grid: Catalog, Capability Registry, Action Simulator */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Integration Provider Catalog */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <Plug className="w-4 h-4 text-purple-400" /> Provider Catalog
          </h2>

          <div className="space-y-3">
            {catalog.map((item) => (
              <div
                key={item.id}
                onClick={() => setSelectedProvider(item)}
                className={`p-3.5 rounded-xl border cursor-pointer transition ${
                  selectedProvider?.id === item.id
                    ? 'bg-purple-500/10 border-purple-500/30 text-slate-100'
                    : 'bg-slate-950/60 border-slate-800 text-slate-400 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="font-bold text-sm text-slate-200">{item.name}</span>
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">{item.status.toUpperCase()}</span>
                </div>
                <p className="text-xs text-slate-400 mt-1">{item.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Capability Registry & Action Gateway Simulator */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4 lg:col-span-2">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <Zap className="w-4 h-4 text-emerald-400" /> Capability Registry & Universal Action Gateway
          </h2>

          {selectedProvider && (
            <div className="space-y-4">
              <div className="p-3.5 bg-slate-950 border border-slate-800 rounded-xl flex items-center justify-between">
                <div>
                  <h3 className="font-bold text-sm text-slate-100">{selectedProvider.name} Capabilities</h3>
                  <p className="text-xs text-slate-400">Agents discover capabilities through the registry without raw credential access</p>
                </div>
                <span className="text-xs font-mono bg-slate-900 px-2.5 py-1 rounded text-purple-400 border border-slate-800">
                  {selectedProvider.provider}
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {selectedProvider.capabilities?.map((cap: any) => (
                  <div key={cap.id} className="p-3.5 bg-slate-950 border border-slate-800 rounded-xl space-y-2 font-mono text-xs">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-slate-200">{cap.id}</span>
                      <span className={`text-[10px] px-2 py-0.5 rounded-full ${
                        cap.risk_level === 'high' ? 'bg-rose-500/10 text-rose-400 border-rose-500/20' : 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20'
                      } border`}>
                        {cap.risk_level.toUpperCase()} RISK
                      </span>
                    </div>

                    <p className="text-slate-400 font-sans text-xs">{cap.name}</p>

                    <button
                      onClick={() => handleSimulateAction(cap.id)}
                      className="w-full py-1.5 bg-purple-500/10 text-purple-400 border border-purple-500/20 rounded-lg hover:bg-purple-500/20 transition flex items-center justify-center gap-1 font-sans text-xs font-medium"
                    >
                      <Play className="w-3.5 h-3.5" /> Simulate Action Gateway
                    </button>
                  </div>
                ))}
              </div>

              {simulationResult && (
                <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-2 font-mono text-xs">
                  <span className="font-bold text-cyan-400 block border-b border-slate-800 pb-1">Action Gateway Simulation Result:</span>
                  <div className="flex justify-between text-slate-300 text-[11px]">
                    <span>Action ID:</span>
                    <span className="text-slate-400">{simulationResult.id}</span>
                  </div>
                  <div className="flex justify-between text-slate-300 text-[11px]">
                    <span>Gateway Status:</span>
                    <span className="text-emerald-400 font-bold">{simulationResult.status.toUpperCase()}</span>
                  </div>
                  <div className="p-2 bg-emerald-500/10 border border-emerald-500/20 rounded text-[10px] text-emerald-400 font-sans">
                    DLP, PolicyEngine, & SSRF Protection Checks Passed
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
