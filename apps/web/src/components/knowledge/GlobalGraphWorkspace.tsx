'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { 
  Network, 
  Search, 
  Shield, 
  GitCommit, 
  CheckCircle2, 
  AlertCircle, 
  Layers, 
  RefreshCw, 
  Zap, 
  Check, 
  XCircle, 
  Activity, 
  Brain,
  Sliders,
  Maximize2
} from 'lucide-react';

interface SemanticEntity {
  id: string;
  organizationId: string;
  workspaceId?: string;
  entityType: string;
  entityId: string;
  displayName: string;
  status: string;
  source: string;
}

interface SemanticRelationship {
  id: string;
  fromEntityId: string;
  relationshipType: string;
  toEntityId: string;
  source: string;
  status: string;
  confidence: string;
}

interface ImpactResponse {
  rootEntityId: string;
  directDependencies: SemanticEntity[];
  indirectDependencies: SemanticEntity[];
  affectedWorkflows: any[];
  affectedAgents: any[];
  affectedIntegrations: any[];
  totalImpactedCount: number;
}

export const GlobalGraphWorkspace: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'explorer' | 'path' | 'impact' | 'proposals' | 'health'>('explorer');
  const [health, setHealth] = useState<any>(null);
  const [proposals, setProposals] = useState<SemanticRelationship[]>([]);
  const [impactData, setImpactData] = useState<ImpactResponse | null>(null);
  const [selectedEntityId, setSelectedEntityId] = useState<string>('ent_wf_01');
  const [neighborsData, setNeighborsData] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Path finder state
  const [fromEntity, setFromEntity] = useState('ent_usr_01');
  const [toEntity, setToEntity] = useState('ent_integ_01');
  const [pathResult, setPathResult] = useState<any[]>([]);

  const fetchGraphData = useCallback(async () => {
    setIsLoading(true);
    try {
      const [hRes, pRes, nRes] = await Promise.all([
        fetch('/api/v1/graph/health'),
        fetch('/api/v1/graph/relationships'),
        fetch(`/api/v1/graph/entities/${selectedEntityId}/neighbors`)
      ]);

      if (hRes.ok) setHealth(await hRes.json());
      if (pRes.ok) setProposals(await pRes.json());
      if (nRes.ok) setNeighborsData(await nRes.json());
    } catch (err) {
      console.error('Failed to fetch Semantic Graph data:', err);
    } finally {
      setIsLoading(false);
    }
  }, [selectedEntityId]);

  useEffect(() => {
    fetchGraphData();
  }, [fetchGraphData]);

  const handleCalculateImpact = async () => {
    try {
      const res = await fetch(`/api/v1/graph/impact/${selectedEntityId}`);
      if (res.ok) {
        setImpactData(await res.json());
      }
    } catch (err) {
      console.error('Failed to calculate impact:', err);
    }
  };

  const handleFindPath = async () => {
    try {
      const res = await fetch(`/api/v1/graph/path?fromEntityId=${fromEntity}&toEntityId=${toEntity}`);
      if (res.ok) {
        setPathResult(await res.json());
      }
    } catch (err) {
      console.error('Failed to find graph path:', err);
    }
  };

  const handleApproveProposal = async (relId: string) => {
    try {
      const res = await fetch(`/api/v1/graph/relationships/${relId}/approve`, {
        method: 'POST'
      });
      if (res.ok) {
        fetchGraphData();
      }
    } catch (err) {
      console.error('Failed to approve proposal:', err);
    }
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8 bg-slate-950 text-slate-100 min-h-screen">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-3">
            <Network className="w-8 h-8 text-cyan-400" />
            <h1 className="text-3xl font-bold tracking-tight text-white">Enterprise Semantic Graph</h1>
          </div>
          <p className="text-slate-400 mt-1">
            Unified Relationship Layer & Authorization-Aware Semantic Business Context
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button 
            onClick={fetchGraphData}
            className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg text-sm font-medium transition"
          >
            <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
            Sync Graph
          </button>
        </div>
      </div>

      {/* Top Health Indicators */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="text-slate-400 text-xs font-semibold uppercase tracking-wider">Registered Entities</div>
          <div className="flex items-center gap-2 mt-2">
            <Layers className="w-5 h-5 text-cyan-400" />
            <span className="text-xl font-bold text-white">{health?.entityCount || 10}</span>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="text-slate-400 text-xs font-semibold uppercase tracking-wider">Semantic Relationships</div>
          <div className="flex items-center gap-2 mt-2">
            <GitCommit className="w-5 h-5 text-emerald-400" />
            <span className="text-xl font-bold text-white">{health?.relationshipCount || 8}</span>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="text-slate-400 text-xs font-semibold uppercase tracking-wider">Orphan Node Rate</div>
          <div className="flex items-center gap-2 mt-2">
            <AlertCircle className="w-5 h-5 text-amber-400" />
            <span className="text-xl font-bold text-white">{((health?.orphanRate || 0) * 100).toFixed(1)}%</span>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="text-slate-400 text-xs font-semibold uppercase tracking-wider">Sync Lag</div>
          <div className="flex items-center gap-2 mt-2">
            <Activity className="w-5 h-5 text-indigo-400" />
            <span className="text-xl font-bold text-white">{health?.syncLagSeconds || 0.5}s</span>
          </div>
        </div>
      </div>

      {/* Main Workspace Navigation */}
      <div className="flex border-b border-slate-800 gap-6">
        <button
          onClick={() => setActiveTab('explorer')}
          className={`pb-3 text-sm font-medium border-b-2 transition ${
            activeTab === 'explorer'
              ? 'border-cyan-400 text-cyan-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          Graph Explorer
        </button>
        <button
          onClick={() => setActiveTab('path')}
          className={`pb-3 text-sm font-medium border-b-2 transition ${
            activeTab === 'path'
              ? 'border-cyan-400 text-cyan-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          Path Finder (A &rarr; B)
        </button>
        <button
          onClick={() => setActiveTab('impact')}
          className={`pb-3 text-sm font-medium border-b-2 transition ${
            activeTab === 'impact'
              ? 'border-cyan-400 text-cyan-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          Impact Analysis (Blast Radius)
        </button>
        <button
          onClick={() => setActiveTab('proposals')}
          className={`pb-3 text-sm font-medium border-b-2 transition ${
            activeTab === 'proposals'
              ? 'border-cyan-400 text-cyan-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          AI Proposals & Review ({proposals.length})
        </button>
      </div>

      {/* Explorer Tab */}
      {activeTab === 'explorer' && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="md:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold text-white flex items-center gap-2">
                <Maximize2 className="w-5 h-5 text-cyan-400" />
                Focus Subgraph View
              </h2>
              <span className="text-xs font-mono text-slate-400">Root: {selectedEntityId}</span>
            </div>

            {/* Visual Node Representation */}
            <div className="p-8 bg-slate-950 border border-slate-800 rounded-xl flex flex-col items-center justify-center min-h-[300px] space-y-6">
              {neighborsData?.entity && (
                <div className="p-4 bg-cyan-950 border border-cyan-800 text-cyan-300 rounded-xl font-semibold text-center shadow-lg w-64">
                  <div className="text-xs uppercase text-cyan-500 font-mono">{neighborsData.entity.entity_type}</div>
                  <div className="text-lg text-white">{neighborsData.entity.display_name}</div>
                  <div className="text-xs text-slate-400 font-mono">{neighborsData.entity.id}</div>
                </div>
              )}

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full pt-4">
                {neighborsData?.neighbors?.map((item: any, idx: number) => (
                  <div 
                    key={idx}
                    onClick={() => setSelectedEntityId(item.entity.id)}
                    className="p-3 bg-slate-900 hover:bg-slate-800 border border-slate-800 rounded-lg cursor-pointer transition flex items-center justify-between"
                  >
                    <div>
                      <span className="text-xs text-emerald-400 font-mono block">
                        {item.direction === 'outgoing' ? '&rarr;' : '&larr;'} {item.relationship.relationship_type}
                      </span>
                      <span className="text-sm font-medium text-white">{item.entity.display_name}</span>
                    </div>
                    <span className="text-xs bg-slate-800 text-slate-400 px-2 py-0.5 rounded font-mono">
                      {item.entity.entity_type}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Node Inspector Drawer */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
            <h3 className="text-md font-semibold text-white border-b border-slate-800 pb-2">
              Entity Inspector
            </h3>
            {neighborsData?.entity ? (
              <div className="space-y-3 text-xs">
                <div><span className="text-slate-400">Display Name:</span> <span className="font-semibold text-white">{neighborsData.entity.display_name}</span></div>
                <div><span className="text-slate-400">Entity Type:</span> <span className="font-mono text-cyan-400">{neighborsData.entity.entity_type}</span></div>
                <div><span className="text-slate-400">Domain Entity ID:</span> <span className="font-mono text-slate-300">{neighborsData.entity.entity_id}</span></div>
                <div><span className="text-slate-400">Source:</span> <span className="font-mono text-slate-300">{neighborsData.entity.source}</span></div>
                <div><span className="text-slate-400">Organization Scope:</span> <span className="font-mono text-slate-300">{neighborsData.entity.organization_id}</span></div>
                <div><span className="text-slate-400">Workspace Scope:</span> <span className="font-mono text-slate-300">{neighborsData.entity.workspace_id}</span></div>
              </div>
            ) : (
              <div className="text-slate-500 text-sm">Select a node to inspect entity details.</div>
            )}
          </div>
        </div>
      )}

      {/* Path Finder Tab */}
      {activeTab === 'path' && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-6">
          <h2 className="text-lg font-semibold text-white">Find Traversal Path Between Entities</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="text-xs font-medium text-slate-400">From Entity ID</label>
              <input
                type="text"
                value={fromEntity}
                onChange={(e) => setFromEntity(e.target.value)}
                className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-cyan-500"
              />
            </div>
            <div>
              <label className="text-xs font-medium text-slate-400">To Entity ID</label>
              <input
                type="text"
                value={toEntity}
                onChange={(e) => setToEntity(e.target.value)}
                className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-cyan-500"
              />
            </div>
            <div className="flex items-end">
              <button
                onClick={handleFindPath}
                className="w-full py-2.5 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg text-sm font-medium transition"
              >
                Find Path
              </button>
            </div>
          </div>

          {pathResult.length > 0 && (
            <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2">
              <div className="text-xs text-slate-400 font-semibold uppercase">Resolved Graph Path</div>
              <div className="flex items-center flex-wrap gap-2 text-sm">
                {pathResult.map((step, idx) => (
                  <React.Fragment key={step.id}>
                    <span className="px-3 py-1 bg-slate-800 text-white rounded font-medium">
                      {step.display_name} ({step.entity_type})
                    </span>
                    {idx < pathResult.length - 1 && <span className="text-cyan-400 font-bold">&rarr;</span>}
                  </React.Fragment>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Impact Analysis Tab */}
      {activeTab === 'impact' && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-white">Blast Radius & Downstream Impact</h2>
            <button
              onClick={handleCalculateImpact}
              className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-medium rounded-lg transition"
            >
              Analyze Blast Radius
            </button>
          </div>

          {impactData && (
            <div className="space-y-4">
              <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg flex items-center justify-between">
                <span className="text-sm font-medium text-slate-300">Total Downstream Impacted Entities</span>
                <span className="text-xl font-bold text-emerald-400">{impactData.totalImpactedCount}</span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2">
                  <h4 className="text-xs font-semibold text-slate-400 uppercase">Affected Workflows</h4>
                  {impactData.affectedWorkflows.map((wf) => (
                    <div key={wf.id} className="text-sm text-white font-medium">{wf.display_name}</div>
                  ))}
                  {impactData.affectedWorkflows.length === 0 && <div className="text-xs text-slate-500">None affected</div>}
                </div>

                <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2">
                  <h4 className="text-xs font-semibold text-slate-400 uppercase">Affected Integrations</h4>
                  {impactData.affectedIntegrations.map((ig) => (
                    <div key={ig.id} className="text-sm text-white font-medium">{ig.display_name}</div>
                  ))}
                  {impactData.affectedIntegrations.length === 0 && <div className="text-xs text-slate-500">None affected</div>}
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* AI Proposals & Review Tab */}
      {activeTab === 'proposals' && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
          <div className="p-4 border-b border-slate-800 font-semibold text-white">
            AI-Suggested Relationship Proposals & Human Review
          </div>
          <div className="divide-y divide-slate-800">
            {proposals.map((p) => (
              <div key={p.id} className="p-4 flex items-center justify-between">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-xs text-cyan-400 font-semibold bg-cyan-950 border border-cyan-800 px-2 py-0.5 rounded">
                      {p.relationshipType}
                    </span>
                    <span className="text-sm text-white">{p.fromEntityId} &rarr; {p.toEntityId}</span>
                  </div>
                  <div className="text-xs text-slate-400">Confidence: {p.confidence} | Source: {p.source}</div>
                </div>

                <button
                  onClick={() => handleApproveProposal(p.id)}
                  className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-medium rounded transition flex items-center gap-1"
                >
                  <Check className="w-3.5 h-3.5" /> Approve Proposal
                </button>
              </div>
            ))}
            {proposals.length === 0 && (
              <div className="p-8 text-center text-slate-500">No pending AI relationship proposals.</div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
