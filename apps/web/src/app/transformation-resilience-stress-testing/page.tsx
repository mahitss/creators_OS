import React from 'react';
import { TransformationResilienceStressWorkspace } from '@/components/transformation-resilience-stress/TransformationResilienceStressWorkspace';

export const metadata = {
  title: 'Vapor OS — Autonomous Resilience Simulation & Stress Testing 2.0',
  description: 'Continuous enterprise stress testing, non-production failure injection into Digital Twin sandboxes, compound failure interaction modeling, multi-dimensional scorecards, regression detection, and governed remediation recommendations.',
};

export default function TransformationResilienceStressPage() {
  return <TransformationResilienceStressWorkspace />;
}
