import React, { useState, useEffect } from 'react';
import { Users, UserPlus, Shield, UserX, AlertCircle, CheckCircle2, Mail, Lock } from 'lucide-react';

interface Member {
  id: string;
  workspace_id: string;
  user_id: string;
  email: string;
  role: string;
  status: string;
  joined_at: string;
}

export const WorkspaceMembers: React.FC = () => {
  const [members, setMembers] = useState<Member[]>([]);
  const [inviteEmail, setInviteEmail] = useState('');
  const [inviteRole, setInviteRole] = useState('member');
  const [showInviteModal, setShowInviteModal] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [workspaceId, setWorkspaceId] = useState<string>('');

  const fetchMembers = React.useCallback(async (wsId?: string) => {
    const targetWs = wsId || workspaceId;
    if (!targetWs) return;
    try {
      const res = await fetch(`/api/v1/workspaces/${targetWs}/members`, {
        credentials: 'include'
      });
      if (res.ok) {
        setMembers(await res.json());
      }
    } catch (err) {
      console.error("Failed to fetch workspace members:", err);
    }
  }, [workspaceId]);

  useEffect(() => {
    async function init() {
      try {
        const meRes = await fetch('/api/v1/auth/me', { credentials: 'include' });
        if (meRes.ok) {
          const meData = await meRes.json();
          if (meData?.workspace_id) {
            setWorkspaceId(meData.workspace_id);
            fetchMembers(meData.workspace_id);
          }
        }
      } catch {
        // quiet
      }
    }
    init();
  }, [fetchMembers]);

  const handleInvite = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!workspaceId) return;
    setError(null);
    try {
      const res = await fetch(`/api/v1/workspaces/${workspaceId}/invitations`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ email: inviteEmail, role: inviteRole })
      });
      if (res.ok) {
        setInviteEmail('');
        setShowInviteModal(false);
        fetchMembers();
      } else {
        const data = await res.json();
        setError(data.detail || "Failed to invite member.");
      }
    } catch (err) {
      setError("Network error while inviting member.");
    }
  };

  const handleRoleChange = async (userId: string, newRole: string) => {
    if (!workspaceId) return;
    setError(null);
    try {
      const res = await fetch(`/api/v1/workspaces/${workspaceId}/members/${userId}/role`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ role: newRole })
      });
      if (res.ok) {
        fetchMembers();
      } else {
        const data = await res.json();
        setError(data.detail || "Failed to update role.");
      }
    } catch (err) {
      setError("Error updating role.");
    }
  };

  const handleSuspend = async (userId: string) => {
    if (!workspaceId) return;
    setError(null);
    try {
      const res = await fetch(`/api/v1/workspaces/${workspaceId}/members/${userId}/suspend`, {
        method: 'POST',
        credentials: 'include'
      });
      if (res.ok) {
        fetchMembers();
      } else {
        const data = await res.json();
        setError(data.detail || "Failed to suspend member.");
      }
    } catch (err) {
      setError("Error suspending member.");
    }
  };

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-8 text-zinc-100">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-zinc-800 pb-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
            <Users className="w-8 h-8 text-indigo-400" />
            Workspace & Team Members
          </h1>
          <p className="text-zinc-400 mt-1">
            Manage workspace roles, permissions, invitations, and member suspension status.
          </p>
        </div>

        <button
          onClick={() => setShowInviteModal(true)}
          className="flex items-center gap-2 px-4 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm rounded-xl transition-all shadow-lg shadow-indigo-600/20"
        >
          <UserPlus className="w-4 h-4" /> Invite Team Member
        </button>
      </div>

      {error && (
        <div className="p-4 bg-rose-500/10 border border-rose-500/30 rounded-xl text-rose-400 text-sm flex items-center gap-2">
          <AlertCircle className="w-5 h-5 flex-shrink-0" /> {error}
        </div>
      )}

      {/* Invite Modal */}
      {showInviteModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-zinc-900 border border-zinc-800 rounded-2xl max-w-md w-full p-6 space-y-4 shadow-2xl">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Mail className="w-5 h-5 text-indigo-400" /> Invite Team Member
            </h2>
            <form onSubmit={handleInvite} className="space-y-4">
              <div>
                <label className="text-xs text-zinc-400 font-medium">Email Address</label>
                <input
                  type="email"
                  required
                  placeholder="colleague@company.com"
                  value={inviteEmail}
                  onChange={e => setInviteEmail(e.target.value)}
                  className="w-full mt-1 px-3.5 py-2 bg-zinc-950 border border-zinc-800 rounded-xl text-sm text-zinc-100 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="text-xs text-zinc-400 font-medium">Workspace Role</label>
                <select
                  value={inviteRole}
                  onChange={e => setInviteRole(e.target.value)}
                  className="w-full mt-1 px-3.5 py-2 bg-zinc-950 border border-zinc-800 rounded-xl text-sm text-zinc-100 focus:outline-none focus:border-indigo-500"
                >
                  <option value="owner">Owner (Full Administration)</option>
                  <option value="admin">Admin (Manage Members & Settings)</option>
                  <option value="member">Member (Create Missions & Use Agents)</option>
                  <option value="viewer">Viewer (Read-Only Access)</option>
                </select>
              </div>

              <div className="flex items-center justify-end gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setShowInviteModal(false)}
                  className="px-4 py-2 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 rounded-xl text-xs font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-xs font-semibold transition-all"
                >
                  Send Invitation
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Members Table */}
      <div className="bg-zinc-900/60 border border-zinc-800 rounded-xl overflow-hidden shadow-xl">
        <div className="divide-y divide-zinc-800/60">
          {members.map(m => (
            <div key={m.id} className="p-4 flex items-center justify-between hover:bg-zinc-800/30 transition-colors text-sm">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="font-semibold text-white">{m.email}</span>
                  <span className={`px-2 py-0.5 text-xs font-semibold rounded capitalize ${
                    m.role === 'owner' ? 'bg-purple-500/20 text-purple-300 border border-purple-500/30' :
                    m.role === 'admin' ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30' :
                    m.role === 'member' ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' :
                    'bg-zinc-800 text-zinc-400'
                  }`}>
                    {m.role}
                  </span>
                  <span className={`px-2 py-0.5 text-xs font-semibold rounded capitalize ${
                    m.status === 'active' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-rose-500/20 text-rose-400'
                  }`}>
                    {m.status}
                  </span>
                </div>
                <div className="text-xs text-zinc-500 font-mono">User ID: {m.user_id}</div>
              </div>

              <div className="flex items-center gap-3">
                <select
                  value={m.role}
                  onChange={e => handleRoleChange(m.user_id, e.target.value)}
                  className="px-3 py-1.5 bg-zinc-950 border border-zinc-800 rounded-lg text-xs text-zinc-300 focus:outline-none focus:border-indigo-500"
                >
                  <option value="owner">Owner</option>
                  <option value="admin">Admin</option>
                  <option value="member">Member</option>
                  <option value="viewer">Viewer</option>
                </select>

                {m.status === 'active' && (
                  <button
                    onClick={() => handleSuspend(m.user_id)}
                    className="px-3 py-1.5 bg-rose-500/20 text-rose-300 hover:bg-rose-500/30 border border-rose-500/30 rounded-lg text-xs font-medium transition-all"
                  >
                    Suspend
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
