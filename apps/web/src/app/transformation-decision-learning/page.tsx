import { TransformationDecisionLearningWorkspace } from '@/components/transformation-decision-learning/TransformationDecisionLearningWorkspace';

export const metadata = {
  title: 'Enterprise Decision Learning 2.0 | Vapor OS',
  description: 'Question → Context → Evidence → Options → Decision → Approval → Execution → Actual Outcome → Variance → Lessons → Pattern Detection → Forecast Calibration.',
};

export default function TransformationDecisionLearningPage() {
  return <TransformationDecisionLearningWorkspace />;
}
