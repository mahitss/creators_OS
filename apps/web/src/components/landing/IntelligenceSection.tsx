'use client';

import React from 'react';

export function IntelligenceSection() {
  return (
    <section id="intelligence" className="py-28 bg-[#050505] border-t border-[rgba(255,255,255,0.08)] relative">
      <div className="max-w-7xl mx-auto px-6 sm:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          {/* Left Column: Contextual Intelligence Overview */}
          <div className="lg:col-span-6 flex flex-col gap-6">
            <div className="inline-flex items-center gap-2 text-xs font-mono text-[#7CF7C5] tracking-widest uppercase">
              <span>[ 03 // INTELLIGENCE LAYER ]</span>
            </div>
            <h2 className="text-3xl sm:text-5xl font-bold text-[#F5F7FA] tracking-tight font-sans">
              INTELLIGENCE THAT <br />
              UNDERSTANDS CONTEXT.
            </h2>
            <p className="text-[rgba(245,247,250,0.55)] text-base sm:text-lg leading-relaxed font-light">
              Kinetiq turns fragmented enterprise signals into contextual intelligence. Operating an enterprise model gateway with dynamic routing, continuous token accounting, and DLP perimeter protection.
            </p>

            {/* Visual Layers: DATA → CONTEXT → REASONING → DECISION */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 pt-2">
              <div className="p-3.5 rounded-xl bg-[#0A0C0F] border border-[rgba(255,255,255,0.08)] flex flex-col gap-1">
                <span className="text-[10px] font-mono text-[rgba(245,247,250,0.55)]">01 LAYER</span>
                <span className="text-xs font-bold text-[#F5F7FA] font-mono">DATA</span>
                <span className="text-[9px] text-[rgba(245,247,250,0.40)]">Raw Signals</span>
              </div>
              <div className="p-3.5 rounded-xl bg-[#0A0C0F] border border-[rgba(255,255,255,0.08)] flex flex-col gap-1">
                <span className="text-[10px] font-mono text-[rgba(245,247,250,0.55)]">02 LAYER</span>
                <span className="text-xs font-bold text-[#7CF7C5] font-mono">CONTEXT</span>
                <span className="text-[9px] text-[rgba(245,247,250,0.40)]">Graph Vault</span>
              </div>
              <div className="p-3.5 rounded-xl bg-[#0A0C0F] border border-[rgba(255,255,255,0.08)] flex flex-col gap-1">
                <span className="text-[10px] font-mono text-[rgba(245,247,250,0.55)]">03 LAYER</span>
                <span className="text-xs font-bold text-[#9BB7FF] font-mono">REASONING</span>
                <span className="text-[9px] text-[rgba(245,247,250,0.40)]">Multi-Model</span>
              </div>
              <div className="p-3.5 rounded-xl bg-[#0A0C0F] border border-[rgba(255,255,255,0.08)] flex flex-col gap-1">
                <span className="text-[10px] font-mono text-[rgba(245,247,250,0.55)]">04 LAYER</span>
                <span className="text-xs font-bold text-[#7CF7C5] font-mono">DECISION</span>
                <span className="text-[9px] text-[rgba(245,247,250,0.40)]">Action Plan</span>
              </div>
            </div>

            {/* Feature Bullets */}
            <div className="flex flex-col gap-3.5 pt-2">
              <div className="flex items-start gap-3">
                <div className="w-5 h-5 rounded bg-[#7CF7C5]/10 border border-[#7CF7C5]/30 flex items-center justify-center text-[#7CF7C5] font-mono text-[10px] shrink-0 mt-0.5">
                  ✓
                </div>
                <div className="text-xs">
                  <span className="font-semibold text-[#F5F7FA]">Capability-Aware Dynamic Routing:</span>
                  <span className="text-[rgba(245,247,250,0.55)] ml-1 font-light">Routes inference requests across verified providers with automated secondary fallback.</span>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="w-5 h-5 rounded bg-[#9BB7FF]/10 border border-[#9BB7FF]/30 flex items-center justify-center text-[#9BB7FF] font-mono text-[10px] shrink-0 mt-0.5">
                  ✓
                </div>
                <div className="text-xs">
                  <span className="font-semibold text-[#F5F7FA]">Real-Time Token Accounting & FinOps:</span>
                  <span className="text-[rgba(245,247,250,0.55)] ml-1 font-light">Every token consumed is tracked per workspace, agent mission, and user.</span>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column: Gateway Terminal / Pipeline Inspector */}
          <div className="lg:col-span-6 p-6 sm:p-8 rounded-2xl bg-[#0A0C0F] border border-[rgba(255,255,255,0.10)] shadow-2xl flex flex-col gap-5 relative font-mono text-xs">
            {/* Terminal Top Bar */}
            <div className="flex items-center justify-between border-b border-[rgba(255,255,255,0.08)] pb-3">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-rose-500/80" />
                <span className="w-2.5 h-2.5 rounded-full bg-amber-500/80" />
                <span className="w-2.5 h-2.5 rounded-full bg-[#7CF7C5]" />
                <span className="text-[11px] text-[rgba(245,247,250,0.55)] ml-2">model_gateway_pipeline.py</span>
              </div>
              <span className="text-[10px] text-[#7CF7C5]">STREAMING_ACTIVE</span>
            </div>

            {/* Terminal Code Trace */}
            <div className="flex flex-col gap-2.5 text-[rgba(245,247,250,0.85)]">
              <div className="text-[rgba(245,247,250,0.40)]"># 1. Authoritative Request with Tenant Context</div>
              <div className="text-[#9BB7FF]">
                POST /api/v1/ai/generate → Auth: Bearer [SESSION_HMAC]
              </div>
              <div className="text-[rgba(245,247,250,0.40)]"># 2. Context Extraction & DLP Sanitization</div>
              <div className="text-[#7CF7C5]">
                [DLP Sentinel] 0 secrets detected • Context graph retrieved
              </div>
              <div className="text-[rgba(245,247,250,0.40)]"># 3. Model Gateway Routing (OpenRouter)</div>
              <div className="text-[#F5F7FA]">
                [Router] Target: openrouter/auto → Status: 200 OK (38ms latency)
              </div>
              <div className="text-[rgba(245,247,250,0.40)]"># 4. Token & Cost Attribution</div>
              <div className="text-[#FFB86B]">
                [FinOps] Attribution: ws_default_01 • Token budget verified
              </div>
            </div>

            {/* Status Footer */}
            <div className="pt-3 border-t border-[rgba(255,255,255,0.08)] flex items-center justify-between text-[11px] text-[rgba(245,247,250,0.55)]">
              <span>Circuit Breaker: CLOSED</span>
              <span className="text-[#7CF7C5]">● 100% OPERATIONAL</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
