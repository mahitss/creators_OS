'use client';

import React from 'react';
import { AppShell } from '@/components/shell/AppShell';
import { IdentityWorkspace } from '@/components/admin/IdentityWorkspace';

export default function EnterpriseIdentityPage() {
  return (
    <AppShell>
      <IdentityWorkspace />
    </AppShell>
  );
}
