import { TransformationSimulationWorkspace } from '@/components/transformation-simulation/TransformationSimulationWorkspace';

export const metadata = {
  title: 'Digital Twin Simulation 2.0 | Vapor OS',
  description: 'Strategy → Operating Model → Portfolios → Dependencies → Capacity → Decision Simulation → Range Outputs (Low/Expected/High) → Human Approval.',
};

export default function TransformationSimulationPage() {
  return <TransformationSimulationWorkspace />;
}
