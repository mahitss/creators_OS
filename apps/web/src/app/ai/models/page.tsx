'use client';

import React from 'react';
import { AppShell } from '@/components/shell/AppShell';
import { ModelGatewayWorkspace } from '@/components/models/ModelGatewayWorkspace';

export default function AIModelsPage() {
  return (
    <AppShell>
      <ModelGatewayWorkspace />
    </AppShell>
  );
}
