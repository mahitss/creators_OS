'use client';

import React from 'react';

export interface ToastMessage {
  id: string;
  type: 'info' | 'success' | 'warning' | 'error';
  title: string;
  description?: string;
}

export interface ToastProps {
  toasts: ToastMessage[];
  onDismiss: (id: string) => void;
}

export const ToastContainer: React.FC<ToastProps> = ({ toasts, onDismiss }) => {
  if (toasts.length === 0) return null;

  const typeStyles = {
    info: 'border-[rgba(255,255,255,0.12)] text-[#F5F5F5] bg-[#0B0B0B]',
    success: 'border-[rgba(98,230,178,0.25)] text-[#62E6B2] bg-[#0B0B0B]',
    warning: 'border-[rgba(231,185,94,0.25)] text-[#E7B95E] bg-[#0B0B0B]',
    error: 'border-[rgba(255,107,122,0.25)] text-[#FF6B7A] bg-[#0B0B0B]',
  };

  return (
    <div className="fixed bottom-4 right-4 z-50 flex flex-col gap-2 max-w-sm w-full pointer-events-none">
      {toasts.map((toast) => (
        <div
          key={toast.id}
          className={`pointer-events-auto flex items-start justify-between p-3 rounded-lg border shadow-xl backdrop-blur-md animate-in slide-in-from-bottom-2 ${typeStyles[toast.type]}`}
          role="alert"
        >
          <div className="flex flex-col gap-0.5">
            <span className="text-xs font-semibold">{toast.title}</span>
            {toast.description && <span className="text-[11px] opacity-80">{toast.description}</span>}
          </div>
          <button
            onClick={() => onDismiss(toast.id)}
            className="text-xs opacity-60 hover:opacity-100 p-0.5"
            aria-label="Dismiss toast"
          >
            ✕
          </button>
        </div>
      ))}
    </div>
  );
};
