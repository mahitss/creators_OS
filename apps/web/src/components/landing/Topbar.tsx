'use client';

import React from 'react';
import Link from 'next/link';
import { BrandLogo } from './BrandLogo';
import styles from './landing.module.css';

interface TopbarProps {
  isOpen: boolean;
  onToggleMenu: () => void;
}

export function Topbar({ isOpen, onToggleMenu }: TopbarProps) {
  return (
    <header className={styles.topbar}>
      {/* Brand S-Bolt Mark */}
      <BrandLogo />

      {/* Primary Navigation Links */}
      <nav className={styles.links} aria-label="Primary">
        <a href="#about">About</a>
        <a href="#features">Features</a>
        <a href="#faq">FAQ</a>
        <a href="#contact">Contact</a>
      </nav>

      {/* Header CTA Pill */}
      <Link href="/login" className={`${styles.pill} ${styles.pillNav}`}>
        <span>Get Started</span>
      </Link>

      {/* Mobile Burger Button */}
      <button
        type="button"
        className={styles.burger}
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
