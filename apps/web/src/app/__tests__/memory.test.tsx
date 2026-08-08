import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import MemoryPage from '../memory/page';
import { describe, it, expect, vi, beforeEach } from 'vitest';

// Mock next/navigation
vi.mock('next/navigation', () => ({
  usePathname: () => '/memory',
  useParams: () => ({ id: 'mem_test_01' }),
  useRouter: () => ({
    push: vi.fn(),
  }),
}));

describe('Memory Foundation Workspace', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('renders memory workspace header and add memory action trigger', async () => {
    render(<MemoryPage />);

    await waitFor(() => {
      expect(screen.getByText(/Context Vault Memory/i)).toBeInTheDocument();
      expect(screen.getByText(/\+ Add Memory/i)).toBeInTheDocument();
    });
  });

  it('displays honest empty state when workspace has no stored memories', async () => {
    render(<MemoryPage />);

    await waitFor(() => {
      expect(screen.getByText(/Vapor hasn't learned anything about this workspace yet/i)).toBeInTheDocument();
      expect(screen.queryByText(/0 vector nodes/i)).not.toBeInTheDocument();
    });
  });
});
