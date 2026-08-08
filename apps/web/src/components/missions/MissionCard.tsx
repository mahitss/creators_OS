import React from 'react';
import Link from 'next/link';
import { Card, Typography, Badge, Button } from '@vapor/ui';
import { Mission, completeMission, archiveMission } from '../../lib/api/missions';
import { formatDate, truncateText } from '@vapor/utils';

export interface MissionCardProps {
  mission: Mission;
  onMissionUpdate?: (updated: Mission) => void;
}

export const MissionCard: React.FC<MissionCardProps> = ({ mission, onMissionUpdate }) => {
  const isCompleted = mission.status === 'completed';
  const isArchived = mission.status === 'archived';

  const statusVariant = {
    active: 'emerald',
    draft: 'default',
    completed: 'cyan',
    archived: 'amber',
  }[mission.status] as any;

  const priorityVariant = {
    low: 'default',
    medium: 'cyan',
    high: 'amber',
    urgent: 'crimson',
  }[mission.priority] as any;

  const handleComplete = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    try {
      const updated = await completeMission(mission.id);
      if (onMissionUpdate) onMissionUpdate(updated);
    } catch (err) {
      console.error('Failed to complete mission:', err);
    }
  };

  const handleArchive = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    try {
      const updated = await archiveMission(mission.id);
      if (onMissionUpdate) onMissionUpdate(updated);
    } catch (err) {
      console.error('Failed to archive mission:', err);
    }
  };

  return (
    <Link href={`/missions/${mission.id}`}>
      <Card
        variant="panel"
        className="flex flex-col gap-3 p-4 border-slate-800/80 hover:border-slate-700 hover:bg-slate-850/50 transition-all cursor-pointer group"
      >
        <div className="flex items-start justify-between gap-3">
          <div className="flex flex-col gap-1">
            <Typography variant="h3" className="text-sm font-semibold text-slate-100 group-hover:text-emerald-400 transition-colors">
              {mission.title}
            </Typography>
            {mission.description && (
              <Typography variant="body" className="text-xs text-slate-400 line-clamp-2">
                {truncateText(mission.description, 140)}
              </Typography>
            )}
          </div>
          <div className="flex items-center gap-1.5 shrink-0">
            <Badge variant={statusVariant}>{mission.status.toUpperCase()}</Badge>
            <Badge variant={priorityVariant}>{mission.priority.toUpperCase()}</Badge>
          </div>
        </div>

        <div className="flex items-center justify-between pt-2 border-t border-slate-800/60 text-xs text-slate-500">
          <span className="font-mono text-[11px]">
            Updated {formatDate(mission.updated_at)}
          </span>

          <div className="flex items-center gap-2">
            {!isCompleted && !isArchived && (
              <Button variant="ghost" size="sm" onClick={handleComplete}>
                ✓ Complete
              </Button>
            )}
            {!isArchived && (
              <Button variant="ghost" size="sm" onClick={handleArchive}>
                Archive
              </Button>
            )}
          </div>
        </div>
      </Card>
    </Link>
  );
};
