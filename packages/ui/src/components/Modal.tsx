'use client';

import React from 'react';

export interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
}

export const Modal: React.FC<ModalProps> = ({ isOpen, onClose, title, children }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
      <div
        className="relative w-full max-w-lg bg-[#0B0B0B] border border-[rgba(255,255,255,0.12)] rounded-xl shadow-2xl p-6 overflow-hidden animate-in fade-in zoom-in-95 duration-150"
        role="dialog"
        aria-modal="true"
      >
        <div className="flex items-center justify-between pb-4 border-b border-[rgba(255,255,255,0.08)] mb-4">
          {title && <h2 className="text-base font-semibold text-[#F5F5F5]">{title}</h2>}
          <button
            onClick={onClose}
            className="text-[#666666] hover:text-[#F5F5F5] transition-colors p-1 rounded-md hover:bg-[#121212]"
            aria-label="Close Modal"
          >
            ✕
          </button>
        </div>
        <div>{children}</div>
      </div>
    </div>
  );
};
