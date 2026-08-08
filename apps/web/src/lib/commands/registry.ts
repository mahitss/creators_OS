export interface CommandItem {
  id: string;
  label: string;
  description: string;
  category: 'Navigation' | 'Create' | 'Account' | 'Search';
  shortcut?: string;
  icon: string;
  action: (handlers: {
    router: any;
    openCreateMission?: () => void;
    openCreateContent?: () => void;
    openAddMemory?: () => void;
  }) => void;
}

export const COMMAND_REGISTRY: CommandItem[] = [
  {
    id: 'nav-home',
    label: 'Navigate Home',
    description: 'Go to Executive Brief overview',
    category: 'Navigation',
    shortcut: 'G H',
    icon: '🏛️',
    action: ({ router }) => router.push('/'),
  },
  {
    id: 'nav-attention',
    label: 'Navigate Attention Center',
    description: 'Open workspace actionable inbox',
    category: 'Navigation',
    shortcut: 'G A',
    icon: '🔔',
    action: ({ router }) => router.push('/attention'),
  },
  {
    id: 'nav-missions',
    label: 'Navigate Missions Orchestrator',
    description: 'View active and planned missions',
    category: 'Navigation',
    shortcut: 'G M',
    icon: '⚡',
    action: ({ router }) => router.push('/missions'),
  },
  {
    id: 'nav-content',
    label: 'Navigate Studio Content Canvas',
    description: 'View deliverable articles, scripts and reports',
    category: 'Navigation',
    shortcut: 'G C',
    icon: '🎨',
    action: ({ router }) => router.push('/content'),
  },
  {
    id: 'nav-memory',
    label: 'Navigate Context Vault Memory',
    description: 'View saved workspace preferences and facts',
    category: 'Navigation',
    shortcut: 'G K',
    icon: '🧠',
    action: ({ router }) => router.push('/memory'),
  },
  {
    id: 'create-mission',
    label: 'Create Mission',
    description: 'Orchestrate a new workspace mission',
    category: 'Create',
    shortcut: 'C M',
    icon: '⚡',
    action: ({ openCreateMission, router }) => {
      if (openCreateMission) openCreateMission();
      else router.push('/missions');
    },
  },
  {
    id: 'create-content',
    label: 'Create Content',
    description: 'Create a deliverable article, script or report',
    category: 'Create',
    shortcut: 'C C',
    icon: '🎨',
    action: ({ openCreateContent, router }) => {
      if (openCreateContent) openCreateContent();
      else router.push('/content');
    },
  },
  {
    id: 'add-memory',
    label: 'Add Memory',
    description: 'Teach Vapor workspace context preferences',
    category: 'Create',
    shortcut: 'C K',
    icon: '🧠',
    action: ({ openAddMemory, router }) => {
      if (openAddMemory) openAddMemory();
      else router.push('/memory');
    },
  },
  {
    id: 'sign-out',
    label: 'Sign Out',
    description: 'Sign out of active user session',
    category: 'Account',
    shortcut: 'S O',
    icon: '🚪',
    action: ({ router }) => router.push('/auth/login'),
  },
];
