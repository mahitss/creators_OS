import React from 'react';

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: 'default' | 'emerald' | 'cyan' | 'amber' | 'crimson';
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = 'default',
  className = '',
  ...props
}) => {
  const variantStyles = {
    default: 'bg-[#121212] text-[#A3A3A3] border-[rgba(255,255,255,0.10)]',
    emerald: 'bg-[rgba(98,230,178,0.08)] text-[#62E6B2] border-[rgba(98,230,178,0.25)]',
    cyan: 'bg-[rgba(98,230,178,0.08)] text-[#62E6B2] border-[rgba(98,230,178,0.25)]',
    amber: 'bg-[rgba(231,185,94,0.10)] text-[#E7B95E] border-[rgba(231,185,94,0.25)]',
    crimson: 'bg-[rgba(255,107,122,0.10)] text-[#FF6B7A] border-[rgba(255,107,122,0.25)]',
  };

  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 text-xs font-mono font-medium border rounded-full ${variantStyles[variant]} ${className}`}
      {...props}
    >
      {children}
    </span>
  );
};
