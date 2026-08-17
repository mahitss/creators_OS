'use client';

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
      <div className="flex items-center gap-2">
        <span className="text-emerald-400 text-sm">💡</span>
        <Typography variant="h3" className="text-xs font-bold text-emerald-400 uppercase tracking-wider">
          Recommended Next Step
        </Typography>
      </div>

      <Card
        variant="panel"
        className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-5 p-5 sm:p-6 border-emerald-500/30 bg-gradient-to-r from-emerald-500/10 via-emerald-500/5 to-transparent rounded-xl shadow-md"
      >
        <div className="flex flex-col gap-1.5 max-w-xl">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400" />
            <Typography variant="h3" className="text-sm sm:text-base font-bold text-slate-100">
              {recommendation.title}
            </Typography>
          </div>
          <Typography variant="body" className="text-xs sm:text-sm text-slate-300 leading-relaxed">
            {recommendation.reason}
          </Typography>
        </div>

        <Link href={recommendation.action_href} className="shrink-0 w-full sm:w-auto">
          <Button variant="primary" size="md" className="w-full sm:w-auto font-bold shadow-md">
            {recommendation.action_label} →
          </Button>
        </Link>
      </Card>
    </div>
  );
};
