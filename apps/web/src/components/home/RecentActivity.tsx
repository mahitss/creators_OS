'use client';

import React from 'react';
import { Activity } from 'lucide-react';
import { ActivityItem } from '../../lib/api/home';

interface RecentActivityProps {
  activities: ActivityItem[];
}

export const RecentActivity: React.FC<RecentActivityProps> = ({ activities }) => {
  return (
    <div className="flex flex-col gap-2.5">
      <div className="flex items-center justify-between pb-1">
        <div className="flex items-center gap-2">
          <Activity className="w-3.5 h-3.5 text-[#858585]" />
          <span className="text-xs font-bold text-[#F5F5F5] uppercase tracking-widest font-mono">
            AGENT EXECUTION FEED
          </span>
        </div>
        <span className="text-[10px] font-mono text-[#62E6B2] flex items-center gap-1">
          <span className="w-1.5 h-1.5 rounded-full bg-[#62E6B2]" />
          STREAMING
        </span>
      </div>

      {activities.length === 0 ? (
        <div className="p-4 rounded-lg bg-[#080808] border border-[rgba(255,255,255,0.06)] text-xs text-[#666666] font-mono">
          No active agent task events in buffer.
        </div>
      ) : (
        <div className="flex flex-col divide-y divide-[rgba(255,255,255,0.04)] bg-[#080808] rounded-lg border border-[rgba(255,255,255,0.06)] overflow-hidden">
          {activities.map((act) => (
            <div
              key={act.id}
              className="flex items-center justify-between p-3 text-xs hover:bg-[#0D0D0D] transition-colors"
            >
              <div className="flex items-center gap-2.5 min-w-0">
                <span className="w-1.5 h-1.5 rounded-full bg-[#62E6B2] shrink-0" />
                <span className="font-medium text-[#F5F5F5] truncate font-sans">
                  {act.title}
                </span>
              </div>
              <span className="text-[10px] font-mono text-[#666666] shrink-0 ml-3">
                {act.timestamp}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

