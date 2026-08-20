'use client';

import React from 'react';

export function PositioningSection() {
  return (
    <section id="system" className="py-24 bg-[#080A0D] border-t border-b border-slate-900 relative">
      <div className="max-w-7xl mx-auto px-6 sm:px-8">
        <div className="max-w-3xl flex flex-col gap-4">
          <div className="inline-flex items-center gap-2 text-xs font-mono text-cyan-400 tracking-widest uppercase">
            <span>[ 01 // OPERATING MODEL ]</span>
          </div>
          <h2 className="text-3xl sm:text-4xl font-bold text-white tracking-tight">
            Engineered for Enterprise Command, Coordination, and Truth.
          </h2>
          <p className="text-slate-400 text-base sm:text-lg leading-relaxed font-light">
            Modern enterprises don&apos;t need fragmented chatbot widgets or isolated automation scripts. Kinetiq establishes an authoritative, unified operating kernel where memory, multi-agent reasoning, continuous workflows, and policy gates execute under strict cryptographic isolation.
          </p>
        </div>

        {/* 3 Core Pillars */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-16">
          {/* Pillar 1 */}
          <div className="p-8 rounded-2xl bg-[#0B0E12] border border-slate-800/90 flex flex-col gap-4 relative overflow-hidden group hover:border-cyan-500/40 transition-all duration-300">
            <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400 font-mono text-lg font-bold">
              01
            </div>
            <h3 className="text-xl font-semibold text-white tracking-tight">
              Authoritative Context & Memory
            </h3>
            <p className="text-sm text-slate-400 leading-relaxed font-light">
              Structured knowledge graphs, document embeddings, and semantic memory vaults synchronize continuously across tenant boundaries without data leakage.
            </p>
            <div className="text-[11px] font-mono text-cyan-400/80 pt-2">
              → Graph Ontology & Vector Storage
            </div>
          </div>

          {/* Pillar 2 */}
          <div className="p-8 rounded-2xl bg-[#0B0E12] border border-slate-800/90 flex flex-col gap-4 relative overflow-hidden group hover:border-emerald-500/40 transition-all duration-300">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 font-mono text-lg font-bold">
              02
            </div>
            <h3 className="text-xl font-semibold text-white tracking-tight">
              Deterministic Agent Orchestration
            </h3>
            <p className="text-sm text-slate-400 leading-relaxed font-light">
              Autonomous agents execute goal-driven missions with structured tool registries, step-by-step verification, state-machine transitions, and budget controls.
            </p>
            <div className="text-[11px] font-mono text-emerald-400/80 pt-2">
              → Multi-Agent Collaboration Mesh
            </div>
          </div>

          {/* Pillar 3 */}
          <div className="p-8 rounded-2xl bg-[#0B0E12] border border-slate-800/90 flex flex-col gap-4 relative overflow-hidden group hover:border-blue-500/40 transition-all duration-300">
            <div className="w-10 h-10 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400 font-mono text-lg font-bold">
              03
            </div>
            <h3 className="text-xl font-semibold text-white tracking-tight">
              Zero-Trust Policy & Resilience
            </h3>
            <p className="text-sm text-slate-400 leading-relaxed font-light">
              Every inference call, tool execution, and state mutation passes through real-time RBAC/ABAC policy engines, DLP secret masking, and circuit breaker failover.
            </p>
            <div className="text-[11px] font-mono text-blue-400/80 pt-2">
              → Continuous Governance & Audit Trail
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
