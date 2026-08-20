'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { KinetiqCanvas } from './KinetiqCanvas';

export function HeroSection() {
  const [bootStage, setBootStage] = useState<number>(0);

  useEffect(() => {
    const timers = [
      setTimeout(() => setBootStage(1), 200),
      setTimeout(() => setBootStage(2), 400),
      setTimeout(() => setBootStage(3), 600),
      setTimeout(() => setBootStage(4), 800),
      setTimeout(() => setBootStage(5), 1000),
      setTimeout(() => setBootStage(6), 1200),
      setTimeout(() => setBootStage(7), 1400),
      setTimeout(() => setBootStage(8), 1600),
    ];
    return () => timers.forEach(clearTimeout);
  }, []);

  return (
    <section className="relative min-h-[100svh] flex items-center justify-center pt-32 lg:pt-36 pb-16 lg:pb-24 overflow-hidden bg-[#050505]">
      {/* Background ambient lighting */}
      <div className="absolute top-1/3 left-1/4 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[450px] bg-gradient-to-tr from-[#7CF7C5]/10 via-[#9BB7FF]/5 to-transparent blur-[140px] pointer-events-none rounded-full" />
      <div className="absolute bottom-10 right-1/4 w-[450px] h-[350px] bg-[#7CF7C5]/5 blur-[120px] pointer-events-none rounded-full" />

      {/* Subtle Technical Grid */}
      <div
        className={`absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,0.035)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.035)_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_40%,#000_70%,transparent_100%)] transition-opacity duration-1000 pointer-events-none ${
          bootStage >= 1 ? 'opacity-100' : 'opacity-0'
        }`}
      />

      <div className="w-full max-w-[1440px] mx-auto px-5 sm:px-8 lg:px-12 grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-10 items-center relative z-10">
        {/* Left Column: Typography & CTAs */}
        <div className="lg:col-span-7 flex flex-col items-start text-left max-w-[680px]">
          {/* Eyebrow badge */}
          <div
            className={`inline-flex items-center gap-2.5 px-3.5 py-1.5 rounded-full bg-[#0A0C0F] border border-[rgba(255,255,255,0.10)] shadow-[0_0_15px_rgba(124,247,197,0.08)] mb-6 transition-all duration-700 ${
              bootStage >= 2 ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-2'
            }`}
          >
            <span className="w-2 h-2 rounded-full bg-[#7CF7C5] animate-pulse shadow-[0_0_6px_rgba(124,247,197,0.8)]" />
            <span className="text-[11px] font-mono tracking-widest text-[#7CF7C5] uppercase">
              KINETIQ / INTELLIGENCE OPERATING LAYER
            </span>
          </div>

          {/* Main Headline */}
          <div className="flex flex-col gap-2">
            <h1
              className={`text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight text-[#F5F7FA] font-sans leading-[1.08] max-w-[640px] transition-all duration-700 ${
                bootStage >= 5 ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-3'
              }`}
            >
              THE INTELLIGENCE <br />
              <span className="text-[#7CF7C5]">OPERATING</span> LAYER.
            </h1>
          </div>

          {/* Supporting Description */}
          <p
            className={`text-base sm:text-lg text-[rgba(245,247,250,0.60)] font-sans font-light leading-relaxed max-w-[580px] mt-6 transition-all duration-700 ${
              bootStage >= 6 ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-3'
            }`}
          >
            Connect intelligence, execution, and control in one autonomous enterprise system. Unify enterprise data, AI models, governed agents, workflows, and decisions under strict security boundaries.
          </p>

          {/* Technical Capability Tags */}
          <div
            className={`flex flex-wrap gap-2 mt-6 transition-all duration-700 ${
              bootStage >= 7 ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-2'
            }`}
          >
            <span className="px-3 py-1 rounded-md bg-[#0A0C0F] border border-[rgba(255,255,255,0.10)] text-[11px] font-mono text-[rgba(245,247,250,0.65)]">
              OpenRouter AI Gateway
            </span>
            <span className="px-3 py-1 rounded-md bg-[#0A0C0F] border border-[rgba(255,255,255,0.10)] text-[11px] font-mono text-[rgba(245,247,250,0.65)]">
              Zero-Trust Identity
            </span>
            <span className="px-3 py-1 rounded-md bg-[#0A0C0F] border border-[rgba(255,255,255,0.10)] text-[11px] font-mono text-[rgba(245,247,250,0.65)]">
              Policy Engine
            </span>
            <span className="px-3 py-1 rounded-md bg-[#0A0C0F] border border-[rgba(255,255,255,0.10)] text-[11px] font-mono text-[rgba(245,247,250,0.65)]">
              Tenant Isolation
            </span>
            <span className="px-3 py-1 rounded-md bg-[#0A0C0F] border border-[rgba(255,255,255,0.10)] text-[11px] font-mono text-[rgba(245,247,250,0.65)]">
              Agent Runtime
            </span>
          </div>

          {/* Action CTAs */}
          <div
            className={`flex flex-col sm:flex-row items-stretch sm:items-center gap-3.5 mt-8 w-full sm:w-auto transition-all duration-700 ${
              bootStage >= 7 ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-3'
            }`}
          >
            <Link
              href="/login"
              className="px-7 py-3.5 rounded-xl bg-gradient-to-r from-[#7CF7C5] via-[#7CF7C5] to-[#9BB7FF] hover:opacity-90 text-[#050505] font-bold text-sm font-mono tracking-wider uppercase transition-all shadow-[0_0_30px_rgba(124,247,197,0.25)] hover:shadow-[0_0_40px_rgba(124,247,197,0.45)] text-center active:scale-95 whitespace-nowrap"
            >
              ENTER KINETIQ →
            </Link>

            <a
              href="#system"
              className="px-6 py-3.5 rounded-xl bg-[#0A0C0F] hover:bg-[#12161F] border border-[rgba(255,255,255,0.10)] hover:border-[rgba(255,255,255,0.25)] text-[#F5F7FA] font-mono text-sm tracking-wider uppercase transition-all text-center whitespace-nowrap"
            >
              EXPLORE THE SYSTEM ↓
            </a>
          </div>

          {/* Cryptographic Subtext */}
          <div
            className={`text-[11px] font-mono text-[rgba(245,247,250,0.45)] mt-6 flex items-center gap-2 transition-all duration-700 ${
              bootStage >= 8 ? 'opacity-100' : 'opacity-0'
            }`}
          >
            <span className="w-1.5 h-1.5 rounded-full bg-[#7CF7C5]" />
            <span>Google OIDC • Server-Side Verification • Strict Tenant Boundaries</span>
          </div>
        </div>

        {/* Right Column: 3D Intelligence Topology Visual & Live Telemetry Panel */}
        <div
          className={`lg:col-span-5 flex flex-col items-center justify-center relative w-full transition-all duration-1000 ${
            bootStage >= 4 ? 'opacity-100 scale-100' : 'opacity-0 scale-95'
          }`}
        >
          {/* 3D Visual Container */}
          <div className="w-full min-h-[380px] sm:min-h-[440px] lg:min-h-[500px] relative flex items-center justify-center">
            <KinetiqCanvas />
          </div>

          {/* Real-time System Telemetry Panel */}
          <div className="w-full max-w-[420px] bg-[#0A0C0F]/90 backdrop-blur-md border border-[rgba(255,255,255,0.10)] rounded-xl p-4 shadow-xl -mt-6 relative z-20">
            <div className="flex items-center justify-between border-b border-[rgba(255,255,255,0.08)] pb-2 mb-3">
              <span className="text-[10px] font-mono tracking-widest text-[#7CF7C5] uppercase font-semibold flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-[#7CF7C5] animate-pulse" />
                SYSTEM TELEMETRY
              </span>
              <span className="text-[10px] font-mono text-[rgba(245,247,250,0.45)]">
                KINETIQ-RUNTIME-1.0
              </span>
            </div>
            <div className="grid grid-cols-2 gap-y-2 gap-x-4 text-[11px] font-mono">
              <div className="flex items-center justify-between">
                <span className="text-[rgba(245,247,250,0.50)]">AI GATEWAY</span>
                <span className="text-[#7CF7C5] font-semibold">ONLINE</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-[rgba(245,247,250,0.50)]">MODEL ROUTING</span>
                <span className="text-[#9BB7FF] font-semibold">ACTIVE</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-[rgba(245,247,250,0.50)]">POLICY ENGINE</span>
                <span className="text-[#7CF7C5] font-semibold">ENFORCED</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-[rgba(245,247,250,0.50)]">EVENT STREAM</span>
                <span className="text-[#7CF7C5] font-semibold">READY</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
