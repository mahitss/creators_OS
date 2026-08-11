'use client';

import React from 'react';
import { AppShell } from '@/components/shell/AppShell';
import { PolicyIntelligenceWorkspace } from '@/components/admin/PolicyIntelligenceWorkspace';

export default function EnterpriseGovernancePage() {
  return (
    <AppShell>
      <div className="max-w-6xl mx-auto w-full py-4">
        <PolicyIntelligenceWorkspace />
      </div>
    </AppShell>
  );
}
