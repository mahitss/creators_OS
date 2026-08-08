import React from 'react';
import { ErrorState } from '@vapor/ui';

interface HomeErrorStateProps {
  message?: string;
  onRetry: () => void;
}

export const HomeErrorState: React.FC<HomeErrorStateProps> = ({
  message = 'Something went wrong loading your brief.',
  onRetry,
}) => {
  return (
    <div className="flex-1 flex items-center justify-center p-6">
      <ErrorState
        title="Brief Loading Error"
        message={message}
        onRetry={onRetry}
      />
    </div>
  );
};
