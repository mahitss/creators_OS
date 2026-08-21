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
    if (path === '/' || path === '/home' || path === '/workspace') return 'Workspace Home';
    if (path.startsWith('/missions')) return 'Missions Orchestration';
    if (path.startsWith('/content')) return 'Studio Content';
    if (path.startsWith('/memory')) return 'Context Vault Memory';
    if (path.startsWith('/settings')) return 'System Settings';
    return 'Kinetiq';
  };

  return (
    <header className="h-14 bg-[#050505] border-b border-[rgba(255,255,255,0.08)] px-4 flex items-center justify-between gap-4 sticky top-0 z-30 shrink-0">
      {/* Left: Mobile Menu Toggle & Title */}
      <div className="flex items-center gap-3">
        <IconButton
          ariaLabel="Open Navigation Menu"
          icon={<span className="text-sm">☰</span>}
          onClick={onOpenMobileSidebar}
          size="sm"
          className="lg:hidden"
        />
        <h1 className="text-xs font-medium text-[#F5F5F5] font-sans tracking-wide">
          {getPageTitle(pathname)}
        </h1>
      </div>

      {/* Right: Command Palette Trigger & User Menu */}
      <div className="flex items-center gap-3">
        <button
          onClick={onOpenCommandPalette}
          className="hidden sm:flex items-center gap-2 px-3 py-1.5 bg-[#0A0A0A] border border-[rgba(255,255,255,0.10)] rounded-md text-xs text-[#B5B5B5] hover:text-[#F5F5F5] hover:border-[rgba(255,255,255,0.16)] transition-colors"
          aria-label="Open Command Palette"
        >
          <span>Search or command...</span>
          <kbd className="px-1.5 py-0.5 text-[10px] font-mono bg-[#050505] text-[#666666] rounded border border-[rgba(255,255,255,0.10)]">
            ⌘K
          </kbd>
        </button>

        <UserMenu user={user} onSignOut={onSignOut} />
      </div>
    </header>
  );
};
