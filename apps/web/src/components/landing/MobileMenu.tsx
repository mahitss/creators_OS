'use client';

import React from 'react';
import Link from 'next/link';

interface MobileMenuProps {
  isOpen: boolean;
  onClose: () => void;
}

export function MobileMenu({ isOpen, onClose }: MobileMenuProps) {
  return (
    <nav className="menu" id="menu" aria-hidden={!isOpen}>
      <div className="menu-inner">
        <p className="menu-eyebrow">Menu</p>
        <ul className="menu-list">
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
      <div className="menu-foot">
        <Link href="/login" className="pill" onClick={onClose}>
          <span>Get Started</span>
        </Link>
        <a href="#architecture" className="ghost" onClick={onClose}>
          View Architecture
        </a>
      </div>
    </nav>
  );
}
