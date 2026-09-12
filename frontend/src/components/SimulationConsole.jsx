import React from 'react';
import { PlayCircle, CheckCircle, XCircle, AlertTriangle, Terminal } from 'lucide-react';

export default function SimulationConsole({ simulations }) {
  if (!simulations || simulations.length === 0) {
    return (
      <div className="bg-gradient-to-br from-[#111827] via-[#0F172A] to-[#1E293B] border border-gray-800 rounded-2xl p-5 text-center text-gray-500 text-xs font-mono">
        No simulation runs recorded yet.
      </div>
    );
  }

  return (
    <div className="bg-gradient-to-br from-[#111827] via-[#0F172A] to-[#1E293B] border border-emerald-900/40 rounded-2xl p-5 shadow-[0_4px_20px_rgba(0,0,0,0.3)]">
      <div className="flex items-center justify-between mb-4 border-b border-gray-800/80 pb-3.5">
        <div className="flex items-center gap-2.5">
          <div className="p-1.5 bg-emerald-500/10 border border-emerald-500/30 rounded-lg text-emerald-400">
            <PlayCircle className="w-4 h-4" />
          </div>
          <h2 className="font-bold text-gray-100 text-sm tracking-wide">Policy Simulator Execution Console</h2>
        </div>
        <span className="text-xs font-mono text-emerald-400 bg-emerald-950/80 border border-emerald-800/60 px-2.5 py-0.5 rounded-full font-semibold">
          {simulations.length} Simulation Runs Executed
        </span>
      </div>

      <div className="space-y-4">
        {simulations.map((sim, idx) => (
          <div 
            key={idx}
            className={`border rounded-xl p-4 font-mono text-xs transition-all ${
              sim.success 
                ? 'bg-emerald-950/20 border-emerald-800/60 shadow-[0_0_15px_rgba(16,185,129,0.1)]' 
                : 'bg-red-950/20 border-red-800/60 shadow-[0_0_15px_rgba(239,68,68,0.1)]'
            }`}
          >
            {/* Header */}
            <div className="flex items-center justify-between mb-2.5">
              <div className="flex items-center gap-2.5">
                {sim.success ? (
                  <CheckCircle className="w-4.5 h-4.5 text-emerald-400" />
                ) : (
                  <XCircle className="w-4.5 h-4.5 text-red-400" />
                )}
                <span className="font-bold text-gray-100">Policy Version: {sim.policy_version}</span>
                <span className="text-gray-500 text-[10px]">({sim.simulation_id})</span>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-gray-400">Functionality: <strong className={sim.functionality_score === 100 ? 'text-emerald-400' : 'text-red-400'}>{sim.functionality_score}%</strong></span>
                <span className="text-gray-400">Security Score: <strong className="text-cyan-400">{sim.security_score}</strong></span>
              </div>
            </div>

            <p className="text-gray-300 font-sans text-xs mb-2 leading-relaxed">{sim.details}</p>

            {/* Failure Trace Details */}
            {!sim.success && sim.denied_actions && sim.denied_actions.length > 0 && (
              <div className="mt-3.5 pt-2.5 border-t border-red-900/60 space-y-2">
                <span className="text-red-400 font-bold block text-[11px] flex items-center gap-1.5">
                  <AlertTriangle className="w-3.5 h-3.5" /> Denied Workloads Trace Log:
                </span>
                {sim.denied_actions.map((act, aIdx) => (
                  <div key={aIdx} className="bg-[#0B0F19] p-2.5 rounded-lg border border-red-900/60 text-red-300 text-[11px] font-mono shadow-inner">
                    <div>❌ <strong>{act.service}</strong> missing permission <span className="underline font-bold text-red-200">{act.permission}</span> on <span className="underline">{act.resource}</span></div>
                    <div className="text-gray-400 text-[10px] mt-1">{act.error}</div>
                  </div>
                ))}
              </div>
            )}

          </div>
        ))}
      </div>
    </div>
  );
}
