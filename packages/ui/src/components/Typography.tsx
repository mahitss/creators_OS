import React from 'react';

export interface TypographyProps extends React.HTMLAttributes<HTMLElement> {
  variant?: 'h1' | 'h2' | 'h3' | 'body' | 'caption' | 'code';
  as?: React.ElementType;
}

export const Typography: React.FC<TypographyProps> = ({
  children,
  variant = 'body',
  as,
  className = '',
  ...props
}) => {
  const Component = as || (variant === 'h1' ? 'h1' : variant === 'h2' ? 'h2' : variant === 'h3' ? 'h3' : variant === 'code' ? 'code' : 'p');

  const variantStyles = {
    h1: 'text-2xl font-bold tracking-tight text-[#F5F5F5]',
    h2: 'text-lg font-semibold tracking-tight text-[#F5F5F5]',
    h3: 'text-base font-medium text-[#F5F5F5]',
    body: 'text-sm text-[#A3A3A3] leading-relaxed',
    caption: 'text-xs text-[#666666] font-normal',
    code: 'font-mono text-xs text-[#62E6B2] bg-[#080808] px-1.5 py-0.5 rounded border border-[rgba(255,255,255,0.10)] tabular-nums',
  };

  return (
    <Component className={`${variantStyles[variant]} ${className}`} {...props}>
      {children}
    </Component>
  );
};
