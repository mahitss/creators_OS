import React from 'react';
import { Typography } from '@vapor/ui';

interface ExecutiveGreetingProps {
  greeting: string;
  summaryStatement: string;
}

export const ExecutiveGreeting: React.FC<ExecutiveGreetingProps> = ({
  greeting,
  summaryStatement,
}) => {
  return (
    <div className="flex flex-col gap-1 pb-2">
      <Typography variant="h1" className="text-xl sm:text-2xl font-bold tracking-tight text-slate-100">
        {greeting}
      </Typography>
      <Typography variant="caption" className="text-slate-400 text-xs sm:text-sm max-w-xl">
        {summaryStatement}
      </Typography>
    </div>
  );
};
