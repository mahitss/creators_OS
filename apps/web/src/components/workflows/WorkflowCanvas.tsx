'use client';

import React, { useState, useEffect } from 'react';
import {
  GitBranch,
  Play,
  CheckCircle2,
  AlertTriangle,
  Zap,
  Cpu,
  Wrench,
  Clock,
  ShieldCheck,
  RotateCcw,
  Sliders,
  Plus,
  Trash2,
  Eye,
  Check,
  Save,
  ArrowRight,
  HelpCircle,
  FileCode,
  Share2
} from 'lucide-react';
import { WorkflowCopilot } from './WorkflowCopilot';

// ... interface definitions ...


interface NodeConfig {
  tool_name?: string;
  description?: string;
  approval_required?: boolean;
  input_schema?: Record<string, any>;
  [key: string]: any;
}

interface WorkflowNode {
  id: string;
  node_key: string;
  type: string; // trigger, condition, branch, agent, tool, approval, delay, transform, notification, mission, end
  title: string;
  config: NodeConfig;
  position?: { x: number; y: number };
}

interface WorkflowEdge {
  id: string;
  source_node_id: string;
  target_node_id: string;
  condition_handle?: string;
}

interface WorkflowDefinition {
  nodes: WorkflowNode[];
  edges: WorkflowEdge[];
  variables: Record<string, any>;
}

interface WorkflowCanvasProps {
  workflowId: string;
}

export const WorkflowCanvas: React.FC<WorkflowCanvasProps> = ({ workflowId }) => {
  const [workflow, setWorkflow] = useState<any>(null);
  const [nodes, setNodes] = useState<WorkflowNode[]>([]);
  const [edges, setEdges] = useState<WorkflowEdge[]>([]);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [saving, setSaving] = useState<boolean>(false);
  const [publishing, setPublishing] = useState<boolean>(false);
  const [showPublishModal, setShowPublishModal] = useState<boolean>(false);
  const [publishResult, setPublishResult] = useState<any>(null);
  const [showTestModal, setShowTestModal] = useState<boolean>(false);
  const [testResult, setTestResult] = useState<any>(null);
  const [testing, setTesting] = useState<boolean>(false);

  // Form config state
  const [configTitle, setConfigTitle] = useState('');
  const [configToolName, setConfigToolName] = useState('');
  const [configDescription, setConfigDescription] = useState('');
  const [configApprovalRequired, setConfigApprovalRequired] = useState(false);

  useEffect(() => {
    fetchWorkflow();
  }, [workflowId]);

  const fetchWorkflow = async () => {
    setLoading(true);
    try {
      const res = await fetch(`/api/v1/workflows/${workflowId}`);
      if (res.ok) {
        const data = await res.json();
        setWorkflow(data);
        // Load initial definition
        const def = data.definition || { nodes: [], edges: [], variables: {} };
        if (def.nodes && def.nodes.length > 0) {
          setNodes(def.nodes);
          setEdges(def.edges || []);
        } else {
          // Default template nodes if empty
          setNodes([
            { id: 'node_trig_1', node_key: 'trig_1', type: 'trigger', title: 'Schedule Trigger', config: { description: 'Fires daily' }, position: { x: 50, y: 100 } },
            { id: 'node_agent_1', node_key: 'agent_1', type: 'agent', title: 'Executive Agent', config: { description: 'Synthesize brief' }, position: { x: 250, y: 100 } },
            { id: 'node_end_1', node_key: 'end_1', type: 'end', title: 'End Workflow', config: {}, position: { x: 450, y: 100 } }
          ]);
          setEdges([
            { id: 'e1', source_node_id: 'node_trig_1', target_node_id: 'node_agent_1' },
            { id: 'e2', source_node_id: 'node_agent_1', target_node_id: 'node_end_1' }
          ]);
        }
      }
    } catch (err) {
      console.error('Failed to fetch workflow', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddNode = (type: string) => {
    const newId = `node_${type}_${Date.now().toString().slice(-4)}`;
    const newNode: WorkflowNode = {
      id: newId,
      node_key: newId,
      type,
      title: `${type.toUpperCase()} Node`,
      config: { description: `New ${type} node` },
      position: { x: 100 + nodes.length * 40, y: 150 }
    };
    setNodes([...nodes, newNode]);
    setSelectedNodeId(newId);
    setConfigTitle(newNode.title);
    setConfigDescription(newNode.config.description || '');
    setConfigToolName(newNode.config.tool_name || '');
    setConfigApprovalRequired(!!newNode.config.approval_required);
  };

  const handleSelectNode = (n: WorkflowNode) => {
    setSelectedNodeId(n.id);
    setConfigTitle(n.title);
    setConfigDescription(n.config.description || '');
    setConfigToolName(n.config.tool_name || '');
    setConfigApprovalRequired(!!n.config.approval_required);
  };

  const handleSaveNodeConfig = () => {
    if (!selectedNodeId) return;
    setNodes(nodes.map((n) => {
      if (n.id === selectedNodeId) {
        return {
          ...n,
          title: configTitle,
          config: {
            ...n.config,
            description: configDescription,
            tool_name: configToolName || undefined,
            approval_required: configApprovalRequired
          }
        };
      }
      return n;
    }));
  };

  const handleDeleteNode = (id: string) => {
    setNodes(nodes.filter((n) => n.id !== id));
    setEdges(edges.filter((e) => e.source_node_id !== id && e.target_node_id !== id));
    if (selectedNodeId === id) setSelectedNodeId(null);
  };

  const handleSaveDraft = async () => {
    setSaving(true);
    try {
      await fetch(`/api/v1/workflows/${workflowId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          definition: {
            nodes,
            edges,
            variables: {}
          }
        })
      });
    } catch (err) {
      console.error('Failed to save draft workflow', err);
    } finally {
      setSaving(false);
    }
  };

  const handlePublish = async () => {
    setPublishing(true);
    setPublishResult(null);
    try {
      // First save draft
      await handleSaveDraft();
      // Publish
      const res = await fetch(`/api/v1/workflows/${workflowId}/publish`, { method: 'POST' });
      if (res.ok) {
        const data = await res.json();
        setPublishResult(data);
        fetchWorkflow();
      }
    } catch (err) {
      console.error('Failed to publish workflow', err);
    } finally {
      setPublishing(false);
    }
  };

  const handleDryRunTest = async () => {
    setTesting(true);
    setTestResult(null);
    try {
      await handleSaveDraft();
      const res = await fetch(`/api/v1/workflows/${workflowId}/test`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          test_event_payload: { event_type: 'calendar.event_updated', is_deadline_change: true }
        })
      });
      if (res.ok) {
        const data = await res.json();
        setTestResult(data);
      }
    } catch (err) {
      console.error('Failed to run dry-run simulation', err);
    } finally {
      setTesting(false);
    }
  };

  const selectedNode = nodes.find((n) => n.id === selectedNodeId);

  return (
    <div className="flex flex-col h-full bg-slate-950 text-slate-100 p-6 space-y-4 overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-indigo-500/10 text-indigo-400 rounded-lg border border-indigo-500/20">
            <GitBranch className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="text-xl font-bold tracking-tight text-slate-50">{workflow?.name || 'Visual Workflow Builder'}</h1>
              <span className={`text-[10px] px-2 py-0.5 rounded-full border font-medium ${
                workflow?.status === 'active' ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400' : 'bg-slate-800 border-slate-700 text-slate-400'
              }`}>
                {workflow?.status?.toUpperCase() || 'DRAFT'} v{workflow?.version || 1}
              </span>
            </div>
            <p className="text-xs text-slate-400">{workflow?.description || 'Authoring visual DAG workflow definition'}</p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={handleDryRunTest}
            disabled={testing}
            className="flex items-center space-x-1.5 px-3 py-1.5 bg-slate-900 border border-slate-700 text-slate-300 hover:text-slate-100 rounded-lg text-xs font-medium transition"
          >
            <Eye className="w-3.5 h-3.5 text-cyan-400" />
            <span>{testing ? 'Simulating...' : 'Dry-Run Simulation'}</span>
          </button>

          <button
            onClick={handleSaveDraft}
            disabled={saving}
            className="flex items-center space-x-1.5 px-3 py-1.5 bg-slate-900 border border-slate-700 text-slate-300 hover:text-slate-100 rounded-lg text-xs font-medium transition"
          >
            <Save className="w-3.5 h-3.5 text-amber-400" />
            <span>{saving ? 'Saving...' : 'Save Draft'}</span>
          </button>

          <button
            onClick={handlePublish}
            disabled={publishing}
            className="flex items-center space-x-1.5 px-3.5 py-1.5 bg-gradient-to-r from-emerald-500 to-emerald-600 hover:from-emerald-600 hover:to-emerald-700 text-slate-950 font-semibold rounded-lg text-xs shadow-lg shadow-emerald-500/10 transition"
          >
            <ShieldCheck className="w-4 h-4" />
            <span>{publishing ? 'Publishing...' : 'Publish Workflow'}</span>
          </button>
        </div>
      </div>

      {/* Main Authoring Layout */}
      <div className="grid grid-cols-1 xl:grid-cols-12 gap-4 flex-1 overflow-hidden">
        {/* Node Palette Sidebar */}
        <div className="xl:col-span-2 bg-slate-900/50 border border-slate-800 rounded-xl p-4 flex flex-col space-y-4 overflow-y-auto">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Node Palette</h2>

          <div className="space-y-2">
            {[
              { type: 'trigger', label: 'Trigger', icon: <Zap className="w-4 h-4 text-amber-400" />, desc: 'Event or Schedule' },
              { type: 'condition', label: 'Condition', icon: <Sliders className="w-4 h-4 text-cyan-400" />, desc: 'Structured Comparison' },
              { type: 'agent', label: 'Agent', icon: <Cpu className="w-4 h-4 text-indigo-400" />, desc: 'Agent Runtime Task' },
              { type: 'tool', label: 'Tool Call', icon: <FileCode className="w-4 h-4 text-emerald-400" />, desc: 'Tool Registry Action' },
              { type: 'approval', label: 'Human Approval', icon: <ShieldCheck className="w-4 h-4 text-rose-400" />, desc: 'Pause for Approval' },
              { type: 'delay', label: 'Delay', icon: <Clock className="w-4 h-4 text-slate-400" />, desc: 'Scheduled Delay' },
              { type: 'end', label: 'End Terminal', icon: <CheckCircle2 className="w-4 h-4 text-emerald-500" />, desc: 'Workflow Completion' }
            ].map((item) => (
              <button
                key={item.type}
                onClick={() => handleAddNode(item.type)}
                className="w-full flex items-center justify-between p-3 bg-slate-900/80 border border-slate-800 hover:border-slate-700 rounded-lg text-left transition group"
              >
                <div className="flex items-center space-x-3">
                  <div className="p-1.5 bg-slate-950 rounded border border-slate-800">{item.icon}</div>
                  <div>
                    <div className="text-xs font-medium text-slate-200 group-hover:text-slate-100">{item.label}</div>
                    <div className="text-[10px] text-slate-400">{item.desc}</div>
                  </div>
                </div>
                <Plus className="w-3.5 h-3.5 text-slate-500 group-hover:text-slate-300" />
              </button>
            ))}
          </div>
        </div>

        {/* Visual Graph Canvas */}
        <div className="xl:col-span-5 bg-slate-950 border border-slate-800 rounded-xl p-4 flex flex-col relative overflow-hidden bg-grid-pattern">
          <div className="flex items-center justify-between text-xs text-slate-400 mb-4 border-b border-slate-900 pb-2">
            <span>Visual DAG Canvas ({nodes.length} Nodes, {edges.length} Edges)</span>
            <span className="text-[10px] font-mono bg-slate-900 px-2 py-0.5 rounded border border-slate-800">Deterministic Cycle Prevention Active</span>
          </div>

          {/* Node Flow Representation */}
          <div className="flex-1 overflow-auto flex items-center justify-center p-6 space-x-6">
            {nodes.map((n, idx) => (
              <React.Fragment key={n.id}>
                {idx > 0 && <ArrowRight className="w-5 h-5 text-slate-600 shrink-0" />}
                <div
                  onClick={() => handleSelectNode(n)}
                  className={`p-4 rounded-xl border w-48 shadow-lg cursor-pointer transition relative group ${
                    selectedNodeId === n.id
                      ? 'bg-slate-900 border-indigo-500 ring-2 ring-indigo-500/20'
                      : 'bg-slate-900/80 border-slate-800 hover:border-slate-700'
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-[10px] uppercase tracking-wider font-mono font-semibold text-indigo-400">{n.type}</span>
                    <button
                      onClick={(e) => { e.stopPropagation(); handleDeleteNode(n.id); }}
                      className="text-slate-600 hover:text-rose-400 transition"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                  <h3 className="text-xs font-bold text-slate-100">{n.title}</h3>
                  <p className="text-[11px] text-slate-400 mt-1 line-clamp-1">{n.config.description || 'Configured node'}</p>
                </div>
              </React.Fragment>
            ))}
          </div>
        </div>

        {/* Node Configuration & Variable Picker Panel */}
        <div className="xl:col-span-2 bg-slate-900/50 border border-slate-800 rounded-xl p-4 flex flex-col space-y-4 overflow-y-auto">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Node Configuration</h2>

          {selectedNode ? (
            <div className="space-y-3 text-xs">
              <div>
                <label className="block text-slate-400 mb-1">Title</label>
                <input
                  type="text"
                  value={configTitle}
                  onChange={(e) => setConfigTitle(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block text-slate-400 mb-1">Description</label>
                <input
                  type="text"
                  value={configDescription}
                  onChange={(e) => setConfigDescription(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200 focus:outline-none focus:border-indigo-500"
                />
              </div>

              {selectedNode.type === 'tool' && (
                <div>
                  <label className="block text-slate-400 mb-1">Tool Registry Name</label>
                  <select
                    value={configToolName}
                    onChange={(e) => setConfigToolName(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200"
                  >
                    <option value="create_content">create_content</option>
                    <option value="get_calendar_events">get_calendar_events</option>
                    <option value="search_drive_files">search_drive_files</option>
                    <option value="create_mission">create_mission</option>
                  </select>
                </div>
              )}

              <div className="flex items-center space-x-2 pt-2">
                <input
                  type="checkbox"
                  id="approval_chk"
                  checked={configApprovalRequired}
                  onChange={(e) => setConfigApprovalRequired(e.target.checked)}
                  className="rounded border-slate-800 bg-slate-950 text-indigo-500 focus:ring-0"
                />
                <label htmlFor="approval_chk" className="text-slate-300">Require Human Approval</label>
              </div>

              <button
                onClick={handleSaveNodeConfig}
                className="w-full mt-3 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-lg transition"
              >
                Apply Node Settings
              </button>

              {/* Variable Picker Box */}
              <div className="pt-4 border-t border-slate-800 space-y-2">
                <span className="text-[10px] text-slate-400 font-mono block">STRUCTURED VARIABLE PICKER</span>
                <div className="space-y-1">
                  {['event.subject', 'agent.result', 'trigger.sender', 'mission.id'].map((varName) => (
                    <div
                      key={varName}
                      onClick={() => setConfigDescription((prev) => `${prev} {{${varName}}}`)}
                      className="p-1.5 bg-slate-950 border border-slate-800 rounded text-[11px] font-mono text-cyan-400 hover:border-cyan-500/50 cursor-pointer transition"
                    >
                      {`{{${varName}}}`}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center py-12 text-slate-500 text-xs">
              Select a node on the canvas to inspect and modify configuration.
            </div>
          )}
        </div>

        {/* AI Workflow Copilot Assistant Panel */}
        <div className="xl:col-span-3 overflow-hidden flex flex-col">
          <WorkflowCopilot
            workflowId={workflowId}
            selectedNodeId={selectedNodeId}
            onApplyProposal={(newDef) => {
              if (newDef && newDef.nodes) {
                setNodes(newDef.nodes);
                setEdges(newDef.edges || []);
              }
            }}
          />
        </div>
      </div>

      {/* Dry Run Simulation Result Banner */}
      {testResult && (
        <div className={`p-4 rounded-xl border text-xs space-y-1.5 ${
          testResult.simulated && testResult.policy_decision === 'ALLOW'
            ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300'
            : 'bg-amber-500/10 border-amber-500/30 text-amber-300'
        }`}>
          <div className="flex items-center justify-between font-semibold">
            <span>DRY-RUN SIMULATION RESULT: {testResult.policy_decision}</span>
            <span>Evaluated Nodes: {testResult.evaluated_nodes?.length || 0}</span>
          </div>
          <p className="text-[11px] text-slate-300">{testResult.reason}</p>
        </div>
      )}
    </div>
  );
};
