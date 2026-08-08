import React from 'react';

export interface IconButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  icon: React.ReactNode;
  ariaLabel: string;
  variant?: 'primary' | 'secondary' | 'ghost' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}

export const IconButton = React.forwardRef<HTMLButtonElement, IconButtonProps>(
  ({ icon, ariaLabel, variant = 'ghost', size = 'md', isLoading = false, disabled, className = '', ...props }, ref) => {
    const baseStyles = 'inline-flex items-center justify-center rounded-md font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 disabled:opacity-40 disabled:pointer-events-none active:scale-[0.97]';

    const variantStyles = {
      primary: 'bg-emerald-500 text-slate-950 hover:bg-emerald-400',
      secondary: 'bg-slate-800 text-slate-200 border border-slate-700 hover:bg-slate-700',
      outline: 'border border-slate-800 text-slate-300 hover:bg-slate-800 hover:text-slate-100',
      ghost: 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/60',
    };

    const sizeStyles = {
      sm: 'w-7 h-7 text-xs',
      md: 'w-9 h-9 text-sm',
      lg: 'w-11 h-11 text-base',
    };

    return (
      <button
        ref={ref}
        aria-label={ariaLabel}
        disabled={disabled || isLoading}
        className={`${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${className}`}
        {...props}
      >
        {isLoading ? (
          <span className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
        ) : (
          icon
        )}
      </button>
    );
  }
);

IconButton.displayName = 'IconButton';
