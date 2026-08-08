import React from 'react';
import Link from 'next/link';
import { Card, Typography, Button } from '@vapor/ui';

interface TodaysBriefProps {
  isEmptyState: boolean;
}

export const TodaysBrief: React.FC<TodaysBriefProps> = ({ isEmptyState }) => {
  return (
    <Card variant="panel" className="flex flex-col gap-4 p-6 border-slate-800/80 bg-[#12141C]">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          <Typography variant="h3" className="text-sm font-semibold text-slate-200">
            Today's Brief
          </Typography>
        </div>
        <Typography variant="caption" className="text-slate-500 font-mono text-[11px]">
          REALTIME_CONTEXT
        </Typography>
      </div>

      {isEmptyState ? (
        <div className="flex flex-col gap-3 py-2">
          <Typography variant="body" className="text-slate-300">
            Your workspace is initialized and ready. Vapor hasn't completed any background missions yet.
          </Typography>
          <div className="pt-2">
            <Link href="/missions">
              <Button variant="primary" size="sm">
                Open Missions Orchestrator
              </Button>
            </Link>
          </div>
        </div>
      ) : (
        <div className="flex flex-col gap-2">
          <Typography variant="body" className="text-slate-300">
            Executive background daemons are actively observing system events.
          </Typography>
        </div>
      )}
    </Card>
  );
};
