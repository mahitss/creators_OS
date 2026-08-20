'use client';

import React from 'react';
import { LandingNavbar } from '../components/landing/LandingNavbar';
import { HeroSection } from '../components/landing/HeroSection';
import { PositioningSection } from '../components/landing/PositioningSection';
import { SpatialArchitectureSection } from '../components/landing/SpatialArchitectureSection';
import { IntelligenceSection } from '../components/landing/IntelligenceSection';
import { AgentsAutomationSection } from '../components/landing/AgentsAutomationSection';
import { GovernanceSecuritySection } from '../components/landing/GovernanceSecuritySection';
import { LiveHealthSection } from '../components/landing/LiveHealthSection';
import { FinalCtaSection } from '../components/landing/FinalCtaSection';
import { LandingFooter } from '../components/landing/LandingFooter';

export default function LandingPage() {
  return (
    <main className="min-h-screen bg-[#050608] text-slate-100 flex flex-col font-sans selection:bg-cyan-500/30 selection:text-cyan-200 overflow-x-hidden antialiased">
      {/* Public Landing Navigation */}
      <LandingNavbar />

      {/* 01 Hero Section with 3D Spatial Core */}
      <HeroSection />

      {/* 02 Positioning & What Kinetiq Is */}
      <PositioningSection />

      {/* 03 Interactive Spatial Architecture */}
      <SpatialArchitectureSection />

      {/* 04 Intelligence & Model Gateway */}
      <IntelligenceSection />

      {/* 05 Autonomous Agents & Workflows */}
      <AgentsAutomationSection />

      {/* 06 Zero-Trust Governance & Security */}
      <GovernanceSecuritySection />

      {/* 07 Live Kernel Telemetry */}
      <LiveHealthSection />

      {/* 08 Final Call to Action */}
      <FinalCtaSection />

      {/* 09 Minimalist Footer */}
      <LandingFooter />
    </main>
  );
}
