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

// ----------------- AGENT RUNTIME V1 CORE TYPES -----------------

export type AgentStatus = 'DRAFT' | 'ACTIVE' | 'PAUSED' | 'DISABLED' | 'ARCHIVED';

export type AgentRunStatus =
  | 'QUEUED'
  | 'INITIALIZING'
  | 'PLANNING'
  | 'EXECUTING'
  | 'WAITING_TOOL'
  | 'OBSERVING'
  | 'COMPLETED'
  | 'FAILED'
  | 'CANCELLED'
  | 'TIMED_OUT';

export type ToolRiskLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export type AgentActionType = 'RESPOND' | 'TOOL_CALL' | 'WAIT' | 'COMPLETE' | 'FAIL';

export type AgentEventType =
  | 'AGENT_RUN_CREATED'
  | 'AGENT_INITIALIZED'
  | 'CONTEXT_ASSEMBLED'
  | 'MODEL_REQUESTED'
  | 'MODEL_RESPONDED'
  | 'TOOL_REQUESTED'
  | 'TOOL_AUTHORIZED'
  | 'TOOL_DENIED'
  | 'TOOL_EXECUTED'
  | 'OBSERVATION_RECORDED'
  | 'AGENT_STEP_STARTED'
  | 'AGENT_STEP_COMPLETED'
  | 'AGENT_PAUSED'
  | 'AGENT_FAILED'
  | 'AGENT_COMPLETED';

export interface Agent {
  id: string;
  workspaceId: string;
  name: string;
  description: string;
  status: AgentStatus;
  systemInstructions: string;
  capabilities: string[];
  allowedTools: string[];
  allowedModels: string[];
  maxSteps: number;
  maxRuntimeSeconds: number;
  maxTokenBudget: number;
  createdBy: string;
  createdAt: string;
  updatedAt?: string;
  currentVersion?: number;
  latestVersionId?: string;
  total_runs?: number;
  totalRuns?: number;
}

export interface AgentVersion {
  id: string;
  agentId: string;
  workspaceId: string;
  version: number;
  instructions: string;
  capabilities: string[];
  toolPolicy: Record<string, unknown>;
  modelPolicy: Record<string, unknown>;
  limits: {
    maxSteps?: number;
    maxRuntimeSeconds?: number;
    maxTokenBudget?: number;
  };
  createdAt: string;
  createdBy: string;
}

export interface AgentRun {
  id: string;
  agentId: string;
  agentVersionId?: string;
  agent_version_id?: string;
  missionId?: string | null;
  mission_id?: string | null;
  workspaceId: string;
  workspace_id?: string;
  status: AgentRunStatus | string;
  currentStep: number;
  current_step?: number;
  maxSteps?: number;
  max_steps?: number;
  goal?: string;
  finalResult?: string | null;
  final_result?: string | null;
  errorMessage?: string | null;
  error_message?: string | null;
  failureType?: string | null;
  failure_type?: string | null;
  startedAt?: string | null;
  started_at?: string | null;
  completedAt?: string | null;
  completed_at?: string | null;
  durationMs: number;
  duration_ms?: number;
  inputTokens: number;
  input_tokens?: number;
  outputTokens: number;
  output_tokens?: number;
  totalTokens: number;
  total_tokens?: number;
  costUsd: number;
  cost_usd?: number;
  errorInfo?: Record<string, unknown> | string | null;
  resultData?: Record<string, unknown> | string | null;
  createdAt: string;
  created_at?: string;
}

export interface AgentObservation {
  id: string;
  agentRunId: string;
  workspaceId: string;
  stepNumber: number;
  observationType: string;
  toolName?: string | null;
  status: 'success' | 'failed' | 'denied';
  summary: string;
  rawData?: Record<string, unknown>;
  timestamp: string;
}

export interface AgentEvent {
  id: string;
  agentRunId: string;
  workspaceId: string;
  missionId?: string | null;
  eventType: AgentEventType;
  correlationId: string;
  timestamp: string;
  payload: Record<string, unknown>;
}

export type ToolCategory =
  | 'READ'
  | 'SEARCH'
  | 'DATA'
  | 'CONTENT'
  | 'COMMUNICATION'
  | 'WORKFLOW'
  | 'SYSTEM'
  | 'ADMIN';

export interface ToolDefinition {
  id: string;
  name: string;
  description: string;
  version?: number | string;
  category: ToolCategory | string;
  inputSchema?: Record<string, unknown>;
  input_schema?: Record<string, unknown>;
  outputSchema?: Record<string, unknown>;
  output_schema?: Record<string, unknown>;
  requiredPermissions?: string[];
  required_permissions?: string[];
  riskLevel?: ToolRiskLevel | string;
  risk_level?: ToolRiskLevel | string;
  timeoutMs?: number;
  timeout_ms?: number;
  timeoutSeconds?: number;
  timeout_seconds?: number;
  enabled: boolean;
}

export interface AgentToolDiscoveryResponse {
  agentId?: string;
  agent_id?: string;
  workspaceId?: string;
  workspace_id?: string;
  authorizedTools?: ToolDefinition[];
  authorized_tools?: ToolDefinition[];
  deniedTools?: Array<{ tool_id?: string; name: string; reason: string }>;
  denied_tools?: Array<{ tool_id?: string; name: string; reason: string }>;
  totalAuthorized?: number;
  total_authorized?: number;
  totalDenied?: number;
  total_denied?: number;
}

export interface ToolExecutionContext {
  userId: string;
  workspaceId: string;
  tenantId?: string;
  userRole?: string;
  agentId?: string;
  agentVersionId?: string;
  agentRunId?: string;
  missionId?: string;
  requestId?: string;
  traceId?: string;
}

export interface ToolCallAuditLog {
  id: string;
  toolId?: string;
  tool_id?: string;
  toolName?: string;
  tool_name?: string;
  agentRunId?: string | null;
  agent_run_id?: string | null;
  missionId?: string | null;
  mission_id?: string | null;
  workspaceId?: string;
  workspace_id?: string;
  userId?: string;
  user_id?: string;
  timestamp: string;
  authorizationResult?: 'AUTHORIZED' | 'DENIED' | 'APPROVAL_REQUIRED' | string;
  authorization_result?: 'AUTHORIZED' | 'DENIED' | 'APPROVAL_REQUIRED' | string;
  policyResult?: Record<string, unknown>;
  policy_result?: Record<string, unknown>;
  durationMs?: number;
  duration_ms?: number;
  status: 'SUCCESS' | 'FAILED' | 'TIMEOUT' | 'DENIED' | string;
  errorCode?: string | null;
  error_code?: string | null;
  idempotencyKey?: string | null;
  idempotency_key?: string | null;
  truncated?: boolean;
  inputSanitized?: Record<string, unknown>;
  input_sanitized?: Record<string, unknown>;
  outputSanitized?: Record<string, unknown>;
  output_sanitized?: Record<string, unknown>;
  output_summary?: Record<string, unknown>;
}

export type MemoryType = 'EPISODIC' | 'SEMANTIC' | 'PROCEDURAL' | 'WORKING';

export interface MemoryProvenance {
  sourceType?: string;
  source_type?: string;
  sourceId?: string | null;
  source_id?: string | null;
  createdBy?: string;
  created_by?: string;
  confidence?: number;
  timestamp?: string;
}

export interface MemoryRecord {
  id: string;
  workspaceId?: string;
  workspace_id?: string;
  type: MemoryType | string;
  title: string;
  content: string;
  sourceType?: string;
  source_type?: string;
  sourceId?: string | null;
  source_id?: string | null;
  importance?: 'low' | 'medium' | 'high' | 'critical' | string;
  confidence?: number;
  isArchived?: boolean;
  is_archived?: boolean;
  createdAt?: string;
  created_at?: string;
  updatedAt?: string;
  updated_at?: string;
  provenance?: MemoryProvenance;
  metadata?: Record<string, unknown>;
}

export interface CitationItem {
  sourceType?: 'document' | 'knowledge' | 'memory' | 'mission_step' | string;
  source_type?: 'document' | 'knowledge' | 'memory' | 'mission_step' | string;
  sourceId?: string;
  source_id?: string;
  title: string;
  snippet?: string;
  workspaceId?: string;
  workspace_id?: string;
  confidence?: number;
}

export interface ContextSnapshot {
  id: string;
  agentRunId?: string;
  agent_run_id?: string;
  workspaceId?: string;
  workspace_id?: string;
  sources?: Array<{ type: string; id: string; title?: string }>;
  memoryIds?: string[];
  memory_ids?: string[];
  knowledgeIds?: string[];
  knowledge_ids?: string[];
  documentIds?: string[];
  document_ids?: string[];
  policyVersion?: string;
  policy_version?: string;
  agentVersionId?: string | null;
  agent_version_id?: string | null;
  tokenBudget?: number;
  token_budget?: number;
  estimatedTokens?: number;
  estimated_tokens?: number;
  createdAt?: string;
  created_at?: string;
}

export interface ContextPreview {
  sections: Array<{
    name: string;
    content: string;
    estimatedTokens?: number;
    estimated_tokens?: number;
    isUntrusted?: boolean;
    is_untrusted?: boolean;
  }>;
  totalEstimatedTokens?: number;
  total_estimated_tokens?: number;
  tokenCeiling?: number;
  token_ceiling?: number;
  isBudgetExceeded?: boolean;
  is_budget_exceeded?: boolean;
  citations: CitationItem[];
  sources?: Array<{ type: string; id: string; title?: string }>;
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

