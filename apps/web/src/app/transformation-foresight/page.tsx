import { TransformationForesightWorkspace } from '@/components/transformation-foresight/TransformationForesightWorkspace';

export const metadata = {
  title: 'Enterprise Transformation Foresight 2.0 | Vapor OS',
  description: 'Observed Signals → Drivers → Future States → Scenarios → Multi-Order Propagation → Vulnerability & Robustness → No-Regret Actions → Triggers & Reviews.',
};

export default function TransformationForesightPage() {
  return <TransformationForesightWorkspace />;
}
