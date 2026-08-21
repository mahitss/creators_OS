'use client';

import React from 'react';

export interface DialogProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  description?: string;
  children: React.ReactNode;
}

export const Dialog: React.FC<DialogProps> = ({
  isOpen,
  onClose,
  title,
  description,
  children,
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
      <div
        className="relative w-full max-w-md bg-[#0B0B0B] border border-[rgba(255,255,255,0.12)] rounded-xl shadow-2xl p-6 overflow-hidden animate-in fade-in zoom-in-95 duration-150"
        role="dialog"
        aria-modal="true"
        aria-labelledby={title ? 'dialog-title' : undefined}
        aria-describedby={description ? 'dialog-description' : undefined}
      >
        <div className="flex items-center justify-between pb-3 border-b border-[rgba(255,255,255,0.08)] mb-4">
          <div>
            {title && (
              <h2 id="dialog-title" className="text-base font-semibold text-[#F5F5F5]">
                {title}
              </h2>
            )}
            {description && (
              <p id="dialog-description" className="text-xs text-[#A3A3A3] mt-0.5">
                {description}
              </p>
            )}
          </div>
          <button
            onClick={onClose}
            className="text-[#666666] hover:text-[#F5F5F5] transition-colors p-1 rounded hover:bg-[#121212]"
            aria-label="Close dialog"
          >
            ✕
          </button>
        </div>
        <div>{children}</div>
      </div>
    </div>
  );
};
