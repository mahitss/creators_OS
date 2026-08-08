import React from 'react';
import Link from 'next/link';
import { Card, Typography, Button } from '@vapor/ui';
import { RecommendationItem } from '../../lib/api/home';

interface PrimaryRecommendationProps {
  recommendation?: RecommendationItem | null;
}

export const PrimaryRecommendation: React.FC<PrimaryRecommendationProps> = ({ recommendation }) => {
  if (!recommendation) return null;

  return (
    <div className="flex flex-col gap-3">
      <Typography variant="h3" className="text-xs font-semibold text-emerald-400 uppercase tracking-wider">
        Recommended Next Step
      </Typography>

      <Card variant="panel" className="flex flex-col gap-3 p-5 border-emerald-500/20 bg-emerald-500/5">
        <div className="flex items-start justify-between gap-4">
          <div className="flex flex-col gap-1">
            <Typography variant="h3" className="text-sm font-semibold text-slate-100">
              {recommendation.title}
            </Typography>
            <Typography variant="body" className="text-xs text-slate-300">
              {recommendation.reason}
            </Typography>
          </div>

          <Link href={recommendation.action_href}>
            <Button variant="primary" size="sm">
              {recommendation.action_label}
            </Button>
          </Link>
        </div>
      </Card>
    </div>
  );
};
