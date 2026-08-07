import React from 'react';
import { Card, Typography, TerminalIcon } from '@vapor/ui';

export default function Home() {
  return (
    <main className="flex-1 flex flex-col items-center justify-center p-6 bg-[#090A0F]">
      <Card variant="panel" className="max-w-md w-full flex flex-col items-center text-center gap-4 border border-slate-800/80">
        <div className="flex items-center gap-2 text-emerald-400">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          <Typography variant="code">VAPOR_OS // KERNEL_ACTIVE</Typography>
        </div>
        <div className="flex items-center gap-2 text-slate-400 mt-2">
          <TerminalIcon size={20} />
          <Typography variant="h2">Vapor OS Platform Foundation</Typography>
        </div>
        <Typography variant="caption" className="text-slate-400 max-w-sm">
          System kernel initialized. All shared packages, API routes, database models, and AI provider abstractions are active.
        </Typography>
      </Card>
    </main>
  );
}
