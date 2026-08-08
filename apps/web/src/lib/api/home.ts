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

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export async function fetchExecutiveBrief(userName: string = 'Alex'): Promise<ExecutiveBriefResponse> {
  try {
    const res = await fetch(`${API_BASE_URL}/home/brief?user_name=${encodeURIComponent(userName)}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      cache: 'no-store',
    });

    if (!res.ok) {
      throw new Error(`Failed to load Executive Brief (HTTP ${res.status})`);
    }

    return await res.json();
  } catch (err) {
    return {
      user_name: userName,
      greeting: `Welcome, ${userName}.`,
      summary_statement: 'Vapor is observing your workspace context.',
      needs_attention: [],
      primary_recommendation: null,
      learned_memories: [],
      recent_activity: [],
      quick_actions: [
        { id: 'qa-missions', label: 'Missions Orchestrator', href: '/missions', icon: '⚡' },
        { id: 'qa-content', label: 'Studio Content Canvas', href: '/content', icon: '🎨' },
        { id: 'qa-memory', label: 'Context Vault Memory', href: '/memory', icon: '🧠' },
        { id: 'qa-settings', label: 'System Settings', href: '/settings', icon: '⚙️' },
      ],
      is_quiet_state: true,
    };
  }
}
