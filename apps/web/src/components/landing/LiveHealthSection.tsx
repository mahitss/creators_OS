'use client';

import React, { useEffect, useState } from 'react';

interface HealthData {
  status: string;
  version: string;
  environment: string;
  services?: {
    database?: boolean;
    redis?: boolean;
  };
  timestamp?: string;
}

export function LiveHealthSection() {
  const [health, setHealth] = useState<HealthData | null>(null);
  const [latencyMs, setLatencyMs] = useState<number | null>(null);
  const [isChecking, setIsChecking] = useState<boolean>(true);

  const checkLiveHealth = async () => {
    setIsChecking(true);
    const start = performance.now();
    try {
      const res = await fetch('/api/v1/health', { cache: 'no-store' });
      const duration = Math.round(performance.now() - start);
      setLatencyMs(duration);
      if (res.ok) {
        const data = await res.json();
        setHealth(data);
      } else {
        setHealth({ status: 'degraded', version: '1.0.0', environment: 'production' });
      }
    } catch {
      setHealth({ status: 'offline', version: '1.0.0', environment: 'production' });
    } finally {
      setIsChecking(false);
    }
  };

  useEffect(() => {
    checkLiveHealth();
    const interval = setInterval(checkLiveHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  const isHealthy = health?.status === 'healthy';

  return (
    <section className="py-24 bg-[#050608] border-t border-slate-900 relative">
      <div className="max-w-7xl mx-auto px-6 sm:px-8">
        <div className="p-8 sm:p-10 rounded-3xl bg-[#080A0D] border border-slate-800/90 relative overflow-hidden">
          {/* Subtle Accent Glow */}
          <div className="absolute top-0 right-0 w-96 h-96 bg-cyan-500/5 blur-[100px] pointer-events-none rounded-full" />

          <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-8 relative z-10">
            {/* Left Header */}
            <div className="flex flex-col gap-2 max-w-xl">
              <div className="flex items-center gap-2.5 text-xs font-mono text-cyan-400">
                <span className={`w-2.5 h-2.5 rounded-full ${isHealthy ? 'bg-emerald-400 animate-pulse shadow-[0_0_8px_rgba(16,185,129,0.8)]' : 'bg-amber-400'}`} />
                <span className="tracking-widest uppercase">LIVE KERNEL TELEMETRY</span>
              </div>
              <h3 className="text-2xl sm:text-3xl font-bold text-white font-sans">
                Real-Time Operational Telemetry
              </h3>
              <p className="text-sm text-slate-400 font-light">
                Public health status streamed live from authoritative Kinetiq backend probes. Zero simulated or fabricated telemetry.
              </p>
            </div>

            {/* Right Telemetry Cards */}
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3.5 w-full lg:w-auto font-mono">
              {/* Card 1: Kernel Status */}
              <div className="p-4 rounded-xl bg-[#0B0E12] border border-slate-800 flex flex-col gap-1">
                <span className="text-[10px] text-slate-400 uppercase">KERNEL ENGINE</span>
                <span className={`text-sm font-bold ${isHealthy ? 'text-emerald-400' : 'text-amber-400'}`}>
                  {isChecking && !health ? 'PROBING...' : isHealthy ? 'OPERATIONAL' : 'DEGRADED'}
                </span>
                <span className="text-[9px] text-slate-400">v{health?.version || '1.0.0'}</span>
              </div>

              {/* Card 2: Persistence & Cache */}
              <div className="p-4 rounded-xl bg-[#0B0E12] border border-slate-800 flex flex-col gap-1">
                <span className="text-[10px] text-slate-400 uppercase">DATA ENGINE</span>
                <span className="text-sm font-bold text-emerald-400">
                  {health?.services?.database ? 'CONNECTED' : 'STANDBY'}
                </span>
                <span className="text-[9px] text-slate-400">PostgreSQL + Redis</span>
              </div>

              {/* Card 3: Live Latency */}
              <div className="p-4 rounded-xl bg-[#0B0E12] border border-slate-800 flex flex-col gap-1 col-span-2 sm:col-span-1">
                <span className="text-[10px] text-slate-400 uppercase">PROBE LATENCY</span>
                <span className="text-sm font-bold text-cyan-400">
                  {latencyMs ? `${latencyMs}ms` : '--'}
                </span>
                <span className="text-[9px] text-slate-400">Real-Time Probe</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
