export interface Content {
  id: string;
  workspace_id: string;
  mission_id?: string | null;
  mission_title?: string | null;
  title: string;
  type: 'article' | 'script' | 'social_post' | 'email' | 'report' | 'outline';
  status: 'draft' | 'in_review' | 'approved' | 'archived';
  content: string;
  created_by: string;
  created_at: string;
  updated_at: string;
  published_at?: string | null;
  archived_at?: string | null;
}

export interface ContentListResponse {
  content_items: Content[];
  total: number;
}

export interface ContentCreateInput {
  title: string;
  type: 'article' | 'script' | 'social_post' | 'email' | 'report' | 'outline';
  content?: string;
  mission_id?: string;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export async function fetchContentItems(params?: {
  type?: string;
  status?: string;
  mission_id?: string;
  search?: string;
}): Promise<ContentListResponse> {
  const query = new URLSearchParams();
  if (params?.type && params.type !== 'all') query.set('type', params.type);
  if (params?.status && params.status !== 'all') query.set('status', params.status);
  if (params?.mission_id) query.set('mission_id', params.mission_id);
  if (params?.search) query.set('search', params.search);

  const res = await fetch(`${API_BASE_URL}/content?${query.toString()}`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
    cache: 'no-store',
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch content items (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function createContentItem(input: ContentCreateInput): Promise<Content> {
  const res = await fetch(`${API_BASE_URL}/content`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input),
  });

  if (!res.ok) {
    throw new Error(`Failed to create content (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function getContentItem(id: string): Promise<Content> {
  const res = await fetch(`${API_BASE_URL}/content/${id}`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
    cache: 'no-store',
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch content item ${id} (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function updateContentItem(
  id: string,
  input: Partial<ContentCreateInput> & { status?: string }
): Promise<Content> {
  const res = await fetch(`${API_BASE_URL}/content/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input),
  });

  if (!res.ok) {
    throw new Error(`Failed to update content (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function archiveContentItem(id: string): Promise<Content> {
  const res = await fetch(`${API_BASE_URL}/content/${id}/archive`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to archive content (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function approveContentItem(id: string): Promise<Content> {
  const res = await fetch(`${API_BASE_URL}/content/${id}/approve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to approve content (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function generateContentAI(
  id: string,
  intent: 'draft' | 'rewrite' | 'expand' | 'summarize' | 'improve',
  customPrompt?: string
): Promise<Content> {
  const res = await fetch(`${API_BASE_URL}/content/${id}/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ intent, custom_prompt: customPrompt }),
  });

  if (!res.ok) {
    throw new Error(`Failed to generate AI content (HTTP ${res.status})`);
  }

  return await res.json();
}
