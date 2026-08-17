'use client';

import React from 'react';
import { Card, Typography, EmptyState } from '@vapor/ui';
import { ActivityItem } from '../../lib/api/home';

interface RecentActivityProps {
  activities: ActivityItem[];
}

export const RecentActivity: React.FC<RecentActivityProps> = ({ activities }) => {
  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-slate-400 text-sm">🤖</span>
          <Typography variant="h3" className="text-xs font-bold text-slate-300 uppercase tracking-wider">
            Live AI Agent Feed
          </Typography>
        </div>
        <span className="text-[10px] font-mono text-emerald-400 flex items-center gap-1">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
          STREAMING
        </span>
      </div>

      {activities.length === 0 ? (
        <Card variant="panel" className="p-5 border-slate-800/80 bg-[#121520] rounded-lg">
          <EmptyState
            title="No Recent Activity"
            description="Vapor hasn't executed any autonomous background tasks in the last 15 minutes. As agents trigger missions, telemetry will stream here in real time."
          />
        </Card>
      ) : (
        <div className="flex flex-col gap-2">
          {activities.map((act) => (
            <Card
              key={act.id}
              variant="panel"
              className="flex items-center justify-between p-3.5 border-slate-800/80 bg-[#121520] hover:border-slate-700/80 transition-all rounded-lg"
            >
              <div className="flex items-center gap-3 min-w-0">
                <span className="w-2 h-2 rounded-full bg-emerald-400 shrink-0" />
                <Typography variant="body" className="text-xs font-medium text-slate-200 truncate">
                  {act.title}
                </Typography>
              </div>
              <span className="text-[11px] font-mono text-slate-500 shrink-0 ml-3 bg-slate-900 px-2 py-0.5 rounded border border-slate-800">
                {act.timestamp}
              </span>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};
