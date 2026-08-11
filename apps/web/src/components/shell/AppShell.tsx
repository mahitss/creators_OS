'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { fetchAttentionCount } from '../../lib/api/attention';
import { CommandPalette } from '../command/CommandPalette';

export interface AppShellProps {
  children: React.ReactNode;
}

export const AppShell: React.FC<AppShellProps> = ({ children }) => {
  const pathname = usePathname();
  const [openAttentionCount, setOpenAttentionCount] = useState<number>(0);
  const [isCommandPaletteOpen, setIsCommandPaletteOpen] = useState<boolean>(false);

  useEffect(() => {
    let isMounted = true;
    const loadCount = async () => {
      const count = await fetchAttentionCount();
      if (isMounted) setOpenAttentionCount(count);
    };
    loadCount();
    const interval = setInterval(loadCount, 15000);
    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  // Global Cmd+K / Ctrl+K keyboard shortcut listener
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setIsCommandPaletteOpen((prev) => !prev);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const navItems = [
    { label: 'Executive Brief', href: '/', icon: '🏛️' },
    { label: 'Attention Center', href: '/attention', icon: '🔔', badgeCount: openAttentionCount },
    { label: 'Missions', href: '/missions', icon: '⚡' },
    { label: 'Content Canvas', href: '/content', icon: '🎨' },
    { label: 'Email Triage', href: '/gmail', icon: '✉️' },
    { label: 'Document Context', href: '/drive', icon: '📄' },
    { label: 'Context Memory', href: '/memory', icon: '🧠' },
    { label: 'Automations', href: '/automations', icon: '⚡' },
    { label: 'Workflows', href: '/workflows', icon: '🌿' },
    { label: 'FinOps & Infra', href: '/finops', icon: '💰' },
    { label: 'Enterprise Governance', href: '/admin/governance', icon: '🏛️' },
    { label: 'Enterprise Identity & SSO', href: '/admin/identity', icon: '🔑' },
    { label: 'Enterprise Data Security', href: '/admin/data', icon: '🛡️' },
    { label: 'Settings', href: '/settings', icon: '⚙️' },
  ];

  return (
    <div className="min-h-screen bg-[#0A0C10] text-slate-100 flex flex-col selection:bg-emerald-500/30 selection:text-emerald-200">
      {/* Top Application Header */}
      <header className="h-14 border-b border-slate-800/80 bg-[#0D0F17]/90 backdrop-blur sticky top-0 z-40 px-4 sm:px-6 flex items-center justify-between">
        <div className="flex items-center gap-6">
          <Link href="/" className="flex items-center gap-2 group">
            <span className="w-3 h-3 rounded-full bg-emerald-500 shadow-[0_0_12px_rgba(16,185,129,0.8)] group-hover:scale-110 transition-transform" />
            <span className="font-bold tracking-widest text-sm text-slate-100 uppercase font-mono">
              VAPOR<span className="text-emerald-400">_OS</span>
            </span>
          </Link>

          <nav className="hidden md:flex items-center gap-1">
            {navItems.map((item) => {
              const isActive = pathname === item.href || (item.href !== '/' && pathname?.startsWith(item.href));
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`px-3 py-1.5 rounded-md text-xs font-medium transition-all flex items-center gap-1.5 ${
                    isActive
                      ? 'bg-slate-800/90 text-emerald-400 border border-slate-700/60 shadow-sm'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
                  }`}
                >
                  <span>{item.icon}</span>
                  <span>{item.label}</span>
                  {item.badgeCount !== undefined && item.badgeCount > 0 && (
                    <span className="ml-1 px-1.5 py-0.2 rounded-full bg-amber-500/20 text-amber-400 border border-amber-500/40 text-[10px] font-bold">
                      {item.badgeCount}
                    </span>
                  )}
                </Link>
              );
            })}
          </nav>
        </div>

        <div className="flex items-center gap-3">
          {/* Global Search / Command Palette Trigger Button */}
          <button
            onClick={() => setIsCommandPaletteOpen(true)}
            className="flex items-center gap-2 px-3 py-1.5 rounded-md bg-slate-900 border border-slate-800 hover:border-slate-700 text-xs text-slate-400 hover:text-slate-200 transition-all font-mono"
          >
            <span>🔍 Search</span>
            <kbd className="px-1.5 py-0.5 rounded bg-slate-800 text-[10px] text-slate-400 border border-slate-700">
              ⌘K
            </kbd>
          </button>

          <div className="hidden sm:flex items-center gap-2 px-2.5 py-1 rounded-full bg-slate-900 border border-slate-800 text-[11px] font-mono text-slate-400">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
            <span>ws_default_01</span>
          </div>
        </div>
      </header>

      {/* Main Workspace Body */}
      <main className="flex-1 px-4 sm:px-6 py-6 flex flex-col max-w-7xl mx-auto w-full">
        {children}
      </main>

      {/* Mobile Bottom Navigation */}
      <div className="md:hidden fixed bottom-0 left-0 right-0 h-14 bg-[#0D0F17] border-t border-slate-800 flex items-center justify-around px-2 z-40">
        <button
          onClick={() => setIsCommandPaletteOpen(true)}
          className="flex flex-col items-center gap-0.5 text-slate-400"
        >
          <span className="text-base">🔍</span>
          <span className="text-[10px]">Search</span>
        </button>

        {navItems.map((item) => {
          const isActive = pathname === item.href || (item.href !== '/' && pathname?.startsWith(item.href));
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex flex-col items-center gap-0.5 relative ${
                isActive ? 'text-emerald-400' : 'text-slate-400'
              }`}
            >
              <span className="text-base">{item.icon}</span>
              <span className="text-[10px]">{item.label.split(' ')[0]}</span>
              {item.badgeCount !== undefined && item.badgeCount > 0 && (
                <span className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-amber-500 text-slate-950 text-[9px] font-bold flex items-center justify-center">
                  {item.badgeCount}
                </span>
              )}
            </Link>
          );
        })}
      </div>

      {/* Command Palette Modal */}
      <CommandPalette
        isOpen={isCommandPaletteOpen}
        onClose={() => setIsCommandPaletteOpen(false)}
      />
    </div>
  );
};
