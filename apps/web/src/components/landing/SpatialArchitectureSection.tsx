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
    id: 'data',
    name: 'DATA',
    category: 'ENTERPRISE DATA FABRIC',
    code: 'DATA_LAYER_01',
    description: 'Enterprise data lakes, continuous event streams, and operational databases structured for real-time AI ingestion.',
    capabilities: ['Structured & Unstructured Ingestion', 'Tenant-Isolated Storage', 'Streaming Webhooks & Change Feeds', 'Cryptographic Data Protection'],
    techStack: 'PostgreSQL • Redis • Vector Indices',
  },
  {
    id: 'knowledge',
    name: 'KNOWLEDGE',
    category: 'ORGANIZATIONAL MEMORY',
    code: 'KNOWLEDGE_VAULT_02',
    description: 'Context and organizational memory powering decisions. Semantic graphs, document embeddings, and learned workspace insights.',
    capabilities: ['Semantic Vector Search', 'Knowledge Graph Traversal', 'Document Vault Indexing', 'Continuous Experience Learning'],
    techStack: 'pgvector • NetworkX • Semantic Embeddings',
  },
  {
    id: 'models',
    name: 'MODELS',
    category: 'INTELLIGENCE GATEWAY',
    code: 'MODEL_ROUTER_03',
    description: 'Capability-aware AI routing across configured providers. Dynamic OpenRouter integration with automated failover and token accounting.',
    capabilities: ['Multi-Provider Dynamic Routing', 'SSE Token Streaming', 'Circuit Breaker Fallback', 'Real-Time Cost Attribution'],
    techStack: 'OpenRouter API • Model Registry • Streaming SSE',
  },
  {
    id: 'agents',
    name: 'AGENTS',
    category: 'AUTONOMOUS RUNTIME',
    code: 'AGENT_MESH_04',
    description: 'Autonomous execution coordinated through governed agent runtimes. Multi-agent collaboration with structured tool sandboxes.',
    capabilities: ['Goal Decomposition & Planning', 'Tool Sandbox Execution', 'Attention Inbox Escalation', 'Sub-Agent Delegation'],
    techStack: 'LangGraph State • Async Worker • Tool Registry',
  },
  {
    id: 'workflows',
    name: 'WORKFLOWS',
    category: 'EXECUTION PIPELINE',
    code: 'WORKFLOW_ENGINE_05',
    description: 'Stateful DAG and cyclic execution graphs with event triggers. Automates complex business processes with deterministic guarantees.',
    capabilities: ['DAG & Cyclic Graph Runtime', 'Event-Driven Triggers', 'Stateful Retry & Exponential Backoff', 'Step Output Pipeline'],
    techStack: 'Async Task Queues • Webhook Engine • CRON',
  },
  {
    id: 'decisions',
    name: 'DECISIONS',
    category: 'STRATEGIC FORESIGHT',
    code: 'DECISION_ENGINE_06',
    description: 'Strategic foresight, counterfactual learning, and risk simulation. Evaluates scenarios before high-stakes enterprise commitments.',
    capabilities: ['Monte Carlo Simulation', 'Early Warning Indicators', 'Counterfactual Learning Loops', 'Drift Calibration'],
    techStack: 'Probabilistic Modeling • Bayesian Inference',
  },
  {
    id: 'security',
    name: 'SECURITY',
    category: 'ZERO-TRUST BOUNDARY',
    code: 'POLICY_ENGINE_07',
    description: 'Zero-trust boundary attestation and DLP masking. Enforces server-side identity verification, RBAC/ABAC, and immutable audit logs.',
    capabilities: ['Google OIDC Verification', 'Row-Level Tenant Isolation', 'Real-Time DLP Secret Redaction', 'Immutable Audit Trails'],
    techStack: 'JWT HMAC-SHA256 • OIDC • PolicyEngine',
  },
  {
    id: 'operations',
    name: 'OPERATIONS',
    category: 'CONTINUOUS RESILIENCE',
    code: 'RESILIENCE_SENTINEL_08',
    description: 'Continuous observability, RUM telemetry, and circuit breakers. Ensures 99.99% operational continuity under infrastructure stress.',
    capabilities: ['Automated Fail-Fast Breakers', 'Prometheus Metrics Exposition', 'RUM Web Vitals Telemetry', 'Degraded Fallbacks'],
    techStack: 'OpenTelemetry • Prometheus • Circuit State',
  },
];

export function SpatialArchitectureSection() {
  const [activeNodeId, setActiveNodeId] = useState<string>('models');
  const activeNode = SYSTEM_NODES.find(n => n.id === activeNodeId) || SYSTEM_NODES[0];

  return (
    <section id="system" className="relative min-h-[90svh] py-28 lg:py-36 bg-[#0A0C0F] border-t border-[rgba(255,255,255,0.08)]">
      {/* Ambient glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[500px] bg-[#7CF7C5]/5 blur-[160px] pointer-events-none rounded-full" />

      <div className="w-full max-w-[1440px] mx-auto px-5 sm:px-8 lg:px-12 relative z-10">
        {/* Section Header */}
        <div className="max-w-3xl flex flex-col items-start text-left gap-3">
          <div className="inline-flex items-center gap-2 text-xs font-mono text-[#7CF7C5] tracking-widest uppercase">
            <span>[ 02 // SYSTEM VISUALIZATION ]</span>
          </div>
          <h2 className="text-3xl sm:text-5xl font-bold text-[#F5F7FA] tracking-tight font-sans leading-tight">
            ONE SYSTEM. <br />
            MANY INTELLIGENCES.
          </h2>
          <p className="text-[rgba(245,247,250,0.55)] text-base sm:text-lg font-light mt-2 max-w-2xl leading-relaxed">
            An interconnected enterprise nervous system. Select any architectural node to inspect its runtime guarantees and technical capabilities.
          </p>
        </div>

        {/* Interactive Architecture Grid & Inspector Panel */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 mt-14 items-start">
          {/* Left: 8 Interactive Nodes (7 cols) */}
          <div className="lg:col-span-7 grid grid-cols-1 sm:grid-cols-2 gap-3.5">
            {SYSTEM_NODES.map(node => {
              const isActive = node.id === activeNodeId;

              return (
                <button
                  key={node.id}
                  type="button"
                  onMouseEnter={() => setActiveNodeId(node.id)}
                  onClick={() => setActiveNodeId(node.id)}
                  className={`text-left p-5 rounded-2xl border transition-all duration-300 relative overflow-hidden flex flex-col justify-between min-h-[140px] ${
                    isActive
                      ? 'bg-[#12161F] border-[#7CF7C5] shadow-[0_0_25px_rgba(124,247,197,0.15)] ring-1 ring-[#7CF7C5]/40'
                      : 'bg-[#050505] border-[rgba(255,255,255,0.08)] hover:border-[rgba(255,255,255,0.20)] hover:bg-[#080A0D]'
                  }`}
                >
                  {/* Top: Category & Status */}
                  <div className="flex items-center justify-between w-full">
                    <span className="text-[10px] font-mono tracking-wider text-[rgba(245,247,250,0.55)] uppercase">
                      {node.category}
                    </span>
                    <span
                      className={`w-2 h-2 rounded-full transition-all ${
                        isActive ? 'bg-[#7CF7C5] shadow-[0_0_8px_rgba(124,247,197,0.8)] scale-125' : 'bg-slate-700'
                      }`}
                    />
                  </div>

                  {/* Middle: Title & Code */}
                  <div className="my-2">
                    <h3 className={`text-base font-bold font-sans ${isActive ? 'text-[#F5F7FA]' : 'text-slate-200'}`}>
                      {node.name}
                    </h3>
                    <div className="text-[11px] font-mono text-[#9BB7FF] mt-0.5">
                      {node.code}
                    </div>
                  </div>

                  {/* Bottom: Connection status */}
                  <div className="text-[10px] font-mono text-[rgba(245,247,250,0.55)] flex items-center gap-1.5">
                    <span className={isActive ? 'text-[#7CF7C5]' : 'text-slate-500'}>●</span>
                    <span>{isActive ? 'INSPECTING' : 'ONLINE'}</span>
                  </div>
                </button>
              );
            })}
          </div>

          {/* Right: Technical Subsystem Inspector Panel (5 cols) */}
          <div className="lg:col-span-5 p-7 sm:p-8 rounded-2xl bg-[#050505] border border-[rgba(255,255,255,0.10)] shadow-2xl relative flex flex-col gap-6 sticky top-28 backdrop-blur-md">
            {/* Header Badge */}
            <div className="flex items-center justify-between border-b border-[rgba(255,255,255,0.08)] pb-4">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-[#7CF7C5] shadow-[0_0_8px_rgba(124,247,197,0.8)] animate-pulse" />
                <span className="text-xs font-mono tracking-widest text-[#7CF7C5] uppercase">
                  NODE SPECIFICATION
                </span>
              </div>
              <span className="text-[10px] font-mono text-[rgba(245,247,250,0.55)] bg-[#0A0C0F] px-2.5 py-1 rounded border border-[rgba(255,255,255,0.10)]">
                {activeNode.code}
              </span>
            </div>

            {/* Name & Description */}
            <div className="flex flex-col gap-2">
              <h3 className="text-2xl font-bold text-[#F5F7FA] font-sans">
                {activeNode.name}
              </h3>
              <p className="text-sm text-[rgba(245,247,250,0.80)] font-light leading-relaxed">
                {activeNode.description}
              </p>
            </div>

            {/* Verified Capabilities */}
            <div className="flex flex-col gap-2.5 pt-2 border-t border-[rgba(255,255,255,0.08)]">
              <span className="text-[11px] font-mono text-[rgba(245,247,250,0.55)] uppercase tracking-wider">
                CORE CAPABILITIES
              </span>
              <div className="flex flex-col gap-2">
                {activeNode.capabilities.map((cap, idx) => (
                  <div key={idx} className="flex items-center gap-2.5 text-xs text-slate-200">
                    <span className="text-[#7CF7C5] font-mono text-[10px]">▶</span>
                    <span>{cap}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Technical Stack */}
            <div className="pt-3 border-t border-[rgba(255,255,255,0.08)] flex flex-col gap-1.5">
              <span className="text-[10px] font-mono text-[rgba(245,247,250,0.55)] uppercase tracking-wider">
                RUNTIME ENGINE STACK
              </span>
              <div className="text-xs font-mono text-[#7CF7C5] bg-[#0A0C0F] p-3 rounded-lg border border-[rgba(255,255,255,0.08)]">
                {activeNode.techStack}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
