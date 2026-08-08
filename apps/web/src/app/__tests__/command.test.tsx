import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { CommandPalette } from '../../components/command/CommandPalette';
import { describe, it, expect, vi } from 'vitest';

// Mock next/navigation
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: vi.fn(),
  }),
}));

describe('Command Palette & Search Component', () => {
  it('renders search and command tabs and supports mode switching', async () => {
    render(<CommandPalette isOpen={true} onClose={vi.fn()} />);

    expect(screen.getByText(/Entity Search/i)).toBeInTheDocument();
    expect(screen.getByText(/Commands/i)).toBeInTheDocument();

    // Switch to Command Mode
    fireEvent.click(screen.getByText(/Commands/i));

    await waitFor(() => {
      expect(screen.getByText(/Navigate Home/i)).toBeInTheDocument();
      expect(screen.getByText(/Create Mission/i)).toBeInTheDocument();
    });
  });
});
