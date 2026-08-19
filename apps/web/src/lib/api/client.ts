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
  // In browser, use relative path so Next.js proxy rewrites route seamlessly and preserves cookies
  if (typeof window !== 'undefined') {
    if (process.env.NEXT_PUBLIC_API_URL && process.env.NEXT_PUBLIC_API_URL.startsWith('/')) {
      return process.env.NEXT_PUBLIC_API_URL;
    }
    return '/api/v1';
  }
  // In SSR / server context, connect to internal backend target
  return process.env.API_INTERNAL_URL || (process.env.NODE_ENV === 'production' ? 'http://vapor-api:8000/api/v1' : 'http://127.0.0.1:8000/api/v1');
}

/**
 * Dynamically resolves headers from session context.
 * Relies on HttpOnly session cookies for authoritative identity.
 */
export function getDefaultHeaders(): Record<string, string> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  if (typeof window !== 'undefined') {
    const authToken = window.sessionStorage?.getItem('vapor_auth_token') || 
                      window.localStorage?.getItem('vapor_auth_token');
    if (authToken) {
      headers['Authorization'] = `Bearer ${authToken}`;
    }
  }

  return headers;
}

export interface ApiClientOptions extends RequestInit {
  timeout?: number;
}

export async function apiClient<T = any>(
  endpoint: string,
  options: ApiClientOptions = {}
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

  const timeoutMs = options.timeout || 10000;
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  let res: Response;
  try {
    res = await fetch(url, {
      ...options,
      headers,
      credentials: options.credentials || 'include',
      cache: options.cache || 'no-store',
      signal: options.signal || controller.signal,
    });
  } catch (networkErr: any) {
    if (networkErr?.name === 'AbortError') {
      throw new ApiConnectionError(`Request timed out for ${normalizedEndpoint}. Backend took longer than ${timeoutMs}ms.`);
    }
    console.error(`[API Network Error] ${options.method || 'GET'} ${url}:`, networkErr);
    throw new ApiConnectionError(`Connection failed for ${normalizedEndpoint}. Verify backend is operational.`);
  } finally {
    clearTimeout(timeoutId);
  }

  if (!res.ok) {
    let errorData: any = null;
    try {
      errorData = await res.json();
    } catch {
      // Body not JSON
    }
    const message = errorData?.detail || errorData?.message || `HTTP ${res.status}: ${res.statusText || 'API Request Failed'}`;
    const code = errorData?.error_code || `HTTP_${res.status}`;
    throw new ApiError(message, res.status, code, errorData?.details);
  }

  try {
    return await res.json();
  } catch (jsonErr) {
    return {} as T;
  }
}
