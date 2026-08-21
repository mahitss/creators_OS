'use client';

import React from 'react';
import Link from 'next/link';
import { AlertCircle, ArrowRight } from 'lucide-react';
import { Badge, Button } from '@vapor/ui';
import { AttentionItem } from '../../lib/api/home';

interface NeedsAttentionProps {
  items: AttentionItem[];
}

export const NeedsAttention: React.FC<NeedsAttentionProps> = ({ items }) => {
  if (items.length === 0) return null;

  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-center justify-between pb-1 border-b border-[rgba(255,255,255,0.06)]">
        <div className="flex items-center gap-2">
          <AlertCircle className="w-3.5 h-3.5 text-[#E7B95E]" />
          <span className="text-xs font-bold text-[#F5F5F5] uppercase tracking-widest font-mono">
            ATTENTION QUEUE ({items.length})
          </span>
        </div>
        <Link href="/attention" className="text-[11px] font-mono text-[#62E6B2] hover:underline flex items-center gap-1">
          <span>All Items</span>
          <ArrowRight className="w-3 h-3" />
        </Link>
      </div>

      <div className="flex flex-col divide-y divide-[rgba(255,255,255,0.06)] bg-[#080808] rounded-xl border border-[rgba(255,255,255,0.06)] overflow-hidden">
        {items.map((item) => (
          <div
            key={item.id}
            className="flex flex-col gap-3 p-4 sm:p-5 hover:bg-[#0B0B0B] transition-colors"
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-[#E7B95E] shrink-0" />
                <span className="text-sm font-semibold text-[#F5F5F5] font-sans">
                  {item.title}
                </span>
              </div>
              <Badge variant={item.risk_level === 'HIGH' ? 'crimson' : 'amber'}>
                {item.risk_level} RISK
              </Badge>
            </div>

            <p className="text-xs sm:text-sm text-[#A3A3A3] leading-relaxed">
              {item.context}
            </p>

            <div className="p-2.5 rounded bg-[#050505] border border-[rgba(255,255,255,0.06)] text-xs text-[#858585]">
              <span className="font-semibold text-[#E7B95E] font-mono text-[10px] uppercase tracking-wider mr-1.5">
                IMPACT:
              </span>
              {item.why_it_matters}
            </div>

            <div className="flex items-center gap-3 pt-1">
              <Link href={item.primary_action.href}>
                <Button variant="primary" size="sm">
                  {item.primary_action.label}
                </Button>
              </Link>
              <Link href="/attention">
                <Button variant="secondary" size="sm">
                  Review Context
                </Button>
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

