'use client';

import React, { useState, useEffect } from 'react';
import { PlateVideo } from './PlateVideo';
import { Topbar } from './Topbar';
import { MobileMenu } from './MobileMenu';
import { HeroContent } from './HeroContent';
import { PartnerLogos } from './PartnerLogos';

export function LandingExperience() {
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setIsOpen(false);
      }
    };
    const handleResize = () => {
      const aspect = window.innerWidth / window.innerHeight;
      if (aspect > 1.1) {
        setIsOpen(false);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return (
    <div className={`stage ${isOpen ? 'is-open' : ''}`}>
      {/* Background CloudFront Video Plate */}
      <PlateVideo />

      {/* Topbar Navigation */}
      <Topbar isOpen={isOpen} onToggleMenu={() => setIsOpen(!isOpen)} />

      {/* Fullscreen Mobile Menu Overlay */}
      <MobileMenu isOpen={isOpen} onClose={() => setIsOpen(false)} />

      {/* Hero Typography & CTAs */}
      <HeroContent />

      {/* Partner Logos Strip */}
      <PartnerLogos />
    </div>
  );
}
