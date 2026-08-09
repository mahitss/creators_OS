'use client';

import React from 'react';
import { AgentControlCenter } from '@/components/admin/AgentControlCenter';

export default function AdminAgentsPage() {
  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100">
      <AgentControlCenter />
    </div>
  );
}
