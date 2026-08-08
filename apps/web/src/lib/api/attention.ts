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

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export async function fetchAttentionItems(statusFilter: string = 'open'): Promise<AttentionListResponse> {
  const query = new URLSearchParams();
  if (statusFilter && statusFilter !== 'all') query.set('status', statusFilter);

  const res = await fetch(`${API_BASE_URL}/attention?${query.toString()}`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
    cache: 'no-store',
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch attention items (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function fetchAttentionCount(): Promise<number> {
  try {
    const res = await fetch(`${API_BASE_URL}/attention/count`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      cache: 'no-store',
    });

    if (!res.ok) return 0;
    const data: AttentionCountResponse = await res.json();
    return data.open_count || 0;
  } catch (err) {
    return 0;
  }
}

export async function reconcileAttentionItems(): Promise<AttentionListResponse> {
  const res = await fetch(`${API_BASE_URL}/attention/reconcile`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to reconcile attention (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function resolveAttentionItem(id: string): Promise<AttentionItem> {
  const res = await fetch(`${API_BASE_URL}/attention/${id}/resolve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to resolve attention item (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function dismissAttentionItem(id: string): Promise<AttentionItem> {
  const res = await fetch(`${API_BASE_URL}/attention/${id}/dismiss`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to dismiss attention item (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function snoozeAttentionItem(id: string, minutes: number = 60): Promise<AttentionItem> {
  const res = await fetch(`${API_BASE_URL}/attention/${id}/snooze?minutes=${minutes}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to snooze attention item (HTTP ${res.status})`);
  }

  return await res.json();
}
