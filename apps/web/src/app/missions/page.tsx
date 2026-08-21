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
  const [statusFilter, setStatusFilter] = useState('all');
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
      <div className="max-w-5xl mx-auto w-full flex flex-col gap-6 py-4">
        {/* Header Bar */}
        <div className="flex items-center justify-between">
          <div className="flex flex-col gap-0.5">
            <Typography variant="h1" className="text-xl font-bold font-mono tracking-tight text-neutral-100">
              Missions
            </Typography>
            <Typography variant="caption" className="text-neutral-400 font-mono text-xs">
              Executive AI operating system mission execution engine and runtime.
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
          <div className="flex flex-col items-center justify-center p-16 gap-3">
            <Spinner size="md" />
            <Typography variant="caption" className="text-neutral-500 font-mono text-xs">
              Streaming workspace missions ledger...
            </Typography>
          </div>
        ) : isError ? (
          <ErrorState
            title="Missions Stream Offline"
            message="Could not retrieve missions for active workspace."
            onRetry={loadMissions}
          />
        ) : missions.length === 0 ? (
          <div className="py-12">
            <EmptyState
              title="No missions yet."
              description="Create your first autonomous mission to begin planning and execution."
              icon={<span className="text-2xl font-mono">⚡</span>}
              action={
                <Button variant="primary" size="sm" onClick={() => setIsCreateOpen(true)}>
                  + Create Mission
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
