'use client';

import React from 'react';
import Link from 'next/link';
import styles from './landing.module.css';

interface MobileMenuProps {
  isOpen: boolean;
  onClose: () => void;
}

export function MobileMenu({ isOpen, onClose }: MobileMenuProps) {
  return (
    <nav className={styles.menu} id="menu" aria-hidden={!isOpen}>
      <div className={styles.menuInner}>
        <p className={styles.menuEyebrow}>Menu</p>
        <ul className={styles.menuList}>
          <li>
            <a href="#about" onClick={onClose}>About</a>
          </li>
          <li>
            <a href="#features" onClick={onClose}>Features</a>
          </li>
          <li>
            <a href="#faq" onClick={onClose}>FAQ</a>
          </li>
          <li>
            <a href="#contact" onClick={onClose}>Contact</a>
          </li>
        </ul>
      </div>
      <div className={styles.menuFoot}>
        <Link href="/login" className={styles.pill} onClick={onClose}>
          <span>Get Started</span>
        </Link>
        <a href="#architecture" className={styles.ghost} onClick={onClose}>
          View Architecture
        </a>
      </div>
    </nav>
  );
}
