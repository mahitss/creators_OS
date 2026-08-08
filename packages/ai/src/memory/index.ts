export interface VectorEmbedding {
  id: string;
  vector: number[];
  payload: Record<string, unknown>;
}

export interface MemorySearchResult {
  id: string;
  score: number;
  content: string;
  metadata: Record<string, unknown>;
}

export interface MemoryStoreInterface {
  upsertEmbedding(embedding: VectorEmbedding): Promise<void>;
  searchMemory(queryVector: number[], topK: number): Promise<MemorySearchResult[]>;
  purgeMemory(id: string): Promise<void>;
}
