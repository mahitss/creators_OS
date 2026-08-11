'use client';

import React from 'react';
import { AppShell } from '@/components/shell/AppShell';
import { CollaborationCenterWorkspace } from '@/components/collaboration/CollaborationCenterWorkspace';

export default function CollaborationPage() {
  return (
    <AppShell>
      <CollaborationCenterWorkspace />
    </AppShell>
  );
}
