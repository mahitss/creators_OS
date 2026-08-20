'use client';

import React from 'react';
import Link from 'next/link';
import { BrandLogo } from './BrandLogo';

interface TopbarProps {
  isOpen: boolean;
  onToggleMenu: () => void;
}

export function Topbar({ isOpen, onToggleMenu }: TopbarProps) {
  return (
    <header className="topbar">
      {/* Brand S-Bolt Mark */}
      <BrandLogo />

      {/* Primary Navigation Links */}
      <nav className="links" aria-label="Primary">
        <a href="#about">About</a>
        <a href="#features">Features</a>
        <a href="#faq">FAQ</a>
        <a href="#contact">Contact</a>
      </nav>

      {/* Header CTA Pill */}
      <Link href="/login" className="pill pill-nav">
        <span>Get Started</span>
      </Link>

      {/* Mobile Burger Button */}
      <button
        type="button"
        className="burger"
        onClick={onToggleMenu}
        aria-label={isOpen ? 'Close Menu' : 'Open Menu'}
        aria-expanded={isOpen}
        aria-controls="menu"
      >
        <i />
        <i />
      </button>
    </header>
  );
}
