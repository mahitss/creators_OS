'use client';

import React, { useState, useEffect, useCallback } from 'react';
import Link from 'next/link';
import { useParams, useRouter } from 'next/navigation';
import { AppShell } from '../../../components/shell/AppShell';
import { getMemory, updateMemory, archiveMemory, restoreMemory, deleteMemory, Memory } from '../../../lib/api/memories';
import { Typography, Card, Badge, Button, Spinner, ErrorState, Dialog, Input, Textarea, Select } from '@vapor/ui';
import { formatDate } from '@vapor/utils';

export default function MemoryDetailPage() {
  const params = useParams();
  const router = useRouter();
  const memoryId = params.id as string;

  const [memory, setMemory] = useState<Memory | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);
  const [isEditing, setIsEditing] = useState(false);

  // Edit form
  const [editTitle, setEditTitle] = useState('');
  const [editContent, setEditContent] = useState('');
  const [editType, setEditType] = useState<any>('preference');
  const [editImportance, setEditImportance] = useState<any>('medium');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const loadMemoryDetail = useCallback(async () => {
    setIsLoading(true);
    setIsError(false);
    try {
      const res = await getMemory(memoryId);
      setMemory(res);
      setEditTitle(res.title);
      setEditContent(res.content);
      setEditType(res.type);
      setEditImportance(res.importance);
    } catch (err) {
      console.error('Failed to load memory detail:', err);
      setIsError(true);
    } finally {
      setIsLoading(false);
    }
  }, [memoryId]);

  useEffect(() => {
    if (memoryId) loadMemoryDetail();
  }, [memoryId, loadMemoryDetail]);

  const handleArchiveToggle = async () => {
    if (!memory) return;
    try {
      if (memory.is_archived) await restoreMemory(memory.id);
      else await archiveMemory(memory.id);
      await loadMemoryDetail();
    } catch (err) {
      console.error('Failed to toggle archive:', err);
    }
  };

  const handleDelete = async () => {
    if (!memory) return;
    try {
      await deleteMemory(memory.id);
      router.push('/memory');
    } catch (err) {
      console.error('Failed to delete memory:', err);
    }
  };

  const handleEditSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!memory || !editTitle.trim() || !editContent.trim()) return;

    setIsSubmitting(true);
    try {
      const updated = await updateMemory(memory.id, {
        title: editTitle.trim(),
        content: editContent.trim(),
        type: editType,
        importance: editImportance,
      });
      setMemory(updated);
      setIsEditing(false);
    } catch (err) {
      console.error('Failed to update memory:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <AppShell>
      <div className="max-w-4xl mx-auto w-full flex flex-col gap-6 py-2">
        <Link href="/memory" className="inline-flex items-center gap-1 text-xs text-slate-400 hover:text-emerald-400 transition-colors">
          ← Back to Memory Workspace
        </Link>

        {isLoading ? (
          <div className="flex flex-col items-center justify-center p-12 gap-3">
            <Spinner size="md" />
            <Typography variant="caption" className="text-slate-500 font-mono">
              Opening memory record...
            </Typography>
          </div>
        ) : isError || !memory ? (
          <ErrorState
            title="Memory Record Not Found"
            message="The requested memory record could not be found or belongs to another workspace."
            onRetry={loadMemoryDetail}
          />
        ) : (
          <div className="flex flex-col gap-6">
            <Card variant="panel" className="flex flex-col gap-5 p-6 border-slate-800/80">
              <div className="flex items-start justify-between gap-4">
                <div className="flex flex-col gap-2">
                  <div className="flex items-center gap-2">
                    <Badge variant="emerald">{memory.type.toUpperCase()}</Badge>
                    <Badge variant={memory.importance === 'critical' ? 'crimson' : memory.importance === 'high' ? 'amber' : 'default'}>
                      {memory.importance.toUpperCase()} IMPORTANCE
                    </Badge>
                  </div>
                  <Typography variant="h1" className="text-xl sm:text-2xl font-bold text-slate-100">
                    {memory.title}
                  </Typography>
                </div>

                <div className="flex items-center gap-2">
                  <Button variant="ghost" size="sm" onClick={() => setIsEditing(true)}>
                    Edit
                  </Button>
                  <Button variant="ghost" size="sm" onClick={handleArchiveToggle}>
                    {memory.is_archived ? 'Restore' : 'Archive'}
                  </Button>
                  <Button variant="ghost" size="sm" className="text-rose-400 hover:text-rose-300" onClick={handleDelete}>
                    Delete
                  </Button>
                </div>
              </div>

              <div className="p-4 rounded bg-slate-900/60 border border-slate-800">
                <Typography variant="body" className="text-slate-200 whitespace-pre-wrap leading-relaxed">
                  {memory.content}
                </Typography>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2 border-t border-slate-800 text-[11px] font-mono text-slate-500">
                <div>
                  <span className="block text-slate-400 font-semibold">Source Type</span>
                  <span>{memory.source_type}</span>
                </div>
                <div>
                  <span className="block text-slate-400 font-semibold">Created At</span>
                  <span>{formatDate(memory.created_at)}</span>
                </div>
                <div>
                  <span className="block text-slate-400 font-semibold">Updated At</span>
                  <span>{formatDate(memory.updated_at)}</span>
                </div>
                <div>
                  <span className="block text-slate-400 font-semibold">Last Accessed</span>
                  <span>{formatDate(memory.last_accessed_at)}</span>
                </div>
              </div>
            </Card>
          </div>
        )}

        {/* Edit Dialog */}
        {memory && (
          <Dialog isOpen={isEditing} onClose={() => setIsEditing(false)} title="Edit Memory Record">
            <form onSubmit={handleEditSubmit} className="flex flex-col gap-4 mt-2">
              <Select
                label="Memory Type"
                value={editType}
                onChange={(e) => setEditType(e.target.value as any)}
                options={[
                  { label: 'Preference', value: 'preference' },
                  { label: 'Fact', value: 'fact' },
                  { label: 'Decision', value: 'decision' },
                  { label: 'Goal', value: 'goal' },
                  { label: 'Insight', value: 'insight' },
                  { label: 'Lesson', value: 'lesson' },
                  { label: 'Context', value: 'context' },
                ]}
              />
              <Input
                label="Title"
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
                required
              />
              <Textarea
                label="Content"
                value={editContent}
                onChange={(e) => setEditContent(e.target.value)}
                rows={4}
                required
              />
              <Select
                label="Importance"
                value={editImportance}
                onChange={(e) => setEditImportance(e.target.value as any)}
                options={[
                  { label: 'Low', value: 'low' },
                  { label: 'Medium', value: 'medium' },
                  { label: 'High', value: 'high' },
                  { label: 'Critical', value: 'critical' },
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
