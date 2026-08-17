/**
 * Vapor OS Centralized API Client
 * Authoritative client for all frontend API communication with the Core Kernel.
 */

export class ApiError extends Error {
  public status: number;
  public errorCode?: string;
  public details?: unknown;

  constructor(message: string, status: number = 500, errorCode?: string, details?: unknown) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.errorCode = errorCode;
    this.details = details;
  }
}

export class ApiConnectionError extends ApiError {
  constructor(message: string = 'Unable to connect to Vapor OS API. Verify the backend service is running.') {
    super(message, 503, 'CONNECTION_REFUSED');
    this.name = 'ApiConnectionError';
  }
}

export function getApiBaseUrl(): string {
  // If explicitly configured with absolute or relative URL
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL;
  }
  // In browser, default to '/api/v1' so Next.js proxy rewrites route seamlessly
  if (typeof window !== 'undefined') {
    return '/api/v1';
  }
  // In SSR / server context, connect to internal backend target
  return process.env.API_INTERNAL_URL || (process.env.NODE_ENV === 'production' ? 'http://vapor-api:8000/api/v1' : 'http://127.0.0.1:8000/api/v1');
}

/**
 * Dynamically resolves authentication and tenant headers from session context.
 * In development / test mode, defaults to developer test identities if not set.
 * In production mode, extracts exclusively from authenticated user session.
 */
export function getDefaultHeaders(): Record<string, string> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  if (typeof window !== 'undefined') {
    const isDev = process.env.NODE_ENV === 'development' || process.env.NODE_ENV === 'test';
    
    // Dynamically derive from active authenticated session / storage
    const activeWorkspace = window.sessionStorage?.getItem('vapor_workspace_id') || 
                            window.localStorage?.getItem('vapor_workspace_id') ||
                            (isDev ? 'ws_default_01' : undefined);
                            
    const activeUser = window.sessionStorage?.getItem('vapor_user_id') || 
                       window.localStorage?.getItem('vapor_user_id') ||
                       (isDev ? 'usr_alex' : undefined);
                       
    const authToken = window.sessionStorage?.getItem('vapor_auth_token') || 
                      window.localStorage?.getItem('vapor_auth_token');

    if (activeWorkspace) headers['X-Workspace-Id'] = activeWorkspace;
    if (activeUser) headers['X-User-Id'] = activeUser;
    if (authToken) headers['Authorization'] = `Bearer ${authToken}`;
  } else {
    // SSR fallback for development / test builds
    if (process.env.NODE_ENV === 'development' || process.env.NODE_ENV === 'test') {
      headers['X-Workspace-Id'] = process.env.DEFAULT_WORKSPACE_ID || 'ws_default_01';
      headers['X-User-Id'] = process.env.DEFAULT_USER_ID || 'usr_alex';
    }
  }

  return headers;
}

export async function apiClient<T = any>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const baseUrl = getApiBaseUrl();
  const normalizedEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
  
  // Clean full URL construction
  const url = baseUrl.endsWith('/')
    ? `${baseUrl.slice(0, -1)}${normalizedEndpoint}`
    : `${baseUrl}${normalizedEndpoint}`;

  const headers = {
    ...getDefaultHeaders(),
    ...(options.headers as Record<string, string> || {}),
  };

  let res: Response;
  try {
    res = await fetch(url, {
      ...options,
      headers,
      cache: options.cache || 'no-store',
    });
  } catch (networkErr: any) {
    console.error(`[API Network Error] ${options.method || 'GET'} ${url}:`, networkErr);
    throw new ApiConnectionError(`Connection failed for ${normalizedEndpoint}. Verify backend is operational.`);
  }

  if (!res.ok) {
    let errorData: any = null;
    try {
      errorData = await res.json();
    } catch {
      // Body not JSON
    }
    const message = errorData?.message || `HTTP ${res.status}: ${res.statusText || 'API Request Failed'}`;
    const code = errorData?.error_code || `HTTP_${res.status}`;
    throw new ApiError(message, res.status, code, errorData?.details);
  }

  try {
    return await res.json();
  } catch (jsonErr) {
    return {} as T;
  }
}
