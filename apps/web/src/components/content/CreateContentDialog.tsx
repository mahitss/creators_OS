import React, { useState, useEffect } from 'react';
import { Dialog, Input, Textarea, Select, Button } from '@vapor/ui';
import { createContentItem, Content } from '../../lib/api/content';
import { fetchMissions, Mission } from '../../lib/api/missions';

export interface CreateContentDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: (newContent: Content) => void;
}

export const CreateContentDialog: React.FC<CreateContentDialogProps> = ({
  isOpen,
  onClose,
  onSuccess,
}) => {
  const [title, setTitle] = useState('');
  const [type, setType] = useState<any>('article');
  const [content, setContent] = useState('');
  const [missionId, setMissionId] = useState<string>('');
  const [missions, setMissions] = useState<Mission[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (isOpen) {
      fetchMissions()
        .then((res) => setMissions(res.missions))
        .catch(() => setMissions([]));
    }
  }, [isOpen]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) {
      setError('Deliverable title is required.');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const cnt = await createContentItem({
        title: title.trim(),
        type,
        content: content.trim(),
        mission_id: missionId || undefined,
      });
      setTitle('');
      setContent('');
      setType('article');
      setMissionId('');
      onSuccess(cnt);
      onClose();
    } catch (err: any) {
      setError(err?.message || 'Failed to create deliverable.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Dialog isOpen={isOpen} onClose={onClose} title="Create Content Deliverable" description="Create a structured deliverable for articles, scripts, social posts, emails, or reports.">
      <form onSubmit={handleSubmit} className="flex flex-col gap-4 mt-2">
        <Input
          label="Deliverable Title"
          placeholder="e.g. Comprehensive Docker Video Script"
          value={title}
          onChange={(e) => {
            setTitle(e.target.value);
            if (error) setError('');
          }}
          error={error}
          autoFocus
          required
        />

        <Select
          label="Deliverable Type"
          value={type}
          onChange={(e) => setType(e.target.value as any)}
          options={[
            { label: 'Article (Blog or Documentation)', value: 'article' },
            { label: 'Script (Video or Audio)', value: 'script' },
            { label: 'Social Post (Short-form)', value: 'social_post' },
            { label: 'Email (Newsletter or Update)', value: 'email' },
            { label: 'Report (Analysis or Summary)', value: 'report' },
            { label: 'Outline (Structured Concept)', value: 'outline' },
          ]}
        />

        {missions.length > 0 && (
          <Select
            label="Associate with Mission (Optional)"
            value={missionId}
            onChange={(e) => setMissionId(e.target.value)}
            options={[
              { label: 'None (Standalone Deliverable)', value: '' },
              ...missions.map((m) => ({ label: m.title, value: m.id })),
            ]}
          />
        )}

        <Textarea
          label="Initial Text Content (Optional)"
          placeholder="Enter draft text or leave blank for AI generation..."
          value={content}
          onChange={(e) => setContent(e.target.value)}
          rows={3}
        />

        <div className="flex items-center justify-end gap-2 pt-3 border-t border-slate-800">
          <Button type="button" variant="ghost" onClick={onClose} disabled={isLoading}>
            Cancel
          </Button>
          <Button type="submit" variant="primary" isLoading={isLoading}>
            Create Deliverable
          </Button>
        </div>
      </form>
    </Dialog>
  );
};
