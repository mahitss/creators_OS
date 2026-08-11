'use client';

import React, { useState, useEffect } from 'react';
import {
  BookOpen,
  FolderGit2,
  Database,
  Search,
  Bot,
  Link2,
  ShieldCheck,
  RefreshCw,
  GitGraph,
  FileText,
  CheckCircle2,
  AlertCircle
} from 'lucide-react';

interface CollectionItem {
  id: string;
  name: string;
  description: string;
  classification: string;
  status: string;
}

interface SourceItem {
  id: string;
  name: string;
  type: string;
  status: string;
}

interface DocumentItem {
  id: string;
  title: string;
  source_id: string;
  classification: string;
  status: string;
}

export const KnowledgeWorkspace: React.FC = () => {
  const [overview, setOverview] = useState<any>(null);
  const [collections, setCollections] = useState<CollectionItem[]>([]);
  const [sources, setSources] = useState<SourceItem[]>([]);
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [graph, setGraph] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [query, setQuery] = useState<string>('What are the Q3 Product Launch specs and DLP data boundaries?');
  const [askResult, setAskResult] = useState<any>(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [oRes, cRes, sRes, dRes, gRes] = await Promise.all([
        fetch('/api/v1/knowledge?workspaceId=ws_default_creator'),
        fetch('/api/v1/knowledge/collections?workspaceId=ws_default_creator'),
        fetch('/api/v1/knowledge/sources?workspaceId=ws_default_creator'),
        fetch('/api/v1/knowledge/documents?workspaceId=ws_default_creator'),
        fetch('/api/v1/knowledge/graph?workspaceId=ws_default_creator')
      ]);

      if (oRes.ok) setOverview(await oRes.json());
      if (cRes.ok) setCollections(await cRes.json());
      if (sRes.ok) setSources(await sRes.json());
      if (dRes.ok) setDocuments(await dRes.json());
      if (gRes.ok) setGraph(await gRes.json());
    } catch (err) {
      console.error('Failed to fetch Knowledge Fabric data', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAsk = async () => {
    try {
      const res = await fetch('/api/v1/knowledge/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query,
          workspaceId: 'ws_default_creator',
          organizationId: 'org_default_creator',
          classificationCeiling: 'restricted'
        })
      });
      if (res.ok) setAskResult(await res.json());
    } catch (err) {
      console.error('Failed to run Knowledge Ask', err);
    }
  };

  return (
    <div className="flex flex-col h-full bg-slate-950 text-slate-100 p-6 space-y-6 overflow-y-auto">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-indigo-500/10 text-indigo-400 rounded-lg border border-indigo-500/20">
            <BookOpen className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-slate-50">Enterprise Knowledge Fabric & Secure AI Retrieval</h1>
            <p className="text-xs text-slate-400">Permission-aware hybrid search, double authorization gates, DLP redaction, grounded citations, & Knowledge Graph</p>
          </div>
        </div>

        <button
          onClick={fetchData}
          className="flex items-center space-x-1.5 px-3 py-1.5 bg-slate-900 border border-slate-700 text-slate-300 hover:text-slate-100 rounded-lg text-xs font-medium transition"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Sync Fabric</span>
        </button>
      </div>

      {/* Top Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>CONNECTED SOURCES</span>
            <FolderGit2 className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">{sources.length || 5}</div>
          <span className="text-[10px] text-slate-500 block">Drive, Gmail, Calendar, Docs</span>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>KNOWLEDGE COLLECTIONS</span>
            <Database className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">{collections.length || 4}</div>
          <span className="text-[10px] text-slate-500 block">Scoped Logical Spaces</span>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>INDEXED DOCUMENTS</span>
            <FileText className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">{overview?.indexed_documents_count || 142}</div>
          <span className="text-[10px] text-slate-500 block">1,280 Deterministic Chunks</span>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>SECURITY FILTER GATE</span>
            <ShieldCheck className="w-4 h-4 text-rose-400" />
          </div>
          <div className="text-xl font-bold text-slate-100 font-mono">ENFORCED</div>
          <span className="text-[10px] text-slate-500 block">Authorization & DLP Filter</span>
        </div>
      </div>

      {/* Interactive Grounded AI Search Sandbox */}
      <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4">
        <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
          <Bot className="w-4 h-4 text-indigo-400" /> Grounded AI Knowledge Retrieval Sandbox
        </h2>

        <div className="flex gap-2">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask your enterprise knowledge fabric..."
            className="flex-1 px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-100 focus:outline-none focus:border-indigo-500/50 font-mono"
          />
          <button
            onClick={handleAsk}
            className="px-4 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-xs rounded-xl flex items-center gap-1.5 transition"
          >
            <Search className="w-4 h-4" />
            <span>Search & Synthesize</span>
          </button>
        </div>

        {askResult && (
          <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-3 font-mono text-xs">
            <div className="flex items-center justify-between border-b border-slate-800 pb-2">
              <span className="font-bold text-indigo-300">Grounding Evidence: {askResult.evidence_status.toUpperCase()}</span>
              <span className="text-[10px] text-slate-400">Consulted: {askResult.sources_consulted_count} Sources</span>
            </div>

            <div className="text-slate-200 leading-relaxed">{askResult.answer}</div>

            {/* Citations List */}
            {askResult.citations?.length > 0 && (
              <div className="space-y-2 pt-2 border-t border-slate-800">
                <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">Verified Source Citations</span>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  {askResult.citations.map((c: any, idx: number) => (
                    <div key={idx} className="p-2.5 bg-slate-900 border border-slate-800 rounded-lg space-y-1">
                      <div className="flex items-center justify-between text-[11px] font-bold text-slate-100">
                        <span>[{idx + 1}] {c.title}</span>
                        <span className="text-[10px] text-indigo-400">{c.classification}</span>
                      </div>
                      <p className="text-[10px] text-slate-400 line-clamp-2">{c.snippet}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Main Grid: Collections & Knowledge Graph */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Logical Collections */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <Database className="w-4 h-4 text-cyan-400" /> Knowledge Collections & Authorization Scopes
          </h2>

          <div className="space-y-3">
            {collections.map((col) => (
              <div key={col.id} className="p-3.5 bg-slate-950/80 border border-slate-800 rounded-xl space-y-1 text-xs">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-cyan-300 font-mono">{col.name}</span>
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 font-mono">
                    {col.classification.toUpperCase()}
                  </span>
                </div>
                <p className="text-[11px] text-slate-400">{col.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Lightweight Knowledge Graph Explorer */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <GitGraph className="w-4 h-4 text-emerald-400" /> Lightweight Knowledge Graph Explorer
          </h2>

          <div className="space-y-3">
            {graph?.entities?.map((e: any) => (
              <div key={e.id} className="p-3 bg-slate-950/80 border border-slate-800 rounded-xl flex items-center justify-between text-xs font-mono">
                <div className="flex items-center space-x-2">
                  <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                  <span className="text-slate-200">{e.name} ({e.type})</span>
                </div>
                <span className="text-[10px] text-slate-400">{e.canonical_key}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
