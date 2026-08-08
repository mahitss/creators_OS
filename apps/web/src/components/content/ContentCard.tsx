import React from 'react';
import Link from 'next/link';
import { Card, Typography, Badge, Button } from '@vapor/ui';
import { Content } from '../../lib/api/content';
import { formatDate } from '@vapor/utils';

export interface ContentCardProps {
  item: Content;
  onApprove: (id: string) => void;
  onArchive: (id: string) => void;
}

export const ContentCard: React.FC<ContentCardProps> = ({
  item,
  onApprove,
  onArchive,
}) => {
  const statusVariant = {
    draft: 'default',
    in_review: 'amber',
    approved: 'emerald',
    archived: 'amber',
  }[item.status] as any;

  return (
    <Card variant="panel" className="flex flex-col gap-3 p-4 border-slate-800/80 hover:border-slate-700 transition-all">
      <div className="flex items-start justify-between gap-3">
        <div className="flex flex-col gap-1.5">
          <div className="flex items-center gap-2">
            <Badge variant="cyan">{item.type.toUpperCase()}</Badge>
            <Badge variant={statusVariant}>{item.status.toUpperCase()}</Badge>
            <Link href={`/content/${item.id}`}>
              <Typography variant="h3" className="text-sm font-semibold text-slate-100 hover:text-emerald-400 transition-colors">
                {item.title}
              </Typography>
            </Link>
          </div>
          {item.content && (
            <Typography variant="body" className="text-xs text-slate-400 line-clamp-2 leading-relaxed">
              {item.content}
            </Typography>
          )}
        </div>

        <div className="flex items-center gap-1.5 shrink-0">
          {item.status !== 'approved' && item.status !== 'archived' && (
            <Button variant="primary" size="sm" onClick={() => onApprove(item.id)}>
              ✓ Approve
            </Button>
          )}
          {item.status !== 'archived' && (
            <Button variant="ghost" size="sm" onClick={() => onArchive(item.id)}>
              Archive
            </Button>
          )}
        </div>
      </div>

      <div className="flex items-center justify-between pt-2 border-t border-slate-800/60 text-[11px] font-mono text-slate-500">
        {item.mission_title ? (
          <Link href={`/missions/${item.mission_id}`} className="text-emerald-400/80 hover:underline">
            Mission: {item.mission_title}
          </Link>
        ) : (
          <span>Standalone Deliverable</span>
        )}
        <span>Updated {formatDate(item.updated_at)}</span>
      </div>
    </Card>
  );
};
