export interface TaskNode {
  id: string;
  title: string;
  agentId: string;
  dependencies: string[]; // TaskNode IDs that must complete first
  payload: Record<string, unknown>;
}

export interface DAGManifest {
  id: string;
  workspaceId: string;
  nodes: TaskNode[];
  estimatedCostUsd: number;
}

export interface OrchestratorInterface {
  planDAG(goalDescription: string, workspaceContext: Record<string, unknown>): Promise<DAGManifest>;
  executeDAG(manifest: DAGManifest): AsyncIterable<{ nodeId: string; status: string }>;
}
