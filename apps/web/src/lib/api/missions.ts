import { apiClient } from './client';

export interface MissionActivity {
  id: string;
  mission_id: string;
  action: string;
  details: Record<string, unknown>;
  created_at: string;
}

export interface PlanStep {
  order: number;
  title: string;
  description: string;
}

export interface MissionPlan {
  id: string;
  mission_id: string;
  version: number;
  goal: string;
  summary: string;
  steps: PlanStep[];
  deliverables: string[];
  open_questions: string[];
  recommendations: string[];
  usage_metadata: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface MissionStep {
  id: string;
  mission_id: string;
  plan_version_id?: string | null;
  title: string;
  description: string;
  order: number;
  status: 'pending' | 'ready' | 'in_progress' | 'completed' | 'failed' | 'skipped';
  failure_reason?: string | null;
  output?: Record<string, unknown> | null;
  created_at: string;
  updated_at: string;
  started_at?: string | null;
  completed_at?: string | null;
}

export interface MissionExecution {
  id: string;
  mission_id: string;
  status: 'idle' | 'running' | 'paused' | 'completed' | 'failed' | 'cancelled';
  completed_steps_count: number;
  total_steps_count: number;
  created_at: string;
  updated_at: string;
  started_at?: string | null;
  completed_at?: string | null;
}

export interface MissionStepsPayload {
  execution?: MissionExecution | null;
  steps: MissionStep[];
}

export interface Mission {
  id: string;
  workspace_id: string;
  title: string;
  description: string;
  status: 'draft' | 'active' | 'completed' | 'archived';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  created_by: string;
  created_at: string;
  updated_at: string;
  completed_at?: string | null;
  activities: MissionActivity[];
  latest_plan?: MissionPlan | null;
}

export interface MissionListResponse {
  missions: Mission[];
  total: number;
}

export interface MissionCreateInput {
  title: string;
  description?: string;
  priority?: 'low' | 'medium' | 'high' | 'urgent';
}

export interface MissionUpdateInput {
  title?: string;
  description?: string;
  priority?: 'low' | 'medium' | 'high' | 'urgent';
  status?: 'draft' | 'active' | 'completed' | 'archived';
}

export async function fetchMissions(params?: {
  status?: string;
  priority?: string;
  search?: string;
}): Promise<MissionListResponse> {
  const query = new URLSearchParams();
  if (params?.status && params.status !== 'all') query.set('status', params.status);
  if (params?.priority && params.priority !== 'all') query.set('priority', params.priority);
  if (params?.search) query.set('search', params.search);

  const qStr = query.toString();
  return await apiClient<MissionListResponse>(`/missions${qStr ? `?${qStr}` : ''}`);
}

export async function createMission(input: MissionCreateInput): Promise<Mission> {
  return await apiClient<Mission>('/missions', {
    method: 'POST',
    body: JSON.stringify(input),
  });
}

export async function getMission(id: string): Promise<Mission> {
  return await apiClient<Mission>(`/missions/${id}`);
}

export async function updateMission(id: string, input: MissionUpdateInput): Promise<Mission> {
  return await apiClient<Mission>(`/missions/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(input),
  });
}

export async function completeMission(id: string): Promise<Mission> {
  return await apiClient<Mission>(`/missions/${id}/complete`, {
    method: 'POST',
  });
}

export async function archiveMission(id: string): Promise<Mission> {
  return await apiClient<Mission>(`/missions/${id}/archive`, {
    method: 'POST',
  });
}

export async function generateMissionPlan(id: string): Promise<MissionPlan> {
  return await apiClient<MissionPlan>(`/missions/${id}/plan`, {
    method: 'POST',
  });
}

export async function getMissionPlan(id: string): Promise<MissionPlan> {
  return await apiClient<MissionPlan>(`/missions/${id}/plan`);
}

export async function regenerateMissionPlan(id: string): Promise<MissionPlan> {
  return await apiClient<MissionPlan>(`/missions/${id}/plan/regenerate`, {
    method: 'POST',
  });
}

export async function convertPlanToSteps(id: string): Promise<MissionStepsPayload> {
  return await apiClient<MissionStepsPayload>(`/missions/${id}/steps`, {
    method: 'POST',
  });
}

export async function fetchMissionSteps(id: string): Promise<MissionStepsPayload> {
  return await apiClient<MissionStepsPayload>(`/missions/${id}/steps`);
}

export async function startExecution(id: string): Promise<MissionStepsPayload> {
  return await apiClient<MissionStepsPayload>(`/missions/${id}/start`, {
    method: 'POST',
  });
}

export async function pauseExecution(id: string): Promise<MissionStepsPayload> {
  return await apiClient<MissionStepsPayload>(`/missions/${id}/pause`, {
    method: 'POST',
  });
}

export async function cancelExecution(id: string): Promise<MissionStepsPayload> {
  return await apiClient<MissionStepsPayload>(`/missions/${id}/cancel`, {
    method: 'POST',
  });
}

export async function completeStep(stepId: string): Promise<MissionStepsPayload> {
  return await apiClient<MissionStepsPayload>(`/mission-steps/${stepId}/complete`, {
    method: 'POST',
  });
}

export async function skipStep(stepId: string): Promise<MissionStepsPayload> {
  return await apiClient<MissionStepsPayload>(`/mission-steps/${stepId}/skip`, {
    method: 'POST',
  });
}
