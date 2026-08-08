import React from 'react';
import Link from 'next/link';
import { Card, Typography, Badge } from '@vapor/ui';
import { LearnedMemoryItem } from '../../lib/api/home';

interface LearnedMemoriesSectionProps {
  memories: LearnedMemoryItem[];
}

export const LearnedMemoriesSection: React.FC<LearnedMemoriesSectionProps> = ({ memories }) => {
  if (!memories || memories.length === 0) return null;

  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <Typography variant="h3" className="text-xs font-semibold text-cyan-400 uppercase tracking-wider">
          Saved Workspace Context
        </Typography>
        <Link href="/memory" className="text-xs font-mono text-slate-400 hover:text-cyan-400 transition-colors">
          View Vault →
        </Link>
      </div>

      <div className="flex flex-col gap-2">
        {memories.map((mem) => (
          <Card key={mem.id} variant="panel" className="flex items-start justify-between p-3.5 border-slate-800/80">
            <div className="flex flex-col gap-1">
              <div className="flex items-center gap-2">
                <Badge variant="cyan">{mem.type.toUpperCase()}</Badge>
                <Typography variant="body" className="text-xs font-semibold text-slate-200">
                  {mem.title}
                </Typography>
              </div>
              <Typography variant="caption" className="text-xs text-slate-400 line-clamp-1">
                {mem.content}
              </Typography>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
