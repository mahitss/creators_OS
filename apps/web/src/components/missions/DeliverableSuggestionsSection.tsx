import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Card, Typography, Button, Badge } from '@vapor/ui';
import {
  DeliverableSuggestion,
  acceptDeliverableSuggestion,
  dismissDeliverableSuggestion,
} from '../../lib/api/deliverables';

export interface DeliverableSuggestionsSectionProps {
  suggestions: DeliverableSuggestion[];
  onRefresh: () => void;
}

export const DeliverableSuggestionsSection: React.FC<DeliverableSuggestionsSectionProps> = ({
  suggestions,
  onRefresh,
}) => {
  const router = useRouter();
  const [loadingId, setLoadingId] = useState<string | null>(null);

  if (!suggestions || suggestions.length === 0) return null;

  const handleAccept = async (id: string) => {
    setLoadingId(id);
    try {
      const content = await acceptDeliverableSuggestion(id);
      router.push(`/content/${content.id}`);
    } catch (err) {
      console.error('Failed to accept deliverable suggestion:', err);
    } finally {
      setLoadingId(null);
    }
  };

  const handleDismiss = async (id: string) => {
    setLoadingId(id);
    try {
      await dismissDeliverableSuggestion(id);
      onRefresh();
    } catch (err) {
      console.error('Failed to dismiss deliverable suggestion:', err);
    } finally {
      setLoadingId(null);
    }
  };

  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-center gap-2">
        <span className="w-2 h-2 rounded-full bg-cyan-500 animate-pulse" />
        <Typography variant="h3" className="text-xs font-semibold text-cyan-400 uppercase tracking-wider">
          Potential Deliverables ({suggestions.length})
        </Typography>
      </div>

      <div className="flex flex-col gap-3">
        {suggestions.map((sugg) => (
          <Card
            key={sugg.id}
            variant="panel"
            className="flex flex-col gap-3 p-4 border-cyan-500/30 bg-cyan-500/5"
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex flex-col gap-1">
                <div className="flex items-center gap-2">
                  <Badge variant="cyan">{sugg.type.toUpperCase()}</Badge>
                  <Typography variant="h3" className="text-sm font-semibold text-slate-100">
                    {sugg.title}
                  </Typography>
                </div>
                <Typography variant="body" className="text-xs text-slate-300">
                  {sugg.reason}
                </Typography>
              </div>

              <div className="flex items-center gap-2 shrink-0">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => handleDismiss(sugg.id)}
                  disabled={loadingId === sugg.id}
                >
                  Dismiss
                </Button>
                <Button
                  variant="primary"
                  size="sm"
                  onClick={() => handleAccept(sugg.id)}
                  isLoading={loadingId === sugg.id}
                >
                  Create Draft
                </Button>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
