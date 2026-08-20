'use client';

import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';

export function KinetiqCanvas() {
  const containerRef = useRef<HTMLDivElement>(null);
  const [hasWebGL, setHasWebGL] = useState<boolean>(true);
  const [isLoaded, setIsLoaded] = useState<boolean>(false);

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
    const height = container.clientHeight || 600;

    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    camera.position.z = 20;

    const renderer = new THREE.WebGLRenderer({
      alpha: true,
      antialias: true,
      powerPreference: 'high-performance',
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    container.appendChild(renderer.domElement);
    setIsLoaded(true);

    // Group for entire spatial intelligence topology
    const rootGroup = new THREE.Group();
    scene.add(rootGroup);

    // 1. Central Intelligence Core (Layered Wireframe Icosahedron)
    const coreGeo = new THREE.IcosahedronGeometry(2.6, 2);
    const coreMat = new THREE.MeshBasicMaterial({
      color: 0x7CF7C5,
      wireframe: true,
      transparent: true,
      opacity: 0.85,
    });
    const coreMesh = new THREE.Mesh(coreGeo, coreMat);
    rootGroup.add(coreMesh);

    // 2. Inner Nucleus Glow
    const glowGeo = new THREE.SphereGeometry(1.6, 24, 24);
    const glowMat = new THREE.MeshBasicMaterial({
      color: 0x7CF7C5,
      transparent: true,
      opacity: 0.18,
    });
    const glowMesh = new THREE.Mesh(glowGeo, glowMat);
    rootGroup.add(glowMesh);

    // 3. Distributed Computing Octahedron Shell
    const shellGeo = new THREE.OctahedronGeometry(4.4, 1);
    const shellMat = new THREE.MeshBasicMaterial({
      color: 0x9BB7FF,
      wireframe: true,
      transparent: true,
      opacity: 0.35,
    });
    const shellMesh = new THREE.Mesh(shellGeo, shellMat);
    rootGroup.add(shellMesh);

    // 4. Orbital Neural Pathway Rings
    const ringMat1 = new THREE.MeshBasicMaterial({
      color: 0x7CF7C5,
      wireframe: true,
      transparent: true,
      opacity: 0.25,
    });
    const ringGeo1 = new THREE.TorusGeometry(6.6, 0.025, 16, 120);
    const ring1 = new THREE.Mesh(ringGeo1, ringMat1);
    ring1.rotation.x = Math.PI / 3;
    ring1.rotation.y = Math.PI / 6;
    rootGroup.add(ring1);

    const ringMat2 = new THREE.MeshBasicMaterial({
      color: 0x9BB7FF,
      wireframe: true,
      transparent: true,
      opacity: 0.2,
    });
    const ringGeo2 = new THREE.TorusGeometry(8.0, 0.02, 16, 120);
    const ring2 = new THREE.Mesh(ringGeo2, ringMat2);
    ring2.rotation.x = -Math.PI / 4;
    ring2.rotation.y = Math.PI / 4;
    rootGroup.add(ring2);

    // 5. Distributed Topology Nodes & Interconnect Lines
    const nodeCount = 36;
    const nodePositions: THREE.Vector3[] = [];
    const nodeGeometry = new THREE.SphereGeometry(0.12, 8, 8);
    const nodeMaterial = new THREE.MeshBasicMaterial({
      color: 0x7CF7C5,
      transparent: true,
      opacity: 0.9,
    });

    const nodesGroup = new THREE.Group();
    rootGroup.add(nodesGroup);

    for (let i = 0; i < nodeCount; i++) {
      const radius = 3.2 + Math.random() * 5.0;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(Math.random() * 2 - 1);

      const pos = new THREE.Vector3(
        radius * Math.sin(phi) * Math.cos(theta),
        radius * Math.sin(phi) * Math.sin(theta),
        radius * Math.cos(phi)
      );
      nodePositions.push(pos);

      const nodeMesh = new THREE.Mesh(nodeGeometry, nodeMaterial);
      nodeMesh.position.copy(pos);
      nodesGroup.add(nodeMesh);
    }

    // Interconnect lines between nearby nodes
    const lineMaterial = new THREE.LineBasicMaterial({
      color: 0x9BB7FF,
      transparent: true,
      opacity: 0.22,
    });
    const linePositions: number[] = [];

    for (let i = 0; i < nodeCount; i++) {
      for (let j = i + 1; j < nodeCount; j++) {
        const dist = nodePositions[i].distanceTo(nodePositions[j]);
        if (dist < 4.2) {
          linePositions.push(
            nodePositions[i].x, nodePositions[i].y, nodePositions[i].z,
            nodePositions[j].x, nodePositions[j].y, nodePositions[j].z
          );
        }
      }
    }

    const lineGeometry = new THREE.BufferGeometry();
    lineGeometry.setAttribute('position', new THREE.Float32BufferAttribute(linePositions, 3));
    const linesMesh = new THREE.LineSegments(lineGeometry, lineMaterial);
    rootGroup.add(linesMesh);

    // 6. Data Stream Particles (Flowing along neural paths)
    const particleCount = 140;
    const particlePositions = new Float32Array(particleCount * 3);
    const particleColors = new Float32Array(particleCount * 3);

    const mintColor = new THREE.Color(0x7CF7C5);
    const blueColor = new THREE.Color(0x9BB7FF);

    for (let i = 0; i < particleCount; i++) {
      const radius = 2.8 + Math.random() * 6.0;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(Math.random() * 2 - 1);

      particlePositions[i * 3] = radius * Math.sin(phi) * Math.cos(theta);
      particlePositions[i * 3 + 1] = radius * Math.sin(phi) * Math.sin(theta);
      particlePositions[i * 3 + 2] = radius * Math.cos(phi);

      const c = i % 2 === 0 ? mintColor : blueColor;
      particleColors[i * 3] = c.r;
      particleColors[i * 3 + 1] = c.g;
      particleColors[i * 3 + 2] = c.b;
    }

    const particleGeo = new THREE.BufferGeometry();
    particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
    particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));

    const particleMat = new THREE.PointsMaterial({
      size: 0.07,
      vertexColors: true,
      transparent: true,
      opacity: 0.7,
    });
    const particlePoints = new THREE.Points(particleGeo, particleMat);
    rootGroup.add(particlePoints);

    // Mouse Interaction
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

    // Resize Handler
    const onResize = () => {
      if (!container) return;
      const newW = container.clientWidth;
      const newH = container.clientHeight;
      camera.aspect = newW / newH;
      camera.updateProjectionMatrix();
      renderer.setSize(newW, newH);
    };

    window.addEventListener('resize', onResize);

    // Visibility Observer to pause rendering when offscreen
    const observer = new IntersectionObserver(
      (entries) => {
        isVisible = entries[0].isIntersecting;
      },
      { threshold: 0.05 }
    );
    observer.observe(container);

    // Animation Loop
    const clock = new THREE.Clock();

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);

      if (!isVisible) return;

      const delta = clock.getDelta();
      const time = clock.getElapsedTime();

      if (!prefersReducedMotion) {
        targetX += (mouseX - targetX) * 0.04;
        targetY += (mouseY - targetY) * 0.04;

        rootGroup.rotation.y = time * 0.12 + targetX * 0.35;
        rootGroup.rotation.x = Math.sin(time * 0.08) * 0.12 - targetY * 0.25;

        coreMesh.rotation.y += delta * 0.35;
        coreMesh.rotation.z += delta * 0.15;

        shellMesh.rotation.y -= delta * 0.2;
        shellMesh.rotation.x += delta * 0.12;

        ring1.rotation.z += delta * 0.15;
        ring2.rotation.z -= delta * 0.12;

        const pulse = 1.0 + Math.sin(time * 1.8) * 0.05;
        glowMesh.scale.set(pulse, pulse, pulse);

        particlePoints.rotation.y += delta * 0.04;
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
      glowGeo.dispose();
      glowMat.dispose();
      shellGeo.dispose();
      shellMat.dispose();
      ringGeo1.dispose();
      ringMat1.dispose();
      ringGeo2.dispose();
      ringMat2.dispose();
      nodeGeometry.dispose();
      nodeMaterial.dispose();
      lineGeometry.dispose();
      lineMaterial.dispose();
      particleGeo.dispose();
      particleMat.dispose();
      renderer.dispose();
    };
  }, []);

  if (!hasWebGL) {
    return (
      <div className="w-full h-full flex items-center justify-center relative">
        <div className="w-64 h-64 rounded-full border border-[#7CF7C5]/30 flex items-center justify-center relative animate-pulse">
          <div className="w-48 h-48 rounded-full border border-[#9BB7FF]/20 flex items-center justify-center">
            <div className="w-24 h-24 rounded-full bg-gradient-to-tr from-[#7CF7C5]/20 to-[#9BB7FF]/20 blur-md" />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div
      ref={containerRef}
      className={`w-full h-full min-h-[420px] lg:min-h-[580px] relative transition-opacity duration-700 ${
        isLoaded ? 'opacity-100' : 'opacity-0'
      }`}
      aria-hidden="true"
    />
  );
}
