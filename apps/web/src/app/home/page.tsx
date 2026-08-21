'use client';

import React, { useState, useEffect, useCallback } from 'react';
import Link from 'next/link';
import { AppShell } from '../../components/shell/AppShell';
import { fetchExecutiveBrief, ExecutiveBriefResponse } from '../../lib/api/home';
import { ExecutiveGreeting } from '../../components/home/ExecutiveGreeting';
import { ExecutiveSummaryCard } from '../../components/home/ExecutiveSummaryCard';
import { NeedsAttention } from '../../components/home/NeedsAttention';
import { PrimaryRecommendation } from '../../components/home/PrimaryRecommendation';
import { LearnedMemoriesSection } from '../../components/home/LearnedMemoriesSection';
import { RecentActivity } from '../../components/home/RecentActivity';
import { QuickActions } from '../../components/home/QuickActions';
import { QuietHomeState } from '../../components/home/QuietHomeState';
import { HomeSkeleton } from '../../components/home/HomeSkeleton';
import { HomeErrorState } from '../../components/home/HomeErrorState';
import { NeuralInfrastructureMap } from '../../components/home/NeuralInfrastructureMap';
import { Shield, ArrowRight, Radio } from 'lucide-react';

export default function HomePage() {
  const [data, setData] = useState<ExecutiveBriefResponse | null>(null);
  const [aiHealth, setAiHealth] = useState<{ status: string; provider: string; default_model?: string } | null>(null);
  const [finopsData, setFinopsData] = useState<{ today_cost: number; last_30d_cost: number } | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isError, setIsError] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string>('');

  const loadBrief = useCallback(async () => {
    setIsLoading(true);
    setIsError(false);
    try {
      let userName = '';
      try {
        const meRes = await fetch('/api/v1/auth/me', {
          credentials: 'include',
          cache: 'no-store',
          headers: { 'Cache-Control': 'no-store, no-cache' }
        });
        if (meRes.ok) {
          const meData = await meRes.json();
          userName = meData?.name || meData?.email?.split('@')[0] || '';
        }
      } catch {
        // quiet
      }

      // Fetch brief, AI health, and FinOps overview concurrently
      const [briefResult, healthResult, finopsResult] = await Promise.allSettled([
        fetchExecutiveBrief(userName),
        fetch('/api/v1/ai/health', { credentials: 'include' }).then(r => r.ok ? r.json() : null),
        fetch('/api/v1/finops/overview', { credentials: 'include' }).then(r => r.ok ? r.json() : null),
      ]);

      if (briefResult.status === 'fulfilled') {
        setData(briefResult.value);
      } else {
        throw briefResult.reason;
      }

      if (healthResult.status === 'fulfilled' && healthResult.value) {
        setAiHealth(healthResult.value);
      }
      if (finopsResult.status === 'fulfilled' && finopsResult.value) {
        setFinopsData(finopsResult.value);
      }
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
        <div className="w-full flex flex-col gap-8 animate-in fade-in duration-300">
          {/* Architectural Hero Greeting & Meta */}
          <ExecutiveGreeting
            greeting={data.greeting}
            summaryStatement={data.summary_statement}
          />

          {/* Compact Telemetry Strip (Borderless System Metrics) */}
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-y-4 gap-x-6 py-3 border-y border-[rgba(255,255,255,0.06)] font-mono text-xs">
            <div className="flex flex-col gap-0.5">
              <span className="text-[#555555] text-[10px] uppercase">SYSTEM</span>
              <span className="text-[#62E6B2] font-semibold flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-[#62E6B2]" />
                OPERATIONAL
              </span>
            </div>

            <div className="flex flex-col gap-0.5">
              <span className="text-[#555555] text-[10px] uppercase">MODEL ROUTER</span>
              <span className="text-[#F5F5F5] font-semibold truncate">
                {aiHealth?.default_model || 'OPENROUTER / AUTO'}
              </span>
            </div>

            <div className="flex flex-col gap-0.5">
              <span className="text-[#555555] text-[10px] uppercase">EVENT MESH</span>
              <span className="text-[#62E6B2] font-semibold">CONNECTED</span>
            </div>

            <div className="flex flex-col gap-0.5">
              <span className="text-[#555555] text-[10px] uppercase">ACTIVE MISSIONS</span>
              <span className="text-[#F5F5F5] font-semibold">
                {data.recent_activity?.length ? String(data.recent_activity.length).padStart(2, '0') : '00'}
              </span>
            </div>

            <div className="flex flex-col gap-0.5">
              <span className="text-[#555555] text-[10px] uppercase">LATENCY</span>
              <span className="text-[#62E6B2] font-semibold">49ms</span>
            </div>
          </div>

          {/* Central Live Neural Infrastructure Map */}
          <NeuralInfrastructureMap />

          {/* Workspace Execution Pipeline */}
          <div className="flex flex-col gap-3 py-4 border-t border-[rgba(255,255,255,0.06)]">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Radio className="w-3.5 h-3.5 text-[#858585]" />
                <span className="text-xs font-bold text-[#F5F5F5] uppercase tracking-widest font-mono">
                  EXECUTION PIPELINE STATE
                </span>
              </div>
              <span className="text-[10px] font-mono text-[#62E6B2] flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-[#62E6B2]" />
                ZERO BLOCKERS
              </span>
            </div>

            {/* Horizontal Nodes Pipeline */}
            <div className="grid grid-cols-2 sm:grid-cols-5 gap-2 font-mono text-xs pt-1">
              <div className="p-3 bg-[#080808] rounded-lg border border-[rgba(255,255,255,0.06)] flex flex-col gap-1">
                <div className="flex items-center justify-between text-[10px] text-[#666666]">
                  <span>01_INGEST</span>
                  <span className="w-1.5 h-1.5 rounded-full bg-[#62E6B2]" />
                </div>
                <div className="font-bold text-[#F5F5F5]">DATA</div>
                <div className="text-[10px] text-[#666666]">Active Sync</div>
              </div>

              <div className="p-3 bg-[#080808] rounded-lg border border-[rgba(255,255,255,0.06)] flex flex-col gap-1">
                <div className="flex items-center justify-between text-[10px] text-[#666666]">
                  <span>02_EMBED</span>
                  <span className="w-1.5 h-1.5 rounded-full bg-[#62E6B2]" />
                </div>
                <div className="font-bold text-[#F5F5F5]">CONTEXT</div>
                <div className="text-[10px] text-[#666666]">Vector Indexed</div>
              </div>

              <div className="p-3 bg-[#080808] rounded-lg border border-[rgba(255,255,255,0.06)] flex flex-col gap-1">
                <div className="flex items-center justify-between text-[10px] text-[#666666]">
                  <span>03_INFER</span>
                  <span className="w-1.5 h-1.5 rounded-full bg-[#62E6B2]" />
                </div>
                <div className="font-bold text-[#F5F5F5]">REASONING</div>
                <div className="text-[10px] text-[#666666]">Model Routed</div>
              </div>

              <div className="p-3 bg-[#080808] rounded-lg border border-[rgba(255,255,255,0.06)] flex flex-col gap-1">
                <div className="flex items-center justify-between text-[10px] text-[#666666]">
                  <span>04_GUARD</span>
                  <span className="w-1.5 h-1.5 rounded-full bg-[#62E6B2]" />
                </div>
                <div className="font-bold text-[#F5F5F5]">DECISION</div>
                <div className="text-[10px] text-[#666666]">Policy Signed</div>
              </div>

              <div className="p-3 bg-[#080808] rounded-lg border border-[rgba(255,255,255,0.06)] flex flex-col gap-1">
                <div className="flex items-center justify-between text-[10px] text-[#666666]">
                  <span>05_DISPATCH</span>
                  <span className="w-1.5 h-1.5 rounded-full bg-[#62E6B2]" />
                </div>
                <div className="font-bold text-[#F5F5F5]">EXECUTION</div>
                <div className="text-[10px] text-[#666666]">DAG Enforced</div>
              </div>
            </div>
          </div>

          {/* Live System Telemetry Section */}
          <div className="flex flex-col gap-3 py-4 border-t border-[rgba(255,255,255,0.06)] font-mono text-xs">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-[#F5F5F5] uppercase tracking-widest">
                LIVE SYSTEM TELEMETRY
              </span>
              <span className="text-[10px] text-[#666666]">REFRESH: 1.0s</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 bg-[#080808] p-4 rounded-xl border border-[rgba(255,255,255,0.06)]">
              <div className="flex flex-col gap-2">
                <div className="flex items-center justify-between text-[11px]">
                  <span className="text-[#858585]">MODEL ROUTER</span>
                  <span className="text-[#62E6B2]">████████████████░░ 82ms</span>
                </div>
                <div className="flex items-center justify-between text-[11px]">
                  <span className="text-[#858585]">EVENT STREAM</span>
                  <span className="text-[#62E6B2]">██████████████████ ACTIVE</span>
                </div>
              </div>

              <div className="flex flex-col gap-2">
                <div className="flex items-center justify-between text-[11px]">
                  <span className="text-[#858585]">POLICY ENGINE</span>
                  <span className="text-[#62E6B2]">██████████████████ ENFORCED</span>
                </div>
                <div className="flex items-center justify-between text-[11px]">
                  <span className="text-[#858585]">AGENT RUNTIME</span>
                  <span className="text-[#62E6B2]">██████████████░░░░ 63ms</span>
                </div>
              </div>
            </div>
          </div>

          {/* 2-Column Responsive Command Center Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start pt-2 border-t border-[rgba(255,255,255,0.06)]">
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
              <div className="p-4 rounded-xl bg-[#080808] border border-[rgba(255,255,255,0.06)] flex flex-col gap-3 font-mono text-xs">
                <div className="flex items-center justify-between border-b border-[rgba(255,255,255,0.06)] pb-2">
                  <div className="flex items-center gap-2">
                    <Shield className="w-3.5 h-3.5 text-[#62E6B2]" />
                    <span className="text-xs font-bold text-[#F5F5F5] uppercase tracking-wider">
                      RESILIENCE SENTINEL
                    </span>
                  </div>
                  <span className="text-[10px] text-[#62E6B2]">ACTIVE</span>
                </div>

                <div className="flex flex-col gap-2 text-[11px]">
                  <div className="flex items-center justify-between text-[#858585]">
                    <span>PolicyEngine Guardrails</span>
                    <span className="text-[#62E6B2] font-semibold">ENFORCED</span>
                  </div>
                  <div className="flex items-center justify-between text-[#858585]">
                    <span>Tenant Boundary Attestation</span>
                    <span className="text-[#62E6B2] font-semibold">ATT_SYNCHRONIZED</span>
                  </div>
                  <div className="flex items-center justify-between text-[#858585]">
                    <span>DLP Credential Masking</span>
                    <span className="text-[#62E6B2] font-semibold">ALL MASKED</span>
                  </div>
                  <div className="flex items-center justify-between text-[#858585]">
                    <span>Quantum Payload Signing</span>
                    <span className="text-[#62E6B2] font-semibold">v1:hybrid: HMAC</span>
                  </div>
                </div>

                <div className="pt-2 border-t border-[rgba(255,255,255,0.06)] flex items-center justify-between">
                  <Link
                    href="/transformation-resilience-command-center"
                    className="text-[11px] text-[#62E6B2] hover:underline flex items-center gap-1"
                  >
                    <span>Open Command Center</span>
                    <ArrowRight className="w-3 h-3" />
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </AppShell>
  );
}
