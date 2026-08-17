import { apiClient } from './client';
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

export async function fetchMissionDeliverableSuggestions(missionId: string): Promise<DeliverableSuggestionListResponse> {
  return await apiClient<DeliverableSuggestionListResponse>(`/missions/${missionId}/deliverable-suggestions`);
}

export async function analyzeMissionDeliverables(missionId: string): Promise<DeliverableSuggestion | null> {
  return await apiClient<DeliverableSuggestion | null>(`/missions/${missionId}/deliverable-suggestions/analyze`, {
    method: 'POST',
  });
}

export async function acceptDeliverableSuggestion(suggestionId: string): Promise<Content> {
  return await apiClient<Content>(`/deliverable-suggestions/${suggestionId}/accept`, {
    method: 'POST',
  });
}

export async function dismissDeliverableSuggestion(suggestionId: string): Promise<DeliverableSuggestion> {
  return await apiClient<DeliverableSuggestion>(`/deliverable-suggestions/${suggestionId}/dismiss`, {
    method: 'POST',
  });
}
