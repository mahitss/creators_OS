import React, { useState } from 'react';
import { Dialog, Input, Textarea, Select, Button } from '@vapor/ui';
import { createMission, Mission } from '../../lib/api/missions';

export interface CreateMissionDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: (newMission: Mission) => void;
}

export const CreateMissionDialog: React.FC<CreateMissionDialogProps> = ({
  isOpen,
  onClose,
  onSuccess,
}) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<'low' | 'medium' | 'high' | 'urgent'>('medium');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) {
      setError('Mission title is required.');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const created = await createMission({
        title: title.trim(),
        description: description.trim(),
        priority,
      });
      setTitle('');
      setDescription('');
      setPriority('medium');
      onSuccess(created);
      onClose();
    } catch (err: any) {
      setError(err?.message || 'Failed to create mission.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Dialog isOpen={isOpen} onClose={onClose} title="Create New Mission" description="Define a meaningful piece of work for Vapor to observe and execute.">
      <form onSubmit={handleSubmit} className="flex flex-col gap-4 mt-2">
        <Input
          label="Mission Title"
          placeholder="e.g. Prepare a YouTube video about Docker"
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
          label="Description & Guidance"
          placeholder="Provide key context, requirements, or steps..."
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={3}
        />

        <Select
          label="Priority Level"
          value={priority}
          onChange={(e) => setPriority(e.target.value as any)}
          options={[
            { label: 'Low Priority', value: 'low' },
            { label: 'Medium Priority', value: 'medium' },
            { label: 'High Priority', value: 'high' },
            { label: 'Urgent Priority', value: 'urgent' },
          ]}
        />

        <div className="flex items-center justify-end gap-2 pt-3 border-t border-slate-800">
          <Button type="button" variant="ghost" onClick={onClose} disabled={isLoading}>
            Cancel
          </Button>
          <Button type="submit" variant="primary" isLoading={isLoading}>
            Create Mission
          </Button>
        </div>
      </form>
    </Dialog>
  );
};
