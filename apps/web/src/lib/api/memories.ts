import { apiClient } from './client';

export interface Memory {
  id: string;
  workspace_id: string;
  type: 'preference' | 'fact' | 'decision' | 'goal' | 'insight' | 'lesson' | 'relationship' | 'context';
  title: string;
  content: string;
  source_type: string;
  source_id?: string | null;
  importance: 'low' | 'medium' | 'high' | 'critical';
  is_archived: boolean;
  created_at: string;
  updated_at: string;
  last_accessed_at: string;
  expires_at?: string | null;
  metadata_dict?: Record<string, unknown>;
}

export interface MemoryListResponse {
  memories: Memory[];
  total: number;
}

export interface MemoryCandidate {
  id: string;
  workspace_id: string;
  source_type: string;
  source_id?: string | null;
  type: string;
  title: string;
  content: string;
  confidence: number;
  status: string;
  created_at: string;
}

export interface MemoryCandidateListResponse {
  candidates: MemoryCandidate[];
  total: number;
}

export interface MemoryCreateInput {
  type: 'preference' | 'fact' | 'decision' | 'goal' | 'insight' | 'lesson' | 'relationship' | 'context';
  title: string;
  content: string;
  importance?: 'low' | 'medium' | 'high' | 'critical';
  source_type?: string;
  source_id?: string;
}

export async function fetchMemories(params?: {
  type?: string;
  importance?: string;
  search?: string;
  archived?: boolean;
}): Promise<MemoryListResponse> {
  const query = new URLSearchParams();
  if (params?.type && params.type !== 'all') query.set('type', params.type);
  if (params?.importance && params.importance !== 'all') query.set('importance', params.importance);
  if (params?.search) query.set('search', params.search);
  if (params?.archived) query.set('archived', 'true');

  const qStr = query.toString();
  return await apiClient<MemoryListResponse>(`/memories${qStr ? `?${qStr}` : ''}`);
}

export async function createMemory(input: MemoryCreateInput): Promise<Memory> {
  return await apiClient<Memory>('/memories', {
    method: 'POST',
    body: JSON.stringify(input),
  });
}

export async function getMemory(id: string): Promise<Memory> {
  return await apiClient<Memory>(`/memories/${id}`);
}

export async function updateMemory(id: string, input: Partial<MemoryCreateInput> & { is_archived?: boolean }): Promise<Memory> {
  return await apiClient<Memory>(`/memories/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(input),
  });
}

export async function archiveMemory(id: string): Promise<Memory> {
  return await apiClient<Memory>(`/memories/${id}/archive`, {
    method: 'POST',
  });
}

export async function restoreMemory(id: string): Promise<Memory> {
  return await apiClient<Memory>(`/memories/${id}/restore`, {
    method: 'POST',
  });
}

export async function deleteMemory(id: string): Promise<void> {
  await apiClient<void>(`/memories/${id}`, {
    method: 'DELETE',
  });
}

export async function fetchMemoryCandidates(): Promise<MemoryCandidateListResponse> {
  return await apiClient<MemoryCandidateListResponse>('/memory-candidates');
}

export async function approveMemoryCandidate(id: string): Promise<Memory> {
  return await apiClient<Memory>(`/memory-candidates/${id}/approve`, {
    method: 'POST',
  });
}

export async function rejectMemoryCandidate(id: string): Promise<void> {
  await apiClient<void>(`/memory-candidates/${id}/reject`, {
    method: 'POST',
  });
}
