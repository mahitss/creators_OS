import { apiClient } from './client';

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

export async function fetchIntegrations(): Promise<IntegrationListResponse> {
  return await apiClient<IntegrationListResponse>('/integrations');
}

export async function fetchIntegration(provider: string): Promise<IntegrationConnection | null> {
  try {
    return await apiClient<IntegrationConnection>(`/integrations/${provider}`);
  } catch (err) {
    return null;
  }
}

export async function connectIntegration(provider: string): Promise<OAuthConnectUrlResponse> {
  return await apiClient<OAuthConnectUrlResponse>(`/integrations/${provider}/connect`, {
    method: 'POST',
  });
}

export async function handleOAuthCallback(provider: string, code: string, state: string): Promise<IntegrationConnection> {
  return await apiClient<IntegrationConnection>(`/integrations/${provider}/callback?code=${code}&state=${state}`);
}

export async function disconnectIntegration(provider: string): Promise<IntegrationConnection> {
  return await apiClient<IntegrationConnection>(`/integrations/${provider}/disconnect`, {
    method: 'POST',
  });
}

export async function refreshIntegration(provider: string): Promise<IntegrationConnection> {
  return await apiClient<IntegrationConnection>(`/integrations/${provider}/refresh`, {
    method: 'POST',
  });
}
