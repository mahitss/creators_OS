import React from 'react';
import { EnterpriseEvaluationWorkspace } from '@/components/evaluations/EnterpriseEvaluationWorkspace';

export const metadata = {
  title: 'Evaluation Datasets & Golden Suites — Vapor OS',
  description: 'Immutable Golden Datasets, Benchmark Suites & Version Management'
};

export default function DatasetsPage() {
  return <EnterpriseEvaluationWorkspace />;
}
