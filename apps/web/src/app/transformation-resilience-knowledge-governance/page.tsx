import React from 'react';
import { TransformationResilienceKnowledgeGovernanceWorkspace } from '@/components/transformation-resilience-knowledge-governance/TransformationResilienceKnowledgeGovernanceWorkspace';

export const metadata = {
  title: 'Vapor OS — Continuous Knowledge Assurance & Evidence Quality 2.0',
  description: 'Assurance layer for decision knowledge tracking health dimensions, source independence, context drift, revalidation packets, and lineage.',
};

export default function TransformationResilienceKnowledgeGovernancePage() {
  return <TransformationResilienceKnowledgeGovernanceWorkspace />;
}
