'use client';

import React from 'react';
import { AppShell } from '@/components/shell/AppShell';
import { GovernanceWorkspace } from '@/components/admin/GovernanceWorkspace';

export default function EnterpriseGovernancePage() {
  return (
    <AppShell>
      <GovernanceWorkspace />
    </AppShell>
  );
}
