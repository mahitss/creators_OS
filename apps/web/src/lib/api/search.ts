import { apiClient } from './client';

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

export async function fetchSearchResults(query: string): Promise<SearchListResponse> {
  if (!query || !query.trim()) {
    return { results: [], total: 0 };
  }

  return await apiClient<SearchListResponse>(`/search?q=${encodeURIComponent(query.trim())}`);
}
