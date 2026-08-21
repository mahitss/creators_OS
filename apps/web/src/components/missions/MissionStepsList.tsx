import React from 'react';
import { Card, Typography, Badge, Button } from '@vapor/ui';
import { MissionStep } from '../../lib/api/missions';

export interface MissionStepsListProps {
  steps: MissionStep[];
  onCompleteStep?: (stepId: string) => void;
  onSkipStep?: (stepId: string) => void;
  isActionLoading?: boolean;
}

export const MissionStepsList: React.FC<MissionStepsListProps> = ({
  steps,
  onCompleteStep,
  onSkipStep,
  isActionLoading = false,
}) => {
  if (!steps || steps.length === 0) return null;

  const getStatusBadge = (status: MissionStep['status']) => {
    const s = String(status).toUpperCase();
    switch (s) {
      case 'RUNNING':
      case 'IN_PROGRESS':
        return <Badge variant="emerald">RUNNING</Badge>;
      case 'READY':
        return <Badge variant="cyan">READY</Badge>;
      case 'COMPLETED':
        return <Badge variant="cyan">COMPLETED</Badge>;
      case 'FAILED':
        return <Badge variant="crimson">FAILED</Badge>;
      case 'SKIPPED':
        return <Badge variant="amber">SKIPPED</Badge>;
      default:
        return <Badge variant="default">PENDING</Badge>;
    }
  };

  const getStepTypeBadge = (stepType?: string) => {
    const t = (stepType || 'analysis').toLowerCase();
    const colors: Record<string, string> = {
      retrieval: 'text-sky-400 bg-sky-500/10 border-sky-500/30',
      analysis: 'text-purple-400 bg-purple-500/10 border-purple-500/30',
      reasoning: 'text-amber-400 bg-amber-500/10 border-amber-500/30',
      generation: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30',
      action: 'text-cyan-400 bg-cyan-500/10 border-cyan-500/30',
    };
    const cls = colors[t] || 'text-neutral-400 bg-neutral-900 border-neutral-800';
    return (
      <span className={`px-1.5 py-0.5 text-[10px] font-mono font-semibold rounded border uppercase ${cls}`}>
        {t}
      </span>
    );
  };

  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <Typography variant="h3" className="text-xs font-semibold text-neutral-300 uppercase tracking-wider font-mono">
          Execution Steps ({steps.length})
        </Typography>
      </div>

      <div className="flex flex-col gap-3">
        {steps.map((step, idx) => {
          const stepNum = step.step_number || step.order || idx + 1;
          const sUpper = String(step.status).toUpperCase();
          const isRunning = sUpper === 'RUNNING' || sUpper === 'IN_PROGRESS';
          const isCompleted = sUpper === 'COMPLETED';
          const isFailed = sUpper === 'FAILED';
          const isExecutable = sUpper === 'READY' || sUpper === 'PENDING';

          return (
            <Card
              key={step.id || `step_${stepNum}`}
              variant="panel"
              className={`flex flex-col gap-3 p-4 bg-neutral-950 border transition-all ${
                isRunning
                  ? 'border-emerald-500/50 bg-emerald-950/10'
                  : isCompleted
                  ? 'border-neutral-800/80 bg-neutral-900/20'
                  : isFailed
                  ? 'border-rose-500/50 bg-rose-950/10'
                  : 'border-neutral-800'
              }`}
            >
              <div className="flex items-start justify-between gap-3">
                <div className="flex items-start gap-3">
                  <span className="w-6 h-6 rounded bg-neutral-900 border border-neutral-800 text-neutral-300 font-mono text-xs flex items-center justify-center font-bold shrink-0 mt-0.5">
                    {stepNum}
                  </span>
                  <div className="flex flex-col gap-1">
                    <div className="flex items-center gap-2">
                      <Typography variant="h3" className="text-sm font-semibold text-neutral-100 font-mono">
                        {step.name || step.title}
                      </Typography>
                      {getStepTypeBadge(step.step_type)}
                    </div>
                    {step.description && (
                      <Typography variant="body" className="text-xs text-neutral-400 leading-relaxed">
                        {step.description}
                      </Typography>
                    )}
                  </div>
                </div>

                <div className="flex items-center gap-2 shrink-0">
                  {getStatusBadge(step.status)}
                </div>
              </div>

              {/* Step Metrics */}
              <div className="flex items-center gap-4 text-[11px] font-mono text-neutral-500 pt-1 border-t border-neutral-900">
                {step.duration_ms !== undefined && step.duration_ms > 0 && (
                  <span>⏱ {step.duration_ms}ms</span>
                )}
                {step.token_usage && step.token_usage.total_tokens > 0 && (
                  <span>🪙 {step.token_usage.total_tokens} tokens</span>
                )}
                {step.cost_usd !== undefined && step.cost_usd > 0 && (
                  <span>💵 ${step.cost_usd.toFixed(4)}</span>
                )}
                {step.retry_count !== undefined && step.retry_count > 0 && (
                  <span className="text-amber-400">↺ Retries: {step.retry_count}/{step.max_retries || 3}</span>
                )}
              </div>

              {/* Step Error if failed */}
              {step.error && (
                <div className="p-2.5 rounded bg-rose-950/30 border border-rose-900/50 font-mono text-xs text-rose-300">
                  <span className="text-[10px] text-rose-400 font-semibold block mb-1 uppercase">Failure Reason</span>
                  <pre className="whitespace-pre-wrap leading-relaxed text-[11px]">
                    {typeof step.error === 'object' ? JSON.stringify(step.error, null, 2) : String(step.error)}
                  </pre>
                </div>
              )}

              {/* Step Output Result if completed */}
              {step.output && (
                <div className="p-2.5 rounded bg-neutral-900/80 border border-neutral-800 font-mono text-xs text-neutral-300">
                  <span className="text-[10px] text-emerald-400 font-semibold block mb-1 uppercase">Step Output Payload</span>
                  <pre className="whitespace-pre-wrap leading-relaxed text-[11px] max-h-48 overflow-y-auto">
                    {typeof step.output === 'object' ? JSON.stringify(step.output, null, 2) : String(step.output)}
                  </pre>
                </div>
              )}

              {/* Interactive Actions */}
              {isExecutable && onCompleteStep && onSkipStep && (
                <div className="flex items-center justify-end gap-2 pt-2 border-t border-neutral-900">
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
