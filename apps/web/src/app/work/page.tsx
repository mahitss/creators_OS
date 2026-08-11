'use client';

import React from 'react';
import { AppShell } from '@/components/shell/AppShell';
import { WorkQueueWorkspace } from '@/components/collaboration/WorkQueueWorkspace';

export default function WorkPage() {
  return (
    <AppShell>
      <WorkQueueWorkspace />
    </AppShell>
  );
}
