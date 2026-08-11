'use client';

import React from 'react';
import { AppShell } from '@/components/shell/AppShell';
import { FinOpsWorkspace } from '@/components/finops/FinOpsWorkspace';

export default function FinOpsPage() {
  return (
    <AppShell>
      <FinOpsWorkspace />
    </AppShell>
  );
}
