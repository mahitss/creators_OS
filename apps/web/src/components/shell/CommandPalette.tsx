'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Dialog, Input } from '@vapor/ui';

export interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
  onSignOut: () => void;
}

export const CommandPalette: React.FC<CommandPaletteProps> = ({ isOpen, onClose, onSignOut }) => {
  const router = useRouter();
  const [query, setQuery] = useState('');

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        if (isOpen) onClose();
        else {
          // Open trigger handled by parent shell
        }
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const actions = [
    { id: 'nav-home', label: 'Navigate: Home', shortcut: 'G H', perform: () => router.push('/') },
    { id: 'nav-missions', label: 'Navigate: Missions', shortcut: 'G M', perform: () => router.push('/missions') },
    { id: 'nav-content', label: 'Navigate: Content', shortcut: 'G C', perform: () => router.push('/content') },
    { id: 'nav-memory', label: 'Navigate: Memory', shortcut: 'G R', perform: () => router.push('/memory') },
    { id: 'nav-settings', label: 'Navigate: Settings', shortcut: 'G S', perform: () => router.push('/settings') },
    { id: 'action-signout', label: 'System: Sign Out', shortcut: 'Shift + Q', perform: onSignOut },
  ];

  const filteredActions = actions.filter((action) =>
    action.label.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <Dialog isOpen={isOpen} onClose={onClose} title="Vapor Command Palette">
      <div className="flex flex-col gap-3">
        <Input
          placeholder="Search commands or navigate workspace..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          autoFocus
        />
        <div className="flex flex-col gap-1 max-h-60 overflow-y-auto" role="listbox">
          {filteredActions.length === 0 ? (
            <span className="text-xs text-slate-500 py-3 text-center">No commands found</span>
          ) : (
            filteredActions.map((action) => (
              <button
                key={action.id}
                onClick={() => {
                  action.perform();
                  onClose();
                }}
                className="flex items-center justify-between px-3 py-2 text-xs rounded hover:bg-slate-800 text-slate-200 hover:text-emerald-400 transition-colors text-left"
                role="option"
                aria-selected="false"
              >
                <span>{action.label}</span>
                <kbd className="px-1.5 py-0.5 text-[10px] font-mono bg-slate-950 text-slate-500 rounded border border-slate-800">
                  {action.shortcut}
                </kbd>
              </button>
            ))
          )}
        </div>
      </div>
    </Dialog>
  );
};
