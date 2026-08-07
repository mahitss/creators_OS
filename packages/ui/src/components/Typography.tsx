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
    h1: 'text-2xl font-bold tracking-tight text-slate-100',
    h2: 'text-lg font-semibold tracking-tight text-slate-100',
    h3: 'text-base font-medium text-slate-200',
    body: 'text-sm text-slate-300 leading-relaxed',
    caption: 'text-xs text-slate-500 font-normal',
    code: 'font-mono text-xs text-emerald-400 bg-slate-950 px-1.5 py-0.5 rounded border border-slate-800 tabular-nums',
  };

  return (
    <Component className={`${variantStyles[variant]} ${className}`} {...props}>
      {children}
    </Component>
  );
};
