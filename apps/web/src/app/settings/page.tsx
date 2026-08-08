import React from 'react';
import { AppShell } from '../../components/shell/AppShell';
import { Card, Typography, Switch } from '@vapor/ui';

export default function SettingsPage() {
  return (
    <AppShell>
      <div className="max-w-2xl mx-auto w-full flex flex-col gap-6 py-4">
        <div>
          <Typography variant="h2">System Settings</Typography>
          <Typography variant="caption" className="text-slate-400">
            Configure system governance, resource caps, and key vault.
          </Typography>
        </div>

        <Card variant="panel" className="flex flex-col gap-4">
          <Typography variant="h3">System Preferences</Typography>
          <div className="flex items-center justify-between py-2 border-b border-slate-800/80">
            <div>
              <Typography variant="body" className="font-medium text-slate-200">
                Sub-100ms Reduced Motion
              </Typography>
              <Typography variant="caption" className="text-slate-400">
                Disable UI transition animations across workspaces.
              </Typography>
            </div>
            <Switch checked={false} onChange={() => {}} />
          </div>

          <div className="flex items-center justify-between py-2">
            <div>
              <Typography variant="body" className="font-medium text-slate-200">
                Proactive Executive Briefings
              </Typography>
              <Typography variant="caption" className="text-slate-400">
                Allow Executive AI to observe workspace events in the background.
              </Typography>
            </div>
            <Switch checked={true} onChange={() => {}} />
          </div>
        </Card>
      </div>
    </AppShell>
  );
}
