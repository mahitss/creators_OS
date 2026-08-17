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
              className="flex items-center gap-3 p-3.5 border-slate-800/80 bg-[#121520] hover:border-emerald-500/60 hover:bg-[#161B28] transition-all rounded-lg cursor-pointer shadow-sm"
            >
              <span className="text-lg p-2 rounded-md bg-slate-900 border border-slate-800 group-hover:border-emerald-500/40 group-hover:bg-emerald-500/10 group-hover:scale-105 transition-all shrink-0">
                {act.icon}
              </span>
              <div className="flex flex-col min-w-0">
                <Typography variant="body" className="text-xs font-semibold text-slate-200 group-hover:text-emerald-400 transition-colors truncate">
                  {act.label}
                </Typography>
                <Typography variant="caption" className="text-[10px] font-mono text-slate-500 truncate">
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
