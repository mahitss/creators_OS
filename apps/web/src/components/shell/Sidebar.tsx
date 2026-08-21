'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { IconButton } from '@vapor/ui';

export interface NavItem {
  id: string;
  label: string;
  href: string;
  icon: React.ReactNode;
  isAvailable: boolean;
}

interface SidebarProps {
  navItems: NavItem[];
  isMobileOpen: boolean;
  onMobileClose: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ navItems, isMobileOpen, onMobileClose }) => {
  const pathname = usePathname();
  const [isCollapsed, setIsCollapsed] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem('vapor_sidebar_collapsed');
    if (saved) setIsCollapsed(saved === 'true');
  }, []);

  const toggleCollapse = () => {
    const nextState = !isCollapsed;
    setIsCollapsed(nextState);
    localStorage.setItem('vapor_sidebar_collapsed', String(nextState));
  };

  return (
    <>
      {/* Mobile Backdrop */}
      {isMobileOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/80 backdrop-blur-sm lg:hidden"
          onClick={onMobileClose}
          aria-hidden="true"
        />
      )}

      <aside
        className={`fixed top-0 bottom-0 left-0 z-40 flex flex-col bg-[#070707] border-r border-[rgba(255,255,255,0.08)] transition-all duration-200 ease-out ${
          isCollapsed ? 'w-16' : 'w-60'
        } ${
          isMobileOpen ? 'translate-x-0 w-64' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        {/* Header / Brand Logo */}
        <div className="flex items-center justify-between h-14 px-4 border-b border-[rgba(255,255,255,0.08)]">
          <Link href="/home" className="flex items-center gap-2.5 overflow-hidden">
            <span className="w-2.5 h-2.5 rounded-full bg-[#62E6B2] shadow-none shrink-0" />
            {(!isCollapsed || isMobileOpen) && (
              <span className="font-semibold tracking-wider text-[#F5F5F5] text-sm font-sans uppercase">
                KINETIQ
              </span>
            )}
          </Link>
          <IconButton
            ariaLabel={isCollapsed ? 'Expand Sidebar' : 'Collapse Sidebar'}
            icon={<span className="text-xs">{isCollapsed ? '→' : '←'}</span>}
            onClick={toggleCollapse}
            size="sm"
            className="hidden lg:flex"
          />
        </div>

        {/* Navigation Items */}
        <nav className="flex-1 py-3 px-2 flex flex-col gap-1 overflow-y-auto" aria-label="Main Navigation">
          {navItems.map((item) => {
            const isActive = pathname === item.href || (item.href !== '/' && pathname.startsWith(item.href));

            if (!item.isAvailable) {
              return (
                <div
                  key={item.id}
                  className={`flex items-center gap-3 px-3 py-2 text-xs rounded-md text-[#404040] cursor-not-allowed select-none ${
                    isCollapsed && !isMobileOpen ? 'justify-center' : ''
                  }`}
                  title={`${item.label} (Coming in Sprint 4)`}
                >
                  <span className="shrink-0 opacity-40">{item.icon}</span>
                  {(!isCollapsed || isMobileOpen) && (
                    <div className="flex items-center justify-between w-full">
                      <span>{item.label}</span>
                      <span className="text-[9px] font-mono uppercase bg-[#111111] text-[#666666] px-1.5 py-0.5 rounded border border-[rgba(255,255,255,0.06)]">
                        Soon
                      </span>
                    </div>
                  )}
                </div>
              );
            }

            return (
              <Link
                key={item.id}
                href={item.href}
                onClick={onMobileClose}
                className={`flex items-center gap-3 px-3 py-2 text-xs font-medium rounded-md transition-colors focus-visible:outline-none ${
                  isActive
                    ? 'bg-[#151515] text-[#F5F5F5] font-semibold border-l-2 border-[#62E6B2]'
                    : 'text-[#777777] hover:text-[#F5F5F5] hover:bg-[#0D0D0D]'
                } ${isCollapsed && !isMobileOpen ? 'justify-center px-0' : ''}`}
              >
                <span className={`shrink-0 ${isActive ? 'text-[#62E6B2]' : 'text-[#858585]'}`}>{item.icon}</span>
                {(!isCollapsed || isMobileOpen) && <span>{item.label}</span>}
              </Link>
            );
          })}
        </nav>

        {/* Sidebar Footer */}
        {(!isCollapsed || isMobileOpen) && (
          <div className="p-3 border-t border-[rgba(255,255,255,0.08)] text-[11px] font-mono text-[#666666]">
            KERNEL_V0.1.0 // ACTIVE
          </div>
        )}
      </aside>
    </>
  );
};
