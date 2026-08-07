import React from 'react';

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'panel' | 'elevated' | 'outline';
}

export const Card: React.FC<CardProps> = ({
  children,
  variant = 'panel',
  className = '',
  ...props
}) => {
  const variantStyles = {
    panel: 'bg-slate-900/90 border border-slate-800/80',
    elevated: 'bg-slate-850 border border-slate-700/60 shadow-xl shadow-black/40',
    outline: 'bg-transparent border border-slate-800 hover:border-slate-700',
  };

  return (
    <div
      className={`rounded-lg p-5 transition-all ${variantStyles[variant]} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};
