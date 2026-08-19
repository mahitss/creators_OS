'use client';

import React, { useState, useEffect, useCallback } from 'react';
import Link from 'next/link';
import { AppShell } from '../components/shell/AppShell';
import { fetchExecutiveBrief, ExecutiveBriefResponse } from '../lib/api/home';
import { ExecutiveGreeting } from '../components/home/ExecutiveGreeting';
import { ExecutiveSummaryCard } from '../components/home/ExecutiveSummaryCard';
import { NeedsAttention } from '../components/home/NeedsAttention';
import { PrimaryRecommendation } from '../components/home/PrimaryRecommendation';
import { LearnedMemoriesSection } from '../components/home/LearnedMemoriesSection';
import { RecentActivity } from '../components/home/RecentActivity';
import { QuickActions } from '../components/home/QuickActions';
import { QuietHomeState } from '../components/home/QuietHomeState';
import { HomeSkeleton } from '../components/home/HomeSkeleton';
import { HomeErrorState } from '../components/home/HomeErrorState';
import { Card, Typography } from '@vapor/ui';

export default function Home() {
  const [data, setData] = useState<ExecutiveBriefResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isError, setIsError] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string>('');

  const loadBrief = useCallback(async () => {
    setIsLoading(true);
    setIsError(false);
    try {
      let userName = 'Alex';
      try {
        const meRes = await fetch('/api/v1/auth/me', { credentials: 'include' });
        if (meRes.ok) {
          const meData = await meRes.json();
          if (meData?.name) {
            userName = meData.name;
          }
        }
      } catch {
        // Fall back to default brief query
      }

      const result = await fetchExecutiveBrief(userName);
      setData(result);
    } catch (err: any) {
      setIsError(true);
      setErrorMessage(err?.message || 'Something went wrong loading your brief.');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadBrief();
  }, [loadBrief]);

  return (
    <AppShell>
      {isLoading ? (
        <HomeSkeleton />
      ) : isError || !data ? (
        <HomeErrorState message={errorMessage} onRetry={loadBrief} />
      ) : (
        <div className="w-full flex flex-col gap-6 animate-in fade-in duration-300">
          {/* Top Hero Command Header */}
          <ExecutiveGreeting
            greeting={data.greeting}
            summaryStatement={data.summary_statement}
          />

          {/* Operational KPI Metric Strip */}
          <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-5 gap-3">
            <div className="p-3.5 rounded-xl bg-[#121520] border border-slate-800/80 flex flex-col gap-1 shadow-sm">
              <div className="flex items-center justify-between text-[11px] font-mono text-slate-400">
                <span>SYSTEM STATUS</span>
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              </div>
              <div className="text-base sm:text-lg font-bold text-emerald-400 font-sans">OPERATIONAL</div>
              <div className="text-[10px] font-mono text-slate-400">Neon DB & Redis Active</div>
            </div>

            <div className="p-3.5 rounded-xl bg-[#121520] border border-slate-800/80 flex flex-col gap-1 shadow-sm">
              <div className="flex items-center justify-between text-[11px] font-mono text-slate-400">
                <span>ATTENTION INBOX</span>
                <span className="text-amber-400 text-xs">🔔</span>
              </div>
              <div className="text-base sm:text-lg font-bold text-slate-100 font-sans">
                {data.needs_attention?.length ? `${data.needs_attention.length} Pending` : 'All Clear (0)'}
              </div>
              <div className="text-[10px] font-mono text-slate-400">
                {data.needs_attention?.length ? 'Review Required' : '0 Items Pending'}
              </div>
            </div>

            <div className="p-3.5 rounded-xl bg-[#121520] border border-slate-800/80 flex flex-col gap-1 shadow-sm">
              <div className="flex items-center justify-between text-[11px] font-mono text-slate-400">
                <span>ACTIVE MISSIONS</span>
                <span className="text-emerald-400 text-xs">⚡</span>
              </div>
              <div className="text-base sm:text-lg font-bold text-slate-100 font-sans">
                {data.recent_activity?.length ? `${data.recent_activity.length} Active` : 'No Active Missions'}
              </div>
              <div className="text-[10px] font-mono text-slate-400">
                {data.recent_activity?.length ? 'In Progress' : 'Idle Workspace'}
              </div>
            </div>

            <div className="p-3.5 rounded-xl bg-[#121520] border border-slate-800/80 flex flex-col gap-1 shadow-sm">
              <div className="flex items-center justify-between text-[11px] font-mono text-slate-400">
                <span>AI GATEWAY</span>
                <span className="text-cyan-400 text-xs">🤖</span>
              </div>
              <div className="text-base sm:text-lg font-bold text-slate-100 font-sans">OpenRouter</div>
              <div className="text-[10px] font-mono text-cyan-400">openrouter/auto Active</div>
            </div>

            <div className="hidden lg:flex p-3.5 rounded-xl bg-[#121520] border border-slate-800/80 flex-col gap-1 shadow-sm">
              <div className="flex items-center justify-between text-[11px] font-mono text-slate-400">
                <span>COST ATTRIBUTION</span>
                <span className="text-slate-400 text-xs">💰</span>
              </div>
              <div className="text-base sm:text-lg font-bold text-slate-100 font-sans">No Usage</div>
              <div className="text-[10px] font-mono text-slate-400">Zero Token Spend</div>
            </div>
          </div>

          {/* 2-Column Responsive Command Center Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
            {/* Primary Command Column (8 cols) */}
            <div className="lg:col-span-8 flex flex-col gap-6">
              <ExecutiveSummaryCard summaryStatement={data.summary_statement} />

              {data.needs_attention && data.needs_attention.length > 0 && (
                <NeedsAttention items={data.needs_attention} />
              )}

              {data.primary_recommendation && (
                <PrimaryRecommendation recommendation={data.primary_recommendation} />
              )}

              {data.is_quiet_state && (
                <QuietHomeState />
              )}

              {data.learned_memories && data.learned_memories.length > 0 && (
                <LearnedMemoriesSection memories={data.learned_memories} />
              )}
            </div>

            {/* Right Operations & Activity Column (4 cols) */}
            <div className="lg:col-span-4 flex flex-col gap-6">
              <QuickActions actions={data.quick_actions} />

              <RecentActivity activities={data.recent_activity} />

              {/* System Resilience Sentinel Widget */}
              <Card variant="panel" className="p-5 border-slate-800/80 bg-[#121520] rounded-xl flex flex-col gap-3.5 shadow-sm">
                <div className="flex items-center justify-between border-b border-slate-800/80 pb-2.5">
                  <div className="flex items-center gap-2">
                    <span className="text-emerald-400 text-xs">🛡️</span>
                    <Typography variant="h3" className="text-xs font-bold text-slate-300 uppercase tracking-wider">
                      Resilience Sentinel
                    </Typography>
                  </div>
                  <span className="text-[10px] font-mono text-emerald-400">ACTIVE</span>
                </div>

                <div className="flex flex-col gap-2.5 text-xs">
                  <div className="flex items-center justify-between text-slate-400">
                    <span>PolicyEngine Guardrails</span>
                    <span className="font-mono text-emerald-400 font-semibold">ENFORCED</span>
                  </div>
                  <div className="flex items-center justify-between text-slate-400">
                    <span>Tenant Boundary Attestation</span>
                    <span className="font-mono text-emerald-400 font-semibold">ATT_SYNCHRONIZED</span>
                  </div>
                  <div className="flex items-center justify-between text-slate-400">
                    <span>DLP Credential Masking</span>
                    <span className="font-mono text-emerald-400 font-semibold">ALL MASKED</span>
                  </div>
                  <div className="flex items-center justify-between text-slate-400">
                    <span>Quantum Payload Signing</span>
                    <span className="font-mono text-emerald-400 font-semibold">v1:hybrid: HMAC</span>
                  </div>
                </div>

                <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between">
                  <Link
                    href="/transformation-resilience-command-center"
                    className="text-[11px] font-mono text-emerald-400 hover:text-emerald-300 transition-colors"
                  >
                    Open Command Center →
                  </Link>
                </div>
              </Card>
            </div>
          </div>
        </div>
      )}
    </AppShell>
  );
}
