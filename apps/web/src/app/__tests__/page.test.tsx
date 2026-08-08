import { render, screen } from '@testing-library/react';
import Home from '../page';
import { describe, it, expect, vi } from 'vitest';

// Mock next/navigation
vi.mock('next/navigation', () => ({
  usePathname: () => '/',
  useRouter: () => ({
    push: vi.fn(),
  }),
}));

describe('Vapor Authenticated Application Shell', () => {
  it('renders application shell with sidebar and topbar title without errors', () => {
    render(<Home />);
    expect(screen.getByText(/VAPOR_OS // SHELL_READY/i)).toBeInTheDocument();
    expect(screen.getByText(/Authenticated Application Shell/i)).toBeInTheDocument();
    expect(screen.getByText(/Workspace Home/i)).toBeInTheDocument();
  });
});
