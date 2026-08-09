'use client';

import React from 'react';
import { MemoryWorkspace } from '@/components/memory/MemoryWorkspace';

export default function MemoryPage() {
  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100">
      <MemoryWorkspace />
    </div>
  );
}
