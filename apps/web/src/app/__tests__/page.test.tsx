import { render, screen } from '@testing-library/react';
import LandingPage from '../page';
import { describe, it, expect, vi } from 'vitest';

// Mock next/navigation
vi.mock('next/navigation', () => ({
  usePathname: () => '/',
  useRouter: () => ({
    push: vi.fn(),
  }),
}));

describe('Kinetiq Public Landing Page', () => {
  it('renders landing page with Kinetiq branding, hero headline, and CTA', () => {
    render(<LandingPage />);
    expect(screen.getAllByText(/KINETIQ/i).length).toBeGreaterThan(0);
    expect(screen.getByText(/Spatial AI Operating System/i)).toBeInTheDocument();
    expect(screen.getAllByText(/Enter Kinetiq/i).length).toBeGreaterThan(0);
  });
});
