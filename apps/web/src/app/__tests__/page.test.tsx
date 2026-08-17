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
    expect(screen.getByText(/VAPOR/i)).toBeInTheDocument();
    expect(screen.getByText(/Executive Brief/i)).toBeInTheDocument();
  });
});
