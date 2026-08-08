export type AgentStatus = 'idle' | 'thinking' | 'executing' | 'verifying' | 'paused' | 'failed';

export interface AgentManifest {
  id: string;
  name: string;
  role: string;
  systemPromptTemplate: string;
  allowedToolIds: string[];
}

export interface AgentExecutionStep {
  stepId: string;
  agentId: string;
  toolCallId?: string;
  inputPayload: Record<string, unknown>;
  outputResult?: Record<string, unknown>;
  durationMs: number;
  status: 'pending' | 'success' | 'failure';
}

export interface AgentInterface {
  readonly manifest: AgentManifest;
  executeStep(stepInput: Record<string, unknown>): Promise<AgentExecutionStep>;
}
