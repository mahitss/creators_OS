'use client';

import React from 'react';

export interface TabItem {
  id: string;
  label: string;
  badge?: string | number;
  disabled?: boolean;
}

export interface TabsProps {
  tabs: TabItem[];
  activeTabId: string;
  onChange: (tabId: string) => void;
  className?: string;
}

export const Tabs: React.FC<TabsProps> = ({ tabs, activeTabId, onChange, className = '' }) => {
  return (
    <div className={`flex items-center gap-1 border-b border-slate-800/80 ${className}`} role="tablist">
      {tabs.map((tab) => {
        const isActive = tab.id === activeTabId;
        return (
          <button
            key={tab.id}
            role="tab"
            aria-selected={isActive}
            disabled={tab.disabled}
            onClick={() => !tab.disabled && onChange(tab.id)}
            className={`flex items-center gap-2 px-3 py-2 text-xs font-medium border-b-2 transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 ${
              isActive
                ? 'border-emerald-500 text-emerald-400 font-semibold'
                : 'border-transparent text-slate-400 hover:text-slate-200 hover:border-slate-700'
            } ${tab.disabled ? 'opacity-40 cursor-not-allowed' : ''}`}
          >
            <span>{tab.label}</span>
            {tab.badge !== undefined && (
              <span className={`px-1.5 py-0.5 text-[10px] rounded-full font-mono ${isActive ? 'bg-emerald-500/20 text-emerald-300' : 'bg-slate-800 text-slate-400'}`}>
                {tab.badge}
              </span>
            )}
          </button>
        );
      })}
    </div>
  );
};
