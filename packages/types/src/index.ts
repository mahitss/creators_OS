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

export type MissionStatus =
  | 'DRAFT'
  | 'QUEUED'
  | 'PLANNING'
  | 'RUNNING'
  | 'WAITING'
  | 'PAUSED'
  | 'COMPLETED'
  | 'FAILED'
  | 'CANCELLED'
  | 'active'
  | 'completed'
  | 'archived';

export type MissionPriority = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL' | 'low' | 'medium' | 'high' | 'urgent';

export type MissionStepStatus = 'PENDING' | 'RUNNING' | 'COMPLETED' | 'FAILED' | 'SKIPPED' | 'pending' | 'ready' | 'in_progress' | 'completed' | 'failed' | 'skipped';

export type MissionStepType = 'retrieval' | 'analysis' | 'reasoning' | 'generation' | 'action';

export type MissionEventType =
  | 'MISSION_CREATED'
  | 'MISSION_QUEUED'
  | 'MISSION_PLANNING'
  | 'PLAN_CREATED'
  | 'STEP_STARTED'
  | 'STEP_COMPLETED'
  | 'STEP_FAILED'
  | 'MODEL_REQUEST'
  | 'MODEL_RESPONSE'
  | 'MISSION_PAUSED'
  | 'MISSION_RESUMED'
  | 'MISSION_CANCELLED'
  | 'MISSION_COMPLETED'
  | 'MISSION_FAILED';

export interface MissionTokenUsage {
  inputTokens: number;
  outputTokens: number;
  totalTokens: number;
}

export interface Mission {
  id: string;
  workspaceId: string;
  tenantId?: string;
  name: string;
  title: string;
  goal: string;
  description: string;
  status: MissionStatus;
  priority: MissionPriority;
  agentId?: string | null;
  model?: string | null;
  context?: Record<string, unknown>;
  plan?: Record<string, unknown> | null;
  currentStep: number;
  progress: number;
  createdBy: string;
  createdAt: string;
  updatedAt?: string;
  startedAt?: string | null;
  completedAt?: string | null;
  failedAt?: string | null;
  cancelledAt?: string | null;
  error?: Record<string, unknown> | string | null;
  result?: Record<string, unknown> | string | null;
  tokenUsage?: MissionTokenUsage;
  cost?: number;
  metadata?: Record<string, unknown>;
}

export interface MissionStep {
  id: string;
  missionId: string;
  workspaceId?: string;
  stepNumber: number;
  name: string;
  title?: string;
  description: string;
  stepType: MissionStepType;
  status: MissionStepStatus;
  input?: Record<string, unknown>;
  output?: Record<string, unknown> | null;
  error?: Record<string, unknown> | string | null;
  retryCount: number;
  maxRetries: number;
  tokenUsage?: MissionTokenUsage;
  costUsd?: number;
  durationMs?: number;
  startedAt?: string | null;
  completedAt?: string | null;
  createdAt: string;
  updatedAt?: string;
}

export interface MissionEvent {
  id: string;
  missionId: string;
  workspaceId: string;
  stepId?: string | null;
  eventType: MissionEventType;
  timestamp: string;
  payload: Record<string, unknown>;
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

