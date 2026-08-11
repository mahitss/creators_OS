'use client';

import React from 'react';
import { AppShell } from '@/components/shell/AppShell';
import { ExecutionGovernanceWorkspace } from '@/components/execution/ExecutionGovernanceWorkspace';

export default function ExecutionPage() {
  return (
    <AppShell>
      <ExecutionGovernanceWorkspace />
    </AppShell>
  );
}
