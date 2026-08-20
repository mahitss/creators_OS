'use client';

import React from 'react';
import Link from 'next/link';

export function HeroSection() {
  return (
    <section className="relative min-h-[100svh] flex items-center justify-center pt-32 lg:pt-36 pb-16 lg:pb-24 overflow-hidden bg-[#050505] text-[#F5F7FA]">
      {/* Background ambient lighting */}
      <div className="absolute top-1/3 left-1/4 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[450px] bg-gradient-to-tr from-[#7CF7C5]/10 via-[#9BB7FF]/5 to-transparent blur-[140px] pointer-events-none rounded-full" />
      <div className="absolute bottom-10 right-1/4 w-[450px] h-[350px] bg-[#7CF7C5]/5 blur-[120px] pointer-events-none rounded-full" />

      {/* Subtle Technical Grid */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,0.035)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.035)_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_40%,#000_70%,transparent_100%)] pointer-events-none opacity-100" />

      <div className="w-full max-w-[1440px] mx-auto px-5 sm:px-8 lg:px-12 grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-10 items-center relative z-10">
        {/* Left Column: Typography & CTAs */}
        <div className="lg:col-span-7 flex flex-col items-start text-left max-w-[680px]">
          {/* Eyebrow badge */}
          <div className="inline-flex items-center gap-2.5 px-3.5 py-1.5 rounded-full bg-[#0A0C0F] border border-[rgba(255,255,255,0.12)] shadow-[0_0_15px_rgba(124,247,197,0.08)] mb-6">
            <span className="w-2 h-2 rounded-full bg-[#7CF7C5] shadow-[0_0_6px_rgba(124,247,197,0.8)]" />
            <span className="text-[11px] font-mono tracking-widest text-[#7CF7C5] uppercase font-semibold">
              KINETIQ / INTELLIGENCE OPERATING LAYER
            </span>
          </div>

          {/* Main Headline */}
          <div className="flex flex-col gap-2">
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight text-[#F5F7FA] font-sans leading-[1.08] max-w-[640px]">
              THE INTELLIGENCE <br />
              <span className="text-[#7CF7C5]">OPERATING</span> LAYER.
            </h1>
          </div>

          {/* Supporting Description */}
          <p className="text-base sm:text-lg text-[rgba(245,247,250,0.65)] font-sans font-light leading-relaxed max-w-[580px] mt-6">
            Connect intelligence, execution, and control in one autonomous enterprise system. Unify enterprise data, AI models, governed agents, workflows, and decisions under strict security boundaries.
          </p>

          {/* Technical Capability Tags */}
          <div className="flex flex-wrap gap-2 mt-6">
            <span className="px-3 py-1 rounded-md bg-[#0A0C0F] border border-[rgba(255,255,255,0.12)] text-[11px] font-mono text-[rgba(245,247,250,0.75)]">
              OpenRouter AI Gateway
            </span>
            <span className="px-3 py-1 rounded-md bg-[#0A0C0F] border border-[rgba(255,255,255,0.12)] text-[11px] font-mono text-[rgba(245,247,250,0.75)]">
              Zero-Trust Identity
            </span>
            <span className="px-3 py-1 rounded-md bg-[#0A0C0F] border border-[rgba(255,255,255,0.12)] text-[11px] font-mono text-[rgba(245,247,250,0.75)]">
              Policy Engine
            </span>
            <span className="px-3 py-1 rounded-md bg-[#0A0C0F] border border-[rgba(255,255,255,0.12)] text-[11px] font-mono text-[rgba(245,247,250,0.75)]">
              Tenant Isolation
            </span>
            <span className="px-3 py-1 rounded-md bg-[#0A0C0F] border border-[rgba(255,255,255,0.12)] text-[11px] font-mono text-[rgba(245,247,250,0.75)]">
              Agent Runtime
            </span>
          </div>

          {/* Action CTAs */}
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3.5 mt-8 w-full sm:w-auto">
            <Link
              href="/login"
              className="px-7 py-3.5 rounded-xl bg-gradient-to-r from-[#7CF7C5] via-[#7CF7C5] to-[#9BB7FF] hover:opacity-90 text-[#050505] font-bold text-sm font-mono tracking-wider uppercase transition-all shadow-[0_0_30px_rgba(124,247,197,0.25)] hover:shadow-[0_0_40px_rgba(124,247,197,0.45)] text-center active:scale-95 whitespace-nowrap"
            >
              ENTER KINETIQ →
            </Link>

            <a
              href="#system"
              className="px-6 py-3.5 rounded-xl bg-[#0A0C0F] hover:bg-[#12161F] border border-[rgba(255,255,255,0.15)] hover:border-[rgba(255,255,255,0.30)] text-[#F5F7FA] font-mono text-sm tracking-wider uppercase transition-all text-center whitespace-nowrap"
            >
              EXPLORE THE SYSTEM ↓
            </a>
          </div>

          {/* Cryptographic Subtext */}
          <div className="text-[11px] font-mono text-[rgba(245,247,250,0.45)] mt-6 flex items-center gap-2">
            <span className="w-1.5 h-1.5 rounded-full bg-[#7CF7C5]" />
            <span>Google OIDC • Server-Side Verification • Strict Tenant Boundaries</span>
          </div>
        </div>

        {/* Right Column: Clean Dark Computational Topology Panel */}
        <div className="lg:col-span-5 flex flex-col items-center justify-center relative w-full">
          {/* Engineering Topology Structure (Non-3D Guaranteed Fallback) */}
          <div className="w-full max-w-[460px] bg-[#0A0C0F] border border-[rgba(255,255,255,0.12)] rounded-2xl p-6 shadow-2xl relative overflow-hidden">
            {/* Header */}
            <div className="flex items-center justify-between pb-4 border-b border-[rgba(255,255,255,0.08)] mb-5">
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-[#7CF7C5] animate-pulse shadow-[0_0_8px_rgba(124,247,197,0.8)]" />
                <span className="text-xs font-mono font-bold text-[#F5F7FA] tracking-wider uppercase">
                  KINETIQ TOPOLOGY
                </span>
              </div>
              <span className="text-[10px] font-mono text-[rgba(245,247,250,0.45)] uppercase">
                CONTROL PLANE
              </span>
            </div>

            {/* Execution Graph Nodes */}
            <div className="grid grid-cols-2 gap-3 mb-5">
              <div className="p-3 rounded-xl bg-[#12151B] border border-[rgba(255,255,255,0.08)] flex flex-col gap-1">
                <span className="text-[10px] font-mono text-[rgba(245,247,250,0.45)]">01 INGEST</span>
                <span className="text-xs font-mono font-bold text-[#9BB7FF]">DATA FABRIC</span>
                <span className="text-[9px] font-mono text-[#7CF7C5]">STREAM ACTIVE</span>
              </div>
              <div className="p-3 rounded-xl bg-[#12151B] border border-[rgba(255,255,255,0.08)] flex flex-col gap-1">
                <span className="text-[10px] font-mono text-[rgba(245,247,250,0.45)]">02 ROUTER</span>
                <span className="text-xs font-mono font-bold text-[#7CF7C5]">MODEL GATEWAY</span>
                <span className="text-[9px] font-mono text-[#7CF7C5]">OPENROUTER READY</span>
              </div>
              <div className="p-3 rounded-xl bg-[#12151B] border border-[rgba(255,255,255,0.08)] flex flex-col gap-1">
                <span className="text-[10px] font-mono text-[rgba(245,247,250,0.45)]">03 GUARD</span>
                <span className="text-xs font-mono font-bold text-[#7CF7C5]">POLICY ENGINE</span>
                <span className="text-[9px] font-mono text-[#7CF7C5]">ZERO-TRUST ENFORCED</span>
              </div>
              <div className="p-3 rounded-xl bg-[#12151B] border border-[rgba(255,255,255,0.08)] flex flex-col gap-1">
                <span className="text-[10px] font-mono text-[rgba(245,247,250,0.45)]">04 RUNTIME</span>
                <span className="text-xs font-mono font-bold text-[#9BB7FF]">AGENT MESH</span>
                <span className="text-[9px] font-mono text-[#7CF7C5]">DETERMINISTIC</span>
              </div>
            </div>

            {/* Live Telemetry Status Row */}
            <div className="p-3.5 rounded-xl bg-[#050505] border border-[rgba(255,255,255,0.08)] flex flex-col gap-2 font-mono text-[11px]">
              <div className="flex items-center justify-between text-[10px] text-[rgba(245,247,250,0.45)] uppercase border-b border-[rgba(255,255,255,0.06)] pb-1.5">
                <span>SYSTEM TELEMETRY</span>
                <span className="text-[#7CF7C5]">STABLE</span>
              </div>
              <div className="grid grid-cols-2 gap-y-1.5 text-[10px]">
                <div className="flex items-center justify-between">
                  <span className="text-[rgba(245,247,250,0.55)]">GATEWAY</span>
                  <span className="text-[#7CF7C5]">ONLINE</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-[rgba(245,247,250,0.55)]">ROUTING</span>
                  <span className="text-[#9BB7FF]">ACTIVE</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-[rgba(245,247,250,0.55)]">POLICIES</span>
                  <span className="text-[#7CF7C5]">ENFORCED</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-[rgba(245,247,250,0.55)]">ISOLATION</span>
                  <span className="text-[#7CF7C5]">CRYPTOGRAPHIC</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
