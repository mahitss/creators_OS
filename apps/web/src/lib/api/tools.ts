/**
 * KINETIQ Tool Fabric & Context/Memory Fabric V1 API Client
 */

import {
  ToolDefinition,
  AgentToolDiscoveryResponse,
  ToolCallAuditLog,
  ContextPreview,
  ContextSnapshot,
  MemoryRecord
} from '@vapor/types';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

async function fetchWithAuth(url: string, options: RequestInit = {}) {
  const defaultHeaders: Record<string, string> = {
    'Content-Type': 'application/json',
    'X-Workspace-Id': 'ws_default_workspace',
    'X-User-Id': 'usr_current_user',
    'X-User-Role': 'owner'
  };

  const res = await fetch(url, {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers
    }
  });

  if (!res.ok) {
    const errBody = await res.json().catch(() => ({ message: res.statusText }));
    throw new Error(errBody.message || `Request failed with status ${res.status}`);
  }

  return res.json();
}

export async function listTools(category?: string): Promise<{ tools: ToolDefinition[]; total: number }> {
  const q = category ? `?category=${encodeURIComponent(category)}` : '';
  return fetchWithAuth(`${API_BASE}/tools${q}`);
}

export async function getToolDetails(toolId: string): Promise<ToolDefinition> {
  return fetchWithAuth(`${API_BASE}/tools/${encodeURIComponent(toolId)}`);
}

export async function discoverAgentTools(agentId: string): Promise<AgentToolDiscoveryResponse> {
  return fetchWithAuth(`${API_BASE}/tools/agents/${encodeURIComponent(agentId)}/tools`);
}

export async function listToolAuditLogs(params?: {
  toolId?: string;
  agentRunId?: string;
  limit?: number;
}): Promise<{ logs: ToolCallAuditLog[]; total: number }> {
  const searchParams = new URLSearchParams();
  if (params?.toolId) searchParams.append('tool_id', params.toolId);
  if (params?.agentRunId) searchParams.append('agent_run_id', params.agentRunId);
  if (params?.limit) searchParams.append('limit', String(params.limit));

  const query = searchParams.toString() ? `?${searchParams.toString()}` : '';
  return fetchWithAuth(`${API_BASE}/tools/audit-logs${query}`);
}

export async function previewContext(payload: {
  agent_id: string;
  agent_version_id?: string;
  mission_id?: string;
  goal?: string;
  user_context?: Record<string, any>;
  max_context_tokens?: number;
}): Promise<ContextPreview> {
  return fetchWithAuth(`${API_BASE}/context/preview`, {
    method: 'POST',
    body: JSON.stringify(payload)
  });
}

export async function getContextSnapshot(agentRunId: string): Promise<ContextSnapshot> {
  return fetchWithAuth(`${API_BASE}/context/snapshots/${encodeURIComponent(agentRunId)}`);
}

export async function searchMemories(query: string, typeFilter?: string, limit: number = 10): Promise<{ memories: MemoryRecord[]; count: number; query: string }> {
  return fetchWithAuth(`${API_BASE}/memory/search`, {
    method: 'POST',
    body: JSON.stringify({
      query,
      type_filter: typeFilter,
      limit
    })
  });
}

export async function listMemories(params?: {
  type?: string;
  importance?: string;
  search?: string;
  archived?: boolean;
}): Promise<{ memories: MemoryRecord[]; total: number }> {
  const searchParams = new URLSearchParams();
  if (params?.type) searchParams.append('type', params.type);
  if (params?.importance) searchParams.append('importance', params.importance);
  if (params?.search) searchParams.append('search', params.search);
  if (params?.archived !== undefined) searchParams.append('archived', String(params.archived));

  const query = searchParams.toString() ? `?${searchParams.toString()}` : '';
  return fetchWithAuth(`${API_BASE}/memories${query}`);
}

export async function createMemory(payload: {
  type: string;
  title: string;
  content: string;
  importance?: string;
  source_type?: string;
  source_id?: string;
  confidence?: number;
}): Promise<MemoryRecord> {
  return fetchWithAuth(`${API_BASE}/memory`, {
    method: 'POST',
    body: JSON.stringify(payload)
  });
}

export async function deleteMemory(id: string): Promise<void> {
  await fetchWithAuth(`${API_BASE}/memory/${encodeURIComponent(id)}`, {
    method: 'DELETE'
  });
}
