'use client';

import React from 'react';
import Link from 'next/link';
import { Terminal, ArrowRight } from 'lucide-react';
import { QuickActionItem } from '../../lib/api/home';

interface QuickActionsProps {
  actions: QuickActionItem[];
}

export const QuickActions: React.FC<QuickActionsProps> = ({ actions }) => {
  if (actions.length === 0) return null;

  return (
    <div className="flex flex-col gap-2.5">
      <div className="flex items-center justify-between pb-1">
        <div className="flex items-center gap-2">
          <Terminal className="w-3.5 h-3.5 text-[#858585]" />
          <span className="text-xs font-bold text-[#F5F5F5] uppercase tracking-widest font-mono">
            COMMAND LAUNCHPAD
          </span>
        </div>
        <span className="text-[10px] font-mono text-[#666666]">CLI READY</span>
      </div>

      <div className="flex flex-col divide-y divide-[rgba(255,255,255,0.04)] bg-[#080808] rounded-lg overflow-hidden border border-[rgba(255,255,255,0.06)]">
        {actions.map((act) => {
          const commandAlias = act.href.startsWith('/') ? act.href : `/${act.href}`;
          return (
            <Link
              key={act.id}
              href={act.href}
              className="flex items-center justify-between px-3 py-2.5 text-xs hover:bg-[#0D0D0D] transition-colors group"
            >
              <div className="flex items-center gap-3">
                <span className="font-mono text-[#62E6B2] text-xs font-semibold group-hover:underline">
                  {commandAlias}
                </span>
                <span className="text-[#858585] text-xs font-sans group-hover:text-[#F5F5F5] transition-colors">
                  {act.label}
                </span>
              </div>
              <ArrowRight className="w-3 h-3 text-[#444444] group-hover:text-[#62E6B2] transition-colors" />
            </Link>
          );
        })}
      </div>
    </div>
  );
};

