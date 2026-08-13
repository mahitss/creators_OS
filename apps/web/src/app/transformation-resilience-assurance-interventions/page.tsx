import React from 'react';
import { TransformationResilienceAssuranceInterventionsWorkspace } from '@/components/transformation-resilience-assurance-interventions/TransformationResilienceAssuranceInterventionsWorkspace';

export const metadata = {
  title: 'Vapor OS — Assurance Intervention Orchestration 2.0',
  description: 'Turn credible early warnings into evidence-backed, governed intervention plans: option reversibility, rollback plans, contingency readiness, ActionGateway protection, and human decision authority.',
};

export default function TransformationResilienceAssuranceInterventionsPage() {
  return <TransformationResilienceAssuranceInterventionsWorkspace />;
}
