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
            className="flex flex-col gap-3.5 p-5 border-amber-500/30 bg-gradient-to-r from-amber-500/10 via-amber-500/5 to-transparent rounded-xl shadow-sm"
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-amber-400 animate-pulse" />
                <Typography variant="h3" className="text-sm sm:text-base font-bold text-slate-100">
                  {item.title}
                </Typography>
              </div>
              <Badge variant={item.risk_level === 'HIGH' ? 'crimson' : 'amber'}>
                {item.risk_level} RISK
              </Badge>
            </div>

            <Typography variant="body" className="text-xs sm:text-sm text-slate-300 leading-relaxed">
              {item.context}
            </Typography>

            <div className="p-2.5 rounded-lg bg-black/40 border border-slate-800/80 text-xs text-slate-300">
              <span className="font-semibold text-amber-400 font-mono text-[11px] uppercase tracking-wide mr-1.5">
                Impact Analysis:
              </span>
              {item.why_it_matters}
            </div>

            <div className="flex items-center gap-3 pt-1">
              <Link href={item.primary_action.href}>
                <Button variant="primary" size="sm" className="bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold border-none shadow-md">
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
