import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import MissionsPage from '../missions/page';
import { describe, it, expect, vi, beforeEach } from 'vitest';

// Mock next/navigation
vi.mock('next/navigation', () => ({
  usePathname: () => '/missions',
  useParams: () => ({ id: 'ms_test_01' }),
  useRouter: () => ({
    push: vi.fn(),
  }),
}));

describe('Missions Workspace View', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('renders missions workspace header and create mission trigger button', async () => {
    render(<MissionsPage />);

    await waitFor(() => {
      expect(screen.getByText(/^Missions$/i)).toBeInTheDocument();
      expect(screen.getByText(/\+ Create Mission/i)).toBeInTheDocument();
    });
  });

  it('renders honest empty state when workspace has no active missions', async () => {
    render(<MissionsPage />);

    await waitFor(() => {
      expect(screen.getByText(/No missions yet/i)).toBeInTheDocument();
      expect(screen.queryByText(/Total Missions: 17/i)).not.toBeInTheDocument();
    });
  });
});
