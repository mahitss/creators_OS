import { apiClient } from './client';

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

export async function fetchDriveStatus(): Promise<DriveStatusResponse> {
  try {
    return await apiClient<DriveStatusResponse>('/drive/status');
  } catch (err) {
    return { is_connected: false, file_count: 0 };
  }
}

export async function fetchDriveFiles(searchQuery?: string): Promise<DriveFileListResponse> {
  const query = new URLSearchParams();
  if (searchQuery) query.set('q', searchQuery);
  const qStr = query.toString();
  return await apiClient<DriveFileListResponse>(`/drive/files${qStr ? `?${qStr}` : ''}`);
}

export async function fetchDriveFile(id: string): Promise<DriveFile> {
  return await apiClient<DriveFile>(`/drive/files/${id}`);
}

export async function extractDriveContent(id: string): Promise<DocumentContentResponse> {
  return await apiClient<DocumentContentResponse>(`/drive/files/${id}/content`);
}

export async function syncDrive(): Promise<DriveStatusResponse> {
  return await apiClient<DriveStatusResponse>('/drive/sync', {
    method: 'POST',
  });
}

export async function attachDocumentToMission(missionId: string, fileId: string): Promise<MissionDocumentReference> {
  return await apiClient<MissionDocumentReference>(`/missions/${missionId}/documents/${fileId}`, {
    method: 'POST',
  });
}

export async function fetchMissionDocuments(missionId: string): Promise<MissionDocumentReference[]> {
  return await apiClient<MissionDocumentReference[]>(`/missions/${missionId}/documents`);
}
