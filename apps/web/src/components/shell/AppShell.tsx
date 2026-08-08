'use client';

import React, { useState, useEffect } from 'react';
import { Sidebar, NavItem } from './Sidebar';
import { TopBar } from './TopBar';
import { CommandPalette } from './CommandPalette';
import { UserSession } from './UserMenu';

export interface AppShellProps {
  children: React.ReactNode;
}

export const AppShell: React.FC<AppShellProps> = ({ children }) => {
  const [isMobileOpen, setIsMobileOpen] = useState(false);
  const [isCommandPaletteOpen, setIsCommandPaletteOpen] = useState(false);

  // Real authenticated user state (simulated for foundation shell context)
  const [user, setUser] = useState<UserSession>({
    name: 'Alex Chen',
    email: 'alex@vaporos.io',
    avatarUrl: null,
  });

  const navItems: NavItem[] = [
    { id: 'nav-home', label: 'Home', href: '/', icon: <span>🏠</span>, isAvailable: true },
    { id: 'nav-missions', label: 'Missions', href: '/missions', icon: <span>⚡</span>, isAvailable: true },
    { id: 'nav-content', label: 'Content', href: '/content', icon: <span>🎨</span>, isAvailable: true },
    { id: 'nav-memory', label: 'Memory', href: '/memory', icon: <span>🧠</span>, isAvailable: true },
    { id: 'nav-settings', label: 'Settings', href: '/settings', icon: <span>⚙️</span>, isAvailable: true },
  ];

  const handleSignOut = () => {
    // Clear session token & redirect
    document.cookie = 'vapor_session_token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    window.location.href = '/';
  };

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setIsCommandPaletteOpen((prev) => !prev);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <div className="min-h-screen flex bg-[#090A0F] text-slate-100 antialiased overflow-hidden">
      {/* Sidebar Navigation */}
      <Sidebar
        navItems={navItems}
        isMobileOpen={isMobileOpen}
        onMobileClose={() => setIsMobileOpen(false)}
      />

      {/* Main Viewport Column */}
      <div className="flex-1 flex flex-col min-w-0 lg:pl-60 transition-all duration-200">
        {/* Top Header Bar */}
        <TopBar
          user={user}
          onOpenCommandPalette={() => setIsCommandPaletteOpen(true)}
          onOpenMobileSidebar={() => setIsMobileOpen(true)}
          onSignOut={handleSignOut}
        />

        {/* Main Content Workspace Container */}
        <main className="flex-1 overflow-y-auto p-6 flex flex-col">
          {children}
        </main>
      </div>

      {/* Command Palette Modal */}
      <CommandPalette
        isOpen={isCommandPaletteOpen}
        onClose={() => setIsCommandPaletteOpen(false)}
        onSignOut={handleSignOut}
      />
    </div>
  );
};
