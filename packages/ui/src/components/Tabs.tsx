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
    <div className={`flex items-center gap-1 border-b border-[rgba(255,255,255,0.08)] ${className}`} role="tablist">
      {tabs.map((tab) => {
        const isActive = tab.id === activeTabId;
        return (
          <button
            key={tab.id}
            role="tab"
            aria-selected={isActive}
            disabled={tab.disabled}
            onClick={() => !tab.disabled && onChange(tab.id)}
            className={`flex items-center gap-2 px-3 py-2 text-xs font-semibold border-b-2 transition-all focus-visible:outline-none ${
              isActive
                ? 'border-[#62E6B2] text-[#F5F5F5]'
                : 'border-transparent text-[#666666] hover:text-[#A3A3A3] hover:border-[rgba(255,255,255,0.12)]'
            } ${tab.disabled ? 'opacity-40 cursor-not-allowed' : ''}`}
          >
            <span>{tab.label}</span>
            {tab.badge !== undefined && (
              <span className={`px-1.5 py-0.5 text-[10px] rounded-full font-mono ${isActive ? 'bg-[rgba(98,230,178,0.12)] text-[#62E6B2]' : 'bg-[#151515] text-[#666666]'}`}>
                {tab.badge}
              </span>
            )}
          </button>
        );
      })}
    </div>
  );
};
