'use client';

import React, { useState, useEffect } from 'react';
import { AppShell } from '../../../components/shell/AppShell';
import {
  fetchIntegration,
  connectIntegration,
  disconnectIntegration,
  refreshIntegration,
  IntegrationConnection,
} from '../../../lib/api/integrations';
import { Typography, Card, Badge, Button, Spinner, ErrorState } from '@vapor/ui';
import { formatDate } from '@vapor/utils';

export default function IntegrationsSettingsPage() {
  const [googleConn, setGoogleConn] = useState<IntegrationConnection | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);

  const loadIntegrations = async () => {
    setIsLoading(true);
    setIsError(false);
    try {
      const conn = await fetchIntegration('google');
      setGoogleConn(conn);
    } catch (err) {
      console.error('Failed to load Google integration:', err);
      setIsError(true);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadIntegrations();
  }, []);

  const handleConnect = async () => {
    setIsProcessing(true);
    try {
      const res = await connectIntegration('google');
      // Redirect to Google authorization URL or trigger simulated callback for demo
      window.location.href = res.authorization_url;
    } catch (err) {
      console.error('Failed to connect Google integration:', err);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleDisconnect = async () => {
    setIsProcessing(true);
    try {
      await disconnectIntegration('google');
      await loadIntegrations();
    } catch (err) {
      console.error('Failed to disconnect Google integration:', err);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleRefresh = async () => {
    setIsProcessing(true);
    try {
      await refreshIntegration('google');
      await loadIntegrations();
    } catch (err) {
      console.error('Failed to refresh Google token:', err);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <AppShell>
      <div className="max-w-4xl mx-auto w-full flex flex-col gap-6 py-2">
        {/* Header */}
        <div className="flex flex-col gap-0.5">
          <Typography variant="h1">Integrations & Connected Accounts</Typography>
          <Typography variant="caption" className="text-slate-400">
            Securely authorize external service providers for workspace workflows. OAuth tokens are encrypted at rest.
          </Typography>
        </div>

        {/* Content */}
        {isLoading ? (
          <div className="flex flex-col items-center justify-center p-12 gap-3">
            <Spinner size="md" />
            <Typography variant="caption" className="text-slate-500 font-mono">
              Loading workspace connections...
            </Typography>
          </div>
        ) : isError ? (
          <ErrorState
            title="Integrations Error"
            message="Could not retrieve integration connection status."
            onRetry={loadIntegrations}
          />
        ) : (
          <div className="flex flex-col gap-4">
            {/* Google Reference Provider */}
            <Card variant="panel" className="p-5 border-slate-800 flex flex-col gap-4">
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-slate-900 border border-slate-800 flex items-center justify-center text-xl font-bold">
                    🌐
                  </div>
                  <div className="flex flex-col">
                    <div className="flex items-center gap-2">
                      <Typography variant="h3" className="text-base font-semibold text-slate-100">
                        Google Workspace Identity
                      </Typography>
                      {googleConn && googleConn.status === 'connected' ? (
                        <Badge variant="emerald">CONNECTED</Badge>
                      ) : googleConn && googleConn.status === 'expired' ? (
                        <Badge variant="amber">EXPIRED</Badge>
                      ) : (
                        <Badge variant="default">DISCONNECTED</Badge>
                      )}
                    </div>
                    <Typography variant="caption" className="text-xs text-slate-400">
                      OAuth 2.0 authentication for workspace identity validation.
                    </Typography>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex items-center gap-2">
                  {(!googleConn || googleConn.status === 'disconnected') ? (
                    <Button variant="primary" size="sm" onClick={handleConnect} disabled={isProcessing}>
                      {isProcessing ? 'Connecting...' : 'Connect Google'}
                    </Button>
                  ) : googleConn.status === 'connected' ? (
                    <>
                      <Button variant="ghost" size="sm" onClick={handleRefresh} disabled={isProcessing}>
                        Refresh Token
                      </Button>
                      <Button variant="ghost" size="sm" className="text-rose-400 hover:text-rose-300" onClick={handleDisconnect} disabled={isProcessing}>
                        Disconnect
                      </Button>
                    </>
                  ) : (
                    <Button variant="primary" size="sm" onClick={handleConnect} disabled={isProcessing}>
                      Reconnect Google
                    </Button>
                  )}
                </div>
              </div>

              {/* Connected Details */}
              {googleConn && googleConn.status === 'connected' && (
                <div className="pt-3 border-t border-slate-800/60 flex flex-col gap-2 text-xs font-mono text-slate-400">
                  <div className="flex items-center justify-between">
                    <span>Account: {googleConn.external_account_name || 'Alex (Vapor Creator)'}</span>
                    <span>Connected {formatDate(googleConn.connected_at || googleConn.created_at)}</span>
                  </div>
                  <div className="flex items-center gap-2 pt-1 text-[11px] text-slate-500">
                    <span>Authorized Scopes:</span>
                    {googleConn.scopes.map((s) => (
                      <span key={s} className="px-1.5 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-400">
                        {s.split('/').pop()}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </Card>
          </div>
        )}
      </div>
    </AppShell>
  );
}
