import React from 'react';
import { Spinner } from './Spinner';
import { AlertIcon } from './Icons';

export interface EmptyStateProps {
  title: string;
  description?: string;
  action?: React.ReactNode;
  icon?: React.ReactNode;
}

export const EmptyState: React.FC<EmptyStateProps> = ({ title, description, action, icon }) => {
  return (
    <div className="flex flex-col items-center justify-center p-8 text-center max-w-sm mx-auto gap-3">
      {icon && <div className="p-3 rounded-full bg-slate-800/60 text-slate-400">{icon}</div>}
      <h3 className="text-sm font-semibold text-slate-200">{title}</h3>
      {description && <p className="text-xs text-slate-400 leading-relaxed">{description}</p>}
      {action && <div className="mt-2">{action}</div>}
    </div>
  );
};

export interface ErrorStateProps {
  title?: string;
  message: string;
  onRetry?: () => void;
}

export const ErrorState: React.FC<ErrorStateProps> = ({ title = 'An Error Occurred', message, onRetry }) => {
  return (
    <div className="flex flex-col items-center justify-center p-6 text-center max-w-sm mx-auto gap-3 rounded-lg border border-rose-500/20 bg-rose-500/5">
      <div className="p-2 rounded-full bg-rose-500/10 text-rose-400">
        <AlertIcon size={20} />
      </div>
      <h4 className="text-sm font-semibold text-slate-100">{title}</h4>
      <p className="text-xs text-slate-400">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-1 px-3 py-1.5 text-xs font-medium bg-slate-800 text-slate-200 hover:bg-slate-700 rounded border border-slate-700 transition-colors"
        >
          Try Again
        </button>
      )}
    </div>
  );
};

export interface LoadingStateProps {
  label?: string;
}

export const LoadingState: React.FC<LoadingStateProps> = ({ label = 'Loading...' }) => {
  return (
    <div className="flex flex-col items-center justify-center p-8 text-center gap-3">
      <Spinner size="md" />
      <span className="text-xs font-mono text-slate-500">{label}</span>
    </div>
  );
};
