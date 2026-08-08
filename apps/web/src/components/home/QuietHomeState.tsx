import React from 'react';
import Link from 'next/link';
import { Card, Typography, Button } from '@vapor/ui';

export const QuietHomeState: React.FC = () => {
  return (
    <Card variant="panel" className="flex flex-col items-center justify-center p-8 text-center gap-4 border-slate-800/80 my-4">
      <div className="p-3 rounded-full bg-emerald-500/10 text-emerald-400">
        <span className="text-xl">✓</span>
      </div>
      <div className="flex flex-col gap-1">
        <Typography variant="h2" className="text-base font-semibold text-slate-100">
          You're all caught up.
        </Typography>
        <Typography variant="caption" className="text-xs text-slate-400 max-w-sm leading-relaxed">
          No urgent attention items or pending executions. Vapor is observing your workspace.
        </Typography>
      </div>
      <Link href="/missions">
        <Button variant="primary" size="sm">
          Open Missions Orchestrator
        </Button>
      </Link>
    </Card>
  );
};
