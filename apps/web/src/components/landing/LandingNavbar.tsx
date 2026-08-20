'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';

export function LandingNavbar() {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLiveHealthy, setIsLiveHealthy] = useState(true);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll, { passive: true });

    // Check auth status quietly
    fetch('/api/v1/auth/me', { credentials: 'include' })
      .then(r => r.ok ? r.json() : null)
      .then(data => {
        if (data?.authenticated) setIsAuthenticated(true);
      })
      .catch(() => {});

    // Check system health
    fetch('/api/v1/health')
      .then(r => r.ok ? r.json() : null)
      .then(data => {
        if (data?.status === 'healthy') setIsLiveHealthy(true);
      })
      .catch(() => {});

    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        isScrolled
          ? 'bg-[#050608]/90 backdrop-blur-md border-b border-slate-800/80 py-3 shadow-2xl shadow-black/90'
          : 'bg-transparent py-5'
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 sm:px-8 flex items-center justify-between">
        {/* Brand */}
        <Link href="/" className="flex items-center gap-3 group">
          <div className="w-8 h-8 rounded-lg bg-[#0B0E12] border border-cyan-500/30 flex items-center justify-center shadow-[0_0_15px_rgba(0,240,255,0.15)] group-hover:border-cyan-400/60 transition-all">
            <span className="w-2.5 h-2.5 rounded-full bg-cyan-400 shadow-[0_0_8px_rgba(0,240,255,0.8)] animate-pulse" />
          </div>
          <div className="flex flex-col">
            <span className="font-mono font-bold tracking-[0.2em] text-white text-base leading-none">
              KINETIQ
            </span>
            <span className="text-[9px] font-mono tracking-widest text-slate-400 uppercase mt-0.5">
              SPATIAL OS
            </span>
          </div>
        </Link>

        {/* Center Nav Links */}
        <nav className="hidden md:flex items-center gap-8 text-xs font-mono tracking-wider text-slate-400">
          <a href="#system" className="hover:text-cyan-300 transition-colors">
            SYSTEM
          </a>
          <a href="#architecture" className="hover:text-cyan-300 transition-colors">
            ARCHITECTURE
          </a>
          <a href="#intelligence" className="hover:text-cyan-300 transition-colors">
            INTELLIGENCE
          </a>
          <a href="#governance" className="hover:text-cyan-300 transition-colors">
            GOVERNANCE
          </a>
          <a href="#security" className="hover:text-cyan-300 transition-colors">
            SECURITY
          </a>
        </nav>

        {/* Right CTA & Live Health Indicator */}
        <div className="flex items-center gap-4">
          {/* Live Status Pill */}
          <div className="hidden sm:flex items-center gap-2 px-3 py-1 rounded-full bg-[#0B0E12] border border-slate-800 text-[11px] font-mono">
            <span className={`w-2 h-2 rounded-full ${isLiveHealthy ? 'bg-emerald-400 animate-pulse shadow-[0_0_8px_rgba(16,185,129,0.8)]' : 'bg-amber-400'}`} />
            <span className="text-slate-400">CORE</span>
            <span className="text-emerald-400 font-semibold">{isLiveHealthy ? 'OPERATIONAL' : 'DEGRADED'}</span>
          </div>

          {/* Primary Action Button */}
          <Link
            href={isAuthenticated ? '/home' : '/login'}
            className="px-4 py-2 rounded-lg bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-black font-semibold text-xs font-mono tracking-wider uppercase transition-all shadow-[0_0_20px_rgba(0,240,255,0.25)] hover:shadow-[0_0_30px_rgba(0,240,255,0.4)] active:scale-95"
          >
            {isAuthenticated ? 'Open Workspace →' : 'Enter Kinetiq →'}
          </Link>
        </div>
      </div>
    </header>
  );
}
