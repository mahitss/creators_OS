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
      <Typography variant="h3" className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
        Needs Your Attention
      </Typography>

      <div className="flex flex-col gap-3">
        {items.map((item) => (
          <Card key={item.id} variant="panel" className="flex flex-col gap-3 p-4 border-amber-500/20 bg-amber-500/5">
            <div className="flex items-center justify-between">
              <Typography variant="h3" className="text-sm font-semibold text-slate-100">
                {item.title}
              </Typography>
              <Badge variant={item.risk_level === 'HIGH' ? 'crimson' : 'amber'}>
                {item.risk_level}
              </Badge>
            </div>
            <Typography variant="body" className="text-xs text-slate-300">
              {item.context}
            </Typography>
            <Typography variant="caption" className="text-xs text-slate-400">
              <span className="font-semibold text-slate-300">Why it matters:</span> {item.why_it_matters}
            </Typography>
            <div className="flex items-center gap-2 pt-1">
              <Link href={item.primary_action.href}>
                <Button variant="primary" size="sm">
                  {item.primary_action.label}
                </Button>
              </Link>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
