'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { AppShell } from '../../components/shell/AppShell';
import {
  fetchContentItems,
  approveContentItem,
  archiveContentItem,
  Content,
} from '../../lib/api/content';
import { ContentCard } from '../../components/content/ContentCard';
import { CreateContentDialog } from '../../components/content/CreateContentDialog';
import { Typography, Button, Tabs, Input, EmptyState, Spinner, ErrorState } from '@vapor/ui';

export default function ContentPage() {
  const [contentItems, setContentItems] = useState<Content[]>([]);
  const [activeType, setActiveType] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);
  const [isCreateOpen, setIsCreateOpen] = useState(false);

  const loadContentItems = useCallback(async () => {
    setIsLoading(true);
    setIsError(false);
    try {
      const data = await fetchContentItems({ type: activeType, search: searchQuery });
      setContentItems(data.content_items);
    } catch (err) {
      console.error('Failed to load content workspace:', err);
      setIsError(true);
    } finally {
      setIsLoading(false);
    }
  }, [activeType, searchQuery]);

  useEffect(() => {
    loadContentItems();
  }, [loadContentItems]);

  const handleApprove = async (id: string) => {
    try {
      await approveContentItem(id);
      await loadContentItems();
    } catch (err) {
      console.error('Failed to approve deliverable:', err);
    }
  };

  const handleArchive = async (id: string) => {
    try {
      await archiveContentItem(id);
      await loadContentItems();
    } catch (err) {
      console.error('Failed to archive deliverable:', err);
    }
  };

  const typeTabs = [
    { id: 'all', label: 'All Deliverables' },
    { id: 'article', label: 'Articles' },
    { id: 'script', label: 'Scripts' },
    { id: 'social_post', label: 'Social' },
    { id: 'email', label: 'Emails' },
    { id: 'report', label: 'Reports' },
    { id: 'outline', label: 'Outlines' },
  ];

  return (
    <AppShell>
      <div className="max-w-4xl mx-auto w-full flex flex-col gap-6 py-2">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex flex-col gap-0.5">
            <Typography variant="h1">Studio Content Canvas</Typography>
            <Typography variant="caption" className="text-slate-400">
              Transform mission outputs into articles, scripts, social posts, emails, and reports.
            </Typography>
          </div>
          <Button variant="primary" onClick={() => setIsCreateOpen(true)}>
            + Create Content
          </Button>
        </div>

        {/* Search & Tabs Filter */}
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 pb-2 border-b border-slate-800/80">
          <Tabs tabs={typeTabs} activeTabId={activeType} onChange={setActiveType} />
          <div className="w-full sm:w-60">
            <Input
              placeholder="Search deliverables..."
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
              Loading content deliverables...
            </Typography>
          </div>
        ) : isError ? (
          <ErrorState
            title="Content Workspace Error"
            message="Could not load deliverable records for active workspace."
            onRetry={loadContentItems}
          />
        ) : contentItems.length === 0 ? (
          <div className="py-8">
            <EmptyState
              title="Nothing here yet."
              description="Content created from your missions will appear here."
              icon={<span className="text-2xl">🎨</span>}
              action={
                <Button variant="primary" size="sm" onClick={() => setIsCreateOpen(true)}>
                  + Create Content
                </Button>
              }
            />
          </div>
        ) : (
          <div className="flex flex-col gap-3">
            {contentItems.map((item) => (
              <ContentCard
                key={item.id}
                item={item}
                onApprove={handleApprove}
                onArchive={handleArchive}
              />
            ))}
          </div>
        )}

        {/* Create Dialog */}
        <CreateContentDialog
          isOpen={isCreateOpen}
          onClose={() => setIsCreateOpen(false)}
          onSuccess={() => loadContentItems()}
        />
      </div>
    </AppShell>
  );
}
