'use client';

import React, { useState } from 'react';

interface SystemNode {
  id: string;
  name: string;
  category: string;
  code: string;
  description: string;
  capabilities: string[];
  techStack: string;
}

const SYSTEM_NODES: SystemNode[] = [
  {
    id: 'core',
    name: 'Kinetiq Core Kernel',
    category: 'CENTRAL OPERATING SYSTEM',
    code: 'CORE_KERNEL_01',
    description: 'Central state machine and authoritative coordination layer governing all tenant contexts, agents, and execution graphs.',
    capabilities: ['Multi-tenant Isolation', 'Authoritative Auth Context', 'Event Bus & SSE Streaming', 'State Machine Transitions'],
    techStack: 'FastAPI • SQLAlchemy Async • Redis • PostgreSQL'
  },
  {
    id: 'gateway',
    name: 'Model Gateway',
    category: 'INTELLIGENCE INFRASTRUCTURE',
    code: 'AI_GATEWAY_ROUTER',
    description: 'Cryptographically managed OpenRouter integration with automated multi-provider failover, token accounting, and streaming tool calls.',
    capabilities: ['Dynamic Model Routing', 'Streaming SSE Output', 'Deterministic Fallback', 'Token & Cost Attribution'],
    techStack: 'OpenRouter API • Circuit Breaker • AES-256'
  },
  {
    id: 'agents',
    name: 'Agent Runtime Mesh',
    category: 'AUTONOMOUS EXECUTION',
    code: 'AGENT_RUNTIME_MESH',
    description: 'Deterministic multi-agent execution framework with structured tool registries, goal decomposition, and step-by-step verification.',
    capabilities: ['Autonomous Mission Planning', 'Tool Execution Sandboxing', 'Human-in-the-Loop Pausing', 'Sub-Agent Delegation'],
    techStack: 'LangGraph State • Async Worker • Tool Registry'
  },
  {
    id: 'workflows',
    name: 'Workflow Orchestration Engine',
    category: 'CONTINUOUS OPERATIONS',
    code: 'WORKFLOW_ENGINE_V2',
    description: 'Cyclic and acyclic workflow graphs automating complex enterprise processes with event triggers and scheduled cron executions.',
    capabilities: ['DAG & Cyclic Graph Execution', 'Webhook Event Triggers', 'Stateful Retry Logic', 'Step Output Passing'],
    techStack: 'Async Task Queues • Webhook Engine • CRON'
  },
  {
    id: 'memory',
    name: 'Context & Knowledge Graph',
    category: 'DATA & ONTOLOGY',
    code: 'SEMANTIC_GRAPH_VAULT',
    description: 'Vector embeddings, structured document vaults, and semantic relationship graphs for enterprise memory retrieval.',
    capabilities: ['Vector Semantic Search', 'Cycle-Detected Knowledge Graphs', 'Document Embeddings', 'Tenant-Isolated Vaults'],
    techStack: 'pgvector • NetworkX • Semantic Embeddings'
  },
  {
    id: 'decisions',
    name: 'Decision Intelligence',
    category: 'STRATEGIC PREDICTION',
    code: 'DECISION_LEARNING_ENGINE',
    description: 'Monte Carlo simulations, strategic foresight analysis, and counterfactual learning loops for high-stakes enterprise decisions.',
    capabilities: ['Multi-scenario Simulation', 'Early Warning Indicators', 'Counterfactual Learning', 'Drift Calibration'],
    techStack: 'Probabilistic Modeling • Bayesian Inference'
  },
  {
    id: 'governance',
    name: 'Zero-Trust Policy Engine',
    category: 'SECURITY & COMPLIANCE',
    code: 'POLICY_GOVERNANCE_GATE',
    description: 'Real-time RBAC and ABAC policy enforcement, DLP secret masking, and immutable append-only audit trails.',
    capabilities: ['RBAC / ABAC Rule Evaluation', 'DLP Secret Redaction', 'Immutable Audit Logs', 'SCIM 2.0 Identity Sync'],
    techStack: 'JWT HMAC-SHA256 • OIDC • DLP Engine'
  },
  {
    id: 'resilience',
    name: 'Resilience Sentinel',
    category: 'HIGH AVAILABILITY',
    code: 'CIRCUIT_BREAKER_SENTINEL',
    description: 'Autonomous health probes, distributed circuit breakers, and graceful degradation ensuring 99.99% operational continuity.',
    capabilities: ['Automated Fail-Fast Breakers', 'Prometheus Metrics Exposition', 'RUM Web Vitals Telemetry', 'Degraded Fallbacks'],
    techStack: 'OpenTelemetry • Prometheus • Circuit State'
  }
];

export function SpatialArchitectureSection() {
  const [activeNodeId, setActiveNodeId] = useState<string>('core');
  const activeNode = SYSTEM_NODES.find((n) => n.id === activeNodeId) || SYSTEM_NODES[0];

  return (
    <section id="architecture" className="py-28 bg-[#050608] relative overflow-hidden">
      {/* Ambient background glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[600px] bg-cyan-500/5 blur-[160px] pointer-events-none rounded-full" />

      <div className="max-w-7xl mx-auto px-6 sm:px-8 relative z-10">
        {/* Section Header */}
        <div className="max-w-3xl flex flex-col gap-4">
          <div className="inline-flex items-center gap-2 text-xs font-mono text-cyan-400 tracking-widest uppercase">
            <span>[ 02 // SPATIAL ARCHITECTURE ]</span>
          </div>
          <h2 className="text-3xl sm:text-5xl font-bold text-white tracking-tight">
            An Interconnected Operating Architecture.
          </h2>
          <p className="text-slate-400 text-base sm:text-lg font-light">
            Hover over any architectural node to inspect its internal subsystems, cryptographic boundaries, and capabilities.
          </p>
        </div>

        {/* Interactive Spatial Grid & Detail Panel */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 mt-16 items-start">
          {/* Left: Interactive Node Matrix (7 cols) */}
          <div className="lg:col-span-7 grid grid-cols-1 sm:grid-cols-2 gap-3.5">
            {SYSTEM_NODES.map((node) => {
              const isActive = node.id === activeNodeId;
              const isCore = node.id === 'core';

              return (
                <button
                  key={node.id}
                  type="button"
                  onMouseEnter={() => setActiveNodeId(node.id)}
                  onClick={() => setActiveNodeId(node.id)}
                  className={`text-left p-5 rounded-2xl border transition-all duration-300 relative overflow-hidden flex flex-col justify-between min-h-[140px] ${
                    isActive
                      ? isCore
                        ? 'bg-[#0E1522] border-cyan-400 shadow-[0_0_30px_rgba(0,240,255,0.2)] ring-1 ring-cyan-400/50'
                        : 'bg-[#0E1522] border-cyan-500/80 shadow-[0_0_20px_rgba(0,240,255,0.15)]'
                      : 'bg-[#080A0D] border-slate-800/80 hover:border-slate-700 hover:bg-[#0B0E12]'
                  }`}
                >
                  {/* Top: Category & Status */}
                  <div className="flex items-center justify-between w-full">
                    <span className="text-[10px] font-mono tracking-wider text-slate-400 uppercase">
                      {node.category}
                    </span>
                    <span
                      className={`w-2 h-2 rounded-full transition-all ${
                        isActive ? 'bg-cyan-400 shadow-[0_0_8px_rgba(0,240,255,0.8)] scale-125' : 'bg-slate-700'
                      }`}
                    />
                  </div>

                  {/* Middle: Title */}
                  <div className="my-2">
                    <h3 className={`text-base font-bold font-sans ${isActive ? 'text-white' : 'text-slate-200'}`}>
                      {node.name}
                    </h3>
                    <div className="text-[11px] font-mono text-cyan-400/80 mt-0.5">
                      {node.code}
                    </div>
                  </div>

                  {/* Bottom: Connection status */}
                  <div className="text-[10px] font-mono text-slate-400 flex items-center gap-1.5">
                    <span className={isActive ? 'text-emerald-400' : 'text-slate-400'}>●</span>
                    <span>{isActive ? 'INSPECTING' : 'ONLINE'}</span>
                  </div>
                </button>
              );
            })}
          </div>

          {/* Right: Technical Subsystem Inspector Panel (5 cols) */}
          <div className="lg:col-span-5 p-8 rounded-2xl bg-[#080A0D] border border-cyan-500/30 shadow-2xl relative flex flex-col gap-6 sticky top-28 backdrop-blur-md">
            {/* Header Badge */}
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-cyan-400 shadow-[0_0_8px_rgba(0,240,255,0.8)] animate-pulse" />
                <span className="text-xs font-mono tracking-widest text-cyan-300 uppercase">
                  NODE SPECIFICATION
                </span>
              </div>
              <span className="text-[10px] font-mono text-slate-400 bg-slate-900 px-2 py-1 rounded border border-slate-800">
                {activeNode.code}
              </span>
            </div>

            {/* Name & Description */}
            <div className="flex flex-col gap-2">
              <h3 className="text-2xl font-bold text-white font-sans">
                {activeNode.name}
              </h3>
              <p className="text-sm text-slate-300 font-light leading-relaxed">
                {activeNode.description}
              </p>
            </div>

            {/* Verified Capabilities */}
            <div className="flex flex-col gap-2.5 pt-2 border-t border-slate-800/80">
              <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">
                CORE CAPABILITIES
              </span>
              <div className="flex flex-col gap-2">
                {activeNode.capabilities.map((cap, idx) => (
                  <div key={idx} className="flex items-center gap-2.5 text-xs text-slate-200">
                    <span className="text-cyan-400 font-mono text-[10px]">▶</span>
                    <span>{cap}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Technical Stack */}
            <div className="pt-3 border-t border-slate-800/80 flex flex-col gap-1.5">
              <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">
                UNDERLYING KERNEL STACK
              </span>
              <div className="text-xs font-mono text-emerald-400 bg-[#050608] p-3 rounded-lg border border-slate-800/80">
                {activeNode.techStack}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
