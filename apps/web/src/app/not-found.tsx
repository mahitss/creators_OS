import React from 'react';
import Link from 'next/link';
import { Card, Button, Typography } from '@vapor/ui';

export default function NotFound() {
  return (
    <main className="flex-1 flex items-center justify-center p-6 bg-[#090A0F]">
      <Card variant="panel" className="max-w-md w-full flex flex-col items-center text-center gap-4">
        <Typography variant="h1" className="text-4xl font-mono text-emerald-400">
          404
        </Typography>
        <Typography variant="h2">Resource Not Found</Typography>
        <Typography variant="body" className="text-slate-400 text-xs">
          The requested workspace route or component resource does not exist.
        </Typography>
        <Link href="/">
          <Button variant="secondary" className="mt-2">
            Return to Kernel Shell
          </Button>
        </Link>
      </Card>
    </main>
  );
}
