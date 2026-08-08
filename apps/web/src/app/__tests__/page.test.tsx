import { render, screen } from '@testing-library/react';
import Home from '../page';
import { describe, it, expect } from 'vitest';

describe('Vapor Web Application Shell', () => {
  it('renders minimal application shell without errors', () => {
    render(<Home />);
    expect(screen.getByText(/VAPOR_OS // KERNEL_ACTIVE/i)).toBeInTheDocument();
    expect(screen.getByText(/Vapor OS Platform Foundation/i)).toBeInTheDocument();
  });
});
