'use client';

import React from 'react';
import Link from 'next/link';

export function HeroContent() {
  return (
    <main className="hero">
      <h1 className="headline">
        <span>The Next Layer</span>
        <span>of Intelligence</span>
      </h1>
      <p className="sub">
        <span>A unified infrastructure platform to help teams build,</span>
        <span>ship, and scale AI systems with confidence.</span>
      </p>
      <div className="actions">
        <Link href="/login" className="pill pill-cta">
          <span>Get Started</span>
        </Link>
        <a href="#architecture" className="ghost">
          View Architecture
        </a>
      </div>
    </main>
  );
}
