'use client';

import React, { useState, useEffect, useCallback } from 'react';
import Link from 'next/link';
import { AppShell } from '../../components/shell/AppShell';
import {
  fetchGmailStatus,
  fetchGmailThreads,
  syncGmail,
  GmailThread,
  GmailStatusResponse,
} from '../../lib/api/gmail';
import { Typography, Card, Badge, Button, Tabs, EmptyState, Spinner, ErrorState } from '@vapor/ui';
import { formatDate } from '@vapor/utils';

export default function GmailTriagePage() {
  const [threads, setThreads] = useState<GmailThread[]>([]);
  const [statusInfo, setStatusInfo] = useState<GmailStatusResponse | null>(null);
  const [activeFilter, setActiveFilter] = useState('all');
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);

  const loadTriageData = useCallback(async () => {
    setIsLoading(true);
    setIsError(false);
    try {
      const st = await fetchGmailStatus();
      setStatusInfo(st);

      if (st.is_connected) {
        const res = await fetchGmailThreads(activeFilter);
        setThreads(res.threads);
      }
    } catch (err) {
      console.error('Failed to load Gmail triage data:', err);
      setIsError(true);
    } finally {
      setIsLoading(false);
    }
  }, [activeFilter]);

  useEffect(() => {
    loadTriageData();
  }, [loadTriageData]);

  const handleSync = async () => {
    try {
      await syncGmail();
      await loadTriageData();
    } catch (err) {
      console.error('Failed to sync Gmail:', err);
    }
  };

  const filterTabs = [
    { id: 'all', label: 'All Threads' },
    { id: 'needs_response', label: 'Needs Response' },
    { id: 'unread', label: 'Unread' },
  ];

  return (
    <AppShell>
      <div className="max-w-4xl mx-auto w-full flex flex-col gap-6 py-2">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex flex-col gap-0.5">
            <Typography variant="h1">Email Triage</Typography>
            <Typography variant="caption" className="text-slate-400">
              Read-only email classification and grounded summarization for workspace commitments.
            </Typography>
          </div>
          {statusInfo?.is_connected && (
            <Button variant="ghost" size="sm" onClick={handleSync}>
              🔄 Sync Gmail
            </Button>
          )}
        </div>

        {/* Filter Tabs */}
        {statusInfo?.is_connected && (
          <div className="pb-2 border-b border-slate-800/80">
            <Tabs tabs={filterTabs} activeTabId={activeFilter} onChange={setActiveFilter} />
          </div>
        )}

        {/* Content View */}
        {isLoading ? (
          <div className="flex flex-col items-center justify-center p-12 gap-3">
            <Spinner size="md" />
            <Typography variant="caption" className="text-slate-500 font-mono">
              Loading email triage threads...
            </Typography>
          </div>
        ) : isError ? (
          <ErrorState
            title="Email Triage Error"
            message="Could not load Gmail threads for active workspace."
            onRetry={loadTriageData}
          />
        ) : !statusInfo?.is_connected ? (
          <EmptyState
            title="Gmail Is Not Connected"
            description="Connect Google Workspace in Settings to enable read-only email triage."
            icon={<span className="text-2xl">✉️</span>}
            actionLabel="Open Settings"
            onAction={() => (window.location.href = '/settings/integrations')}
          />
        ) : threads.length === 0 ? (
          <div className="py-8">
            <EmptyState
              title="No Email Threads Found"
              description="No recent email threads matching active filter."
              icon={<span className="text-2xl">📬</span>}
            />
          </div>
        ) : (
          <div className="flex flex-col gap-3">
            {threads.map((t) => (
              <Card
                key={t.id}
                variant="panel"
                className="flex flex-col gap-2 p-4 border-slate-800/80 hover:border-slate-700 transition-all cursor-pointer"
                onClick={() => (window.location.href = `/gmail/msg_01_ws_default_01`)}
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="flex flex-col gap-1">
                    <div className="flex items-center gap-2">
                      <Badge variant="amber">NEEDS RESPONSE</Badge>
                      <Typography variant="h3" className="text-sm font-semibold text-slate-100">
                        {t.subject}
                      </Typography>
                    </div>
                    <Typography variant="body" className="text-xs text-slate-300 line-clamp-1">
                      {t.snippet}
                    </Typography>
                  </div>
                  <span className="text-[11px] font-mono text-slate-500 shrink-0">
                    {formatDate(t.last_message_at)}
                  </span>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>
    </AppShell>
  );
}
