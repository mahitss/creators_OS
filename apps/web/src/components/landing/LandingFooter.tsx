'use client';

import React from 'react';
import Link from 'next/link';

export function LandingFooter() {
  return (
    <footer className="relative py-14 sm:py-16 bg-[#050505] border-t border-[rgba(255,255,255,0.08)] text-[rgba(245,247,250,0.55)] font-mono text-xs">
      <div className="w-full max-w-[1440px] mx-auto px-5 sm:px-8 lg:px-12 flex flex-col md:flex-row items-center justify-between gap-6">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="w-6 h-6 rounded-md bg-[#0A0C0F] border border-[rgba(255,255,255,0.15)] flex items-center justify-center">
            <span className="w-2 h-2 rounded-full bg-[#7CF7C5]" />
          </div>
          <span className="font-bold text-[#F5F7FA] tracking-widest text-sm">
            KINETIQ
          </span>
          <span className="text-[10px] text-[rgba(245,247,250,0.40)]">
            • INTELLIGENCE OPERATING LAYER
          </span>
        </div>

        {/* Links */}
        <div className="flex flex-wrap items-center justify-center gap-6 text-[11px] text-[rgba(245,247,250,0.55)]">
          <a href="#system" className="hover:text-[#7CF7C5] transition-colors py-1">System</a>
          <a href="#intelligence" className="hover:text-[#7CF7C5] transition-colors py-1">Intelligence</a>
          <a href="#automation" className="hover:text-[#7CF7C5] transition-colors py-1">Automation</a>
          <a href="#security" className="hover:text-[#7CF7C5] transition-colors py-1">Security</a>
          <Link href="/login" className="hover:text-[#7CF7C5] transition-colors py-1">Sign In</Link>
        </div>

        {/* Copyright */}
        <div className="text-[10px] text-[rgba(245,247,250,0.40)]">
          © {new Date().getFullYear()} KINETIQ. All rights reserved.
        </div>
      </div>
    </footer>
  );
}
