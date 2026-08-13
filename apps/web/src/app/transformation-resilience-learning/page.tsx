import React from 'react';
import { TransformationResilienceLearningWorkspace } from '@/components/transformation-resilience-learning/TransformationResilienceLearningWorkspace';

export const metadata = {
  title: 'Vapor OS — Enterprise Resilience Learning Fabric 2.0',
  description: 'Assurance memory, outcome learning, expected vs actual outcome comparison, model calibration, warning precision/recall tracking, and continuous resilience intelligence.',
};

export default function TransformationResilienceLearningPage() {
  return <TransformationResilienceLearningWorkspace />;
}
