'use client';

import React from 'react';
import { AppShell } from '@/components/shell/AppShell';
import { PortfolioIntelligenceWorkspace } from '@/components/portfolio/PortfolioIntelligenceWorkspace';

export default function PortfolioPage() {
  return (
    <AppShell>
      <PortfolioIntelligenceWorkspace />
    </AppShell>
  );
}
