import React from 'react';
import { AppShell } from '../../components/shell/AppShell';
import { EmptyState } from '@vapor/ui';

export default function MissionsPage() {
  return (
    <AppShell>
      <div className="flex-1 flex items-center justify-center">
        <EmptyState
          title="Missions Orchestrator"
          description="Autonomous agent mission pipelines will be configured in Sprint 4."
          icon={<span className="text-xl">⚡</span>}
        />
      </div>
    </AppShell>
  );
}
