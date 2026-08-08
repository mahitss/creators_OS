export interface ToolParameterSchema {
  type: string;
  description: string;
  properties?: Record<string, ToolParameterSchema>;
  required?: string[];
}

export interface ToolDefinition {
  id: string;
  name: string;
  description: string;
  parameters: ToolParameterSchema;
}

export interface ToolRegistryInterface {
  registerTool(tool: ToolDefinition): void;
  getTool(id: string): ToolDefinition | undefined;
  listTools(): ToolDefinition[];
}
