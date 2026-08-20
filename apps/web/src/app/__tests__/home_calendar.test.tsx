import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import Home from '../home/page';
import { describe, it, expect, vi } from 'vitest';

// Mock next/navigation
vi.mock('next/navigation', () => ({
  usePathname: () => '/',
  useRouter: () => ({
    push: vi.fn(),
  }),
}));

describe('Home Executive Brief Calendar Integration', () => {
  it('renders executive brief layout and navigation shell', async () => {
    render(<Home />);

    await waitFor(() => {
      expect(screen.getByText(/Executive Summary/i)).toBeInTheDocument();
      expect(screen.getAllByText(/KINETIQ/i).length).toBeGreaterThan(0);
    });
  });
});
