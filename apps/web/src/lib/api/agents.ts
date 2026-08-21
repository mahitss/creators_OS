import { Agent, AgentVersion, AgentRun, AgentObservation, AgentEvent } from '@vapor/types';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

function getHeaders(): HeadersInit {
  return {
    'Content-Type': 'application/json',
    'X-Workspace-Id': typeof window !== 'undefined' ? localStorage.getItem('vapor_workspace_id') || 'ws_default_01' : 'ws_default_01',
    'X-User-Id': typeof window !== 'undefined' ? localStorage.getItem('vapor_user_id') || 'usr_default_01' : 'usr_default_01',
  };
}

export interface FetchAgentsParams {
  status?: string;
}

export interface CreateAgentPayload {
  name: string;
  description?: string;
  system_instructions: string;
  capabilities?: string[];
  allowed_tools?: string[];
  allowed_models?: string[];
  max_steps?: number;
  max_runtime_seconds?: number;
  max_token_budget?: number;
}

export interface UpdateAgentPayload {
  name?: string;
  description?: string;
  status?: string;
  system_instructions?: string;
  capabilities?: string[];
  allowed_tools?: string[];
  allowed_models?: string[];
  max_steps?: number;
  max_runtime_seconds?: number;
  max_token_budget?: number;
}

export interface CreateAgentRunPayload {
  agent_id: string;
  agent_version_id?: string;
  mission_id?: string;
  goal?: string;
  context?: Record<string, any>;
}

export async function fetchAgents(params?: FetchAgentsParams): Promise<Agent[]> {
  const query = new URLSearchParams();
  if (params?.status && params.status !== 'all') {
    query.set('status', params.status);
  }
  const url = `${API_BASE}/api/v1/agents${query.toString() ? `?${query.toString()}` : ''}`;
  const res = await fetch(url, { headers: getHeaders() });
  if (!res.ok) {
    throw new Error(`Failed to fetch agents: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchAgent(id: string): Promise<Agent> {
  const res = await fetch(`${API_BASE}/api/v1/agents/${id}`, { headers: getHeaders() });
  if (!res.ok) {
    throw new Error(`Failed to fetch agent ${id}: ${res.statusText}`);
  }
  return res.json();
}

export async function createAgent(payload: CreateAgentPayload): Promise<Agent> {
  const res = await fetch(`${API_BASE}/api/v1/agents`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Failed to create agent: ${res.statusText}`);
  }
  return res.json();
}

export async function updateAgent(id: string, payload: UpdateAgentPayload): Promise<Agent> {
  const res = await fetch(`${API_BASE}/api/v1/agents/${id}`, {
    method: 'PATCH',
    headers: getHeaders(),
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Failed to update agent: ${res.statusText}`);
  }
  return res.json();
}

export async function pauseAgent(id: string): Promise<Agent> {
  const res = await fetch(`${API_BASE}/api/v1/agents/${id}/pause`, {
    method: 'POST',
    headers: getHeaders(),
  });
  if (!res.ok) {
    throw new Error(`Failed to pause agent: ${res.statusText}`);
  }
  return res.json();
}

export async function resumeAgent(id: string): Promise<Agent> {
  const res = await fetch(`${API_BASE}/api/v1/agents/${id}/resume`, {
    method: 'POST',
    headers: getHeaders(),
  });
  if (!res.ok) {
    throw new Error(`Failed to resume agent: ${res.statusText}`);
  }
  return res.json();
}

export async function disableAgent(id: string): Promise<Agent> {
  const res = await fetch(`${API_BASE}/api/v1/agents/${id}/disable`, {
    method: 'POST',
    headers: getHeaders(),
  });
  if (!res.ok) {
    throw new Error(`Failed to disable agent: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchAgentVersions(id: string): Promise<AgentVersion[]> {
  const res = await fetch(`${API_BASE}/api/v1/agents/${id}/versions`, { headers: getHeaders() });
  if (!res.ok) {
    throw new Error(`Failed to fetch agent versions: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchAgentRuns(params?: { agentId?: string; missionId?: string; status?: string }): Promise<AgentRun[]> {
  const query = new URLSearchParams();
  if (params?.agentId) query.set('agent_id', params.agentId);
  if (params?.missionId) query.set('mission_id', params.missionId);
  if (params?.status && params.status !== 'all') query.set('status', params.status);

  const url = `${API_BASE}/api/v1/agent-runs${query.toString() ? `?${query.toString()}` : ''}`;
  const res = await fetch(url, { headers: getHeaders() });
  if (!res.ok) {
    throw new Error(`Failed to fetch agent runs: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchAgentRun(id: string): Promise<AgentRun & { observations: AgentObservation[]; events: AgentEvent[] }> {
  const res = await fetch(`${API_BASE}/api/v1/agent-runs/${id}`, { headers: getHeaders() });
  if (!res.ok) {
    throw new Error(`Failed to fetch agent run ${id}: ${res.statusText}`);
  }
  return res.json();
}

export async function createAgentRun(payload: CreateAgentRunPayload): Promise<AgentRun> {
  const res = await fetch(`${API_BASE}/api/v1/agent-runs`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Failed to create agent run: ${res.statusText}`);
  }
  return res.json();
}

export async function pauseAgentRun(id: string): Promise<AgentRun> {
  const res = await fetch(`${API_BASE}/api/v1/agent-runs/${id}/pause`, {
    method: 'POST',
    headers: getHeaders(),
  });
  if (!res.ok) {
    throw new Error(`Failed to pause run: ${res.statusText}`);
  }
  return res.json();
}

export async function resumeAgentRun(id: string): Promise<AgentRun> {
  const res = await fetch(`${API_BASE}/api/v1/agent-runs/${id}/resume`, {
    method: 'POST',
    headers: getHeaders(),
  });
  if (!res.ok) {
    throw new Error(`Failed to resume run: ${res.statusText}`);
  }
  return res.json();
}

export async function cancelAgentRun(id: string): Promise<AgentRun> {
  const res = await fetch(`${API_BASE}/api/v1/agent-runs/${id}/cancel`, {
    method: 'POST',
    headers: getHeaders(),
  });
  if (!res.ok) {
    throw new Error(`Failed to cancel run: ${res.statusText}`);
  }
  return res.json();
}
