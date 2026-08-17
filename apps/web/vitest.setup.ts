import '@testing-library/jest-dom';

// Graceful fallback mock for global fetch in unit test environment
const mockFetchResponse = (urlStr: string) => {
  return {
    ok: true,
    status: 200,
    json: async () => ({
      items: [],
      content_items: [],
      deliverables: [],
      suggestions: [],
      missions: [],
      memories: [],
      threads: [],
      integrations: [],
      files: [],
      results: [],
      open_count: 0,
      total: 0,
      is_connected: true,
      thread_count: 0,
      unread_count: 0,
      user_name: 'Alex',
      greeting: 'Welcome, Alex.',
      summary_statement: 'Vapor is observing your workspace context.',
      needs_attention: [],
      primary_recommendation: null,
      learned_memories: [],
      recent_activity: [],
      quick_actions: [
        { id: 'qa-missions', label: 'Missions Orchestrator', href: '/missions', icon: '⚡' },
        { id: 'qa-content', label: 'Studio Content Canvas', href: '/content', icon: '🎨' },
        { id: 'qa-memory', label: 'Context Vault Memory', href: '/memory', icon: '🧠' },
        { id: 'qa-settings', label: 'System Settings', href: '/settings', icon: '⚙️' },
      ],
      is_quiet_state: true,
    }),
    text: async () => '',
    blob: async () => new Blob(),
    headers: new Headers(),
  };
};

const customFetch: typeof global.fetch = async (url, init) => {
  const urlStr = typeof url === 'string' ? url : url.toString();
  return mockFetchResponse(urlStr) as any;
};

// Set on global and globalThis
global.fetch = customFetch;
globalThis.fetch = customFetch;
if (typeof window !== 'undefined') {
  window.fetch = customFetch;
}
