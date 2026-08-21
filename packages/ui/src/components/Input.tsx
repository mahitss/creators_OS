import React from 'react';

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, helperText, className = '', id, ...props }, ref) => {
    const inputId = id || props.name;

    return (
      <div className="flex flex-col gap-1.5 w-full">
        {label && (
          <label htmlFor={inputId} className="text-xs font-medium text-[#A3A3A3]">
            {label}
          </label>
        )}
        <input
          ref={ref}
          id={inputId}
          className={`px-3 py-2 bg-[#080808] border text-[#F5F5F5] placeholder-[#555555] rounded-lg text-sm transition-colors focus:outline-none focus:border-[rgba(255,255,255,0.30)] focus:ring-0 ${
            error ? 'border-[#FF6B7A]' : 'border-[rgba(255,255,255,0.12)] hover:border-[rgba(255,255,255,0.20)]'
          } ${className}`}
          {...props}
        />
        {error && <span className="text-xs text-[#FF6B7A] font-medium">{error}</span>}
        {!error && helperText && <span className="text-xs text-[#666666]">{helperText}</span>}
      </div>
    );
  }
);

Input.displayName = 'Input';
