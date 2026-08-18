'use client';

import React from 'react';
import Link from 'next/link';
import { Card, Typography, Button } from '@vapor/ui';

export const QuietHomeState: React.FC = () => {
  return (
    <Card
      variant="panel"
      className="flex flex-col p-6 sm:p-7 border-slate-800/90 bg-gradient-to-b from-[#121520] to-[#0D0F17] rounded-xl shadow-lg relative overflow-hidden"
    >
      {/* Background Accent Glow */}
      <div className="absolute top-0 right-0 w-64 h-64 bg-emerald-500/5 rounded-full blur-3xl pointer-events-none" />

      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-5 border-b border-slate-800/80">
        <div className="flex items-center gap-3.5">
          <div className="w-10 h-10 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 shrink-0 shadow-inner">
            <span className="text-lg">✓</span>
          </div>
          <div className="flex flex-col gap-0.5">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400" />
              <Typography variant="h2" className="text-base font-bold text-slate-100 tracking-tight">
                Workspace Quiet State
              </Typography>
            </div>
            <Typography variant="caption" className="text-xs text-slate-400 leading-relaxed">
              No active mission blocks or pending executions requiring immediate manual intervention.
            </Typography>
          </div>
        </div>

        <div className="flex items-center gap-2 shrink-0">
          <Link href="/missions">
            <Button variant="primary" size="sm" className="shadow-sm">
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
        <div className="p-3.5 rounded-lg bg-slate-900/60 border border-slate-800/80 flex flex-col gap-1">
          <div className="flex items-center justify-between text-[11px] text-slate-400 font-mono">
            <span>POLICY ENGINE</span>
            <span className="text-emerald-400 font-semibold">ENFORCED</span>
          </div>
          <div className="text-sm font-bold text-slate-200">Zero Trust Active</div>
          <div className="text-[11px] text-slate-500">Continuous tenant & DLP scoping</div>
        </div>

        <div className="p-3.5 rounded-lg bg-slate-900/60 border border-slate-800/80 flex flex-col gap-1">
          <div className="flex items-center justify-between text-[11px] text-slate-400 font-mono">
            <span>AI GATEWAY</span>
            <span className="text-emerald-400 font-semibold">ONLINE</span>
          </div>
          <div className="text-sm font-bold text-slate-200">OpenRouter Active</div>
          <div className="text-[11px] text-slate-500">OpenRouter gateway & model fallback active</div>
        </div>

        <div className="p-3.5 rounded-lg bg-slate-900/60 border border-slate-800/80 flex flex-col gap-1">
          <div className="flex items-center justify-between text-[11px] text-slate-400 font-mono">
            <span>ASYNC BROKER</span>
            <span className="text-emerald-400 font-semibold">STANDBY</span>
          </div>
          <div className="text-sm font-bold text-slate-200">Event Mesh Ready</div>
          <div className="text-[11px] text-slate-500">Redis cache & event queue operational</div>
        </div>
      </div>
    </Card>
  );
};
