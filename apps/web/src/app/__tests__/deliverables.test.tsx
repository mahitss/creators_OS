import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { DeliverableSuggestionsSection } from '../../components/missions/DeliverableSuggestionsSection';
import { describe, it, expect, vi } from 'vitest';

// Mock next/navigation
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: vi.fn(),
  }),
}));

describe('Deliverable Intelligence Suggestions View', () => {
  it('renders potential deliverable suggestions with Create Draft and Dismiss buttons', async () => {
    const suggestions: any = [
      {
        id: 'sugg_01',
        workspace_id: 'ws_test',
        mission_id: 'mis_test',
        type: 'report',
        title: 'Docker Adoption Research Report',
        reason: 'Completed research steps can be compiled into a report.',
        confidence: 0.9,
        status: 'pending',
        created_at: new Date().toISOString(),
      },
    ];

    render(<DeliverableSuggestionsSection suggestions={suggestions} onRefresh={vi.fn()} />);

    expect(screen.getByText(/Potential Deliverables/i)).toBeInTheDocument();
    expect(screen.getByText(/Docker Adoption Research Report/i)).toBeInTheDocument();
    expect(screen.getByText(/Create Draft/i)).toBeInTheDocument();
    expect(screen.getByText(/Dismiss/i)).toBeInTheDocument();
  });
});
