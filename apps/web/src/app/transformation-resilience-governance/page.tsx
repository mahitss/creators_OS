import React from 'react';
import { TransformationResilienceGovernanceWorkspace } from '@/components/transformation-resilience-governance/TransformationResilienceGovernanceWorkspace';

export const metadata = {
  title: 'Vapor OS — Enterprise Resilience Governance 2.0',
  description: 'Continuous assurance certification, control attestation, audit readiness, release gate verification, and evidence-backed production readiness governance.',
};

export default function TransformationResilienceGovernancePage() {
  return <TransformationResilienceGovernanceWorkspace />;
}
