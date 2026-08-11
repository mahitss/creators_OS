'use client';

import React from 'react';
import { AppShell } from '@/components/shell/AppShell';
import { LearningFabricWorkspace } from '@/components/memory/LearningFabricWorkspace';

export default function MemoryExplorePage() {
  return (
    <AppShell>
      <LearningFabricWorkspace />
    </AppShell>
  );
}
