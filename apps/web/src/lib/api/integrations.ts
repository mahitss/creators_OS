export interface IntegrationConnection {
  id: string;
  workspace_id: string;
  provider: 'google' | 'github' | 'youtube' | 'slack' | 'notion';
  status: 'connected' | 'expired' | 'revoked' | 'error' | 'disconnected';
  scopes: string[];
  external_account_id?: string | null;
  external_account_name?: string | null;
  connected_at?: string | null;
  last_synced_at?: string | null;
  last_sync_error?: string | null;
  created_at: string;
  updated_at: string;
}

export interface IntegrationListResponse {
  connections: IntegrationConnection[];
  total: number;
}

export interface OAuthConnectUrlResponse {
  authorization_url: string;
  state: string;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export async function fetchIntegrations(): Promise<IntegrationListResponse> {
  const res = await fetch(`${API_BASE_URL}/integrations`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
    cache: 'no-store',
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch integrations (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function fetchIntegration(provider: string): Promise<IntegrationConnection | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/integrations/${provider}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      cache: 'no-store',
    });

    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    return null;
  }
}

export async function connectIntegration(provider: string): Promise<OAuthConnectUrlResponse> {
  const res = await fetch(`${API_BASE_URL}/integrations/${provider}/connect`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to generate connect URL (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function handleOAuthCallback(provider: string, code: string, state: string): Promise<IntegrationConnection> {
  const res = await fetch(`${API_BASE_URL}/integrations/${provider}/callback?code=${code}&state=${state}`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`OAuth callback failed (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function disconnectIntegration(provider: string): Promise<IntegrationConnection> {
  const res = await fetch(`${API_BASE_URL}/integrations/${provider}/disconnect`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to disconnect integration (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function refreshIntegration(provider: string): Promise<IntegrationConnection> {
  const res = await fetch(`${API_BASE_URL}/integrations/${provider}/refresh`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to refresh integration (HTTP ${res.status})`);
  }

  return await res.json();
}
