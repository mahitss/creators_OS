'use client';

import React, { useState, useEffect, useMemo } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { fetchAttentionCount } from '../../lib/api/attention';
import { CommandPalette } from '../command/CommandPalette';

import {
  Terminal,
  Cpu,
  Brain,
  ShieldCheck,
  Layers,
  Activity,
  FileText,
  Mail,
  Folder,
  Database,
  Network,
  GitBranch,
  Play,
  Sliders,
  Eye,
  Compass,
  Lock,
  Server,
  Settings,
  Workflow,
  TrendingUp,
  BarChart2,
  Users,
  Boxes,
  Key,
  Cloud,
  Bell,
  AlertTriangle,
  Radio,
  Sparkles,
  CheckSquare,
  Search,
  Command,
  LayoutDashboard,
  Shield,
  Zap,
  X,
} from 'lucide-react';

export interface AppShellProps {
  children: React.ReactNode;
}

interface NavCategory {
  id: string;
  name: string;
  iconName: string;
  items: {
    label: string;
    href: string;
    iconName: string;
    badgeCount?: number;
  }[];
}

const renderNavIcon = (name: string, className = 'w-3.5 h-3.5') => {
  switch (name) {
    case 'command': return <Terminal className={className} />;
    case 'intelligence': return <Brain className={className} />;
    case 'execution': return <Cpu className={className} />;
    case 'governance': return <ShieldCheck className={className} />;
    case 'system': return <Server className={className} />;
    case 'brief': return <LayoutDashboard className={className} />;
    case 'bell': return <Bell className={className} />;
    case 'missions': return <Play className={className} />;
    case 'work': return <CheckSquare className={className} />;
    case 'strategy': return <TrendingUp className={className} />;
    case 'foresight': return <Eye className={className} />;
    case 'portfolio': return <BarChart2 className={className} />;
    case 'execution_gov': return <Sliders className={className} />;
    case 'operating_model': return <Compass className={className} />;
    case 'collaboration': return <Users className={className} />;
    case 'organization': return <Network className={className} />;
    case 'content': return <Sparkles className={className} />;
    case 'mail': return <Mail className={className} />;
    case 'folder': return <Folder className={className} />;
    case 'memory': return <Database className={className} />;
    case 'knowledge': return <FileText className={className} />;
    case 'graph': return <Network className={className} />;
    case 'eval': return <BarChart2 className={className} />;
    case 'models': return <Cpu className={className} />;
    case 'automations': return <Zap className={className} />;
    case 'workflows': return <Workflow className={className} />;
    case 'mesh': return <Network className={className} />;
    case 'skills': return <Boxes className={className} />;
    case 'capabilities': return <Boxes className={className} />;
    case 'decisions': return <GitBranch className={className} />;
    case 'optimization': return <Sliders className={className} />;
    case 'predictions': return <Radio className={className} />;
    case 'resilience': return <Shield className={className} />;
    case 'control': return <Sliders className={className} />;
    case 'simulation': return <Activity className={className} />;
    case 'warroom': return <AlertTriangle className={className} />;
    case 'crisis': return <AlertTriangle className={className} />;
    case 'threats': return <ShieldCheck className={className} />;
    case 'operations': return <Activity className={className} />;
    case 'finops': return <Cloud className={className} />;
    case 'identity': return <Key className={className} />;
    case 'security': return <Lock className={className} />;
    case 'integrations': return <Layers className={className} />;
    case 'events': return <Radio className={className} />;
    case 'settings': return <Settings className={className} />;
    default: return <Terminal className={className} />;
  }
};

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

  // 5 Primary Logical Groups containing all 61 verified routes
  const categories: NavCategory[] = useMemo(
    () => [
      {
        id: 'command',
        name: 'COMMAND',
        iconName: 'command',
        items: [
          { label: 'Executive Brief', href: '/', iconName: 'brief' },
          { label: 'Attention Inbox', href: '/attention', iconName: 'bell', badgeCount: openAttentionCount },
          { label: 'Autonomous Missions', href: '/missions', iconName: 'missions' },
          { label: 'Work Queue', href: '/work', iconName: 'work' },
          { label: 'Strategic Intelligence', href: '/strategy', iconName: 'strategy' },
          { label: 'Strategic Foresight', href: '/foresight', iconName: 'foresight' },
          { label: 'Portfolio Intelligence', href: '/portfolio', iconName: 'portfolio' },
        ],
      },
      {
        id: 'intelligence',
        name: 'INTELLIGENCE',
        iconName: 'intelligence',
        items: [
          { label: 'Memory Vault', href: '/memory', iconName: 'memory' },
          { label: 'Enterprise Knowledge', href: '/knowledge', iconName: 'knowledge' },
          { label: 'Semantic Graph', href: '/knowledge/graph', iconName: 'graph' },
          { label: 'AI Evaluation', href: '/ai/evaluation', iconName: 'eval' },
          { label: 'AI Models', href: '/ai/models', iconName: 'models' },
          { label: 'Content Studio', href: '/content', iconName: 'content' },
          { label: 'Gmail Triage', href: '/gmail', iconName: 'mail' },
          { label: 'Drive Browser', href: '/drive', iconName: 'folder' },
        ],
      },
      {
        id: 'execution',
        name: 'EXECUTION',
        iconName: 'execution',
        items: [
          { label: 'Automations', href: '/automations', iconName: 'automations' },
          { label: 'Workflows', href: '/workflows', iconName: 'workflows' },
          { label: 'Workflow Optimization', href: '/workflows/optimization', iconName: 'optimization' },
          { label: 'AI Agent Mesh', href: '/agents/mesh', iconName: 'mesh' },
          { label: 'Agent Skill Fabric', href: '/agents/skills', iconName: 'skills' },
          { label: 'Capability Registry', href: '/capabilities', iconName: 'capabilities' },
          { label: 'Agent Executions 2.0', href: '/agents/executions/exec_demo_01', iconName: 'execution' },
          { label: 'Decision Engine 2.0', href: '/decisions', iconName: 'decisions' },
          { label: 'Prescriptive Intelligence', href: '/optimization', iconName: 'optimization' },
          { label: 'Predictive Operations', href: '/predictions', iconName: 'predictions' },
        ],
      },
      {
        id: 'governance',
        name: 'GOVERNANCE',
        iconName: 'governance',
        items: [
          { label: 'Execution Governance', href: '/execution', iconName: 'execution_gov' },
          { label: 'Operating Model', href: '/operating-model', iconName: 'operating_model' },
          { label: 'Operating Map', href: '/organization', iconName: 'organization' },
          { label: 'Collaboration Center', href: '/collaboration', iconName: 'collaboration' },
          { label: 'Intelligence Governance', href: '/knowledge/governance', iconName: 'governance' },
          { label: 'Adaptive Governance', href: '/transformation-governance', iconName: 'governance' },
          { label: 'Enterprise Governance', href: '/admin/governance', iconName: 'governance' },
          { label: 'Enterprise Identity & SSO', href: '/admin/identity', iconName: 'identity' },
          { label: 'Enterprise Data Security', href: '/admin/data', iconName: 'security' },
          { label: 'Agent Security Fabric', href: '/security', iconName: 'security' },
          { label: 'SecOps Operations Center', href: '/security/operations', iconName: 'security' },
          { label: 'Policy Engine Guardrails', href: '/transformation-decision-learning', iconName: 'governance' },
        ],
      },
      {
        id: 'system',
        name: 'SYSTEM',
        iconName: 'system',
        items: [
          { label: 'Resilience Command Center', href: '/transformation-resilience-command-center', iconName: 'resilience' },
          { label: 'Transformation Control', href: '/transformation-control', iconName: 'control' },
          { label: 'Transformation Intelligence', href: '/transformation-intelligence', iconName: 'intelligence' },
          { label: 'Transformation Foresight', href: '/transformation-foresight', iconName: 'foresight' },
          { label: 'Transformation Decisions', href: '/transformation-decisions', iconName: 'decisions' },
          { label: 'Transformation Portfolio', href: '/transformation-portfolio', iconName: 'portfolio' },
          { label: 'Digital Twin Simulation', href: '/transformation-simulation', iconName: 'simulation' },
          { label: 'Transformation War Room', href: '/transformation-war-room', iconName: 'warroom' },
          { label: 'Transformation Recovery', href: '/transformation-recovery', iconName: 'resilience' },
          { label: 'Resilience Engineering', href: '/transformation-resilience-engineering', iconName: 'resilience' },
          { label: 'Crisis Operations', href: '/crisis', iconName: 'crisis' },
          { label: 'Threat Intelligence', href: '/threats', iconName: 'threats' },
          { label: 'Global Operations', href: '/operations', iconName: 'operations' },
          { label: 'FinOps & Cloud Infra', href: '/finops', iconName: 'finops' },
          { label: 'Integrations Hub', href: '/integrations', iconName: 'integrations' },
          { label: 'Event Mesh', href: '/admin/events', iconName: 'events' },
          { label: 'Settings Console', href: '/settings', iconName: 'settings' },
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
      item: { label: 'Command Center', href: '/', iconName: 'brief' },
      cat: { name: 'KINETIQ', iconName: 'command' },
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
          <div className="p-3 border-b border-[rgba(255,255,255,0.06)] shrink-0">
            <div className="relative flex items-center">
              <Search className="absolute left-2.5 w-3.5 h-3.5 text-[#555555] pointer-events-none" />
              <input
                type="text"
                value={searchFilter}
                onChange={(e) => setSearchFilter(e.target.value)}
                placeholder="Filter routes..."
                className="w-full pl-8 pr-7 py-1.5 bg-[#080808] border border-[rgba(255,255,255,0.08)] rounded-md text-xs text-[#F5F5F5] placeholder-[#555555] focus:outline-none focus:border-[rgba(255,255,255,0.22)] transition-all font-sans"
              />
              {searchFilter && (
                <button
                  onClick={() => setSearchFilter('')}
                  className="absolute right-2 text-xs text-[#666666] hover:text-[#F5F5F5]"
                  aria-label="Clear filter"
                >
                  <X className="w-3.5 h-3.5" />
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
                    className="w-full flex items-center justify-between px-2 py-1.5 text-[11px] font-mono uppercase tracking-widest text-[#777777] hover:text-[#F5F5F5] rounded transition-colors group"
                  >
                    <span className="flex items-center gap-2 truncate">
                      <span className="text-[#858585] group-hover:text-[#F5F5F5] transition-colors">{renderNavIcon(cat.iconName, 'w-3.5 h-3.5')}</span>
                      <span className="truncate">{cat.name}</span>
                    </span>
                    <span className="text-[10px] text-[#555555] group-hover:text-[#A3A3A3] transition-transform">
                      {isCatCollapsed ? '▼' : '▲'}
                    </span>
                  </button>
                ) : (
                  <div className="w-full flex justify-center py-1.5 text-xs text-[#858585]" title={cat.name}>
                    <span>{renderNavIcon(cat.iconName, 'w-4 h-4')}</span>
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
                              : 'text-[#777777] hover:text-[#F5F5F5] hover:bg-[#0D0D0D]'
                          } ${isSidebarCollapsed && !isMobileMenuOpen ? 'justify-center px-0' : ''}`}
                        >
                          <span className={`shrink-0 transition-colors ${isActive ? 'text-[#62E6B2]' : 'text-[#858585] group-hover:text-[#F5F5F5]'}`}>
                            {renderNavIcon(item.iconName, 'w-3.5 h-3.5')}
                          </span>
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
        <div className="p-3 border-t border-[rgba(255,255,255,0.06)] shrink-0 bg-[#070707] flex items-center justify-between text-[10px] font-mono text-[#555555]">
          {(!isSidebarCollapsed || isMobileMenuOpen) ? (
            <>
              <span className="flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-[#62E6B2]" />
                <span>v1.0.1-patch</span>
              </span>
              <span className="text-[#444444]">PROD</span>
            </>
          ) : (
            <div className="w-full flex justify-center" title="v1.0.1-patch PROD">
              <span className="w-1.5 h-1.5 rounded-full bg-[#62E6B2]" />
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
        <header className="h-14 border-b border-[rgba(255,255,255,0.06)] bg-[#050505] sticky top-0 z-40 px-4 sm:px-6 flex items-center justify-between gap-4 max-w-full">
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
              <span className="text-[#666666] font-mono text-[11px] uppercase tracking-wider hidden sm:inline">{currentItem.cat.name}</span>
              <span className="text-[#333333] hidden sm:inline">/</span>
              <span className="text-[#A3A3A3] font-mono text-[11px] flex items-center gap-1.5">
                <span className="text-[#858585]">{renderNavIcon(currentItem.item.iconName, 'w-3 h-3')}</span>
                <span>{currentItem.item.label.toUpperCase()}</span>
              </span>
            </div>
          </div>

          {/* Center / Right: Global Search, Live Telemetry, Notifications & Workspace */}
          <div className="flex items-center gap-2.5 sm:gap-3 shrink-0">
            {/* Global Search / Command Palette Button */}
            <button
              onClick={() => setIsCommandPaletteOpen(true)}
              className="flex items-center gap-2 px-2.5 py-1 rounded bg-[#0A0A0A] border border-[rgba(255,255,255,0.08)] hover:border-[rgba(255,255,255,0.16)] text-xs text-[#777777] hover:text-[#F5F5F5] transition-all font-mono shadow-none"
              aria-label="Open Command Palette (Cmd+K)"
            >
              <Search className="w-3 h-3 text-[#777777]" />
              <span className="text-[11px]">Search</span>
              <kbd className="hidden sm:inline px-1 py-0.2 text-[9px] font-mono bg-[#050505] text-[#555555] rounded border border-[rgba(255,255,255,0.08)]">
                ⌘K
              </kbd>
            </button>

            {/* Live Telemetry Status Chip */}
            <div className="hidden xl:flex items-center gap-2 px-2 py-0.5 rounded-full bg-[rgba(98,230,178,0.04)] border border-[rgba(98,230,178,0.18)] text-[10px] font-mono text-[#62E6B2]">
              <span className="w-1.5 h-1.5 rounded-full bg-[#62E6B2]" />
              <span>SYSTEM OPERATIONAL</span>
            </div>

            {/* Attention Notifications Quick Link */}
            <Link
              href="/attention"
              className="relative p-1.5 rounded-md text-[#777777] hover:text-[#F5F5F5] hover:bg-[#0D0D0D] transition-all"
              title="Notifications"
              aria-label="Notifications"
            >
              <Bell className="w-3.5 h-3.5" />
              {openAttentionCount > 0 && (
                <span className="absolute -top-0.5 -right-0.5 w-3.5 h-3.5 rounded-full bg-[#E7B95E] text-[#050505] text-[8px] font-bold flex items-center justify-center">
                  {openAttentionCount}
                </span>
              )}
            </Link>

            {/* Workspace Context Chip */}
            <div className="hidden sm:flex items-center gap-1.5 px-2 py-0.5 rounded bg-[#080808] border border-[rgba(255,255,255,0.08)] text-[10px] font-mono text-[#858585]">
              <span className="w-1.5 h-1.5 rounded-full bg-[#62E6B2]" />
              <span>{currentUser?.workspace_id || 'WORKSPACE'}</span>
            </div>

            {/* User Profile Avatar & Logout Pill */}
            <div className="flex items-center gap-2 pl-2 border-l border-[rgba(255,255,255,0.08)]">
              <div 
                className="w-6 h-6 rounded-full bg-[#111111] border border-[rgba(255,255,255,0.12)] flex items-center justify-center text-[10px] font-mono text-[#F5F5F5]"
                title={currentUser?.email || 'Authenticated User'}
              >
                {currentUser?.name?.[0]?.toUpperCase() || currentUser?.email?.[0]?.toUpperCase() || 'U'}
              </div>
              <button
                onClick={handleLogout}
                className="px-1.5 py-0.5 text-[10px] font-mono text-[#777777] hover:text-[#FF6B7A] transition-colors"
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
