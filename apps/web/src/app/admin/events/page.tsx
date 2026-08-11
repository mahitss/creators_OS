import React from 'react';
import { EventMeshWorkspace } from '@/components/admin/EventMeshWorkspace';

export const metadata = {
  title: 'Enterprise Event Mesh — Vapor OS',
  description: 'Real-Time Intelligence Fabric & Policy-Governed Durable Event Routing'
};

export default function EventMeshPage() {
  return <EventMeshWorkspace />;
}
