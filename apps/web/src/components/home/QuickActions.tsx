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
      <Typography variant="h3" className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
        Available Quick Actions
      </Typography>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {actions.map((act) => (
          <Link key={act.id} href={act.href}>
            <Card
              variant="panel"
              className="flex items-center gap-3 p-3.5 border-slate-800/80 hover:border-emerald-500/50 hover:bg-slate-800/40 transition-all cursor-pointer group"
            >
              <span className="text-lg p-2 rounded bg-slate-800/80 group-hover:bg-emerald-500/10 transition-colors">
                {act.icon}
              </span>
              <div className="flex flex-col">
                <Typography variant="body" className="text-xs font-semibold text-slate-200 group-hover:text-emerald-400 transition-colors">
                  {act.label}
                </Typography>
                <Typography variant="caption" className="text-[11px] text-slate-500">
                  Open workspace view
                </Typography>
              </div>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
};
