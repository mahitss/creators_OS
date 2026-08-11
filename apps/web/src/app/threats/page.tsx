import { ThreatIntelligenceWorkspace } from '@/components/threats/ThreatIntelligenceWorkspace';

export const metadata = {
  title: 'Enterprise Crisis Prediction & Proactive Threat Intelligence 2.0 | Vapor OS',
  description: 'Governed early-warning engine connecting Signal → Normalization → Weak Signals → Associative Correlation → Threat Patterns → Probability → Early Warning → ActionGateway Mitigation.',
};

export default function ThreatsPage() {
  return <ThreatIntelligenceWorkspace />;
}
