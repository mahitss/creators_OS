import React from 'react';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  disabled,
  className = '',
  ...props
}) => {
  const baseStyles = 'inline-flex items-center justify-center font-semibold transition-all focus:outline-none focus:ring-1 focus:ring-white/20 disabled:opacity-40 disabled:cursor-not-allowed rounded-lg shadow-none';
  
  const variantStyles = {
    primary: 'bg-[#F2F2F2] text-[#050505] hover:bg-[#FFFFFF] active:scale-[0.98]',
    secondary: 'bg-[#0B0B0B] text-[#E5E5E5] border border-[rgba(255,255,255,0.14)] hover:bg-[#151515] hover:border-[rgba(255,255,255,0.22)] active:scale-[0.98]',
    danger: 'bg-[rgba(255,107,122,0.10)] text-[#FF6B7A] border border-[rgba(255,107,122,0.25)] hover:bg-[rgba(255,107,122,0.18)] active:scale-[0.98]',
    ghost: 'bg-transparent text-[#A3A3A3] hover:text-[#F5F5F5] hover:bg-[rgba(255,255,255,0.06)] active:scale-[0.98]',
  };

  const sizeStyles = {
    sm: 'px-2.5 py-1 text-xs gap-1.5',
    md: 'px-4 py-2 text-sm gap-2',
    lg: 'px-6 py-3 text-base gap-2.5',
  };

  return (
    <button
      className={`${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${className}`}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? (
        <span className="inline-block w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin mr-1.5" />
      ) : null}
      {children}
    </button>
  );
};
