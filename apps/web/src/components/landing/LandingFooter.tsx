'use client';

import React from 'react';
import Link from 'next/link';

export function LandingFooter() {
  return (
    <footer className="py-12 bg-[#050608] border-t border-slate-900 text-slate-400 font-mono text-xs">
      <div className="max-w-7xl mx-auto px-6 sm:px-8 flex flex-col md:flex-row items-center justify-between gap-6">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="w-6 h-6 rounded-md bg-[#0B0E12] border border-cyan-500/30 flex items-center justify-center">
            <span className="w-2 h-2 rounded-full bg-cyan-400" />
          </div>
          <span className="font-bold text-slate-200 tracking-widest text-sm">
            KINETIQ
          </span>
          <span className="text-[10px] text-slate-400">
            • AUTONOMOUS ENTERPRISE KERNEL
          </span>
        </div>

        {/* Links */}
        <div className="flex items-center gap-6 text-[11px] text-slate-400">
          <a href="#system" className="hover:text-cyan-300 transition-colors">System</a>
          <a href="#architecture" className="hover:text-cyan-300 transition-colors">Architecture</a>
          <a href="#intelligence" className="hover:text-cyan-300 transition-colors">Intelligence</a>
          <a href="#security" className="hover:text-cyan-300 transition-colors">Security</a>
          <Link href="/login" className="hover:text-cyan-300 transition-colors">Sign In</Link>
        </div>

        {/* Copyright */}
        <div className="text-[10px] text-slate-400">
          © {new Date().getFullYear()} KINETIQ. All rights reserved.
        </div>
      </div>
    </footer>
  );
}
