'use client';

import React from 'react';
import { Avatar, Dropdown, DropdownItem } from '@vapor/ui';
import { useTheme } from '../../app/providers';

export interface UserSession {
  name: string;
  email: string;
  avatarUrl?: string | null;
}

interface UserMenuProps {
  user: UserSession;
  onSignOut: () => void;
}

export const UserMenu: React.FC<UserMenuProps> = ({ user, onSignOut }) => {
  const { theme, setTheme } = useTheme();

  const handleThemeToggle = () => {
    if (theme === 'dark') setTheme('light');
    else if (theme === 'light') setTheme('system');
    else setTheme('dark');
  };

  const menuItems: DropdownItem[] = [
    {
      id: 'user-info',
      label: user.email,
      disabled: true,
      onClick: () => {},
    },
    {
      id: 'theme-toggle',
      label: `Theme: ${theme.toUpperCase()}`,
      onClick: handleThemeToggle,
    },
    {
      id: 'account-settings',
      label: 'Workspace Settings',
      onClick: () => {
        window.location.href = '/settings';
      },
    },
    {
      id: 'sign-out',
      label: 'Sign Out',
      danger: true,
      onClick: onSignOut,
    },
  ];

  return (
    <Dropdown
      trigger={
        <button className="flex items-center gap-2 p-1 rounded-full hover:bg-slate-800 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500">
          <Avatar name={user.name} src={user.avatarUrl} size="sm" />
        </button>
      }
      items={menuItems}
      align="right"
    />
  );
};
