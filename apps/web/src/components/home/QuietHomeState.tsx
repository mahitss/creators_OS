'use client';

import React from 'react';
import Link from 'next/link';
import { Card, Typography, Button } from '@vapor/ui';

export const QuietHomeState: React.FC = () => {
  return (
    <Card
      variant="panel"
      className="flex flex-col p-6 sm:p-7 border-[rgba(255,255,255,0.10)] bg-[#0A0A0A] rounded-xl shadow-none relative overflow-hidden"
    >
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-5 border-b border-[rgba(255,255,255,0.08)]">
        <div className="flex items-center gap-3.5">
          <div className="w-9 h-9 rounded-lg bg-[#080808] border border-[rgba(255,255,255,0.12)] flex items-center justify-center text-[#62E6B2] shrink-0 font-bold">
            <span className="text-base">✓</span>
          </div>
          <div className="flex flex-col gap-0.5">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-[#62E6B2]" />
              <Typography variant="h2" className="text-base font-bold text-[#F5F5F5] tracking-tight">
                Workspace Quiet State
              </Typography>
            </div>
            <Typography variant="caption" className="text-xs text-[#A3A3A3] leading-relaxed">
              No active mission blocks or pending executions requiring immediate manual intervention.
            </Typography>
          </div>
        </div>

        <div className="flex items-center gap-2.5 shrink-0">
          <Link href="/missions">
            <Button variant="primary" size="sm">
              Launch Mission
            </Button>
          </Link>
          <Link href="/transformation-resilience-command-center">
            <Button variant="secondary" size="sm">
              Command Center
            </Button>
          </Link>
        </div>
      </div>

      {/* Active Operational Sentinel Status Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-5">
        <div className="p-3.5 rounded-lg bg-[#080808] border border-[rgba(255,255,255,0.08)] flex flex-col gap-1">
          <div className="flex items-center justify-between text-[11px] text-[#A3A3A3] font-mono">
            <span>POLICY ENGINE</span>
            <span className="text-[#62E6B2] font-semibold">ENFORCED</span>
          </div>
          <div className="text-sm font-bold text-[#F5F5F5]">Zero Trust Active</div>
          <div className="text-[11px] text-[#666666]">Continuous tenant & DLP scoping</div>
        </div>

        <div className="p-3.5 rounded-lg bg-[#080808] border border-[rgba(255,255,255,0.08)] flex flex-col gap-1">
          <div className="flex items-center justify-between text-[11px] text-[#A3A3A3] font-mono">
            <span>AI GATEWAY</span>
            <span className="text-[#62E6B2] font-semibold">ONLINE</span>
          </div>
          <div className="text-sm font-bold text-[#F5F5F5]">OpenRouter Active</div>
          <div className="text-[11px] text-[#666666]">OpenRouter gateway & model fallback active</div>
        </div>

        <div className="p-3.5 rounded-lg bg-[#080808] border border-[rgba(255,255,255,0.08)] flex flex-col gap-1">
          <div className="flex items-center justify-between text-[11px] text-[#A3A3A3] font-mono">
            <span>ASYNC BROKER</span>
            <span className="text-[#62E6B2] font-semibold">STANDBY</span>
          </div>
          <div className="text-sm font-bold text-[#F5F5F5]">Event Mesh Ready</div>
          <div className="text-[11px] text-[#666666]">Redis cache & event queue operational</div>
        </div>
      </div>
    </Card>
  );
};
