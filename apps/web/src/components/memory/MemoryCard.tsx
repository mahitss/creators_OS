import React from 'react';
import Link from 'next/link';
import { Card, Typography, Badge, Button } from '@vapor/ui';
import { Memory } from '../../lib/api/memories';
import { formatDate } from '@vapor/utils';

export interface MemoryCardProps {
  memory: Memory;
  onArchiveToggle: (id: string, isArchived: boolean) => void;
  onDelete: (id: string) => void;
}

export const MemoryCard: React.FC<MemoryCardProps> = ({
  memory,
  onArchiveToggle,
  onDelete,
}) => {
  const typeVariant = {
    preference: 'emerald',
    fact: 'cyan',
    decision: 'amber',
    goal: 'emerald',
    insight: 'cyan',
    lesson: 'amber',
    relationship: 'default',
    context: 'default',
  }[memory.type] as any;

  return (
    <Card variant="panel" className="flex flex-col gap-3 p-4 border-slate-800/80 hover:border-slate-700 transition-all">
      <div className="flex items-start justify-between gap-3">
        <div className="flex flex-col gap-1.5">
          <div className="flex items-center gap-2">
            <Badge variant={typeVariant}>{memory.type.toUpperCase()}</Badge>
            <Badge variant={memory.importance === 'critical' ? 'crimson' : memory.importance === 'high' ? 'amber' : 'default'}>
              {memory.importance.toUpperCase()}
            </Badge>
            <Link href={`/memory/${memory.id}`}>
              <Typography variant="h3" className="text-sm font-semibold text-slate-100 hover:text-emerald-400 transition-colors">
                {memory.title}
              </Typography>
            </Link>
          </div>
          <Typography variant="body" className="text-xs text-slate-300 whitespace-pre-wrap leading-relaxed">
            {memory.content}
          </Typography>
        </div>

        <div className="flex items-center gap-1.5 shrink-0">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => onArchiveToggle(memory.id, memory.is_archived)}
          >
            {memory.is_archived ? 'Restore' : 'Archive'}
          </Button>
          <Button
            variant="ghost"
            size="sm"
            className="text-rose-400 hover:text-rose-300"
            onClick={() => onDelete(memory.id)}
          >
            Delete
          </Button>
        </div>
      </div>

      <div className="flex items-center justify-between pt-2 border-t border-slate-800/60 text-[11px] font-mono text-slate-500">
        <span>Source: {memory.source_type}</span>
        <span>Updated {formatDate(memory.updated_at)}</span>
      </div>
    </Card>
  );
};
