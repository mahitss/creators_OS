'use client';

import React from 'react';

export interface SelectOption {
  label: string;
  value: string;
  disabled?: boolean;
}

export interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  options: SelectOption[];
  label?: string;
  error?: string;
}

export const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
  ({ options, label, error, className = '', id, ...props }, ref) => {
    const selectId = id || props.name;

    return (
      <div className="flex flex-col gap-1.5 w-full">
        {label && (
          <label htmlFor={selectId} className="text-xs font-medium text-[#A3A3A3]">
            {label}
          </label>
        )}
        <select
          ref={ref}
          id={selectId}
          className={`px-3 py-2 bg-[#080808] border text-[#F5F5F5] rounded-lg text-sm transition-colors focus-visible:outline-none focus-visible:border-[rgba(255,255,255,0.30)] ${
            error ? 'border-[#FF6B7A]' : 'border-[rgba(255,255,255,0.12)] hover:border-[rgba(255,255,255,0.20)]'
          } ${className}`}
          {...props}
        >
          {options.map((opt) => (
            <option key={opt.value} value={opt.value} disabled={opt.disabled} className="bg-[#0B0B0B] text-[#F5F5F5]">
              {opt.label}
            </option>
          ))}
        </select>
        {error && <span className="text-xs text-[#FF6B7A] font-medium">{error}</span>}
      </div>
    );
  }
);

Select.displayName = 'Select';
