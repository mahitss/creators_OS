import React from 'react';
import { Card, Typography, Button, Badge } from '@vapor/ui';
import { MemoryCandidate } from '../../lib/api/memories';

export interface CandidateApprovalBannerProps {
  candidates: MemoryCandidate[];
  onApprove: (id: string) => void;
  onReject: (id: string) => void;
}

export const CandidateApprovalBanner: React.FC<CandidateApprovalBannerProps> = ({
  candidates,
  onApprove,
  onReject,
}) => {
  if (!candidates || candidates.length === 0) return null;

  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-center gap-2">
        <span className="w-2 h-2 rounded-full bg-amber-500 animate-pulse" />
        <Typography variant="h3" className="text-xs font-semibold text-amber-400 uppercase tracking-wider">
          Candidates Awaiting Review ({candidates.length})
        </Typography>
      </div>

      <div className="flex flex-col gap-3">
        {candidates.map((cand) => (
          <Card
            key={cand.id}
            variant="panel"
            className="flex flex-col gap-3 p-4 border-amber-500/30 bg-amber-500/5"
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex flex-col gap-1">
                <div className="flex items-center gap-2">
                  <Badge variant="amber">{cand.type.toUpperCase()}</Badge>
                  <Typography variant="h3" className="text-sm font-semibold text-slate-100">
                    {cand.title}
                  </Typography>
                </div>
                <Typography variant="body" className="text-xs text-slate-300">
                  {cand.content}
                </Typography>
              </div>

              <div className="flex items-center gap-2 shrink-0">
                <Button variant="ghost" size="sm" onClick={() => onReject(cand.id)}>
                  Reject
                </Button>
                <Button variant="primary" size="sm" onClick={() => onApprove(cand.id)}>
                  ✓ Save to Memory
                </Button>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
