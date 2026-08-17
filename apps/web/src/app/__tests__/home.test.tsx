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

describe('Executive Intelligence Home View', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('renders executive summary statement and quick actions', async () => {
    render(<Home />);

    await waitFor(() => {
      expect(screen.getByText(/Executive Summary/i)).toBeInTheDocument();
      expect(screen.getByText(/Missions Orchestrator/i)).toBeInTheDocument();
    });
  });

  it('displays quiet home state when workspace is clear of active/failed tasks', async () => {
    render(<Home />);

    await waitFor(() => {
      expect(screen.getByText(/Workspace Quiet State/i)).toBeInTheDocument();
      expect(screen.queryByText(/0%/i)).not.toBeInTheDocument();
      expect(screen.queryByText(/0 tasks/i)).not.toBeInTheDocument();
    });
  });
});
