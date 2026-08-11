'use client';

import React from 'react';
import { AppShell } from '@/components/shell/AppShell';
import { PerformanceIntelligenceWorkspace } from '@/components/performance/PerformanceIntelligenceWorkspace';

export default function PerformancePage() {
  return (
    <AppShell>
      <PerformanceIntelligenceWorkspace />
    </AppShell>
  );
}
