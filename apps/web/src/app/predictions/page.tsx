'use client';

import React from 'react';
import { AppShell } from '@/components/shell/AppShell';
import { PredictiveOperationsWorkspace } from '@/components/predictions/PredictiveOperationsWorkspace';

export default function PredictionsPage() {
  return (
    <AppShell>
      <PredictiveOperationsWorkspace />
    </AppShell>
  );
}
