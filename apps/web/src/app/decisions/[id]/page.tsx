'use client';

import React from 'react';
import { useParams } from 'next/navigation';
import { AppShell } from '../../../components/shell/AppShell';
import { DecisionDetailWorkspace } from '../../../components/decisions/DecisionDetailWorkspace';

export default function DecisionDetailPage() {
  const params = useParams();
  const decisionId = params.id as string;

  return (
    <AppShell>
      <div className="max-w-6xl mx-auto w-full py-4">
        <DecisionDetailWorkspace decisionId={decisionId} />
      </div>
    </AppShell>
  );
}
