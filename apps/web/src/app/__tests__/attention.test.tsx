import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import AttentionPage from '../attention/page';
import { describe, it, expect, vi, beforeEach } from 'vitest';

// Mock next/navigation
vi.mock('next/navigation', () => ({
  usePathname: () => '/attention',
  useRouter: () => ({
    push: vi.fn(),
  }),
}));

describe('Attention Center Workspace', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('renders attention center header and reconcile action trigger', async () => {
    render(<AttentionPage />);

    await waitFor(() => {
      expect(screen.getByText(/Attention Center/i)).toBeInTheDocument();
      expect(screen.getByText(/Reconcile/i)).toBeInTheDocument();
    });
  });

  it('displays quiet empty state when workspace has no open attention items', async () => {
    render(<AttentionPage />);

    await waitFor(() => {
      expect(screen.getByText(/You're all caught up/i)).toBeInTheDocument();
      expect(screen.queryByText(/99\+/i)).not.toBeInTheDocument();
    });
  });
});
