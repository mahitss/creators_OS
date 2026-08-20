'use client';

import React from 'react';
import Link from 'next/link';

export function FinalCtaSection() {
  return (
    <section className="py-28 bg-[#080A0D] border-t border-slate-900 relative overflow-hidden text-center">
      {/* Background Ambient Glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[400px] bg-cyan-500/10 blur-[140px] pointer-events-none rounded-full" />

      <div className="max-w-4xl mx-auto px-6 sm:px-8 relative z-10 flex flex-col items-center gap-6">
        <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-[#050608] border border-cyan-500/30 text-[11px] font-mono text-cyan-300">
          <span>◈ ENTERPRISE READINESS APPROVED</span>
        </div>

        <h2 className="text-4xl sm:text-6xl font-bold text-white tracking-tight font-sans">
          Step into the Intelligent Operating System.
        </h2>

        <p className="text-base sm:text-lg text-slate-300 font-light max-w-2xl leading-relaxed">
          Access your secure Kinetiq workspace, orchestrate autonomous missions, and govern multi-agent operations with cryptographic certainty.
        </p>

        <div className="pt-4 flex flex-col sm:flex-row items-center gap-4">
          <Link
            href="/login"
            className="px-8 py-4 rounded-xl bg-gradient-to-r from-cyan-500 via-cyan-400 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-black font-bold text-sm font-mono tracking-wider uppercase transition-all shadow-[0_0_30px_rgba(0,240,255,0.35)] hover:shadow-[0_0_45px_rgba(0,240,255,0.6)] active:scale-95"
          >
            Enter Kinetiq →
          </Link>
        </div>

        <div className="text-xs font-mono text-slate-400 pt-4 flex items-center gap-2">
          <span>Google Identity Verification</span>
          <span>•</span>
          <span>Zero-Trust RBAC</span>
          <span>•</span>
          <span>Instant Workspace Provisioning</span>
        </div>
      </div>
    </section>
  );
}
