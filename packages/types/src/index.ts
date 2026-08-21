export type Role = 'OWNER' | 'ADMIN' | 'OPERATOR' | 'ANALYST' | 'VIEWER' | 'MEMBER' | 'READONLY';

export type PermissionAction = 'READ' | 'CREATE' | 'UPDATE' | 'DELETE' | 'EXECUTE' | 'ADMINISTER';

export interface User {
  id: string;
  email: string;
  name: string | null;
  avatarUrl: string | null;
  role?: Role;
  createdAt: string;
  updatedAt: string;
}

export interface Organization {
  id: string;
  name: string;
  slug: string;
  ownerId: string;
  createdAt: string;
}

export interface Workspace {
  id: string;
  orgId: string;
  name: string;
  rootPath: string;
  settings: Record<string, unknown>;
  createdAt: string;
}

export interface Session {
  id: string;
  userId: string;
  token: string;
  expiresAt: string;
}

export interface SystemHealth {
  status: 'healthy' | 'degraded' | 'unhealthy';
  version: string;
  database: boolean;
  redis: boolean;
  timestamp: string;
}

export type RiskLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export interface Proposal {
  id: string;
  title: string;
  description: string;
  riskLevel: RiskLevel;
  blastRadius: string[];
  estimatedCostUsd: number;
  estimatedDurationSec: number;
  verificationCommand: string;
  actions: string[];
  createdAt: string;
}

export interface Agent {
  id: string;
  workspaceId: string;
  name: string;
  role: string;
  status: 'IDLE' | 'ACTIVE' | 'BUSY' | 'ERROR' | 'OFFLINE';
  capabilities: string[];
  allowedTools: string[];
  createdAt: string;
}

export interface Mission {
  id: string;
  workspaceId: string;
  title: string;
  description: string;
  status: 'PENDING' | 'PLANNING' | 'RUNNING' | 'WAITING' | 'COMPLETED' | 'FAILED' | 'CANCELLED' | 'TIMED_OUT' | 'active' | 'completed' | 'paused' | 'failed';
  priority: 'low' | 'medium' | 'high' | 'critical';
  createdBy: string;
  createdAt: string;
  completedAt?: string | null;
}

export interface Workflow {
  id: string;
  workspaceId: string;
  name: string;
  status: 'ACTIVE' | 'PAUSED' | 'ARCHIVED';
  triggerType: string;
  stepsCount: number;
  createdAt: string;
}

export interface Model {
  id: string;
  name: string;
  provider: string;
  category: 'FAST' | 'REASONING' | 'CODE' | 'VISION';
  contextWindow: number;
  costPer1kInputUsd: number;
  costPer1kOutputUsd: number;
  isAvailable: boolean;
}

export interface ModelRequest {
  id: string;
  model: string;
  promptLength: number;
  latencyMs: number;
  status: 'SUCCESS' | 'FALLBACK' | 'ERROR';
  costUsd: number;
  timestamp: string;
}

export interface TelemetryEvent {
  id: string;
  traceId: string;
  tenantId: string;
  workspaceId: string;
  service: string;
  operation: string;
  durationMs: number;
  status: 'OK' | 'ERROR' | 'TIMEOUT';
  timestamp: string;
}

export interface AuditEvent {
  id: string;
  actorId: string;
  tenantId: string;
  workspaceId: string;
  action: PermissionAction;
  resource: string;
  status: 'ALLOWED' | 'DENIED';
  timestamp: string;
  details?: Record<string, unknown>;
}

