import React from 'react';
import { AppShell } from '../../components/shell/AppShell';
import { EmptyState } from '@vapor/ui';

export default function MemoryPage() {
  return (
    <AppShell>
      <div className="flex-1 flex items-center justify-center">
        <EmptyState
          title="Context Vault Memory"
          description="Vector embeddings, Knowledge Items (KIs), and state stores will be surfaced in Sprint 4."
          icon={<span className="text-xl">🧠</span>}
        />
      </div>
    </AppShell>
  );
}
