import { apiClient } from './client';

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

export async function fetchGmailStatus(): Promise<GmailStatusResponse> {
  try {
    return await apiClient<GmailStatusResponse>('/gmail/status');
  } catch (err) {
    return { is_connected: false, thread_count: 0, unread_count: 0 };
  }
}

export async function fetchGmailThreads(filterType: string = 'all'): Promise<GmailThreadListResponse> {
  const query = new URLSearchParams();
  if (filterType && filterType !== 'all') query.set('filter', filterType);
  const qStr = query.toString();
  return await apiClient<GmailThreadListResponse>(`/gmail/threads${qStr ? `?${qStr}` : ''}`);
}

export async function fetchGmailMessage(id: string): Promise<GmailMessage> {
  return await apiClient<GmailMessage>(`/gmail/messages/${id}`);
}

export async function summarizeEmail(id: string): Promise<EmailSummaryResponse> {
  return await apiClient<EmailSummaryResponse>(`/gmail/messages/${id}/summarize`, {
    method: 'POST',
  });
}

export async function createMissionFromEmail(id: string): Promise<CreateMissionFromEmailResponse> {
  return await apiClient<CreateMissionFromEmailResponse>(`/gmail/messages/${id}/create-mission`, {
    method: 'POST',
  });
}

export async function syncGmail(): Promise<GmailStatusResponse> {
  return await apiClient<GmailStatusResponse>('/gmail/sync', {
    method: 'POST',
  });
}
