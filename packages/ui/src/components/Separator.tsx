import React from 'react';

export interface SeparatorProps {
  orientation?: 'horizontal' | 'vertical';
  className?: string;
}

export const Separator: React.FC<SeparatorProps> = ({ orientation = 'horizontal', className = '' }) => {
  if (orientation === 'vertical') {
    return <div className={`w-[1px] h-full bg-slate-800/80 ${className}`} role="separator" aria-orientation="vertical" />;
  }

  return <div className={`h-[1px] w-full bg-slate-800/80 ${className}`} role="separator" aria-orientation="horizontal" />;
};
