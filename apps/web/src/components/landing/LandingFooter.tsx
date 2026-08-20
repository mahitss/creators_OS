'use client';

import React from 'react';
import Link from 'next/link';

export function LandingFooter() {
  return (
    <footer className="py-12 bg-[#050505] border-t border-[rgba(255,255,255,0.08)] text-[rgba(245,247,250,0.55)] font-mono text-xs">
      <div className="max-w-7xl mx-auto px-6 sm:px-8 flex flex-col md:flex-row items-center justify-between gap-6">
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
        <div className="flex items-center gap-6 text-[11px] text-[rgba(245,247,250,0.55)]">
          <a href="#system" className="hover:text-[#7CF7C5] transition-colors">System</a>
          <a href="#intelligence" className="hover:text-[#7CF7C5] transition-colors">Intelligence</a>
          <a href="#automation" className="hover:text-[#7CF7C5] transition-colors">Automation</a>
          <a href="#security" className="hover:text-[#7CF7C5] transition-colors">Security</a>
          <Link href="/login" className="hover:text-[#7CF7C5] transition-colors">Sign In</Link>
        </div>

        {/* Copyright */}
        <div className="text-[10px] text-[rgba(245,247,250,0.40)]">
          © {new Date().getFullYear()} KINETIQ. All rights reserved.
        </div>
      </div>
    </footer>
  );
}
