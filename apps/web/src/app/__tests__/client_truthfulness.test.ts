import { describe, it, expect, vi } from 'vitest';
import { apiClient, ApiError, ApiConnectionError } from '../../lib/api/client';
import { fetchExecutiveBrief } from '../../lib/api/home';

describe('API Failure-State Truthfulness & Retry Logic', () => {
  it('throws ApiConnectionError when network fails without swallowing into fake empty state', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('Failed to fetch')));

    await expect(fetchExecutiveBrief('Alex')).rejects.toThrow();
  });

  it('throws ApiError when backend returns 500 server error', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error',
        json: async () => ({ message: 'Core kernel failure', error_code: 'ERR_KERNEL_DOWN' }),
      })
    );

    await expect(fetchExecutiveBrief('Alex')).rejects.toThrow('Core kernel failure');
  });

  it('successfully returns data on operational retry', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: true,
        status: 200,
        json: async () => ({
          user_name: 'Alex',
          greeting: 'Welcome back, Alex.',
          summary_statement: 'Kernel active.',
          needs_attention: [],
          primary_recommendation: null,
          learned_memories: [],
          recent_activity: [],
          quick_actions: [],
          is_quiet_state: true,
        }),
      })
    );

    const brief = await fetchExecutiveBrief('Alex');
    expect(brief.greeting).toBe('Welcome back, Alex.');
  });
});
