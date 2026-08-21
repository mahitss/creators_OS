import React, { useState } from 'react';
import { Dialog, Input, Textarea, Select, Button } from '@vapor/ui';
import { createMission, Mission } from '../../lib/api/missions';

export interface CreateMissionDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: (newMission: Mission) => void;
}

const AVAILABLE_AGENTS = [
  { label: 'Executive Autonomous Agent (Default)', value: 'ag_executive_core' },
  { label: 'Autonomous Research Analyst', value: 'ag_research_analyst' },
  { label: 'Infrastructure & DevOps Engineer', value: 'ag_infra_devops' },
  { label: 'Security & Compliance Auditor', value: 'ag_security_auditor' },
  { label: 'Full-Stack Software Engineer', value: 'ag_software_engineer' },
];

const AVAILABLE_MODELS = [
  { label: 'OpenRouter Auto Pool (openrouter/free)', value: 'openrouter/free' },
  { label: 'NVIDIA Nemotron 3 Ultra 550B', value: 'nvidia/nemotron-3-ultra-550b-a55b:free' },
  { label: 'DeepSeek R1 Reasoning', value: 'deepseek/deepseek-r1:free' },
  { label: 'Meta Llama 3.3 70B Instruct', value: 'meta-llama/llama-3.3-70b-instruct:free' },
  { label: 'Qwen 2.5 Coder 32B Instruct', value: 'qwen/qwen-2.5-coder-32b-instruct:free' },
  { label: 'Cohere North Mini Code', value: 'cohere/north-mini-code:free' },
];

export const CreateMissionDialog: React.FC<CreateMissionDialogProps> = ({
  isOpen,
  onClose,
  onSuccess,
}) => {
  const [name, setName] = useState('');
  const [goal, setGoal] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<string>('medium');
  const [agentId, setAgentId] = useState<string>('ag_executive_core');
  const [model, setModel] = useState<string>('openrouter/free');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) {
      setError('Mission name is required.');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const created = await createMission({
        name: name.trim(),
        title: name.trim(),
        goal: goal.trim() || name.trim(),
        description: description.trim(),
        priority: priority.toUpperCase(),
        agentId: agentId,
        model: model,
        context: {
          runtime_target: 'kinetiq_kernel_v1',
          created_via: 'web_console',
        },
      });
      setName('');
      setGoal('');
      setDescription('');
      setPriority('medium');
      onSuccess(created);
      onClose();
    } catch (err: any) {
      setError(err?.message || 'Failed to create mission.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Dialog
      isOpen={isOpen}
      onClose={onClose}
      title="Create Autonomous Mission"
      description="Initialize a new mission in DRAFT state for autonomous planning and worker execution."
    >
      <form onSubmit={handleSubmit} className="flex flex-col gap-4 mt-2">
        <Input
          label="Mission Name"
          placeholder="e.g. Q3 Architecture Security & Boundary Audit"
          value={name}
          onChange={(e) => {
            setName(e.target.value);
            if (error) setError('');
          }}
          error={error}
          autoFocus
          required
        />

        <Input
          label="Goal / Primary Objective"
          placeholder="e.g. Audit all API endpoints, classify vulnerabilities, and produce verification report"
          value={goal}
          onChange={(e) => setGoal(e.target.value)}
        />

        <Textarea
          label="Context & Execution Directives"
          placeholder="Provide specific parameters, target repositories, boundary conditions, or constraints..."
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={3}
        />

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <Select
            label="Priority Level"
            value={priority}
            onChange={(e) => setPriority(e.target.value)}
            options={[
              { label: 'Low Priority', value: 'low' },
              { label: 'Medium Priority', value: 'medium' },
              { label: 'High Priority', value: 'high' },
              { label: 'Critical / Urgent', value: 'critical' },
            ]}
          />

          <Select
            label="Autonomous Agent"
            value={agentId}
            onChange={(e) => setAgentId(e.target.value)}
            options={AVAILABLE_AGENTS}
          />

          <Select
            label="Execution Model"
            value={model}
            onChange={(e) => setModel(e.target.value)}
            options={AVAILABLE_MODELS}
          />
        </div>

        <div className="flex items-center justify-end gap-2 pt-3 border-t border-neutral-800">
          <Button type="button" variant="ghost" onClick={onClose} disabled={isLoading}>
            Cancel
          </Button>
          <Button type="submit" variant="primary" isLoading={isLoading}>
            Initialize Mission
          </Button>
        </div>
      </form>
    </Dialog>
  );
};
