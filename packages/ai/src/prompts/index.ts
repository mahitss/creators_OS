export interface VersionedPromptTemplate {
  id: string;
  version: string;
  template: string;
  variableKeys: string[];
}

export interface PromptManagerInterface {
  getTemplate(id: string, version?: string): VersionedPromptTemplate;
  renderPrompt(id: string, variables: Record<string, string>): string;
}
