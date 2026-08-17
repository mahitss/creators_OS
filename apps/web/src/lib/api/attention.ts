import { apiClient, getApiBaseUrl, getDefaultHeaders } from './client';

export interface ActionLink {
  label: string;
  href: string;
}

export interface AttentionItem {
  id: string;
  workspace_id: string;
  type: 'mission_failed' | 'mission_paused' | 'step_failed' | 'approval_required' | 'memory_review' | 'deliverable_suggestion' | 'content_review' | 'system_error';
  title: string;
  description: string;
  severity: 'urgent' | 'high' | 'medium' | 'low';
  source_type: string;
  source_id: string;
  status: 'open' | 'snoozed' | 'resolved' | 'dismissed' | 'expired';
  primary_action: ActionLink;
  created_at: string;
  updated_at: string;
  snoozed_until?: string | null;
}

export interface AttentionListResponse {
  items: AttentionItem[];
  total: number;
  open_count: number;
}

export interface AttentionCountResponse {
  open_count: number;
}

export async function fetchAttentionItems(statusFilter: string = 'open'): Promise<AttentionListResponse> {
  const query = new URLSearchParams();
  if (statusFilter && statusFilter !== 'all') query.set('status', statusFilter);
  const qStr = query.toString();
  const endpoint = `/attention${qStr ? `?${qStr}` : ''}`;
  return await apiClient<AttentionListResponse>(endpoint);
}

export async function fetchAttentionCount(): Promise<number> {
  try {
    const data = await apiClient<AttentionCountResponse>('/attention/count');
    return data.open_count || 0;
  } catch (err) {
    return 0;
  }
}

export async function reconcileAttentionItems(): Promise<AttentionListResponse> {
  return await apiClient<AttentionListResponse>('/attention/reconcile', {
    method: 'POST',
  });
}

export async function resolveAttentionItem(id: string): Promise<AttentionItem> {
  return await apiClient<AttentionItem>(`/attention/${id}/resolve`, {
    method: 'POST',
  });
}

export async function dismissAttentionItem(id: string): Promise<AttentionItem> {
  return await apiClient<AttentionItem>(`/attention/${id}/dismiss`, {
    method: 'POST',
  });
}

export async function snoozeAttentionItem(id: string, minutes: number = 60): Promise<AttentionItem> {
  return await apiClient<AttentionItem>(`/attention/${id}/snooze?minutes=${minutes}`, {
    method: 'POST',
  });
}
