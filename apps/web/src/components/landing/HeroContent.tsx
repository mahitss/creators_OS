'use client';

import React from 'react';
import Link from 'next/link';
import styles from './landing.module.css';

export function HeroContent() {
  return (
    <main className={styles.hero}>
      <h1 className={styles.headline}>
        <span>The Next Layer</span>
        <span>of Intelligence</span>
      </h1>
      <p className={styles.sub}>
        <span>A unified infrastructure platform to help teams build,</span>
        <span>ship, and scale AI systems with confidence.</span>
      </p>
      <div className={styles.actions}>
        <Link href="/login" className={`${styles.pill} ${styles.pillCta}`}>
          <span>Get Started</span>
        </Link>
        <a href="#architecture" className={styles.ghost}>
          View Architecture
        </a>
      </div>
    </main>
  );
}
