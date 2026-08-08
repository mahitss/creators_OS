'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { AppShell } from '../../components/shell/AppShell';
import {
  fetchMemories,
  fetchMemoryCandidates,
  approveMemoryCandidate,
  rejectMemoryCandidate,
  archiveMemory,
  restoreMemory,
  deleteMemory,
  Memory,
  MemoryCandidate,
} from '../../lib/api/memories';
import { MemoryCard } from '../../components/memory/MemoryCard';
import { CandidateApprovalBanner } from '../../components/memory/CandidateApprovalBanner';
import { AddMemoryDialog } from '../../components/memory/AddMemoryDialog';
import { Typography, Button, Tabs, Input, EmptyState, Spinner, ErrorState } from '@vapor/ui';

export default function MemoryPage() {
  const [memories, setMemories] = useState<Memory[]>([]);
  const [candidates, setCandidates] = useState<MemoryCandidate[]>([]);
  const [activeType, setActiveType] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);
  const [isAddOpen, setIsAddOpen] = useState(false);

  const loadMemoryWorkspace = useCallback(async () => {
    setIsLoading(true);
    setIsError(false);
    try {
      const [memData, candData] = await Promise.all([
        fetchMemories({ type: activeType, search: searchQuery }),
        fetchMemoryCandidates(),
      ]);
      setMemories(memData.memories);
      setCandidates(candData.candidates);
    } catch (err) {
      console.error('Failed to load memory workspace:', err);
      setIsError(true);
    } finally {
      setIsLoading(false);
    }
  }, [activeType, searchQuery]);

  useEffect(() => {
    loadMemoryWorkspace();
  }, [loadMemoryWorkspace]);

  const handleApproveCandidate = async (id: string) => {
    try {
      await approveMemoryCandidate(id);
      await loadMemoryWorkspace();
    } catch (err) {
      console.error('Failed to approve candidate:', err);
    }
  };

  const handleRejectCandidate = async (id: string) => {
    try {
      await rejectMemoryCandidate(id);
      await loadMemoryWorkspace();
    } catch (err) {
      console.error('Failed to reject candidate:', err);
    }
  };

  const handleArchiveToggle = async (id: string, isArchived: boolean) => {
    try {
      if (isArchived) await restoreMemory(id);
      else await archiveMemory(id);
      await loadMemoryWorkspace();
    } catch (err) {
      console.error('Failed to toggle archive:', err);
    }
  };

  const handleDeleteMemory = async (id: string) => {
    try {
      await deleteMemory(id);
      await loadMemoryWorkspace();
    } catch (err) {
      console.error('Failed to delete memory:', err);
    }
  };

  const typeTabs = [
    { id: 'all', label: 'All Context' },
    { id: 'preference', label: 'Preferences' },
    { id: 'fact', label: 'Facts' },
    { id: 'decision', label: 'Decisions' },
    { id: 'goal', label: 'Goals' },
    { id: 'insight', label: 'Insights' },
    { id: 'lesson', label: 'Lessons' },
  ];

  return (
    <AppShell>
      <div className="max-w-4xl mx-auto w-full flex flex-col gap-6 py-2">
        {/* Header Bar */}
        <div className="flex items-center justify-between">
          <div className="flex flex-col gap-0.5">
            <Typography variant="h1">Context Vault Memory</Typography>
            <Typography variant="caption" className="text-slate-400">
              Workspace preferences, facts, and lessons learned across mission executions.
            </Typography>
          </div>
          <Button variant="primary" onClick={() => setIsAddOpen(true)}>
            + Add Memory
          </Button>
        </div>

        {/* Candidate Review Banner */}
        <CandidateApprovalBanner
          candidates={candidates}
          onApprove={handleApproveCandidate}
          onReject={handleRejectCandidate}
        />

        {/* Search & Tabs Filter */}
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 pb-2 border-b border-slate-800/80">
          <Tabs tabs={typeTabs} activeTabId={activeType} onChange={setActiveType} />
          <div className="w-full sm:w-60">
            <Input
              placeholder="Search memories..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
        </div>

        {/* Content View */}
        {isLoading ? (
          <div className="flex flex-col items-center justify-center p-12 gap-3">
            <Spinner size="md" />
            <Typography variant="caption" className="text-slate-500 font-mono">
              Loading workspace context memory...
            </Typography>
          </div>
        ) : isError ? (
          <ErrorState
            title="Memory Error"
            message="Could not load memory records for active workspace."
            onRetry={loadMemoryWorkspace}
          />
        ) : memories.length === 0 ? (
          <div className="py-8">
            <EmptyState
              title="Vapor hasn't learned anything about this workspace yet."
              description="Useful preferences, decisions and insights can be saved here as you work."
              icon={<span className="text-2xl">🧠</span>}
              action={
                <Button variant="primary" size="sm" onClick={() => setIsAddOpen(true)}>
                  + Add Memory
                </Button>
              }
            />
          </div>
        ) : (
          <div className="flex flex-col gap-3">
            {memories.map((mem) => (
              <MemoryCard
                key={mem.id}
                memory={mem}
                onArchiveToggle={handleArchiveToggle}
                onDelete={handleDeleteMemory}
              />
            ))}
          </div>
        )}

        {/* Add Memory Dialog */}
        <AddMemoryDialog
          isOpen={isAddOpen}
          onClose={() => setIsAddOpen(false)}
          onSuccess={() => loadMemoryWorkspace()}
        />
      </div>
    </AppShell>
  );
}
