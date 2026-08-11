'use client';

import React from 'react';
import { AppShell } from '@/components/shell/AppShell';
import { AgentMeshWorkspace } from '@/components/admin/AgentMeshWorkspace';

export default function AgentMeshPage() {
  return (
    <AppShell>
      <AgentMeshWorkspace />
    </AppShell>
  );
}
