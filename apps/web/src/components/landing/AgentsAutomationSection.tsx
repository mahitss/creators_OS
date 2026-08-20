'use client';

import React from 'react';

export function AgentsAutomationSection() {
  return (
    <section className="py-28 bg-[#050608] border-t border-slate-900 relative">
      <div className="max-w-7xl mx-auto px-6 sm:px-8">
        <div className="max-w-3xl flex flex-col gap-4">
          <div className="inline-flex items-center gap-2 text-xs font-mono text-cyan-400 tracking-widest uppercase">
            <span>[ 04 // AGENTS & WORKFLOWS ]</span>
          </div>
          <h2 className="text-3xl sm:text-4xl font-bold text-white tracking-tight">
            Autonomous Missions with Deterministic Controls.
          </h2>
          <p className="text-slate-400 text-base sm:text-lg font-light leading-relaxed">
            Kinetiq replaces brittle prompt chains with robust, observable agent runtimes. Agents operate through strict capability registries, verifiable step execution, and human-in-the-loop escalation.
          </p>
        </div>

        {/* 4 Execution Grid Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mt-16">
          {/* Card 1 */}
          <div className="p-6 rounded-2xl bg-[#080A0D] border border-slate-800/80 hover:border-cyan-500/40 transition-all flex flex-col gap-3.5">
            <div className="text-cyan-400 font-mono text-xs uppercase tracking-wider">
              01 // DECOMPOSITION
            </div>
            <h3 className="text-lg font-bold text-white">Goal Decomposition</h3>
            <p className="text-xs text-slate-400 font-light leading-relaxed">
              Missions are dynamically split into discrete, sequenced steps with explicit input/output contracts and dependencies.
            </p>
          </div>

          {/* Card 2 */}
          <div className="p-6 rounded-2xl bg-[#080A0D] border border-slate-800/80 hover:border-emerald-500/40 transition-all flex flex-col gap-3.5">
            <div className="text-emerald-400 font-mono text-xs uppercase tracking-wider">
              02 // CAPABILITY REGISTRY
            </div>
            <h3 className="text-lg font-bold text-white">Tool Sandboxing</h3>
            <p className="text-xs text-slate-400 font-light leading-relaxed">
              Tools are registered with strict permission schemas. Database, external APIs, and file mutations are audited per invocation.
            </p>
          </div>

          {/* Card 3 */}
          <div className="p-6 rounded-2xl bg-[#080A0D] border border-slate-800/80 hover:border-blue-500/40 transition-all flex flex-col gap-3.5">
            <div className="text-blue-400 font-mono text-xs uppercase tracking-wider">
              03 // STATE MACHINES
            </div>
            <h3 className="text-lg font-bold text-white">Workflow Graphs</h3>
            <p className="text-xs text-slate-400 font-light leading-relaxed">
              Cyclic and DAG workflows execute with automated retry exponential backoff and webhook event trigger bindings.
            </p>
          </div>

          {/* Card 4 */}
          <div className="p-6 rounded-2xl bg-[#080A0D] border border-slate-800/80 hover:border-purple-500/40 transition-all flex flex-col gap-3.5">
            <div className="text-purple-400 font-mono text-xs uppercase tracking-wider">
              04 // HUMAN-IN-THE-LOOP
            </div>
            <h3 className="text-lg font-bold text-white">Attention Inbox</h3>
            <p className="text-xs text-slate-400 font-light leading-relaxed">
              High-risk actions, significant budget changes, and sensitive mutations pause execution for explicit human authorization.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
