'use client';

import React from 'react';
import { AppShell } from '@/components/shell/AppShell';
import { CapabilityRegistryWorkspace } from '@/components/capabilities/CapabilityRegistryWorkspace';

export default function CapabilitiesPage() {
  return (
    <AppShell>
      <CapabilityRegistryWorkspace />
    </AppShell>
  );
}
