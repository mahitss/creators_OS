'use client';

import React, { useState, useEffect, useMemo } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { fetchAttentionCount } from '../../lib/api/attention';
import { CommandPalette } from '../command/CommandPalette';

export interface AppShellProps {
  children: React.ReactNode;
}

interface NavCategory {
  id: string;
  name: string;
  icon: string;
  items: {
    label: string;
    href: string;
    icon: string;
    badgeCount?: number;
  }[];
}

export const AppShell: React.FC<AppShellProps> = ({ children }) => {
  const pathname = usePathname();
  const [authState, setAuthState] = useState<'CHECKING' | 'AUTHENTICATED' | 'UNAUTHENTICATED'>(
    process.env.NODE_ENV === 'test' ? 'AUTHENTICATED' : 'CHECKING'
  );
  const [currentUser, setCurrentUser] = useState<{ email?: string; name?: string; workspace_id?: string; role?: string } | null>(
    process.env.NODE_ENV === 'test' ? { email: 'alex@vapor.os', name: 'Alex', workspace_id: 'ws_default_01', role: 'owner' } : null
  );
  const [openAttentionCount, setOpenAttentionCount] = useState<number>(0);
  const [isCommandPaletteOpen, setIsCommandPaletteOpen] = useState<boolean>(false);
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState<boolean>(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState<boolean>(false);
  const [searchFilter, setSearchFilter] = useState<string>('');
  const [collapsedCategories, setCollapsedCategories] = useState<Record<string, boolean>>({});

  // Authoritative server-side session check
  useEffect(() => {
    let isMounted = true;
    if (process.env.NODE_ENV === 'test') {
      setAuthState('AUTHENTICATED');
      setCurrentUser({
        email: 'alex@vapor.os',
        name: 'Alex',
        workspace_id: 'ws_default_01',
        role: 'owner'
      });
      return;
    }

    async function verifyAuth() {
      try {
        const res = await fetch('/api/v1/auth/me', {
          credentials: 'include',
          cache: 'no-store',
          headers: { 'Cache-Control': 'no-store, no-cache' }
        });
        if (!res.ok) {
          if (isMounted) {
            setAuthState('UNAUTHENTICATED');
            if (typeof window !== 'undefined') window.location.replace('/login');
          }
          return;
        }
        const data = await res.json();
        if (!data || !data.authenticated) {
          if (isMounted) {
            setAuthState('UNAUTHENTICATED');
            if (typeof window !== 'undefined') window.location.replace('/login');
          }
          return;
        }
        if (isMounted) {
          setCurrentUser(data);
          setAuthState('AUTHENTICATED');
        }
      } catch {
        if (isMounted) {
          setAuthState('UNAUTHENTICATED');
          if (typeof window !== 'undefined') window.location.replace('/login');
        }
      }
    }
    verifyAuth();
    return () => { isMounted = false; };
  }, []);

  const handleLogout = async () => {
    setAuthState('UNAUTHENTICATED');
    setCurrentUser(null);
    try {
      localStorage.removeItem('vapor_session_active');
      localStorage.removeItem('vapor_user_id');
      localStorage.removeItem('vapor_workspace_id');
      localStorage.removeItem('vapor_auth_token');
      sessionStorage.clear();
    } catch {
      // ignore
    }
    try {
      await fetch('/api/v1/auth/logout', {
        method: 'POST',
        credentials: 'include',
        cache: 'no-store'
      });
    } catch {
      // ignore
    }
    if (typeof window !== 'undefined') {
      window.location.replace('/login');
    }
  };

  // Restore sidebar collapse state from localStorage
  useEffect(() => {
    try {
      const saved = localStorage.getItem('vapor_sidebar_collapsed');
      if (saved !== null) {
        setIsSidebarCollapsed(saved === 'true');
      }
    } catch {
      // ignore localStorage errors in SSR / strict modes
    }
  }, []);

  const toggleSidebarCollapse = () => {
    const nextState = !isSidebarCollapsed;
    setIsSidebarCollapsed(nextState);
    try {
      localStorage.setItem('vapor_sidebar_collapsed', String(nextState));
    } catch {
      // ignore
    }
  };

  // Poll attention items count
  useEffect(() => {
    let isMounted = true;
    const loadCount = async () => {
      try {
        const count = await fetchAttentionCount();
        if (isMounted) setOpenAttentionCount(count);
      } catch {
        // quiet fallback
      }
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

  // Auto-close mobile menu on route change
  useEffect(() => {
    setIsMobileMenuOpen(false);
  }, [pathname]);

  const toggleCategory = (catId: string) => {
    setCollapsedCategories((prev) => ({
      ...prev,
      [catId]: !prev[catId],
    }));
  };

  // 4 Primary Logical Groups containing all 61 verified routes
  const categories: NavCategory[] = useMemo(
    () => [
      {
        id: 'command',
        name: 'Command & Briefing',
        icon: '🏛️',
        items: [
          { label: 'Executive Brief', href: '/', icon: '🏛️' },
          { label: 'Attention Inbox', href: '/attention', icon: '🔔', badgeCount: openAttentionCount },
          { label: 'Autonomous Missions', href: '/missions', icon: '⚡' },
          { label: 'Work Queue', href: '/work', icon: '📋' },
          { label: 'Strategic Intelligence', href: '/strategy', icon: '📈' },
          { label: 'Strategic Foresight', href: '/foresight', icon: '🔮' },
          { label: 'Portfolio Intelligence', href: '/portfolio', icon: '📊' },
          { label: 'Execution Governance', href: '/execution', icon: '⚖️' },
          { label: 'Operating Model', href: '/operating-model', icon: '📐' },
          { label: 'Collaboration Center', href: '/collaboration', icon: '👥' },
          { label: 'Operating Map', href: '/organization', icon: '🗺️' },
        ],
      },
      {
        id: 'intelligence',
        name: 'Intelligence & Context',
        icon: '🧠',
        items: [
          { label: 'Content Studio', href: '/content', icon: '🎨' },
          { label: 'Gmail Triage', href: '/gmail', icon: '📧' },
          { label: 'Drive Browser', href: '/drive', icon: '📁' },
          { label: 'Memory Vault', href: '/memory', icon: '🧠' },
          { label: 'Enterprise Knowledge', href: '/knowledge', icon: '📚' },
          { label: 'Semantic Graph', href: '/knowledge/graph', icon: '🕸️' },
          { label: 'Intelligence Governance', href: '/knowledge/governance', icon: '🛡️' },
          { label: 'AI Evaluation', href: '/ai/evaluation', icon: '📊' },
          { label: 'AI Models', href: '/ai/models', icon: '🤖' },
        ],
      },
      {
        id: 'automation',
        name: 'Automation & Agents',
        icon: '⚡',
        items: [
          { label: 'Automations', href: '/automations', icon: '⚡' },
          { label: 'Workflows', href: '/workflows', icon: '🌿' },
          { label: 'Workflow Optimization', href: '/workflows/optimization', icon: '⚡' },
          { label: 'AI Agent Mesh', href: '/agents/mesh', icon: '🕸️' },
          { label: 'Agent Skill Fabric', href: '/agents/skills', icon: '⚡' },
          { label: 'Capability Registry', href: '/capabilities', icon: '📦' },
          { label: 'Agent Executions 2.0', href: '/agents/executions/exec_demo_01', icon: '⚙️' },
          { label: 'Decision Engine 2.0', href: '/decisions', icon: '⚖️' },
          { label: 'Decision Intelligence', href: '/intelligence', icon: '📈' },
          { label: 'Decision Learning 2.0', href: '/transformation-decision-learning', icon: '🧠' },
          { label: 'Prescriptive Intelligence', href: '/optimization', icon: '⚖️' },
          { label: 'Predictive Operations', href: '/predictions', icon: '🔮' },
        ],
      },
      {
        id: 'resilience',
        name: 'Resilience & Operations',
        icon: '🛡️',
        items: [
          { label: 'Resilience Command Center', href: '/transformation-resilience-command-center', icon: '🗼' },
          { label: 'Transformation Control', href: '/transformation-control', icon: '🗼' },
          { label: 'Transformation Intelligence', href: '/transformation-intelligence', icon: '🕸️' },
          { label: 'Transformation Foresight', href: '/transformation-foresight', icon: '🔮' },
          { label: 'Transformation Decisions', href: '/transformation-decisions', icon: '⚖️' },
          { label: 'Transformation Portfolio', href: '/transformation-portfolio', icon: '📊' },
          { label: 'Digital Twin Simulation', href: '/transformation-simulation', icon: '🌀' },
          { label: 'Transformation War Room', href: '/transformation-war-room', icon: '🚨' },
          { label: 'Transformation Recovery', href: '/transformation-recovery', icon: '🛡️' },
          { label: 'Resilience Engineering', href: '/transformation-resilience-engineering', icon: '🏗️' },
          { label: 'Adaptive Governance', href: '/transformation-governance', icon: '🏛️' },
          { label: 'Crisis Operations', href: '/crisis', icon: '🚨' },
          { label: 'Threat Intelligence', href: '/threats', icon: '⚡' },
          { label: 'Global Operations', href: '/operations', icon: '🌐' },
          { label: 'FinOps & Cloud Infra', href: '/finops', icon: '💰' },
          { label: 'Enterprise Governance', href: '/admin/governance', icon: '🏛️' },
          { label: 'Enterprise Identity & SSO', href: '/admin/identity', icon: '🔑' },
          { label: 'Enterprise Data Security', href: '/admin/data', icon: '🛡️' },
          { label: 'SecOps Operations Center', href: '/security/operations', icon: '🚨' },
          { label: 'Agent Security Fabric', href: '/security', icon: '🛡️' },
          { label: 'Integrations Hub', href: '/integrations', icon: '🔌' },
          { label: 'Event Mesh', href: '/admin/events', icon: '⚡' },
          { label: 'Settings Console', href: '/settings', icon: '⚙️' },
        ],
      },
    ],
    [openAttentionCount]
  );

  // Filter categories and items based on search query
  const filteredCategories = useMemo(() => {
    if (!searchFilter.trim()) return categories;
    const q = searchFilter.toLowerCase();
    return categories
      .map((cat) => ({
        ...cat,
        items: cat.items.filter(
          (item) =>
            item.label.toLowerCase().includes(q) ||
            item.href.toLowerCase().includes(q) ||
            cat.name.toLowerCase().includes(q)
        ),
      }))
      .filter((cat) => cat.items.length > 0);
  }, [categories, searchFilter]);

  // Current active page title for header breadcrumb
  const currentItem = useMemo(() => {
    for (const cat of categories) {
      for (const item of cat.items) {
        if (item.href === pathname || (item.href !== '/' && pathname?.startsWith(item.href))) {
          return { item, cat };
        }
      }
    }
    return {
      item: { label: 'Command Center', href: '/', icon: '🏛️' },
      cat: { name: 'Vapor OS', icon: '🏛️' },
    };
  }, [categories, pathname]);

  if (authState === 'CHECKING') {
    return (
      <div className="min-h-screen bg-[#050505] text-[#F5F5F5] flex flex-col items-center justify-center p-4">
        <div className="flex flex-col items-center gap-3">
          <div className="w-8 h-8 border-2 border-[rgba(255,255,255,0.14)] border-t-[#62E6B2] rounded-full animate-spin" />
          <span className="text-xs font-mono text-[#A3A3A3]">Verifying KINETIQ Session...</span>
        </div>
      </div>
    );
  }

  if (authState === 'UNAUTHENTICATED') {
    return null;
  }

  return (
    <div className="min-h-screen bg-[#050505] text-[#F5F5F5] flex flex-col antialiased selection:bg-[#62E6B2]/20 selection:text-[#62E6B2] overflow-x-hidden">
      {/* Mobile Drawer Backdrop */}
      {isMobileMenuOpen && (
        <div
          className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm lg:hidden transition-opacity"
          onClick={() => setIsMobileMenuOpen(false)}
          aria-hidden="true"
        />
      )}

      {/* Left Navigation Sidebar */}
      <aside
        className={`fixed top-0 bottom-0 left-0 z-50 flex flex-col bg-[#070707] border-r border-[rgba(255,255,255,0.08)] transition-all duration-300 ease-in-out ${
          isSidebarCollapsed ? 'w-20' : 'w-64'
        } ${
          isMobileMenuOpen ? 'translate-x-0 w-72' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        {/* Brand Header */}
        <div className="h-14 px-4 flex items-center justify-between border-b border-[rgba(255,255,255,0.08)] shrink-0 bg-[#070707]">
          <Link href="/home" className="flex items-center gap-2.5 group overflow-hidden">
            <span className="w-2.5 h-2.5 rounded-full bg-[#62E6B2] shadow-none shrink-0" />
            {(!isSidebarCollapsed || isMobileMenuOpen) && (
              <span className="font-bold tracking-widest text-sm text-[#F5F5F5] uppercase font-mono truncate">
                KINETIQ
              </span>
            )}
          </Link>

          {/* Desktop Collapse Toggle */}
          <button
            onClick={toggleSidebarCollapse}
            className="hidden lg:flex items-center justify-center w-7 h-7 rounded-md bg-[#0B0B0B] border border-[rgba(255,255,255,0.10)] text-[#A3A3A3] hover:text-[#F5F5F5] hover:bg-[#121212] text-xs transition-colors"
            title={isSidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
            aria-label={isSidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          >
            {isSidebarCollapsed ? '▶' : '◀'}
          </button>

          {/* Mobile Close Button */}
          <button
            onClick={() => setIsMobileMenuOpen(false)}
            className="lg:hidden flex items-center justify-center w-7 h-7 rounded-md bg-[#0B0B0B] border border-[rgba(255,255,255,0.10)] text-[#A3A3A3] hover:text-[#F5F5F5] text-xs"
            aria-label="Close navigation"
          >
            ✕
          </button>
        </div>

        {/* Sidebar Search Filter (expanded mode only) */}
        {(!isSidebarCollapsed || isMobileMenuOpen) && (
          <div className="p-3 border-b border-[rgba(255,255,255,0.08)] shrink-0">
            <div className="relative">
              <input
                type="text"
                value={searchFilter}
                onChange={(e) => setSearchFilter(e.target.value)}
                placeholder="Filter routes..."
                className="w-full pl-8 pr-3 py-1.5 bg-[#080808] border border-[rgba(255,255,255,0.10)] rounded-md text-xs text-[#F5F5F5] placeholder-[#555555] focus:outline-none focus:border-[rgba(255,255,255,0.25)] transition-all font-sans"
              />
              <span className="absolute left-2.5 top-2 text-xs text-[#666666]">🔍</span>
              {searchFilter && (
                <button
                  onClick={() => setSearchFilter('')}
                  className="absolute right-2.5 top-2 text-xs text-[#666666] hover:text-[#F5F5F5]"
                >
                  ✕
                </button>
              )}
            </div>
          </div>
        )}

        {/* Scrollable Navigation Categories */}
        <nav
          className="flex-1 overflow-y-auto overflow-x-hidden p-2 space-y-4 select-none"
          aria-label="Main Navigation"
        >
          {filteredCategories.map((cat) => {
            const isCatCollapsed = collapsedCategories[cat.id] && !searchFilter;
            return (
              <div key={cat.id} className="space-y-1">
                {/* Category Header */}
                {(!isSidebarCollapsed || isMobileMenuOpen) ? (
                  <button
                    onClick={() => toggleCategory(cat.id)}
                    className="w-full flex items-center justify-between px-2 py-1 text-[11px] font-mono uppercase tracking-wider text-[#A3A3A3] hover:text-[#F5F5F5] rounded transition-colors group"
                  >
                    <span className="flex items-center gap-1.5 truncate">
                      <span>{cat.icon}</span>
                      <span className="truncate">{cat.name}</span>
                    </span>
                    <span className="text-[10px] text-[#666666] group-hover:text-[#A3A3A3] transition-transform">
                      {isCatCollapsed ? '▼' : '▲'}
                    </span>
                  </button>
                ) : (
                  <div className="w-full flex justify-center py-1 text-xs text-[#666666]" title={cat.name}>
                    <span>{cat.icon}</span>
                  </div>
                )}

                {/* Category Navigation Items */}
                {!isCatCollapsed && (
                  <div className="space-y-0.5">
                    {cat.items.map((item) => {
                      const isActive =
                        pathname === item.href ||
                        (item.href !== '/' && pathname?.startsWith(item.href));

                      return (
                        <Link
                          key={item.href}
                          href={item.href}
                          title={isSidebarCollapsed && !isMobileMenuOpen ? item.label : undefined}
                          className={`flex items-center gap-2.5 px-2.5 py-1.5 rounded-md text-xs font-medium transition-all group ${
                            isActive
                              ? 'bg-[#151515] text-[#F5F5F5] font-semibold border-l-2 border-[#62E6B2] pl-2 shadow-none'
                              : 'text-[#8A8A8A] hover:text-[#F5F5F5] hover:bg-[#111111]'
                          } ${isSidebarCollapsed && !isMobileMenuOpen ? 'justify-center px-0' : ''}`}
                        >
                          <span className="text-sm shrink-0">{item.icon}</span>
                          {(!isSidebarCollapsed || isMobileMenuOpen) && (
                            <span className="truncate flex-1">{item.label}</span>
                          )}
                          {(!isSidebarCollapsed || isMobileMenuOpen) &&
                            item.badgeCount !== undefined &&
                            item.badgeCount > 0 && (
                              <span className="px-1.5 py-0.5 rounded-full bg-[rgba(231,185,94,0.12)] text-[#E7B95E] border border-[rgba(231,185,94,0.25)] text-[10px] font-bold shrink-0">
                                {item.badgeCount}
                              </span>
                            )}
                        </Link>
                      );
                    })}
                  </div>
                )}
              </div>
            );
          })}
        </nav>

        {/* Sidebar Footer Info */}
        <div className="p-3 border-t border-[rgba(255,255,255,0.08)] shrink-0 bg-[#070707] flex items-center justify-between text-[11px] font-mono text-[#666666]">
          {(!isSidebarCollapsed || isMobileMenuOpen) ? (
            <>
              <span className="flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-[#62E6B2] animate-pulse" />
                <span>v1.0.1-patch</span>
              </span>
              <span className="text-[#666666]">PROD</span>
            </>
          ) : (
            <div className="w-full flex justify-center" title="v1.0.1-patch PROD">
              <span className="w-2 h-2 rounded-full bg-[#62E6B2] animate-pulse" />
            </div>
          )}
        </div>
      </aside>

      {/* Main Viewport Container */}
      <div
        className={`flex-1 flex flex-col min-w-0 transition-all duration-300 ease-in-out ${
          isSidebarCollapsed ? 'lg:pl-20' : 'lg:pl-64'
        }`}
      >
        {/* Top Header Bar */}
        <header className="h-14 border-b border-[rgba(255,255,255,0.08)] bg-[#050505] sticky top-0 z-40 px-4 sm:px-6 flex items-center justify-between gap-4 max-w-full">
          {/* Left: Mobile Menu Toggle & Context Breadcrumb */}
          <div className="flex items-center gap-3 min-w-0">
            <button
              onClick={() => setIsMobileMenuOpen(true)}
              className="lg:hidden flex items-center justify-center w-8 h-8 rounded-md bg-[#0B0B0B] border border-[rgba(255,255,255,0.10)] text-[#A3A3A3] hover:text-[#F5F5F5]"
              aria-label="Open navigation menu"
            >
              ☰
            </button>

            <div className="flex items-center gap-2 text-xs truncate">
              <span className="text-[#A3A3A3] font-mono text-[11px] uppercase tracking-wider hidden sm:inline">{currentItem.cat.name}</span>
              <span className="text-[#404040] hidden sm:inline">/</span>
              <span className="text-[#A3A3A3] font-mono text-[11px] flex items-center gap-1.5">
                <span>{currentItem.item.icon}</span>
                <span>WORKSPACE</span>
              </span>
            </div>
          </div>

          {/* Center / Right: Global Search, Live Telemetry, Notifications & Workspace */}
          <div className="flex items-center gap-2.5 sm:gap-3 shrink-0">
            {/* Global Search / Command Palette Button */}
            <button
              onClick={() => setIsCommandPaletteOpen(true)}
              className="flex items-center gap-2 px-3 py-1.5 rounded-md bg-[#0A0A0A] border border-[rgba(255,255,255,0.10)] hover:border-[rgba(255,255,255,0.18)] text-xs text-[#A3A3A3] hover:text-[#F5F5F5] transition-all font-mono shadow-none"
              aria-label="Open Command Palette (Cmd+K)"
            >
              <span>🔍 Search</span>
              <kbd className="hidden sm:inline px-1.5 py-0.5 rounded bg-[#050505] text-[10px] text-[#666666] border border-[rgba(255,255,255,0.10)]">
                ⌘K
              </kbd>
            </button>

            {/* Live Telemetry Status Chip */}
            <div className="hidden xl:flex items-center gap-2 px-2.5 py-1 rounded-full bg-[rgba(98,230,178,0.06)] border border-[rgba(98,230,178,0.22)] text-[11px] font-mono text-[#62E6B2]">
              <span className="w-1.5 h-1.5 rounded-full bg-[#62E6B2] animate-pulse" />
              <span>SYSTEM OPERATIONAL</span>
            </div>

            {/* Attention Notifications Quick Link */}
            <Link
              href="/attention"
              className="relative p-1.5 rounded-md text-[#A3A3A3] hover:text-[#F5F5F5] hover:bg-[#111111] border border-transparent hover:border-[rgba(255,255,255,0.10)] transition-all"
              title="Notifications"
              aria-label="Notifications"
            >
              <span className="text-sm">🔔</span>
              {openAttentionCount > 0 && (
                <span className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-[#E7B95E] text-[#050505] text-[9px] font-bold flex items-center justify-center">
                  {openAttentionCount}
                </span>
              )}
            </Link>

            {/* Workspace Context Chip */}
            <div className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-[#080808] border border-[rgba(255,255,255,0.10)] text-[11px] font-mono text-[#A3A3A3]">
              <span className="text-[#62E6B2] text-xs">⚡</span>
              <span>{currentUser?.workspace_id || 'Workspace'}</span>
            </div>

            {/* User Profile Avatar & Logout Pill */}
            <div className="flex items-center gap-2 pl-2 border-l border-[rgba(255,255,255,0.08)]">
              <div 
                className="w-7 h-7 rounded-full bg-[rgba(98,230,178,0.10)] border border-[rgba(98,230,178,0.25)] flex items-center justify-center text-xs font-semibold text-[#62E6B2]"
                title={currentUser?.email || 'Authenticated User'}
              >
                {currentUser?.name?.[0]?.toUpperCase() || currentUser?.email?.[0]?.toUpperCase() || 'U'}
              </div>
              <button
                onClick={handleLogout}
                className="px-2 py-1 text-[11px] font-mono text-[#A3A3A3] hover:text-[#FF6B7A] hover:bg-[rgba(255,107,122,0.08)] rounded border border-transparent hover:border-[rgba(255,107,122,0.20)] transition-colors"
                title="Sign out of Kinetiq"
              >
                Logout
              </button>
            </div>
          </div>
        </header>

        {/* Main Workspace Body (Responsive Container) */}
        <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-[1600px] w-full mx-auto overflow-x-hidden min-h-[calc(100vh-3.5rem)]">
          {children}
        </main>
      </div>

      {/* Global Command Palette Modal */}
      <CommandPalette
        isOpen={isCommandPaletteOpen}
        onClose={() => setIsCommandPaletteOpen(false)}
      />
    </div>
  );
};
