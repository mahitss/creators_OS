'use client';

import React from 'react';
import { AppShell } from '@/components/shell/AppShell';
import { DecisionIntelligenceWorkspace } from '@/components/admin/DecisionIntelligenceWorkspace';

export default function IntelligencePage() {
  return (
    <AppShell>
      <DecisionIntelligenceWorkspace />
    </AppShell>
  );
}
