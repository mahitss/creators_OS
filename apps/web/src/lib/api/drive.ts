export interface DriveFile {
  id: string;
  workspace_id: string;
  external_file_id: string;
  name: string;
  mime_type: string;
  description: string;
  web_url: string;
  owner_name: string;
  size_bytes: number;
  modified_time: string;
}

export interface DriveFileListResponse {
  files: DriveFile[];
  total: number;
}

export interface DriveStatusResponse {
  is_connected: boolean;
  last_synced_at?: string | null;
  file_count: number;
}

export interface DocumentContentResponse {
  file_id: string;
  name: string;
  mime_type: string;
  text: string;
  pages: number;
  truncated: boolean;
}

export interface MissionDocumentReference {
  id: string;
  mission_id: string;
  drive_file_id: string;
  file_name: string;
  mime_type: string;
  web_url: string;
  created_at: string;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export async function fetchDriveStatus(): Promise<DriveStatusResponse> {
  try {
    const res = await fetch(`${API_BASE_URL}/drive/status`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      cache: 'no-store',
    });

    if (!res.ok) return { is_connected: false, file_count: 0 };
    return await res.json();
  } catch (err) {
    return { is_connected: false, file_count: 0 };
  }
}

export async function fetchDriveFiles(searchQuery?: string): Promise<DriveFileListResponse> {
  const query = new URLSearchParams();
  if (searchQuery) query.set('q', searchQuery);

  const res = await fetch(`${API_BASE_URL}/drive/files?${query.toString()}`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
    cache: 'no-store',
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch Drive files (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function fetchDriveFile(id: string): Promise<DriveFile> {
  const res = await fetch(`${API_BASE_URL}/drive/files/${id}`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
    cache: 'no-store',
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch Drive file (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function extractDriveContent(id: string): Promise<DocumentContentResponse> {
  const res = await fetch(`${API_BASE_URL}/drive/files/${id}/content`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to extract document content (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function syncDrive(): Promise<DriveStatusResponse> {
  const res = await fetch(`${API_BASE_URL}/drive/sync`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to sync Drive (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function attachDocumentToMission(missionId: string, fileId: string): Promise<MissionDocumentReference> {
  const res = await fetch(`${API_BASE_URL}/missions/${missionId}/documents/${fileId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error(`Failed to attach document to mission (HTTP ${res.status})`);
  }

  return await res.json();
}

export async function fetchMissionDocuments(missionId: string): Promise<MissionDocumentReference[]> {
  const res = await fetch(`${API_BASE_URL}/missions/${missionId}/documents`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
    cache: 'no-store',
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch mission documents (HTTP ${res.status})`);
  }

  return await res.json();
}
