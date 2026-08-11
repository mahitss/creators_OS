import React from 'react';
import { KnowledgeGovernanceWorkspace } from '@/components/knowledge/KnowledgeGovernanceWorkspace';

export const metadata = {
  title: 'Knowledge Health Dashboard — Vapor OS',
  description: 'Source Health, Stale Data Monitoring, Active Conflicts & Grounding Telemetry'
};

export default function HealthPage() {
  return <KnowledgeGovernanceWorkspace />;
}
