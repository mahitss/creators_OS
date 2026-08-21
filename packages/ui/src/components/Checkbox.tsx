'use client';

import React from 'react';

export interface CheckboxProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label?: string;
}

export const Checkbox = React.forwardRef<HTMLInputElement, CheckboxProps>(
  ({ label, className = '', id, ...props }, ref) => {
    const checkboxId = id || props.name;

    return (
      <label htmlFor={checkboxId} className="inline-flex items-center gap-2 cursor-pointer text-sm text-[#A3A3A3] select-none">
        <input
          ref={ref}
          type="checkbox"
          id={checkboxId}
          className={`w-4 h-4 rounded border-[rgba(255,255,255,0.16)] bg-[#080808] text-[#62E6B2] focus:ring-0 accent-[#62E6B2] cursor-pointer ${className}`}
          {...props}
        />
        {label && <span>{label}</span>}
      </label>
    );
  }
);

Checkbox.displayName = 'Checkbox';
