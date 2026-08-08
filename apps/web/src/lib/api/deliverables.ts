import { Content } from './content';

export interface DeliverableSuggestion {
  id: string;
  workspace_id: string;
  mission_id: string;
  type: 'article' | 'script' | 'social_post' | 'email' | 'report' | 'outline';
  title: string;
  reason: string;
  source_data?: Record<string, unknown>;
  confidence: number;
  status: 'pending' | 'accepted' | 'dismissed' | 'expired';
  created_at: string;
}

export interface DeliverableSuggestionListResponse {
  suggestions: DeliverableSuggestion[];
  total: number;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export async function fetchMissionDeliverableSuggestions(missionId: string): Promise<DeliverableSuggestionListResponse> {
  const res = await fetch(`${API_BASE_URL}/missions/${missionId}/deliverable-suggestions`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
    cache: 'no-store',
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch deliverable suggestions (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function analyzeMissionDeliverables(missionId: string): Promise<DeliverableSuggestion | null> {
  const res = await fetch(`${API_BASE_URL}/missions/${missionId}/deliverable-suggestions/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to analyze deliverable intelligence (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function acceptDeliverableSuggestion(suggestionId: string): Promise<Content> {
  const res = await fetch(`${API_BASE_URL}/deliverable-suggestions/${suggestionId}/accept`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to accept deliverable suggestion (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function dismissDeliverableSuggestion(suggestionId: string): Promise<DeliverableSuggestion> {
  const res = await fetch(`${API_BASE_URL}/deliverable-suggestions/${suggestionId}/dismiss`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to dismiss deliverable suggestion (HTTP ${res.status})`);
  }

  return await res.json();
}
