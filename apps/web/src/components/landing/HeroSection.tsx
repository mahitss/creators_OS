'use client';

import React from 'react';
import Link from 'next/link';
import { KinetiqCanvas } from './KinetiqCanvas';

export function HeroSection() {
  return (
    <section className="relative min-h-[90vh] flex items-center justify-center pt-28 pb-16 overflow-hidden bg-[#050608]">
      {/* Background ambient lighting */}
      <div className="absolute top-1/3 left-1/4 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[500px] bg-gradient-to-tr from-cyan-500/10 via-blue-600/5 to-transparent blur-[140px] pointer-events-none rounded-full" />
      <div className="absolute bottom-10 right-1/4 w-[500px] h-[400px] bg-emerald-500/5 blur-[120px] pointer-events-none rounded-full" />

      {/* Subtle Grid Lines */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#0B0E12_1px,transparent_1px),linear-gradient(to_bottom,#0B0E12_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_40%,#000_70%,transparent_100%)] opacity-40 pointer-events-none" />

      <div className="max-w-7xl mx-auto px-6 sm:px-8 w-full grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-8 items-center relative z-10">
        {/* Left Column: Typography & CTAs */}
        <div className="lg:col-span-6 flex flex-col gap-6 text-left">
          {/* Eyebrow badge */}
          <div className="inline-flex items-center gap-2.5 px-3.5 py-1.5 rounded-full bg-[#080A0D] border border-cyan-500/30 w-fit shadow-[0_0_15px_rgba(0,240,255,0.1)]">
            <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse shadow-[0_0_6px_rgba(0,240,255,0.8)]" />
            <span className="text-[11px] font-mono tracking-widest text-cyan-300 uppercase">
              AUTONOMOUS ENTERPRISE KERNEL
            </span>
          </div>

          {/* Headline */}
          <div className="flex flex-col gap-2">
            <h1 className="text-4xl sm:text-6xl lg:text-7xl font-bold tracking-tight text-white font-sans leading-[1.05]">
              Spatial AI Operating System.
            </h1>
            <p className="text-lg sm:text-xl text-slate-300 font-sans font-light leading-relaxed max-w-xl">
              Kinetiq unifies enterprise context, multi-agent runtimes, continuous workflows, decision intelligence, and zero-trust governance inside one controlled operating environment.
            </p>
          </div>

          {/* Architecture Highlights Pill Row */}
          <div className="flex flex-wrap gap-2 pt-2">
            <span className="px-2.5 py-1 rounded bg-[#080A0D] border border-slate-800 text-[11px] font-mono text-slate-400">
              Zero-Trust Identity
            </span>
            <span className="px-2.5 py-1 rounded bg-[#080A0D] border border-slate-800 text-[11px] font-mono text-slate-400">
              Deterministic Agents
            </span>
            <span className="px-2.5 py-1 rounded bg-[#080A0D] border border-slate-800 text-[11px] font-mono text-slate-400">
              OpenRouter Multi-Gateway
            </span>
            <span className="px-2.5 py-1 rounded bg-[#080A0D] border border-slate-800 text-[11px] font-mono text-slate-400">
              Tenant Isolation
            </span>
          </div>

          {/* Actions */}
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-4 pt-4">
            <Link
              href="/login"
              className="px-6 py-3.5 rounded-xl bg-gradient-to-r from-cyan-500 via-cyan-400 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-black font-bold text-sm font-mono tracking-wider uppercase transition-all shadow-[0_0_25px_rgba(0,240,255,0.3)] hover:shadow-[0_0_35px_rgba(0,240,255,0.5)] text-center active:scale-95"
            >
              Enter Kinetiq →
            </Link>

            <a
              href="#architecture"
              className="px-6 py-3.5 rounded-xl bg-[#080A0D] hover:bg-[#0E121A] border border-slate-800 hover:border-slate-700 text-slate-300 hover:text-white font-mono text-sm tracking-wider uppercase transition-all text-center"
            >
              Explore Architecture ↓
            </a>
          </div>

          {/* Truthful Subtext */}
          <div className="text-[11px] font-mono text-slate-400 pt-2 flex items-center gap-2">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
            <span>Google OIDC • Strict RBAC/ABAC • AES-256 / HMAC Cryptography</span>
          </div>
        </div>

        {/* Right Column: 3D Spatial Canvas */}
        <div className="lg:col-span-6 flex items-center justify-center relative min-h-[420px] lg:min-h-[560px]">
          <div className="w-full h-full relative">
            <KinetiqCanvas />

            {/* Floating Spatial Label Badges */}
            <div className="absolute top-6 right-4 px-3 py-1.5 rounded-lg bg-[#080A0D]/90 border border-cyan-500/30 backdrop-blur-md text-[10px] font-mono text-cyan-300 shadow-lg pointer-events-none animate-bounce duration-1000">
              ◈ KINETIQ_CORE_v1.0
            </div>
            <div className="absolute bottom-6 left-4 px-3 py-1.5 rounded-lg bg-[#080A0D]/90 border border-emerald-500/30 backdrop-blur-md text-[10px] font-mono text-emerald-300 shadow-lg pointer-events-none">
              ◉ 683/683 KERNEL GATES VERIFIED
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
