import React, { useState } from 'react';
import { Dialog, Input, Textarea, Select, Button } from '@vapor/ui';
import { createMemory, Memory } from '../../lib/api/memories';

export interface AddMemoryDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: (newMemory: Memory) => void;
}

export const AddMemoryDialog: React.FC<AddMemoryDialogProps> = ({
  isOpen,
  onClose,
  onSuccess,
}) => {
  const [type, setType] = useState<any>('preference');
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [importance, setImportance] = useState<any>('medium');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim() || !content.trim()) {
      setError('Title and content are required.');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const mem = await createMemory({
        type,
        title: title.trim(),
        content: content.trim(),
        importance,
      });
      setTitle('');
      setContent('');
      setType('preference');
      setImportance('medium');
      onSuccess(mem);
      onClose();
    } catch (err: any) {
      setError(err?.message || 'Failed to save memory.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Dialog isOpen={isOpen} onClose={onClose} title="Save Context Memory" description="Teach Vapor useful preferences, facts, goals, or decisions for future missions.">
      <form onSubmit={handleSubmit} className="flex flex-col gap-4 mt-2">
        <Select
          label="Memory Type"
          value={type}
          onChange={(e) => setType(e.target.value as any)}
          options={[
            { label: 'Preference (How user prefers work done)', value: 'preference' },
            { label: 'Fact (Verified domain knowledge)', value: 'fact' },
            { label: 'Decision (Past user choices)', value: 'decision' },
            { label: 'Goal (Long-term workspace objective)', value: 'goal' },
            { label: 'Insight (Observed pattern)', value: 'insight' },
            { label: 'Lesson (Learned from past attempts)', value: 'lesson' },
            { label: 'Context (Project context)', value: 'context' },
          ]}
        />

        <Input
          label="Memory Title"
          placeholder="e.g. User prefers beginner-friendly Docker explanations"
          value={title}
          onChange={(e) => {
            setTitle(e.target.value);
            if (error) setError('');
          }}
          error={error}
          autoFocus
          required
        />

        <Textarea
          label="Detailed Memory Content"
          placeholder="Explain the preference, fact, or choice in clear detail..."
          value={content}
          onChange={(e) => setContent(e.target.value)}
          rows={3}
          required
        />

        <Select
          label="Importance Weight"
          value={importance}
          onChange={(e) => setImportance(e.target.value as any)}
          options={[
            { label: 'Low Weight', value: 'low' },
            { label: 'Medium Weight', value: 'medium' },
            { label: 'High Weight', value: 'high' },
            { label: 'Critical Weight', value: 'critical' },
          ]}
        />

        <div className="flex items-center justify-end gap-2 pt-3 border-t border-slate-800">
          <Button type="button" variant="ghost" onClick={onClose} disabled={isLoading}>
            Cancel
          </Button>
          <Button type="submit" variant="primary" isLoading={isLoading}>
            Save to Memory
          </Button>
        </div>
      </form>
    </Dialog>
  );
};
