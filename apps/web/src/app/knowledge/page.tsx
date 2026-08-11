'use client';

import React from 'react';
import { AppShell } from '@/components/shell/AppShell';
import { KnowledgeWorkspace } from '@/components/admin/KnowledgeWorkspace';

export default function EnterpriseKnowledgePage() {
  return (
    <AppShell>
      <KnowledgeWorkspace />
    </AppShell>
  );
}
