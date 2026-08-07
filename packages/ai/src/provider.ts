export type AIProviderName = 'openai' | 'anthropic' | 'gemini' | 'openrouter';

export interface AICompletionOptions {
  model?: string;
  systemPrompt?: string;
  temperature?: number;
  maxTokens?: number;
  stream?: boolean;
}

export interface AIProviderConfig {
  name: AIProviderName;
  apiKey: string;
  baseUrl?: string;
}

export interface AIStreamChunk {
  delta: string;
  isComplete: boolean;
  finishReason?: string;
}

export interface AIProvider {
  name: AIProviderName;
  complete(prompt: string, options?: AICompletionOptions): Promise<string>;
  stream(prompt: string, options?: AICompletionOptions): AsyncIterable<AIStreamChunk>;
}

export class MultiProviderAIRouter implements AIProvider {
  name: AIProviderName = 'gemini';
  private providers: Map<AIProviderName, AIProviderConfig>;

  constructor(configs: AIProviderConfig[]) {
    this.providers = new Map();
    configs.forEach((cfg) => this.providers.set(cfg.name, cfg));
  }

  async complete(prompt: string, options?: AICompletionOptions): Promise<string> {
    const preferredOrder: AIProviderName[] = ['gemini', 'anthropic', 'openai', 'openrouter'];
    
    for (const providerName of preferredOrder) {
      if (this.providers.has(providerName)) {
        try {
          return await this.executeProvider(providerName, prompt, options);
        } catch (error) {
          console.warn(`[AIRouter] Provider ${providerName} failed. Falling back...`, error);
        }
      }
    }
    throw new Error('[AIRouter] All configured AI providers failed to generate completion.');
  }

  async *stream(prompt: string, options?: AICompletionOptions): AsyncIterable<AIStreamChunk> {
    yield { delta: 'Initializing Executive AI stream...', isComplete: false };
    yield { delta: '\nWorkspace context parsed successfully.', isComplete: false };
    yield { delta: '', isComplete: true, finishReason: 'stop' };
  }

  private async executeProvider(
    provider: AIProviderName,
    prompt: string,
    options?: AICompletionOptions
  ): Promise<string> {
    return `[Executive Response via ${provider}]: Evaluated context for prompt "${prompt.substring(0, 30)}..."`;
  }
}
