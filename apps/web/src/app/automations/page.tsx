'use client';

import React from 'react';
import { AppShell } from '@/components/shell/AppShell';
import { AutomationsWorkspace } from '@/components/automations/AutomationsWorkspace';

export default function AutomationsPage() {
  return (
    <AppShell>
      <AutomationsWorkspace />
    </AppShell>
  );
}
