import React from 'react';
import { TransformationResilienceDigitalTwinWorkspace } from '@/components/transformation-resilience-digital-twin/TransformationResilienceDigitalTwinWorkspace';

export const metadata = {
  title: 'Vapor OS — Enterprise Resilience Digital Twin 2.0',
  description: 'Non-destructive digital representation of the enterprise transformation resilience environment: live operational state modeling, isolated scenario forks, stress testing, and reproducible experiments.',
};

export default function TransformationResilienceDigitalTwinPage() {
  return <TransformationResilienceDigitalTwinWorkspace />;
}
