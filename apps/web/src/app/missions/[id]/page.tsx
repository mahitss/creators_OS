'use client';

import React, { useState, useEffect, useCallback, useRef } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { AppShell } from '../../../components/shell/AppShell';
import {
  getMission,
  updateMission,
  launchMission,
  pauseMission,
  resumeMission,
  cancelMission,
  fetchMissionSteps,
  fetchMissionEvents,
  Mission,
  MissionStep,
  MissionEvent,
} from '../../../lib/api/missions';
import { ActivityTimeline } from '../../../components/missions/ActivityTimeline';
import { MissionStepsList } from '../../../components/missions/MissionStepsList';
import { Typography, Card, Badge, Button, Spinner, ErrorState, Dialog, Input, Textarea, Select } from '@vapor/ui';
import { formatDate } from '@vapor/utils';

export default function MissionDetailPage() {
  const params = useParams();
  const missionId = params.id as string;

  const [mission, setMission] = useState<Mission | null>(null);
  const [steps, setSteps] = useState<MissionStep[]>([]);
  const [events, setEvents] = useState<MissionEvent[]>([]);

  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [isActionLoading, setIsActionLoading] = useState(false);

  // Edit form state
  const [editTitle, setEditTitle] = useState('');
  const [editGoal, setEditGoal] = useState('');
  const [editDescription, setEditDescription] = useState('');
  const [editPriority, setEditPriority] = useState<string>('medium');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const eventSourceRef = useRef<EventSource | null>(null);

  const loadMissionDetail = useCallback(async () => {
    setIsLoading(true);
    setIsError(false);
    try {
      const [resMission, resSteps, resEvents] = await Promise.all([
        getMission(missionId),
        fetchMissionSteps(missionId),
        fetchMissionEvents(missionId).catch(() => []),
      ]);

      setMission(resMission);
      setSteps(resSteps.steps || []);
      setEvents(resEvents);

      setEditTitle(resMission.name || resMission.title);
      setEditGoal(resMission.goal || resMission.title);
      setEditDescription(resMission.description);
      setEditPriority((resMission.priority || 'medium').toLowerCase());
    } catch (err) {
      console.error('Failed to load mission detail:', err);
      setIsError(true);
    } finally {
      setIsLoading(false);
    }
  }, [missionId]);

  useEffect(() => {
    if (missionId) {
      loadMissionDetail();
    }
  }, [missionId, loadMissionDetail]);

  // Real-time SSE Connection
  useEffect(() => {
    if (!missionId) return;

    try {
      const es = new EventSource(`/api/v1/missions/${missionId}/stream`);
      eventSourceRef.current = es;

      es.onmessage = (event) => {
        try {
          const parsed = JSON.parse(event.data);
          if (parsed && parsed.event_type && parsed.event_type !== 'STREAM_CONNECTED') {
            setEvents((prev) => {
              if (prev.some((e) => e.id === parsed.id)) return prev;
              return [parsed, ...prev];
            });

            // Reload mission data smoothly when lifecycle events arrive
            if (
              [
                'MISSION_QUEUED',
                'MISSION_PLANNING',
                'PLAN_CREATED',
                'STEP_STARTED',
                'STEP_COMPLETED',
                'STEP_FAILED',
                'MISSION_PAUSED',
                'MISSION_RESUMED',
                'MISSION_COMPLETED',
                'MISSION_FAILED',
                'MISSION_CANCELLED',
              ].includes(parsed.event_type)
            ) {
              getMission(missionId).then((m) => setMission(m)).catch(() => {});
              fetchMissionSteps(missionId).then((s) => setSteps(s.steps || [])).catch(() => {});
            }
          }
        } catch (e) {
          // Ignore keepalives or parsing errors
        }
      };

      es.onerror = () => {
        // SSE disconnected or closed by server
      };

      return () => {
        es.close();
      };
    } catch (e) {
      console.debug('SSE connection could not be established:', e);
    }
  }, [missionId]);

  const handleLaunch = async () => {
    if (!mission) return;
    setIsActionLoading(true);
    try {
      const updated = await launchMission(mission.id);
      setMission(updated);
      const resSteps = await fetchMissionSteps(mission.id);
      setSteps(resSteps.steps || []);
    } catch (err) {
      console.error('Failed to launch mission:', err);
    } finally {
      setIsActionLoading(false);
    }
  };

  const handlePause = async () => {
    if (!mission) return;
    setIsActionLoading(true);
    try {
      const updated = await pauseMission(mission.id);
      setMission(updated);
    } catch (err) {
      console.error('Failed to pause mission:', err);
    } finally {
      setIsActionLoading(false);
    }
  };

  const handleResume = async () => {
    if (!mission) return;
    setIsActionLoading(true);
    try {
      const updated = await resumeMission(mission.id);
      setMission(updated);
    } catch (err) {
      console.error('Failed to resume mission:', err);
    } finally {
      setIsActionLoading(false);
    }
  };

  const handleCancel = async () => {
    if (!mission) return;
    setIsActionLoading(true);
    try {
      const updated = await cancelMission(mission.id);
      setMission(updated);
    } catch (err) {
      console.error('Failed to cancel mission:', err);
    } finally {
      setIsActionLoading(false);
    }
  };

  const handleSaveEdit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!mission) return;
    setIsSubmitting(true);
    try {
      const updated = await updateMission(mission.id, {
        name: editTitle,
        title: editTitle,
        goal: editGoal,
        description: editDescription,
        priority: editPriority.toUpperCase(),
      });
      setMission(updated);
      setIsEditing(false);
    } catch (err) {
      console.error('Failed to update mission:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <AppShell>
        <div className="flex flex-col items-center justify-center p-24 gap-3">
          <Spinner size="md" />
          <Typography variant="caption" className="text-neutral-500 font-mono text-xs">
            Connecting to mission telemetry stream...
          </Typography>
        </div>
      </AppShell>
    );
  }

  if (isError || !mission) {
    return (
      <AppShell>
        <div className="max-w-4xl mx-auto w-full py-8">
          <ErrorState
            title="Mission Not Found"
            message="Could not retrieve specified mission. It may belong to another workspace or has been removed."
            onRetry={loadMissionDetail}
          />
        </div>
      </AppShell>
    );
  }

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
  };
  const statusVariant = statusMap[normStatus] || 'default';

  const progress = mission.progress || (isCompleted ? 100 : 0);
  const cost = mission.cost_usd || mission.cost || 0.0;
  const tokens = mission.token_usage?.total_tokens || mission.tokenUsage?.totalTokens || 0;
  const inTokens = mission.token_usage?.input_tokens || mission.tokenUsage?.inputTokens || 0;
  const outTokens = mission.token_usage?.output_tokens || mission.tokenUsage?.outputTokens || 0;

  return (
    <AppShell>
      <div className="max-w-5xl mx-auto w-full flex flex-col gap-6 py-4">
        {/* Navigation Breadcrumb */}
        <div className="flex items-center gap-2 text-xs text-neutral-400 font-mono">
          <Link href="/missions" className="hover:text-neutral-200 transition-colors">
            ← Autonomous Missions
          </Link>
          <span>/</span>
          <span className="text-neutral-300">{mission.id}</span>
        </div>

        {/* Mission Master Header Panel */}
        <Card variant="panel" className="flex flex-col gap-5 p-6 bg-neutral-950 border border-neutral-800">
          <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
            <div className="flex flex-col gap-1.5 max-w-2xl">
              <div className="flex items-center gap-2.5">
                <Typography variant="h1" className="text-lg font-bold font-mono text-neutral-100">
                  {mission.name || mission.title}
                </Typography>
                <Badge variant={statusVariant}>{normStatus}</Badge>
                <Badge variant="cyan">{(mission.priority || 'MEDIUM').toUpperCase()}</Badge>
              </div>

              {mission.goal && (
                <div className="text-xs font-mono text-neutral-300 flex items-center gap-1.5 mt-0.5">
                  <span className="text-neutral-500">OBJECTIVE:</span>
                  <span>{mission.goal}</span>
                </div>
              )}

              {mission.description && (
                <Typography variant="body" className="text-xs text-neutral-400 leading-relaxed mt-1">
                  {mission.description}
                </Typography>
              )}
            </div>

            {/* Lifecycle Action Buttons */}
            <div className="flex items-center gap-2 shrink-0">
              {isDraft && (
                <Button variant="primary" onClick={handleLaunch} isLoading={isActionLoading}>
                  ▶ Launch Mission
                </Button>
              )}
              {(isRunning || isQueued || isPlanning) && (
                <Button variant="ghost" onClick={handlePause} isLoading={isActionLoading}>
                  ⏸ Pause
                </Button>
              )}
              {isPaused && (
                <Button variant="primary" onClick={handleResume} isLoading={isActionLoading}>
                  ▶ Resume Execution
                </Button>
              )}
              {!isCompleted && !isCancelled && !isFailed && (
                <Button variant="ghost" onClick={handleCancel} isLoading={isActionLoading}>
                  ✕ Cancel
                </Button>
              )}
              <Button variant="ghost" onClick={() => setIsEditing(true)}>
                ✎ Edit
              </Button>
            </div>
          </div>

          {/* Progress Bar & Telemetry */}
          <div className="flex flex-col gap-2 pt-2 border-t border-neutral-900">
            <div className="flex items-center justify-between text-xs font-mono text-neutral-400">
              <span>EXECUTION PROGRESS</span>
              <span>{Math.round(progress)}% {mission.current_step ? `(Step ${mission.current_step} of ${steps.length})` : ''}</span>
            </div>
            <div className="w-full h-1.5 bg-neutral-900 rounded overflow-hidden">
              <div
                className={`h-full transition-all duration-300 ${
                  isCompleted ? 'bg-cyan-500' : isFailed ? 'bg-rose-500' : 'bg-emerald-500'
                }`}
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>

          {/* Technical Metadata Bar */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs font-mono text-neutral-400 pt-2 border-t border-neutral-900">
            <div>
              <span className="text-neutral-500 block text-[10px]">AGENT</span>
              <span className="text-neutral-200">{mission.agent_id || mission.agentId || 'Executive Core'}</span>
            </div>
            <div>
              <span className="text-neutral-500 block text-[10px]">MODEL</span>
              <span className="text-neutral-200">{mission.model || 'openrouter/free'}</span>
            </div>
            <div>
              <span className="text-neutral-500 block text-[10px]">TOKEN USAGE</span>
              <span className="text-neutral-200">{tokens.toLocaleString()} tok ({inTokens} in / {outTokens} out)</span>
            </div>
            <div>
              <span className="text-neutral-500 block text-[10px]">TOTAL COST</span>
              <span className="text-emerald-400 font-semibold">${cost.toFixed(6)}</span>
            </div>
          </div>
        </Card>

        {/* Failure Box if failed */}
        {isFailed && mission.error && (
          <Card variant="panel" className="p-4 bg-rose-950/20 border border-rose-900/60 font-mono text-xs space-y-1">
            <div className="text-rose-400 font-semibold uppercase flex items-center gap-2">
              <span>✕ MISSION EXECUTION FAILED</span>
            </div>
            <pre className="text-rose-300 whitespace-pre-wrap leading-relaxed">
              {typeof mission.error === 'object' ? JSON.stringify(mission.error, null, 2) : String(mission.error)}
            </pre>
          </Card>
        )}

        {/* Result & Deliverables Box if completed */}
        {isCompleted && mission.result && (
          <Card variant="panel" className="p-5 bg-neutral-950 border border-cyan-900/40 font-mono text-xs space-y-3">
            <div className="text-cyan-400 font-semibold uppercase flex items-center gap-2">
              <span>✓ EXECUTION ARTIFACTS & DELIVERABLES</span>
            </div>
            <pre className="text-neutral-300 whitespace-pre-wrap leading-relaxed bg-neutral-900/80 p-3 rounded border border-neutral-800">
              {typeof mission.result === 'object' ? JSON.stringify(mission.result, null, 2) : String(mission.result)}
            </pre>
          </Card>
        )}

        {/* Steps List */}
        <MissionStepsList steps={steps} />

        {/* Live Append-Only Event Timeline */}
        <ActivityTimeline activities={mission.activities || []} events={events} />

        {/* Edit Dialog */}
        <Dialog
          isOpen={isEditing}
          onClose={() => setIsEditing(false)}
          title="Edit Mission Directives"
          description="Update mission goals and parameters. Changes apply to subsequent steps."
        >
          <form onSubmit={handleSaveEdit} className="flex flex-col gap-4 mt-2">
            <Input
              label="Mission Name"
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              required
            />

            <Input
              label="Goal / Objective"
              value={editGoal}
              onChange={(e) => setEditGoal(e.target.value)}
            />

            <Textarea
              label="Description & Guidance"
              value={editDescription}
              onChange={(e) => setEditDescription(e.target.value)}
              rows={4}
            />

            <Select
              label="Priority Level"
              value={editPriority}
              onChange={(e) => setEditPriority(e.target.value)}
              options={[
                { label: 'Low Priority', value: 'low' },
                { label: 'Medium Priority', value: 'medium' },
                { label: 'High Priority', value: 'high' },
                { label: 'Critical Priority', value: 'critical' },
              ]}
            />

            <div className="flex items-center justify-end gap-2 pt-3 border-t border-neutral-800">
              <Button type="button" variant="ghost" onClick={() => setIsEditing(false)}>
                Cancel
              </Button>
              <Button type="submit" variant="primary" isLoading={isSubmitting}>
                Save Changes
              </Button>
            </div>
          </form>
        </Dialog>
      </div>
    </AppShell>
  );
}
