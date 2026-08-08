export interface AIStreamChunk {
  delta: string;
  isComplete: boolean;
  finishReason?: 'stop' | 'length' | 'tool_call' | 'error';
  metadata?: Record<string, unknown>;
}

export interface StreamHandlerInterface {
  processStream(stream: AsyncIterable<string>): AsyncIterable<AIStreamChunk>;
}
