import React from 'react';
import { AppShell } from '../../components/shell/AppShell';
import { EmptyState } from '@vapor/ui';

export default function ContentPage() {
  return (
    <AppShell>
      <div className="flex-1 flex items-center justify-center">
        <EmptyState
          title="Studio Content Canvas"
          description="Source file editor, diff inspector, and artifact previews will be constructed in Sprint 4."
          icon={<span className="text-xl">🎨</span>}
        />
      </div>
    </AppShell>
  );
}
