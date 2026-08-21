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
      className="flex flex-col gap-4 p-5 sm:p-6 border-[rgba(255,255,255,0.10)] bg-[#080808] rounded-xl shadow-none relative overflow-hidden"
    >
      <div className="flex items-center justify-between border-b border-[rgba(255,255,255,0.08)] pb-3">
        <div className="flex items-center gap-2.5">
          <div className="w-2 h-2 rounded-full bg-[#62E6B2] shadow-none" />
          <Typography variant="h3" className="text-sm font-bold text-[#F5F5F5] uppercase tracking-wider">
            Executive Summary
          </Typography>
        </div>
        <div className="flex items-center gap-2 text-[11px] font-mono text-[#A3A3A3]">
          <span className="px-2 py-0.5 rounded-full bg-[rgba(98,230,178,0.06)] border border-[rgba(98,230,178,0.22)] text-[#62E6B2] font-semibold uppercase">
            LIVE BRIEF
          </span>
          <span className="text-[#404040] hidden sm:inline">•</span>
          <span className="text-[#A3A3A3] hidden sm:inline">OpenRouter Gateway</span>
        </div>
      </div>

      <Typography variant="body" className="text-[#F5F5F5] text-sm sm:text-base leading-relaxed font-sans">
        {summaryStatement}
      </Typography>

      <div className="flex items-center justify-between pt-2 text-[11px] font-mono text-[#666666] border-t border-[rgba(255,255,255,0.06)]">
        <span>AI Gateway: OpenRouter (openrouter/auto)</span>
        <span>Storage: Neon PostgreSQL • Redis Connected</span>
      </div>
    </Card>
  );
};
