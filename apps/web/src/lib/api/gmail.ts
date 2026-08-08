export interface GmailThread {
  id: string;
  workspace_id: string;
  external_thread_id: string;
  subject: string;
  last_message_at: string;
  message_count: number;
  snippet: string;
}

export interface GmailMessage {
  id: string;
  workspace_id: string;
  thread_id: string;
  external_message_id: string;
  sender_name: string;
  sender_email: string;
  subject: string;
  snippet: string;
  received_at: string;
  is_unread: boolean;
  label_ids: string[];
  ai_classification: 'needs_response' | 'informational' | 'important' | 'low_priority';
  ai_summary?: string | null;
  full_body?: string | null;
}

export interface GmailThreadListResponse {
  threads: GmailThread[];
  total: number;
}

export interface GmailStatusResponse {
  is_connected: boolean;
  last_synced_at?: string | null;
  thread_count: number;
  unread_count: number;
}

export interface EmailSummaryResponse {
  message_id: string;
  classification: string;
  importance: string;
  summary: string;
  reason: string;
}

export interface CreateMissionFromEmailResponse {
  mission_id: string;
  title: string;
  description: string;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export async function fetchGmailStatus(): Promise<GmailStatusResponse> {
  try {
    const res = await fetch(`${API_BASE_URL}/gmail/status`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      cache: 'no-store',
    });

    if (!res.ok) return { is_connected: false, thread_count: 0, unread_count: 0 };
    return await res.json();
  } catch (err) {
    return { is_connected: false, thread_count: 0, unread_count: 0 };
  }
}

export async function fetchGmailThreads(filterType: string = 'all'): Promise<GmailThreadListResponse> {
  const query = new URLSearchParams();
  if (filterType && filterType !== 'all') query.set('filter', filterType);

  const res = await fetch(`${API_BASE_URL}/gmail/threads?${query.toString()}`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
    cache: 'no-store',
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch Gmail threads (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function fetchGmailMessage(id: string): Promise<GmailMessage> {
  const res = await fetch(`${API_BASE_URL}/gmail/messages/${id}`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
    cache: 'no-store',
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch Gmail message (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function summarizeEmail(id: string): Promise<EmailSummaryResponse> {
  const res = await fetch(`${API_BASE_URL}/gmail/messages/${id}/summarize`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to summarize email (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function createMissionFromEmail(id: string): Promise<CreateMissionFromEmailResponse> {
  const res = await fetch(`${API_BASE_URL}/gmail/messages/${id}/create-mission`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to create mission from email (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function syncGmail(): Promise<GmailStatusResponse> {
  const res = await fetch(`${API_BASE_URL}/gmail/sync`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to sync Gmail (HTTP ${res.status})`);
  }

  return await res.json();
}
