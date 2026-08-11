'use client';

import React from 'react';
import { AppShell } from '@/components/shell/AppShell';
import { StrategicPlanningWorkspace } from '@/components/strategy/StrategicPlanningWorkspace';

export default function StrategyPage() {
  return (
    <AppShell>
      <StrategicPlanningWorkspace />
    </AppShell>
  );
}
