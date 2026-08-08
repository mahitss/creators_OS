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

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

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

  const res = await fetch(`${API_BASE_URL}/memories?${query.toString()}`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
    cache: 'no-store',
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch memories (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function createMemory(input: MemoryCreateInput): Promise<Memory> {
  const res = await fetch(`${API_BASE_URL}/memories`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input),
  });

  if (!res.ok) {
    throw new Error(`Failed to create memory (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function getMemory(id: string): Promise<Memory> {
  const res = await fetch(`${API_BASE_URL}/memories/${id}`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
    cache: 'no-store',
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch memory ${id} (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function updateMemory(id: string, input: Partial<MemoryCreateInput> & { is_archived?: boolean }): Promise<Memory> {
  const res = await fetch(`${API_BASE_URL}/memories/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input),
  });

  if (!res.ok) {
    throw new Error(`Failed to update memory (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function archiveMemory(id: string): Promise<Memory> {
  const res = await fetch(`${API_BASE_URL}/memories/${id}/archive`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to archive memory (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function restoreMemory(id: string): Promise<Memory> {
  const res = await fetch(`${API_BASE_URL}/memories/${id}/restore`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to restore memory (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function deleteMemory(id: string): Promise<void> {
  const res = await fetch(`${API_BASE_URL}/memories/${id}`, {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to delete memory (HTTP ${res.status})`);
  }
}

export async function fetchMemoryCandidates(): Promise<MemoryCandidateListResponse> {
  const res = await fetch(`${API_BASE_URL}/memory-candidates`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
    cache: 'no-store',
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch memory candidates (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function approveMemoryCandidate(id: string): Promise<Memory> {
  const res = await fetch(`${API_BASE_URL}/memory-candidates/${id}/approve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to approve candidate (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function rejectMemoryCandidate(id: string): Promise<void> {
  const res = await fetch(`${API_BASE_URL}/memory-candidates/${id}/reject`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to reject candidate (HTTP ${res.status})`);
  }
}
