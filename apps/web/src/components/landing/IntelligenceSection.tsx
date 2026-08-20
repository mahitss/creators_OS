'use client';

import React from 'react';

export function IntelligenceSection() {
  return (
    <section id="intelligence" className="py-28 bg-[#080A0D] border-t border-slate-900 relative">
      <div className="max-w-7xl mx-auto px-6 sm:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          {/* Left Column: Technical Overview */}
          <div className="lg:col-span-6 flex flex-col gap-6">
            <div className="inline-flex items-center gap-2 text-xs font-mono text-cyan-400 tracking-widest uppercase">
              <span>[ 03 // MODEL GATEWAY ]</span>
            </div>
            <h2 className="text-3xl sm:text-4xl font-bold text-white tracking-tight">
              Enterprise AI Gateway & Multi-Model Routing.
            </h2>
            <p className="text-slate-400 text-base leading-relaxed font-light">
              Kinetiq operates a secure model gateway integrated directly with OpenRouter and leading enterprise foundation models. No raw API keys are ever exposed client-side. Every inference call is streamed via Server-Sent Events (SSE), budgeted in real time, and protected by automated fallback circuit breakers.
            </p>

            {/* Feature Bullet List */}
            <div className="flex flex-col gap-4 pt-2">
              <div className="flex items-start gap-3">
                <div className="w-6 h-6 rounded bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 font-mono text-xs shrink-0 mt-0.5">
                  ✓
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-white">Dynamic Model Routing & Fallback</h4>
                  <p className="text-xs text-slate-400 font-light mt-0.5">
                    Route requests intelligently across OpenAI, Anthropic, DeepSeek, and open-source models with automated secondary provider failover on latency spikes.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="w-6 h-6 rounded bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 font-mono text-xs shrink-0 mt-0.5">
                  ✓
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-white">Real-Time Token Accounting & FinOps</h4>
                  <p className="text-xs text-slate-400 font-light mt-0.5">
                    Every token consumed by agents or users is attributed by workspace, user, and mission with automated budget ceiling enforcement.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="w-6 h-6 rounded bg-blue-500/10 border border-blue-500/30 flex items-center justify-center text-blue-400 font-mono text-xs shrink-0 mt-0.5">
                  ✓
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-white">Zero-Trust DLP & Prompt Sanitization</h4>
                  <p className="text-xs text-slate-400 font-light mt-0.5">
                    Credentials, API keys, and sensitive PII are automatically masked and sanitized before payloads leave the enterprise perimeter.
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column: Gateway Terminal / Diagram Card */}
          <div className="lg:col-span-6 p-6 sm:p-8 rounded-2xl bg-[#0B0E12] border border-slate-800 shadow-2xl flex flex-col gap-5 relative font-mono text-xs">
            {/* Terminal Top Bar */}
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-rose-500/80" />
                <span className="w-2.5 h-2.5 rounded-full bg-amber-500/80" />
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-500/80" />
                <span className="text-[11px] text-slate-400 ml-2 font-mono">gateway_pipeline.py</span>
              </div>
              <span className="text-[10px] text-cyan-400">STREAMING_ACTIVE</span>
            </div>

            {/* Terminal Code Trace */}
            <div className="flex flex-col gap-2.5 text-slate-300">
              <div className="text-slate-400"># 1. Incoming Inference Request with Tenant Context</div>
              <div className="text-cyan-300">
                POST /api/v1/ai/generate → Auth: Bearer [SESSION_HMAC]
              </div>
              <div className="text-slate-400"># 2. Policy & DLP Validation</div>
              <div className="text-emerald-400">
                [DLP Sentinel] 0 sensitive credentials detected in prompt
              </div>
              <div className="text-slate-400"># 3. Model Gateway Routing (OpenRouter)</div>
              <div className="text-blue-300">
                [Router] Primary: openrouter/auto → Status: 200 OK (38ms latency)
              </div>
              <div className="text-slate-400"># 4. Token & Cost Attribution</div>
              <div className="text-amber-300">
                [FinOps] Prompt: 482 tok | Completion: 194 tok | Spend: $0.0014
              </div>
            </div>

            {/* Status Footer */}
            <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
              <span>Circuit Breaker: CLOSED</span>
              <span className="text-emerald-400">● 100% HEALTHY</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
