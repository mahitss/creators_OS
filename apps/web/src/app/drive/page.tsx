'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { AppShell } from '../../components/shell/AppShell';
import {
  fetchDriveStatus,
  fetchDriveFiles,
  syncDrive,
  DriveFile,
  DriveStatusResponse,
} from '../../lib/api/drive';
import { Typography, Card, Badge, Button, Input, EmptyState, Spinner, ErrorState } from '@vapor/ui';
import { formatDate, formatBytes } from '@vapor/utils';

export default function DriveBrowserPage() {
  const [files, setFiles] = useState<DriveFile[]>([]);
  const [statusInfo, setStatusInfo] = useState<DriveStatusResponse | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);

  const loadDriveData = useCallback(async () => {
    setIsLoading(true);
    setIsError(false);
    try {
      const st = await fetchDriveStatus();
      setStatusInfo(st);

      if (st.is_connected) {
        const res = await fetchDriveFiles(searchQuery);
        setFiles(res.files);
      }
    } catch (err) {
      console.error('Failed to load Drive data:', err);
      setIsError(true);
    } finally {
      setIsLoading(false);
    }
  }, [searchQuery]);

  useEffect(() => {
    loadDriveData();
  }, [loadDriveData]);

  const handleSync = async () => {
    try {
      await syncDrive();
      await loadDriveData();
    } catch (err) {
      console.error('Failed to sync Drive:', err);
    }
  };

  const getMimeBadge = (mime: string) => {
    if (mime.includes('document')) return <Badge variant="emerald">Google Doc</Badge>;
    if (mime.includes('pdf')) return <Badge variant="amber">PDF</Badge>;
    if (mime.includes('markdown') || mime.includes('plain')) return <Badge variant="cyan">Text</Badge>;
    return <Badge variant="default">Binary</Badge>;
  };

  return (
    <AppShell>
      <div className="max-w-4xl mx-auto w-full flex flex-col gap-6 py-2">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex flex-col gap-0.5">
            <Typography variant="h1">Document Context Browser</Typography>
            <Typography variant="caption" className="text-slate-400">
              Discover and select read-only Google Drive files to attach as context for Missions.
            </Typography>
          </div>
          {statusInfo?.is_connected && (
            <Button variant="ghost" size="sm" onClick={handleSync}>
              🔄 Sync Drive
            </Button>
          )}
        </div>

        {/* Search Input */}
        {statusInfo?.is_connected && (
          <div className="w-full max-w-md">
            <Input
              type="text"
              placeholder="Search document name or description..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
        )}

        {/* Content View */}
        {isLoading ? (
          <div className="flex flex-col items-center justify-center p-12 gap-3">
            <Spinner size="md" />
            <Typography variant="caption" className="text-slate-500 font-mono">
              Loading Google Drive document metadata...
            </Typography>
          </div>
        ) : isError ? (
          <ErrorState
            title="Drive Browser Error"
            message="Could not load Google Drive files for active workspace."
            onRetry={loadDriveData}
          />
        ) : !statusInfo?.is_connected ? (
          <EmptyState
            title="Google Drive Is Not Connected"
            description="Connect Google Workspace in Settings to enable document context integration."
            icon={<span className="text-2xl">📄</span>}
            actionLabel="Open Settings"
            onAction={() => (window.location.href = '/settings/integrations')}
          />
        ) : files.length === 0 ? (
          <div className="py-8">
            <EmptyState
              title="No Drive Documents Found"
              description="No recent documents matching search query."
              icon={<span className="text-2xl">📂</span>}
            />
          </div>
        ) : (
          <div className="flex flex-col gap-3">
            {files.map((f) => (
              <Card
                key={f.id}
                variant="panel"
                className="flex items-center justify-between p-4 border-slate-800/80 hover:border-slate-700 transition-all"
              >
                <div className="flex items-start gap-3">
                  <span className="text-xl pt-0.5">📄</span>
                  <div className="flex flex-col gap-1">
                    <div className="flex items-center gap-2">
                      {getMimeBadge(f.mime_type)}
                      <Typography variant="h3" className="text-sm font-semibold text-slate-100">
                        {f.name}
                      </Typography>
                    </div>
                    <Typography variant="body" className="text-xs text-slate-400">
                      {f.description || 'No description provided.'}
                    </Typography>
                    <div className="flex items-center gap-3 text-[11px] text-slate-500 font-mono">
                      <span>Owner: {f.owner_name}</span>
                      <span>Size: {formatBytes(f.size_bytes)}</span>
                      <span>Modified: {formatDate(f.modified_time)}</span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <a
                    href={f.web_url}
                    target="_blank"
                    rel="noreferrer"
                    className="px-3 py-1.5 rounded text-xs font-mono bg-slate-900 border border-slate-800 text-slate-300 hover:text-slate-100 transition-colors"
                  >
                    Open ↗
                  </a>
                  <Button variant="primary" size="sm" onClick={() => alert(`Document '${f.name}' selected for Mission context.`)}>
                    Attach to Mission
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>
    </AppShell>
  );
}
