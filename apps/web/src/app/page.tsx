'use client';

import React from 'react';
import { LandingNavbar } from '../components/landing/LandingNavbar';
import { HeroSection } from '../components/landing/HeroSection';
import { SpatialArchitectureSection } from '../components/landing/SpatialArchitectureSection';
import { IntelligenceSection } from '../components/landing/IntelligenceSection';
import { AgentsAutomationSection } from '../components/landing/AgentsAutomationSection';
import { GovernanceSecuritySection } from '../components/landing/GovernanceSecuritySection';
import { LiveHealthSection } from '../components/landing/LiveHealthSection';
import { FinalCtaSection } from '../components/landing/FinalCtaSection';
import { LandingFooter } from '../components/landing/LandingFooter';

export default function LandingPage() {
  return (
    <main className="min-h-screen bg-[#050505] text-[#F5F7FA] flex flex-col font-sans selection:bg-[#7CF7C5]/30 selection:text-[#7CF7C5] overflow-x-clip antialiased">
      {/* Fixed Technical Navigation */}
      <LandingNavbar />

      {/* 01 — HERO (Autonomous Enterprise System + 3D Intelligence Topology) */}
      <HeroSection />

      {/* 02 — SYSTEM ARCHITECTURE (ONE SYSTEM. MANY INTELLIGENCES.) */}
      <SpatialArchitectureSection />

      {/* 03 — INTELLIGENCE LAYER (INTELLIGENCE THAT UNDERSTANDS CONTEXT.) */}
      <IntelligenceSection />

      {/* 04 — AUTONOMOUS EXECUTION (FROM DECISION TO EXECUTION.) */}
      <AgentsAutomationSection />

      {/* 05 — SECURITY (ZERO-TRUST LATTICE & POLICY ENGINE) */}
      <GovernanceSecuritySection />

      {/* 06 — OPERATING MODEL (SIGNALS → CONTEXT → DECISIONS → EXECUTION → OUTCOMES) */}
      <LiveHealthSection />

      {/* 07 — FINAL CTA (THE OPERATING LAYER FOR INTELLIGENT ENTERPRISES.) */}
      <FinalCtaSection />

      {/* Technical Footer */}
      <LandingFooter />
    </main>
  );
}
