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
    camera.position.z = 18;

    const renderer = new THREE.WebGLRenderer({
      alpha: true,
      antialias: true,
      powerPreference: 'high-performance'
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.2;

    container.appendChild(renderer.domElement);
    setIsLoaded(true);

    // Group for entire spatial core
    const coreGroup = new THREE.Group();
    scene.add(coreGroup);

    // 1. Central Luminous Nucleus (Inner Icosahedron)
    const nucleusGeo = new THREE.IcosahedronGeometry(2.4, 2);
    const nucleusMat = new THREE.MeshBasicMaterial({
      color: 0x00F0FF,
      wireframe: true,
      transparent: true,
      opacity: 0.85
    });
    const nucleusMesh = new THREE.Mesh(nucleusGeo, nucleusMat);
    coreGroup.add(nucleusMesh);

    // 2. Inner Glow Sphere
    const glowGeo = new THREE.SphereGeometry(1.6, 32, 32);
    const glowMat = new THREE.MeshBasicMaterial({
      color: 0x00E599,
      transparent: true,
      opacity: 0.25
    });
    const glowMesh = new THREE.Mesh(glowGeo, glowMat);
    coreGroup.add(glowMesh);

    // 3. Middle Structural Octahedron
    const octGeo = new THREE.OctahedronGeometry(4.2, 1);
    const octMat = new THREE.MeshBasicMaterial({
      color: 0x3B82F6,
      wireframe: true,
      transparent: true,
      opacity: 0.4
    });
    const octMesh = new THREE.Mesh(octGeo, octMat);
    coreGroup.add(octMesh);

    // 4. Outer Orbital Kinetic Rings
    const ringMat1 = new THREE.MeshBasicMaterial({
      color: 0x00F0FF,
      wireframe: true,
      transparent: true,
      opacity: 0.3
    });
    const ringGeo1 = new THREE.TorusGeometry(6.2, 0.03, 16, 100);
    const ring1 = new THREE.Mesh(ringGeo1, ringMat1);
    ring1.rotation.x = Math.PI / 3;
    ring1.rotation.y = Math.PI / 6;
    coreGroup.add(ring1);

    const ringMat2 = new THREE.MeshBasicMaterial({
      color: 0x00E599,
      wireframe: true,
      transparent: true,
      opacity: 0.25
    });
    const ringGeo2 = new THREE.TorusGeometry(7.5, 0.025, 16, 100);
    const ring2 = new THREE.Mesh(ringGeo2, ringMat2);
    ring2.rotation.x = -Math.PI / 4;
    ring2.rotation.y = Math.PI / 4;
    coreGroup.add(ring2);

    // 5. Data Particles Swarm
    const particleCount = 180;
    const particlePositions = new Float32Array(particleCount * 3);
    const particleColors = new Float32Array(particleCount * 3);

    const cyan = new THREE.Color(0x00F0FF);
    const emerald = new THREE.Color(0x00E599);
    const blue = new THREE.Color(0x3B82F6);

    for (let i = 0; i < particleCount; i++) {
      const radius = 3.0 + Math.random() * 6.5;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos((Math.random() * 2) - 1);

      particlePositions[i * 3] = radius * Math.sin(phi) * Math.cos(theta);
      particlePositions[i * 3 + 1] = radius * Math.sin(phi) * Math.sin(theta);
      particlePositions[i * 3 + 2] = radius * Math.cos(phi);

      const color = i % 3 === 0 ? cyan : i % 3 === 1 ? emerald : blue;
      particleColors[i * 3] = color.r;
      particleColors[i * 3 + 1] = color.g;
      particleColors[i * 3 + 2] = color.b;
    }

    const particleGeo = new THREE.BufferGeometry();
    particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
    particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));

    const particleMat = new THREE.PointsMaterial({
      size: 0.08,
      vertexColors: true,
      transparent: true,
      opacity: 0.75
    });
    const particlePoints = new THREE.Points(particleGeo, particleMat);
    coreGroup.add(particlePoints);

    // Mouse Parallax Interaction
    let mouseX = 0;
    let mouseY = 0;
    let targetX = 0;
    let targetY = 0;

    const onMouseMove = (e: MouseEvent) => {
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
    let clock = new THREE.Clock();

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);

      if (!isVisible) return;

      const delta = clock.getDelta();
      const time = clock.getElapsedTime();

      // Smooth mouse follow
      targetX += (mouseX - targetX) * 0.04;
      targetY += (mouseY - targetY) * 0.04;

      coreGroup.rotation.y = time * 0.15 + targetX * 0.4;
      coreGroup.rotation.x = Math.sin(time * 0.1) * 0.15 - targetY * 0.3;

      nucleusMesh.rotation.y += delta * 0.4;
      nucleusMesh.rotation.z += delta * 0.2;

      octMesh.rotation.y -= delta * 0.25;
      octMesh.rotation.x += delta * 0.15;

      ring1.rotation.z += delta * 0.2;
      ring2.rotation.z -= delta * 0.15;

      // Pulsate nucleus glow
      const pulse = 1.0 + Math.sin(time * 2.0) * 0.06;
      glowMesh.scale.set(pulse, pulse, pulse);

      // Rotate particle cloud
      particlePoints.rotation.y += delta * 0.05;

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
      renderer.dispose();
    };
  }, []);

  if (!hasWebGL) {
    return (
      <div className="w-full h-full flex items-center justify-center relative">
        <div className="w-64 h-64 rounded-full border border-cyan-500/30 flex items-center justify-center relative animate-pulse">
          <div className="w-48 h-48 rounded-full border border-emerald-500/20 flex items-center justify-center">
            <div className="w-24 h-24 rounded-full bg-gradient-to-tr from-cyan-500/20 to-emerald-500/20 blur-md" />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div
      ref={containerRef}
      className={`w-full h-full min-h-[420px] lg:min-h-[560px] relative transition-opacity duration-700 ${
        isLoaded ? 'opacity-100' : 'opacity-0'
      }`}
      aria-hidden="true"
    />
  );
}
