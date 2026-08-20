'use client';

import React, { useEffect, useState } from 'react';

interface HealthData {
  status?: string;
  version?: string;
  environment?: string;
  services?: {
    database?: boolean;
    redis?: boolean;
  };
}

export function LiveHealthSection() {
  const [health, setHealth] = useState<HealthData | null>(null);
  const [latencyMs, setLatencyMs] = useState<number | null>(null);
  const [isAvailable, setIsAvailable] = useState<boolean | null>(null);

  const checkLiveHealth = async () => {
    const start = performance.now();
    try {
      const res = await fetch('/api/v1/health', { cache: 'no-store' });
      const duration = Math.round(performance.now() - start);
      setLatencyMs(duration);
      if (res.ok) {
        const data = await res.json();
        setHealth(data);
        setIsAvailable(data?.status === 'healthy');
      } else {
        setIsAvailable(false);
      }
    } catch {
      setIsAvailable(false);
    }
  };

  useEffect(() => {
    checkLiveHealth();
    const interval = setInterval(checkLiveHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <section className="relative py-24 lg:py-32 bg-[#0A0C0F] border-t border-[rgba(255,255,255,0.08)]">
      <div className="w-full max-w-[1440px] mx-auto px-5 sm:px-8 lg:px-12">
        <div className="p-8 sm:p-10 rounded-3xl bg-[#050505] border border-[rgba(255,255,255,0.10)] relative overflow-hidden">
          {/* Subtle Accent Glow */}
          <div className="absolute top-0 right-0 w-96 h-96 bg-[#7CF7C5]/5 blur-[100px] pointer-events-none rounded-full" />

          <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-8 relative z-10">
            {/* Left Header */}
            <div className="flex flex-col items-start text-left gap-2 max-w-xl">
              <div className="flex items-center gap-2.5 text-xs font-mono text-[#7CF7C5]">
                <span
                  className={`w-2.5 h-2.5 rounded-full ${
                    isAvailable === true
                      ? 'bg-[#7CF7C5] animate-pulse shadow-[0_0_8px_rgba(124,247,197,0.8)]'
                      : isAvailable === false
                      ? 'bg-rose-400'
                      : 'bg-amber-400'
                  }`}
                />
                <span className="tracking-widest uppercase">[ 06 // LIVE SYSTEM STATUS ]</span>
              </div>
              <h3 className="text-2xl sm:text-3xl font-bold text-[#F5F7FA] font-sans">
                Real-Time Operational Telemetry
              </h3>
              <p className="text-sm text-[rgba(245,247,250,0.55)] font-light">
                {isAvailable === true
                  ? 'Live telemetry retrieved from authoritative backend health probes. Zero synthetic data.'
                  : isAvailable === false
                  ? 'Live system telemetry is currently unavailable. No synthetic operational metrics are displayed.'
                  : 'Probing live backend health endpoint...'}
              </p>
            </div>

            {/* Right Telemetry Cards */}
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3.5 w-full lg:w-auto font-mono">
              {/* Card 1: Kernel Status */}
              <div className="p-4 rounded-xl bg-[#0A0C0F] border border-[rgba(255,255,255,0.08)] flex flex-col gap-1">
                <span className="text-[10px] text-[rgba(245,247,250,0.55)] uppercase">KERNEL STATUS</span>
                <span
                  className={`text-sm font-bold ${
                    isAvailable === true
                      ? 'text-[#7CF7C5]'
                      : isAvailable === false
                      ? 'text-rose-400'
                      : 'text-amber-400'
                  }`}
                >
                  {isAvailable === true ? 'OPERATIONAL' : isAvailable === false ? 'UNAVAILABLE' : 'PROBING...'}
                </span>
                <span className="text-[9px] text-[rgba(245,247,250,0.40)]">
                  {health?.version ? `v${health.version}` : 'Authoritative Probe'}
                </span>
              </div>

              {/* Card 2: Persistence & Cache */}
              <div className="p-4 rounded-xl bg-[#0A0C0F] border border-[rgba(255,255,255,0.08)] flex flex-col gap-1">
                <span className="text-[10px] text-[rgba(245,247,250,0.55)] uppercase">PERSISTENCE</span>
                <span className="text-sm font-bold text-[#F5F7FA]">
                  {isAvailable === true && health?.services?.database ? 'CONNECTED' : isAvailable === true ? 'STANDBY' : 'UNAVAILABLE'}
                </span>
                <span className="text-[9px] text-[rgba(245,247,250,0.40)]">PostgreSQL & Redis</span>
              </div>

              {/* Card 3: Live Latency */}
              <div className="p-4 rounded-xl bg-[#0A0C0F] border border-[rgba(255,255,255,0.08)] flex flex-col gap-1 col-span-2 sm:col-span-1">
                <span className="text-[10px] text-[rgba(245,247,250,0.55)] uppercase">PROBE LATENCY</span>
                <span className="text-sm font-bold text-[#9BB7FF]">
                  {latencyMs !== null ? `${latencyMs}ms` : '--'}
                </span>
                <span className="text-[9px] text-[rgba(245,247,250,0.40)]">Real-Time Probe</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
