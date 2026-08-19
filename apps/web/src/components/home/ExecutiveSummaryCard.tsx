'use client';

import React from 'react';
import { Card, Typography } from '@vapor/ui';

interface ExecutiveSummaryCardProps {
  summaryStatement: string;
}

export const ExecutiveSummaryCard: React.FC<ExecutiveSummaryCardProps> = ({ summaryStatement }) => {
  return (
    <Card
      variant="panel"
      className="flex flex-col gap-4 p-5 sm:p-6 border-slate-800/90 bg-[#121520] rounded-xl shadow-md relative overflow-hidden"
    >
      <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
        <div className="flex items-center gap-2.5">
          <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.8)]" />
          <Typography variant="h3" className="text-sm font-bold text-slate-100 uppercase tracking-wider">
            Executive Summary
          </Typography>
        </div>
        <div className="flex items-center gap-2 text-[11px] font-mono text-slate-400">
          <span className="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-emerald-400 font-semibold">
            LIVE BRIEF
          </span>
          <span className="text-slate-600 hidden sm:inline">•</span>
          <span className="text-slate-400 hidden sm:inline">OpenRouter Gateway</span>
        </div>
      </div>

      <Typography variant="body" className="text-slate-200 text-sm sm:text-base leading-relaxed font-sans">
        {summaryStatement}
      </Typography>

      <div className="flex items-center justify-between pt-2 text-[11px] font-mono text-slate-500 border-t border-slate-800/40">
        <span>AI Gateway: OpenRouter (openrouter/auto)</span>
        <span>Storage: Neon PostgreSQL • Redis Connected</span>
      </div>
    </Card>
  );
};
