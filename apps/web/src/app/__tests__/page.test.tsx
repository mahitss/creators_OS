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

describe('Kinetiq Enterprise Intelligence Landing Page', () => {
  it('renders full 7-section architectural landing page with branding, 3D core, telemetry, and CTAs', () => {
    render(<LandingPage />);
    expect(screen.getAllByText(/KINETIQ/i).length).toBeGreaterThan(0);
    expect(screen.getByText(/THE INTELLIGENCE/i)).toBeInTheDocument();
    expect(screen.getAllByText(/ENTER KINETIQ/i).length).toBeGreaterThan(0);
    expect(screen.getByText(/ONE SYSTEM/i)).toBeInTheDocument();
    expect(screen.getByText(/INTELLIGENCE THAT/i)).toBeInTheDocument();
    expect(screen.getByText(/FROM DECISION/i)).toBeInTheDocument();
    expect(screen.getByText(/AUTONOMY/i)).toBeInTheDocument();
    expect(screen.getByText(/THE OPERATING LAYER/i)).toBeInTheDocument();
  });
});
