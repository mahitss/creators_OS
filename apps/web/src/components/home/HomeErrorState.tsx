import React from 'react';
import { Button } from '@vapor/ui';

interface HomeErrorStateProps {
  message?: string;
  onRetry: () => void;
}

export const HomeErrorState: React.FC<HomeErrorStateProps> = ({
  message = 'Unable to connect to Vapor Core API kernel.',
  onRetry,
}) => {
  const isConnectionRefused = message.toLowerCase().includes('connection') || message.toLowerCase().includes('fetch');

  return (
    <div className="flex-1 flex items-center justify-center p-6 min-h-[400px]">
      <div className="max-w-md w-full bg-[#121520] border border-rose-900/40 rounded-2xl p-6 shadow-2xl flex flex-col items-center text-center gap-4">
        <div className="w-12 h-12 rounded-xl bg-rose-950/60 border border-rose-500/30 flex items-center justify-center text-rose-400 text-xl font-bold">
          ⚠️
        </div>
        
        <div className="flex flex-col gap-1">
          <h3 className="text-base font-bold text-slate-100">
            {isConnectionRefused ? 'Backend Kernel Offline' : 'Executive Brief Error'}
          </h3>
          <p className="text-slate-400 font-mono text-xs">
            {message}
          </p>
        </div>

        {isConnectionRefused && (
          <div className="w-full text-left bg-slate-900/80 border border-slate-800 rounded-lg p-3 text-[11px] font-mono text-slate-400 space-y-1">
            <div className="text-slate-300 font-semibold">Troubleshooting:</div>
            <div>• Ensure FastAPI is running on port 8000</div>
            <div>• Command: <code className="text-cyan-400">uvicorn app.main:app --port 8000</code></div>
            <div>• Docker: <code className="text-cyan-400">docker-compose up -d</code></div>
          </div>
        )}

        <div className="flex gap-3 pt-2">
          <Button variant="primary" onClick={onRetry} className="bg-rose-600 hover:bg-rose-500 text-white font-medium px-5 py-2">
            Retry Connection
          </Button>
        </div>
      </div>
    </div>
  );
};
