'use client';

import React from 'react';

interface ExecutiveSummaryCardProps {
  summaryStatement: string;
}

export const ExecutiveSummaryCard: React.FC<ExecutiveSummaryCardProps> = ({ summaryStatement }) => {
  return (
    <div className="flex flex-col gap-3 py-4">
      <div className="flex items-center justify-between border-b border-[rgba(255,255,255,0.06)] pb-2">
        <div className="flex items-center gap-2">
          <span className="w-1.5 h-1.5 rounded-full bg-[#62E6B2]" />
          <span className="text-xs font-bold text-[#F5F5F5] uppercase tracking-widest font-mono">
            EXECUTIVE SUMMARY BRIEF
          </span>
        </div>
        <div className="flex items-center gap-2 text-[10px] font-mono text-[#666666]">
          <span className="text-[#62E6B2]">LIVE STREAM</span>
          <span>•</span>
          <span>OBSERVING</span>
        </div>
      </div>

      <div className="text-base sm:text-lg text-[#F5F5F5] font-sans leading-relaxed font-normal">
        {summaryStatement}
      </div>

      {/* Editorial Infrastructure Breakdown */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-3 mt-1 border-t border-[rgba(255,255,255,0.06)] text-[11px] font-mono">
        <div>
          <div className="text-[#555555]">AI GATEWAY</div>
          <div className="text-[#F5F5F5] font-medium mt-0.5">OpenRouter / auto</div>
        </div>
        <div>
          <div className="text-[#555555]">STORAGE</div>
          <div className="text-[#F5F5F5] font-medium mt-0.5">Neon PostgreSQL</div>
        </div>
        <div>
          <div className="text-[#555555]">CACHE & EVENT</div>
          <div className="text-[#F5F5F5] font-medium mt-0.5">Redis Pub/Sub</div>
        </div>
        <div>
          <div className="text-[#555555]">POLICY</div>
          <div className="text-[#62E6B2] font-medium mt-0.5">Zero Trust Enforced</div>
        </div>
      </div>
    </div>
  );
};

