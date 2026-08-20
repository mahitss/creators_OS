'use client';

import React from 'react';

export function AgentsAutomationSection() {
  return (
    <section id="automation" className="py-28 bg-[#0A0C0F] border-t border-[rgba(255,255,255,0.08)] relative">
      <div className="max-w-7xl mx-auto px-6 sm:px-8">
        <div className="max-w-3xl flex flex-col gap-3">
          <div className="inline-flex items-center gap-2 text-xs font-mono text-[#7CF7C5] tracking-widest uppercase">
            <span>[ 04 // AUTONOMOUS EXECUTION ]</span>
          </div>
          <h2 className="text-3xl sm:text-5xl font-bold text-[#F5F7FA] tracking-tight font-sans">
            FROM DECISION <br />
            TO EXECUTION.
          </h2>
          <p className="text-[rgba(245,247,250,0.55)] text-base sm:text-lg font-light leading-relaxed">
            Kinetiq does not simply generate text. It executes governed multi-agent workflows, coordinates continuous tools, and verifies state mutations through deterministic state machines.
          </p>
        </div>

        {/* Execution Flow Diagram: INTENT → PLAN → AGENT → TOOL → ACTION → RESULT */}
        <div className="mt-12 p-6 sm:p-8 rounded-2xl bg-[#050505] border border-[rgba(255,255,255,0.10)] overflow-x-auto">
          <div className="flex items-center justify-between min-w-[720px] gap-2">
            {[
              { step: '01', title: 'INTENT', desc: 'Goal definition' },
              { step: '02', title: 'PLAN', desc: 'Step decomposition' },
              { step: '03', title: 'AGENT', desc: 'Role assignment' },
              { step: '04', title: 'TOOL', desc: 'Sandbox capability' },
              { step: '05', title: 'ACTION', desc: 'Policy validation' },
              { step: '06', title: 'RESULT', desc: 'Verified state' },
            ].map((item, idx) => (
              <React.Fragment key={item.step}>
                <div className="flex flex-col items-center text-center p-3 rounded-xl bg-[#0A0C0F] border border-[rgba(255,255,255,0.08)] w-28 shrink-0">
                  <span className="text-[9px] font-mono text-[#7CF7C5]">{item.step}</span>
                  <span className="text-xs font-bold font-mono text-[#F5F7FA] mt-1">{item.title}</span>
                  <span className="text-[9px] text-[rgba(245,247,250,0.45)] mt-0.5">{item.desc}</span>
                </div>
                {idx < 5 && (
                  <span className="text-[#9BB7FF] font-mono text-xs shrink-0">→</span>
                )}
              </React.Fragment>
            ))}
          </div>
        </div>

        {/* 4 Governance Pillars: AUTHORIZATION, POLICY, EXECUTION, OBSERVABILITY */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mt-8">
          <div className="p-6 rounded-2xl bg-[#050505] border border-[rgba(255,255,255,0.08)] hover:border-[#7CF7C5]/40 transition-all flex flex-col gap-2.5">
            <div className="text-[#7CF7C5] font-mono text-xs uppercase tracking-wider">
              01 // AUTHORIZATION
            </div>
            <h3 className="text-base font-bold text-[#F5F7FA]">RBAC & ABAC Gates</h3>
            <p className="text-xs text-[rgba(245,247,250,0.55)] font-light leading-relaxed">
              Every agent execution requires explicit permission grants. Actions violating tenant boundaries fail closed immediately.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-[#050505] border border-[rgba(255,255,255,0.08)] hover:border-[#9BB7FF]/40 transition-all flex flex-col gap-2.5">
            <div className="text-[#9BB7FF] font-mono text-xs uppercase tracking-wider">
              02 // POLICY
            </div>
            <h3 className="text-base font-bold text-[#F5F7FA]">PolicyEngine Rules</h3>
            <p className="text-xs text-[rgba(245,247,250,0.55)] font-light leading-relaxed">
              Real-time policy guardrails inspect inputs, outputs, and tool arguments before mutations are committed.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-[#050505] border border-[rgba(255,255,255,0.08)] hover:border-[#7CF7C5]/40 transition-all flex flex-col gap-2.5">
            <div className="text-[#7CF7C5] font-mono text-xs uppercase tracking-wider">
              03 // EXECUTION
            </div>
            <h3 className="text-base font-bold text-[#F5F7FA]">Deterministic Runtimes</h3>
            <p className="text-xs text-[rgba(245,247,250,0.55)] font-light leading-relaxed">
              Multi-agent state machines execute complex workflows with step-by-step verification and automatic retry backoff.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-[#050505] border border-[rgba(255,255,255,0.08)] hover:border-[#9BB7FF]/40 transition-all flex flex-col gap-2.5">
            <div className="text-[#9BB7FF] font-mono text-xs uppercase tracking-wider">
              04 // OBSERVABILITY
            </div>
            <h3 className="text-base font-bold text-[#F5F7FA]">Attention Inbox</h3>
            <p className="text-xs text-[rgba(245,247,250,0.55)] font-light leading-relaxed">
              High-risk actions, significant budget modifications, and novel anomalies pause execution for human-in-the-loop sign-off.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
