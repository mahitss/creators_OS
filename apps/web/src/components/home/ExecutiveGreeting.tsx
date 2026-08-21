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
    <div className="flex flex-col gap-4 pb-2 border-b border-[rgba(255,255,255,0.06)]">
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
        <div className="flex flex-col gap-1.5">
          <div className="flex items-center gap-2 text-[10px] font-mono text-[#62E6B2] tracking-widest uppercase">
            <span className="w-1.5 h-1.5 rounded-full bg-[#62E6B2]" />
            <span>INTELLIGENCE OPERATING LAYER // ACTIVE</span>
          </div>
          <h1 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold tracking-tight text-[#F5F5F5] uppercase font-sans">
            {greeting}
          </h1>
          <p className="text-sm text-[#A3A3A3] font-sans max-w-2xl">
            YOUR INTELLIGENCE ENVIRONMENT IS ONLINE. {summaryStatement}
          </p>
        </div>

        <div className="flex flex-col sm:items-end text-left sm:text-right gap-1 font-mono text-[11px] text-[#666666] shrink-0">
          <div className="text-[#A3A3A3]">{currentDate}</div>
          <div className="text-[#62E6B2] flex items-center sm:justify-end gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-[#62E6B2]" />
            <span>PROD-US-EAST-1</span>
          </div>
        </div>
      </div>

      {/* Metadata Telemetry Row */}
      <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-[11px] font-mono text-[#666666] pt-1">
        <span><span className="text-[#444444]">SYSTEM:</span> <span className="text-[#A3A3A3]">OPERATIONAL</span></span>
        <span className="text-[#2A2A2A]">•</span>
        <span><span className="text-[#444444]">MODEL ROUTER:</span> <span className="text-[#A3A3A3]">OPENROUTER/AUTO</span></span>
        <span className="text-[#2A2A2A]">•</span>
        <span><span className="text-[#444444]">EVENT MESH:</span> <span className="text-[#62E6B2]">CONNECTED</span></span>
        <span className="text-[#2A2A2A]">•</span>
        <span><span className="text-[#444444]">POLICY ENGINE:</span> <span className="text-[#A3A3A3]">ZERO-TRUST</span></span>
      </div>
    </div>
  );
};
