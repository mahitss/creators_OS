import React from 'react';
import Link from 'next/link';

export default function NotFound() {
  return (
    <main className="min-h-screen w-full flex items-center justify-center p-6 bg-[#090A0F] text-slate-100">
      <div className="max-w-lg w-full bg-[#121520] border border-slate-800/80 rounded-2xl p-8 shadow-2xl flex flex-col items-center text-center gap-6">
        <div className="flex items-center justify-center w-16 h-16 rounded-2xl bg-slate-900 border border-slate-700/60 text-emerald-400 font-mono text-2xl font-bold">
          404
        </div>
        
        <div className="flex flex-col gap-2">
          <h1 className="text-xl font-bold text-slate-100 tracking-tight">Resource Not Found</h1>
          <p className="text-sm text-slate-400">
            The requested workspace route or subsystem resource does not exist in this kernel instance.
          </p>
        </div>

        <div className="w-full grid grid-cols-2 gap-2 text-xs font-mono">
          <Link
            href="/"
            className="p-2.5 rounded-lg bg-slate-900/90 border border-slate-800 hover:border-emerald-500/50 hover:bg-slate-800 transition-colors text-slate-300 flex items-center justify-center gap-2"
          >
            <span>🏛️</span> Executive Brief
          </Link>
          <Link
            href="/attention"
            className="p-2.5 rounded-lg bg-slate-900/90 border border-slate-800 hover:border-emerald-500/50 hover:bg-slate-800 transition-colors text-slate-300 flex items-center justify-center gap-2"
          >
            <span>🔔</span> Attention Inbox
          </Link>
          <Link
            href="/missions"
            className="p-2.5 rounded-lg bg-slate-900/90 border border-slate-800 hover:border-emerald-500/50 hover:bg-slate-800 transition-colors text-slate-300 flex items-center justify-center gap-2"
          >
            <span>⚡</span> Missions
          </Link>
          <Link
            href="/work"
            className="p-2.5 rounded-lg bg-slate-900/90 border border-slate-800 hover:border-emerald-500/50 hover:bg-slate-800 transition-colors text-slate-300 flex items-center justify-center gap-2"
          >
            <span>📋</span> Work Queue
          </Link>
        </div>

        <Link
          href="/"
          className="inline-flex items-center justify-center px-5 py-2.5 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold text-sm transition-colors shadow-md"
        >
          Return to Command Center
        </Link>
      </div>
    </main>
  );
}
