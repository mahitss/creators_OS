import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import Home from '../page';
import { describe, it, expect, vi, beforeEach } from 'vitest';

// Mock next/navigation
vi.mock('next/navigation', () => ({
  usePathname: () => '/',
  useRouter: () => ({
    push: vi.fn(),
  }),
}));

describe('Home / Executive Brief View', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('renders executive brief with user greeting and available quick actions', async () => {
    render(<Home />);

    await waitFor(() => {
      expect(screen.getByText(/Alex/i)).toBeInTheDocument();
      expect(screen.getByText(/Today's Brief/i)).toBeInTheDocument();
      expect(screen.getByText(/Missions Orchestrator/i)).toBeInTheDocument();
    });
  });

  it('displays empty state messaging when workspace is empty without fake metrics', async () => {
    render(<Home />);

    await waitFor(() => {
      expect(screen.getByText(/Vapor hasn't completed any background missions yet/i)).toBeInTheDocument();
      expect(screen.queryByText(/0%/i)).not.toBeInTheDocument();
      expect(screen.queryByText(/0 missions/i)).not.toBeInTheDocument();
    });
  });
});
