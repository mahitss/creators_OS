import { apiClient } from './client';

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

  const qStr = query.toString();
  return await apiClient<ContentListResponse>(`/content${qStr ? `?${qStr}` : ''}`);
}

export async function createContentItem(input: ContentCreateInput): Promise<Content> {
  return await apiClient<Content>('/content', {
    method: 'POST',
    body: JSON.stringify(input),
  });
}

export async function getContentItem(id: string): Promise<Content> {
  return await apiClient<Content>(`/content/${id}`);
}

export async function updateContentItem(
  id: string,
  input: Partial<ContentCreateInput> & { status?: string }
): Promise<Content> {
  return await apiClient<Content>(`/content/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(input),
  });
}

export async function archiveContentItem(id: string): Promise<Content> {
  return await apiClient<Content>(`/content/${id}/archive`, {
    method: 'POST',
  });
}

export async function approveContentItem(id: string): Promise<Content> {
  return await apiClient<Content>(`/content/${id}/approve`, {
    method: 'POST',
  });
}

export async function generateContentAI(
  id: string,
  intent: 'draft' | 'rewrite' | 'expand' | 'summarize' | 'improve',
  customPrompt?: string
): Promise<Content> {
  return await apiClient<Content>(`/content/${id}/generate`, {
    method: 'POST',
    body: JSON.stringify({ intent, custom_prompt: customPrompt }),
  });
}
