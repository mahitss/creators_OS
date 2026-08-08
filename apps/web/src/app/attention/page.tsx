'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { AppShell } from '../../components/shell/AppShell';
import {
  fetchAttentionItems,
  resolveAttentionItem,
  dismissAttentionItem,
  snoozeAttentionItem,
  reconcileAttentionItems,
  AttentionItem,
} from '../../lib/api/attention';
import { AttentionItemCard } from '../../components/attention/AttentionItemCard';
import { Typography, Button, Tabs, EmptyState, Spinner, ErrorState } from '@vapor/ui';

export default function AttentionPage() {
  const [items, setItems] = useState<AttentionItem[]>([]);
  const [activeStatus, setActiveStatus] = useState('open');
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);

  const loadAttentionCenter = useCallback(async () => {
    setIsLoading(true);
    setIsError(false);
    try {
      const data = await fetchAttentionItems(activeStatus);
      setItems(data.items);
    } catch (err) {
      console.error('Failed to load attention items:', err);
      setIsError(true);
    } finally {
      setIsLoading(false);
    }
  }, [activeStatus]);

  useEffect(() => {
    loadAttentionCenter();
  }, [loadAttentionCenter]);

  const handleReconcile = async () => {
    try {
      await reconcileAttentionItems();
      await loadAttentionCenter();
    } catch (err) {
      console.error('Failed to reconcile attention:', err);
    }
  };

  const handleResolve = async (id: string) => {
    try {
      await resolveAttentionItem(id);
      await loadAttentionCenter();
    } catch (err) {
      console.error('Failed to resolve attention item:', err);
    }
  };

  const handleSnooze = async (id: string) => {
    try {
      await snoozeAttentionItem(id, 60);
      await loadAttentionCenter();
    } catch (err) {
      console.error('Failed to snooze attention item:', err);
    }
  };

  const handleDismiss = async (id: string) => {
    try {
      await dismissAttentionItem(id);
      await loadAttentionCenter();
    } catch (err) {
      console.error('Failed to dismiss attention item:', err);
    }
  };

  const statusTabs = [
    { id: 'open', label: 'Open Attention' },
    { id: 'snoozed', label: 'Snoozed' },
    { id: 'resolved', label: 'Resolved History' },
  ];

  return (
    <AppShell>
      <div className="max-w-4xl mx-auto w-full flex flex-col gap-6 py-2">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex flex-col gap-0.5">
            <Typography variant="h1">Attention Center</Typography>
            <Typography variant="caption" className="text-slate-400">
              Actionable inbox for workspace decisions, reviews, and execution failures requiring user handling.
            </Typography>
          </div>
          <Button variant="ghost" size="sm" onClick={handleReconcile}>
            🔄 Reconcile
          </Button>
        </div>

        {/* Status Tabs */}
        <div className="pb-2 border-b border-slate-800/80">
          <Tabs tabs={statusTabs} activeTabId={activeStatus} onChange={setActiveStatus} />
        </div>

        {/* Content View */}
        {isLoading ? (
          <div className="flex flex-col items-center justify-center p-12 gap-3">
            <Spinner size="md" />
            <Typography variant="caption" className="text-slate-500 font-mono">
              Loading attention inbox...
            </Typography>
          </div>
        ) : isError ? (
          <ErrorState
            title="Attention Inbox Error"
            message="Could not load attention items for active workspace."
            onRetry={loadAttentionCenter}
          />
        ) : items.length === 0 ? (
          <div className="py-8">
            <EmptyState
              title="You're all caught up."
              description="No open attention items requiring user decision or review."
              icon={<span className="text-2xl">🔔</span>}
            />
          </div>
        ) : (
          <div className="flex flex-col gap-3">
            {items.map((item) => (
              <AttentionItemCard
                key={item.id}
                item={item}
                onResolve={handleResolve}
                onSnooze={handleSnooze}
                onDismiss={handleDismiss}
              />
            ))}
          </div>
        )}
      </div>
    </AppShell>
  );
}
