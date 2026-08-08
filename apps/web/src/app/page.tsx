import React from 'react';
import { AppShell } from '../components/shell/AppShell';
import { Card, Typography, TerminalIcon } from '@vapor/ui';

export default function Home() {
  return (
    <AppShell>
      <div className="flex-1 flex flex-col items-center justify-center">
        <Card variant="panel" className="max-w-md w-full flex flex-col items-center text-center gap-4 border border-slate-800/80">
          <div className="flex items-center gap-2 text-emerald-400">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            <Typography variant="code">VAPOR_OS // SHELL_READY</Typography>
          </div>
          <div className="flex items-center gap-2 text-slate-300">
            <TerminalIcon size={20} />
            <Typography variant="h2">Authenticated Application Shell</Typography>
          </div>
          <Typography variant="caption" className="text-slate-400 max-w-sm leading-relaxed">
            The visual design tokens, atomic UI primitives, responsive sidebar, top bar, user menu, theme switcher, and command palette (<kbd className="font-mono bg-slate-950 px-1 rounded border border-slate-800">⌘K</kbd>) are active.
          </Typography>
        </Card>
      </div>
    </AppShell>
  );
}
