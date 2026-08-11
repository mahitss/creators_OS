'use client';

import React from 'react';
import { useParams } from 'next/navigation';
import { AppShell } from '@/components/shell/AppShell';
import { ExecutionTraceWorkspace } from '@/components/agents/ExecutionTraceWorkspace';

export default function AgentExecutionTracePage() {
  const params = useParams();
  const id = typeof params?.id === 'string' ? params.id : 'exec_demo_01';

  return (
    <AppShell>
      <ExecutionTraceWorkspace executionId={id} />
    </AppShell>
  );
}
