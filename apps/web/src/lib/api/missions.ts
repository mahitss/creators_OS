import { apiClient } from './client';

export type MissionStatus =
  | 'DRAFT'
  | 'QUEUED'
  | 'PLANNING'
  | 'RUNNING'
  | 'WAITING'
  | 'PAUSED'
  | 'COMPLETED'
  | 'FAILED'
  | 'CANCELLED'
  | 'draft'
  | 'active'
  | 'completed'
  | 'archived';

export type MissionPriority = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL' | 'low' | 'medium' | 'high' | 'urgent';

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
  step_type?: string;
  expected_output_type?: string;
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
  workspace_id?: string;
  plan_version_id?: string | null;
  step_number?: number;
  order: number;
  name?: string;
  title: string;
  description: string;
  step_type?: string;
  status: 'PENDING' | 'RUNNING' | 'COMPLETED' | 'FAILED' | 'SKIPPED' | 'pending' | 'ready' | 'in_progress' | 'completed' | 'failed' | 'skipped';
  input?: Record<string, unknown>;
  output?: Record<string, unknown> | null;
  error?: Record<string, unknown> | string | null;
  failure_reason?: string | null;
  retry_count?: number;
  max_retries?: number;
  token_usage?: {
    input_tokens: number;
    output_tokens: number;
    total_tokens: number;
  };
  cost_usd?: number;
  duration_ms?: number;
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

export interface MissionEvent {
  id: string;
  mission_id: string;
  workspace_id: string;
  step_id?: string | null;
  event_type: string;
  timestamp: string;
  payload: Record<string, unknown>;
}

export interface MissionResult {
  mission_id: string;
  status: string;
  result?: Record<string, unknown> | null;
  error?: Record<string, unknown> | string | null;
  progress: number;
  token_usage?: {
    input_tokens: number;
    output_tokens: number;
    total_tokens: number;
  };
  cost_usd: number;
  completed_at?: string | null;
}

export interface Mission {
  id: string;
  workspace_id: string;
  tenantId?: string;
  tenant_id?: string;
  title: string;
  name?: string;
  goal?: string;
  description: string;
  status: MissionStatus;
  priority: MissionPriority;
  agent_id?: string | null;
  agentId?: string | null;
  model?: string | null;
  context?: Record<string, unknown>;
  plan?: Record<string, unknown> | null;
  current_step?: number;
  currentStep?: number;
  progress?: number;
  created_by: string;
  createdBy?: string;
  created_at: string;
  createdAt?: string;
  updated_at: string;
  updatedAt?: string;
  started_at?: string | null;
  startedAt?: string | null;
  completed_at?: string | null;
  completedAt?: string | null;
  failed_at?: string | null;
  failedAt?: string | null;
  cancelled_at?: string | null;
  cancelledAt?: string | null;
  error?: Record<string, unknown> | string | null;
  result?: Record<string, unknown> | string | null;
  token_usage?: {
    input_tokens: number;
    output_tokens: number;
    total_tokens: number;
  };
  tokenUsage?: {
    inputTokens: number;
    outputTokens: number;
    totalTokens: number;
  };
  cost?: number;
  cost_usd?: number;
  metadata?: Record<string, unknown>;
  activities: MissionActivity[];
  latest_plan?: MissionPlan | null;
  execution_status?: string;
}

export interface MissionListResponse {
  missions: Mission[];
  total: number;
}

export interface MissionCreateInput {
  title?: string;
  name?: string;
  goal?: string;
  description?: string;
  priority?: string;
  agent_id?: string;
  agentId?: string;
  model?: string;
  context?: Record<string, unknown>;
  metadata?: Record<string, unknown>;
}

export interface MissionUpdateInput {
  title?: string;
  name?: string;
  goal?: string;
  description?: string;
  priority?: string;
  status?: string;
  agent_id?: string;
  model?: string;
  context?: Record<string, unknown>;
  metadata?: Record<string, unknown>;
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

export async function launchMission(id: string): Promise<Mission> {
  return await apiClient<Mission>(`/missions/${id}/launch`, {
    method: 'POST',
  });
}

export async function pauseMission(id: string): Promise<Mission> {
  return await apiClient<Mission>(`/missions/${id}/pause`, {
    method: 'POST',
  });
}

export async function resumeMission(id: string): Promise<Mission> {
  return await apiClient<Mission>(`/missions/${id}/resume`, {
    method: 'POST',
  });
}

export async function cancelMission(id: string): Promise<Mission> {
  return await apiClient<Mission>(`/missions/${id}/cancel`, {
    method: 'POST',
  });
}

export async function fetchMissionEvents(id: string): Promise<MissionEvent[]> {
  return await apiClient<MissionEvent[]>(`/missions/${id}/events`);
}

export async function fetchMissionResult(id: string): Promise<MissionResult> {
  return await apiClient<MissionResult>(`/missions/${id}/result`);
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
