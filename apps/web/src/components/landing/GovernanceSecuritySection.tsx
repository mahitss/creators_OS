'use client';

import React from 'react';

export function GovernanceSecuritySection() {
  return (
    <section id="security" className="relative py-24 sm:py-28 lg:py-32 bg-[#050505] border-t border-[rgba(255,255,255,0.08)] overflow-hidden">
      <div className="w-full max-w-[1440px] mx-auto px-5 sm:px-8 lg:px-12">
        <div className="max-w-3xl flex flex-col items-start text-left gap-3">
          <div className="inline-flex items-center gap-2 text-xs font-mono text-[#7CF7C5] tracking-widest uppercase">
            <span>[ 05 // ENTERPRISE CONTROL ]</span>
          </div>
          <h2 className="text-3xl sm:text-5xl font-bold text-[#F5F7FA] tracking-tight font-sans leading-tight">
            AUTONOMY <br />
            WITH CONTROL.
          </h2>
          <p className="text-[rgba(245,247,250,0.55)] text-base sm:text-lg font-light leading-relaxed max-w-2xl mt-2">
            Autonomous systems need boundaries. Kinetiq enforces them. Built from the ground up with zero-trust identity, strict multi-tenant isolation, and immutable audit streams.
          </p>
        </div>

        {/* 8 Security & Control Badges */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-10">
          {[
            'Identity (Google OIDC)',
            'Tenant Isolation',
            'Role-Based Access (RBAC)',
            'Attribute Access (ABAC)',
            'PolicyEngine Guardrails',
            'Immutable Audit Logs',
            'DLP Secret Masking',
            'Cryptographic HMAC Sessions',
          ].map((item, idx) => (
            <div
              key={idx}
              className="p-3.5 rounded-xl bg-[#0A0C0F] border border-[rgba(255,255,255,0.08)] flex items-center gap-2.5 text-xs font-mono text-[#F5F7FA]"
            >
              <span className="w-1.5 h-1.5 rounded-full bg-[#7CF7C5]" />
              <span>{item}</span>
            </div>
          ))}
        </div>

        {/* 4 Security Details */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
          <div className="p-7 sm:p-8 rounded-2xl bg-[#0A0C0F] border border-[rgba(255,255,255,0.08)] flex flex-col gap-2.5">
            <div className="flex items-center justify-between">
              <span className="text-[#7CF7C5] font-mono text-xs">P0-01 // SERVER IDENTITY</span>
              <span className="text-[10px] font-mono text-[#7CF7C5] bg-[#7CF7C5]/10 px-2 py-0.5 rounded border border-[#7CF7C5]/20">
                VERIFIED
              </span>
            </div>
            <h3 className="text-xl font-bold text-[#F5F7FA]">Authoritative Session Attestation</h3>
            <p className="text-sm text-[rgba(245,247,250,0.55)] font-light leading-relaxed">
              Google OIDC ID tokens are verified server-side against cryptographic client audiences. Sessions are issued as HttpOnly signed tokens. Client header identity spoofing is rejected globally.
            </p>
          </div>

          <div className="p-7 sm:p-8 rounded-2xl bg-[#0A0C0F] border border-[rgba(255,255,255,0.08)] flex flex-col gap-2.5">
            <div className="flex items-center justify-between">
              <span className="text-[#9BB7FF] font-mono text-xs">P0-02 // TENANT ISOLATION</span>
              <span className="text-[10px] font-mono text-[#7CF7C5] bg-[#7CF7C5]/10 px-2 py-0.5 rounded border border-[#7CF7C5]/20">
                ENFORCED
              </span>
            </div>
            <h3 className="text-xl font-bold text-white">Strict Row & Workspace Boundaries</h3>
            <p className="text-sm text-[rgba(245,247,250,0.55)] font-light leading-relaxed">
              All database queries and agent memory lookups are strictly scoped to the authenticated workspace. Cross-tenant IDOR access attempts fail closed with 403 Forbidden.
            </p>
          </div>

          <div className="p-7 sm:p-8 rounded-2xl bg-[#0A0C0F] border border-[rgba(255,255,255,0.08)] flex flex-col gap-2.5">
            <div className="flex items-center justify-between">
              <span className="text-[#7CF7C5] font-mono text-xs">P0-03 // DATA LOSS PREVENTION</span>
              <span className="text-[10px] font-mono text-[#7CF7C5] bg-[#7CF7C5]/10 px-2 py-0.5 rounded border border-[#7CF7C5]/20">
                ACTIVE
              </span>
            </div>
            <h3 className="text-xl font-bold text-white">Real-Time DLP Secret Redaction</h3>
            <p className="text-sm text-[rgba(245,247,250,0.55)] font-light leading-relaxed">
              API keys, private tokens, and sensitive credentials are dynamically masked and redacted before prompts or outputs traverse external networks.
            </p>
          </div>

          <div className="p-7 sm:p-8 rounded-2xl bg-[#0A0C0F] border border-[rgba(255,255,255,0.08)] flex flex-col gap-2.5">
            <div className="flex items-center justify-between">
              <span className="text-[#9BB7FF] font-mono text-xs">P0-04 // AUDIT COMPLIANCE</span>
              <span className="text-[10px] font-mono text-[#7CF7C5] bg-[#7CF7C5]/10 px-2 py-0.5 rounded border border-[#7CF7C5]/20">
                IMMUTABLE
              </span>
            </div>
            <h3 className="text-xl font-bold text-white">Append-Only Audit Stream</h3>
            <p className="text-sm text-[rgba(245,247,250,0.55)] font-light leading-relaxed">
              Every authentication attempt, policy evaluation, workflow execution, and state mutation records to an immutable append-only audit log with actor ID, IP hash, and timestamp.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
