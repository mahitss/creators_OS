'use client';

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
        <div className="flex items-center gap-2">
          <span className="text-cyan-400 text-sm">🧠</span>
          <Typography variant="h3" className="text-xs font-bold text-slate-300 uppercase tracking-wider">
            Workspace Context & Learned Memories
          </Typography>
        </div>
        <Link href="/memory/explore" className="text-[11px] font-mono text-cyan-400 hover:text-cyan-300 transition-colors">
          Explore Vault ({memories.length}) →
        </Link>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {memories.map((mem) => (
          <Card
            key={mem.id}
            variant="panel"
            className="flex flex-col gap-2 p-4 border-[rgba(255,255,255,0.10)] bg-[#0B0B0B] hover:border-[rgba(255,255,255,0.18)] hover:bg-[#121212] transition-all rounded-xl shadow-none"
          >
            <div className="flex items-center justify-between gap-2">
              <Badge variant="emerald">{mem.type.toUpperCase()}</Badge>
              <span className="text-[10px] font-mono text-[#666666]">SYNCHRONIZED</span>
            </div>
            <Typography variant="body" className="text-xs font-bold text-[#F5F5F5] line-clamp-1">
              {mem.title}
            </Typography>
            <Typography variant="caption" className="text-xs text-[#A3A3A3] line-clamp-2 leading-relaxed">
              {mem.content}
            </Typography>
          </Card>
        ))}
      </div>
    </div>
  );
};
