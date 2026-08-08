import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import IntegrationsSettingsPage from '../settings/integrations/page';
import { describe, it, expect, vi } from 'vitest';

// Mock next/navigation
vi.mock('next/navigation', () => ({
  usePathname: () => '/settings/integrations',
  useRouter: () => ({
    push: vi.fn(),
  }),
}));

describe('Integrations Settings Workspace', () => {
  it('renders Google Workspace Identity provider card and connect trigger', async () => {
    render(<IntegrationsSettingsPage />);

    await waitFor(() => {
      expect(screen.getByText(/Integrations & Connected Accounts/i)).toBeInTheDocument();
      expect(screen.getByText(/Google Workspace Identity/i)).toBeInTheDocument();
      expect(screen.getByText(/Connect Google/i)).toBeInTheDocument();
    });
  });
});
