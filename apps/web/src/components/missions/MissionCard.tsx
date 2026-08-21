import React from 'react';
import Link from 'next/link';
import { Card, Typography, Badge, Button } from '@vapor/ui';
import { Mission, launchMission, pauseMission, resumeMission, cancelMission } from '../../lib/api/missions';
import { formatDate, truncateText } from '@vapor/utils';

export interface MissionCardProps {
  mission: Mission;
  onMissionUpdate?: (updated: Mission) => void;
}

export const MissionCard: React.FC<MissionCardProps> = ({ mission, onMissionUpdate }) => {
  const normStatus = (mission.status || 'DRAFT').toUpperCase();
  const isDraft = normStatus === 'DRAFT';
  const isQueued = normStatus === 'QUEUED';
  const isPlanning = normStatus === 'PLANNING';
  const isRunning = normStatus === 'RUNNING';
  const isPaused = normStatus === 'PAUSED';
  const isCompleted = normStatus === 'COMPLETED';
  const isFailed = normStatus === 'FAILED';
  const isCancelled = normStatus === 'CANCELLED';

  const statusMap: Record<string, any> = {
    DRAFT: 'default',
    QUEUED: 'amber',
    PLANNING: 'amber',
    RUNNING: 'emerald',
    WAITING: 'amber',
    PAUSED: 'amber',
    COMPLETED: 'cyan',
    FAILED: 'crimson',
    CANCELLED: 'default',
    active: 'emerald',
    completed: 'cyan',
    archived: 'amber',
  };
  const statusVariant = statusMap[normStatus] || statusMap[mission.status] || 'default';

  const priorityMap: Record<string, any> = {
    LOW: 'default',
    MEDIUM: 'cyan',
    HIGH: 'amber',
    CRITICAL: 'crimson',
    URGENT: 'crimson',
    low: 'default',
    medium: 'cyan',
    high: 'amber',
    urgent: 'crimson',
  };
  const priorityVariant = priorityMap[mission.priority?.toUpperCase()] || priorityMap[mission.priority] || 'default';

  const handleLaunch = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    try {
      const updated = await launchMission(mission.id);
      if (onMissionUpdate) onMissionUpdate(updated);
    } catch (err) {
      console.error('Failed to launch mission:', err);
    }
  };

  const handlePause = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    try {
      const updated = await pauseMission(mission.id);
      if (onMissionUpdate) onMissionUpdate(updated);
    } catch (err) {
      console.error('Failed to pause mission:', err);
    }
  };

  const handleResume = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    try {
      const updated = await resumeMission(mission.id);
      if (onMissionUpdate) onMissionUpdate(updated);
    } catch (err) {
      console.error('Failed to resume mission:', err);
    }
  };

  const handleCancel = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    try {
      const updated = await cancelMission(mission.id);
      if (onMissionUpdate) onMissionUpdate(updated);
    } catch (err) {
      console.error('Failed to cancel mission:', err);
    }
  };

  const progress = mission.progress || (isCompleted ? 100 : 0);
  const cost = mission.cost_usd || mission.cost || 0.0;
  const tokens = mission.token_usage?.total_tokens || mission.tokenUsage?.totalTokens || 0;

  return (
    <Link href={`/missions/${mission.id}`}>
      <Card
        variant="panel"
        className="flex flex-col gap-3 p-4 bg-neutral-950 border border-neutral-800 hover:border-neutral-700 transition-all cursor-pointer group"
      >
        <div className="flex items-start justify-between gap-3">
          <div className="flex flex-col gap-1">
            <Typography variant="h3" className="text-sm font-semibold text-neutral-100 group-hover:text-emerald-400 transition-colors">
              {mission.name || mission.title}
            </Typography>
            {mission.goal && mission.goal !== mission.title && (
              <Typography variant="caption" className="text-xs text-neutral-400 font-mono">
                🎯 {truncateText(mission.goal, 90)}
              </Typography>
            )}
            {mission.description && (
              <Typography variant="body" className="text-xs text-neutral-400 line-clamp-2">
                {truncateText(mission.description, 140)}
              </Typography>
            )}
          </div>
          <div className="flex items-center gap-1.5 shrink-0">
            <Badge variant={statusVariant}>{normStatus}</Badge>
            <Badge variant={priorityVariant}>{(mission.priority || 'MEDIUM').toUpperCase()}</Badge>
          </div>
        </div>

        {/* Progress bar */}
        <div className="flex flex-col gap-1">
          <div className="flex items-center justify-between text-[10px] font-mono text-neutral-400">
            <span>PROGRESS</span>
            <span>{Math.round(progress)}%</span>
          </div>
          <div className="w-full h-1 bg-neutral-900 rounded overflow-hidden">
            <div
              className={`h-full transition-all duration-300 ${
                isCompleted ? 'bg-cyan-500' : isFailed ? 'bg-rose-500' : 'bg-emerald-500'
              }`}
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        <div className="flex items-center justify-between pt-2 border-t border-neutral-800/80 text-xs text-neutral-500 font-mono text-[11px]">
          <div className="flex items-center gap-3">
            <span>Updated {formatDate(mission.updated_at || mission.created_at)}</span>
            {tokens > 0 && <span>{tokens.toLocaleString()} tok</span>}
            {cost > 0 && <span>${cost.toFixed(4)}</span>}
          </div>

          <div className="flex items-center gap-1.5">
            {isDraft && (
              <Button variant="primary" size="sm" onClick={handleLaunch}>
                ▶ Launch
              </Button>
            )}
            {(isRunning || isQueued || isPlanning) && (
              <Button variant="ghost" size="sm" onClick={handlePause}>
                ⏸ Pause
              </Button>
            )}
            {isPaused && (
              <Button variant="primary" size="sm" onClick={handleResume}>
                ▶ Resume
              </Button>
            )}
            {!isCompleted && !isCancelled && !isFailed && (
              <Button variant="ghost" size="sm" onClick={handleCancel}>
                ✕ Cancel
              </Button>
            )}
          </div>
        </div>
      </Card>
    </Link>
  );
};
