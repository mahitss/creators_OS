import React from 'react';
import { Spinner, Typography } from '@vapor/ui';

export default function Loading() {
  return (
    <div className="flex-1 flex flex-col items-center justify-center p-6 bg-[#090A0F] gap-3">
      <Spinner size="lg" />
      <Typography variant="caption" className="text-slate-500 font-mono">
        Initializing Vapor OS Shell...
      </Typography>
    </div>
  );
}
