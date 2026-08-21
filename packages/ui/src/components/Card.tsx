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
    panel: 'bg-[#0B0B0B] border border-[rgba(255,255,255,0.10)]',
    elevated: 'bg-[#101010] border border-[rgba(255,255,255,0.14)] shadow-xl shadow-black/40',
    outline: 'bg-transparent border border-[rgba(255,255,255,0.10)] hover:border-[rgba(255,255,255,0.16)]',
  };

  return (
    <div
      className={`rounded-xl p-5 transition-all ${variantStyles[variant]} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};
