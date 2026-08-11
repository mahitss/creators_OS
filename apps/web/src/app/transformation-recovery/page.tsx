import { TransformationRecoveryWorkspace } from '@/components/transformation-recovery/TransformationRecoveryWorkspace';

export const metadata = {
  title: 'Transformation Recovery Orchestration 2.0 | Vapor OS',
  description: 'Disruption → Impact Propagation → Criticality → Recovery Options → Simulation → Human Approval → Verified Execution → Return to Normal.',
};

export default function TransformationRecoveryPage() {
  return <TransformationRecoveryWorkspace />;
}
