'use client';

import React from 'react';
import Link from 'next/link';
import { Database, ArrowRight } from 'lucide-react';
import { Badge } from '@vapor/ui';
import { LearnedMemoryItem } from '../../lib/api/home';

interface LearnedMemoriesSectionProps {
  memories: LearnedMemoryItem[];
}

export const LearnedMemoriesSection: React.FC<LearnedMemoriesSectionProps> = ({ memories }) => {
  if (!memories || memories.length === 0) return null;

  return (
    <div className="flex flex-col gap-2.5">
      <div className="flex items-center justify-between pb-1 border-b border-[rgba(255,255,255,0.06)]">
        <div className="flex items-center gap-2">
          <Database className="w-3.5 h-3.5 text-[#858585]" />
          <span className="text-xs font-bold text-[#F5F5F5] uppercase tracking-widest font-mono">
            CONTEXT & MEMORY VAULT
          </span>
        </div>
        <Link href="/memory" className="text-[11px] font-mono text-[#62E6B2] hover:underline flex items-center gap-1">
          <span>Vault ({memories.length})</span>
          <ArrowRight className="w-3 h-3" />
        </Link>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
        {memories.map((mem) => (
          <div
            key={mem.id}
            className="flex flex-col gap-2 p-3.5 bg-[#080808] hover:bg-[#0B0B0B] border border-[rgba(255,255,255,0.06)] rounded-lg transition-colors"
          >
            <div className="flex items-center justify-between gap-2">
              <span className="text-[10px] font-mono uppercase bg-[#111111] text-[#62E6B2] px-1.5 py-0.5 rounded border border-[rgba(255,255,255,0.06)]">
                {mem.type.toUpperCase()}
              </span>
              <span className="text-[9px] font-mono text-[#555555]">SYNCHRONIZED</span>
            </div>
            <div className="text-xs font-semibold text-[#F5F5F5] font-sans line-clamp-1">
              {mem.title}
            </div>
            <div className="text-xs text-[#A3A3A3] line-clamp-2 leading-relaxed">
              {mem.content}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

