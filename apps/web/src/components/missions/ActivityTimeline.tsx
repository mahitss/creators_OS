import React from 'react';
import { Typography, Card } from '@vapor/ui';
import { MissionActivity, MissionEvent } from '../../lib/api/missions';
import { formatDate } from '@vapor/utils';

export interface ActivityTimelineProps {
  activities?: MissionActivity[];
  events?: MissionEvent[];
}

export const ActivityTimeline: React.FC<ActivityTimelineProps> = ({ activities = [], events = [] }) => {
  // Combine activities and events into a unified chronological stream
  const unifiedItems = [
    ...activities.map((a) => ({
      id: a.id,
      type: a.action,
      timestamp: a.created_at,
      payload: a.details,
      isEvent: false,
    })),
    ...events.map((e) => ({
      id: e.id,
      type: e.event_type,
      timestamp: e.timestamp,
      payload: e.payload,
      isEvent: true,
    })),
  ].sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());

  if (unifiedItems.length === 0) {
    return (
      <Typography variant="caption" className="text-neutral-500 italic font-mono text-xs">
        No recorded execution events or activity for this mission yet.
      </Typography>
    );
  }

  const getActionBadgeClass = (action: string) => {
    switch (action.toUpperCase()) {
      case 'MISSION_CREATED':
      case 'CREATED':
        return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30';
      case 'MISSION_QUEUED':
        return 'text-amber-400 bg-amber-500/10 border-amber-500/30';
      case 'MISSION_PLANNING':
      case 'PLAN_CREATED':
        return 'text-sky-400 bg-sky-500/10 border-sky-500/30';
      case 'STEP_STARTED':
      case 'MODEL_REQUEST':
        return 'text-cyan-400 bg-cyan-500/10 border-cyan-500/30';
      case 'STEP_COMPLETED':
      case 'MODEL_RESPONSE':
      case 'COMPLETED':
      case 'MISSION_COMPLETED':
        return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30';
      case 'MISSION_PAUSED':
        return 'text-amber-400 bg-amber-500/10 border-amber-500/30';
      case 'MISSION_RESUMED':
        return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30';
      case 'MISSION_CANCELLED':
        return 'text-neutral-400 bg-neutral-800 border-neutral-700';
      case 'STEP_FAILED':
      case 'MISSION_FAILED':
        return 'text-rose-400 bg-rose-500/10 border-rose-500/30';
      default:
        return 'text-neutral-400 bg-neutral-900 border-neutral-800';
    }
  };

  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <Typography variant="h3" className="text-xs font-semibold text-neutral-300 uppercase tracking-wider font-mono">
          Append-Only Event Ledger ({unifiedItems.length})
        </Typography>
        <span className="text-[10px] font-mono text-neutral-500">Live SSE Stream</span>
      </div>

      <div className="relative pl-4 border-l border-neutral-800 flex flex-col gap-3 max-h-[500px] overflow-y-auto pr-2">
        {unifiedItems.map((item) => (
          <div key={item.id} className="relative flex flex-col gap-1">
            <span className="absolute -left-[21px] top-1 w-2.5 h-2.5 rounded-full bg-neutral-800 border-2 border-neutral-950" />
            <div className="flex items-center gap-2">
              <span className={`px-1.5 py-0.5 text-[10px] font-mono font-semibold rounded border ${getActionBadgeClass(item.type)}`}>
                {item.type}
              </span>
              <span className="text-[11px] font-mono text-neutral-500">
                {formatDate(item.timestamp)}
              </span>
            </div>
            {item.payload && Object.keys(item.payload).length > 0 && (
              <Card variant="panel" className="p-2 mt-0.5 bg-neutral-950 text-xs font-mono text-neutral-400 border-neutral-900 overflow-x-auto">
                <pre className="text-[11px] leading-relaxed whitespace-pre-wrap">{JSON.stringify(item.payload, null, 2)}</pre>
              </Card>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
