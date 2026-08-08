import React from 'react';
import Link from 'next/link';
import { Card, Typography, Badge, Button } from '@vapor/ui';
import { AttentionItem } from '../../lib/api/attention';
import { formatDate } from '@vapor/utils';

export interface AttentionItemCardProps {
  item: AttentionItem;
  onResolve: (id: string) => void;
  onSnooze: (id: string) => void;
  onDismiss: (id: string) => void;
}

export const AttentionItemCard: React.FC<AttentionItemCardProps> = ({
  item,
  onResolve,
  onSnooze,
  onDismiss,
}) => {
  const severityVariant = {
    urgent: 'crimson',
    high: 'amber',
    medium: 'default',
    low: 'default',
  }[item.severity] as any;

  return (
    <Card variant="panel" className="flex flex-col gap-3 p-4 border-slate-800/80 hover:border-slate-700 transition-all">
      <div className="flex items-start justify-between gap-3">
        <div className="flex flex-col gap-1.5">
          <div className="flex items-center gap-2">
            <Badge variant={severityVariant}>{item.severity.toUpperCase()}</Badge>
            <Badge variant="cyan">{item.type.replace('_', ' ').toUpperCase()}</Badge>
            <Typography variant="h3" className="text-sm font-semibold text-slate-100">
              {item.title}
            </Typography>
          </div>
          <Typography variant="body" className="text-xs text-slate-300 leading-relaxed">
            {item.description}
          </Typography>
        </div>

        <div className="flex items-center gap-1.5 shrink-0">
          <Link href={item.primary_action.href}>
            <Button variant="primary" size="sm">
              {item.primary_action.label}
            </Button>
          </Link>
          {item.status === 'open' && (
            <>
              <Button variant="ghost" size="sm" onClick={() => onResolve(item.id)}>
                ✓ Resolve
              </Button>
              <Button variant="ghost" size="sm" onClick={() => onSnooze(item.id)}>
                Snooze
              </Button>
              <Button variant="ghost" size="sm" className="text-rose-400 hover:text-rose-300" onClick={() => onDismiss(item.id)}>
                Dismiss
              </Button>
            </>
          )}
        </div>
      </div>

      <div className="flex items-center justify-between pt-2 border-t border-slate-800/60 text-[11px] font-mono text-slate-500">
        <span>Source: {item.source_type} ({item.source_id})</span>
        <span>Created {formatDate(item.created_at)}</span>
      </div>
    </Card>
  );
};
