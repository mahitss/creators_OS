'use client';

import React from 'react';
import Link from 'next/link';

export function FinalCtaSection() {
  const scrollToTop = (e: React.MouseEvent) => {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <section className="py-32 bg-[#050505] border-t border-[rgba(255,255,255,0.08)] relative overflow-hidden text-center">
      {/* Background Ambient Glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[400px] bg-[#7CF7C5]/10 blur-[140px] pointer-events-none rounded-full" />

      <div className="max-w-4xl mx-auto px-6 sm:px-8 relative z-10 flex flex-col items-center gap-6">
        <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-[#0A0C0F] border border-[rgba(255,255,255,0.10)] text-[11px] font-mono text-[#7CF7C5]">
          <span>◈ READY FOR ENTERPRISE DEPLOYMENT</span>
        </div>

        <h2 className="text-4xl sm:text-6xl font-bold text-[#F5F7FA] tracking-tight font-sans">
          THE ENTERPRISE <br />
          INTELLIGENCE LAYER <br />
          IS HERE.
        </h2>

        <p className="text-base sm:text-lg text-[rgba(245,247,250,0.55)] font-light max-w-2xl leading-relaxed">
          Access your secure Kinetiq workspace, orchestrate autonomous missions, and govern multi-agent operations with cryptographic certainty.
        </p>

        <div className="pt-4 flex flex-col sm:flex-row items-center gap-4">
          <Link
            href="/login"
            className="px-8 py-4 rounded-xl bg-gradient-to-r from-[#7CF7C5] via-[#7CF7C5] to-[#9BB7FF] hover:opacity-90 text-[#050505] font-bold text-sm font-mono tracking-wider uppercase transition-all shadow-[0_0_30px_rgba(124,247,197,0.3)] hover:shadow-[0_0_45px_rgba(124,247,197,0.5)] active:scale-95"
          >
            [ ENTER KINETIQ ]
          </Link>

          <button
            onClick={scrollToTop}
            className="px-6 py-4 rounded-xl bg-[#0A0C0F] hover:bg-[#12161F] border border-[rgba(255,255,255,0.10)] text-[rgba(245,247,250,0.55)] hover:text-[#F5F7FA] font-mono text-sm tracking-wider uppercase transition-all"
          >
            RETURN TO TOP ↑
          </button>
        </div>

        <div className="text-xs font-mono text-[rgba(245,247,250,0.40)] pt-4 flex items-center gap-2">
          <span>Google Identity Verification</span>
          <span>•</span>
          <span>Zero-Trust RBAC</span>
          <span>•</span>
          <span>Tenant Isolated Workspaces</span>
        </div>
      </div>
    </section>
  );
}
