'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { KinetiqCanvas } from './KinetiqCanvas';

export function HeroSection() {
  // Coordinated System Boot Sequence Stage (0: black, 1: grid, 2: nodes, 3: connections, 4: 3d, 5: wordmark, 6: headline, 7: cta, 8: idle)
  const [bootStage, setBootStage] = useState<number>(0);

  useEffect(() => {
    const timers = [
      setTimeout(() => setBootStage(1), 300),
      setTimeout(() => setBootStage(2), 600),
      setTimeout(() => setBootStage(3), 900),
      setTimeout(() => setBootStage(4), 1200),
      setTimeout(() => setBootStage(5), 1500),
      setTimeout(() => setBootStage(6), 1800),
      setTimeout(() => setBootStage(7), 2100),
      setTimeout(() => setBootStage(8), 2500),
    ];
    return () => timers.forEach(clearTimeout);
  }, []);

  return (
    <section className="relative min-h-[95vh] flex items-center justify-center pt-28 pb-20 overflow-hidden bg-[#050505]">
      {/* Background ambient lighting */}
      <div className="absolute top-1/3 left-1/4 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[500px] bg-gradient-to-tr from-[#7CF7C5]/10 via-[#9BB7FF]/5 to-transparent blur-[140px] pointer-events-none rounded-full" />
      <div className="absolute bottom-10 right-1/4 w-[500px] h-[400px] bg-[#7CF7C5]/5 blur-[120px] pointer-events-none rounded-full" />

      {/* Subtle Technical Grid (Boot stage 1+) */}
      <div
        className={`absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,0.045)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.045)_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_40%,#000_70%,transparent_100%)] transition-opacity duration-1000 pointer-events-none ${
          bootStage >= 1 ? 'opacity-100' : 'opacity-0'
        }`}
      />

      <div className="max-w-7xl mx-auto px-6 sm:px-8 w-full grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-8 items-center relative z-10">
        {/* Left Column: Typography & CTAs */}
        <div className="lg:col-span-6 flex flex-col gap-6 text-left">
          {/* Eyebrow badge (Boot stage 2+) */}
          <div
            className={`inline-flex items-center gap-2.5 px-3.5 py-1.5 rounded-full bg-[#0A0C0F] border border-[rgba(255,255,255,0.10)] w-fit shadow-[0_0_15px_rgba(124,247,197,0.08)] transition-all duration-700 ${
              bootStage >= 2 ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-2'
            }`}
          >
            <span className="w-2 h-2 rounded-full bg-[#7CF7C5] animate-pulse shadow-[0_0_6px_rgba(124,247,197,0.8)]" />
            <span className="text-[11px] font-mono tracking-widest text-[#7CF7C5] uppercase">
              AUTONOMOUS ENTERPRISE SYSTEM
            </span>
          </div>

          {/* Headline & Wordmark (Boot stage 5 & 6) */}
          <div className="flex flex-col gap-3">
            <span
              className={`text-sm font-mono tracking-[0.3em] text-[#9BB7FF] uppercase transition-all duration-700 ${
                bootStage >= 5 ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-2'
              }`}
            >
              KINETIQ
            </span>
            <h1
              className={`text-4xl sm:text-6xl lg:text-7xl font-bold tracking-tight text-[#F5F7FA] font-sans leading-[1.05] transition-all duration-700 ${
                bootStage >= 6 ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-3'
              }`}
            >
              THE INTELLIGENCE <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#F5F7FA] via-[#7CF7C5] to-[#9BB7FF]">
                OPERATING LAYER.
              </span>
            </h1>
            <p
              className={`text-base sm:text-lg text-[rgba(245,247,250,0.55)] font-sans font-light leading-relaxed max-w-xl transition-all duration-700 ${
                bootStage >= 6 ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-3'
              }`}
            >
              Connect intelligence, execution, and control in one autonomous enterprise system. An intelligent operating layer uniting enterprise data, AI models, governed agents, workflows, and decisions.
            </p>
          </div>

          {/* Technical Specs Pill Row (Boot stage 7+) */}
          <div
            className={`flex flex-wrap gap-2 pt-1 transition-all duration-700 ${
              bootStage >= 7 ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-2'
            }`}
          >
            <span className="px-2.5 py-1 rounded bg-[#0A0C0F] border border-[rgba(255,255,255,0.10)] text-[11px] font-mono text-[rgba(245,247,250,0.55)]">
              Multi-Model AI Gateway
            </span>
            <span className="px-2.5 py-1 rounded bg-[#0A0C0F] border border-[rgba(255,255,255,0.10)] text-[11px] font-mono text-[rgba(245,247,250,0.55)]">
              Deterministic Agent Runtime
            </span>
            <span className="px-2.5 py-1 rounded bg-[#0A0C0F] border border-[rgba(255,255,255,0.10)] text-[11px] font-mono text-[rgba(245,247,250,0.55)]">
              Zero-Trust Identity & RBAC
            </span>
            <span className="px-2.5 py-1 rounded bg-[#0A0C0F] border border-[rgba(255,255,255,0.10)] text-[11px] font-mono text-[rgba(245,247,250,0.55)]">
              Tenant Isolation
            </span>
          </div>

          {/* Action CTAs (Boot stage 7+) */}
          <div
            className={`flex flex-col sm:flex-row items-stretch sm:items-center gap-4 pt-3 transition-all duration-700 ${
              bootStage >= 7 ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-3'
            }`}
          >
            <Link
              href="/login"
              className="px-7 py-3.5 rounded-xl bg-gradient-to-r from-[#7CF7C5] via-[#7CF7C5] to-[#9BB7FF] hover:opacity-90 text-[#050505] font-bold text-sm font-mono tracking-wider uppercase transition-all shadow-[0_0_30px_rgba(124,247,197,0.25)] hover:shadow-[0_0_40px_rgba(124,247,197,0.45)] text-center active:scale-95"
            >
              ENTER KINETIQ →
            </Link>

            <a
              href="#system"
              className="px-6 py-3.5 rounded-xl bg-[#0A0C0F] hover:bg-[#12161F] border border-[rgba(255,255,255,0.10)] hover:border-[rgba(255,255,255,0.25)] text-[#F5F7FA] font-mono text-sm tracking-wider uppercase transition-all text-center"
            >
              EXPLORE THE SYSTEM ↓
            </a>
          </div>

          {/* Cryptographic Subtext */}
          <div
            className={`text-[11px] font-mono text-[rgba(245,247,250,0.55)] pt-1 flex items-center gap-2 transition-all duration-700 ${
              bootStage >= 8 ? 'opacity-100' : 'opacity-0'
            }`}
          >
            <span className="w-1.5 h-1.5 rounded-full bg-[#7CF7C5]" />
            <span>Google OIDC • Server-Side Verification • Strict Tenant Boundaries</span>
          </div>
        </div>

        {/* Right Column: Procedural 3D Intelligence Structure (Boot stage 4+) */}
        <div
          className={`lg:col-span-6 flex items-center justify-center relative min-h-[420px] lg:min-h-[580px] transition-all duration-1000 ${
            bootStage >= 4 ? 'opacity-100 scale-100' : 'opacity-0 scale-95'
          }`}
        >
          <div className="w-full h-full relative">
            <KinetiqCanvas />

            {/* Spatial Status Indicators */}
            <div className="absolute top-6 right-4 px-3 py-1.5 rounded-lg bg-[#0A0C0F]/90 border border-[rgba(255,255,255,0.10)] backdrop-blur-md text-[10px] font-mono text-[#7CF7C5] shadow-lg pointer-events-none">
              ◈ KINETIQ_TOPOLOGY_ACTIVE
            </div>
            <div className="absolute bottom-6 left-4 px-3 py-1.5 rounded-lg bg-[#0A0C0F]/90 border border-[rgba(255,255,255,0.10)] backdrop-blur-md text-[10px] font-mono text-[#9BB7FF] shadow-lg pointer-events-none">
              ◉ DISTRIBUTED EXECUTION MESH
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
