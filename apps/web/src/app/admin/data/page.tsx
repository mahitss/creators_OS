'use client';

import React from 'react';
import { AppShell } from '@/components/shell/AppShell';
import { DataSecurityWorkspace } from '@/components/admin/DataSecurityWorkspace';

export default function EnterpriseDataSecurityPage() {
  return (
    <AppShell>
      <DataSecurityWorkspace />
    </AppShell>
  );
}
