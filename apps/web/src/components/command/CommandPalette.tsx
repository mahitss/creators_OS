import React, { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { Dialog, Input, Typography, Badge } from '@vapor/ui';
import { fetchSearchResults, SearchResult } from '../../lib/api/search';
import { COMMAND_REGISTRY, CommandItem } from '../../lib/commands/registry';

export interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
  onOpenCreateMission?: () => void;
  onOpenCreateContent?: () => void;
  onOpenAddMemory?: () => void;
}

export const CommandPalette: React.FC<CommandPaletteProps> = ({
  isOpen,
  onClose,
  onOpenCreateMission,
  onOpenCreateContent,
  onOpenAddMemory,
}) => {
  const router = useRouter();
  const [mode, setMode] = useState<'search' | 'command'>('search');
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(0);

  // Filter commands by query
  const filteredCommands = COMMAND_REGISTRY.filter((cmd) => {
    if (!query.trim()) return true;
    const q = query.toLowerCase();
    return (
      cmd.label.toLowerCase().includes(q) ||
      cmd.description.toLowerCase().includes(q) ||
      cmd.category.toLowerCase().includes(q)
    );
  });

  // Debounced Entity Search
  useEffect(() => {
    if (mode !== 'search' || !query.trim()) {
      setResults([]);
      setIsLoading(false);
      return;
    }

    setIsLoading(true);
    const timer = setTimeout(() => {
      fetchSearchResults(query)
        .then((res) => setResults(res.results))
        .catch(() => setResults([]))
        .finally(() => setIsLoading(false));
    }, 200);

    return () => clearTimeout(timer);
  }, [query, mode]);

  // Handle Command Execution
  const executeCommand = useCallback(
    (cmd: CommandItem) => {
      onClose();
      cmd.action({
        router,
        openCreateMission: onOpenCreateMission,
        openCreateContent: onOpenCreateContent,
        openAddMemory: onOpenAddMemory,
      });
    },
    [router, onClose, onOpenCreateMission, onOpenCreateContent, onOpenAddMemory]
  );

  // Handle Result Navigation
  const executeResult = useCallback(
    (res: SearchResult) => {
      onClose();
      router.push(res.url);
    },
    [router, onClose]
  );

  // Keyboard navigation inside Palette
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!isOpen) return;

      if (e.key === 'ArrowDown') {
        e.preventDefault();
        const max = mode === 'search' ? results.length : filteredCommands.length;
        if (max > 0) setSelectedIndex((prev) => (prev + 1) % max);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        const max = mode === 'search' ? results.length : filteredCommands.length;
        if (max > 0) setSelectedIndex((prev) => (prev - 1 + max) % max);
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (mode === 'search' && results[selectedIndex]) {
          executeResult(results[selectedIndex]);
        } else if (mode === 'command' && filteredCommands[selectedIndex]) {
          executeCommand(filteredCommands[selectedIndex]);
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, mode, results, filteredCommands, selectedIndex, executeResult, executeCommand]);

  if (!isOpen) return null;

  return (
    <Dialog isOpen={isOpen} onClose={onClose} title="Global Search & Command Center">
      <div className="flex flex-col gap-3 mt-1">
        {/* Mode Switcher Tabs */}
        <div className="flex items-center justify-between border-b border-slate-800 pb-2">
          <div className="flex items-center gap-2">
            <button
              onClick={() => {
                setMode('search');
                setSelectedIndex(0);
              }}
              className={`px-3 py-1 text-xs font-semibold rounded-md transition-all ${
                mode === 'search' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              🔍 Entity Search
            </button>
            <button
              onClick={() => {
                setMode('command');
                setSelectedIndex(0);
              }}
              className={`px-3 py-1 text-xs font-semibold rounded-md transition-all ${
                mode === 'command' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              ⚡ Commands
            </button>
          </div>
          <Typography variant="caption" className="text-[11px] font-mono text-slate-500">
            Esc to close
          </Typography>
        </div>

        {/* Input Field */}
        <Input
          placeholder={mode === 'search' ? 'Search missions, content, memories, attention...' : 'Search commands (e.g. Create Mission, Sign Out)...'}
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setSelectedIndex(0);
          }}
          autoFocus
        />

        {/* Entity Search Results Mode */}
        {mode === 'search' && (
          <div className="flex flex-col gap-1 max-h-72 overflow-y-auto pt-1">
            {isLoading ? (
              <div className="py-6 text-center text-xs font-mono text-slate-500">Searching workspace entities...</div>
            ) : !query.trim() ? (
              <div className="py-6 text-center text-xs font-mono text-slate-500">Type a query to search across Missions, Content, Memory & Attention.</div>
            ) : results.length === 0 ? (
              <div className="py-6 text-center text-xs text-slate-400">No workspace items found matching "{query}".</div>
            ) : (
              results.map((res, idx) => (
                <div
                  key={`${res.type}-${res.id}`}
                  onClick={() => executeResult(res)}
                  className={`flex items-start justify-between p-2.5 rounded-md cursor-pointer transition-colors ${
                    idx === selectedIndex ? 'bg-slate-800 border border-slate-700' : 'hover:bg-slate-900/60'
                  }`}
                >
                  <div className="flex flex-col gap-0.5">
                    <div className="flex items-center gap-2">
                      <Badge variant={res.type === 'mission' ? 'cyan' : res.type === 'content' ? 'amber' : res.type === 'memory' ? 'emerald' : 'default'}>
                        {res.type.toUpperCase()}
                      </Badge>
                      <Typography variant="body" className="text-xs font-semibold text-slate-200">
                        {res.title}
                      </Typography>
                    </div>
                    <Typography variant="caption" className="text-[11px] text-slate-400 line-clamp-1">
                      {res.description}
                    </Typography>
                  </div>
                  <span className="text-[10px] font-mono text-slate-500 shrink-0">Open →</span>
                </div>
              ))
            )}
          </div>
        )}

        {/* Command Mode */}
        {mode === 'command' && (
          <div className="flex flex-col gap-1 max-h-72 overflow-y-auto pt-1">
            {filteredCommands.length === 0 ? (
              <div className="py-6 text-center text-xs text-slate-400">No matching commands found.</div>
            ) : (
              filteredCommands.map((cmd, idx) => (
                <div
                  key={cmd.id}
                  onClick={() => executeCommand(cmd)}
                  className={`flex items-center justify-between p-2.5 rounded-md cursor-pointer transition-colors ${
                    idx === selectedIndex ? 'bg-slate-800 border border-slate-700' : 'hover:bg-slate-900/60'
                  }`}
                >
                  <div className="flex items-center gap-2.5">
                    <span className="text-sm">{cmd.icon}</span>
                    <div className="flex flex-col">
                      <Typography variant="body" className="text-xs font-semibold text-slate-200">
                        {cmd.label}
                      </Typography>
                      <Typography variant="caption" className="text-[11px] text-slate-400">
                        {cmd.description}
                      </Typography>
                    </div>
                  </div>
                  {cmd.shortcut && (
                    <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-400">
                      {cmd.shortcut}
                    </span>
                  )}
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </Dialog>
  );
};
