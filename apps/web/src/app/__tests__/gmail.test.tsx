import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import GmailTriagePage from '../gmail/page';
import { describe, it, expect, vi } from 'vitest';

// Mock next/navigation
vi.mock('next/navigation', () => ({
  usePathname: () => '/gmail',
  useRouter: () => ({
    push: vi.fn(),
  }),
}));

describe('Gmail Intelligence Triage Workspace', () => {
  it('renders Email Triage header and sync controls', async () => {
    render(<GmailTriagePage />);

    await waitFor(() => {
      expect(screen.getByText(/Email Triage/i)).toBeInTheDocument();
      expect(screen.getByText(/Read-only email classification/i)).toBeInTheDocument();
    });
  });
});
