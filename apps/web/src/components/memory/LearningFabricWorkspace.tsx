'use client';

import React, { useState, useEffect } from 'react';
import { 
  Brain, 
  Search, 
  Filter, 
  CheckCircle2, 
  AlertTriangle, 
  ShieldCheck, 
  FileText, 
  History, 
  Trash2, 
  Edit3, 
  ThumbsUp, 
  ThumbsDown,
  Layers,
  Sparkles,
  GitPullRequest
} from 'lucide-react';

interface AgentMemoryData {
  id: string;
  organizationId: string;
  workspaceId: string;
  ownerType: string;
  ownerId: string;
  memoryType: string;
  scope: string;
  title: string;
  content: string;
  status: string;
  importance: string;
  confidence: number;
  createdAt: string;
  updatedAt: string;
  expiresAt?: string;
}

interface MemoryCandidateData {
  id: string;
  workspaceId: string;
  proposedByAgentId: string;
  memoryType: string;
  suggestedContent: any;
  evidenceReference: any;
  status: string;
  createdAt: string;
}

interface MemoryConflictData {
  id: string;
  workspaceId: string;
  memoryIdA: string;
  memoryIdB: string;
  conflictReason: string;
  status: string;
  resolutionNotes?: string;
  resolvedBy?: string;
  createdAt: string;
}

export const LearningFabricWorkspace: React.FC = () => {
  const [memories, setMemories] = useState<AgentMemoryData[]>([
    {
      id: 'mem_gov_001',
      organizationId: 'org_default_creator',
      workspaceId: 'ws_default_01',
      ownerType: 'agent',
      ownerId: 'ag_creator_ops_01',
      memoryType: 'semantic',
      scope: 'workspace',
      title: 'Service X Deployment Region',
      content: 'Service X primary deployment region is us-east-1.',
      status: 'active',
      importance: 'high',
      confidence: 0.95,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    },
    {
      id: 'mem_gov_002',
      organizationId: 'org_default_creator',
      workspaceId: 'ws_default_01',
      ownerType: 'workspace',
      ownerId: 'ws_default_01',
      memoryType: 'procedural',
      scope: 'workspace',
      title: 'Report Publishing Procedure',
      content: 'To publish Q3 report, execute step A (Grounding), step B (DLP Scan), step C (Executive Sign-off).',
      status: 'active',
      importance: 'high',
      confidence: 0.90,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    }
  ]);

  const [candidates, setCandidates] = useState<MemoryCandidateData[]>([
    {
      id: 'cand_001',
      workspaceId: 'ws_default_01',
      proposedByAgentId: 'ag_creator_ops_01',
      memoryType: 'semantic',
      suggestedContent: { title: 'Proposed Preference: Nightly Builds', content: 'Workspace team prefers nightly builds scheduled at 02:00 UTC.' },
      evidenceReference: { executionId: 'exec_demo_01' },
      status: 'pending_review',
      createdAt: new Date().toISOString()
    }
  ]);

  const [conflicts, setConflicts] = useState<MemoryConflictData[]>([
    {
      id: 'conf_001',
      workspaceId: 'ws_default_01',
      memoryIdA: 'mem_gov_001',
      memoryIdB: 'mem_draft_99',
      conflictReason: 'Conflicting deployment region (us-east-1 vs us-west-2).',
      status: 'unresolved',
      createdAt: new Date().toISOString()
    }
  ]);

  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedType, setSelectedType] = useState<string>('all');
  const [selectedScope, setSelectedScope] = useState<string>('all');
  const [activeTab, setActiveTab] = useState<'memories' | 'review' | 'conflicts' | 'procedural'>('memories');
  const [editingMemory, setEditingMemory] = useState<AgentMemoryData | null>(null);
  const [correctedContent, setCorrectedContent] = useState<string>('');

  const fetchMemories = async () => {
    try {
      const res = await fetch(`/api/v1/memory/search?query=${searchQuery}&type=${selectedType}&scope=${selectedScope}`);
      if (res.ok) {
        const data = await res.json();
        setMemories(data || []);
      }
    } catch (e) {
      // Keep fallback
    }
  };

  useEffect(() => {
    fetchMemories();
  }, [searchQuery, selectedType, selectedScope]);

  const handleCorrect = async (id: string) => {
    try {
      const res = await fetch(`/api/v1/memory/${id}/correct`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ correctedContent: correctedContent, reason: 'Operator manual correction' })
      });
      if (res.ok) {
        setEditingMemory(null);
        fetchMemories();
      }
    } catch (e) {
      setMemories(prev => prev.map(m => m.id === id ? { ...m, content: correctedContent } : m));
      setEditingMemory(null);
    }
  };

  const handleInvalidate = async (id: string) => {
    try {
      const res = await fetch(`/api/v1/memory/${id}/invalidate`, { method: 'POST' });
      if (res.ok) fetchMemories();
    } catch (e) {
      setMemories(prev => prev.map(m => m.id === id ? { ...m, status: 'deprecated' } : m));
    }
  };

  const handleResolveConflict = async (conflictId: string) => {
    try {
      const res = await fetch(`/api/v1/memory/conflicts/${conflictId}/resolve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ resolution: 'resolved_a', notes: 'Operator verified authorative source A wins.' })
      });
      if (res.ok) {
        setConflicts(prev => prev.filter(c => c.id !== conflictId));
      }
    } catch (e) {
      setConflicts(prev => prev.filter(c => c.id !== conflictId));
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl text-white space-y-4">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-indigo-500/20 text-indigo-400 rounded-lg border border-indigo-500/30">
              <Brain className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight">Enterprise Agent Memory 3.0 & Learning Fabric</h1>
              <p className="text-xs text-slate-400">Governed, provenance-backed agent memory with conflict resolution & DLP boundary control</p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs border-t border-slate-800 pt-4 text-slate-400">
          <div>Active Memories: <span className="text-slate-200 font-mono">{memories.length}</span></div>
          <div>Review Candidates: <span className="text-amber-400 font-mono">{candidates.length}</span></div>
          <div>Unresolved Conflicts: <span className="text-rose-400 font-mono">{conflicts.length}</span></div>
          <div>DLP Protection: <span className="text-emerald-400 font-semibold flex items-center gap-1 inline-flex"><ShieldCheck className="w-3.5 h-3.5" /> Enforced</span></div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
        <button
          onClick={() => setActiveTab('memories')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition ${
            activeTab === 'memories' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          All Memories ({memories.length})
        </button>
        <button
          onClick={() => setActiveTab('review')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition ${
            activeTab === 'review' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Review Queue ({candidates.length})
        </button>
        <button
          onClick={() => setActiveTab('conflicts')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition ${
            activeTab === 'conflicts' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Active Conflicts ({conflicts.length})
        </button>
        <button
          onClick={() => setActiveTab('procedural')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition ${
            activeTab === 'procedural' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Procedural Knowledge
        </button>
      </div>

      {/* Search & Filter Controls */}
      {activeTab === 'memories' && (
        <div className="flex flex-col md:flex-row items-center gap-3">
          <div className="relative flex-1 w-full">
            <Search className="w-4 h-4 absolute left-3 top-3 text-slate-500" />
            <input
              type="text"
              placeholder="Search memories by title or content..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-slate-900 border border-slate-800 rounded-lg pl-9 pr-4 py-2 text-sm text-slate-200 focus:outline-none focus:border-indigo-500"
            />
          </div>

          <select
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
            className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-200"
          >
            <option value="all">All Memory Types</option>
            <option value="semantic">Semantic</option>
            <option value="episodic">Episodic</option>
            <option value="procedural">Procedural</option>
            <option value="preference">Preference</option>
          </select>

          <select
            value={selectedScope}
            onChange={(e) => setSelectedScope(e.target.value)}
            className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-200"
          >
            <option value="all">All Scopes</option>
            <option value="workspace">Workspace</option>
            <option value="agent">Agent</option>
            <option value="private">Private</option>
          </select>
        </div>
      )}

      {/* Tab Content: All Memories */}
      {activeTab === 'memories' && (
        <div className="space-y-4">
          {memories.map((m) => (
            <div key={m.id} className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="px-2 py-0.5 text-xs font-semibold rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 uppercase">
                    {m.memoryType}
                  </span>
                  <h3 className="text-base font-semibold text-white">{m.title}</h3>
                  <span className="text-xs text-slate-500 font-mono">({m.id})</span>
                </div>

                <div className="flex items-center gap-2">
                  <span className={`px-2.5 py-0.5 text-xs font-medium rounded-full ${
                    m.status === 'active' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-slate-800 text-slate-400'
                  }`}>
                    {m.status}
                  </span>

                  <button
                    onClick={() => { setEditingMemory(m); setCorrectedContent(m.content); }}
                    className="p-1.5 hover:bg-slate-800 text-slate-400 hover:text-white rounded transition"
                  >
                    <Edit3 className="w-4 h-4" />
                  </button>

                  <button
                    onClick={() => handleInvalidate(m.id)}
                    className="p-1.5 hover:bg-slate-800 text-slate-400 hover:text-rose-400 rounded transition"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>

              <p className="text-sm text-slate-300 bg-slate-950 p-3 rounded-lg border border-slate-800 font-mono">
                {m.content}
              </p>

              {editingMemory?.id === m.id && (
                <div className="p-4 bg-slate-950 border border-indigo-500/30 rounded-lg space-y-3">
                  <h4 className="text-xs font-semibold text-indigo-400">Human Correction & Versioning</h4>
                  <textarea
                    value={correctedContent}
                    onChange={(e) => setCorrectedContent(e.target.value)}
                    className="w-full bg-slate-900 border border-slate-800 rounded p-2 text-xs text-slate-200 font-mono"
                    rows={3}
                  />
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleCorrect(m.id)}
                      className="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-medium rounded transition"
                    >
                      Save Versioned Correction
                    </button>
                    <button
                      onClick={() => setEditingMemory(null)}
                      className="px-3 py-1.5 bg-slate-800 text-slate-300 text-xs font-medium rounded transition"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              )}

              <div className="flex items-center justify-between text-xs text-slate-400 pt-2 border-t border-slate-800/50">
                <div>Owner: <span className="text-slate-200 font-mono">{m.ownerId}</span></div>
                <div>Confidence: <span className="text-emerald-400 font-mono">{(m.confidence * 100).toFixed(0)}%</span></div>
                <div>Importance: <span className="text-slate-200 capitalize">{m.importance}</span></div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Tab Content: Review Queue */}
      {activeTab === 'review' && (
        <div className="space-y-4">
          {candidates.map((c) => (
            <div key={c.id} className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono text-amber-400">Proposed Candidate: {c.id}</span>
                <span className="text-xs text-slate-400">Proposed by Agent: <span className="font-mono text-white">{c.proposedByAgentId}</span></span>
              </div>
              <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 text-xs text-slate-300 font-mono">
                {JSON.stringify(c.suggestedContent)}
              </div>
              <div className="flex items-center gap-2">
                <button className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-medium rounded transition flex items-center gap-1">
                  <ThumbsUp className="w-3.5 h-3.5" /> Approve & Promote to Active
                </button>
                <button className="px-3 py-1.5 bg-rose-600/20 hover:bg-rose-600/30 text-rose-300 text-xs font-medium rounded transition flex items-center gap-1 border border-rose-500/30">
                  <ThumbsDown className="w-3.5 h-3.5" /> Reject Candidate
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Tab Content: Active Conflicts */}
      {activeTab === 'conflicts' && (
        <div className="space-y-4">
          {conflicts.map((conf) => (
            <div key={conf.id} className="bg-slate-900 border border-rose-500/30 rounded-xl p-5 space-y-3">
              <div className="flex items-center gap-2 text-rose-400 font-semibold text-sm">
                <AlertTriangle className="w-4 h-4" /> Conflict: {conf.conflictReason}
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs font-mono">
                <div className="p-3 bg-slate-950 rounded border border-slate-800 text-slate-300">
                  Memory A: {conf.memoryIdA}
                </div>
                <div className="p-3 bg-slate-950 rounded border border-slate-800 text-slate-300">
                  Memory B: {conf.memoryIdB}
                </div>
              </div>
              <button
                onClick={() => handleResolveConflict(conf.id)}
                className="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-medium rounded transition"
              >
                Resolve Conflict (Authoritative Source A Wins)
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Tab Content: Procedural */}
      {activeTab === 'procedural' && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
          <h2 className="text-base font-semibold text-white">Versioned Procedural Knowledge Guides</h2>
          <div className="space-y-3">
            {memories.filter(m => m.memoryType === 'procedural').map((p) => (
              <div key={p.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-2">
                <div className="flex items-center justify-between text-xs text-slate-300">
                  <span className="font-semibold text-indigo-400">{p.title}</span>
                  <span className="text-slate-500 font-mono">ID: {p.id}</span>
                </div>
                <p className="text-xs text-slate-300 font-mono">{p.content}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
