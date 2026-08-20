'use client';

import React from 'react';
import Link from 'next/link';

export function BrandLogo() {
  return (
    <Link href="/" className="brand" aria-label="Home">
      <svg viewBox="0 0 31.5 48.5" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="bg1" x1="8" y1="0" x2="34.1" y2="28.9" gradientUnits="userSpaceOnUse">
            <stop offset="0" stopColor="#9e9e9e" />
            <stop offset="0.28" stopColor="#a6a6a6" />
            <stop offset="0.34" stopColor="#a3a3a3" />
            <stop offset="0.40" stopColor="#3a3a3a" />
            <stop offset="0.55" stopColor="#414141" />
            <stop offset="0.60" stopColor="#7a7a7a" />
            <stop offset="0.68" stopColor="#8e8e8e" />
            <stop offset="0.80" stopColor="#a9a9a9" />
            <stop offset="0.95" stopColor="#c4c4c4" />
            <stop offset="1" stopColor="#cccccc" />
          </linearGradient>
        </defs>
        <path
          d="M21.5 0 L21.5 19.5 L31.5 19.5 L31.5 29 L10 48.5 L10 28.5 L0.5 28.5 L0.5 18.5 Z"
          fill="url(#bg1)"
        />
        <rect x="0.5" y="18.5" width="9" height="10" fill="#fdfdfd" />
        <rect x="22" y="19.5" width="9.5" height="9.5" fill="#fdfdfd" />
      </svg>
    </Link>
  );
}
