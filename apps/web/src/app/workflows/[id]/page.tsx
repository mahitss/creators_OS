'use client';

import React from 'react';
import { useParams } from 'next/navigation';
import { AppShell } from '@/components/shell/AppShell';
import { WorkflowCanvas } from '@/components/workflows/WorkflowCanvas';

export default function WorkflowDetailPage() {
  const params = useParams();
  const workflowId = (params?.id as string) || 'wf_default';

  return (
    <AppShell>
      <WorkflowCanvas workflowId={workflowId} />
    </AppShell>
  );
}
