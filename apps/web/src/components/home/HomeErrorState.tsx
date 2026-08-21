import React from 'react';
import { AlertTriangle } from 'lucide-react';
import { Button } from '@vapor/ui';

interface HomeErrorStateProps {
  message?: string;
  onRetry: () => void;
}

export const HomeErrorState: React.FC<HomeErrorStateProps> = ({
  message = 'Unable to connect to Kinetiq Core API kernel.',
  onRetry,
}) => {
  const isConnectionRefused = message.toLowerCase().includes('connection') || message.toLowerCase().includes('fetch');

  return (
    <div className="flex-1 flex items-center justify-center p-6 min-h-[400px]">
      <div className="max-w-md w-full bg-[#080808] border border-[rgba(255,107,122,0.20)] rounded-xl p-6 flex flex-col items-center text-center gap-4">
        <div className="w-10 h-10 rounded-lg bg-[rgba(255,107,122,0.08)] border border-[rgba(255,107,122,0.20)] flex items-center justify-center text-[#FF6B7A]">
          <AlertTriangle className="w-5 h-5" />
        </div>
        
        <div className="flex flex-col gap-1">
          <h3 className="text-sm font-bold text-[#F5F5F5] font-sans uppercase tracking-wider">
            {isConnectionRefused ? 'Backend Kernel Offline' : 'Executive Brief Error'}
          </h3>
          <p className="text-[#A3A3A3] font-mono text-xs">
            {message}
          </p>
        </div>

        {isConnectionRefused && (
          <div className="w-full text-left bg-[#050505] border border-[rgba(255,255,255,0.06)] rounded p-3 text-[11px] font-mono text-[#858585] space-y-1">
            <div className="text-[#F5F5F5] font-semibold">Troubleshooting:</div>
            <div>• Ensure FastAPI is running on port 8000</div>
            <div>• Command: <code className="text-[#62E6B2]">uvicorn app.main:app --port 8000</code></div>
          </div>
        )}

        <div className="flex gap-3 pt-2">
          <Button variant="danger" onClick={onRetry} size="sm">
            Retry Connection
          </Button>
        </div>
      </div>
    </div>
  );
};

