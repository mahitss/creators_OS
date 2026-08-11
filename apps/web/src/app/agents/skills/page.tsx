'use client';

import React from 'react';
import { AppShell } from '@/components/shell/AppShell';
import { SkillFabricWorkspace } from '@/components/skills/SkillFabricWorkspace';

export default function AgentSkillsPage() {
  return (
    <AppShell>
      <SkillFabricWorkspace />
    </AppShell>
  );
}
