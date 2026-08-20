'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';

export function LandingNavbar() {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll, { passive: true });

    // Check auth status quietly
    fetch('/api/v1/auth/me', { credentials: 'include' })
      .then(r => (r.ok ? r.json() : null))
      .then(data => {
        if (data?.authenticated) setIsAuthenticated(true);
      })
      .catch(() => {});

    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        isScrolled
          ? 'bg-[#050505]/95 backdrop-blur-md border-b border-[rgba(255,255,255,0.10)] py-4 shadow-2xl shadow-black/90'
          : 'bg-transparent py-6'
      }`}
    >
      <div className="w-full max-w-[1440px] mx-auto px-5 sm:px-8 lg:px-12 grid grid-cols-2 md:grid-cols-[1fr_auto_1fr] items-center">
        {/* Left: Brand Mark */}
        <Link href="/" className="flex items-center gap-3 group justify-self-start">
          <div className="w-8 h-8 rounded-lg bg-[#0A0C0F] border border-[rgba(255,255,255,0.15)] flex items-center justify-center shadow-[0_0_15px_rgba(124,247,197,0.1)] group-hover:border-[#7CF7C5]/50 transition-all shrink-0">
            <span className="w-2.5 h-2.5 rounded-full bg-[#7CF7C5] shadow-[0_0_8px_rgba(124,247,197,0.8)] animate-pulse" />
          </div>
          <div className="flex flex-col">
            <span className="font-mono font-bold tracking-[0.25em] text-[#F5F7FA] text-base leading-none">
              KINETIQ
            </span>
            <span className="text-[9px] font-mono tracking-widest text-[rgba(245,247,250,0.55)] uppercase mt-1 leading-tight">
              INTELLIGENCE OPERATING LAYER
            </span>
          </div>
        </Link>

        {/* Center: Navigation Links (Desktop) */}
        <nav className="hidden md:flex items-center gap-8 text-xs font-mono tracking-widest text-[rgba(245,247,250,0.55)] justify-self-center">
          <a href="#system" className="hover:text-[#7CF7C5] transition-colors py-1">
            SYSTEM
          </a>
          <a href="#intelligence" className="hover:text-[#7CF7C5] transition-colors py-1">
            INTELLIGENCE
          </a>
          <a href="#automation" className="hover:text-[#7CF7C5] transition-colors py-1">
            AUTOMATION
          </a>
          <a href="#security" className="hover:text-[#7CF7C5] transition-colors py-1">
            SECURITY
          </a>
        </nav>

        {/* Right: CTA Button */}
        <div className="flex items-center gap-4 justify-self-end">
          <Link
            href={isAuthenticated ? '/home' : '/login'}
            className="px-4 py-2.5 rounded-lg bg-[#0A0C0F] hover:bg-[#12161F] border border-[rgba(255,255,255,0.15)] hover:border-[#7CF7C5]/60 text-[#F5F7FA] hover:text-[#7CF7C5] font-mono font-semibold text-xs tracking-wider uppercase transition-all shadow-sm active:scale-95 whitespace-nowrap"
          >
            {isAuthenticated ? '[ OPEN WORKSPACE ]' : '[ ENTER KINETIQ ]'}
          </Link>
        </div>
      </div>
    </header>
  );
}
