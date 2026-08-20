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
  it('renders landing page with Kinetiq branding, hero headline, 7 sections, and CTA', () => {
    render(<LandingPage />);
    expect(screen.getAllByText(/KINETIQ/i).length).toBeGreaterThan(0);
    expect(screen.getByText(/THE INTELLIGENCE/i)).toBeInTheDocument();
    expect(screen.getAllByText(/ENTER KINETIQ/i).length).toBeGreaterThan(0);
    expect(screen.getByText(/ONE SYSTEM/i)).toBeInTheDocument();
    expect(screen.getByText(/FROM DECISION/i)).toBeInTheDocument();
    expect(screen.getByText(/AUTONOMY/i)).toBeInTheDocument();
    expect(screen.getByText(/THE ENTERPRISE/i)).toBeInTheDocument();
  });
});
