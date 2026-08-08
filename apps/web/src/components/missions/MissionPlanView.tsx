import React from 'react';
import { Card, Typography, Badge, Button } from '@vapor/ui';
import { MissionPlan } from '../../lib/api/missions';

export interface MissionPlanViewProps {
  plan: MissionPlan;
  onRegenerate: () => void;
  isRegenerating: boolean;
}

export const MissionPlanView: React.FC<MissionPlanViewProps> = ({
  plan,
  onRegenerate,
  isRegenerating,
}) => {
  return (
    <Card variant="panel" className="flex flex-col gap-5 p-6 border-emerald-500/20 bg-emerald-500/5">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          <Typography variant="h3" className="text-sm font-semibold text-slate-100">
            Executive Mission Plan
          </Typography>
          <Badge variant="emerald">PLAN V{plan.version}</Badge>
        </div>

        <Button
          variant="secondary"
          size="sm"
          onClick={onRegenerate}
          isLoading={isRegenerating}
        >
          ↻ Regenerate Plan
        </Button>
      </div>

      {/* Goal & Summary */}
      <div className="flex flex-col gap-2 p-3.5 rounded bg-slate-900/80 border border-slate-800">
        <Typography variant="caption" className="text-[11px] font-mono uppercase text-emerald-400 font-semibold">
          Goal Statement
        </Typography>
        <Typography variant="body" className="text-sm text-slate-200 font-medium">
          {plan.goal}
        </Typography>
        <Typography variant="caption" className="text-xs text-slate-400 mt-1 leading-relaxed">
          {plan.summary}
        </Typography>
      </div>

      {/* Steps */}
      {plan.steps && plan.steps.length > 0 && (
        <div className="flex flex-col gap-3">
          <Typography variant="h3" className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
            Execution Steps
          </Typography>
          <div className="flex flex-col gap-2">
            {plan.steps.map((step) => (
              <div key={step.order} className="flex items-start gap-3 p-3 rounded bg-slate-900/60 border border-slate-800">
                <span className="w-6 h-6 rounded-full bg-emerald-500/10 text-emerald-400 font-mono text-xs flex items-center justify-center font-bold shrink-0">
                  {step.order}
                </span>
                <div className="flex flex-col gap-0.5">
                  <Typography variant="body" className="text-xs font-semibold text-slate-200">
                    {step.title}
                  </Typography>
                  <Typography variant="caption" className="text-xs text-slate-400 leading-relaxed">
                    {step.description}
                  </Typography>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Deliverables & Recommendations grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Deliverables */}
        {plan.deliverables && plan.deliverables.length > 0 && (
          <div className="flex flex-col gap-2 p-3.5 rounded bg-slate-900/60 border border-slate-800">
            <Typography variant="caption" className="text-[11px] font-mono uppercase text-cyan-400 font-semibold">
              Expected Deliverables
            </Typography>
            <ul className="list-disc list-inside text-xs text-slate-300 flex flex-col gap-1">
              {plan.deliverables.map((item, idx) => (
                <li key={idx}>{item}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Recommendations */}
        {plan.recommendations && plan.recommendations.length > 0 && (
          <div className="flex flex-col gap-2 p-3.5 rounded bg-slate-900/60 border border-slate-800">
            <Typography variant="caption" className="text-[11px] font-mono uppercase text-amber-400 font-semibold">
              Executive Recommendations
            </Typography>
            <ul className="list-disc list-inside text-xs text-slate-300 flex flex-col gap-1">
              {plan.recommendations.map((item, idx) => (
                <li key={idx}>{item}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Open Questions */}
      {plan.open_questions && plan.open_questions.length > 0 && (
        <div className="flex flex-col gap-2 p-3.5 rounded bg-slate-900/60 border border-slate-800">
          <Typography variant="caption" className="text-[11px] font-mono uppercase text-rose-400 font-semibold">
            Questions / Clarifications Required
          </Typography>
          <ul className="list-disc list-inside text-xs text-slate-300 flex flex-col gap-1">
            {plan.open_questions.map((q, idx) => (
              <li key={idx}>{q}</li>
            ))}
          </ul>
        </div>
      )}
    </Card>
  );
};
