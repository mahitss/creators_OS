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

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export async function fetchMissions(params?: {
  status?: string;
  priority?: string;
  search?: string;
}): Promise<MissionListResponse> {
  const query = new URLSearchParams();
  if (params?.status && params.status !== 'all') query.set('status', params.status);
  if (params?.priority && params.priority !== 'all') query.set('priority', params.priority);
  if (params?.search) query.set('search', params.search);

  const res = await fetch(`${API_BASE_URL}/missions?${query.toString()}`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
    cache: 'no-store',
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch missions (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function createMission(input: MissionCreateInput): Promise<Mission> {
  const res = await fetch(`${API_BASE_URL}/missions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input),
  });

  if (!res.ok) {
    throw new Error(`Failed to create mission (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function getMission(id: string): Promise<Mission> {
  const res = await fetch(`${API_BASE_URL}/missions/${id}`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
    cache: 'no-store',
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch mission ${id} (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function updateMission(id: string, input: MissionUpdateInput): Promise<Mission> {
  const res = await fetch(`${API_BASE_URL}/missions/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input),
  });

  if (!res.ok) {
    throw new Error(`Failed to update mission (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function completeMission(id: string): Promise<Mission> {
  const res = await fetch(`${API_BASE_URL}/missions/${id}/complete`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to complete mission (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function archiveMission(id: string): Promise<Mission> {
  const res = await fetch(`${API_BASE_URL}/missions/${id}/archive`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to archive mission (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function generateMissionPlan(id: string): Promise<MissionPlan> {
  const res = await fetch(`${API_BASE_URL}/missions/${id}/plan`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to generate mission plan (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function getMissionPlan(id: string): Promise<MissionPlan> {
  const res = await fetch(`${API_BASE_URL}/missions/${id}/plan`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
    cache: 'no-store',
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch mission plan (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function regenerateMissionPlan(id: string): Promise<MissionPlan> {
  const res = await fetch(`${API_BASE_URL}/missions/${id}/plan/regenerate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to regenerate mission plan (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function convertPlanToSteps(id: string): Promise<MissionStepsPayload> {
  const res = await fetch(`${API_BASE_URL}/missions/${id}/steps`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to convert plan to steps (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function fetchMissionSteps(id: string): Promise<MissionStepsPayload> {
  const res = await fetch(`${API_BASE_URL}/missions/${id}/steps`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
    cache: 'no-store',
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch mission steps (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function startExecution(id: string): Promise<MissionStepsPayload> {
  const res = await fetch(`${API_BASE_URL}/missions/${id}/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to start execution (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function pauseExecution(id: string): Promise<MissionStepsPayload> {
  const res = await fetch(`${API_BASE_URL}/missions/${id}/pause`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to pause execution (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function cancelExecution(id: string): Promise<MissionStepsPayload> {
  const res = await fetch(`${API_BASE_URL}/missions/${id}/cancel`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to cancel execution (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function completeStep(stepId: string): Promise<MissionStepsPayload> {
  const res = await fetch(`${API_BASE_URL}/mission-steps/${stepId}/complete`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to complete step (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function skipStep(stepId: string): Promise<MissionStepsPayload> {
  const res = await fetch(`${API_BASE_URL}/mission-steps/${stepId}/skip`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to skip step (HTTP ${res.status})`);
  }

  return await res.json();
}
