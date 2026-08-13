import React from 'react';
import { TransformationResilienceSensingWorkspace } from '@/components/transformation-resilience-sensing/TransformationResilienceSensingWorkspace';

export const metadata = {
  title: 'Vapor OS — Enterprise Transformation Resilience Sensing 2.0',
  description: 'Continuous portfolio resilience intelligence, live signal observation, drift detection, and assumption monitoring.',
};

export default function TransformationResilienceSensingPage() {
  return <TransformationResilienceSensingWorkspace />;
}
