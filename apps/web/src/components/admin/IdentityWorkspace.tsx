'use client';

import React, { useState, useEffect } from 'react';
import {
  KeyRound,
  ShieldAlert,
  Globe,
  Users,
  CheckCircle2,
  AlertCircle,
  RefreshCw,
  Cpu,
  Lock,
  ExternalLink,
  Layers,
  FileCheck2
} from 'lucide-react';

interface IdPItem {
  id: string;
  type: string;
  name: string;
  status: string;
  configuration_summary: any;
}

interface DomainItem {
  id: string;
  domain: string;
  status: string;
  verification_token: string;
}

interface GroupMappingItem {
  id: string;
  external_group: string;
  role: string;
  scope: string;
  status: string;
}

interface ServiceAccountItem {
  id: string;
  name: string;
  status: string;
  owner_id: string;
}

export const IdentityWorkspace: React.FC = () => {
  const [providers, setProviders] = useState<IdPItem[]>([]);
  const [domains, setDomains] = useState<DomainItem[]>([]);
  const [mappings, setMappings] = useState<GroupMappingItem[]>([]);
  const [serviceAccounts, setServiceAccounts] = useState<ServiceAccountItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [testResult, setTestResult] = useState<string | null>(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [pRes, dRes, mRes, saRes] = await Promise.all([
        fetch('/api/v1/admin/identity/providers?organizationId=org_default_creator'),
        fetch('/api/v1/admin/identity/domains?organizationId=org_default_creator'),
        fetch('/api/v1/admin/identity/group-mappings?organizationId=org_default_creator'),
        fetch('/api/v1/admin/identity/service-accounts?organizationId=org_default_creator')
      ]);

      if (pRes.ok) setProviders(await pRes.json());
      if (dRes.ok) setDomains(await dRes.json());
      if (mRes.ok) setMappings(await mRes.json());
      if (saRes.ok) setServiceAccounts(await saRes.json());
    } catch (err) {
      console.error('Failed to fetch Identity data', err);
    } finally {
      setLoading(false);
    }
  };

  const handleTestConnection = async (idpId: string) => {
    try {
      const res = await fetch(`/api/v1/admin/identity/providers/${idpId}/test`, { method: 'POST' });
      const data = await res.json();
      setTestResult(`Test Success: ${data.details}`);
    } catch (err) {
      setTestResult('Test Failed');
    }
  };

  return (
    <div className="flex flex-col h-full bg-slate-950 text-slate-100 p-6 space-y-6 overflow-y-auto">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-cyan-500/10 text-cyan-400 rounded-lg border border-cyan-500/20">
            <KeyRound className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-slate-50">Enterprise Identity & SSO Control Plane</h1>
            <p className="text-xs text-slate-400">OIDC, SAML 2.0, SCIM 2.0 provisioning, domain verification, group mapping, & zero-trust machine service accounts</p>
          </div>
        </div>

        <button
          onClick={fetchData}
          className="flex items-center space-x-1.5 px-3 py-1.5 bg-slate-900 border border-slate-700 text-slate-300 hover:text-slate-100 rounded-lg text-xs font-medium transition"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh Identity</span>
        </button>
      </div>

      {testResult && (
        <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-xs text-emerald-300 flex items-center justify-between font-mono">
          <span>{testResult}</span>
          <button onClick={() => setTestResult(null)} className="text-slate-400 hover:text-slate-200">✕</button>
        </div>
      )}

      {/* Main Grid: Identity Providers & Verified Domains */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Identity Providers */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <Lock className="w-4 h-4 text-cyan-400" /> Enterprise Identity Providers (SSO)
          </h2>

          <div className="space-y-3">
            {providers.map((p) => (
              <div key={p.id} className="p-3.5 bg-slate-950/80 border border-slate-800 rounded-xl space-y-2 text-xs">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-cyan-300 font-mono">{p.name} ({p.type.toUpperCase()})</span>
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono">
                    {p.status.toUpperCase()}
                  </span>
                </div>
                <div className="text-[11px] text-slate-400 font-mono">
                  Config: {JSON.stringify(p.configuration_summary)}
                </div>
                <div className="pt-1 flex items-center justify-end">
                  <button
                    onClick={() => handleTestConnection(p.id)}
                    className="px-2.5 py-1 bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 rounded text-[10px] font-medium hover:bg-cyan-500/20"
                  >
                    Test Connection
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Verified Domains & Group Mappings */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <Globe className="w-4 h-4 text-indigo-400" /> Verified Domains & IdP Group Mappings
          </h2>

          <div className="space-y-4">
            <div>
              <div className="text-[11px] font-semibold text-slate-400 uppercase mb-2">Verified Domains</div>
              {domains.map((d) => (
                <div key={d.id} className="p-3 bg-slate-950/80 border border-slate-800 rounded-xl flex items-center justify-between text-xs font-mono">
                  <span className="text-slate-200">{d.domain}</span>
                  <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    {d.status.toUpperCase()}
                  </span>
                </div>
              ))}
            </div>

            <div>
              <div className="text-[11px] font-semibold text-slate-400 uppercase mb-2">IdP Group Mappings</div>
              {mappings.map((m) => (
                <div key={m.id} className="p-3 bg-slate-950/80 border border-slate-800 rounded-xl flex items-center justify-between text-xs">
                  <span className="font-mono text-slate-300">{m.external_group}</span>
                  <span className="font-mono text-indigo-300">→ {m.role}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Machine Identity: Service Accounts & SCIM 2.0 Status */}
      <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4">
        <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
          <Cpu className="w-4 h-4 text-amber-400" /> Service Accounts & SCIM 2.0 Machine Identities
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {serviceAccounts.map((sa) => (
            <div key={sa.id} className="p-3.5 bg-slate-950/80 border border-slate-800 rounded-xl space-y-1.5 text-xs">
              <div className="flex items-center justify-between">
                <span className="font-bold text-amber-300">{sa.name}</span>
                <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono">
                  {sa.status.toUpperCase()}
                </span>
              </div>
              <div className="text-[11px] text-slate-400 font-mono">Owner: {sa.owner_id} | Hashed Token Active</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
