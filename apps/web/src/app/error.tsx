'use client';

import React, { useEffect } from 'react';
import { Card, Button, Typography, AlertIcon } from '@vapor/ui';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error('[Vapor Error Boundary Caught]:', error);
  }, [error]);

  return (
    <main className="flex-1 flex items-center justify-center p-6 bg-[#090A0F]">
      <Card variant="panel" className="max-w-md w-full flex flex-col items-center text-center gap-4 border border-rose-500/30">
        <div className="flex items-center justify-center p-3 rounded-full bg-rose-500/10 text-rose-400">
          <AlertIcon size={24} />
        </div>
        <Typography variant="h2" className="text-slate-100">
          Application Error Detected
        </Typography>
        <Typography variant="body" className="text-slate-400 text-xs max-w-xs">
          {error.message || 'An unexpected rendering error occurred in the Vapor application shell.'}
        </Typography>
        <Button variant="secondary" onClick={() => reset()} className="mt-2">
          Try Again
        </Button>
      </Card>
    </main>
  );
}
