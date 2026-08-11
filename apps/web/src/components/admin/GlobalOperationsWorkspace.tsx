'use client';

import React, { useState, useEffect } from 'react';
import { 
  Activity, 
  Shield, 
  AlertTriangle, 
  Layers, 
  RefreshCw, 
  Zap, 
  Cpu, 
  CheckCircle, 
  Lock, 
  Terminal, 
  DollarSign, 
  Brain, 
  Play, 
  Pause, 
  XCircle, 
  Check, 
  MessageSquare,
  Network
} from 'lucide-react';

interface OperationsOverview {
  systemStatus: string;
  activeIncidentsCount: number;
  workflowHealth: string;
  agentHealth: string;
  integrationHealth: string;
  securityHealth: string;
  costHealth: string;
  eventHealth: string;
  contributingSignals: any[];
  lastUpdated: string;
}

interface ServiceNode {
  id: string;
  name: string;
  category: string;
  status: string;
  dependencies: string[];
  latencyMs: number;
  errorRate: number;
  throughputQps: number;
}

interface ControlAction {
  id: string;
  actionType: string;
  targetResource: string;
  requestedBy: string;
  reason: string;
  riskLevel: string;
  status: string;
  createdAt: string;
  completedAt?: string;
}

export const GlobalOperationsWorkspace: React.FC = () => {
  const [overview, setOverview] = useState<OperationsOverview | null>(null);
  const [services, setServices] = useState<ServiceNode[]>([]);
  const [actions, setActions] = useState<ControlAction[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'overview' | 'services' | 'actions' | 'assistant'>('overview');

  // Control Action Form state
  const [actionType, setActionType] = useState('pause_service');
  const [targetResource, setTargetResource] = useState('sys_integration_fabric');
  const [reason, setReason] = useState('Operator maintenance isolation');
  const [riskLevel, setRiskLevel] = useState('medium');

  // AI Assistant Query state
  const [aiQuery, setAiQuery] = useState('');
  const [aiResponse, setAiResponse] = useState<any>(null);
  const [isAiLoading, setIsAiLoading] = useState(false);

  const fetchData = async () => {
    setIsLoading(true);
    try {
      const [ovRes, srvRes, actRes] = await Promise.all([
        fetch('/api/v1/operations/overview'),
        fetch('/api/v1/operations/services'),
        fetch('/api/v1/operations/actions')
      ]);

      if (ovRes.ok) setOverview(await ovRes.json());
      if (srvRes.ok) setServices(await srvRes.json());
      if (actRes.ok) setActions(await actRes.json());
    } catch (err) {
      console.error('Failed to fetch Operations telemetry:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleRequestAction = async () => {
    try {
      const res = await fetch('/api/v1/operations/actions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-User-Id': 'usr_executive_01'
        },
        body: JSON.stringify({
          actionType,
          targetResource,
          reason,
          riskLevel
        })
      });
      if (res.ok) {
        fetchData();
      }
    } catch (err) {
      console.error('Failed to request control action:', err);
    }
  };

  const handleApproveAction = async (actionId: string) => {
    try {
      const res = await fetch(`/api/v1/operations/actions/${actionId}/approve`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-User-Id': 'usr_approver_02' // Different user for 2-person approval requirement
        },
        body: JSON.stringify({ comments: 'Approved by second operator' })
      });
      if (res.ok) {
        fetchData();
      }
    } catch (err) {
      console.error('Failed to approve action:', err);
    }
  };

  const handleAiQuerySubmit = async () => {
    if (!aiQuery.trim()) return;
    setIsAiLoading(true);
    try {
      const res = await fetch('/api/v1/operations/ai-query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: aiQuery })
      });
      if (res.ok) {
        setAiResponse(await res.json());
      }
    } catch (err) {
      console.error('AI Operations query failed:', err);
    } finally {
      setIsAiLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8 bg-slate-950 text-slate-100 min-h-screen">
      {/* Top Operations Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-3">
            <Activity className="w-8 h-8 text-emerald-400" />
            <h1 className="text-3xl font-bold tracking-tight text-white">Global Operations Center</h1>
          </div>
          <p className="text-slate-400 mt-1">
            Enterprise Control Plane — Aggregate Telemetry & Policy-Governed Operational Control
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

      {/* Top Executive Health Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="text-slate-400 text-xs font-semibold uppercase tracking-wider">Overall System Health</div>
          <div className="flex items-center gap-2 mt-2">
            <CheckCircle className="w-5 h-5 text-emerald-400" />
            <span className="text-xl font-bold text-white uppercase">{overview?.systemStatus || 'Healthy'}</span>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="text-slate-400 text-xs font-semibold uppercase tracking-wider">Active Incidents</div>
          <div className="flex items-center gap-2 mt-2">
            <AlertTriangle className="w-5 h-5 text-amber-400" />
            <span className="text-xl font-bold text-white">{overview?.activeIncidentsCount || 0}</span>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="text-slate-400 text-xs font-semibold uppercase tracking-wider">Security & DLP Boundary</div>
          <div className="flex items-center gap-2 mt-2">
            <Shield className="w-5 h-5 text-indigo-400" />
            <span className="text-xl font-bold text-white uppercase">{overview?.securityHealth || 'Healthy'}</span>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="text-slate-400 text-xs font-semibold uppercase tracking-wider">FinOps & Infra Cost</div>
          <div className="flex items-center gap-2 mt-2">
            <DollarSign className="w-5 h-5 text-emerald-400" />
            <span className="text-xl font-bold text-white uppercase">{overview?.costHealth || 'Healthy'}</span>
          </div>
        </div>
      </div>

      {/* Main Tabs */}
      <div className="flex border-b border-slate-800 gap-6">
        <button
          onClick={() => setActiveTab('overview')}
          className={`pb-3 text-sm font-medium border-b-2 transition ${
            activeTab === 'overview'
              ? 'border-emerald-400 text-emerald-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          Operations Overview
        </button>
        <button
          onClick={() => setActiveTab('services')}
          className={`pb-3 text-sm font-medium border-b-2 transition ${
            activeTab === 'services'
              ? 'border-emerald-400 text-emerald-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          Service Dependency Map ({services.length})
        </button>
        <button
          onClick={() => setActiveTab('actions')}
          className={`pb-3 text-sm font-medium border-b-2 transition ${
            activeTab === 'actions'
              ? 'border-emerald-400 text-emerald-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          Control Action Gateway ({actions.length})
        </button>
        <button
          onClick={() => setActiveTab('assistant')}
          className={`pb-3 text-sm font-medium border-b-2 transition ${
            activeTab === 'assistant'
              ? 'border-emerald-400 text-emerald-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          AI Operations Assistant
        </button>
      </div>

      {/* Overview Tab */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <h2 className="text-lg font-semibold text-white mb-4">Contributing Telemetry Signals</h2>
            <div className="divide-y divide-slate-800">
              {overview?.contributingSignals.map((sig, idx) => (
                <div key={idx} className="py-3 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className="text-xs font-mono bg-slate-800 text-slate-300 px-2 py-0.5 rounded">
                      {sig.source}
                    </span>
                    <span className="text-sm font-medium text-slate-200">{sig.metric}</span>
                  </div>
                  <div className="flex items-center gap-4">
                    <span className="text-sm font-bold text-white">{sig.value}</span>
                    <span className="text-xs px-2.5 py-0.5 bg-emerald-950 border border-emerald-800 text-emerald-400 rounded-full">
                      {sig.status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Services Dependency Map Tab */}
      {activeTab === 'services' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {services.map((srv) => (
            <div key={srv.id} className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Cpu className="w-5 h-5 text-emerald-400" />
                  <h3 className="font-semibold text-white">{srv.name}</h3>
                </div>
                <span className="text-xs px-2.5 py-0.5 bg-emerald-950 border border-emerald-800 text-emerald-400 rounded-full font-mono">
                  {srv.status}
                </span>
              </div>

              <div className="grid grid-cols-3 gap-2 text-xs text-slate-300 pt-2 border-t border-slate-800">
                <div><span className="text-slate-500">Latency:</span> {srv.latencyMs} ms</div>
                <div><span className="text-slate-500">Error Rate:</span> {(srv.errorRate * 100).toFixed(2)}%</div>
                <div><span className="text-slate-500">Throughput:</span> {srv.throughputQps} QPS</div>
              </div>

              {srv.dependencies.length > 0 && (
                <div className="text-xs text-slate-400 pt-2 flex items-center gap-2">
                  <Network className="w-3.5 h-3.5 text-slate-500" />
                  Dependencies: <span className="font-mono text-slate-300">{srv.dependencies.join(', ')}</span>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Control Action Gateway Tab */}
      {activeTab === 'actions' && (
        <div className="space-y-6">
          {/* Action Request Form */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
              <Lock className="w-5 h-5 text-amber-400" />
              Control Action Gateway Dispatcher
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div>
                <label className="text-xs font-medium text-slate-400">Action Type</label>
                <select
                  value={actionType}
                  onChange={(e) => setActionType(e.target.value)}
                  className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-emerald-500"
                >
                  <option value="pause_service">pause_service</option>
                  <option value="resume_service">resume_service</option>
                  <option value="disable_agent">disable_agent</option>
                  <option value="cancel_workflow">cancel_workflow</option>
                  <option value="replay_event">replay_event</option>
                  <option value="disable_integration">disable_integration</option>
                  <option value="revoke_session">revoke_session</option>
                  <option value="retry_ingestion">retry_ingestion</option>
                </select>
              </div>

              <div>
                <label className="text-xs font-medium text-slate-400">Target Resource</label>
                <input
                  type="text"
                  value={targetResource}
                  onChange={(e) => setTargetResource(e.target.value)}
                  className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-emerald-500"
                />
              </div>

              <div>
                <label className="text-xs font-medium text-slate-400">Risk Level</label>
                <select
                  value={riskLevel}
                  onChange={(e) => setRiskLevel(e.target.value)}
                  className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-emerald-500"
                >
                  <option value="low">Low (Auto-exec)</option>
                  <option value="medium">Medium (Auto-exec)</option>
                  <option value="high">High (Requires 2-Person Approval)</option>
                  <option value="critical">Critical (Requires 2-Person Approval)</option>
                </select>
              </div>

              <div>
                <label className="text-xs font-medium text-slate-400">Operator Reason</label>
                <input
                  type="text"
                  value={reason}
                  onChange={(e) => setReason(e.target.value)}
                  className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-emerald-500"
                />
              </div>
            </div>

            <button
              onClick={handleRequestAction}
              className="mt-4 px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-sm font-medium transition flex items-center gap-2"
            >
              <Zap className="w-4 h-4" /> Dispatch Control Action
            </button>
          </div>

          {/* Actions Audit History */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
            <div className="p-4 border-b border-slate-800 font-semibold text-white">
              Control Action Audit Log & Pending Approvals
            </div>
            <div className="divide-y divide-slate-800">
              {actions.map((act) => (
                <div key={act.id} className="p-4 flex items-center justify-between">
                  <div className="space-y-1">
                    <div className="flex items-center gap-3">
                      <span className="font-mono text-xs text-emerald-400 font-semibold bg-emerald-950 border border-emerald-800 px-2 py-0.5 rounded">
                        {act.actionType}
                      </span>
                      <span className="text-sm font-medium text-white">{act.targetResource}</span>
                      <span className="text-xs text-slate-400">Risk: {act.riskLevel.toUpperCase()}</span>
                    </div>
                    <div className="text-xs text-slate-400">
                      Requested by <span className="text-slate-200">{act.requestedBy}</span>: &quot;{act.reason}&quot;
                    </div>
                  </div>

                  <div className="flex items-center gap-3">
                    <span className={`text-xs px-2.5 py-0.5 rounded-full ${
                      act.status === 'completed' ? 'bg-emerald-950 text-emerald-400 border border-emerald-800' :
                      act.status === 'pending_approval' ? 'bg-amber-950 text-amber-400 border border-amber-800' :
                      'bg-slate-800 text-slate-300'
                    }`}>
                      {act.status}
                    </span>

                    {act.status === 'pending_approval' && (
                      <button
                        onClick={() => handleApproveAction(act.id)}
                        className="px-3 py-1 bg-amber-600 hover:bg-amber-500 text-white text-xs rounded transition flex items-center gap-1 font-medium"
                      >
                        <Check className="w-3.5 h-3.5" /> Approve (2-Person Gate)
                      </button>
                    )}
                  </div>
                </div>
              ))}
              {actions.length === 0 && (
                <div className="p-8 text-center text-slate-500">No control actions requested.</div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* AI Operations Assistant Tab */}
      {activeTab === 'assistant' && (
        <div className="space-y-6">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
            <h2 className="text-lg font-semibold text-white flex items-center gap-2">
              <Brain className="w-5 h-5 text-cyan-400" />
              AI Operations Diagnostic Assistant
            </h2>
            <p className="text-slate-400 text-sm">
              Ask evidence-backed natural language diagnostic questions about system degradation, incidents, workflows, or costs.
            </p>

            <div className="flex gap-3">
              <input
                type="text"
                value={aiQuery}
                onChange={(e) => setAiQuery(e.target.value)}
                placeholder="e.g. Why is the platform degraded? Which services are failing?"
                className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2.5 text-sm text-white focus:outline-none focus:border-cyan-500"
              />
              <button
                onClick={handleAiQuerySubmit}
                disabled={isAiLoading}
                className="px-5 py-2.5 bg-cyan-600 hover:bg-cyan-500 disabled:bg-slate-800 text-white rounded-lg text-sm font-medium transition flex items-center gap-2"
              >
                <MessageSquare className="w-4 h-4" />
                {isAiLoading ? 'Analyzing...' : 'Ask Assistant'}
              </button>
            </div>
          </div>

          {aiResponse && (
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
              <h3 className="text-md font-semibold text-white border-b border-slate-800 pb-2">
                Diagnostic Analysis & Evidence
              </h3>

              <p className="text-slate-200 text-sm leading-relaxed">{aiResponse.answer}</p>

              <div>
                <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Evidence Signals Cited</h4>
                <div className="space-y-1">
                  {aiResponse.evidenceSignals.map((ev: any, idx: number) => (
                    <div key={idx} className="text-xs font-mono bg-slate-950 p-2 rounded border border-slate-800 text-slate-300">
                      [{ev.source}] {ev.metric} = {ev.value} ({ev.status})
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
