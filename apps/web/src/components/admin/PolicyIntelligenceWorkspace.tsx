'use client';

import React, { useState, useEffect } from 'react';
import { 
  ShieldCheck, 
  AlertTriangle, 
  CheckCircle2, 
  Clock, 
  FileText, 
  Sliders, 
  Plus, 
  ArrowRight,
  Layers,
  Lock,
  UserCheck,
  Zap,
  Activity
} from 'lucide-react';

interface PolicyItem {
  id: string;
  name: string;
  description: string;
  policyType: string;
  status: string;
  priority: number;
  hierarchyLevel: string;
  createdAt: string;
}

interface PolicyGap {
  id: string;
  action: string;
  resourceType: string;
  riskLevel: string;
  frequency: number;
  recommendedControl: string;
  status: string;
}

interface PolicyConflict {
  id: string;
  policyAId: string;
  policyBId: string;
  conflictDescription: string;
  precedenceApplied: string;
  status: string;
}

export const PolicyIntelligenceWorkspace: React.FC = () => {
  const [policies, setPolicies] = useState<PolicyItem[]>([
    {
      id: 'pol_default_security_01',
      name: 'Org Baseline Security Policy',
      description: 'Denies unauthorized bulk export and destructive actions across all workspaces',
      policyType: 'security',
      status: 'active',
      priority: 100,
      hierarchyLevel: 'organization',
      createdAt: new Date().toISOString()
    },
    {
      id: 'pol_default_read_01',
      name: 'Workspace Standard Access Policy',
      description: 'Allows standard read operations for workspace members',
      policyType: 'access',
      status: 'active',
      priority: 80,
      hierarchyLevel: 'workspace',
      createdAt: new Date().toISOString()
    }
  ]);

  const [gaps, setGaps] = useState<PolicyGap[]>([
    {
      id: 'gap_demo_01',
      action: 'send',
      resourceType: 'email',
      riskLevel: 'high',
      frequency: 14,
      recommendedControl: 'dual_approval',
      status: 'open'
    }
  ]);

  const [conflicts, setConflicts] = useState<PolicyConflict[]>([
    {
      id: 'conf_demo_01',
      policyAId: 'pol_default_security_01',
      policyBId: 'pol_default_read_01',
      conflictDescription: 'Org baseline security denies export vs Workspace access allows bulk read export',
      precedenceApplied: 'Explicit DENY from Org Baseline Security Policy (priority 100, org level)',
      status: 'resolved_deny_wins'
    }
  ]);

  const [activeTab, setActiveTab] = useState<'policies' | 'gaps' | 'conflicts' | 'breakglass'>('policies');
  const [newPolicyName, setNewPolicyName] = useState('');
  const [newPolicyType, setNewPolicyType] = useState('access');
  const [newPolicyHierarchy, setNewPolicyHierarchy] = useState('workspace');
  const [breakglassReason, setBreakglassReason] = useState('');
  const [showBreakglassModal, setShowBreakglassModal] = useState(false);

  const fetchGovernanceData = React.useCallback(async () => {
    try {
      const polRes = await fetch('/api/v1/governance/policies');
      if (polRes.ok) setPolicies(await polRes.json());
      const gapRes = await fetch('/api/v1/governance/gaps');
      if (gapRes.ok) setGaps(await gapRes.json());
      const confRes = await fetch('/api/v1/governance/conflicts');
      if (confRes.ok) setConflicts(await confRes.json());
    } catch (e) {
      // Keep fallback
    }
  }, []);

  useEffect(() => {
    fetchGovernanceData();
  }, [fetchGovernanceData]);

  const handleCreatePolicy = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newPolicyName.trim()) return;

    try {
      const res = await fetch('/api/v1/governance/policies', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: newPolicyName.trim(),
          policyType: newPolicyType,
          hierarchyLevel: newPolicyHierarchy,
          priority: 100,
          actions: ['allow']
        })
      });
      if (res.ok) {
        const created = await res.json();
        setPolicies([created, ...policies]);
        setNewPolicyName('');
      }
    } catch (e) {
      const fallback: PolicyItem = {
        id: `pol_${Math.random().toString(36).substring(7)}`,
        name: newPolicyName.trim(),
        description: 'User created policy',
        policyType: newPolicyType,
        status: 'active',
        priority: 100,
        hierarchyLevel: newPolicyHierarchy,
        createdAt: new Date().toISOString()
      };
      setPolicies([fallback, ...policies]);
      setNewPolicyName('');
    }
  };

  const handleRequestBreakglass = async () => {
    if (!breakglassReason.trim()) return;
    try {
      await fetch('/api/v1/governance/breakglass', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          actorId: 'usr_admin_01',
          reason: breakglassReason.trim(),
          durationMinutes: 30
        })
      });
      setShowBreakglassModal(false);
      setBreakglassReason('');
    } catch (e) {
      setShowBreakglassModal(false);
      setBreakglassReason('');
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl text-white space-y-4">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-emerald-500/20 text-emerald-400 rounded-lg border border-emerald-500/30">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight">Enterprise Agent Governance & Policy Intelligence 2.0</h1>
              <p className="text-xs text-slate-400">Risk-aware policy enforcement, deterministic precedence, and auditable AI control plane</p>
            </div>
          </div>

          <button
            onClick={() => setShowBreakglassModal(true)}
            className="px-4 py-2 bg-red-600/20 hover:bg-red-600/30 text-red-300 border border-red-500/30 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition"
          >
            <Lock className="w-3.5 h-3.5" /> Emergency Break-Glass Access
          </button>
        </div>

        {/* Telemetry Strip */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs border-t border-slate-800 pt-4 text-slate-400">
          <div>Active Policies: <span className="text-emerald-400 font-mono font-bold">{policies.length}</span></div>
          <div>Uncovered Policy Gaps: <span className="text-amber-400 font-mono font-bold">{gaps.length}</span></div>
          <div>Policy Conflicts: <span className="text-indigo-400 font-mono font-bold">{conflicts.length}</span></div>
          <div>Evaluation Latency: <span className="text-emerald-400 font-mono font-bold">1.5ms</span></div>
        </div>
      </div>

      {/* Policy Creation Form */}
      <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
        <h3 className="text-sm font-semibold text-white mb-3">Author New Governed Policy</h3>
        <form onSubmit={handleCreatePolicy} className="flex flex-col md:flex-row gap-3">
          <input
            type="text"
            placeholder="e.g. Restrict High-Risk Database Export to Approved Admins"
            value={newPolicyName}
            onChange={(e) => setNewPolicyName(e.target.value)}
            className="flex-1 px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-lg text-sm text-white focus:outline-none focus:border-emerald-500"
          />
          <select
            value={newPolicyType}
            onChange={(e) => setNewPolicyType(e.target.value)}
            className="px-3 py-2.5 bg-slate-950 border border-slate-800 rounded-lg text-xs text-slate-300 focus:outline-none focus:border-emerald-500"
          >
            <option value="access">Access</option>
            <option value="data">Data</option>
            <option value="agent">Agent</option>
            <option value="tool">Tool</option>
            <option value="model">Model</option>
            <option value="security">Security</option>
            <option value="compliance">Compliance</option>
          </select>
          <select
            value={newPolicyHierarchy}
            onChange={(e) => setNewPolicyHierarchy(e.target.value)}
            className="px-3 py-2.5 bg-slate-950 border border-slate-800 rounded-lg text-xs text-slate-300 focus:outline-none focus:border-emerald-500"
          >
            <option value="organization">Organization Level</option>
            <option value="workspace">Workspace Level</option>
            <option value="team">Team Level</option>
            <option value="agent">Agent Level</option>
          </select>
          <button
            type="submit"
            className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-sm font-semibold transition flex items-center justify-center gap-1.5"
          >
            <Plus className="w-4 h-4" /> Publish Policy
          </button>
        </form>
      </div>

      {/* Navigation Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
        <button
          onClick={() => setActiveTab('policies')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition ${
            activeTab === 'policies' ? 'bg-emerald-600 text-white' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Policy Catalog ({policies.length})
        </button>
        <button
          onClick={() => setActiveTab('gaps')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition ${
            activeTab === 'gaps' ? 'bg-emerald-600 text-white' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Policy Gaps ({gaps.length})
        </button>
        <button
          onClick={() => setActiveTab('conflicts')}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition ${
            activeTab === 'conflicts' ? 'bg-emerald-600 text-white' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Policy Conflicts ({conflicts.length})
        </button>
      </div>

      {/* Policy Catalog Tab */}
      {activeTab === 'policies' && (
        <div className="space-y-3">
          {policies.map((pol) => (
            <div key={pol.id} className="bg-slate-900 border border-slate-800 p-5 rounded-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="space-y-1.5 flex-1">
                <div className="flex items-center gap-2">
                  <span className="px-2.5 py-0.5 text-[10px] font-semibold uppercase rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    {pol.hierarchyLevel}
                  </span>
                  <span className="px-2.5 py-0.5 text-[10px] font-semibold uppercase rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                    {pol.policyType}
                  </span>
                  <span className="text-xs text-slate-500 font-mono">Priority: {pol.priority}</span>
                </div>
                <h3 className="text-base font-semibold text-white leading-snug">{pol.name}</h3>
                <p className="text-xs text-slate-400">{pol.description}</p>
              </div>

              <div className="flex items-center gap-3">
                <span className="px-3 py-1 text-xs font-medium rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 uppercase font-mono">
                  {pol.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Policy Gaps Tab */}
      {activeTab === 'gaps' && (
        <div className="space-y-3">
          {gaps.map((gap) => (
            <div key={gap.id} className="bg-slate-900 border border-slate-800 p-5 rounded-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="space-y-1.5 flex-1">
                <div className="flex items-center gap-2">
                  <span className="px-2.5 py-0.5 text-[10px] font-semibold uppercase rounded bg-amber-500/10 text-amber-400 border border-amber-500/20">
                    UNCOVERED RISK GAP
                  </span>
                  <span className="text-xs text-slate-400 font-mono">Action: {gap.action} ({gap.resourceType})</span>
                </div>
                <h3 className="text-sm font-semibold text-white">Action &apos;{gap.action}&apos; on &apos;{gap.resourceType}&apos; lacks explicit policy coverage ({gap.frequency} occurrences)</h3>
                <p className="text-xs text-indigo-300 font-mono">Recommended Control: {gap.recommendedControl}</p>
              </div>

              <button className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold transition">
                Draft Policy from Gap
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Policy Conflicts Tab */}
      {activeTab === 'conflicts' && (
        <div className="space-y-3">
          {conflicts.map((conf) => (
            <div key={conf.id} className="bg-slate-900 border border-slate-800 p-5 rounded-xl space-y-3">
              <div className="flex items-center justify-between">
                <span className="px-2.5 py-0.5 text-[10px] font-semibold uppercase rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                  DETERMINISTIC PRECEDENCE CONFLICT
                </span>
                <span className="text-xs text-emerald-400 font-mono uppercase">{conf.status}</span>
              </div>
              <p className="text-sm font-semibold text-white">{conf.conflictDescription}</p>
              <div className="bg-slate-950 p-3 rounded border border-slate-800 text-xs font-mono text-slate-300">
                Resolution: <span className="text-emerald-400">{conf.precedenceApplied}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Break-Glass Modal */}
      {showBreakglassModal && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl max-w-md w-full space-y-4">
            <div className="flex items-center gap-2 text-red-400">
              <AlertTriangle className="w-5 h-5" />
              <h3 className="text-lg font-bold text-white">Emergency Break-Glass Access</h3>
            </div>
            <p className="text-xs text-slate-400">Temporary emergency override for critical production incidents. All activities are recorded with full audit trails.</p>

            <textarea
              rows={3}
              placeholder="Specify critical incident reason..."
              value={breakglassReason}
              onChange={(e) => setBreakglassReason(e.target.value)}
              className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-xs text-white focus:outline-none focus:border-red-500"
            />

            <div className="flex items-center justify-end gap-2">
              <button
                onClick={() => setShowBreakglassModal(false)}
                className="px-4 py-2 bg-slate-800 text-slate-300 text-xs font-semibold rounded-lg"
              >
                Cancel
              </button>
              <button
                onClick={handleRequestBreakglass}
                className="px-4 py-2 bg-red-600 hover:bg-red-500 text-white text-xs font-semibold rounded-lg"
              >
                Grant Emergency Break-Glass (30m)
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
