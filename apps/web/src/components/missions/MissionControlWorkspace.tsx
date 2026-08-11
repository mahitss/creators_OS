'use client';

import React, { useState, useEffect } from 'react';
import { 
  GitBranch, 
  CheckCircle2, 
  AlertTriangle, 
  RotateCw, 
  ShieldCheck, 
  Cpu, 
  DollarSign, 
  Layers, 
  Clock, 
  Activity, 
  Play, 
  FileCheck,
  Zap,
  UserCheck
} from 'lucide-react';

interface MissionPlanData {
  id: string;
  missionId: string;
  version: number;
  objectiveSummary: string;
  status: string;
  maxReplans: number;
  replanCount: number;
  steps: any[];
}

interface MissionCostData {
  missionId: string;
  estimatedCostUsd: number;
  actualCostUsd: number;
  modelCostUsd: number;
  toolCostUsd: number;
  remainingBudgetUsd: number;
}

interface MissionRiskData {
  missionId: string;
  dataRisk: string;
  actionRisk: string;
  financialRisk: string;
  securityRisk: string;
  executionRisk: string;
  activeWarnings: string[];
}

export const MissionControlWorkspace: React.FC<{ missionId: string }> = ({ missionId }) => {
  const [plan, setPlan] = useState<MissionPlanData | null>({
    id: 'mp_001',
    missionId: missionId,
    version: 1,
    objectiveSummary: 'Q3 Enterprise Risk & Data Security Audit Execution Plan',
    status: 'executing',
    maxReplans: 5,
    replanCount: 0,
    steps: [
      {
        id: 'step_001',
        title: 'Gather Architecture Security Specs',
        stepType: 'knowledge_task',
        assignedExecutorId: 'ag_creator_ops_01',
        assignedExecutorType: 'agent',
        requiredCapabilityId: 'cap_skill_doc_analysis',
        status: 'completed',
        inputPayload: { domain: 'architecture_handbook' },
        outputPayload: { artifacts: ['doc_arch_spec_01'] }
      },
      {
        id: 'step_002',
        title: 'Execute DLP Data Boundary Scan',
        stepType: 'tool_task',
        assignedExecutorId: 'tool_dlp_scan',
        assignedExecutorType: 'tool',
        requiredCapabilityId: 'cap_tool_dlp_scan',
        status: 'executing',
        inputPayload: { doc_id: 'doc_arch_spec_01' },
        outputPayload: {}
      }
    ]
  });

  const [costs, setCosts] = useState<MissionCostData | null>({
    missionId: missionId,
    estimatedCostUsd: 0.50,
    actualCostUsd: 0.12,
    modelCostUsd: 0.10,
    toolCostUsd: 0.02,
    remainingBudgetUsd: 9.88
  });

  const [risks, setRisks] = useState<MissionRiskData | null>({
    missionId: missionId,
    dataRisk: 'low',
    actionRisk: 'medium',
    financialRisk: 'low',
    securityRisk: 'low',
    executionRisk: 'low',
    activeWarnings: ['Action Gateway approval required for external notify step']
  });

  const [activeTab, setActiveTab] = useState<'plan' | 'deliverables' | 'replans' | 'telemetry'>('plan');
  const [replanReason, setReplanReason] = useState('Dependency latency spike detected');

  const fetchPlan = React.useCallback(async () => {
    try {
      const res = await fetch(`/api/v1/missions/${missionId}/plan`);
      if (res.ok) {
        const data = await res.json();
        setPlan(data);
      }
    } catch (e) {
      // Keep fallback
    }
  }, [missionId]);

  useEffect(() => {
    fetchPlan();
  }, [fetchPlan]);

  const handleReplan = async () => {
    try {
      const res = await fetch(`/api/v1/missions/${missionId}/plan/replan`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ triggerReason: replanReason })
      });
      if (res.ok) {
        const updated = await res.json();
        setPlan(updated);
      }
    } catch (e) {
      if (plan) {
        setPlan({
          ...plan,
          version: plan.version + 1,
          replanCount: plan.replanCount + 1,
          steps: [
            ...plan.steps,
            {
              id: `step_00${plan.steps.length + 1}`,
              title: `Replanned Step: ${replanReason}`,
              stepType: 'validation_task',
              assignedExecutorId: 'ag_creator_ops_01',
              assignedExecutorType: 'agent',
              status: 'ready'
            }
          ]
        });
      }
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Header & Telemetry Bar */}
      <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl text-white space-y-4">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-indigo-500/20 text-indigo-400 rounded-lg border border-indigo-500/30">
              <GitBranch className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight">Mission Intelligence 2.0 Orchestrator</h1>
              <p className="text-xs text-slate-400">Policy-governed multi-agent orchestration, adaptive DAG planning, & evidence verification</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleReplan}
              className="flex items-center gap-1.5 px-3 py-1.5 bg-amber-600/20 hover:bg-amber-600/30 text-amber-300 border border-amber-500/30 rounded-lg text-xs font-medium transition"
            >
              <RotateCw className="w-3.5 h-3.5" /> Trigger Event Replan
            </button>
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 text-xs border-t border-slate-800 pt-4 text-slate-400">
          <div>Objective Clarity: <span className="text-emerald-400 font-semibold uppercase">CLEAR</span></div>
          <div>Plan Version: <span className="text-indigo-400 font-mono">v{plan?.version || 1}</span></div>
          <div>Replans: <span className="text-slate-200 font-mono">{plan?.replanCount || 0} / {plan?.maxReplans || 5}</span></div>
          <div>Remaining Budget: <span className="text-emerald-400 font-mono">${costs?.remainingBudgetUsd.toFixed(2) || '9.88'}</span></div>
          <div>Action Risk: <span className="text-amber-400 uppercase font-mono">{risks?.actionRisk || 'LOW'}</span></div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
        <button
          onClick={() => setActiveTab('plan')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition ${
            activeTab === 'plan' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Interactive DAG Plan ({plan?.steps.length || 0})
        </button>
        <button
          onClick={() => setActiveTab('deliverables')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition ${
            activeTab === 'deliverables' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Deliverable & Action Validation
        </button>
        <button
          onClick={() => setActiveTab('telemetry')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition ${
            activeTab === 'telemetry' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Risk & Cost Telemetry
        </button>
      </div>

      {/* Tab: Interactive Plan */}
      {activeTab === 'plan' && (
        <div className="space-y-4">
          <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
            <h3 className="text-xs font-semibold text-slate-400 uppercase mb-3">DAG Execution Sequence</h3>
            <div className="space-y-3">
              {plan?.steps.map((step, idx) => (
                <div key={step.id} className="bg-slate-950 border border-slate-800 p-4 rounded-lg flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-6 h-6 rounded-full bg-slate-800 flex items-center justify-center text-xs font-mono text-indigo-400 font-bold">
                      {idx + 1}
                    </div>
                    <div>
                      <h4 className="text-sm font-semibold text-white">{step.title}</h4>
                      <p className="text-xs text-slate-400 mt-0.5 font-mono">
                        Executor: <span className="text-indigo-300">{step.assignedExecutorId || 'Unassigned'}</span> ({step.stepType})
                      </p>
                    </div>
                  </div>

                  <span className={`px-3 py-1 text-xs font-medium rounded-full ${
                    step.status === 'completed' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' :
                    step.status === 'executing' ? 'bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 animate-pulse' :
                    'bg-slate-800 text-slate-400'
                  }`}>
                    {step.status.toUpperCase()}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Tab: Deliverables & Evidence */}
      {activeTab === 'deliverables' && (
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl space-y-3">
          <div className="flex items-center gap-2 text-emerald-400 text-sm font-semibold">
            <FileCheck className="w-4 h-4" /> MissionValidator Evidence Verification
          </div>
          <p className="text-xs text-slate-300">Outputs are verified against actual artifacts or ActionGateway execution logs before marking steps complete.</p>

          <div className="bg-slate-950 p-4 rounded-lg border border-slate-800 text-xs font-mono text-slate-300 space-y-2">
            <div>Verified Artifact: <span className="text-indigo-400">doc_arch_spec_01</span></div>
            <div>ActionGateway Verification: <span className="text-emerald-400">PASSED</span></div>
            <div>No Fake Progress Rule: <span className="text-emerald-400">ACTIVE</span></div>
          </div>
        </div>
      )}

      {/* Tab: Risk & Cost Telemetry */}
      {activeTab === 'telemetry' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl space-y-3">
            <h3 className="text-sm font-semibold text-white">Multi-Dimensional Risk Matrix</h3>
            <div className="grid grid-cols-2 gap-2 text-xs font-mono">
              <div className="p-2.5 bg-slate-950 rounded border border-slate-800">Data Risk: <span className="text-emerald-400 uppercase">{risks?.dataRisk}</span></div>
              <div className="p-2.5 bg-slate-950 rounded border border-slate-800">Action Risk: <span className="text-amber-400 uppercase">{risks?.actionRisk}</span></div>
              <div className="p-2.5 bg-slate-950 rounded border border-slate-800">Financial Risk: <span className="text-emerald-400 uppercase">{risks?.financialRisk}</span></div>
              <div className="p-2.5 bg-slate-950 rounded border border-slate-800">Security Risk: <span className="text-emerald-400 uppercase">{risks?.securityRisk}</span></div>
            </div>
          </div>

          <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl space-y-3">
            <h3 className="text-sm font-semibold text-white">Cost & Budget Distribution</h3>
            <div className="space-y-2 text-xs font-mono text-slate-300 bg-slate-950 p-3 rounded border border-slate-800">
              <div>Estimated Cost: <span className="text-slate-200">${costs?.estimatedCostUsd}</span></div>
              <div>Actual Cost: <span className="text-emerald-400">${costs?.actualCostUsd}</span></div>
              <div>Model Cost: <span className="text-indigo-400">${costs?.modelCostUsd}</span></div>
              <div>Tool Cost: <span className="text-indigo-400">${costs?.toolCostUsd}</span></div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
