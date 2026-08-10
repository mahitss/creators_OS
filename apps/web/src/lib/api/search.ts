export interface SearchResult {
  type: 'mission' | 'content' | 'memory' | 'attention';
  id: string;
  title: string;
  description: string;
  url: string;
  updated_at: string;
}

export interface SearchListResponse {
  results: SearchResult[];
  total: number;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export async function fetchSearchResults(query: string): Promise<SearchListResponse> {
  if (!query || !query.trim()) {
    return { results: [], total: 0 };
  }

  const res = await fetch(`${API_BASE_URL}/search?q=${encodeURIComponent(query.trim())}`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
    cache: 'no-store',
  });

  if (!res.ok) {
    throw new Error(`Search request failed (HTTP ${res.status})`);
  }

  return await res.json();
}
