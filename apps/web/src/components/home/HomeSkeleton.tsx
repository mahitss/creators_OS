import React from 'react';
import { Skeleton } from '@vapor/ui';

export const HomeSkeleton: React.FC = () => {
  return (
    <div className="w-full flex flex-col gap-8 animate-in fade-in duration-200 font-mono">
      {/* Greeting Skeleton */}
      <div className="flex flex-col gap-2 pb-4 border-b border-[rgba(255,255,255,0.06)]">
        <Skeleton width="180px" height="14px" />
        <Skeleton width="380px" height="32px" />
        <Skeleton width="60%" height="16px" />
      </div>

      {/* Telemetry Strip Skeleton */}
      <div className="grid grid-cols-2 sm:grid-cols-5 gap-4 py-3 border-y border-[rgba(255,255,255,0.06)]">
        <Skeleton height="36px" />
        <Skeleton height="36px" />
        <Skeleton height="36px" />
        <Skeleton height="36px" />
        <Skeleton height="36px" />
      </div>

      {/* Canvas Skeleton */}
      <div className="w-full h-80 bg-[#080808] rounded-xl border border-[rgba(255,255,255,0.06)] flex items-center justify-center">
        <Skeleton width="40%" height="24px" />
      </div>

      {/* Content Skeleton */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        <div className="lg:col-span-8 flex flex-col gap-4">
          <Skeleton width="100%" height="120px" />
          <Skeleton width="100%" height="140px" />
        </div>
        <div className="lg:col-span-4 flex flex-col gap-4">
          <Skeleton width="100%" height="180px" />
        </div>
      </div>
    </div>
  );
};

