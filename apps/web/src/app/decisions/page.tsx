'use client';

import React from 'react';
import { AppShell } from '../../components/shell/AppShell';
import { DecisionEngineWorkspace } from '../../components/decisions/DecisionEngineWorkspace';

export default function DecisionsPage() {
  return (
    <AppShell>
      <div className="max-w-6xl mx-auto w-full py-4">
        <DecisionEngineWorkspace />
      </div>
    </AppShell>
  );
}
