import React from 'react';
import { KnowledgeGovernanceWorkspace } from '@/components/knowledge/KnowledgeGovernanceWorkspace';

export const metadata = {
  title: 'Intelligence Governance & Trust — Vapor OS',
  description: 'Enterprise Intelligence Governance, Provenance, Freshness & Conflict Resolution'
};

export default function GovernancePage() {
  return <KnowledgeGovernanceWorkspace />;
}
