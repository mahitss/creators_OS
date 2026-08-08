'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { AppShell } from '../../components/shell/AppShell';
import { fetchMissions, Mission } from '../../lib/api/missions';
import { MissionCard } from '../../components/missions/MissionCard';
import { MissionFilterBar } from '../../components/missions/MissionFilterBar';
import { CreateMissionDialog } from '../../components/missions/CreateMissionDialog';
import { Typography, Button, EmptyState, Spinner, ErrorState } from '@vapor/ui';

export default function MissionsPage() {
  const [missions, setMissions] = useState<Mission[]>([]);
  const [statusFilter, setStatusFilter] = useState('active');
  const [priorityFilter, setPriorityFilter] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);
  const [isCreateOpen, setIsCreateOpen] = useState(false);

  const loadMissions = useCallback(async () => {
    setIsLoading(true);
    setIsError(false);
    try {
      const res = await fetchMissions({
        status: statusFilter,
        priority: priorityFilter,
        search: searchQuery,
      });
      setMissions(res.missions);
    } catch (err) {
      console.error('Failed to load missions:', err);
      setIsError(true);
    } finally {
      setIsLoading(false);
    }
  }, [statusFilter, priorityFilter, searchQuery]);

  useEffect(() => {
    loadMissions();
  }, [loadMissions]);

  const handleMissionUpdate = (updated: Mission) => {
    setMissions((prev) =>
      prev.map((m) => (m.id === updated.id ? updated : m))
    );
  };

  return (
    <AppShell>
      <div className="max-w-4xl mx-auto w-full flex flex-col gap-6 py-2">
        {/* Header Bar */}
        <div className="flex items-center justify-between">
          <div className="flex flex-col gap-0.5">
            <Typography variant="h1">Missions</Typography>
            <Typography variant="caption" className="text-slate-400">
              Work items defined for Executive background observation and execution.
            </Typography>
          </div>
          <Button variant="primary" onClick={() => setIsCreateOpen(true)}>
            + Create Mission
          </Button>
        </div>

        {/* Filter Bar */}
        <MissionFilterBar
          activeStatus={statusFilter}
          onStatusChange={setStatusFilter}
          activePriority={priorityFilter}
          onPriorityChange={setPriorityFilter}
          searchQuery={searchQuery}
          onSearchChange={setSearchQuery}
        />

        {/* Content View */}
        {isLoading ? (
          <div className="flex flex-col items-center justify-center p-12 gap-3">
            <Spinner size="md" />
            <Typography variant="caption" className="text-slate-500 font-mono">
              Loading workspace missions...
            </Typography>
          </div>
        ) : isError ? (
          <ErrorState
            title="Missions Error"
            message="Could not retrieve missions for active workspace."
            onRetry={loadMissions}
          />
        ) : missions.length === 0 ? (
          <div className="py-8">
            <EmptyState
              title="No missions yet."
              description="Create your first mission and give Vapor something meaningful to work on."
              icon={<span className="text-2xl">⚡</span>}
              action={
                <Button variant="primary" size="sm" onClick={() => setIsCreateOpen(true)}>
                  Create Mission
                </Button>
              }
            />
          </div>
        ) : (
          <div className="flex flex-col gap-3">
            {missions.map((mission) => (
              <MissionCard
                key={mission.id}
                mission={mission}
                onMissionUpdate={handleMissionUpdate}
              />
            ))}
          </div>
        )}

        {/* Create Mission Modal */}
        <CreateMissionDialog
          isOpen={isCreateOpen}
          onClose={() => setIsCreateOpen(false)}
          onSuccess={() => {
            loadMissions();
          }}
        />
      </div>
    </AppShell>
  );
}
