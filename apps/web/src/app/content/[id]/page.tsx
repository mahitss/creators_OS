'use client';

import React, { useState, useEffect, useCallback } from 'react';
import Link from 'next/link';
import { useParams, useRouter } from 'next/navigation';
import { AppShell } from '../../../components/shell/AppShell';
import {
  getContentItem,
  updateContentItem,
  approveContentItem,
  archiveContentItem,
  generateContentAI,
  Content,
} from '../../../lib/api/content';
import { AIGenerationPanel } from '../../../components/content/AIGenerationPanel';
import { Typography, Card, Badge, Button, Spinner, ErrorState, Input, Textarea, Select } from '@vapor/ui';
import { formatDate } from '@vapor/utils';

export default function ContentDetailPage() {
  const params = useParams();
  const router = useRouter();
  const contentId = params.id as string;

  const [item, setItem] = useState<Content | null>(null);
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [type, setType] = useState<any>('article');
  const [status, setStatus] = useState<any>('draft');

  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);
  const [saveState, setSaveState] = useState<'saved' | 'saving' | 'failed'>('saved');
  const [isGenerating, setIsGenerating] = useState(false);
  const [aiError, setAiError] = useState('');

  const loadContentDetail = useCallback(async () => {
    setIsLoading(true);
    setIsError(false);
    try {
      const res = await getContentItem(contentId);
      setItem(res);
      setTitle(res.title);
      setContent(res.content);
      setType(res.type);
      setStatus(res.status);
    } catch (err) {
      console.error('Failed to load content detail:', err);
      setIsError(true);
    } finally {
      setIsLoading(false);
    }
  }, [contentId]);

  useEffect(() => {
    if (contentId) loadContentDetail();
  }, [contentId, loadContentDetail]);

  const handleSave = async () => {
    if (!item) return;
    setSaveState('saving');
    try {
      const updated = await updateContentItem(item.id, {
        title: title.trim(),
        type,
        status,
        content,
      });
      setItem(updated);
      setSaveState('saved');
    } catch (err) {
      console.error('Failed to save content:', err);
      setSaveState('failed');
    }
  };

  const handleApprove = async () => {
    if (!item) return;
    try {
      const updated = await approveContentItem(item.id);
      setItem(updated);
      setStatus(updated.status);
    } catch (err) {
      console.error('Failed to approve content:', err);
    }
  };

  const handleArchive = async () => {
    if (!item) return;
    try {
      const updated = await archiveContentItem(item.id);
      setItem(updated);
      setStatus(updated.status);
    } catch (err) {
      console.error('Failed to archive content:', err);
    }
  };

  const handleAIGenerate = async (intent: 'draft' | 'rewrite' | 'expand' | 'summarize' | 'improve') => {
    if (!item) return;
    setIsGenerating(true);
    setAiError('');
    try {
      const updated = await generateContentAI(item.id, intent);
      setItem(updated);
      setContent(updated.content);
      setSaveState('saved');
    } catch (err: any) {
      setAiError(err?.message || 'AI generation failed. Your existing text was preserved.');
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <AppShell>
      <div className="max-w-4xl mx-auto w-full flex flex-col gap-6 py-2">
        <Link href="/content" className="inline-flex items-center gap-1 text-xs text-slate-400 hover:text-emerald-400 transition-colors">
          ← Back to Studio Content Canvas
        </Link>

        {isLoading ? (
          <div className="flex flex-col items-center justify-center p-12 gap-3">
            <Spinner size="md" />
            <Typography variant="caption" className="text-slate-500 font-mono">
              Opening deliverable editor...
            </Typography>
          </div>
        ) : isError || !item ? (
          <ErrorState
            title="Deliverable Not Found"
            message="The requested deliverable could not be found or belongs to another workspace."
            onRetry={loadContentDetail}
          />
        ) : (
          <div className="flex flex-col gap-6">
            {/* Header Control Panel */}
            <Card variant="panel" className="flex flex-col gap-4 p-5 border-slate-800/80">
              <div className="flex items-start justify-between gap-4">
                <div className="flex flex-col gap-2 w-full">
                  <div className="flex items-center gap-2">
                    <Badge variant="cyan">{type.toUpperCase()}</Badge>
                    <Badge variant={status === 'approved' ? 'emerald' : status === 'archived' ? 'amber' : 'default'}>
                      {status.toUpperCase()}
                    </Badge>
                    <Typography variant="caption" className="text-xs font-mono text-slate-400 ml-auto">
                      {saveState === 'saving' ? 'Saving...' : saveState === 'failed' ? '⚠️ Save Failed' : '✓ Saved'}
                    </Typography>
                  </div>
                  <Input
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    className="text-lg font-bold bg-transparent border-slate-800"
                    placeholder="Deliverable Title..."
                  />
                </div>

                <div className="flex items-center gap-2 shrink-0 pt-6">
                  <Button variant="ghost" size="sm" onClick={handleSave} disabled={saveState === 'saving'}>
                    Save
                  </Button>
                  {status !== 'approved' && status !== 'archived' && (
                    <Button variant="primary" size="sm" onClick={handleApprove}>
                      ✓ Approve
                    </Button>
                  )}
                  {status !== 'archived' && (
                    <Button variant="ghost" size="sm" onClick={handleArchive}>
                      Archive
                    </Button>
                  )}
                </div>
              </div>

              {/* Linked Mission Context Reference */}
              {item.mission_id && (
                <div className="flex items-center justify-between p-3 rounded bg-slate-900/60 border border-slate-800/80 text-xs">
                  <div className="flex items-center gap-2 text-slate-300">
                    <span className="text-emerald-400">⚡ Linked Mission:</span>
                    <span className="font-semibold">{item.mission_title || item.mission_id}</span>
                  </div>
                  <Link href={`/missions/${item.mission_id}`} className="text-emerald-400 hover:underline">
                    Open Mission →
                  </Link>
                </div>
              )}
            </Card>

            {/* AI Generation Studio Panel */}
            <AIGenerationPanel
              onGenerate={handleAIGenerate}
              isGenerating={isGenerating}
            />

            {aiError && (
              <div className="p-3 rounded bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs font-semibold">
                {aiError}
              </div>
            )}

            {/* Main Text Content Editor */}
            <Card variant="panel" className="flex flex-col gap-2 p-5 border-slate-800/80">
              <Typography variant="caption" className="text-xs font-mono text-slate-400 uppercase tracking-wider">
                Deliverable Content (Markdown / Plain Text)
              </Typography>
              <Textarea
                value={content}
                onChange={(e) => {
                  setContent(e.target.value);
                  setSaveState('saving');
                }}
                rows={18}
                placeholder="Write or generate content here..."
                className="font-mono text-sm leading-relaxed border-slate-800/80 bg-slate-950/40"
              />
            </Card>
          </div>
        )}
      </div>
    </AppShell>
  );
}
