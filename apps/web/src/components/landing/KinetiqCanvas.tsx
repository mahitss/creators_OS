'use client';

import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';

interface TopologyNodeDef {
  id: string;
  name: string;
  code: string;
  pos: [number, number, number];
  type: 'data' | 'model' | 'policy' | 'agent' | 'tool' | 'execution' | 'memory' | 'event';
  color: number;
}

const TOPOLOGY_NODES: TopologyNodeDef[] = [
  { id: 'data', name: 'DATA FABRIC', code: '01_INGEST', pos: [-4.6, 2.2, 1.2], type: 'data', color: 0x9BB7FF },
  { id: 'event', name: 'EVENT BUS', code: '02_STREAM', pos: [-4.8, -1.8, -1.0], type: 'event', color: 0x9BB7FF },
  { id: 'model', name: 'MODEL GATEWAY', code: '03_ROUTER', pos: [-1.6, 3.4, -0.8], type: 'model', color: 0x7CF7C5 },
  { id: 'memory', name: 'KNOWLEDGE VAULT', code: '04_MEMORY', pos: [-1.8, -3.0, 1.4], type: 'memory', color: 0x9BB7FF },
  { id: 'policy', name: 'POLICY ENGINE', code: '05_GUARD', pos: [1.8, 2.6, 0.8], type: 'policy', color: 0x7CF7C5 },
  { id: 'agent', name: 'AGENT RUNTIME', code: '06_WORKER', pos: [4.4, 1.4, -1.2], type: 'agent', color: 0x7CF7C5 },
  { id: 'tool', name: 'TOOL SANDBOX', code: '07_SANDBOX', pos: [2.2, -2.6, -1.4], type: 'tool', color: 0x9BB7FF },
  { id: 'execution', name: 'EXECUTION DAG', code: '08_RUNTIME', pos: [4.8, -1.8, 1.0], type: 'execution', color: 0x7CF7C5 },
];

// Technical pipeline connections
const PIPELINE_EDGES: [string, string][] = [
  ['data', 'model'],
  ['event', 'data'],
  ['event', 'policy'],
  ['model', 'policy'],
  ['memory', 'model'],
  ['memory', 'agent'],
  ['policy', 'agent'],
  ['agent', 'tool'],
  ['agent', 'execution'],
  ['tool', 'execution'],
];

export function KinetiqCanvas() {
  const containerRef = useRef<HTMLDivElement>(null);
  const [hasWebGL, setHasWebGL] = useState<boolean>(true);
  const [isLoaded, setIsLoaded] = useState<boolean>(false);
  const [activeStep, setActiveStep] = useState<string>('model');

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    // Check reduced motion preference safely
    const prefersReducedMotion =
      typeof window !== 'undefined' && typeof window.matchMedia === 'function'
        ? window.matchMedia('(prefers-reduced-motion: reduce)').matches
        : false;

    // WebGL support check
    try {
      const canvas = document.createElement('canvas');
      const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
      if (!gl) {
        setHasWebGL(false);
        return;
      }
    } catch {
      setHasWebGL(false);
      return;
    }

    let animationFrameId: number;
    let isVisible = true;

    // Scene, Camera, Renderer
    const scene = new THREE.Scene();
    const width = container.clientWidth || 600;
    const height = container.clientHeight || 560;

    const camera = new THREE.PerspectiveCamera(38, width / height, 0.1, 1000);
    camera.position.set(0, 0, 19);

    const renderer = new THREE.WebGLRenderer({
      alpha: true,
      antialias: true,
      powerPreference: 'high-performance',
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    container.appendChild(renderer.domElement);
    setIsLoaded(true);

    const rootGroup = new THREE.Group();
    scene.add(rootGroup);

    // ─────────────────────────────────────────────────────────
    // 1. CENTRAL COMPUTATIONAL CORE (Floating Hexagonal / Rectangular Prism)
    // ─────────────────────────────────────────────────────────
    const coreGroup = new THREE.Group();
    rootGroup.add(coreGroup);

    // Core body (Dark graphite prism)
    const coreGeo = new THREE.BoxGeometry(2.4, 1.4, 2.0);
    const coreMat = new THREE.MeshBasicMaterial({
      color: 0x0A0C0F,
      transparent: true,
      opacity: 0.92,
    });
    const coreMesh = new THREE.Mesh(coreGeo, coreMat);
    coreGroup.add(coreMesh);

    // Core metallic wireframe edges
    const coreEdgesGeo = new THREE.EdgesGeometry(coreGeo);
    const coreEdgesMat = new THREE.LineBasicMaterial({
      color: 0x7CF7C5,
      transparent: true,
      opacity: 0.8,
    });
    const coreEdges = new THREE.LineSegments(coreEdgesGeo, coreEdgesMat);
    coreGroup.add(coreEdges);

    // Core internal status beacon
    const beaconGeo = new THREE.BoxGeometry(0.6, 0.12, 0.6);
    const beaconMat = new THREE.MeshBasicMaterial({
      color: 0x7CF7C5,
      transparent: true,
      opacity: 0.95,
    });
    const beaconMesh = new THREE.Mesh(beaconGeo, beaconMat);
    beaconMesh.position.y = 0.72;
    coreGroup.add(beaconMesh);

    // ─────────────────────────────────────────────────────────
    // 2. DISTRIBUTED ASYMMETRIC SYSTEM NODES
    // ─────────────────────────────────────────────────────────
    const nodeMeshes: {
      id: string;
      group: THREE.Group;
      basePos: THREE.Vector3;
      indicatorMat: THREE.MeshBasicMaterial;
      edgesMat: THREE.LineBasicMaterial;
    }[] = [];

    const nodeBoxGeo = new THREE.BoxGeometry(1.1, 0.7, 0.8);
    const nodeBoxEdges = new THREE.EdgesGeometry(nodeBoxGeo);

    TOPOLOGY_NODES.forEach((node) => {
      const nodeGroup = new THREE.Group();
      const pos = new THREE.Vector3(...node.pos);
      nodeGroup.position.copy(pos);

      // Node Body
      const bodyMat = new THREE.MeshBasicMaterial({
        color: 0x0E1117,
        transparent: true,
        opacity: 0.88,
      });
      const bodyMesh = new THREE.Mesh(nodeBoxGeo, bodyMat);
      nodeGroup.add(bodyMesh);

      // Node Metallic Edges
      const edgesMat = new THREE.LineBasicMaterial({
        color: node.color,
        transparent: true,
        opacity: 0.45,
      });
      const edges = new THREE.LineSegments(nodeBoxEdges, edgesMat);
      nodeGroup.add(edges);

      // Indicator Center Pip
      const pipGeo = new THREE.SphereGeometry(0.12, 8, 8);
      const indicatorMat = new THREE.MeshBasicMaterial({
        color: node.color,
        transparent: true,
        opacity: 0.7,
      });
      const pip = new THREE.Mesh(pipGeo, indicatorMat);
      pip.position.set(0, 0, 0.42);
      nodeGroup.add(pip);

      rootGroup.add(nodeGroup);
      nodeMeshes.push({
        id: node.id,
        group: nodeGroup,
        basePos: pos.clone(),
        indicatorMat,
        edgesMat,
      });
    });

    // ─────────────────────────────────────────────────────────
    // 3. PRECISION TECHNICAL CONNECTION LINES
    // ─────────────────────────────────────────────────────────
    const linesMaterial = new THREE.LineBasicMaterial({
      color: 0x9BB7FF,
      transparent: true,
      opacity: 0.28,
    });

    const activeLineMaterial = new THREE.LineBasicMaterial({
      color: 0x7CF7C5,
      transparent: true,
      opacity: 0.85,
    });

    const edgeObjects: {
      source: string;
      target: string;
      line: THREE.Line;
      activeLine: THREE.Line;
    }[] = [];

    PIPELINE_EDGES.forEach(([sourceId, targetId]) => {
      const sourceDef = TOPOLOGY_NODES.find((n) => n.id === sourceId);
      const targetDef = TOPOLOGY_NODES.find((n) => n.id === targetId);
      if (!sourceDef || !targetDef) return;

      const p1 = new THREE.Vector3(...sourceDef.pos);
      const p2 = new THREE.Vector3(...targetDef.pos);

      // Base passive line
      const geo = new THREE.BufferGeometry().setFromPoints([p1, p2]);
      const line = new THREE.Line(geo, linesMaterial);
      rootGroup.add(line);

      // Active pulse line
      const activeGeo = new THREE.BufferGeometry().setFromPoints([p1, p1.clone()]);
      const activeLine = new THREE.Line(activeGeo, activeLineMaterial);
      rootGroup.add(activeLine);

      edgeObjects.push({ source: sourceId, target: targetId, line, activeLine });
    });

    // Connecting core to key pipeline hubs
    const corePos = new THREE.Vector3(0, 0, 0);
    ['model', 'policy', 'agent', 'memory'].forEach((hubId) => {
      const hubDef = TOPOLOGY_NODES.find((n) => n.id === hubId);
      if (!hubDef) return;
      const hubPos = new THREE.Vector3(...hubDef.pos);
      const geo = new THREE.BufferGeometry().setFromPoints([corePos, hubPos]);
      const hubLine = new THREE.Line(
        geo,
        new THREE.LineBasicMaterial({ color: 0x7CF7C5, transparent: true, opacity: 0.2 })
      );
      rootGroup.add(hubLine);
    });

    // ─────────────────────────────────────────────────────────
    // 4. DATA PACKET PULSES (Flowing along pipelines)
    // ─────────────────────────────────────────────────────────
    const packetCount = 6;
    const packetGeo = new THREE.SphereGeometry(0.1, 8, 8);
    const packetMat = new THREE.MeshBasicMaterial({
      color: 0x7CF7C5,
      transparent: true,
      opacity: 0.95,
    });

    const packets: { mesh: THREE.Mesh; edgeIndex: number; progress: number; speed: number }[] = [];
    for (let i = 0; i < packetCount; i++) {
      const mesh = new THREE.Mesh(packetGeo, packetMat);
      mesh.visible = false;
      rootGroup.add(mesh);
      packets.push({
        mesh,
        edgeIndex: i % edgeObjects.length,
        progress: (i / packetCount),
        speed: 0.35 + Math.random() * 0.25,
      });
    }

    // ─────────────────────────────────────────────────────────
    // 5. INTERACTION & RESIZE
    // ─────────────────────────────────────────────────────────
    let mouseX = 0;
    let mouseY = 0;
    let targetX = 0;
    let targetY = 0;

    const onMouseMove = (e: MouseEvent) => {
      if (prefersReducedMotion) return;
      const rect = container.getBoundingClientRect();
      mouseX = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      mouseY = -(((e.clientY - rect.top) / rect.height) * 2 - 1);
    };

    window.addEventListener('mousemove', onMouseMove, { passive: true });

    const onResize = () => {
      if (!container) return;
      const newW = container.clientWidth;
      const newH = container.clientHeight;
      camera.aspect = newW / newH;
      camera.updateProjectionMatrix();
      renderer.setSize(newW, newH);
    };

    window.addEventListener('resize', onResize);

    const observer = new IntersectionObserver(
      (entries) => {
        isVisible = entries[0].isIntersecting;
      },
      { threshold: 0.05 }
    );
    observer.observe(container);

    // ─────────────────────────────────────────────────────────
    // 6. EXECUTION PIPELINE CYCLE ANIMATION
    // ─────────────────────────────────────────────────────────
    const pipelineSequence = ['data', 'model', 'policy', 'agent', 'tool', 'execution'];
    let stepTimer = 0;
    let currentStepIdx = 0;

    const clock = new THREE.Clock();

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);

      if (!isVisible) return;

      const delta = clock.getDelta();
      const time = clock.getElapsedTime();

      // Sequential node activation cycle
      stepTimer += delta;
      if (stepTimer > 1.2) {
        stepTimer = 0;
        currentStepIdx = (currentStepIdx + 1) % pipelineSequence.length;
        const nextActive = pipelineSequence[currentStepIdx];
        setActiveStep(nextActive);
      }

      if (!prefersReducedMotion) {
        // Damped subtle mouse parallax (constrained to 2–3 degrees)
        targetX += (mouseX - targetX) * 0.04;
        targetY += (mouseY - targetY) * 0.04;

        rootGroup.rotation.y = targetX * 0.12;
        rootGroup.rotation.x = -targetY * 0.08;

        // Central Core subtle hover
        coreGroup.position.y = Math.sin(time * 1.2) * 0.08;
        coreGroup.rotation.y = Math.sin(time * 0.5) * 0.06;

        // Core status beacon pulse
        const beaconPulse = 0.6 + Math.sin(time * 3.0) * 0.4;
        beaconMat.opacity = beaconPulse;

        // Node levitation & activation highlight
        nodeMeshes.forEach((nodeObj, idx) => {
          const isActive = pipelineSequence[currentStepIdx] === nodeObj.id;
          const floatOffset = Math.sin(time * 1.4 + idx * 0.8) * 0.06;
          nodeObj.group.position.y = nodeObj.basePos.y + floatOffset;

          if (isActive) {
            nodeObj.indicatorMat.opacity = 1.0;
            nodeObj.edgesMat.opacity = 0.95;
          } else {
            nodeObj.indicatorMat.opacity = 0.45;
            nodeObj.edgesMat.opacity = 0.35;
          }
        });

        // Data packets traversal
        packets.forEach((pkt) => {
          pkt.progress += delta * pkt.speed;
          if (pkt.progress >= 1.0) {
            pkt.progress = 0;
            pkt.edgeIndex = Math.floor(Math.random() * edgeObjects.length);
          }

          const edge = edgeObjects[pkt.edgeIndex];
          if (edge) {
            const srcDef = TOPOLOGY_NODES.find((n) => n.id === edge.source);
            const tgtDef = TOPOLOGY_NODES.find((n) => n.id === edge.target);
            if (srcDef && tgtDef) {
              const p1 = new THREE.Vector3(...srcDef.pos);
              const p2 = new THREE.Vector3(...tgtDef.pos);
              pkt.mesh.position.lerpVectors(p1, p2, pkt.progress);
              pkt.mesh.visible = true;
            }
          }
        });
      }

      renderer.render(scene, camera);
    };

    animate();

    return () => {
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('resize', onResize);
      observer.disconnect();
      cancelAnimationFrame(animationFrameId);
      if (container && renderer.domElement && container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
      coreGeo.dispose();
      coreMat.dispose();
      coreEdgesGeo.dispose();
      coreEdgesMat.dispose();
      beaconGeo.dispose();
      beaconMat.dispose();
      nodeBoxGeo.dispose();
      nodeBoxEdges.dispose();
      linesMaterial.dispose();
      activeLineMaterial.dispose();
      packetGeo.dispose();
      packetMat.dispose();
      renderer.dispose();
    };
  }, []);

  if (!hasWebGL) {
    return (
      <div className="w-full h-full flex items-center justify-center relative p-6">
        <div className="w-full max-w-sm rounded-xl border border-[rgba(255,255,255,0.12)] bg-[#0A0C0F] p-5 font-mono text-xs">
          <div className="flex items-center justify-between pb-3 border-b border-[rgba(255,255,255,0.08)]">
            <span className="text-[#7CF7C5] font-semibold flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-[#7CF7C5]" />
              EXECUTION TOPOLOGY
            </span>
            <span className="text-[rgba(245,247,250,0.4)]">STATIC FALLBACK</span>
          </div>
          <div className="py-4 flex flex-col gap-2 text-[11px] text-[rgba(245,247,250,0.7)]">
            <div className="flex items-center justify-between">
              <span>DATA FABRIC</span>
              <span className="text-[#7CF7C5]">ONLINE</span>
            </div>
            <div className="flex items-center justify-between">
              <span>MODEL GATEWAY</span>
              <span className="text-[#9BB7FF]">ACTIVE</span>
            </div>
            <div className="flex items-center justify-between">
              <span>POLICY ENGINE</span>
              <span className="text-[#7CF7C5]">ENFORCED</span>
            </div>
            <div className="flex items-center justify-between">
              <span>AGENT RUNTIME</span>
              <span className="text-[#7CF7C5]">READY</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full h-full relative flex items-center justify-center">
      {/* 3D WebGL Canvas Viewport */}
      <div
        ref={containerRef}
        className={`w-full h-full min-h-[380px] sm:min-h-[440px] lg:min-h-[500px] relative transition-opacity duration-700 ${
          isLoaded ? 'opacity-100' : 'opacity-0'
        }`}
        aria-hidden="true"
      />

      {/* Crisp Technical Node Annotations */}
      <div className="absolute inset-0 pointer-events-none hidden sm:block">
        <div className="absolute top-6 left-4 px-2.5 py-1 rounded bg-[#0A0C0F]/90 border border-[rgba(255,255,255,0.12)] text-[10px] font-mono text-[#9BB7FF] flex items-center gap-1.5">
          <span className={`w-1.5 h-1.5 rounded-full ${activeStep === 'data' ? 'bg-[#7CF7C5]' : 'bg-[#9BB7FF]'}`} />
          DATA FABRIC // 01_INGEST
        </div>
        <div className="absolute top-4 right-12 px-2.5 py-1 rounded bg-[#0A0C0F]/90 border border-[rgba(255,255,255,0.12)] text-[10px] font-mono text-[#7CF7C5] flex items-center gap-1.5">
          <span className={`w-1.5 h-1.5 rounded-full ${activeStep === 'model' ? 'bg-[#7CF7C5]' : 'bg-[rgba(255,255,255,0.3)]'}`} />
          MODEL GATEWAY // 03_ROUTER
        </div>
        <div className="absolute top-1/2 left-2 -translate-y-1/2 px-2.5 py-1 rounded bg-[#0A0C0F]/90 border border-[rgba(255,255,255,0.12)] text-[10px] font-mono text-[rgba(245,247,250,0.6)] flex items-center gap-1.5">
          <span className="w-1.5 h-1.5 rounded-full bg-[#7CF7C5] animate-pulse" />
          KINETIQ CORE
        </div>
        <div className="absolute bottom-16 right-4 px-2.5 py-1 rounded bg-[#0A0C0F]/90 border border-[rgba(255,255,255,0.12)] text-[10px] font-mono text-[#7CF7C5] flex items-center gap-1.5">
          <span className={`w-1.5 h-1.5 rounded-full ${activeStep === 'execution' ? 'bg-[#7CF7C5]' : 'bg-[rgba(255,255,255,0.3)]'}`} />
          EXECUTION DAG // 08_RUNTIME
        </div>
      </div>
    </div>
  );
}
