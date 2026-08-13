import React from 'react';
import { TransformationResilienceAssuranceCommandWorkspace } from '@/components/transformation-resilience-assurance-command/TransformationResilienceAssuranceCommandWorkspace';

export const metadata = {
  title: 'Vapor OS — Assurance Operations Center 2.0',
  description: 'Real-time operational command center unifying signals, risks, warnings, conflicts, interventions, decision queues, dependency hotspots, and governed executive response.',
};

export default function TransformationResilienceAssuranceCommandPage() {
  return <TransformationResilienceAssuranceCommandWorkspace />;
}
