import React from 'react';
import { Card, Typography } from '@vapor/ui';

interface ExecutiveSummaryCardProps {
  summaryStatement: string;
}

export const ExecutiveSummaryCard: React.FC<ExecutiveSummaryCardProps> = ({ summaryStatement }) => {
  return (
    <Card variant="panel" className="flex flex-col gap-3 p-5 border-slate-800/80 bg-[#12141C]">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          <Typography variant="h3" className="text-sm font-semibold text-slate-100">
            Executive Summary
          </Typography>
        </div>
        <Typography variant="caption" className="text-slate-500 font-mono text-[11px]">
          REALTIME_BRIEF
        </Typography>
      </div>
      <Typography variant="body" className="text-slate-300 text-sm leading-relaxed">
        {summaryStatement}
      </Typography>
    </Card>
  );
};
