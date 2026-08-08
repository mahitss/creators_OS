'use client';

import React, { useState, useEffect, useCallback } from 'react';
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

export default function Home() {
  const [data, setData] = useState<ExecutiveBriefResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isError, setIsError] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string>('');

  const loadBrief = useCallback(async () => {
    setIsLoading(true);
    setIsError(false);
    try {
      const result = await fetchExecutiveBrief('Alex');
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
        <div className="max-w-3xl mx-auto w-full flex flex-col gap-6 py-2 animate-in fade-in duration-200">
          <ExecutiveGreeting
            greeting={data.greeting}
            summaryStatement={data.summary_statement}
          />

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

          <RecentActivity activities={data.recent_activity} />

          <QuickActions actions={data.quick_actions} />
        </div>
      )}
    </AppShell>
  );
}
