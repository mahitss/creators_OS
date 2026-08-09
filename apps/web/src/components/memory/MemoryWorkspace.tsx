import React, { useState, useEffect } from 'react';
import { Database, ShieldCheck, CheckCircle2, AlertTriangle, GitPullRequest, Info, FileText, Lock, Clock, Sparkles, User, Layers, ArrowRight } from 'lucide-react';

interface MemoryItem {
  id: string;
  scope: string;
  statement: string;
  type: string;
  confidence: number;
  status: string;
  source_references: any[];
  created_at: string;
}

interface MemoryConflict {
  id: string;
  memory_a_id: string;
  memory_b_id: string;
  reason: string;
  status: string;
  created_at: string;
}

export const MemoryWorkspace: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'workspace' | 'personal' | 'mission' | 'candidates' | 'conflicts'>('workspace');
  const [memories, setMemories] = useState<MemoryItem[]>([]);
  const [conflicts, setConflicts] = useState<MemoryConflict[]>([]);
  const [selectedProvenance, setSelectedProvenance] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchData();
  }, [activeTab]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const headers = { 'X-Workspace-Id': 'ws_default_01', 'X-User-Id': 'usr_alex' };
      if (activeTab === 'conflicts') {
        const res = await fetch('/api/v1/memories/conflicts', { headers });
        if (res.ok) setConflicts(await res.json());
      } else {
        const res = await fetch('/api/v1/memories', { headers });
        if (res.ok) {
          const data = await res.json();
          setMemories(data.memories || []);
        }
      }
    } catch (err) {
      console.error("Failed to load memory data:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleApproveCandidate = async (id: string) => {
    try {
      const res = await fetch(`/api/v1/memories/candidates/${id}/approve`, {
        method: 'POST',
        headers: { 'X-Workspace-Id': 'ws_default_01', 'X-User-Id': 'usr_alex' }
      });
      if (res.ok) fetchData();
    } catch (err) {
      console.error("Failed to approve candidate:", err);
    }
  };

  const handleResolveConflict = async (id: string, choice: string) => {
    try {
      const res = await fetch(`/api/v1/memories/conflicts/${id}/resolve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Workspace-Id': 'ws_default_01', 'X-User-Id': 'usr_alex' },
        body: JSON.stringify({ choice })
      });
      if (res.ok) fetchData();
    } catch (err) {
      console.error("Failed to resolve conflict:", err);
    }
  };

  const fetchProvenance = async (id: string) => {
    try {
      const res = await fetch(`/api/v1/memories/${id}/provenance`, {
        headers: { 'X-Workspace-Id': 'ws_default_01', 'X-User-Id': 'usr_alex' }
      });
      if (res.ok) setSelectedProvenance(await res.json());
    } catch (err) {
      console.error("Failed to fetch provenance:", err);
    }
  };

  const filteredMemories = memories.filter(m => {
    if (activeTab === 'workspace') return m.scope === 'workspace';
    if (activeTab === 'personal') return m.scope === 'personal';
    if (activeTab === 'mission') return m.scope === 'mission';
    if (activeTab === 'candidates') return m.status === 'candidate';
    return true;
  });

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8 text-zinc-100">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-zinc-800 pb-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
            <Database className="w-8 h-8 text-emerald-400" />
            Agent Knowledge & Memory 2.0
          </h1>
          <p className="text-zinc-400 mt-1">
            Traceable, human-approved, policy-scoped memory architecture with explicit provenance and conflict resolution.
          </p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-2 border-b border-zinc-800 pb-3 font-medium text-xs">
        {[
          { id: 'workspace', label: 'Workspace Memory', icon: Layers },
          { id: 'personal', label: 'Personal Memory', icon: User },
          { id: 'mission', label: 'Mission Memory', icon: Sparkles },
          { id: 'candidates', label: 'Candidates Inbox', icon: GitPullRequest },
          { id: 'conflicts', label: 'Conflicts Resolver', icon: AlertTriangle }
        ].map(tab => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl transition-all ${
                isActive ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-900'
              }`}
            >
              <Icon className="w-4 h-4" /> {tab.label}
            </button>
          );
        })}
      </div>

      {/* Content Grid */}
      {activeTab === 'conflicts' ? (
        <div className="space-y-4">
          {conflicts.length === 0 ? (
            <div className="p-12 text-center bg-zinc-900/40 border border-zinc-800 rounded-2xl text-zinc-500 text-sm">
              No active memory conflicts detected.
            </div>
          ) : (
            conflicts.map(c => (
              <div key={c.id} className="p-6 bg-zinc-900/80 border border-amber-500/30 rounded-2xl space-y-4 shadow-xl">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono text-amber-400 uppercase tracking-wider font-semibold">MEMORY CONFLICT DETECTED</span>
                  <span className="px-2.5 py-1 text-xs rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30 font-semibold">
                    {c.status}
                  </span>
                </div>

                <p className="text-sm text-zinc-300 font-mono bg-zinc-950 p-3 rounded-xl border border-zinc-800">{c.reason}</p>

                <div className="flex items-center justify-end gap-3">
                  <button
                    onClick={() => handleResolveConflict(c.id, 'keep_a')}
                    className="px-4 py-2 bg-zinc-800 hover:bg-zinc-700 text-zinc-200 text-xs font-semibold rounded-xl"
                  >
                    Keep Existing Memory (A)
                  </button>
                  <button
                    onClick={() => handleResolveConflict(c.id, 'keep_b')}
                    className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold rounded-xl transition-all shadow-lg shadow-emerald-600/20"
                  >
                    Accept New Memory (B) & Supersede
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {filteredMemories.map(m => (
            <div key={m.id} className="p-6 bg-zinc-900/60 border border-zinc-800 rounded-2xl space-y-4 hover:border-zinc-700 transition-all shadow-xl">
              <div className="flex items-start justify-between">
                <div>
                  <span className="text-xs font-mono text-emerald-400 uppercase tracking-wider font-semibold">{m.scope} SCOPE</span>
                  <h3 className="text-lg font-bold text-white mt-1">{m.statement}</h3>
                </div>
                <span className={`px-2.5 py-1 text-xs rounded-full font-semibold border ${
                  m.status === 'active' ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30' :
                  m.status === 'candidate' ? 'bg-amber-500/20 text-amber-300 border-amber-500/30' :
                  'bg-zinc-800 text-zinc-400 border-zinc-700'
                }`}>
                  {m.status}
                </span>
              </div>

              <div className="flex items-center justify-between text-xs text-zinc-400 border-t border-zinc-800/80 pt-3">
                <span className="font-mono">Confidence: {(m.confidence * 100).toFixed(0)}%</span>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => fetchProvenance(m.id)}
                    className="flex items-center gap-1 text-indigo-400 hover:text-indigo-300 font-semibold"
                  >
                    <Info className="w-3.5 h-3.5" /> Provenance
                  </button>
                  {m.status === 'candidate' && (
                    <button
                      onClick={() => handleApproveCandidate(m.id)}
                      className="flex items-center gap-1 px-3 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg font-semibold transition-all"
                    >
                      <CheckCircle2 className="w-3.5 h-3.5" /> Approve
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Provenance Drawer */}
      {selectedProvenance && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-end">
          <div className="bg-zinc-900 border-l border-zinc-800 w-full max-w-md h-full p-6 space-y-6 shadow-2xl overflow-y-auto">
            <div className="flex items-center justify-between border-b border-zinc-800 pb-4">
              <div>
                <span className="text-xs font-mono text-indigo-400">PROVENANCE TRACE</span>
                <h2 className="text-xl font-bold text-white mt-0.5">Memory Origin</h2>
              </div>
              <button onClick={() => setSelectedProvenance(null)} className="text-zinc-400 hover:text-white text-sm">Close</button>
            </div>

            <div className="space-y-4 text-xs text-zinc-300 font-mono">
              <div className="p-3 bg-zinc-950 border border-zinc-800 rounded-xl space-y-1">
                <div className="text-zinc-500">STATEMENT:</div>
                <div className="text-zinc-100 font-bold">{selectedProvenance.statement}</div>
              </div>

              <div className="p-3 bg-zinc-950 border border-zinc-800 rounded-xl space-y-1">
                <div className="text-zinc-500">SCOPE & OWNER:</div>
                <div className="text-emerald-400">{selectedProvenance.scope} | {selectedProvenance.owner_id}</div>
              </div>

              <div className="p-3 bg-zinc-950 border border-zinc-800 rounded-xl space-y-2">
                <div className="text-zinc-500">SOURCE REFERENCES:</div>
                {selectedProvenance.source_references && selectedProvenance.source_references.length > 0 ? (
                  selectedProvenance.source_references.map((ref: any, idx: number) => (
                    <div key={idx} className="p-2 bg-zinc-900 border border-zinc-800 rounded text-zinc-300">
                      <div>Type: {ref.type || 'Drive/Gmail'}</div>
                      <div>Title: {ref.title || 'Document'}</div>
                      <div className="text-zinc-500">Location: {ref.location || 'Section 1'}</div>
                    </div>
                  ))
                ) : (
                  <div className="text-zinc-500">User confirmed decision</div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
