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

describe('KINETIQ — The Next Layer of Intelligence Landing Page', () => {
  it('renders single-screen cinematic landing page with exact headline, navigation, CTAs, and partner marks', () => {
    render(<LandingPage />);
    expect(screen.getByText(/The Next Layer/i)).toBeInTheDocument();
    expect(screen.getByText(/of Intelligence/i)).toBeInTheDocument();
    expect(screen.getAllByText(/Get Started/i).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/View Architecture/i).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/About/i).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/Features/i).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/FAQ/i).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/Contact/i).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/logoipsum/i).length).toBe(4);
  });
});
