export type AIProviderId = 'openai' | 'anthropic' | 'gemini' | 'openrouter';

export interface AIModelOptions {
  model: string;
  temperature?: number;
  maxTokens?: number;
  topP?: number;
  stopSequences?: string[];
}

export interface AISessionCredentials {
  providerId: AIProviderId;
  apiKey: string;
  baseUrl?: string;
  organizationId?: string;
}

export interface AIProviderInterface {
  readonly id: AIProviderId;
  generateCompletion(prompt: string, options: AIModelOptions): Promise<string>;
  generateStream(prompt: string, options: AIModelOptions): AsyncIterable<string>;
}
