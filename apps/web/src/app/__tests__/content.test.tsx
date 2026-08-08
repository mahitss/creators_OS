import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import ContentPage from '../content/page';
import { describe, it, expect, vi, beforeEach } from 'vitest';

// Mock next/navigation
vi.mock('next/navigation', () => ({
  usePathname: () => '/content',
  useParams: () => ({ id: 'cnt_test_01' }),
  useRouter: () => ({
    push: vi.fn(),
  }),
}));

describe('Studio Content Canvas Workspace', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('renders studio content canvas header and create action trigger', async () => {
    render(<ContentPage />);

    await waitFor(() => {
      expect(screen.getByText(/Studio Content Canvas/i)).toBeInTheDocument();
      expect(screen.getByText(/\+ Create Content/i)).toBeInTheDocument();
    });
  });

  it('displays honest empty state when workspace has no content deliverables', async () => {
    render(<ContentPage />);

    await waitFor(() => {
      expect(screen.getByText(/Nothing here yet/i)).toBeInTheDocument();
      expect(screen.getByText(/Content created from your missions will appear here/i)).toBeInTheDocument();
      expect(screen.queryByText(/0 publications/i)).not.toBeInTheDocument();
    });
  });
});
