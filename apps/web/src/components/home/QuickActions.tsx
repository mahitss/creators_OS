'use client';

import React from 'react';
import Link from 'next/link';
import { Card, Typography } from '@vapor/ui';
import { QuickActionItem } from '../../lib/api/home';

interface QuickActionsProps {
  actions: QuickActionItem[];
}

export const QuickActions: React.FC<QuickActionsProps> = ({ actions }) => {
  if (actions.length === 0) return null;

  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-slate-400 text-sm">⚡</span>
          <Typography variant="h3" className="text-xs font-bold text-slate-300 uppercase tracking-wider">
            Fast Command Launchpad
          </Typography>
        </div>
        <span className="text-[10px] font-mono text-slate-500">HOTKEYS READY</span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
        {actions.map((act) => (
          <Link key={act.id} href={act.href} className="group">
            <Card
              variant="panel"
              className="flex items-center gap-3 p-3.5 border-[rgba(255,255,255,0.10)] bg-[#0B0B0B] hover:border-[rgba(255,255,255,0.18)] hover:bg-[#121212] transition-all rounded-lg cursor-pointer shadow-none"
            >
              <span className="text-lg p-2 rounded-md bg-[#080808] border border-[rgba(255,255,255,0.08)] group-hover:border-[rgba(98,230,178,0.30)] group-hover:bg-[rgba(98,230,178,0.06)] transition-all shrink-0">
                {act.icon}
              </span>
              <div className="flex flex-col min-w-0">
                <Typography variant="body" className="text-xs font-semibold text-[#F5F5F5] group-hover:text-[#62E6B2] transition-colors truncate">
                  {act.label}
                </Typography>
                <Typography variant="caption" className="text-[10px] font-mono text-[#666666] truncate">
                  {act.href}
                </Typography>
              </div>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
};
