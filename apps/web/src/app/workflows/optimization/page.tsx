'use client';

import React from 'react';
import { AppShell } from '@/components/shell/AppShell';
import { WorkflowOptimizationWorkspace } from '@/components/workflows/WorkflowOptimizationWorkspace';

export default function WorkflowOptimizationPage() {
  return (
    <AppShell>
      <WorkflowOptimizationWorkspace />
    </AppShell>
  );
}
