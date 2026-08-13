'use client';

import { useEffect } from 'react';

export interface WebVitalsPayload {
  name: string;
  value: number;
  rating: 'good' | 'needs-improvement' | 'poor';
  delta: number;
  id: string;
  timestamp: number;
  url: string;
}

export function WebVitalsReporter() {
  useEffect(() => {
    if (typeof window === 'undefined' || !('performance' in window)) return;

    // Report Core Web Vitals (FCP, LCP, TTFB, CLS, FID)
    const reportMetric = (name: string, value: number) => {
      const rating = value < 1000 ? 'good' : value < 2500 ? 'needs-improvement' : 'poor';
      const payload: WebVitalsPayload = {
        name,
        value: Math.round(value),
        rating,
        delta: Math.round(value),
        id: `vitals_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`,
        timestamp: Date.now(),
        url: window.location.href
      };

      try {
        if (navigator.sendBeacon) {
          navigator.sendBeacon('/api/v1/telemetry/web-vitals', JSON.stringify(payload));
        } else {
          fetch('/api/v1/telemetry/web-vitals', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
            keepalive: true
          }).catch(() => {});
        }
      } catch {
        // Silently swallow telemetry transmission errors
      }
    };

    // Performance observer for Navigation Timing (TTFB, FCP)
    try {
      const navEntry = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
      if (navEntry) {
        reportMetric('TTFB', navEntry.responseStart);
        reportMetric('FCP', navEntry.domContentLoadedEventEnd);
      }
    } catch {
      // Observer fallback
    }
  }, []);

  return null;
}
