import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import DriveBrowserPage from '../drive/page';
import { describe, it, expect, vi } from 'vitest';

// Mock next/navigation
vi.mock('next/navigation', () => ({
  usePathname: () => '/drive',
  useRouter: () => ({
    push: vi.fn(),
  }),
}));

describe('Google Drive Document Context Workspace', () => {
  it('renders Document Context Browser header and search controls', async () => {
    render(<DriveBrowserPage />);

    await waitFor(() => {
      expect(screen.getByText(/Document Context Browser/i)).toBeInTheDocument();
      expect(screen.getByText(/Discover and select read-only Google Drive files/i)).toBeInTheDocument();
    });
  });
});
