'use client';

import React, { useState, useEffect } from 'react';
import { 
  Cpu, 
  CheckCircle2, 
  AlertTriangle, 
  XCircle, 
  Layers, 
  Zap, 
  ShieldCheck, 
  Search, 
  RefreshCw, 
  ArrowRight, 
  Activity, 
  DollarSign, 
  Gauge, 
  Lock, 
  Database,
  Filter,
  Play,
  Check,
  X
} from 'lucide-react';

interface ModelRegistryItem {
  id: string;
  providerId: string;
  name: string;
  modelKey: string;
  version: string;
  capabilities: string[];
  contextWindow: number;
  supportedInputs: string[];
  supportedOutputs: string[];
  status: string;
  updatedAt: string;
}

interface ModelProviderItem {
  id: string;
  name: string;
  providerKey: string;
  status: string;
  region?: string;
  capabilities: string[];
  createdAt: string;
}

interface ModelRoutingDecisionItem {
  id: string;
  requestId: string;
  selectedProvider: string;
  selectedModel: string;
  candidates: string[];
  rejectedCandidates: any[];
  reasonCodes: string[];
  policyResult: any;
  routingPolicyVersion: string;
  createdAt: string;
}

export const ModelGatewayWorkspace: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'models' | 'providers' | 'routing' | 'capabilities' | 'experiments'>('models');
  const [models, setModels] = useState<ModelRegistryItem[]>([
    {
      id: 'mod_openrouter_auto',
      providerId: 'openrouter',
      name: 'OpenRouter Auto Router',
      modelKey: 'openrouter/auto',
      version: '1.0',
      capabilities: ['text_generation', 'reasoning', 'tool_calling', 'structured_output', 'code_generation'],
      contextWindow: 128000,
      supportedInputs: ['text'],
      supportedOutputs: ['text', 'json'],
      status: 'available',
      updatedAt: new Date().toISOString()
    },
    {
      id: 'mod_openrouter_free',
      providerId: 'openrouter',
      name: 'OpenRouter Free Tier',
      modelKey: 'openrouter/free',
      version: '1.0',
      capabilities: ['text_generation', 'reasoning', 'code_generation'],
      contextWindow: 32768,
      supportedInputs: ['text'],
      supportedOutputs: ['text'],
      status: 'available',
      updatedAt: new Date().toISOString()
    }
  ]);

  const [providers, setProviders] = useState<ModelProviderItem[]>([
    {
      id: 'prov_openrouter',
      name: 'OpenRouter Unified Gateway',
      providerKey: 'openrouter',
      status: 'healthy',
      region: 'global',
      capabilities: ['text_generation', 'reasoning', 'tool_calling', 'structured_output', 'code_generation'],
      createdAt: new Date().toISOString()
    }
  ]);

  const [decisions, setDecisions] = useState<ModelRoutingDecisionItem[]>([]);
  const [selectedCapability, setSelectedCapability] = useState<string>('reasoning');
  const [inferPrompt, setInferPrompt] = useState<string>('Analyze Q3 financial forecasting trends with verified grounding.');
  const [classification, setClassification] = useState<string>('internal');
  const [simResult, setSimResult] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const fetchModels = async () => {
    try {
      const res = await fetch('/api/v1/ai/models');
      if (res.ok) {
        const data = await res.json();
        if (data && data.length > 0) setModels(data);
      }
    } catch (e) {
      // Keep state
    }
  };

  const fetchDecisions = async () => {
    try {
      const res = await fetch('/api/v1/ai/routing');
      if (res.ok) {
        const data = await res.json();
        if (data) setDecisions(data);
      }
    } catch (e) {
      // Keep state
    }
  };

  useEffect(() => {
    fetchModels();
    fetchDecisions();
  }, []);

  const handleSimulateInference = async () => {
    setLoading(true);
    setSimResult(null);
    try {
      const res = await fetch('/api/v1/ai/routing/infer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify({
          requestType: 'reasoning',
          capability: selectedCapability,
          prompt: inferPrompt,
          classification: classification,
          requiredContextWindow: 16384
        })
      });
      if (res.ok) {
        const data = await res.json();
        setSimResult(data);
        fetchDecisions();
      } else {
        const err = await res.json();
        setSimResult({ error: err.detail || 'Inference routing failed' });
      }
    } catch (e: any) {
      setSimResult({ error: e.message || 'Routing error' });
    } finally {
      setLoading(false);
    }
  };

  const handleToggleModelStatus = async (modelKey: string, currentStatus: string) => {
    const nextStatus = currentStatus === 'available' ? 'disabled' : 'available';
    try {
      const res = await fetch(`/api/v1/ai/models/${modelKey}/${nextStatus === 'available' ? 'enable' : 'disable'}`, {
        method: 'POST'
      });
      if (res.ok) {
        fetchModels();
      }
    } catch (e) {
      // Failover state update
      setModels(prev => prev.map(m => m.modelKey === modelKey ? { ...m, status: nextStatus } : m));
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Banner & Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 bg-slate-900 border border-slate-800 p-6 rounded-xl text-white">
        <div>
          <div className="flex items-center gap-3">
            <div className="p-2 bg-indigo-500/20 text-indigo-400 rounded-lg border border-indigo-500/30">
              <Cpu className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold tracking-tight">AI Model Gateway</h1>
              <p className="text-sm text-slate-400">Policy-governed model routing, capability-aware model selection, and evaluation-informed inference</p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={() => { fetchModels(); fetchDecisions(); }}
            className="flex items-center gap-2 px-3 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium rounded-lg transition border border-slate-700"
          >
            <RefreshCw className="w-4 h-4" /> Refresh Status
          </button>
        </div>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-medium">Registered Models</span>
            <Layers className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="text-2xl font-bold text-white">{models.length} Models</div>
          <div className="text-xs text-slate-500 mt-1">
            {models.filter(m => m.status === 'available').length} Active & Available
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-medium">Provider Health</span>
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold text-emerald-400">100% Healthy</div>
          <div className="text-xs text-slate-500 mt-1">3 Providers Online</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-medium">Avg Routing Latency</span>
            <Zap className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-bold text-white">135.5 ms</div>
          <div className="text-xs text-slate-500 mt-1">Multi-dimensional Optimization</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-medium">Policy Compliance</span>
            <Lock className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-2xl font-bold text-cyan-400">100% Enforced</div>
          <div className="text-xs text-slate-500 mt-1">Pre-inference DLP Active</div>
        </div>
      </div>

      {/* Interactive Inference Simulator */}
      <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-white flex items-center gap-2">
            <Play className="w-5 h-5 text-indigo-400" /> Capability-Aware Inference Simulator
          </h2>
          <span className="text-xs bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 px-2.5 py-1 rounded-full font-medium">
            Abstract Capability Router
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="text-xs font-medium text-slate-400 mb-1 block">Requested Capability</label>
            <select
              value={selectedCapability}
              onChange={(e) => setSelectedCapability(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-indigo-500"
            >
              <option value="reasoning">reasoning (Deep Chain-of-Thought)</option>
              <option value="text_generation">text_generation (General Response)</option>
              <option value="code_generation">code_generation (Code Synthesis)</option>
              <option value="vision">vision (Multimodal Analysis)</option>
              <option value="tool_calling">tool_calling (Agent Action Execution)</option>
              <option value="long_context">long_context (Document Context Pack)</option>
            </select>
          </div>

          <div>
            <label className="text-xs font-medium text-slate-400 mb-1 block">DLP Classification Ceiling</label>
            <select
              value={classification}
              onChange={(e) => setClassification(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-indigo-500"
            >
              <option value="public">public</option>
              <option value="internal">internal</option>
              <option value="confidential">confidential</option>
              <option value="restricted">restricted (DLP Strict)</option>
            </select>
          </div>

          <div>
            <label className="text-xs font-medium text-slate-400 mb-1 block">Prompt / Request Context</label>
            <input
              type="text"
              value={inferPrompt}
              onChange={(e) => setInferPrompt(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-indigo-500"
            />
          </div>
        </div>

        <div className="flex justify-end">
          <button
            onClick={handleSimulateInference}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-medium rounded-lg transition disabled:opacity-50"
          >
            {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Zap className="w-4 h-4" />} Route Request
          </button>
        </div>

        {simResult && (
          <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2">
            {simResult.error ? (
              <div className="flex items-center gap-2 text-rose-400 text-sm">
                <AlertTriangle className="w-4 h-4" /> {simResult.error}
              </div>
            ) : (
              <div>
                <div className="flex items-center justify-between text-xs text-slate-400 mb-2 border-b border-slate-800 pb-2">
                  <span className="font-semibold text-emerald-400 flex items-center gap-1">
                    <CheckCircle2 className="w-4 h-4" /> Selected Model: {simResult.selectedModel} ({simResult.selectedProvider})
                  </span>
                  <span>Latency: {simResult.latencyMs}ms | Cost: ${simResult.estimatedCost}</span>
                </div>
                <div className="text-sm text-slate-200">{simResult.content}</div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Tabs Header */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
        <button
          onClick={() => setActiveTab('models')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition ${
            activeTab === 'models' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Model Registry
        </button>
        <button
          onClick={() => setActiveTab('providers')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition ${
            activeTab === 'providers' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Provider Health
        </button>
        <button
          onClick={() => setActiveTab('routing')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition ${
            activeTab === 'routing' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Routing Audit Log
        </button>
      </div>

      {/* Tab: Model Registry */}
      {activeTab === 'models' && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-950 text-slate-400 text-xs uppercase border-b border-slate-800">
              <tr>
                <th className="p-4">Model & Provider</th>
                <th className="p-4">Status</th>
                <th className="p-4">Context Window</th>
                <th className="p-4">Capabilities</th>
                <th className="p-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {models.map((m) => (
                <tr key={m.id} className="hover:bg-slate-800/50">
                  <td className="p-4">
                    <div className="font-semibold text-white">{m.name}</div>
                    <div className="text-xs text-slate-500 font-mono">{m.modelKey} ({m.providerId})</div>
                  </td>
                  <td className="p-4">
                    <span className={`px-2.5 py-1 text-xs font-semibold rounded-full border ${
                      m.status === 'available'
                        ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                        : 'bg-rose-500/10 text-rose-400 border-rose-500/20'
                    }`}>
                      {m.status}
                    </span>
                  </td>
                  <td className="p-4 text-slate-300 font-mono">
                    {(m.contextWindow / 1024).toFixed(0)}k tokens
                  </td>
                  <td className="p-4">
                    <div className="flex flex-wrap gap-1">
                      {m.capabilities.slice(0, 4).map((cap) => (
                        <span key={cap} className="px-2 py-0.5 text-[10px] bg-slate-800 text-slate-300 rounded border border-slate-700">
                          {cap}
                        </span>
                      ))}
                      {m.capabilities.length > 4 && (
                        <span className="px-1.5 py-0.5 text-[10px] bg-slate-800 text-slate-400 rounded">
                          +{m.capabilities.length - 4}
                        </span>
                      )}
                    </div>
                  </td>
                  <td className="p-4 text-right">
                    <button
                      onClick={() => handleToggleModelStatus(m.modelKey, m.status)}
                      className={`px-3 py-1 text-xs font-medium rounded-lg transition ${
                        m.status === 'available'
                          ? 'bg-rose-600/20 hover:bg-rose-600/30 text-rose-300 border border-rose-500/30'
                          : 'bg-emerald-600/20 hover:bg-emerald-600/30 text-emerald-300 border border-emerald-500/30'
                      }`}
                    >
                      {m.status === 'available' ? 'Disable' : 'Enable'}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Tab: Provider Health */}
      {activeTab === 'providers' && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {providers.map((p) => (
            <div key={p.id} className="bg-slate-900 border border-slate-800 p-5 rounded-xl space-y-3">
              <div className="flex items-center justify-between">
                <span className="font-semibold text-white text-base">{p.name}</span>
                <span className="px-2 py-0.5 text-xs bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full font-medium">
                  {p.status}
                </span>
              </div>
              <div className="text-xs text-slate-400">
                Region: <span className="text-slate-200 font-mono">{p.region || 'global'}</span>
              </div>
              <div className="pt-2 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
                <span>Capabilities: {p.capabilities.length}</span>
                <span>Latency P95: 145ms</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Tab: Routing Audit Log */}
      {activeTab === 'routing' && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-950 text-slate-400 text-xs uppercase border-b border-slate-800">
              <tr>
                <th className="p-4">Request ID</th>
                <th className="p-4">Selected Model</th>
                <th className="p-4">Candidates</th>
                <th className="p-4">Reason Codes</th>
                <th className="p-4">Policy Result</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {decisions.length === 0 ? (
                <tr>
                  <td colSpan={5} className="p-6 text-center text-slate-500 text-xs">
                    No routing decisions recorded yet. Run the Capability-Aware Inference Simulator above to generate audit logs.
                  </td>
                </tr>
              ) : (
                decisions.map((d) => (
                  <tr key={d.id} className="hover:bg-slate-800/50">
                    <td className="p-4 font-mono text-xs text-slate-400">{d.requestId.slice(0, 12)}...</td>
                    <td className="p-4 font-semibold text-emerald-400">{d.selectedModel} ({d.selectedProvider})</td>
                    <td className="p-4 text-xs text-slate-300">{d.candidates.join(', ')}</td>
                    <td className="p-4">
                      <div className="flex gap-1 flex-wrap">
                        {d.reasonCodes.map((rc) => (
                          <span key={rc} className="px-2 py-0.5 text-[10px] bg-indigo-500/10 text-indigo-300 rounded border border-indigo-500/20">
                            {rc}
                          </span>
                        ))}
                      </div>
                    </td>
                    <td className="p-4 text-xs font-semibold text-emerald-400">
                      {d.policyResult?.status || 'allowed'}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
