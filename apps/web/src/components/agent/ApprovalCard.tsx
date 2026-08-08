'use client';

import React, { useState } from 'react';
import { Card, Typography, Badge, Button } from '@vapor/ui';

export interface ApprovalCardProps {
  approvalId: string;
  runId: string;
  toolName: string;
  actionDescription: string;
  riskLevel: string;
  onApprove: (approvalId: string) => Promise<void>;
  onReject: (approvalId: string) => Promise<void>;
}

export const ApprovalCard: React.FC<ApprovalCardProps> = ({
  approvalId,
  toolName,
  actionDescription,
  riskLevel,
  onApprove,
  onReject,
}) => {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleApprove = async () => {
    setIsSubmitting(true);
    try {
      await onApprove(approvalId);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleReject = async () => {
    setIsSubmitting(true);
    try {
      await onReject(approvalId);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Card variant="panel" className="p-4 border-amber-500/40 bg-amber-950/10 flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-amber-400 font-bold">⚠️ APPROVAL REQUIRED</span>
          <Badge variant={riskLevel === 'external_side_effect' ? 'amber' : 'sky'}>
            {riskLevel.toUpperCase().replace(/_/g, ' ')}
          </Badge>
        </div>
        <Typography variant="caption" className="text-slate-400 font-mono text-[11px]">
          Tool: {toolName}
        </Typography>
      </div>

      <Typography variant="body" className="text-xs text-slate-200 font-mono bg-slate-900/60 p-2.5 rounded border border-slate-800">
        {actionDescription}
      </Typography>

      <div className="flex items-center justify-end gap-3 pt-1">
        <Button variant="ghost" size="sm" onClick={handleReject} disabled={isSubmitting}>
          Reject Action
        </Button>
        <Button variant="primary" size="sm" onClick={handleApprove} disabled={isSubmitting}>
          Approve Action
        </Button>
      </div>
    </Card>
  );
};
