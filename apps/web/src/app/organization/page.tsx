'use client';

import React from 'react';
import { AppShell } from '@/components/shell/AppShell';
import { OrganizationOperatingWorkspace } from '@/components/organization/OrganizationOperatingWorkspace';

export default function OrganizationPage() {
  return (
    <AppShell>
      <OrganizationOperatingWorkspace />
    </AppShell>
  );
}
