'use client';

import React from 'react';

export function GovernanceSecuritySection() {
  return (
    <section id="security" className="py-28 bg-[#080A0D] border-t border-slate-900 relative">
      <div className="max-w-7xl mx-auto px-6 sm:px-8">
        <div className="max-w-3xl flex flex-col gap-4">
          <div className="inline-flex items-center gap-2 text-xs font-mono text-cyan-400 tracking-widest uppercase">
            <span>[ 05 // ZERO-TRUST SECURITY ]</span>
          </div>
          <h2 className="text-3xl sm:text-4xl font-bold text-white tracking-tight">
            Cryptographic Isolation & Zero-Trust Defense.
          </h2>
          <p className="text-slate-400 text-base sm:text-lg font-light leading-relaxed">
            Enterprise AI demands uncompromising security. Kinetiq enforces fail-closed authorization boundaries, cryptographic identity verification, and multi-tenant isolation across all 101 API surfaces.
          </p>
        </div>

        {/* 4 Security Pillars Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-16">
          {/* Security Box 1 */}
          <div className="p-8 rounded-2xl bg-[#0B0E12] border border-slate-800/80 flex flex-col gap-3">
            <div className="flex items-center justify-between">
              <span className="text-cyan-400 font-mono text-xs">P0-01 // IDENTITY BOUNDARY</span>
              <span className="text-[10px] font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">VERIFIED</span>
            </div>
            <h3 className="text-xl font-bold text-white">Authoritative Session & Google OIDC</h3>
            <p className="text-sm text-slate-400 font-light leading-relaxed">
              Sessions are cryptographically verified via server-side Google OpenID Connect and issued as HttpOnly, SameSite=Lax signed tokens. Client header identity spoofing is rejected globally.
            </p>
          </div>

          {/* Security Box 2 */}
          <div className="p-8 rounded-2xl bg-[#0B0E12] border border-slate-800/80 flex flex-col gap-3">
            <div className="flex items-center justify-between">
              <span className="text-emerald-400 font-mono text-xs">P0-02 // TENANT ISOLATION</span>
              <span className="text-[10px] font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">ENFORCED</span>
            </div>
            <h3 className="text-xl font-bold text-white">Strict Multi-Tenant Row & Workspace Isolation</h3>
            <p className="text-sm text-slate-400 font-light leading-relaxed">
              Every database query and agent execution is explicitly bound to the authenticated tenant membership. Cross-tenant IDOR access attempts fail closed with 403 Forbidden.
            </p>
          </div>

          {/* Security Box 3 */}
          <div className="p-8 rounded-2xl bg-[#0B0E12] border border-slate-800/80 flex flex-col gap-3">
            <div className="flex items-center justify-between">
              <span className="text-blue-400 font-mono text-xs">P0-03 // NETWORK DEFENSE</span>
              <span className="text-[10px] font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">PROTECTED</span>
            </div>
            <h3 className="text-xl font-bold text-white">CSRF Protection & Strict CORS Matrix</h3>
            <p className="text-sm text-slate-400 font-light leading-relaxed">
              State-changing mutations are verified against explicit origin whitelists. Arbitrary or wildcard origins are rejected with strict enterprise Content Security Policy (CSP).
            </p>
          </div>

          {/* Security Box 4 */}
          <div className="p-8 rounded-2xl bg-[#0B0E12] border border-slate-800/80 flex flex-col gap-3">
            <div className="flex items-center justify-between">
              <span className="text-purple-400 font-mono text-xs">P0-04 // AUDIT IMMUTABILITY</span>
              <span className="text-[10px] font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">IMMUTABLE</span>
            </div>
            <h3 className="text-xl font-bold text-white">Append-Only Audit Logs & PolicyEngine</h3>
            <p className="text-sm text-slate-400 font-light leading-relaxed">
              Every authentication event, policy decision, agent run, and data mutation writes to an immutable append-only audit stream with actor ID, IP hash, and timestamp.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
