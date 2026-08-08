import React from 'react';
import { Card, Typography, EmptyState } from '@vapor/ui';
import { ActivityItem } from '../../lib/api/home';

interface RecentActivityProps {
  activities: ActivityItem[];
}

export const RecentActivity: React.FC<RecentActivityProps> = ({ activities }) => {
  return (
    <div className="flex flex-col gap-3">
      <Typography variant="h3" className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
        Recent AI Activity
      </Typography>

      {activities.length === 0 ? (
        <Card variant="panel" className="p-4 border-slate-800/80">
          <EmptyState
            title="No Recent Activity"
            description="Vapor hasn't completed any background work yet. Your activity will appear here as missions execute."
          />
        </Card>
      ) : (
        <div className="flex flex-col gap-2">
          {activities.map((act) => (
            <Card key={act.id} variant="panel" className="flex items-center justify-between p-3 border-slate-800/80">
              <div className="flex items-center gap-3">
                <span className="w-2 h-2 rounded-full bg-emerald-500" />
                <Typography variant="body" className="text-xs font-medium text-slate-200">
                  {act.title}
                </Typography>
              </div>
              <Typography variant="caption" className="text-[11px] font-mono text-slate-500">
                {act.timestamp}
              </Typography>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};
