'use client';

import React from 'react';
import Link from 'next/link';
import { Zap, ArrowRight } from 'lucide-react';
import { Button } from '@vapor/ui';
import { RecommendationItem } from '../../lib/api/home';

interface PrimaryRecommendationProps {
  recommendation?: RecommendationItem | null;
}

export const PrimaryRecommendation: React.FC<PrimaryRecommendationProps> = ({ recommendation }) => {
  if (!recommendation) return null;

  return (
    <div className="flex flex-col gap-2.5">
      <div className="flex items-center gap-2 pb-1 border-b border-[rgba(255,255,255,0.06)]">
        <Zap className="w-3.5 h-3.5 text-[#62E6B2]" />
        <span className="text-xs font-bold text-[#F5F5F5] uppercase tracking-widest font-mono">
          RECOMMENDED ACTION
        </span>
      </div>

      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-4 sm:p-5 bg-[#080808] rounded-xl border border-[rgba(255,255,255,0.06)] hover:bg-[#0B0B0B] transition-colors">
        <div className="flex flex-col gap-1 max-w-xl">
          <div className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 rounded-full bg-[#62E6B2] shrink-0" />
            <span className="text-sm font-semibold text-[#F5F5F5] font-sans">
              {recommendation.title}
            </span>
          </div>
          <p className="text-xs text-[#A3A3A3] leading-relaxed">
            {recommendation.reason}
          </p>
        </div>

        <Link href={recommendation.action_href} className="shrink-0 w-full sm:w-auto">
          <Button variant="primary" size="sm" className="w-full sm:w-auto">
            {recommendation.action_label}
          </Button>
        </Link>
      </div>
    </div>
  );
};

