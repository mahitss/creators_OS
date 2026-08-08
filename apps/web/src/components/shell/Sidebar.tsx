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
        className={`fixed top-0 bottom-0 left-0 z-40 flex flex-col bg-[#12141C] border-r border-slate-800/80 transition-all duration-200 ease-out ${
          isCollapsed ? 'w-16' : 'w-60'
        } ${
          isMobileOpen ? 'translate-x-0 w-64' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        {/* Header / Brand Logo */}
        <div className="flex items-center justify-between h-14 px-4 border-b border-slate-800/80">
          <Link href="/" className="flex items-center gap-2.5 overflow-hidden">
            <span className="w-3 h-3 rounded-full bg-emerald-500 shrink-0" />
            {(!isCollapsed || isMobileOpen) && (
              <span className="font-semibold tracking-wide text-slate-100 text-sm font-sans">
                VAPOR <span className="text-xs font-mono text-emerald-400 font-normal">OS</span>
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
                  className={`flex items-center gap-3 px-3 py-2 text-xs rounded-md text-slate-600 cursor-not-allowed select-none ${
                    isCollapsed && !isMobileOpen ? 'justify-center' : ''
                  }`}
                  title={`${item.label} (Coming in Sprint 4)`}
                >
                  <span className="shrink-0 opacity-50">{item.icon}</span>
                  {(!isCollapsed || isMobileOpen) && (
                    <div className="flex items-center justify-between w-full">
                      <span>{item.label}</span>
                      <span className="text-[9px] font-mono uppercase bg-slate-800/60 text-slate-500 px-1.5 py-0.5 rounded">
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
                className={`flex items-center gap-3 px-3 py-2 text-xs font-medium rounded-md transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 ${
                  isActive
                    ? 'bg-emerald-500/10 text-emerald-400 font-semibold border-l-2 border-emerald-500'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                } ${isCollapsed && !isMobileOpen ? 'justify-center px-0' : ''}`}
              >
                <span className="shrink-0">{item.icon}</span>
                {(!isCollapsed || isMobileOpen) && <span>{item.label}</span>}
              </Link>
            );
          })}
        </nav>

        {/* Sidebar Footer */}
        {(!isCollapsed || isMobileOpen) && (
          <div className="p-3 border-t border-slate-800/80 text-[11px] font-mono text-slate-600">
            KERNEL_V0.1.0 // ACTIVE
          </div>
        )}
      </aside>
    </>
  );
};
