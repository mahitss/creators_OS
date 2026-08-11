'use client';

import React from 'react';
import { AppShell } from '@/components/shell/AppShell';
import { IntegrationFabricWorkspace } from '@/components/admin/IntegrationFabricWorkspace';

export default function IntegrationsPage() {
  return (
    <AppShell>
      <IntegrationFabricWorkspace />
    </AppShell>
  );
}
