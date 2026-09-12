import React from 'react';
import { ShieldAlert, Lock, CheckCircle2, XCircle } from 'lucide-react';

const RISK_BADGES = {
  low: 'bg-emerald-950/80 border-emerald-700/80 text-emerald-300 shadow-[0_0_8px_rgba(16,185,129,0.2)]',
  medium: 'bg-blue-950/80 border-blue-700/80 text-blue-300 shadow-[0_0_8px_rgba(59,130,246,0.2)]',
  high: 'bg-amber-950/80 border-amber-700/80 text-amber-300 shadow-[0_0_8px_rgba(245,158,11,0.2)]',
  critical: 'bg-red-950/80 border-red-700/80 text-red-300 shadow-[0_0_8px_rgba(239,68,68,0.2)]',
};

export default function PolicyMatrix({ roleDetails, evidenceList, state }) {
  const perms = roleDetails?.permission_details || [];
  const initialPerms = state?.initial_permissions || [];
  const currentPerms = state?.current_permissions || [];

  const evidenceMap = {};
  if (evidenceList) {
    evidenceList.forEach(e => {
      evidenceMap[e.permission_id] = e;
    });
  }

  return (
    <div className="bg-gradient-to-br from-[#111827] via-[#0F172A] to-[#1E293B] border border-purple-900/40 rounded-2xl p-5 shadow-[0_4px_20px_rgba(0,0,0,0.3)]">
      <div className="flex items-center justify-between mb-4 border-b border-gray-800/80 pb-3.5">
        <div className="flex items-center gap-2.5">
          <div className="p-1.5 bg-purple-500/10 border border-purple-500/30 rounded-lg text-purple-400">
            <Lock className="w-4 h-4" />
          </div>
          <h2 className="font-bold text-gray-100 text-sm tracking-wide">IAM Policy Permission Matrix (Developer Role)</h2>
        </div>
        <div className="flex items-center gap-4 text-xs font-mono">
          <span className="text-gray-400">Baseline: <strong className="text-gray-200">{initialPerms.length}</strong></span>
          <span className="text-gray-400">Final Privilege: <strong className="text-purple-400">{currentPerms.length}</strong></span>
        </div>
      </div>

      <div className="overflow-x-auto rounded-xl border border-gray-800/80">
        <table className="w-full text-left text-xs">
          <thead className="bg-[#0B0F19] text-gray-400 uppercase font-mono border-b border-gray-800">
            <tr>
              <th className="py-3 px-3.5">Permission</th>
              <th className="py-3 px-3.5">Resource & Action</th>
              <th className="py-3 px-3.5">Risk</th>
              <th className="py-3 px-3.5">90-Day Access Logs</th>
              <th className="py-3 px-3.5">Dependencies</th>
              <th className="py-3 px-3.5">Agent Decision</th>
              <th className="py-3 px-3.5">Evidence & Rationale</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-800/60 font-sans">
            {perms.map((item, idx) => {
              const p = item.permission;
              const usage = item.usage || {};
              const impact = item.dependency_impact || {};
              const ev = evidenceMap[p.id];

              const wasInitial = initialPerms.includes(p.id);
              const isCurrent = currentPerms.includes(p.id);

              let statusBadge = null;
              if (wasInitial && !isCurrent) {
                statusBadge = (
                  <span className="inline-flex items-center gap-1 bg-red-950/80 border border-red-800 text-red-400 px-2.5 py-0.5 rounded-full font-mono font-bold text-[10px] shadow-[0_0_8px_rgba(239,68,68,0.3)]">
                    <XCircle className="w-3 h-3" /> REMOVED
                  </span>
                );
              } else if (ev?.decision === 'preserved') {
                statusBadge = (
                  <span className="inline-flex items-center gap-1 bg-amber-950/80 border border-amber-700 text-amber-300 px-2.5 py-0.5 rounded-full font-mono font-bold text-[10px] shadow-[0_0_8px_rgba(245,158,11,0.3)]">
                    <ShieldAlert className="w-3 h-3" /> PRESERVED (DEPENDENCY)
                  </span>
                );
              } else {
                statusBadge = (
                  <span className="inline-flex items-center gap-1 bg-emerald-950/80 border border-emerald-700 text-emerald-400 px-2.5 py-0.5 rounded-full font-mono font-bold text-[10px] shadow-[0_0_8px_rgba(16,185,129,0.3)]">
                    <CheckCircle2 className="w-3 h-3" /> RETAINED
                  </span>
                );
              }

              return (
                <tr key={idx} className="hover:bg-gray-800/40 transition">
                  {/* Permission ID */}
                  <td className="py-3.5 px-3.5 font-mono font-bold text-gray-100">
                    {p.id}
                  </td>

                  {/* Resource & Action */}
                  <td className="py-3.5 px-3.5 text-gray-300">
                    <span className="text-cyan-300 font-mono font-medium">{p.resource}</span> ({p.action})
                  </td>

                  {/* Risk Level */}
                  <td className="py-3.5 px-3.5 font-mono">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-extrabold uppercase border ${RISK_BADGES[p.risk_level]}`}>
                      {p.risk_level}
                    </span>
                  </td>

                  {/* Access Logs */}
                  <td className="py-3.5 px-3.5 text-gray-300 font-mono">
                    <div>Direct User: <strong className="text-white">{usage.direct_calls || 0}</strong></div>
                    <div className="text-[11px] text-gray-400">Service: {usage.service_calls || 0}</div>
                  </td>

                  {/* Dependencies */}
                  <td className="py-3.5 px-3.5">
                    {impact.has_dependencies ? (
                      <span className="text-amber-300 font-mono text-[10px] font-semibold bg-amber-950/60 border border-amber-700/60 px-2.5 py-0.5 rounded-full inline-block">
                        ⚠️ {impact.affected_services.join(', ')}
                      </span>
                    ) : (
                      <span className="text-gray-500 font-mono text-[11px]">None</span>
                    )}
                  </td>

                  {/* Agent Decision */}
                  <td className="py-3.5 px-3.5">
                    {statusBadge}
                  </td>

                  {/* Rationale */}
                  <td className="py-3.5 px-3.5 text-gray-300 leading-tight text-[11px]">
                    {ev?.explanation || p.description}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
