import React from 'react';
import { Tabs, Input, Select } from '@vapor/ui';

export interface MissionFilterBarProps {
  activeStatus: string;
  onStatusChange: (status: string) => void;
  activePriority: string;
  onPriorityChange: (priority: string) => void;
  searchQuery: string;
  onSearchChange: (search: string) => void;
}

export const MissionFilterBar: React.FC<MissionFilterBarProps> = ({
  activeStatus,
  onStatusChange,
  activePriority,
  onPriorityChange,
  searchQuery,
  onSearchChange,
}) => {
  const statusTabs = [
    { id: 'all', label: 'All' },
    { id: 'draft', label: 'Draft' },
    { id: 'running', label: 'Running' },
    { id: 'paused', label: 'Paused' },
    { id: 'completed', label: 'Completed' },
    { id: 'failed', label: 'Failed' },
  ];

  const priorityOptions = [
    { label: 'All Priorities', value: 'all' },
    { label: 'Low', value: 'low' },
    { label: 'Medium', value: 'medium' },
    { label: 'High', value: 'high' },
    { label: 'Critical / Urgent', value: 'critical' },
  ];

  return (
    <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 pb-2 border-b border-neutral-800">
      <Tabs tabs={statusTabs} activeTabId={activeStatus} onChange={onStatusChange} />

      <div className="flex items-center gap-2">
        <div className="w-36">
          <Select
            options={priorityOptions}
            value={activePriority}
            onChange={(e) => onPriorityChange(e.target.value)}
          />
        </div>
        <div className="w-48 sm:w-60">
          <Input
            placeholder="Search missions..."
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
          />
        </div>
      </div>
    </div>
  );
};
