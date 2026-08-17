import { apiClient } from './client';

export interface ActionLink {
  label: string;
  href: string;
}

export interface AttentionItem {
  id: string;
  title: string;
  context: string;
  why_it_matters: string;
  primary_action: ActionLink;
  secondary_action?: ActionLink | null;
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
}

export interface ActivityItem {
  id: string;
  title: string;
  category: string;
  timestamp: string;
  status: string;
}

export interface QuickActionItem {
  id: string;
  label: string;
  href: string;
  icon: string;
}

export interface RecommendationItem {
  id: string;
  title: string;
  reason: string;
  action_label: string;
  action_href: string;
}

export interface LearnedMemoryItem {
  id: string;
  title: string;
  content: string;
  type: string;
  updated_at: string;
}

export interface ExecutiveBriefResponse {
  user_name: string;
  greeting: string;
  summary_statement: string;
  needs_attention: AttentionItem[];
  primary_recommendation?: RecommendationItem | null;
  learned_memories: LearnedMemoryItem[];
  recent_activity: ActivityItem[];
  quick_actions: QuickActionItem[];
  is_quiet_state: boolean;
}

export async function fetchExecutiveBrief(userName: string = 'Alex'): Promise<ExecutiveBriefResponse> {
  return await apiClient<ExecutiveBriefResponse>(
    `/home/brief?user_name=${encodeURIComponent(userName)}`
  );
}
