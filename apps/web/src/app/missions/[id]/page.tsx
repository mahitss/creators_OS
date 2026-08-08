'use client';

import React, { useState, useEffect, useCallback } from 'react';
import Link from 'next/link';
import { useParams, useRouter } from 'next/navigation';
import { AppShell } from '../../../components/shell/AppShell';
import { getMission, updateMission, completeMission, archiveMission, Mission } from '../../../lib/api/missions';
import { ActivityTimeline } from '../../../components/missions/ActivityTimeline';
import { Typography, Card, Badge, Button, Spinner, ErrorState, Dialog, Input, Textarea, Select } from '@vapor/ui';
import { formatDate } from '@vapor/utils';

export default function MissionDetailPage() {
  const params = useParams();
  const router = useRouter();
  const missionId = params.id as string;

  const [mission, setMission] = useState<Mission | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);
  const [isEditing, setIsEditing] = useState(false);

  // Edit form state
  const [editTitle, setEditTitle] = useState('');
  const [editDescription, setEditDescription] = useState('');
  const [editPriority, setEditPriority] = useState<'low' | 'medium' | 'high' | 'urgent'>('medium');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const loadMissionDetail = useCallback(async () => {
    setIsLoading(true);
    setIsError(false);
    try {
      const res = await getMission(missionId);
      setMission(res);
      setEditTitle(res.title);
      setEditDescription(res.description);
      setEditPriority(res.priority);
    } catch (err) {
      console.error('Failed to load mission detail:', err);
      setIsError(true);
    } finally {
      setIsLoading(false);
    }
  }, [missionId]);

  useEffect(() => {
    if (missionId) loadMissionDetail();
  }, [missionId, loadMissionDetail]);

  const handleComplete = async () => {
    if (!mission) return;
    try {
      const updated = await completeMission(mission.id);
      setMission(updated);
    } catch (err) {
      console.error('Failed to complete mission:', err);
    }
  };

  const handleArchive = async () => {
    if (!mission) return;
    try {
      const updated = await archiveMission(mission.id);
      setMission(updated);
    } catch (err) {
      console.error('Failed to archive mission:', err);
    }
  };

  const handleEditSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!mission || !editTitle.trim()) return;

    setIsSubmitting(true);
    try {
      const updated = await updateMission(mission.id, {
        title: editTitle.trim(),
        description: editDescription.trim(),
        priority: editPriority,
      });
      setMission(updated);
      setIsEditing(false);
    } catch (err) {
      console.error('Failed to update mission:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <AppShell>
      <div className="max-w-4xl mx-auto w-full flex flex-col gap-6 py-2">
        {/* Navigation Back Link */}
        <Link href="/missions" className="inline-flex items-center gap-1 text-xs text-slate-400 hover:text-emerald-400 transition-colors">
          ← Back to Missions
        </Link>

        {isLoading ? (
          <div className="flex flex-col items-center justify-center p-12 gap-3">
            <Spinner size="md" />
            <Typography variant="caption" className="text-slate-500 font-mono">
              Opening mission workspace...
            </Typography>
          </div>
        ) : isError || !mission ? (
          <ErrorState
            title="Mission Not Found"
            message="The requested mission could not be found or belongs to another workspace."
            onRetry={loadMissionDetail}
          />
        ) : (
          <div className="flex flex-col gap-6">
            {/* Header Section */}
            <Card variant="panel" className="flex flex-col gap-4 p-6 border-slate-800/80">
              <div className="flex items-start justify-between gap-4">
                <div className="flex flex-col gap-2">
                  <div className="flex items-center gap-2">
                    <Badge variant={mission.status === 'completed' ? 'cyan' : mission.status === 'archived' ? 'amber' : 'emerald'}>
                      {mission.status.toUpperCase()}
                    </Badge>
                    <Badge variant={mission.priority === 'urgent' ? 'crimson' : mission.priority === 'high' ? 'amber' : 'default'}>
                      {mission.priority.toUpperCase()} PRIORITY
                    </Badge>
                  </div>
                  <Typography variant="h1" className="text-xl sm:text-2xl font-bold text-slate-100">
                    {mission.title}
                  </Typography>
                </div>

                <div className="flex items-center gap-2">
                  <Button variant="ghost" size="sm" onClick={() => setIsEditing(true)}>
                    Edit
                  </Button>
                  {mission.status !== 'completed' && mission.status !== 'archived' && (
                    <Button variant="primary" size="sm" onClick={handleComplete}>
                      ✓ Complete
                    </Button>
                  )}
                  {mission.status !== 'archived' && (
                    <Button variant="ghost" size="sm" onClick={handleArchive}>
                      Archive
                    </Button>
                  )}
                </div>
              </div>

              {mission.description && (
                <div className="pt-2 border-t border-slate-800/60">
                  <Typography variant="body" className="text-slate-300 whitespace-pre-wrap leading-relaxed">
                    {mission.description}
                  </Typography>
                </div>
              )}

              <div className="flex items-center justify-between pt-2 text-[11px] font-mono text-slate-500">
                <span>Created {formatDate(mission.created_at)}</span>
                <span>Updated {formatDate(mission.updated_at)}</span>
              </div>
            </Card>

            {/* Honest AI Area */}
            <Card variant="panel" className="flex flex-col gap-3 p-5 border-slate-800/80 bg-[#12141C]">
              <div className="flex items-center gap-2 text-slate-300">
                <span className="w-2 h-2 rounded-full bg-emerald-500" />
                <Typography variant="h3" className="text-sm font-semibold">
                  Executive AI Execution
                </Typography>
              </div>
              <Typography variant="caption" className="text-slate-400 leading-relaxed">
                Vapor hasn't started automated background execution on this mission yet. Execution agents will be connected in Sprint 6.
              </Typography>
            </Card>

            {/* Activity Timeline */}
            <ActivityTimeline activities={mission.activities} />
          </div>
        )}

        {/* Edit Dialog */}
        {mission && (
          <Dialog isOpen={isEditing} onClose={() => setIsEditing(false)} title="Edit Mission Details">
            <form onSubmit={handleEditSubmit} className="flex flex-col gap-4 mt-2">
              <Input
                label="Mission Title"
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
                required
              />
              <Textarea
                label="Description"
                value={editDescription}
                onChange={(e) => setEditDescription(e.target.value)}
                rows={4}
              />
              <Select
                label="Priority"
                value={editPriority}
                onChange={(e) => setEditPriority(e.target.value as any)}
                options={[
                  { label: 'Low Priority', value: 'low' },
                  { label: 'Medium Priority', value: 'medium' },
                  { label: 'High Priority', value: 'high' },
                  { label: 'Urgent Priority', value: 'urgent' },
                ]}
              />
              <div className="flex items-center justify-end gap-2 pt-3 border-t border-slate-800">
                <Button type="button" variant="ghost" onClick={() => setIsEditing(false)} disabled={isSubmitting}>
                  Cancel
                </Button>
                <Button type="submit" variant="primary" isLoading={isSubmitting}>
                  Save Changes
                </Button>
              </div>
            </form>
          </Dialog>
        )}
      </div>
    </AppShell>
  );
}
