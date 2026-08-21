import React from 'react';

export interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
  helperText?: string;
}

export const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ label, error, helperText, className = '', id, ...props }, ref) => {
    const textareaId = id || props.name;

    return (
      <div className="flex flex-col gap-1.5 w-full">
        {label && (
          <label htmlFor={textareaId} className="text-xs font-medium text-[#A3A3A3]">
            {label}
          </label>
        )}
        <textarea
          ref={ref}
          id={textareaId}
          className={`px-3 py-2 bg-[#080808] border text-[#F5F5F5] placeholder-[#555555] rounded-lg text-sm transition-colors focus-visible:outline-none focus-visible:border-[rgba(255,255,255,0.30)] ${
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

Textarea.displayName = 'Textarea';
