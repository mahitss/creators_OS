import React from 'react';
import { Card, Skeleton } from '@vapor/ui';

export const HomeSkeleton: React.FC = () => {
  return (
    <div className="max-w-3xl mx-auto w-full flex flex-col gap-6 py-2 animate-in fade-in duration-200">
      {/* Greeting Skeleton */}
      <div className="flex flex-col gap-2">
        <Skeleton width="220px" height="28px" />
        <Skeleton width="340px" height="16px" />
      </div>

      {/* Today's Brief Skeleton */}
      <Card variant="panel" className="flex flex-col gap-4 p-6 border-slate-800">
        <Skeleton width="120px" height="18px" />
        <Skeleton width="100%" height="48px" />
      </Card>

      {/* Quick Actions Skeleton */}
      <div className="flex flex-col gap-3">
        <Skeleton width="140px" height="14px" />
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <Skeleton height="60px" />
          <Skeleton height="60px" />
        </div>
      </div>
    </div>
  );
};
