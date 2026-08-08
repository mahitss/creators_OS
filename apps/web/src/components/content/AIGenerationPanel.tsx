import React from 'react';
import { Card, Typography, Button } from '@vapor/ui';

export interface AIGenerationPanelProps {
  onGenerate: (intent: 'draft' | 'rewrite' | 'expand' | 'summarize' | 'improve') => void;
  isGenerating: boolean;
}

export const AIGenerationPanel: React.FC<AIGenerationPanelProps> = ({
  onGenerate,
  isGenerating,
}) => {
  return (
    <Card variant="panel" className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 p-3.5 border-slate-800/80 bg-[#12141C]">
      <div className="flex items-center gap-2">
        <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
        <Typography variant="h3" className="text-xs font-semibold text-slate-200">
          Executive AI Content Studio
        </Typography>
      </div>

      <div className="flex flex-wrap items-center gap-1.5 w-full sm:w-auto">
        <Button
          variant="primary"
          size="sm"
          onClick={() => onGenerate('draft')}
          isLoading={isGenerating}
        >
          ⚡ Draft
        </Button>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => onGenerate('rewrite')}
          disabled={isGenerating}
        >
          Rewrite
        </Button>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => onGenerate('expand')}
          disabled={isGenerating}
        >
          Expand
        </Button>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => onGenerate('summarize')}
          disabled={isGenerating}
        >
          Summarize
        </Button>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => onGenerate('improve')}
          disabled={isGenerating}
        >
          Improve
        </Button>
      </div>
    </Card>
  );
};
