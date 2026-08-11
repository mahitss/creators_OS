import React from 'react';
import { GlobalOperationsWorkspace } from '@/components/admin/GlobalOperationsWorkspace';

export const metadata = {
  title: 'Global Operations Center — Vapor OS',
  description: 'Enterprise Control Plane & Evidence-Backed Operational Control'
};

export default function OperationsPage() {
  return <GlobalOperationsWorkspace />;
}
