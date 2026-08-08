import React from 'react';
import { Card, Typography, Badge, Button } from '@vapor/ui';
import { MissionStep } from '../../lib/api/missions';

export interface MissionStepsListProps {
  steps: MissionStep[];
  onCompleteStep: (stepId: string) => void;
  onSkipStep: (stepId: string) => void;
  isActionLoading: boolean;
}

export const MissionStepsList: React.FC<MissionStepsListProps> = ({
  steps,
  onCompleteStep,
  onSkipStep,
  isActionLoading,
}) => {
  if (!steps || steps.length === 0) return null;

  const getStatusBadge = (status: MissionStep['status']) => {
    switch (status) {
      case 'in_progress': return <Badge variant="emerald">IN PROGRESS</Badge>;
      case 'ready': return <Badge variant="cyan">READY</Badge>;
      case 'completed': return <Badge variant="emerald">COMPLETED</Badge>;
      case 'failed': return <Badge variant="crimson">FAILED</Badge>;
      case 'skipped': return <Badge variant="amber">SKIPPED</Badge>;
      default: return <Badge variant="default">PENDING</Badge>;
    }
  };

  return (
    <div className="flex flex-col gap-3">
      <Typography variant="h3" className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
        Sequential Steps
      </Typography>

      <div className="flex flex-col gap-3">
        {steps.map((step) => {
          const isExecutable = step.status === 'in_progress' || step.status === 'ready';

          return (
            <Card
              key={step.id}
              variant="panel"
              className={`flex flex-col gap-3 p-4 border-slate-800/80 transition-all ${
                step.status === 'in_progress'
                  ? 'border-emerald-500/30 bg-emerald-500/5'
                  : step.status === 'completed'
                  ? 'bg-slate-900/40 opacity-80'
                  : ''
              }`}
            >
              <div className="flex items-start justify-between gap-3">
                <div className="flex items-start gap-3">
                  <span className="w-6 h-6 rounded-full bg-slate-800 text-slate-300 font-mono text-xs flex items-center justify-center font-bold shrink-0 mt-0.5">
                    {step.order}
                  </span>
                  <div className="flex flex-col gap-1">
                    <Typography variant="h3" className="text-sm font-semibold text-slate-100">
                      {step.title}
                    </Typography>
                    {step.description && (
                      <Typography variant="body" className="text-xs text-slate-400 leading-relaxed">
                        {step.description}
                      </Typography>
                    )}
                  </div>
                </div>

                <div className="flex items-center gap-2 shrink-0">
                  {getStatusBadge(step.status)}
                </div>
              </div>

              {/* Step Output Result if completed */}
              {step.output && (
                <div className="p-2.5 rounded bg-slate-950/80 border border-slate-800 font-mono text-xs text-slate-300">
                  <span className="text-[10px] text-emerald-400 font-semibold block mb-1 uppercase">Step Output</span>
                  <pre className="whitespace-pre-wrap">{JSON.stringify(step.output, null, 2)}</pre>
                </div>
              )}

              {/* Interactive Actions for executable steps */}
              {isExecutable && (
                <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-800/60">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => onSkipStep(step.id)}
                    disabled={isActionLoading}
                  >
                    Skip Step
                  </Button>
                  <Button
                    variant="primary"
                    size="sm"
                    onClick={() => onCompleteStep(step.id)}
                    isLoading={isActionLoading}
                  >
                    ✓ Complete Step
                  </Button>
                </div>
              )}
            </Card>
          );
        })}
      </div>
    </div>
  );
};
