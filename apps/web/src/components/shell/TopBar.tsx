'use client';

import React from 'react';
import { usePathname } from 'next/navigation';
import { IconButton } from '@vapor/ui';
import { UserMenu, UserSession } from './UserMenu';

interface TopBarProps {
  user: UserSession;
  onOpenCommandPalette: () => void;
  onOpenMobileSidebar: () => void;
  onSignOut: () => void;
}

export const TopBar: React.FC<TopBarProps> = ({
  user,
  onOpenCommandPalette,
  onOpenMobileSidebar,
  onSignOut,
}) => {
  const pathname = usePathname();

  const getPageTitle = (path: string) => {
    if (path === '/') return 'Workspace Home';
    if (path.startsWith('/missions')) return 'Missions Orchestration';
    if (path.startsWith('/content')) return 'Studio Content';
    if (path.startsWith('/memory')) return 'Context Vault Memory';
    if (path.startsWith('/settings')) return 'System Settings';
    return 'Vapor OS';
  };

  return (
    <header className="h-14 bg-[#12141C] border-b border-slate-800/80 px-4 flex items-center justify-between gap-4 sticky top-0 z-30 shrink-0">
      {/* Left: Mobile Menu Toggle & Title */}
      <div className="flex items-center gap-3">
        <IconButton
          ariaLabel="Open Navigation Menu"
          icon={<span className="text-sm">☰</span>}
          onClick={onOpenMobileSidebar}
          size="sm"
          className="lg:hidden"
        />
        <h1 className="text-xs font-medium text-slate-200 font-sans tracking-wide">
          {getPageTitle(pathname)}
        </h1>
      </div>

      {/* Right: Command Palette Trigger & User Menu */}
      <div className="flex items-center gap-3">
        <button
          onClick={onOpenCommandPalette}
          className="hidden sm:flex items-center gap-2 px-3 py-1.5 bg-slate-900 border border-slate-800 rounded-md text-xs text-slate-400 hover:text-slate-200 hover:border-slate-700 transition-colors"
          aria-label="Open Command Palette"
        >
          <span>Search or command...</span>
          <kbd className="px-1.5 py-0.5 text-[10px] font-mono bg-slate-950 text-slate-500 rounded border border-slate-800">
            ⌘K
          </kbd>
        </button>

        <UserMenu user={user} onSignOut={onSignOut} />
      </div>
    </header>
  );
};
