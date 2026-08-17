'use client';

import React from 'react';
import { Typography } from '@vapor/ui';

interface ExecutiveGreetingProps {
  greeting: string;
  summaryStatement: string;
}

export const ExecutiveGreeting: React.FC<ExecutiveGreetingProps> = ({
  greeting,
  summaryStatement,
}) => {
  const currentDate = new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });

  return (
    <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 pb-2">
      <div className="flex flex-col gap-1">
        <div className="flex items-center gap-2.5">
          <Typography variant="h1" className="text-xl sm:text-2xl lg:text-3xl font-extrabold tracking-tight text-white">
            {greeting}
          </Typography>
          <span className="px-2 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 font-mono text-[11px] font-semibold tracking-wide">
            LIVE BRIEF
          </span>
        </div>
        <Typography variant="caption" className="text-slate-400 text-xs sm:text-sm max-w-2xl leading-relaxed">
          {summaryStatement}
        </Typography>
      </div>

      <div className="flex items-center gap-3 shrink-0">
        <div className="flex flex-col items-end text-right">
          <span className="text-[11px] font-mono text-slate-400 font-medium">{currentDate}</span>
          <span className="text-[10px] font-mono text-emerald-400 flex items-center gap-1">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
            SYNCHRONIZED (PROD-US-EAST-1)
          </span>
        </div>
      </div>
    </div>
  );
};
