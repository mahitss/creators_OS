export type Role = 'OWNER' | 'MEMBER' | 'READONLY';

export interface User {
  id: string;
  email: string;
  name: string | null;
  avatarUrl: string | null;
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
