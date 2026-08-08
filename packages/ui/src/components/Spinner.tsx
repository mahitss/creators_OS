import React from 'react';

export interface SpinnerProps extends React.SVGProps<SVGSVGElement> {
  size?: 'sm' | 'md' | 'lg';
}

export const Spinner: React.FC<SpinnerProps> = ({
  size = 'md',
  className = '',
  ...props
}) => {
  const sizePixels = {
    sm: 16,
    md: 24,
    lg: 32,
  }[size];

  return (
    <svg
      width={sizePixels}
      height={sizePixels}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={`animate-spin text-emerald-500 ${className}`}
      {...props}
    >
      <path d="M21 12a9 9 0 1 1-6.219-8.56" />
    </svg>
  );
};
