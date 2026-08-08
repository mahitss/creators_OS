import React from 'react';
import { Typography, Card } from '@vapor/ui';
import { MissionActivity } from '../../lib/api/missions';
import { formatDate } from '@vapor/utils';

export interface ActivityTimelineProps {
  activities: MissionActivity[];
}

export const ActivityTimeline: React.FC<ActivityTimelineProps> = ({ activities }) => {
  if (!activities || activities.length === 0) {
    return (
      <Typography variant="caption" className="text-slate-500 italic">
        No recorded activity events for this mission yet.
      </Typography>
    );
  }

  const getActionBadgeClass = (action: string) => {
    switch (action) {
      case 'CREATED': return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20';
      case 'UPDATED': return 'text-cyan-400 bg-cyan-500/10 border-cyan-500/20';
      case 'COMPLETED': return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20';
      case 'ARCHIVED': return 'text-amber-400 bg-amber-500/10 border-amber-500/20';
      default: return 'text-slate-400 bg-slate-800 border-slate-700';
    }
  };

  return (
    <div className="flex flex-col gap-3">
      <Typography variant="h3" className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
        Activity & Event Timeline
      </Typography>

      <div className="relative pl-4 border-l border-slate-800 flex flex-col gap-4">
        {activities.map((act) => (
          <div key={act.id} className="relative flex flex-col gap-1">
            <span className="absolute -left-[21px] top-1 w-2.5 h-2.5 rounded-full bg-slate-700 border-2 border-slate-900" />
            <div className="flex items-center gap-2">
              <span className={`px-1.5 py-0.5 text-[10px] font-mono font-semibold rounded border ${getActionBadgeClass(act.action)}`}>
                {act.action}
              </span>
              <span className="text-[11px] font-mono text-slate-500">
                {formatDate(act.created_at)}
              </span>
            </div>
            {act.details && Object.keys(act.details).length > 0 && (
              <Card variant="panel" className="p-2 mt-1 bg-slate-950/60 text-xs font-mono text-slate-400 border-slate-800/60">
                {JSON.stringify(act.details, null, 2)}
              </Card>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
