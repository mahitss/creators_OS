'use client';

import React, { useEffect, useRef, useState } from 'react';

interface NodePosition {
  id: string;
  name: string;
  category: string;
  status: string;
  latency: string;
  x: number; // 0 to 1 normalized
  y: number; // 0 to 1 normalized
  active: boolean;
}

interface Edge {
  from: string;
  to: string;
  protocol: string;
  rate: string;
}

const NODES: NodePosition[] = [
  { id: 'data', name: 'DATA INGESTION', category: 'INGEST', status: 'ACTIVE', latency: '12ms', x: 0.12, y: 0.5, active: true },
  { id: 'memory', name: 'CONTEXT VAULT', category: 'STORAGE', status: 'CONNECTED', latency: '18ms', x: 0.32, y: 0.24, active: true },
  { id: 'model', name: 'MODEL ROUTER', category: 'OPENROUTER', status: 'ONLINE', latency: '49ms', x: 0.52, y: 0.18, active: true },
  { id: 'policy', name: 'POLICY ENGINE', category: 'ZERO-TRUST', status: 'ENFORCED', latency: '4ms', x: 0.52, y: 0.76, active: true },
  { id: 'agent', name: 'AGENT RUNTIME', category: 'PARALLEL', status: 'READY', latency: '22ms', x: 0.72, y: 0.32, active: true },
  { id: 'workflow', name: 'EVENT MESH', category: 'REDIS PUB/SUB', status: 'STREAMING', latency: '8ms', x: 0.72, y: 0.68, active: true },
  { id: 'execution', name: 'EXECUTION DAG', category: 'KERNEL', status: 'OPERATIONAL', latency: '14ms', x: 0.90, y: 0.5, active: true },
];

const EDGES: Edge[] = [
  { from: 'data', to: 'memory', protocol: 'OIDC/gRPC', rate: '2.4 GB/s' },
  { from: 'data', to: 'policy', protocol: 'DLP Scan', rate: '1.8 GB/s' },
  { from: 'memory', to: 'model', protocol: 'RAG Embed', rate: '420 req/s' },
  { from: 'policy', to: 'model', protocol: 'ABAC Guard', rate: '1.2k op/s' },
  { from: 'model', to: 'agent', protocol: 'SSE Stream', rate: '86 tok/s' },
  { from: 'policy', to: 'workflow', protocol: 'Audit Sig', rate: '350 msg/s' },
  { from: 'agent', to: 'workflow', protocol: 'State Sync', rate: '48 msg/s' },
  { from: 'agent', to: 'execution', protocol: 'DAG Task', rate: '99.99%' },
  { from: 'workflow', to: 'execution', protocol: 'Commit', rate: '0 lag' },
];

export const NeuralInfrastructureMap: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const containerRef = useRef<HTMLDivElement | null>(null);
  const [selectedNode, setSelectedNode] = useState<string>('model');
  const [hoveredNode, setHoveredNode] = useState<string | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    let ctx: CanvasRenderingContext2D | null = null;
    try {
      ctx = canvas.getContext('2d');
    } catch {
      // jsdom test environment fallback
    }
    if (!ctx) return;

    let animationFrameId: number;
    let isVisible = true;
    let width = container.clientWidth || 800;
    let height = 360;

    const resize = () => {
      if (!canvas || !container) return;
      width = container.clientWidth || 800;
      height = Math.max(300, Math.min(400, Math.floor(width * 0.40)));
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = width * dpr;
      canvas.height = height * dpr;
      canvas.style.width = `${width}px`;
      canvas.style.height = `${height}px`;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };

    resize();
    window.addEventListener('resize', resize);

    const observer = new IntersectionObserver(([entry]) => {
      isVisible = entry.isIntersecting;
    });
    observer.observe(container);

    const packets = EDGES.map((edge, i) => ({
      edge,
      progress: (i * 0.22) % 1,
      speed: 0.003 + (i % 3) * 0.0015,
    }));

    let lastTime = performance.now();

    const render = (currentTime: number) => {
      if (!isVisible) {
        animationFrameId = requestAnimationFrame(render);
        return;
      }

      const delta = (currentTime - lastTime) / 1000;
      lastTime = currentTime;

      ctx.clearRect(0, 0, width, height);

      // Node coordinates calculation
      const coords: Record<string, { x: number; y: number; node: NodePosition }> = {};
      for (const n of NODES) {
        coords[n.id] = {
          x: Math.round(n.x * width),
          y: Math.round(n.y * height),
          node: n,
        };
      }

      // Draw Connection Lines (Subtle Matte)
      for (const edge of EDGES) {
        const from = coords[edge.from];
        const to = coords[edge.to];
        if (!from || !to) continue;

        const isHighlighted =
          hoveredNode === edge.from ||
          hoveredNode === edge.to ||
          selectedNode === edge.from ||
          selectedNode === edge.to;

        ctx.beginPath();
        ctx.moveTo(from.x, from.y);
        ctx.lineTo(to.x, to.y);
        ctx.strokeStyle = isHighlighted ? 'rgba(98, 230, 178, 0.40)' : 'rgba(255, 255, 255, 0.07)';
        ctx.lineWidth = isHighlighted ? 1.5 : 1;
        ctx.stroke();

        // Edge technical protocol label at midpoint
        if (width > 640 && isHighlighted) {
          const midX = (from.x + to.x) / 2;
          const midY = (from.y + to.y) / 2;
          ctx.font = '9px JetBrains Mono, monospace';
          ctx.fillStyle = '#62E6B2';
          ctx.fillText(edge.protocol, midX - 20, midY - 6);
        }
      }

      // Update & Draw Packets
      for (const p of packets) {
        p.progress += p.speed;
        if (p.progress > 1) p.progress = 0;

        const from = coords[p.edge.from];
        const to = coords[p.edge.to];
        if (!from || !to) continue;

        const px = from.x + (to.x - from.x) * p.progress;
        const py = from.y + (to.y - from.y) * p.progress;

        ctx.beginPath();
        ctx.arc(px, py, 2.5, 0, Math.PI * 2);
        ctx.fillStyle = '#62E6B2';
        ctx.fill();

        // Trailing glow line
        ctx.beginPath();
        const trailProgress = Math.max(0, p.progress - 0.08);
        const tx = from.x + (to.x - from.x) * trailProgress;
        const ty = from.y + (to.y - from.y) * trailProgress;
        ctx.moveTo(px, py);
        ctx.lineTo(tx, ty);
        ctx.strokeStyle = 'rgba(98, 230, 178, 0.25)';
        ctx.lineWidth = 1.5;
        ctx.stroke();
      }

      // Draw Nodes
      for (const n of NODES) {
        const c = coords[n.id];
        if (!c) continue;

        const isSelected = selectedNode === n.id;
        const isHovered = hoveredNode === n.id;

        // Outer ring
        ctx.beginPath();
        ctx.arc(c.x, c.y, 16, 0, Math.PI * 2);
        ctx.fillStyle = isSelected ? '#151515' : isHovered ? '#121212' : '#0B0B0B';
        ctx.fill();
        ctx.strokeStyle = isSelected
          ? '#62E6B2'
          : isHovered
          ? 'rgba(255, 255, 255, 0.25)'
          : 'rgba(255, 255, 255, 0.12)';
        ctx.lineWidth = isSelected ? 1.5 : 1;
        ctx.stroke();

        // Center dot
        ctx.beginPath();
        ctx.arc(c.x, c.y, 4, 0, Math.PI * 2);
        ctx.fillStyle = isSelected || isHovered ? '#62E6B2' : '#F5F5F5';
        ctx.fill();

        // Node Typography & Metadata
        ctx.font = '11px Inter, sans-serif';
        ctx.fillStyle = isSelected ? '#F5F5F5' : '#A3A3A3';
        ctx.textAlign = 'center';
        ctx.fillText(n.name, c.x, c.y + 28);

        ctx.font = '9px JetBrains Mono, monospace';
        ctx.fillStyle = isSelected ? '#62E6B2' : '#666666';
        ctx.fillText(`${n.category} • ${n.latency}`, c.x, c.y + 40);
      }

      animationFrameId = requestAnimationFrame(render);
    };

    animationFrameId = requestAnimationFrame(render);

    const handleMouseMove = (e: MouseEvent) => {
      const rect = canvas.getBoundingClientRect();
      const mx = e.clientX - rect.left;
      const my = e.clientY - rect.top;

      let found: string | null = null;
      for (const n of NODES) {
        const nx = n.x * width;
        const ny = n.y * height;
        const dist = Math.hypot(mx - nx, my - ny);
        if (dist < 22) {
          found = n.id;
          break;
        }
      }
      setHoveredNode(found);
      canvas.style.cursor = found ? 'pointer' : 'default';
    };

    const handleClick = (e: MouseEvent) => {
      const rect = canvas.getBoundingClientRect();
      const mx = e.clientX - rect.left;
      const my = e.clientY - rect.top;

      for (const n of NODES) {
        const nx = n.x * width;
        const ny = n.y * height;
        const dist = Math.hypot(mx - nx, my - ny);
        if (dist < 22) {
          setSelectedNode(n.id);
          break;
        }
      }
    };

    canvas.addEventListener('mousemove', handleMouseMove);
    canvas.addEventListener('click', handleClick);

    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener('resize', resize);
      observer.disconnect();
      canvas.removeEventListener('mousemove', handleMouseMove);
      canvas.removeEventListener('click', handleClick);
    };
  }, [selectedNode, hoveredNode]);

  const activeNodeData = NODES.find((n) => n.id === selectedNode) || NODES[2];

  return (
    <div className="w-full flex flex-col gap-3" ref={containerRef}>
      {/* Header Info Strip */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-1">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-[#62E6B2]" />
          <span className="text-xs font-bold text-[#F5F5F5] uppercase tracking-widest font-mono">
            LIVE SYSTEM INFRASTRUCTURE TOPOLOGY
          </span>
        </div>
        <div className="flex items-center gap-3 text-[10px] font-mono text-[#666666]">
          <span>NODES: 7 OPERATIONAL</span>
          <span className="text-[#333333]">•</span>
          <span>MESH LATENCY: 14ms</span>
          <span className="text-[#333333]">•</span>
          <span className="text-[#62E6B2]">PIPELINE ACTIVE</span>
        </div>
      </div>

      {/* Canvas Visualization Container */}
      <div className="relative w-full bg-[#080808] rounded-xl overflow-hidden min-h-[300px] flex items-center justify-center">
        <canvas ref={canvasRef} className="block w-full h-full" />

        {/* Selected Node Telemetry HUD Overlay */}
        <div className="absolute bottom-3 left-3 right-3 sm:right-auto sm:max-w-xs p-3 rounded-lg bg-[#050505] border border-[rgba(255,255,255,0.08)] flex flex-col gap-1.5 shadow-none pointer-events-none">
          <div className="flex items-center justify-between text-[10px] font-mono">
            <span className="text-[#666666]">INSPECTED NODE</span>
            <span className="text-[#62E6B2] font-semibold">{activeNodeData.status}</span>
          </div>
          <div className="text-xs font-bold text-[#F5F5F5] font-mono">{activeNodeData.name}</div>
          <div className="flex items-center justify-between text-[10px] font-mono text-[#A3A3A3] pt-1 border-t border-[rgba(255,255,255,0.06)]">
            <span>DOMAIN: {activeNodeData.category}</span>
            <span>PING: {activeNodeData.latency}</span>
          </div>
        </div>
      </div>
    </div>
  );
};
