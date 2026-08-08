import React from 'react';
import { Card, Typography, Badge, Button } from '@vapor/ui';
import { MissionExecution } from '../../lib/api/missions';

export interface ExecutionControlBarProps {
  execution?: MissionExecution | null;
  hasPlan: boolean;
  hasSteps: boolean;
  onConvertPlanToSteps: () => void;
  onStart: () => void;
  onPause: () => void;
  onResume: () => void;
  onCancel: () => void;
  isActionLoading: boolean;
}

export const ExecutionControlBar: React.FC<ExecutionControlBarProps> = ({
  execution,
  hasPlan,
  hasSteps,
  onConvertPlanToSteps,
  onStart,
  onPause,
  onResume,
  onCancel,
  isActionLoading,
}) => {
  if (!hasSteps) {
    return (
      <Card variant="panel" className="flex flex-col gap-3 p-5 border-slate-800/80 bg-[#12141C]">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-slate-300">
            <span className="w-2 h-2 rounded-full bg-emerald-500" />
            <Typography variant="h3" className="text-sm font-semibold">
              Mission Execution Sequence
            </Typography>
          </div>
          {hasPlan && (
            <Button
              variant="primary"
              size="sm"
              onClick={onConvertPlanToSteps}
              isLoading={isActionLoading}
            >
              ⚡ Convert Plan into Executable Steps
            </Button>
          )}
        </div>
        <Typography variant="caption" className="text-slate-400 leading-relaxed">
          {hasPlan
            ? 'Convert your structured plan into a sequential execution pipeline to begin.'
            : 'Generate an Executive Mission Plan above before initializing execution steps.'}
        </Typography>
      </Card>
    );
  }

  const status = execution?.status || 'idle';
  const completedCount = execution?.completed_steps_count || 0;
  const totalCount = execution?.total_steps_count || 0;
  const progressPercent = totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0;

  const statusVariant = {
    idle: 'default',
    running: 'emerald',
    paused: 'amber',
    completed: 'cyan',
    failed: 'crimson',
    cancelled: 'amber',
  }[status] as any;

  return (
    <Card variant="panel" className="flex flex-col gap-4 p-5 border-slate-800/80 bg-[#12141C]">
      {/* Header & Controls */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <span className={`w-2.5 h-2.5 rounded-full ${status === 'running' ? 'bg-emerald-500 animate-pulse' : 'bg-slate-600'}`} />
          <Typography variant="h3" className="text-sm font-semibold text-slate-100">
            Execution Pipeline
          </Typography>
          <Badge variant={statusVariant}>{status.toUpperCase()}</Badge>
        </div>

        {/* Action Triggers */}
        <div className="flex items-center gap-2">
          {status === 'idle' && (
            <Button variant="primary" size="sm" onClick={onStart} isLoading={isActionLoading}>
              ▶ Start Execution
            </Button>
          )}
          {status === 'running' && (
            <>
              <Button variant="secondary" size="sm" onClick={onPause} isLoading={isActionLoading}>
                ⏸ Pause
              </Button>
              <Button variant="ghost" size="sm" onClick={onCancel} isLoading={isActionLoading}>
                Cancel
              </Button>
            </>
          )}
          {status === 'paused' && (
            <>
              <Button variant="primary" size="sm" onClick={onResume} isLoading={isActionLoading}>
                ▶ Resume
              </Button>
              <Button variant="ghost" size="sm" onClick={onCancel} isLoading={isActionLoading}>
                Cancel
              </Button>
            </>
          )}
          {(status === 'completed' || status === 'cancelled' || status === 'failed') && (
            <Button variant="ghost" size="sm" onClick={onStart} isLoading={isActionLoading}>
              ↻ Restart Pipeline
            </Button>
          )}
        </div>
      </div>

      {/* Progress Bar */}
      <div className="flex flex-col gap-1.5 pt-1">
        <div className="flex items-center justify-between text-xs font-mono text-slate-400">
          <span>{completedCount} of {totalCount} steps completed</span>
          <span>{progressPercent}%</span>
        </div>
        <div className="w-full h-2 bg-slate-900 rounded-full overflow-hidden border border-slate-800">
          <div
            className="h-full bg-emerald-500 transition-all duration-300 ease-out"
            style={{ width: `${progressPercent}%` }}
          />
        </div>
      </div>
    </Card>
  );
};
