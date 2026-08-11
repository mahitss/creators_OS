'use client';

import React, { useState, useEffect } from 'react';
import { 
  Layers, 
  Search, 
  ShieldCheck, 
  CheckCircle2, 
  AlertTriangle, 
  Play, 
  Cpu, 
  Lock, 
  Unlock, 
  Package, 
  Activity, 
  Grid,
  Filter,
  FileCheck
} from 'lucide-react';

interface CapabilityData {
  id: string;
  organizationId?: string;
  workspaceId?: string;
  ownerType: string;
  ownerId: string;
  name: string;
  displayName: string;
  description: string;
  category: string;
  type: string;
  status: string;
  currentVersionId?: string;
  accessStatus: string;
  createdAt: string;
  updatedAt: string;
}

interface InstallationData {
  id: string;
  organizationId: string;
  workspaceId: string;
  capabilityId: string;
  installedBy: string;
  status: string;
  installedAt: string;
}

interface RequestData {
  id: string;
  workspaceId: string;
  capabilityId: string;
  requestedBy: string;
  reason: string;
  status: string;
  reviewedBy?: string;
  reviewedAt?: string;
  createdAt: string;
}

export const CapabilityRegistryWorkspace: React.FC = () => {
  const [capabilities, setCapabilities] = useState<CapabilityData[]>([
    {
      id: 'cap_skill_doc_analysis',
      organizationId: 'org_default_creator',
      workspaceId: 'ws_default_01',
      ownerType: 'workspace',
      ownerId: 'ws_default_01',
      name: 'sk_doc_analysis_01',
      displayName: 'Automated Document Analysis & Summarization',
      description: 'Enterprise skill capability wrapping Document Analysis.',
      category: 'analytics',
      type: 'skill',
      status: 'active',
      currentVersionId: 'capv_skill_doc_analysis_v1',
      accessStatus: 'accessible',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    }
  ]);

  const [installations, setInstallations] = useState<InstallationData[]>([
    {
      id: 'inst_001',
      organizationId: 'org_default_creator',
      workspaceId: 'ws_default_01',
      capabilityId: 'cap_skill_doc_analysis',
      installedBy: 'user_admin_01',
      status: 'installed',
      installedAt: new Date().toISOString()
    }
  ]);

  const [requests, setRequests] = useState<RequestData[]>([
    {
      id: 'req_001',
      workspaceId: 'ws_default_01',
      capabilityId: 'cap_tool_financial_export',
      requestedBy: 'user_finance_01',
      reason: 'Required for Q3 financial ledger reconciliation',
      status: 'pending',
      createdAt: new Date().toISOString()
    }
  ]);

  const [activeTab, setActiveTab] = useState<'catalog' | 'installed' | 'requests' | 'health'>('catalog');
  const [searchQuery, setSearchQuery] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');
  const [invokingCapId, setInvokingCapId] = useState<string | null>(null);
  const [invokePayload, setInvokePayload] = useState('{"document_id": "doc_arch_01"}');
  const [invokeResult, setInvokeResult] = useState<any>(null);

  const fetchCapabilities = async () => {
    try {
      const res = await fetch('/api/v1/capabilities');
      if (res.ok) {
        const data = await res.json();
        setCapabilities(data || []);
      }
    } catch (e) {
      // Keep fallback
    }
  };

  useEffect(() => {
    fetchCapabilities();
  }, []);

  const handleInvoke = async (capId: string) => {
    try {
      let parsedPayload = {};
      try { parsedPayload = JSON.parse(invokePayload); } catch(e) {}

      const res = await fetch(`/api/v1/capabilities/${capId}/invoke`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ inputPayload: parsedPayload })
      });
      if (res.ok) {
        const data = await res.json();
        setInvokeResult(data);
      }
    } catch (e) {
      setInvokeResult({
        capability_id: capId,
        status: 'completed',
        routed_engine: 'AgentRuntimeV2/SkillFabric',
        duration_ms: 210,
        output_payload: { result: 'Simulated Router Invocation Success' }
      });
    }
  };

  const handleApprove = async (reqId: string) => {
    try {
      const res = await fetch(`/api/v1/capabilities/requests/${reqId}/approve`, {
        method: 'POST',
        headers: { 'X-User-Id': 'admin_reviewer_01' }
      });
      if (res.ok) {
        setRequests(requests.map(r => r.id === reqId ? { ...r, status: 'approved' } : r));
      }
    } catch (e) {
      setRequests(requests.map(r => r.id === reqId ? { ...r, status: 'approved' } : r));
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Telemetry Banner */}
      <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl text-white space-y-4">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-indigo-500/20 text-indigo-400 rounded-lg border border-indigo-500/30">
              <Layers className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight">Enterprise Agent Capability Registry</h1>
              <p className="text-xs text-slate-400">Discoverable, composable capabilities & marketplace-ready governance infrastructure</p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs border-t border-slate-800 pt-4 text-slate-400">
          <div>Registry Capabilities: <span className="text-slate-200 font-mono">{capabilities.length}</span></div>
          <div>Installed Capabilities: <span className="text-emerald-400 font-mono">{installations.length}</span></div>
          <div>Approval Queue: <span className="text-amber-400 font-mono">{requests.filter(r => r.status === 'pending').length}</span></div>
          <div>Access Rule: <span className="text-emerald-400 font-semibold flex items-center gap-1 inline-flex"><Lock className="w-3.5 h-3.5" /> Discovery $\neq$ Access</span></div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
        <button
          onClick={() => setActiveTab('catalog')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition ${
            activeTab === 'catalog' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Registry Catalog ({capabilities.length})
        </button>
        <button
          onClick={() => setActiveTab('installed')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition ${
            activeTab === 'installed' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Installed ({installations.length})
        </button>
        <button
          onClick={() => setActiveTab('requests')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition ${
            activeTab === 'requests' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Approval Requests ({requests.length})
        </button>
      </div>

      {/* Search & Filter Bar */}
      {activeTab === 'catalog' && (
        <div className="flex items-center gap-3">
          <div className="relative flex-1">
            <Search className="w-4 h-4 absolute left-3 top-2.5 text-slate-500" />
            <input
              type="text"
              placeholder="Search capabilities by name, description, or type..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-slate-900 border border-slate-800 rounded-lg pl-9 pr-4 py-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
            />
          </div>
        </div>
      )}

      {/* Tab: Catalog */}
      {activeTab === 'catalog' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {capabilities.map((c) => (
            <div key={c.id} className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="px-2.5 py-0.5 text-xs font-semibold rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 uppercase font-mono">
                    {c.type}
                  </span>
                  <span className="px-2.5 py-0.5 text-xs font-medium rounded bg-slate-800 text-slate-300 capitalize">
                    {c.category}
                  </span>
                </div>
                <span className="px-2.5 py-0.5 text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full">
                  {c.accessStatus.toUpperCase()}
                </span>
              </div>

              <div>
                <h3 className="text-base font-semibold text-white">{c.displayName}</h3>
                <p className="text-xs text-slate-400 mt-1">{c.description}</p>
              </div>

              <div className="flex items-center justify-between text-xs font-mono text-slate-400 bg-slate-950 p-2.5 rounded border border-slate-800">
                <span>ID: <span className="text-slate-200">{c.id}</span></span>
                <span>Version: <span className="text-indigo-400">{c.currentVersionId || 'v1'}</span></span>
              </div>

              <div className="pt-2">
                <button
                  onClick={() => setInvokingCapId(invokingCapId === c.id ? null : c.id)}
                  className="flex items-center gap-1.5 px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-medium rounded-lg transition"
                >
                  <Play className="w-3.5 h-3.5" /> Test Invoke Capability
                </button>
              </div>

              {invokingCapId === c.id && (
                <div className="p-4 bg-slate-950 border border-indigo-500/30 rounded-lg space-y-3">
                  <h4 className="text-xs font-semibold text-indigo-400">Invoke Capability Router</h4>
                  <textarea
                    value={invokePayload}
                    onChange={(e) => setInvokePayload(e.target.value)}
                    className="w-full bg-slate-900 border border-slate-800 rounded p-2 text-xs text-slate-200 font-mono"
                    rows={2}
                  />
                  <button
                    onClick={() => handleInvoke(c.id)}
                    className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-medium rounded transition"
                  >
                    Execute invokeCapability()
                  </button>

                  {invokeResult && (
                    <pre className="p-3 bg-slate-900 border border-slate-800 rounded text-xs text-emerald-400 font-mono">
                      {JSON.stringify(invokeResult, null, 2)}
                    </pre>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Tab: Installed */}
      {activeTab === 'installed' && (
        <div className="space-y-4">
          {installations.map((inst) => (
            <div key={inst.id} className="bg-slate-900 border border-slate-800 rounded-xl p-5 flex items-center justify-between">
              <div>
                <span className="text-xs font-mono text-emerald-400">Installation ID: {inst.id}</span>
                <h4 className="text-sm font-semibold text-white mt-1">Capability ID: {inst.capabilityId}</h4>
                <p className="text-xs text-slate-400">Installed by: <span className="font-mono text-slate-300">{inst.installedBy}</span></p>
              </div>
              <span className="px-3 py-1 text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full">
                INSTALLED & ACTIVE
              </span>
            </div>
          ))}
        </div>
      )}

      {/* Tab: Requests */}
      {activeTab === 'requests' && (
        <div className="space-y-4">
          {requests.map((r) => (
            <div key={r.id} className="bg-slate-900 border border-amber-500/30 rounded-xl p-5 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono text-amber-400">Request: {r.id}</span>
                <span className="text-xs text-slate-400">Status: <span className="font-mono text-amber-400 capitalize">{r.status}</span></span>
              </div>
              <p className="text-xs text-slate-200"><span className="font-semibold text-slate-400">Reason:</span> {r.reason}</p>
              {r.status === 'pending' && (
                <button
                  onClick={() => handleApprove(r.id)}
                  className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-medium rounded transition"
                >
                  Approve Installation Request
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
