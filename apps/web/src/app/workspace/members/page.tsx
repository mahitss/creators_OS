'use client';

import React from 'react';
import { WorkspaceMembers } from '@/components/workspace/WorkspaceMembers';

export default function WorkspaceMembersPage() {
  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100">
      <WorkspaceMembers />
    </div>
  );
}
