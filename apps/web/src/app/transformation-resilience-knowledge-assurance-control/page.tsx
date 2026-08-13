import React from 'react';
import { TransformationResilienceKnowledgeAssuranceControlWorkspace } from '@/components/transformation-resilience-knowledge-assurance-control/TransformationResilienceKnowledgeAssuranceControlWorkspace';

export const metadata = {
  title: 'Vapor OS — Adaptive Knowledge Assurance & Replanning Control 2.0',
  description: 'Continuous plan-impact analysis, live change signal detection, plan staleness tracking, versioned replanning, and stale execution protection.',
};

export default function TransformationResilienceKnowledgeAssuranceControlPage() {
  return <TransformationResilienceKnowledgeAssuranceControlWorkspace />;
}
