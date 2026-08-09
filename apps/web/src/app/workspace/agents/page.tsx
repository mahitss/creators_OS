'use client';

import React from 'react';
import { AgentLibrary } from '@/components/agents/AgentLibrary';

export default function WorkspaceAgentsPage() {
  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100">
      <AgentLibrary />
    </div>
  );
}
