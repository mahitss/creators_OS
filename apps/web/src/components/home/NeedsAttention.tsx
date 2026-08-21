'use client';

import React from 'react';
import Link from 'next/link';
import { Card, Typography, Badge, Button } from '@vapor/ui';
import { AttentionItem } from '../../lib/api/home';

interface NeedsAttentionProps {
  items: AttentionItem[];
}

export const NeedsAttention: React.FC<NeedsAttentionProps> = ({ items }) => {
  if (items.length === 0) return null;

  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-amber-400 text-sm">🔔</span>
          <Typography variant="h3" className="text-xs font-bold text-slate-300 uppercase tracking-wider">
            Needs Your Attention ({items.length})
          </Typography>
        </div>
        <Link href="/attention" className="text-[11px] font-mono text-emerald-400 hover:text-emerald-300 transition-colors">
          View All Items →
        </Link>
      </div>

      <div className="flex flex-col gap-3">
        {items.map((item) => (
          <Card
            key={item.id}
            variant="panel"
            className="flex flex-col gap-3.5 p-5 border-[rgba(255,255,255,0.10)] bg-[#0B0B0B] rounded-xl shadow-none hover:bg-[#0E0E0E] transition-colors"
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-[#E7B95E] shrink-0" />
                <Typography variant="h3" className="text-sm sm:text-base font-bold text-[#F5F5F5]">
                  {item.title}
                </Typography>
              </div>
              <Badge variant={item.risk_level === 'HIGH' ? 'crimson' : 'amber'}>
                {item.risk_level} RISK
              </Badge>
            </div>

            <Typography variant="body" className="text-xs sm:text-sm text-[#A3A3A3] leading-relaxed">
              {item.context}
            </Typography>

            <div className="p-2.5 rounded-lg bg-[#080808] border border-[rgba(255,255,255,0.08)] text-xs text-[#A3A3A3]">
              <span className="font-semibold text-[#E7B95E] font-mono text-[11px] uppercase tracking-wide mr-1.5">
                Impact Analysis:
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
          </Card>
        ))}
      </div>
    </div>
  );
};
