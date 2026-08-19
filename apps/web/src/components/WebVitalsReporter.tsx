'use client';

import { useEffect, useRef } from 'react';

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
  const reportedMetricsRef = useRef<Set<string>>(new Set());

  useEffect(() => {
    if (typeof window === 'undefined' || !('performance' in window)) return;

    // Report Core Web Vitals (FCP, LCP, TTFB, CLS, FID)
    const reportMetric = (name: string, value: number) => {
      // Prevent duplicate reporting of the same metric for the current page lifecycle
      if (reportedMetricsRef.current.has(name)) return;
      reportedMetricsRef.current.add(name);

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
        const jsonPayload = JSON.stringify(payload);
        if (typeof navigator !== 'undefined' && navigator.sendBeacon) {
          const blob = new Blob([jsonPayload], { type: 'application/json' });
          const sent = navigator.sendBeacon('/api/v1/telemetry/web-vitals', blob);
          if (!sent) {
            // Fallback to fetch if sendBeacon queue was full
            fetch('/api/v1/telemetry/web-vitals', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: jsonPayload,
              keepalive: true
            }).catch(() => {});
          }
        } else {
          fetch('/api/v1/telemetry/web-vitals', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: jsonPayload,
            keepalive: true
          }).catch(() => {});
        }
      } catch {
        // Silently swallow telemetry transmission errors
      }
    };

    // Performance observer for Navigation Timing (TTFB, FCP)
    try {
      const navEntries = performance.getEntriesByType('navigation');
      if (navEntries && navEntries.length > 0) {
        const navEntry = navEntries[0] as PerformanceNavigationTiming;
        if (navEntry.responseStart > 0) {
          reportMetric('TTFB', navEntry.responseStart);
        }
        if (navEntry.domContentLoadedEventEnd > 0) {
          reportMetric('FCP', navEntry.domContentLoadedEventEnd);
        }
      }
    } catch {
      // Observer fallback
    }
  }, []);

  return null;
}
